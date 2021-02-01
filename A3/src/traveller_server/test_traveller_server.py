import pytest
import sys
from traveller_server import Town
from traveller_server import TownNetwork
from traveller_server import Character


def testCanCreateTown():
    town1 = Town("Elwood City")
    assert town1.getName() == "Elwood City"
    assert len(town1.getNeighbors()) == 0


def testCanAddNeighborToTown():
    town1 = Town("Elwood City")
    town2 = Town("Crown City")
    town1.addNeighbor(town2)

    neighbors = town1.getNeighbors()

    assert len(neighbors) == 1
    assert neighbors[0].getName() == "Crown City"


def testCanRemoveNeighborFromTown():
    town1 = Town("Elwood City")
    town2 = Town("Crown City")
    town1.addNeighbor(town2)
    town1.removeNeighbor(town2)

    neighbors = town1.getNeighbors()

    assert len(neighbors) == 0


def testCanCreateTownNetwork():
    town1 = Town("Elwood City")
    town2 = Town("Crown City")
    town3 = Town("Skullbone")
    town4 = Town("Detroit")

    tn1 = TownNetwork()
    tn2 = TownNetwork([town1, town2, town3, town4])

    assert len(tn1.getTowns()) == 0
    assert len(tn2.getTowns()) == 4


def testCanCreateCharacter():
    town1 = Town("Elwood City")
    character = Character("Arthur Read", town1)

    assert character.getName() == "Arthur Read"
    assert character.getLocation() == town1


def testCanMoveCharacter():
    town1 = Town("Elwood City")
    town2 = Town("Crown City")
    character = Character("Arthur Read", town1)

    character.moveCharacter(town2)

    assert character.getLocation() == town2


def testCanAnonymouslyRelocate():
    town1 = Town("Elwood City")
    town2 = Town("Crown City")
    town3 = Town("Detroit")
    town4 = Town("Skullbone")

    town1.addNeighbor(town2)
    town2.addNeighbor(town3)
    town3.addNeighbor(town4)

    character = Character("Arthur Read", town1)
    assert character.canAnonymouslyRelocate(town4)
