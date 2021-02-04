#!/usr/bin/env python3

import socket
import sys
import json

CREATED = 0
TOWNS = []
PLACEMENT_COMMANDS = []
INVALID_PLACEMENT = []


def responseFromServer():
    #TODO: respond with boolean, also print invalid placements one by one


def createTownNetwork(params: list):
    for road in params:
        if road["from"] not in TOWNS:
            TOWNS.append(road["from"])
        if road["to"] not in TOWNS:
            TOWNS.append(road["to"])
    msg = {"towns": TOWNS, "roads": params}
    return msg


def placeCharacter(params: dict):
    if params['town'] not in TOWNS:
        msg = ["invalid placement", {"name": params["character"], "town": params["town"]}]
        #TODO: WHEN TO PRINT
        INVALID_PLACEMENT.append(msg)
    else:
        placement = {"name": params["character"], "town": params["town"]}
        PLACEMENT_COMMANDS.append(placement)
        msg = {}
    return msg


def queryPassageSafety(params: dict):
    characterInQuestion = params["character"]
    destination = params["town"]
    msg = {}
    if destination not in TOWNS:
        #TODO: error
    else:
        for placement in PLACEMENT_COMMANDS:
            if placement["character"] == characterInQuestion:
                # Batch query
                query = {"character": characterInQuestion, "destination": destination}
                msg = {"characters": PLACEMENT_COMMANDS, "query": query}
                return json.dumps(msg)
            else:
                #TODO: error
    return msg


def parseUserCommand(commandDict: dict):
    # returns processed json Command
    global CREATED
    processedRequest = None
    toReceive = False
    toSend = True
    jsonKeys = commandDict.keys()
    wellformedCommand = "command" in jsonKeys and "params" in jsonKeys
    if wellformedCommand:
        if commandDict["command"] == "roads" and CREATED == 0:
            processedRequest = createTownNetwork(commandDict["params"])
            CREATED += 1
        elif commandDict["command"] == "place":
            processedRequest = placeCharacter(commandDict["params"])
            toSend = False
        elif commandDict["command"] == "passage-safe?":
            processedRequest = queryPassageSafety(commandDict["params"])
            toReceive = True
    else:
        processedRequest = {"error": "not a request", "object": commandDict}
        print(json.dumps(processedRequest))

    return json.dumps(processedRequest), toSend, toReceive


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
        data = sock.recv(4096).decode("utf-8")
        sessionId = json.dumps(['the server will call me', data])
        print (sessionId)

        # Get first command (should be roads)
        userInput = input("Reading input > ")
        jd = json.JSONDecoder()
        commandDict = jd.decode(userInput)
        if commandDict["command"] == "roads":
            jsonRequest, toSend, toReceive = parseUserCommand(commandDict)
            sock.send(jsonRequest.encode("utf-8"))
            # TODO: can get rid of
            CREATED += 1
        else:
            print("The first command must be a 'roads' command.")
            exit(1)

    except:
        print("Connection failed during signup + session id exchange")
        exit(1)

    # Interaction between client and server (the fun begins)
    while True:
        try:
            userInput = input("Reading input > ")
            jd = json.JSONDecoder()
            commandDict = jd.decode(userInput)
            jsonRequest, toSend, toReceive = parseUserCommand(commandDict)
            if toSend:
                sock.send(jsonRequest.encode("utf-8"))
            if toReceive:
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
