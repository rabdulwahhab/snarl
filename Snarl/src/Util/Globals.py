from math import floor

SCREEN_WIDTH = 450  # in pixels
SCREEN_HEIGHT = 400
SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)
BG_COLOR = (255, 255, 255)  # white...boring

TILE_WIDTH = 30
TILE_HEIGHT = 30

# These are the dimensions of the game display (not necessarily the entire
# screen) in tile units

GAME_WIDTH = floor(SCREEN_WIDTH / TILE_WIDTH)
GAME_HEIGHT = floor(SCREEN_HEIGHT / TILE_HEIGHT)
