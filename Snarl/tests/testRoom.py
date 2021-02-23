import sys
import json

sys.path.append("../src")


def getLocationsAround(location):
    above = [location[0], location[1] + 1]
    below = [location[0], location[1] - 1]
    right = [location[0] + 1, location[1]]
    left = [location[0] - 1, location[1]]
    return [above, right, below, left]


def inBoundaries(location: tuple, dimensions: tuple):
    xValid = 0 <= location[0] < dimensions[0]
    yValid = 0 <= location[1] < dimensions[1]
    return xValid and yValid


def inRoom(point: list, bounds: dict, origin: list):
    xMax = origin[0] + bounds['rows']
    yMax = origin[1] + bounds['columns']
    xInRoom = origin[0] <= point[0] < xMax
    yInRoom = origin[1] <= point[1] < yMax

    return xInRoom and yInRoom


def buildOutput(point, bounds, origin, dimensions, roomLayout):
    output = []
    if inRoom(point, bounds, origin):
        relativeLocation = (point[0] - origin[0], point[1] - origin[1])
        surroundingLocations = getLocationsAround(relativeLocation)
        validAround = [location for location in surroundingLocations if
                       inBoundaries(relativeLocation, dimensions)]
        traversable = [location for location in validAround if
                       roomLayout[relativeLocation[0]][
                           relativeLocation[1]] != 0]
        traversable = list(map(lambda loc: [loc[0] + origin[0],
                                            loc[1] + origin[1]],
                               traversable))
        output.append("Success: Traversable points from ")
        output.append(point)
        output.append(" in room at ")
        output.append(origin)
        output.append(" are ")
        output.append(traversable)
    else:
        output.append("Failure: Point ")
        output.append(point)
        output.append(" is not in room at ")
        output.append(origin)

    return output


def main():
    try:
        inputJson = sys.stdin.read()
        decoded = json.loads(inputJson.replace("\n", ""))
        (room, point) = [decoded[0], decoded[1]]
        dimensions = (room["bounds"]["rows"], room["bounds"]["columns"])
        roomLayout = room["layout"]
        output = buildOutput(point, room['bounds'], room['origin'],
                             dimensions, roomLayout)
        print(str(output))
    except json.JSONDecodeError:
        print("Malformed JSON received. Got: " + inputJson)
        sys.stdin.buffer.flush()
        sys.exit(1)
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)


if __name__ == '__main__':
    main()
