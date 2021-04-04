## How to Run

Our version of Snarl has a GUI which means that it must be run on the VGI machines. 

Once logged into the Khoury machines with a graphical display, you will need to setup the python virtual environment and install the few dependencies. All of this is done automatically by the executable. 

There is a setup script that will initialize the `localSnarl` executable and thereafter allow you to run `./localSnarl` with desired arguments. 

When that is complete, you can launch the game from the command line by running the executable which is in the `local` directory. It will open a window with the game. If needed, the window can be resized to accommodate your viewing comfort. 

The game is played by clicking where you want to move. A status bar at the top of the screen will tell you whose turn it is and when the exit is unlocked. Registered clicks will advance the game.

When the game is over (either won or lost), the window will close automatically and print a message to the console. Right now, the message is not very specific but it should suffice given that you have played the game and witnessed the outcome.
