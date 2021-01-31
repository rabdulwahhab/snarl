#!/usr/bin/env python3

import json
import sys


def execute(dictCommand :dict):
    NETWORK = TownNetwork()
    if "command" in dictCommand.keys() and "params" in dictCommand.keys():
        if dictCommand["command"] == "road":
            # BUILD A NETWORKs
        elif dictCommand["command"] == "place":
            s = set()
            s.__contains__()
            for character in NETWORK.towns:
                if params["character"]["name"] == character.getName():
                    character.name == params["character"]["name"]
            # PLACE character
            # Check if character exists, if they do:
            # Add location, if they don't:
            # Create new character with given location
        elif dictCommand["command"] == "passage-safe?":
            # QUERY command
        else:
            raise Exception("Unrecognized command, malformed JSON given")
    else:
        raise Exception("Malformed JSON given")


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

    # Read from STDIN
    inputCommand = gatherInput()
    try:
        jd = json.JSONDecoder()
        command = jd.decode(inputCommand)
    except:
        print("Malformed Input...")
        exit(1)

    execute(command)

    exit(1)



if __name__ == '__main__':
    main()
