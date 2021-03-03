## Player

For our player interface, we wanted to keep it as minimal as possible, giving Players only the key information needed to play a game. The functionality available to a “player” will be starting a game or joining a game, moving and interacting with tiles, and finally requesting information from a game manager. 

## Starting a game (Send message to GameManager):
  - `startGame(playerName: str) -> None`
  - `joinGame(playerName: str, gameName: str) -> None`

## Movement/Interaction (Send message to GameManager):
  - `move(playerName: str, location: tuple) -> None`
  - `stayPut(playerName: str) -> None`

## Info a player may request (Receiving message from game manager)
  - `whereAmI(playerName: str) -> Location (tuple)`
  - `howMuchCanISee(playerName:str) -> List[Tiles]`
  - This may be added to depending on pending functionality from Growl, Inc.

