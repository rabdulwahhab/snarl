## RuleChecker module:

Our rulechecker module can be split into three main pieces of functionality. 

### Player/Enemy movement from one tile to another 
1. Check if the destination given can be moved to
    - `playerCanMoveTo: (destination tuple, Player, Level) -> boolean`
    - `enemyCanMoveTo: (destination tuple, Enemy, Level) -> boolean`

2. Outputs the possible moves for a player given the number of cardinal moves, and the possible moves for an enemy (given the Enemy may have different rules for movement)
    - `playerPossibleMoves: (location tuple, numMoves int, Level) -> [locations]`
   - `enemyPossibleMoves: (location tuple, Enemy, Level) -> [locations]`

3. Checks if moving to the destination will cause an interaction
   - `destHasEnemy: (destination tuple, Player, Level) -> boolean`
   - `destHasPlayer: (destination tuple, Player, Level) -> boolean`
   - `destHasItem: (destination tuple, Player, Level) -> boolean`
   - `destHasKey: (destination tuple, Player, Level) -> boolean`
   
### Player interaction with Enemy/Item/key
1. Dictates the behavior of a player and enemy interaction
   - `playerEnemyInteraction: (Player, Enemy, Level) -> Level`

2. Dictates the behavior of a player and item interaction
   - `playerItemInteraction: (Player, Item, Level) -> Level`

3. Dictates the behavior when a key has been encountered
   - `playerKeyInteraction: (Player, Level) -> Level`
   
### Determining if a Level or game is over
1. Determines whether the level/game is over
   - `isLevelOver: (Level) -> boolean`
   - `isGameOver: (Dungeon) -> boolean`
   
2. Determines if game has been won
   - `isGameWon: (Dungeon) -> boolean`

Together these pieces will encapsulate the rules for gameplay. 
