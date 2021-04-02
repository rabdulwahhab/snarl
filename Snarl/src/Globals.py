from math import floor
from pygame import font

TILE_WIDTH = 30
TILE_HEIGHT = 30

SCREEN_WIDTH = 1200  # in pixels
SCREEN_HEIGHT = 700

STATUS_BAR_WIDTH = SCREEN_WIDTH
STATUS_BAR_HEIGHT = TILE_HEIGHT * 2

GAME_DISPLAY_WIDTH = SCREEN_WIDTH
GAME_DISPLAY_HEIGHT = SCREEN_HEIGHT - STATUS_BAR_HEIGHT

SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)

BG_COLOR = (255, 255, 255)  # white...boring

# These are the dimensions of the game display (not necessarily the entire
# screen) in tile units

GAME_WIDTH = floor(GAME_DISPLAY_WIDTH / TILE_WIDTH)
GAME_HEIGHT = floor(GAME_DISPLAY_HEIGHT / TILE_HEIGHT)

font.init()
FONT = font.SysFont('arial', 24)
