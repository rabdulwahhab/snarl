#!/usr/bin/env python3

import socket
import sys
import json

CREATED = 0


def createTownNetwork(params):
    return {}


def placeCharacter(params):
    return {}


def queryPassageSafety(params):
    return {}


def parseUserCommand(commandDict: dict):
    # returns processed json Command
    global CREATED
    msg = None
    expectResponse = True
    jsonKeys = commandDict.keys()
    wellformedCommand = "command" in jsonKeys and "params" in jsonKeys
    if wellformedCommand:
        if commandDict["command"] == "roads" and CREATED == 0:
            msg = createTownNetwork(commandDict["params"])
            CREATED += 1
            expectResponse = False
        elif commandDict["command"] == "place":
            msg = placeCharacter(commandDict["params"])
        elif commandDict["command"] == "passage-safe?":
            msg = queryPassageSafety(commandDict["params"])
    else:
        msg = {"error": "not a request", "object": commandDict}
        print(json.dumps(msg))

    return (json.dumps(msg), expectResponse)


def main():
    args = sys.argv[1:]
    sock: socket = None

    if len(args) == 3:
        (hostName, port, userName) = [args[0], int(args[1]), args[2]]
    elif len(args) == 2:
        (hostName, port, userName) = [args[0], int(args[1]),
                                      "Glorifrir Flintshoulder"]
    elif len(args) == 1:
        (hostName, port, userName) = [args[0], 8000, "Glorifrir Flintshoulder"]
    else:
        (hostName, port, userName) = ["localhost", 8000,
                                      "Glorifrir Flintshoulder"]

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostName, port))
    except:
        print("Connection error. Check host and port")
        exit(1)

    print("Connected on port {port} to host {hostName}".format(port=port,
                                                               hostName=hostName))
    try:
        # Send Sign Up name
        sock.send(userName.encode("utf-8"))

        # Receive Session ID
        # data = sock.recv(4096).decode("utf-8")
        # print(data)
    except:
        print("Connection failed during signup + session id exchange")
        exit(1)

    # Interaction between client and server (the fun begins)
    while True:
        try:
            userInput = input("Reading input > ")
            jd = json.JSONDecoder()
            commandDict = jd.decode(userInput)
            jsonRequest, expectServerResp = parseUserCommand(commandDict)
            sock.send(jsonRequest.encode("utf-8"))
            if expectServerResp:
                data = sock.recv(4096).decode("utf-8")
                print(data)
        except json.JSONDecodeError:
            print("JSON error")
            exit(1)
        except:
            print("Connection closed.")
            exit(0)


if __name__ == '__main__':
    main()
