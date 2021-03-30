import sys
import Globals
import json
import pygame
from pygame.locals import *
import argparse
from Render import renderDungeon
from Util import logInFile
from Convert import convertJsonLevel
from Types import *
import GameManager

log = logInFile("localSnarl.py")


def main():
    DEFAULT_LEVEL = './tests/snarl.levels'
    numPlayers = 1
    startLevel = 1
    jsonLevels = []
    isObserving = False
    numLevels = 0

    parser = argparse.ArgumentParser()  # initialize
    # this is how you add an optional argument
    parser.add_argument("--levels",
                        help="Enter the name of an input JSON Level file",
                        nargs='?',
                        const=DEFAULT_LEVEL, type=str)
    parser.add_argument("--players", help="Enter an amount of players 1-4",
                        nargs='?',
                        const=numPlayers, type=int)
    parser.add_argument("--start",
                        nargs='?',
                        help="Enter the number of the level to start the game from",
                        const=startLevel, type=int)
    parser.add_argument("--observe", help="Observe the game", const=isObserving,
                        type=bool, nargs='?')

    # this is called after you define your optional args
    args = parser.parse_args()

    # Parse level
    if args.levels:
        log('got levels flag', args.levels)
        with open(args.levels) as file:
            wholeFile = file.read()
            portions = wholeFile.split('\n\n')
            cleaned = list(filter(lambda port: port != '', portions))
            numLevels = cleaned[0]
            jsonLevels = cleaned[1:]
    else:
        log("using default level")
        with open(DEFAULT_LEVEL) as file:
            wholeFile = file.read()
            portions = wholeFile.split('\n\n')
            cleaned = list(filter(lambda port: port != '', portions))
            numLevels = cleaned[0]
            jsonLevels = cleaned[1:]

    if args.players and 1 <= args.players <= 4:
        log('got players flag', str(args.players))
        numPlayers = args.players
    else:
        print("Players must be from 1-4")
        sys.exit(1)

    if args.start and 0 < args.start <= len(jsonLevels):
        log('got start flag', args.start)
        startLevel = args.start
    if args.observe:
        log('got observe', args.observe)
        isObserving = args.observe

    try:
        rawJsonGameLevels = jsonLevels[startLevel:]
        jsonGameLevels = [json.loads(rawJsonLevel) for rawJsonLevel in
                          rawJsonGameLevels]

        levels = [convertJsonLevel(jsonLevel["rooms"], jsonLevel["hallways"],
                                   jsonLevel["objects"]) for jsonLevel in
                  jsonGameLevels]

        players = [input("Player {}, enter your name > ".format(i)) for i in
                   range(numPlayers)]

        # TODO add players at random locations in level (i.e. modify levels)

        # TODO handle observing

        game = Dungeon(levels, players, startLevel - 1, False)

        # TODO GameManager starts the game now
        # Congratulations, now begins the main game loop
        # Initialize screen
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(Globals.SCREEN_DIMENSIONS)
        pygame.display.set_caption("Snarl Demo")

        # Fill background. Draw onto this
        background = pygame.Surface(screen.get_size())
        background = background.convert()  # converts Surface to single-pixel format
        background.fill(Globals.BG_COLOR)

        renderDungeon(background, game)

        while True:
            # pygame.time.wait(250)
            clock.tick(30)  # cap at 30fps
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)

            # TODO user events
            """
            gameCollection ---> {gameName: dungeon}
            observerCollection ---> {observerName: gameName}

            when observe requested/game state change
                Observer.send(observerName, gameCollection[observerCollection[observerName]])
            """

            # map of keys pressed
            # keys = pygame.key.get_pressed()

            screen.blit(background, (0, 0))  # render pixels to
            pygame.display.update()  # update

    except json.JSONDecodeError:
        print("Malformed levels")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


if __name__ == '__main__':
    main()
