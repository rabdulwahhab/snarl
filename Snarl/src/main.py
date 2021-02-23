import pygame
import sys
from pygame.locals import *
from Create import createDungeon, createLevel, createGenericBoardTiles
from Types import *
from Render import renderDungeon, renderLevel
from Util import logInFile
import Globals
from example2 import exampleLevel2, players, enemies

log = logInFile("main.py")


def main():
    # Initialize screen
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(Globals.SCREEN_DIMENSIONS)
    pygame.display.set_caption("Snarl Demo")

    # Fill background. Draw onto this
    background = pygame.Surface(screen.get_size())
    background = background.convert()  # converts Surface to single-pixel format
    background.fill(Globals.BG_COLOR)

    # render test level (400 x 300)
    dung = createDungeon(exampleLevel2, players, enemies)
    renderDungeon(background, dung)
    # renderLevel(background, exampleLevel2, 0)

    # Event loop
    while True:
        # pygame.time.wait(250)
        clock.tick(30)  # cap at 30fps
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)

        # map of keys pressed
        # keys = pygame.key.get_pressed()

        screen.blit(background, (0, 0))  # render pixels to
        pygame.display.update()  # update


if __name__ == '__main__':
    main()
