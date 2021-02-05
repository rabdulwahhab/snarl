#!/usr/bin/env python3

import socket
import sys
import json

CREATED = 0
TOWNS = []
PLACEMENT_COMMANDS = []


def responseFromServer(data, jsonRequest):
    request = json.loads(jsonRequest)
    response = json.loads(data)

    if len(response["invalid"]) != 0:
        for element in response["invalid"]:
            msg = ["invalid placement", element]
            print(json.dumps(msg))

    queryBooleanResponse = ["the response for", request["query"], "is",
                            response["response"]]
    print(json.dumps(queryBooleanResponse))


def createTownNetwork(params: list):
    global CREATED
    isValid = True
    towns = []

    if CREATED > 0:
        isValid = False
        return isValid, {}

    for road in params:
        jsonKeys = road.keys()
        wellformedCommand = "from" in jsonKeys and "to" in jsonKeys
        if not wellformedCommand:
            isValid = False
            originalCommand = {"command": "place", "params": params}
            msg = {"error": "not a request", "object": originalCommand}
            print(json.dumps(msg))
            return isValid, msg
        else:
            CREATED += 1
            if road["from"] not in towns:
                towns.append(road["from"])
            if road["to"] not in towns:
                towns.append(road["to"])
    msg = {"towns": towns, "roads": params}
    return isValid, msg


def placeCharacter(params: dict):
    jsonKeys = params.keys()
    msg = {}
    wellformedCommand = "character" in jsonKeys and "town" in jsonKeys
    if wellformedCommand:
        placement = {"name": params["character"], "town": params["town"]}
        PLACEMENT_COMMANDS.append(placement)
    else:
        originalCommand = {"command": "place", "params": params}
        msg = {"error": "not a request", "object": originalCommand}
        print(json.dumps(msg))
    return msg


def queryPassageSafety(params: dict):
    jsonKeys = params.keys()
    isValid = True
    wellformedCommand = "character" in jsonKeys and "town" in jsonKeys
    if wellformedCommand:
        query = {"character":   params["character"],
                 "destination": params["town"]}
        msg = {"characters": PLACEMENT_COMMANDS, "query": query}
    else:
        isValid = False
        originalCommand = {"command": "passage-safe?", "params": params}
        msg = {"error": "not a request", "object": originalCommand}
        print(json.dumps(msg))
    return isValid, msg


def parseUserCommand(commandDict: dict):
    # returns processed json Command
    processedRequest = None
    toReceive = False
    toSend = True
    jsonKeys = commandDict.keys()
    wellformedCommand = "command" in jsonKeys and "params" in jsonKeys
    if wellformedCommand:
        if commandDict["command"] == "roads":
            isValid, processedRequest = createTownNetwork(commandDict["params"])
            toSend = isValid
        elif commandDict["command"] == "place":
            processedRequest = placeCharacter(commandDict["params"])
            toSend = False
        elif commandDict["command"] == "passage-safe?":
            isValid, processedRequest = queryPassageSafety(
                commandDict["params"])
            toReceive = isValid
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
        sessionId = json.dumps(['the server will call me', userName])
        print(sessionId)

        while True:
            # Get first command (should be roads)
            userInput = input("Reading input > ")
            try:
                jd = json.JSONDecoder()
                commandDict = jd.decode(userInput)
                if commandDict["command"] == "roads":
                    jsonRequest, toSend, toReceive = parseUserCommand(
                        commandDict)
                    sock.send(jsonRequest.encode("utf-8"))
                    break
                else:
                    raise json.JSONDecodeError
            except json.JSONDecodeError:
                errorMsg = {"error":  "not a request",
                            "object": userInput}
                print(json.dumps(errorMsg))
    except:
        print("Connection closed. Exiting client.")
        exit(1)

    # Interaction between client and server (the fun begins)
    while True:
        try:
            userInput = input("Reading input > ")
            try:
                jd = json.JSONDecoder()
                commandDict = jd.decode(userInput)
                jsonRequest, toSend, toReceive = parseUserCommand(commandDict)
                if toSend:
                    sock.send(jsonRequest.encode("utf-8"))
                if toReceive:
                    data = sock.recv(4096).decode("utf-8")
                    responseFromServer(data, jsonRequest)
            except json.JSONDecodeError:
                errorMsg = {"error":  "not a request",
                            "object": userInput}
                print(json.dumps(errorMsg))
                exit(1)
        except:
            print("Connection closed.")
            exit(0)


if __name__ == '__main__':
    main()
