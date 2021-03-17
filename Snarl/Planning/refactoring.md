## Refactor Plans

- Create refactor branch, push existing branches onto it.
- Convert the list of tiles in Board --> Map of Map of tiles (row, col)
- Change our coordinate system from x, y --> row, col like how input is received
- Build a solid exampleLevel that we can reuse in future tests
- Edit our tests to work again after refactoring for tiles (test harnesses + integration tests)
- Update hallway representation to have waypoints???
- Update tile representation to not have `hasKey`  
- Edit Render module to work with new tile representation
- Add documentation


## Summary of Changes

Our sole focus and biggest change was to uproot the way that we were previously representing tiles in the Board (Room | Hallway) from a list of tiles to a dictionary of row numbers which are dictionaries of column number to Tile. This was a ground-breaking change, so we have had to keep track of and update all places that would be impacted (i.e. directly used the board tiles array). 

Our new implementation of tiles is represented as the following, giving the board knowledge of tile location rather than keeping location at a Tile level.

    {rowNum: {colNum: Tile, colNum: Tile ...},
     rowNum: {colNum: Tile, colNum: Tile ...},
    ...}

Places that we needed to modify to adapt to the new implementation of tiles were:
0. Types: Board
1. Util (whichBoardInLevel)
2. Converting Boards
3. Create
4. RuleChecker
5. testLevel
6. testState

In completing these changes, though tedious, we began seeing the fruits of our labor when looking up what board a tile lived on, and other commonly used functions were able to be condensed into more efficient implementations. 

Additionally, we changed our coordinate system from an x, y (columns, rows) system to a (rows, columns) implementation in order to align with many of the specs we received over time. This change affected our Render and some of our existing tests, but we were able to refactor those to be fully functioning once again!

The final change we felt was necessary was going in to document our code, something that we were lacking in previous assignments. Though this was not a change that resolved any technical debt, we hope this will be helpful when we go back to pieces of code we may have written towards the start of the project. 

Some changes we had planned and decided not to continue with were differentiating our Board type into a Hallway type and a Room type. However, we felt that including waypoints was a small enough change that we did not want to change the structure of our code when we could account for waypoints without adding a unique type for Hallways. 

Overall, the refactor week gave us time to implement some necessary changes and create a solid test Game to ease in testing our code in the future. We anticipate our changes will serve us well as we continue building out Snarl.  

