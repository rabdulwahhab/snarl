import pygame
from pygame.locals import *
from Creation import level
from Render import renderLevel
from DevTools import logInFile

DIMENSIONS = (400, 400)
BG_COLOR = (255, 255, 255)

log = logInFile("main.py")


def main():
    # Initialize screen
    pygame.init()
    screen = pygame.display.set_mode(DIMENSIONS)
    pygame.display.set_caption("Snarl Demo")

    # Fill background. Draw onto this
    background = pygame.Surface(screen.get_size())
    background = background.convert()  # converts Surface to single-pixel format
    background.fill(BG_COLOR)

    # test drawing
    renderLevel(background, level, 0)

    # Event loop
    while True:
        for ev in pygame.event.get():
            if ev.type == QUIT:
                return

        screen.blit(background, (0, 0))  # render pixels to
        pygame.display.flip()  # update


if __name__ == '__main__':
    main()
