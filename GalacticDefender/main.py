import pygame
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Galactic Defender')

# Clock to control the frame rate
clock = pygame.time.Clock()
FPS = 60

# Load assets
player_image = pygame.image.load('player_ship.png').convert_alpha()
enemy_image = pygame.image.load('enemy_ship.png').convert_alpha()
bullet_image = pygame.image.load('bullet.png').convert_alpha()
powerup_images = {
    'shield': pygame.image.load('shield_powerup.png').convert_alpha(),
    'speed': pygame.image.load('speed_powerup.png').convert_alpha()
}

# Load sounds
shoot_sound = pygame.mixer.Sound('shoot.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')
powerup_sound = pygame.mixer.Sound('powerup.wav')
# background_music = 'background_music.mp3'
# pygame.mixer.music.load(background_music)
# pygame.mixer.music.play(-1)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5
        self.lives = 3
        self.shield = False
        self.shield_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

        if self.shield and pygame.time.get_ticks() > self.shield_timer:
            self.shield = False

    def get_hit(self):
        if not self.shield:
            self.lives -= 1
            self.shield = True
            self.shield_timer = pygame.time.get_ticks() + 2000  # 2 seconds of shield


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(1, 3)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, kind, x, y):
        super().__init__()
        self.kind = kind
        self.image = powerup_images[kind]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create enemies
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game variables
score = 0
level = 1

# Font
font = pygame.font.SysFont(None, 36)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()

    # Update
    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        explosion_sound.play()
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        if random.random() > 0.9:
            powerup = PowerUp(random.choice(['shield', 'speed']), hit.rect.centerx, hit.rect.centery)
            all_sprites.add(powerup)
            powerups.add(powerup)

    # Check for player collision with enemies
    enemy_hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in enemy_hits:
        player.get_hit()
        explosion_sound.play()
        if player.lives <= 0:
            running = False

    # Check for player collision with power-ups
    powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
    for powerup in powerup_hits:
        powerup_sound.play()
        if powerup.kind == 'shield':
            player.shield = True
            player.shield_timer = pygame.time.get_ticks() + 5000  # 5 seconds of shield
        elif powerup.kind == 'speed':
            player.speed += 2
            pygame.time.set_timer(USEREVENT + 1, 5000)  # 5 seconds of speed boost

    # Reset speed after boost
    if event.type == USEREVENT + 1:
        player.speed = 5

    # Increase difficulty
    if score > level * 100:
        level += 1
        for i in range(level):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(f'Score: {score}', font, WHITE, screen, 10, 10)
    draw_text(f'Lives: {player.lives}', font, WHITE, screen, SCREEN_WIDTH - 120, 10)
    draw_text(f'Level: {level}', font, WHITE, screen, SCREEN_WIDTH // 2 - 40, 10)

    # Flip the display
    pygame.display.flip()

    # Ensure program maintains a rate of 60 frames per second
    clock.tick(FPS)

pygame.quit()