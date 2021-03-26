from Types import *
from Convert import convertJsonPlayer, convertJsonEnemy
from more_itertools import first_true

"""
receiveUpdate(update) -> None (show to observer)
registerObserver(id) -> None (init local state to show)
unregisterObserver() -> None (leave observing)

"""


def receiveUpdate(observer: ObserverView, gameUpdate: list):
    """
    Given a game update (manager-trace), will update the view for
    the observer.
    :params gameUpdate: list
    """
    [playerName, update] = gameUpdate
    players = [convertJsonPlayer(actorJson) for actorJson in update["actors"] if
               actorJson["type"] == "player"]
    enemies = [convertJsonEnemy(actorJson) for actorJson in update["actors"]
               if actorJson["type"] != "player"]

    keyObj = first_true(update["objects"],
                        pred=lambda obj: obj["type"] == "key")
    exitObj = first_true(update["objects"],
                         pred=lambda obj: obj["type"] == "exit")

    view = ObserverView(observer.name, observer.tiles, keyObj, exitObj,
                        players, enemies,
                        observer.history + [(playerName, update)])
    return view


def registerObserver(observerName: str, game: Dungeon):
    """
    Given an observer and game name, registers an observer with the game.
    Returns an ObserverView on success and None if failure.

    # TODO: in the future, this will reach out the GameManager over the network
        #   to get a game instance to look at
    """
    tiles = {}
    players = {}
    enemies = {}
    for board in game.levels[game.currLevel]:
        tiles.update(board.tiles)
        players.update(board.players)
        enemies.update(board.enemies)
    keyObj = {"type":     "key",
              "location": game.levels[game.currLevel].keyLocation}
    exitObj = {"type":     "exit",
               "location": game.levels[game.currLevel].exitLocation}

    view = ObserverView(observerName, tiles, keyObj, exitObj, players, enemies)
    return view


def unregisterObserver(observerName: str, gameName: str):
    """
    Unregisters an observer from a game.
    :params observerName: str
    :params gameName: str
    """
    return ObserverView("", {})
