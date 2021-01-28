### Traveller Specification: Python 3.6

*_The data definitions for the specification below represent individual Python modules to be created._*

#### Character:
*Properties*
- Unique ID/name
- A Town that signifies its current location 

*Functionality*
- Change location Town

#### Town (Nodes in the TownNetwork)
*Properties*
- Unique ID
- Set of unique Nodes it is connected to (i.e. can't be connected to another Town multiple times)
- Collection of Characters at the Node

*Functionality*
- Add/Remove Characters and neighboring Towns to itself

#### TownNetwork
*Properties*
- Set of Towns

*Functionality*
- Add/Remove a Town
- Given a Character (X) and destination Town (D), can check to see if a path without other Characters exists between the Character and the destination.
    1. Network checks if X's location Town (S) and D exists within its collection.
    2. Network asks S for a set of empty connections (i.e. connections without any characters) that it is connected to.
    3. S returns the set
    4. If D is in the set, return yes. If not, we recur on all returned elements until D is found, keeping track of all visited Towns, or until we run out of Towns to visit, in which case return no.









