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
  - Upon beginning the game, adversaries will receive a full view of the level.
    
    `receiveLevel(gameName: str) -> EnemyView`
  - Before each turn, the adversary will receive an update with changes made up until their move.
    
    `receiveUpdate(gameName: str, update: json) -> EnemyView`  

### Movement/Interaction (Send message to GameManager):
  - The move method allows the enemy to choose where it would like to go.
    
    `move(enemyName: str, location: tuple) -> None`
  - The stay put method allows an adversary to stay put if it chooses to.
    
    `stayPut(enemyName: str) -> None`
