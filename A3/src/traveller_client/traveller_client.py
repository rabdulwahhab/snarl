#!/usr/bin/env python3

import json
import sys

TOWNNETWORK = None


def buildNetwork(commandParams):
    # TODO: refactor for Town, and TownNetwork implementations (var names)
    neighborDictionary = {}  # {nameOfTown: TownObj}
    for road in commandParams:
        fromTown = road["from"]  # name of Town
        toTown = road["to"]

        if fromTown in neighborDictionary.keys():
            if toTown in neighborDictionary.keys():
                neighborDictionary[fromTown].addNeighbor(
                    neighborDictionary[toTown])
                neighborDictionary[toTown].addNeighbor(
                    neighborDictionary[fromTown])
            else:
                # Create to Town
                toTownObj = Town(toTown, [])
                neighborDictionary[toTown] = toTownObj
                neighborDictionary[fromTown].addNeighbor(
                    neighborDictionary[toTown])
                neighborDictionary[toTown].addNeighbor(
                    neighborDictionary[fromTown])
        else:
            # Create from Town
            fromTownObj = Town(fromTown, [])
            neighborDictionary[fromTown] = fromTownObj
            if toTown in neighborDictionary.keys():
                neighborDictionary[fromTown].addNeighbor(
                    neighborDictionary[toTown])
                neighborDictionary[toTown].addNeighbor(
                    neighborDictionary[fromTown])
            else:
                # Create to Town
                toTownObj = Town(toTown, [neighborDictionary[fromTown]])
                neighborDictionary[toTown] = toTownObj
                neighborDictionary[fromTown].addNeighbor(
                    neighborDictionary[toTown])
                neighborDictionary[toTown].addNeighbor(
                    neighborDictionary[fromTown])


def placeCharacter(commandParams, townNetwork):
    # TODO: refactor for Character and Town implementation (var names)
    c = Character(commandParams["character"], commandParams["town"])
    for town in townNetwork:
        if town.name == commandParams["town"]:
            town.characters.add(c)
            return townNetwork
    raise Exception("town not found")


def isPassageSafe(commandParams, townNetwork):
    # TODO: refactor if TownNetwork not a class
    return townNetwork.passageSafe()


def execute(dictCommand: dict):
    NETWORK = None
    jsonKeys = dictCommand.keys()
    wellFormedCommand = "command" in jsonKeys and "params" in jsonKeys
    if wellFormedCommand:
        commandReceived = dictCommand["command"]
        if commandReceived == "road":
            TOWNNETWORK = buildNetwork(commandReceived["params"])
            print("Created TownNetwork successfully!")
            print(TOWNNETWORK)
        elif commandReceived == "place":
            TOWNNETWORK = placeCharacter(commandReceived["params"], TOWNNETWORK)
            print("Character has succesfully been placed in Town")
            print(TOWNNETWORK)
        elif commandReceived == "passage-safe?":
            # QUERY command
            passageSafe = isPassageSafe(commandReceived["params"], TOWNNETWORK)
            print("Is the passage safe?")
            print(passageSafe)
        else:
            raise Exception("Unrecognized command, malformed JSON given")
    else:
        raise Exception("Malformed JSON given")  # TODO could be other cases


def main():
    def gatherInput():
        rawJsonStr = ''
        try:
            print('Reading Input >')
            for line in sys.stdin:
                if line.strip() == 'exit':
                    break
                else:
                    rawJsonStr = rawJsonStr + ' ' + line.strip()
            return rawJsonStr
        except:
            return rawJsonStr

    while True:
        # Read from STDIN
        try:
            inputCommand = gatherInput()
            try:
                jd = json.JSONDecoder()
                command = jd.decode(inputCommand)
                execute(command)
            except:
                print("Malformed Input...")
                exit(1)
        except EOFError:
            print("Got EOF")
            exit(1)


if __name__ == '__main__':
    main()
