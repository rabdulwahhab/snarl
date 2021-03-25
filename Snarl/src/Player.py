from Types import *
from Util import locationInLevelBounds

"""
Human User module where functions represent actions to dispatch on User events

receiveUpdate: currLoc, game -> None (render + other side effects)
makeMove: location -> None (send move to GameManager)
startGame(playerName: str) -> None
joinGame(playerName: str, gameName: str) -> None
move(playerName: str, location: tuple) -> None
stayPut(playerName: str) -> None
whereAmI(playerName: str) -> Location (tuple)
howMuchCanISee(playerName:str) -> List[Tiles
"""

def receiveUpdate(message):
    return True


def getFieldOfView(player: Player, level: Level):
    pLocRow, pLocCol = player.location
    origin = (pLocRow - 2, pLocCol - 2)
    fieldOfView = []
    for r in range(5):
        for c in range(5):
            relLoc = (origin[0] + r, origin[1] + c)
            if locationInLevelBounds(level, relLoc):
                fieldOfView.append(relLoc)
    return fieldOfView