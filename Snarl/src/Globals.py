from math import floor
from pygame import font

SCREEN_WIDTH = 1200  # in pixels
SCREEN_HEIGHT = 800
SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)
BG_COLOR = (255, 255, 255)  # white...boring

TILE_WIDTH = 40
TILE_HEIGHT = 40

# These are the dimensions of the game display (not necessarily the entire
# screen) in tile units

GAME_WIDTH = floor(SCREEN_WIDTH / TILE_WIDTH)
GAME_HEIGHT = floor(SCREEN_HEIGHT / TILE_HEIGHT)

font.init()
FONT = font.SysFont('arial', 24)
