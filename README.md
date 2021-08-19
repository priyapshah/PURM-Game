# Castle Escape
This is a castle-themed video game used to teach and implement pathfinding algorithms, including
- Breadth First Search
- Depth First Search
- A*
- Iterative Deepening Depth First Search
- Random Maze Generation via Depth First Search

## Getting Started
1. Navigate to a new folder and initialize an empty repository: 
`git init`
2. Clone the repository into the folder:

`git remote add origin https://github.com/priyapshah/PURM-Game.git`

`git pull origin master`

3. Ensure python and pygame are up to date:

[I am using Python 3.9.5](https://www.python.org/downloads/)

[This game requires pygame version 2.0.1 or later.](https://www.pygame.org/wiki/GettingStarted)

4. Run:
`python main.py`

## Documentation
### Main.py
Creates screens, handles movement and screen change events, and controls gameplay.
### Graph.py 
Creates a graph of the board and the defines several pathfinding algorithms.
### Path.py
Creates the colorful path generated as the player travels around the screen.
### Sprites.py
Defines the main player and their abilities.
### Enemy.py
Defines the obstacles that do harm to the player and their movements.
### Wall.py
Defines the objects that makeup the walls and ground of the game board. 
### Instructions.py
Creates the buttons and text used on the starting instructions screen.
### Config.py
Defines several variables used throughout the game, such as colors, speed, and tilemaps.
