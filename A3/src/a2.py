#!/usr/bin/env python3

import json
import sys


def baseResult(mathFunc):
    if mathFunc == '--sum':
        return 0
    elif mathFunc == '--product':
        return 1
    else:
        print("Only current options are product and sum")


def calcNumJson(numJson, mathFunc):
    if type(numJson) is int:
        result = numJson
    elif type(numJson) is str:
        result = baseResult(mathFunc)
    elif type(numJson) is list:  # recur here
        result = baseResult(mathFunc)
        for element in numJson:
            if mathFunc == '--sum':
                result += calcNumJson(element, mathFunc)
            elif mathFunc == '--product':
                result *= calcNumJson(element, mathFunc)
    else:
        if "payload" in numJson.keys():
            result = calcNumJson(numJson["payload"], mathFunc)
        else:
            result = baseResult(mathFunc)
    return result


def delimSplit(numJsonStr):
    parsedInputArray = []
    layerStart = 0
    layerEnd = 0
    squareBrack = ['[', ']']
    curlyBrack = ['{', '}']
    i = 0

    while i < len(numJsonStr):
        c = numJsonStr[i]

        if c == squareBrack[0]:
            layerStart += 1
            j = i + 1
            while j < len(numJsonStr):
                if numJsonStr[j] == squareBrack[1]:
                    layerEnd += 1
                    if layerStart == layerEnd:
                        # WE HAVE FOUND IT
                        parsedInputArray.append(numJsonStr[i:j + 1])
                        i = j + 1
                        break
                elif numJsonStr[j] == squareBrack[0]:
                    layerStart += 1
                j += 1
        elif c == curlyBrack[0]:
            layerStart += 1
            j = i + 1
            while j < len(numJsonStr):
                if numJsonStr[j] == curlyBrack[1]:
                    layerEnd += 1
                    if layerStart == layerEnd:
                        # WE HAVE FOUND IT
                        parsedInputArray.append(numJsonStr[i:j + 1])
                        i = j + 1
                        break
                elif numJsonStr[j] == curlyBrack[0]:
                    layerStart += 1
                j += 1
        elif c == '"':
            layerStart += 1
            j = i + 1
            while j < len(numJsonStr):
                if numJsonStr[j] == "\"" and numJsonStr[j - 1] != '\\':
                    layerEnd += 1
                    if layerStart == layerEnd:
                        # WE HAVE FOUND IT
                        parsedInputArray.append(numJsonStr[i:j + 1])
                        i = j + 1
                        break
                j += 1
        else:
            numStr = ""
            while i < len(numJsonStr) and numJsonStr[i] != ' ':
                numStr = numStr + numJsonStr[i]
                i += 1
            if numStr != "":
                parsedInputArray.append(numStr)

        i += 1

    return parsedInputArray


def main():
    def gatherInput():
        rawNumJsonStr = ''
        try:
            print('Reading Input >')
            for line in sys.stdin:
                if line.strip() == 'exit':
                    break
                else:
                    rawNumJsonStr = rawNumJsonStr + ' ' + line.strip()
            return rawNumJsonStr
        except:
            return rawNumJsonStr

    # Check if correct usage
    if len(sys.argv) != 2 or (sys.argv[1] not in ["--sum", "--product"]):
        print("Usage: [--sum | --product] NumJSON ...")
        exit(1)
    else:  # Read from STDIN
        inputtedNumJsons = gatherInput()

        # Parse input stream to list of individual NumJSON strings
        parsedNumJsons = delimSplit(inputtedNumJsons)
        result = parseNumJsons(parsedNumJsons, sys.argv[1])

        print("Processed NumJSONs:")
        print(result)

        exit(0)


def parseNumJsons(parsedNumJsonList, mathFunc):
    result = []
    # Loop, compute, format output
    for strNumJson in parsedNumJsonList:
        resDict = {"object": strNumJson}
        jd = json.JSONDecoder()
        try:
            data = jd.decode(strNumJson)
        except:
            print("Malformed Input...")
            exit(1)
        total = calcNumJson(data, mathFunc)
        resDict["total"] = total
        result.append(resDict)
    return result


if __name__ == '__main__':
    main()
