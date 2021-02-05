# traveller-client tests

from A4.src import a4


def testParseUserCommandInvalidRoad():
    reqDict = {"command": "roads", "params": []}
    resDict = {"error": "not a request", "object": reqDict}

    strReq, toSend, toRecv = a4.parseUserCommand(reqDict)

    assert toSend
    assert not toRecv
    # assert strReq == json.dumps(resDict)


def testParseUserCommandValidRoad():
    reqDict = {"command": "roads",
               "params":  [{"from": "Memphis", "to": "Nashville"}]}
    resDict = {"towns": ["Memphis", "Nashville"],
               "roads": [{"from": "Memphis", "to": "Nashville"}]}

    strReq, toSend, toRecv = a4.parseUserCommand(reqDict)

    assert toSend
    assert not toRecv
    # assert strReq == json.dumps(resDict)
