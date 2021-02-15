import pygame
import sys
from pygame.locals import *
from Creation import level
from Render import renderLevel
from DevTools import logInFile
from Util import Globals

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

    # test drawing
    renderLevel(background, level, 0)

    # Event loop
    while True:
        # pygame.time.wait(250)
        clock.tick(30)  # cap at 30fps
        for ev in pygame.event.get():
            if ev.type == QUIT:
                sys.exit(0)

        # map of keys pressed
        # keys = pygame.key.get_pressed()

        screen.blit(background, (0, 0))  # render pixels to
        pygame.display.update()  # update


if __name__ == '__main__':
    main()
