## Game Manager

For our game manager interface, we deal with all “player” interactions with the game. The functionality for a game manager includes starting a game (given a level), accepting players, taking input, broadcasting different updates to appropriate audiences, and moving a player and executing interactions. 

### Input functionality:
- Function to read input and parse it from files or command line or over the network.
  - `readInput() -> String`

### Functions to set up a Game:
  #### Step 1: Receive level and convert it
    - `acceptLevel(levelJson: str) -> None`
    - `convertJsonLevel(givenLevel: json) -> Level`
  #### Step 2: Initialize a new game with the given level
    - `startGame(level: Level) -> Dungeon`
    - `createDungeon()`

### Functions to accept players:
  #### Step 1: Validate incoming player, make sure no other existing player has givenName
    - `isValidPlayerName(game :Dungeon, name :str) -> Boolean`
  #### Step 2: Accept player and add it to game
    - `addPlayer(player: Player, game: Dungeon) -> None`

### Functions for player movement (Validation logic in RuleChecker module):
  - `move(playerName: str, location: tuple)`
  - `interact(playerName: str, location: tuple)`
  - `interactWithEnemy(playerName: str, location: tuple)`
  - `interactWithKey(playerName: str, location: tuple)`
  - `interactWithExit(playerName: str, location: tuple)`
  - `endGame(game: Dungeon)`

### Functions to broadcast updates:
- Send game state to appropriate users
  - `determineAudience() -> None`
  - `createUpdateMsg(dungeon: Dungeon) -> Json`
  - `createErrorMsg(message: str) -> Json`
  - `broadcast(msg: json, addresses: list) -> None`

