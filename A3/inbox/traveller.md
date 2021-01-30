<h3>Traveller Module Interface</h3>

*Language/Version*: Python 3.6. *Goal*: Create a Python module with the following classes and methods.

<h4>Town</h4>

*   Instance Variables: name - String, neighbors - List of Town, characters - List of Character
*   Constructor: name (String) listOfNeighbors (List of Towns) -> Town | Purpose: Takes in the name of the Town and the neighbors of this Town and returns a Node.
*   Add neighbor: neighbor (Node) -> None | Purpose: Takes in a Town to be added as a neighbor.
*   Remove neighbor: neighborToRemove (Node) -> None | Purpose: Removes a Town from listOfNeighbors
*   Get list of neighbors: void -> listOfNeighbors (List of Nodes) | Purpose: Gets list of neighbors from the Town.
*   Add character: character (Character) -> None | Purpose: Adds the given character to this Town.
*   Delete character: character (Character) -> None | Purpose: Deletes the given character from this Town.
*   Get list of characters: void -> characters (List of Character) | Purpose: Gets list of characters from the Town.

<h4>Character</h4>

*   Instance Variables: name - String, location - Town
*   Constructor: name (String) location (Town) -> Character | Purpose: Creates a character with the specified name and location and returns the created character.
*   Move character: destination (Town) -> None | Purpose: Moves this character to the destination.
*   Get location: void -> Town | Purpose: Get the current location of the character.
*   Check whether a character can move to another Town without running into other characters: destination (Town) -> bool | Purpose: Whether this character can move to the destination Town. Returns true if all Towns between the current location (exclusive) and destination Town (inclusive) are empty.

<h4>TownNetwork</h4>

*   Instance Variables: ListOfTowns - List of Nodes
*   Constructor
    *   Constructor with no arguments: void -> TownNetwork | Purpose: Creates a TownNetwork and returns it.
    *   Constructor with arguments: ListOfTowns (List of Nodes) -> TownNetwork | Purpose: Creates a TownNetwork with the specified list of Towns and returns it.
*   Add a town to the network: town (Node) -> None | Purpose: Adds the specified Town to the network.
*   Remove a town from the network: Town (Node) -> None | Purpose: Removes the specified Town to the network.
