### State Representation

The game state in our version of Snarl is the Dungeon data structure, which contains a precise snapshot of the system at any given moment. This is specifically composed of the levels, rooms, players, etc. Overseeing the game state will be the responsibility of the Game Manager, which will have a module of functions which handle ulterior tasks. The functionality of the Manager Module will include:

#### Setup and maintenance of socket connections/Placing players in games 

    None -> None
#### Handling requests to advance the game (move made, player quit)

    command -> Dungeon
#### Broadcasting updated state to all connected clients

    Dungeon -> None

#### Parsing and application of AI enemy moves for tournaments

    command -> None
#### Keeping time/Game clock

    None -> None
#### Keeping track of which player’s turn it is

    None -> None
#### Validation and error handling of invalid moves

    command -> Boolean 
#### Send move as player to Game Manager

    command -> None

We intend for the Game Manager to compute changes to the game and consolidate as much of the game logic as possible thereby making the game state something that only needs to be passed to the Clients to display for the users. 

A dungeon is a Python class which includes:
- name : string
- levels : list of type Level
- players : list of strings which represent a Player name
- currLevel : integer which represents the index of the level - in levels 
- currRoom : integer which represents the index of the room we’re in within a level
- currPlayer : integer which represents the index of the level in levels  
