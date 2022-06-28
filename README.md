# TETRIS CLONE

## Video Demo: [Demo](https://youtu.be/OH_xnL1LJNU)

## Description:

This project is a small Tetris clone made in Python with the PyGame library. It has all the gameplay features of the original implementation:
- Player score: 
    - The most rows you destroy at once the most score you get.
    - Scoring a Tetris (4 full rows) in sequence gives even more points!
- Faster block dropping if the control is held down.
- Increasing difficulty, via levels, which makes the blocks fall faster and faster.
- Randomly generated blocks. The game tries to stay fair and not generate the same blocks back to back
- Game over and restart.

It also has a small, minimal and colorful UI, respecting the original's design while chosing a cozy color palette.
In game, the UI keeps track of the player's score, the current level and the next block that will be generated.

Finally some small sound effect have been added to enhance the gameplay feel.

### Difficulties encountered:
- Keep the scope of the project small and not overdesign the code
- Finding and implementing the official Tetris rules. It is an extremely famous game and it is easy to think that you know all the rules but some were surprising to me, like the leveling formula or the different ways to handle block rotation.
- This was the first time I used python in a non-trivial project and I had to find my footings a lot with the language at the begining.

### What could be done better (and why it wasn't done):
- Abstract the UI classes and reuse them accross all the UI panels.
    - **Reason**: The game's UI is fairly minimal and does not really need such complex solutions at its current scope.
    - **Cons**: It makes it harder to extend the UI and add more functionality.
- Better sound and audio handling. Right now it is all stored inside module's variables and accessed via a procedure.
    - **Reason**: The game has a very small number of sound effects. Any other solutions felt like over-engineering.
    - **Cons**: Not much. It could be an issue if the game had a larger scope. It also does not keep tracks of which (if) sound is being played, that can result in undesirable outcomes (loud noises).

### Code walkthrough:
- **grid.py (Grid class):**
    - keeps track of the state of the grid of cells. It holds all the data related to free/occupied cells.
    - It provides procedures to: check if a cell is occupied/free, set a cell occupied/free .
    - And finally it checks 2 things every game loop tick:
        - For full rows. If it finds any, removes them and sends a signal that N lines have been completed (via callback).
        - For game over. If the cell at the top-most row is occupied it sends a signal that the game is lost (via callback).
- **input.py (PlayerInput class):**
    - Keeps track of the player's input and the rate at which the game should happen.
    - Registers listeners that want to be notified when input event happens.
    - Throttle input handling to provide a smooth gameplay (via a timer).
- **main.py (GameState and Game classes):**
    - GameState is an enumeration to keep track of which scene to update and render.
    - Game holds the PyGame data and is in charge of keeping the game running, polling events, and calculating the deltaTime for a smooth gameplay.
    - It handles transition between game states and which scene to update and render.
    - It has a few callbacks:
        - onGameLost(): for when the game is lost. It pauses the game and show the correct UI to the player to either replay or exit.
        - onLineScored(): for when N rows have been completed. It then calculates the score to be added to the player's score and if the game's level should be increased.
- **menu.py: (Menu and Button classes):**
    - Button is a simple class that holds UI data, such has the button's color, its prosition and whether it is selected or not. It also renders said button.
    - Menu is the UI for the main menu of the game. It draws the logo, all the available buttons and keep tracks of the button currently overed by the player.
    - When a button is selected by the player, it sets internal state to be picked up by Game on the next game loop tick.
- **playUI.py: (PlayUI class):**
    - UI for when a game is lost.
    - Handles player's choice ot either replay or exit.
- **setup.py:**
    - Boilerplate code for bundling the game in a .exe format.
- **sound.py:**
    - Loads all the required sound effects.
    - Provide a simple interface to play a sound effect with a given name.
- **tetromino.py: (Tetromino class)**
    - It is the unique tetromino the game used. It is "recycled" by reseting its states and by giving it the next block shape.
    - Keeps track of its grid position and its kind (shape).
    - Listens to input events and move to the next desired position after checking if it is available.
    - Handles rotation