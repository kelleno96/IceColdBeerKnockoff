import pygame
import math
import random
import numpy as np


pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Rolling Ball on Incline')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Font
font = pygame.font.SysFont("arialunicode", 36)

ball_radius = 15

# Line properties
left_y = screen_height - ball_radius
right_y = left_y
line_x1 = 100
line_x2 = 700

# Ball properties

initial_ball_x = (line_x1 + line_x2) // 2
initial_ball_y = screen_height - 2 * ball_radius
initial_line_x1 = line_x1
initial_line_x2 = line_x2
initial_line_y = left_y
ball_speed_x = (line_x2 + line_x1) / 2
gravity = 1

# Control speed
control_speed = 3

def setHoleProperties():
    # Hole properties
    holes = []
    for _ in range(5):
        hole_x = random.randint(line_x1 + 50, line_x2 - 50)
        hole_y = random.randint(2*ball_radius, screen_height * 2 / 3)
        hole_radius = random.randint(20, 30)
        holes.append((hole_x, hole_y, hole_radius, red))

    # Goal hole
    goal_x = random.randint(line_x1 + 50, line_x2 - 50)
    goal_y = random.randint(2*ball_radius, screen_height * 2 / 3)
    goal_radius = 25
    holes.append((goal_x, goal_y, goal_radius, green))

    return holes

holes = setHoleProperties()

# Frame rate control
clock = pygame.time.Clock()
FPS = 60

# Score counters
goal_score = 0
fail_score = 0

running = True
ball_x = initial_ball_x
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        left_y -= control_speed
    if keys[pygame.K_s]:
        left_y += control_speed
    if keys[pygame.K_i]:
        right_y -= control_speed
    if keys[pygame.K_k]:
        right_y += control_speed
    if keys[pygame.K_q]:
        break

    left_y = np.clip(left_y, 0, screen_height)
    right_y = np.clip(right_y, 0, screen_height)

    # Calculate line slope
    dx = line_x2 - line_x1
    dy = right_y - left_y
    slope = float(dy) / float(dx)
    angle = math.atan(slope)

    # Exponentially decelerate if slope is small
    if abs(slope) < 0.002:
        ball_speed_x /= 1.2
    else:
        ball_speed_x += gravity * math.sin(angle)

    # Update ball position
    ball_x += ball_speed_x
    ball_y = left_y + (ball_x - line_x1) * slope

    # Check for collisions with holes
    for hole in holes:
        hole_x, hole_y, hole_radius, color = hole
        distance = math.hypot(ball_x - hole_x, ball_y - hole_y)
        if distance < hole_radius:
            if color == green:
                goal_score += 1
                print(f"Goal Score: {goal_score}")
            else:
                goal_score-=1

            # Reset ball position
            ball_x = initial_ball_x
            ball_y = initial_ball_y
            ball_speed_x = 0
            line_x1 = initial_line_x1
            line_x2 = initial_line_x2
            left_y = initial_line_y
            right_y = initial_line_y
            holes = setHoleProperties()
            break

    # Bounce back from the edges
    if ball_x - ball_radius < line_x1 and ball_speed_x < 0:
        ball_speed_x = -ball_speed_x * 0.6
    elif ball_x + ball_radius > line_x2 and ball_speed_x > 0:
        ball_speed_x = -ball_speed_x * 0.6

    screen.fill(black)
    pygame.draw.aaline(screen, white, (line_x1, left_y), (line_x2, right_y), 3, )

    # Draw holes
    for hole_x, hole_y, hole_radius, color in holes:
        pygame.draw.circle(screen, color, (int(hole_x), int(hole_y)), hole_radius)

    # Draw ball
    pygame.draw.circle(screen, white, (int(ball_x), int(ball_y)), ball_radius)

    txtsurf = font.render(f"Score: {goal_score}", True, white)
    screen.blit(txtsurf, (5, 5))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()