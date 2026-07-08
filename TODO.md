- [ ] Management
  - [ ] Create a sub directory
  - [ ] Add some files ??
  - [ ] Yes it is required in the correction

- [ ] Readme
  - [ ] Check the project management part
  - [ ] Description
  - [ ] Instructions 
  - [ ] Resources
  - [ ] Configuration
  - [ ] Highscore
  - [ ] Maze Generation
  - [ ] Implementation
  - [ ] General Software Architecture
  - [ ] Project Management

- [ ] Linter

- [X] Makefile
  - [ ] Add a build target for the package

- [X] Usage: python3 pac-man.py config.json
  - [ ] Allow only one argument (.json config file)
  - [ ] Handle errors gracefully, no crash, no Python traceback

- [ ] JSON Config file
  - [X] Handle comments
  - [X] Fallback to safe defaults in case of errors or invalid keys
  - [ ] Update README.md to explain configuration in details

- [ ] Views
  - [ ] Menus
    - [ ] Main menu
      - [ ] Display highscore
      - [ ] Instructions
      - [ ] Exit

  - [ ] Options menu ? (Not required)

  - [ ] Game view
    - [ ] Current score
    - [ ] Remaining lives
    - [ ] Remaining time
    - [ ] Correction checks
      - [ ] You can move in the maze
      - [ ] You can't cross walls
      - [ ] You can eat pacgums and super pacgums
      - [ ] You can die and re-spawn.

  - [ ] Pause
    - [ ] Resume the game
    - [ ] Return to main (give up)

  - [ ] Game over
    - [ ] Display final score
    - [ ] Highscore: enter player name

  - [ ] Victory
    - [ ] Display final score
    - [ ] Congratulation
    - [ ] Highscore: enter player name


- [ ] Deployment
  - [ ] Deployment to a public gaming platform (Itch.io)
  - [ ] as a free but unlisted/private build
  - [ ] Build as a standalone package
  - [ ] Provide minimal in-package instructions(controls, options, configuration)
  - [ ] Git repository must contain the full source and the packaging script/spec at the root

- [ ] Integrate maze generation
  - [ ] Use as-is
  - [ ] PERFECT = False
  - [ ] Handle errors gracefully

- [ ] Highscore system
  - [ ] JSON File management
    - [ ] Player name: max 10 chars, only alphanumeric and spaces
    - [ ] Score: Only non-negative integers
    - [ ] Store max top 10 highscores
  - [ ] Manage display on screen
  - [ ] Handle empty file
  - [ ] Handle adding new highscores (View, System)
  - [ ] Allow players to enter their name and register new high score
  - [ ] Do not update previous high score of the same name, add new entry

- [ ] Game
  - [ ] Player
    - [ ] Player spawns in the middle
    - [ ] Move with arrow keys or WASD
      - [ ] If necessary, handle AZERTY preset (ZQSD) as an option
    - [ ] Ghost touch player = player loses one life
      - [ ] Player respawns in the middle
      - [ ] For (re)spawning, check if the case is a valid position, if it isn't, find the first valid case to spawn on
    - [ ] Pacgum
      - [ ] Create texture
      - [ ] Spawn in most corridors (3 out of 4 cases?)
      - [ ] Manage counter
    - [ ] Super-Pacgum
      - [ ] Create texture
      - [ ] 1 per corner
      - [ ] Makes ghosts edible for a short time
      - [ ] Eating an edible ghost increases the score by Z points

  - [ ] Ghost
    - [ ] Create algo to move them
      - [ ] Several algos in their class ?
      - [ ] Allow to switch their algo on the fly ?
      - [ ] Hunter on regular
      - [ ] Run away when edible
      - [ ] Variable speed ?
    - [ ] 1 ghost per corner
    - [ ] Respawn
      - [ ] In their corner
      - [ ] After 5 or 10 seconds (variable ?)

  - [ ] Cheat mode
    - [ ] Activation ?
    - [ ] Features
      - [ ] Invincibility (no life lost; ghosts cannot eat the player)
      - [ ] Level skip (immediately win the current level)
      - [ ] Ghost freeze (ghosts stop moving)
      - [ ] Extra lives (add extra lives to the player)
      - [ ] Increased speed (player moves faster)

  - [ ] Game progression
    - [ ] Fixed seed for first level
    - [ ] Random seed for other levels
    - [ ] At least 10 levels
    - [ ] Time limit per level
      - [ ] Display time left
      - [ ] Time ends
        - [ ] Kill Pacman ?
        - [ ] Restart Level ?
        - [ ] Game over ?
    - [ ] Main Menu > start game > Win or Lose > Enter name for highscore > Back to Main Menu
