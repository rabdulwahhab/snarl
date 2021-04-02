import sys

import Globals
import json
import pygame
from pygame.locals import *
import argparse
import math
from Render import renderPlayerView, renderObserverView, renderStatusBar
from Util import logInFile, genXRandCoords, getPlayer, getAllTiles, \
    translateScreenLocation, whichBoardInLevel, locationInLevelBounds, \
    getRandomRoomInLevel, getPlayersInLevel
from Convert import convertJsonLevel
from Create import addPlayersToBoard, addEnemiesToBoard
from Types import *
from Player import getVisibleTiles
import GameManager

log = logInFile("localSnarl.py")


def populateEnemies(levelNum: int, levelEnemies: dict, game: Dungeon):
    for enemyName in levelEnemies.keys():  # Populate enemies in level
        enemyBoardNum = levelEnemies[enemyName][0]
        board: Board = game.levels[levelNum].boards[enemyBoardNum]
        game.levels[levelNum].boards[enemyBoardNum] = addEnemiesToBoard(
            board, {
                enemyName: levelEnemies[enemyName][1]})


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
    parser.add_argument("--observe", help="Observe the game",
                        action="store_true")

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

    if args.players:
        if 1 <= args.players <= 4:
            log('got players flag', str(args.players))
            numPlayers = args.players
        else:
            print("Players must be from 1-4")
            sys.exit(1)

    if args.start and 0 < args.start <= len(jsonLevels):
        log('got start flag', args.start)
        startLevel = args.start

    if args.observe:
        log('got observe')
        isObserving = True

    try:
        rawJsonGameLevels = jsonLevels[(startLevel - 1):]
        jsonGameLevels = [json.loads(rawJsonLevel) for rawJsonLevel in
                          rawJsonGameLevels]
        log("got+converted {} levels".format(len(jsonGameLevels)))

        # this has all the levels needed with the starting level as the first
        # element in the list
        levels = [convertJsonLevel(jsonLevel["rooms"], jsonLevel["hallways"],
                                   jsonLevel["objects"]) for jsonLevel in
                  jsonGameLevels]

        playerNames = [input("Player {}, enter your name > ".format(i + 1)) for
                       i in
                       range(numPlayers)]

        log("Using levels", str(levels))
        forbidden = [levels[0].keyLocation, levels[0].exitLocation]
        players = []
        playerLocs = []
        i = 0
        while i < numPlayers:  # Populate players in level
            playerName = playerNames[i]
            randBoardNum, randBoard = getRandomRoomInLevel(levels[0])
            log("Rand board", str(randBoardNum), str(randBoard.dimensions))
            loc = genXRandCoords(1, forbidden, randBoard.origin,
                                 randBoard.dimensions).pop()
            if loc not in playerLocs:
                player = Player(playerName, loc)
                players.append(player)
                levels[0].boards[randBoardNum] = addPlayersToBoard(randBoard, {
                    playerName: player})
                playerLocs.append(loc)
                i += 1

        game = Dungeon(levels, playerNames, startLevel - 1, False)

        enemies = []  # LIST of dictionaries for each level
        enemyLocs = []
        for i in range(len(game.levels)):
            numZombies = math.floor((i + 1) / 2) + 1
            numGhosts = math.floor(((i + 1) - 1) / 2)
            levelEnemies = {}
            for zombie in range(numZombies):
                randBoardNum, randBoard = getRandomRoomInLevel(levels[0])
                name = "zombie" + str((zombie + 1))
                loc = genXRandCoords(1, playerLocs + forbidden + enemyLocs,
                                     randBoard.origin,
                                     randBoard.dimensions).pop()
                enemyLocs.append(loc)
                newZombie = Enemy(name, loc)
                levelEnemies[name] = (randBoardNum, newZombie)
            for ghost in range(numGhosts):
                randBoardNum, randBoard = getRandomRoomInLevel(levels[0])
                name = "ghost" + str((ghost + 1))
                loc = genXRandCoords(1, playerLocs + forbidden + enemyLocs,
                                     randBoard.origin,
                                     randBoard.dimensions).pop()
                enemyLocs.append(loc)
                newGhost = Enemy(name, loc, "ghost")
                levelEnemies[name] = (randBoardNum, newGhost)

            enemies.append(levelEnemies)
            populateEnemies(i, levelEnemies, game)

        # Initialize screen
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(Globals.SCREEN_DIMENSIONS,
                                         flags=pygame.RESIZABLE)
        pygame.display.set_caption("Local Snarl Demo")

        # Fill background. Draw onto this
        gameDisplaySize = (
            Globals.GAME_DISPLAY_WIDTH, Globals.GAME_DISPLAY_HEIGHT)
        background = pygame.Surface(gameDisplaySize)
        statusBarSize = (Globals.STATUS_BAR_WIDTH, Globals.STATUS_BAR_HEIGHT)
        statusBar = pygame.Surface(statusBarSize)
        background = background.convert()  # converts Surface to single-pixel
        statusBar = statusBar.convert()  # converts Surface to single-pixel
        # format
        background.fill(Globals.BG_COLOR)
        statusBar.fill(Globals.BG_COLOR)

        currLevel0: Level = game.levels[game.currLevel]

        def getEnemies(enemiesDict: list):
            acc = []
            for enemiesInLevel in enemiesDict:
                for enemyName in enemiesInLevel.keys():
                    acc.append(enemiesInLevel[enemyName][1])
            return acc

        allEnemies = getEnemies(enemies)

        log("All enemies", str(allEnemies))
        log("Level has this many boards", str(len(currLevel0.boards)))

        def locationInTiles(location: tuple, tiles: dict):
            lrow, lcol = location
            for row in tiles.keys():
                if lrow == row:
                    for col in tiles[row].keys():
                        if lcol == col:
                            return True
            return False

        if isObserving:
            log("OBSERVER VIEW")
            allTiles = getAllTiles(currLevel0)
            view = ObserverView("observer", allTiles, [currLevel0.keyLocation],
                                [currLevel0.exitLocation],
                                players, allEnemies)
            renderObserverView(background, view)
        else:
            log("PLAYER VIEW")
            player: Player = getPlayer(currLevel0, playerNames[0])
            visibleTiles = getVisibleTiles(player, currLevel0)
            nearbyEnemies = [enemy for enemy in allEnemies if
                             locationInTiles(enemy.location, visibleTiles)]
            nearbyPlayers = [player for player in players if
                             locationInTiles(player.location, visibleTiles)]
            view = PlayerView(playerNames[0],
                              visibleTiles,
                              player.location,
                              [currLevel0.keyLocation],
                              [currLevel0.exitLocation],
                              nearbyPlayers, nearbyEnemies)
            # renderPlayerView(background, view)

        # Block events we don't care about and allow ones we do
        # (speeds processing)
        pygame.event.set_blocked(None)
        pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

        while True:

            # pygame.time.wait(250)
            clock.tick(30)  # cap at 30fps

            if game.isGameOver:  # TODO something special
                log("The game is over!")
                sys.exit(0)

            currLevel: Level = game.levels[game.currLevel]

            # if currLevel.exitUnlocked and getPlayersInLevel(currLevel) == 0:
            #     GameManager.advanceLevel(game)
            #     log("Advancing level")
            #     continue

            playerName = game.players[currLevel.playerTurn]

            log("Player turn", str(currLevel.playerTurn))

            player: Player = getPlayer(currLevel, playerName)
            # player not in level (ejected or exited)
            if not player:
                currLevel.playerTurn = currLevel.playerTurn + 1
                continue

            # Render player view
            board1: Board = currLevel.boards[
                whichBoardInLevel(currLevel,
                                  player.location)]
            visibleTiles = getVisibleTiles(player, currLevel)
            visiblePlayers = [board1.players[pname] for pname in
                              board1.players.keys() if
                              locationInTiles( # FIXME bug when player next to you
                                  board1.players[pname].location,
                                  visibleTiles)]
            visibleEnemies = [board1.enemies[ename] for ename in
                              board1.enemies.keys() if
                              locationInTiles(
                                  board1.enemies[ename].location,
                                  visibleTiles)]
            newView = PlayerView(playerName,
                                 visibleTiles,
                                 player.location,
                                 [currLevel.keyLocation],
                                 [currLevel.exitLocation],
                                 visiblePlayers,
                                 visibleEnemies)
            renderPlayerView(background, newView)
            renderStatusBar(statusBar, game)

            # handle user events
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                if event.type == MOUSEBUTTONDOWN and not isObserving:
                    newLoc = translateScreenLocation(event.pos)
                    if not locationInLevelBounds(currLevel, newLoc):
                        continue
                    log("Got click at", str(event.pos), "--->", str(newLoc))
                    GameManager.move(playerName, newLoc, game)

            """
            gameCollection ---> {gameName: dungeon}
            observerCollection ---> {observerName: gameName}

            when observe requested/game state change
                Observer.send(observerName, gameCollection[observerCollection[observerName]])
            """

            # map of keys pressed

            # keys = pygame.key.get_pressed()
            screen.blit(background,
                        (0, Globals.STATUS_BAR_HEIGHT))  # render pixels to
            screen.blit(statusBar, (0, 0))
            pygame.display.update()  # update


    except FileNotFoundError:
        print("Couldn't find that level file. Try again")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Malformed levels")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


if __name__ == '__main__':
    main()
