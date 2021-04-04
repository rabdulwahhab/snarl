## Adversary Strategies

### Zombies
- If there's a player in the room the zombie lives in, find the one closest to you (based on the distance formula) and move towards it 
    - Of the 4 cardinal locations around you (excluding walls and doors), pick the one that moves you closest to that player
- If there's no players in your room, pick randomly from all possible cardinal moves and move one space around yourself

### Ghosts
- If there's a player in the room the zombie lives in, find the one closest to you (based on the distance formula) and move towards it 
    - Of the 4 cardinal locations around you (including walls and doors), pick the one that moves you closest to that player
- If there's no players in your room, use the distance formula to calculate your distance from all players and continue to move towards a wall until randomly relocated.
- If moving to a wall tile, then teleport to another space in a room within the level randomly