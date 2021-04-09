import json
from Types import *


def welcomeMsg(jsonStr: str):
    out = {
        'type': 'welcome',
        'info': json.loads(jsonStr)
    }
    return json.dumps(out)


def startLevelMsg(levelNum: int, playerNames: list):
    out = {
        "type":    "start-level",
        "level":   levelNum,
        "players": playerNames
    }
    return json.dumps(out)


def translateObjects(view: PlayerView):
    return None


def translateActors(view: PlayerView):
    return None


def playerUpdateMsg(view: PlayerView, msg=None):
    out = {
        "type":     "player-update",
        "layout":   view.tiles,
        "position": view.position,
        "objects":  translateObjects(view),
        "actors":   translateActors(view),
        "message":  msg
    }
    return json.dumps(out)
