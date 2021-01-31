from typing import List


class Town:
    def __init__(self, name):
        self.name: str = name
        self.neighbors: List[Town] = []
        self.characters: List[Character] = []

    def addNeighbor(self, neighbor):
        """
        Takes in a Town to be added as a neighbor.
        :param neighbor:
        :return: None
        """
        self.neighbors.append(neighbor)
        return None

    def removeNeighbor(self, neighbor):
        """
        Removes a Town from listOfNeighbors.
        :param neighbor:
        :return: None
        :raise: Exception if Neighbor doesn't exist in Town
        """
        if neighbor in self.neighbors:
            self.neighbors.remove(neighbor)
            return None
        else:
            raise Exception("Removing a Neighbor not in this Town")

    def getNeighbors(self):
        """
        Gets list of neighbors from the Town.
        :return: List of neighbors of this town
        """
        return self.neighbors

    def addCharacter(self, character):
        """
        Adds the given character to this Town.
        :param character:
        :return: None
        """
        self.characters.append(character)
        return None

    def removeCharacter(self, character):
        """
        Deletes the given character from this Town.
        :param character:
        :return: None
        :raise: Exception if Character doesn't exist in Town
        """
        if character in self.characters:
            self.characters.remove(character)
            return None
        else:
            raise Exception("Removing a Character not in this Town")

    def getCharacters(self):
        """
        Gets list of characters from the Town.
        :return: List of character in this town
        """
        return self.characters

    def getEmptyNeighbors(self):
        """
        Helper function that returns a set of neighbors that is empty.
        :return: Set of Neighbors
        """
        emptyNeighbors = set()
        for currNeighbor in self.neighbors:
            if len(currNeighbor.getCharacters()) == 0:
                emptyNeighbors.add(currNeighbor)
        return emptyNeighbors


class Character:
    def __init__(self, name, location):
        self.name: str = name
        self.location: Town = location

    def moveCharacter(self, town):
        """
        Moves this character to the destination.
        :return: None
        """
        self.location = town
        return None

    def getLocation(self):
        """
        Get the current location of the character.
        :return: Town
        """
        return self.location

    def canAnonymouslyRelocate(self, dest: Town):
        """
        Check whether this Character can move to another Town without
        running into other Characters.
        :param dest: Town
        :return: Boolean
        """
        unvisited = set(self.location.getEmptyNeighbors())
        visited = {self.location}

        while len(unvisited) > 0:
            currentTown = unvisited.pop()
            if len(currentTown.getCharacters()) == 0:
                if currentTown.name == dest.name:  # TODO how to tell if equal?
                    return True
                else:
                    visited.add(currentTown)
                    currTownsNeighbors = currentTown.getEmptyNeighbors()
                    newEmptyNeighbors = currTownsNeighbors.difference(visited)
                    unvisited.add(newEmptyNeighbors)
        return False


class TownNetwork:
    def __init__(self, towns=None):
        if towns is None:
            self.towns: List[Town] = []
        else:
            self.towns: List[Town] = towns

    def addTown(self, town):
        """
        Takes in a Town to be added added to the TownNetwork.
        :param town:
        :return: None
        """
        self.towns.append(town)
        return None

    def removeTown(self, town):
        """
        Removes a Town from the networks.
        :param town:
        :return: None
        :raise: Exception if Town doesn't exist in TownNetwork
        """
        if town in self.towns:
            self.towns.remove(town)
            return None
        else:
            raise Exception("Removing a Town not in this TownNetwork")
