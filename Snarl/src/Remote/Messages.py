import json
from Types import *
from Server import getPlayerUpdate


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
    out = getPlayerUpdate(playerName, game)
    out["message"] = msg
    return formatted(out)
