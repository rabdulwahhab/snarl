from typing import List


class Town:
    def __init__(self, name):
        self._name: str = name
        self._neighbors: List[Town] = []
        self._characters: List[Character] = []

    def getName(self):
        """
        Returns the name of the Town.
        :return: Str
        """
        return self._name

    def addNeighbor(self, neighbor):
        """
        Takes in a Town to be added as a neighbor.
        :param neighbor:
        :return: None
        """
        self._neighbors.append(neighbor)
        return None

    def removeNeighbor(self, neighbor):
        """
        Removes a Town from listOfNeighbors.
        :param neighbor:
        :return: None
        :raise: Exception if Neighbor doesn't exist in Town
        """
        if neighbor in self._neighbors:
            self._neighbors.remove(neighbor)
            return None
        else:
            raise Exception("Removing a Neighbor not in this Town")

    def getNeighbors(self):
        """
        Gets list of neighbors from the Town.
        :return: List of neighbors of this town
        """
        return self._neighbors

    def addCharacter(self, character):
        """
        Adds the given character to this Town.
        :param character:
        :return: None
        """
        self._characters.append(character)
        return None

    def removeCharacter(self, character):
        """
        Deletes the given character from this Town.
        :param character:
        :return: None
        :raise: Exception if Character doesn't exist in Town
        """
        if character in self._characters:
            self._characters.remove(character)
            return None
        else:
            raise Exception("Removing a Character not in this Town")

    def getCharacters(self):
        """
        Gets list of characters from the Town.
        :return: List of character in this town
        """
        return self._characters

    def getEmptyNeighbors(self):
        """
        Helper function that returns a set of neighboring Towns that have
        no Characters.
        :return: Set of Neighbors
        """
        emptyNeighbors = set()
        for currNeighbor in self._neighbors:
            if len(currNeighbor.getCharacters()) == 0:
                emptyNeighbors = emptyNeighbors.union([currNeighbor])
        return emptyNeighbors


class Character:
    def __init__(self, name, location):
        self._name: str = name
        self._location: Town = location

    def getName(self):
        """
        Returns the name of the Character.
        :return: Str
        """
        return self._name

    def moveCharacter(self, town):
        """
        Moves this character to the destination.
        :return: None
        """
        self._location = town
        return None

    def getLocation(self):
        """
        Get the current location of the character.
        :return: Town
        """
        return self._location

    def canAnonymouslyRelocate(self, dest: Town):
        """
        Check whether this Character can move to another Town without
        running into other Characters.
        :param dest: Town
        :return: Boolean
        """
        unvisited = set(self._location.getEmptyNeighbors())
        visited = {self._location}

        while len(unvisited) > 0:
            currentTown = unvisited.pop()
            if len(currentTown.getCharacters()) == 0:
                if currentTown.getName() == dest.getName():
                    return True
                else:
                    visited.add(currentTown)
                    currTownsNeighbors = currentTown.getEmptyNeighbors()
                    newEmptyNeighbors = currTownsNeighbors.difference(visited)
                    unvisited = unvisited.union(newEmptyNeighbors)

        return False


class TownNetwork:
    def __init__(self, towns=None):
        if towns is None:
            self._towns: List[Town] = []
        else:
            self._towns: List[Town] = towns

    def getTowns(self):
        """
        Returns a List of Towns in the TownNetwork.
        :return: List
        """
        return self._towns

    def addTown(self, town):
        """
        Takes in a Town to be added added to the TownNetwork.
        :param town:
        :return: None
        """
        self._towns.append(town)
        return None

    def removeTown(self, town):
        """
        Removes a Town from the networks.
        :param town:
        :return: None
        :raise: Exception if Town doesn't exist in TownNetwork
        """
        if town in self._towns:
            self._towns.remove(town)
            return None
        else:
            raise Exception("Removing a Town not in this TownNetwork")
