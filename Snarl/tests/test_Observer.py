from Types import *
from Observer import receiveUpdate


def testReceiveObserverUpdate():
    """
    Given a json array manager-trace-entry
    check if output ObserverView has all the right information.
    """
    observer = ObserverView("observer", {})
    gameUpdate = ["Saleha",
                  {
                      "type":     "player-update",
                      "layout":   [[0, 0, 1, 0, 0],
                                   [0, 0, 2, 0, 0],
                                   [0, 1, 1, 0, 0],
                                   [0, 1, 1, 0, 0],
                                   [0, 2, 0, 0, 0]],
                      "position": [4, 3],
                      "objects":  [{"type": "key", "position": [4, 2]},
                                   {"type": "exit", "position": [4, 0]}],
                      "actors":   [
                          {"type":     "zombie", "name": "Green man",
                           "position": [4, 1]},
                          {"type":     "player", "name": "Rayyan",
                           "position": [4, 4]}
                      ]
                  }]

    # When
    view = receiveUpdate(observer, gameUpdate)

    # Then
    assert view.name is "observer"
    assert view.keyObj == {"type": "key", "position": [4, 2]}
    assert view.exitObj == {"type": "exit", "position": [4, 0]}
    assert len(view.players) is 1
    assert view.players[0].name == "Rayyan"
    assert view.players[0].location == (4, 4)
    assert len(view.enemies) is 1
    assert view.enemies[0].name == "Green man"
    assert len(view.tiles) is 0  # hasn't changed from initial observer
    assert len(view.history) == 1
