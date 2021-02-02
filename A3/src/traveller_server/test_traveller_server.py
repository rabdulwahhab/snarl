from traveller_server import Character, Town, TownNetwork


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


def testGetEmptyNeighbors():
    town1 = Town("Elwood City")
    town2 = Town("Crown City")
    town3 = Town("Skullbone")
    town4 = Town("Detroit")

    town2.addNeighbor(town3)
    town3.addNeighbor(town2)
    town1.addNeighbor(town2)
    town1.addNeighbor(town3)

    assert town1.getEmptyNeighbors() == {town2, town3}
    assert town4.getEmptyNeighbors() == set()

    character = Character("Arthur Read", town1)
    town4.addCharacter(character)

    town1.addNeighbor(town4)
    town4.addNeighbor(town1)

    assert town1.getEmptyNeighbors() == {town2, town3}

    town4.addNeighbor(town2)
    town4.addNeighbor(town3)

    assert town4.getEmptyNeighbors() == {town1, town2, town3}


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


def testCanAnonymouslyRelocate1():
    town1 = Town("Elwood City")
    town2 = Town("Crown City")
    town3 = Town("Detroit")
    town4 = Town("Skullbone")

    town1.addNeighbor(town2)
    town2.addNeighbor(town3)
    town3.addNeighbor(town4)

    character = Character("Arthur Read", town1)
    assert character.canAnonymouslyRelocate(town4)


def testCanAnonymouslyRelocate2():
    town1 = Town("one")
    town2 = Town("two")
    town3 = Town("three")
    town4 = Town("fou")
    town5 = Town("five")
    town6 = Town("six")
    town7 = Town("seven")
    town8 = Town("eight")

    town1.addNeighbor(town2)
    town1.addNeighbor(town6)
    town2.addNeighbor(town1)
    town2.addNeighbor(town5)
    town2.addNeighbor(town4)
    town2.addNeighbor(town3)
    town3.addNeighbor(town2)
    town3.addNeighbor(town4)
    town4.addNeighbor(town3)
    town4.addNeighbor(town5)
    town4.addNeighbor(town2)
    town5.addNeighbor(town2)
    town5.addNeighbor(town4)
    town6.addNeighbor(town1)
    town7.addNeighbor(town8)
    town8.addNeighbor(town7)

    c1 = Character("Arthur Read", town1)
    town1.addCharacter(c1)
    assert c1.canAnonymouslyRelocate(town4)
    assert not c1.canAnonymouslyRelocate(town7)

    c2 = Character("DW Read", town3)
    town3.addCharacter(c2)
    assert c1.canAnonymouslyRelocate(town4)

    c3 = Character("Buster Baxter", town2)
    town2.addCharacter(c3)
    assert not c1.canAnonymouslyRelocate(town4)

    c4 = Character("Mr. Ratburn", town2)
    town2.addCharacter(c4)
    assert not c4.canAnonymouslyRelocate(town2)
    assert c4.canAnonymouslyRelocate(town5)
