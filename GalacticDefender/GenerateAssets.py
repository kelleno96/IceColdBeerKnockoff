import cv2
import numpy as np
from pydub.generators import Sine
from pydub import AudioSegment

def create_player_ship():
    image = np.zeros((64, 64, 3), dtype=np.uint8)
    cv2.rectangle(image, (24, 44), (40, 64), (255, 255, 255), -1)  # Body
    cv2.rectangle(image, (28, 24), (36, 44), (0, 0, 255), -1)      # Middle
    cv2.rectangle(image, (24, 0), (28, 24), (255, 0, 0), -1)       # Left Wing
    cv2.rectangle(image, (36, 0), (40, 24), (255, 0, 0), -1)       # Right Wing
    cv2.imwrite('player_ship.png', image)

def create_enemy_ship():
    image = np.zeros((64, 64, 3), dtype=np.uint8)
    cv2.rectangle(image, (24, 24), (40, 44), (0, 0, 255), -1)  # Body
    cv2.rectangle(image, (20, 0), (24, 24), (0, 0, 0), -1)     # Left Wing
    cv2.rectangle(image, (40, 0), (44, 24), (0, 0, 0), -1)     # Right Wing
    cv2.imwrite('enemy_ship.png', image)

def create_bullet():
    image = np.zeros((16, 32, 3), dtype=np.uint8)
    cv2.rectangle(image, (6, 0), (10, 32), (255, 255, 255), -1)  # Body
    cv2.rectangle(image, (0, 0), (16, 6), (255, 0, 0), -1)       # Tip
    cv2.imwrite('bullet.png', image)

def create_shield_powerup():
    image = np.zeros((32, 32, 3), dtype=np.uint8)
    cv2.circle(image, (16, 16), 16, (255, 255, 255), -1)  # Outer Circle
    cv2.circle(image, (16, 16), 12, (0, 0, 255), -1)      # Inner Circle
    cv2.imwrite('shield_powerup.png', image)

def create_speed_powerup():
    image = np.zeros((32, 32, 3), dtype=np.uint8)
    points = np.array([[16, 0], [24, 32], [8, 32]], np.int32)  # Arrow Points
    cv2.fillPoly(image, [points], (0, 255, 0))
    cv2.imwrite('speed_powerup.png', image)

def create_sound(filename, frequency, duration_ms):
    sine_wave = Sine(frequency).to_audio_segment(duration=duration_ms)
    sine_wave.export(filename, format="wav")

# Create images
create_player_ship()
create_enemy_ship()
create_bullet()
create_shield_powerup()
create_speed_powerup()

# Create sounds
create_sound("shoot.wav", 440, 500)        # A 440 Hz tone for 500 ms
create_sound("explosion.wav", 60, 500)     # A 60 Hz tone for 500 ms
create_sound("powerup.wav", 880, 500)      # An 880 Hz tone for 500 ms