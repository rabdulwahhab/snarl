import json
from Types import *
import Server
import GameManager


def formatted(msgDict):
    return json.dumps(msgDict) + "\n"


def welcomeMsg(jsonStr: str):
    out = {
        'type': 'welcome',
        'info': json.loads(jsonStr)
    }
    return formatted(out)


def startLevelMsg(levelNum: int, playerNames: list):
    out = {
        "type":    "start-level",
        "level":   levelNum,
        "players": playerNames
    }
    return formatted(out)


def playerUpdateMsg(playerName: str, game: Dungeon, msg=None):
    out = Server.getPlayerUpdate(playerName, game)
    out["message"] = msg
    return formatted(out)


def endLevelMsg(game: Dungeon):
    level: Level = game.levels[game.currLevel]
    out = {
        "type":   "end-level",
        "key":    level.key,
        "exits":  level.exits,
        "ejects": level.ejects
    }
    return formatted(out)


def endGameMsg(game: Dungeon):
    scoresList = []
    for playerName in game.players:
        score = {
            "type": "player-score",
            "name": playerName
        }.update(game.scores[playerName])
        scoresList.append(score)

    out = {
        "type": "end-game",
        "scores": scoresList
    }

    return formatted(out)
