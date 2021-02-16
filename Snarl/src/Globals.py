import pygame
from math import floor

SCREEN_WIDTH = 650  # in pixels
SCREEN_HEIGHT = 500
SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)
BG_COLOR = (255, 255, 255)  # white...boring

TILE_WIDTH = 50
TILE_HEIGHT = 50

# These are the dimensions of the game display (not necessarily the entire
# screen) in tile units

GAME_WIDTH = floor(SCREEN_WIDTH / TILE_WIDTH)
GAME_HEIGHT = floor(SCREEN_HEIGHT / TILE_HEIGHT)

pygame.font.init()
FONT = pygame.font.SysFont('arial', 24)