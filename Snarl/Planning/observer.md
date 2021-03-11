## Observer

### Setup/Teardown Functionality:
The observer can register to look at a game at the beginning. Once they have been registered, they will receive updated from theGame Manager.
- `registerObserver(observerId: str) -> RegistrationResponse`
- `unRegisterObserver(observerId: str) -> RegistrationResponse`
  
- `RegistrationResponse` can be one of: 
  - [0, dungeonState: JSON] 
  - [-1, "failure registering"]
  - [-1, "failure unregistering"] 
  - [0, "successfully unregistered"]

### Observe Functionality:
The Observer may have functionality to look at different components of the game state at any given time. Note, for failure of sending an update, the json half of the tuple would return "null".
- `see(observerId: str) ->  [0, dungeonState: JSON ]`
- `seeLevel(observerId: str, levelNum: int) -> [1, levelState: JSON]`
- `seeBoard(observerId: str, levelNum: int, boardNum: int) -> [2, boardState: JSON]`
- `seePlayer(observerId: str) -> [3, playerState: JSON]`
- `seeEnemies(observerId: str, levelNum: int) -> [4, enemiesState: JSON] `

### Sending Updates Functionality:
Game manager would call on this function to notify the Observer of the updates being broadcast. 
- `updateObserver(observerId: str) -> dungeonState: JSON`





