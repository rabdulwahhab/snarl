## Enemy

Enemies in our system would closely mimic the behavior of 
players save for a few features. They receive the full view of the game like an observer, but not consistent updates from the GameManager. They will make moves through the same
interface that players do.

### Enemy View type 
Similar to our PlayerView and ObserverView, we will be creating an EnemyView which translates the game state
to a viewable representation (to be decided as specifications become more concrete).
    
    EnemyView:
    - name
    - tiles 
    - keyObj
    - exitObj
    - players

### Receiving updates:
  - `receiveLevel(gameName: str) -> EnemyView`
  - `receiveUpdate(gameName: str) -> EnemyView`  

### Movement/Interaction (Send message to GameManager):
  - `move(enemyName: str, location: tuple) -> None`
  - `stayPut(enemyName: str) -> None`
