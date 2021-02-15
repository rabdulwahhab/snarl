import pygame
import sys
from pygame.locals import *
from Creation import level, createGenericDungeon
from Render import renderDungeon
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

    # test dungeon
    dung = createGenericDungeon()

    # Event loop
    while True:
        # pygame.time.wait(250)
        clock.tick(30)  # cap at 30fps
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)

        # map of keys pressed
        # keys = pygame.key.get_pressed()
        renderDungeon(background, dung)

        screen.blit(background, (0, 0))  # render pixels to
        pygame.display.update()  # update


if __name__ == '__main__':
    main()
