from Types import *
from Player import receivePlayerUpdate


def testReceivePlayerUpdate():
    """
    Given a json dict player-update and player name,
    check if output PlayerView has all the right information.
    """
    name = "Saleha"
    playerUpdate = {
        "type":     "player-update",
        "layout":   [[0, 0, 1, 0, 0],
                     [0, 0, 2, 0, 0],
                     [0, 1, 1, 0, 0],
                     [0, 1, 1, 0, 0],
                     [0, 2, 0, 0, 0]],
        "position": [4, 3],
        "objects":  [{"type": "key", "position": [4, 2]}],
        "actors":   [
            {"type": "zombie", "name": "Green man", "position": [4, 1]},
            {"type": "player", "name": "Rayyan", "position": [4, 4]}
        ]
    }

    # When
    view = receivePlayerUpdate(playerUpdate, name)

    # Then
    assert view.name is "Saleha"
    assert view.keyObj == {"type": "key", "position": [4, 2]}
    assert view.exitObj is None
    assert len(view.players) is 1
    assert view.players[0].name == "Rayyan"
    assert view.players[0].location == (4, 4)
    assert len(view.enemies) is 1
    assert view.enemies[0].name == "Green man"
    assert len(view.tiles) is 5
