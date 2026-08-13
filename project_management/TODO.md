# Project Management

To complete our project, we first created a *todo list* with all required point in the subject.  

Then we followed this process:
  - Get a task
  - Write some code / updates
  - Commit / push in a separated branch
  - Ask a review & refactor
  - If ok, merge in the dev branch
  - Refactor again

A more advanced system such a Kanban looked too much for this project.  

### Todo list

- [ ] Readme
  - [ ] Check the project management part
  - [X] Description
  - [X] Instructions
  - [X] Resources
  - [X] Configuration
  - [X] Highscore
  - [X] Maze Generation
  - [X] Implementation
  - [X] General Software Architecture
  - [X] Project Management

- [X] Linter

- [X] Makefile
  - [ ] Add a build target for the package

- [X] Usage: python3 pac-man.py config.json
  - [X] Allow only one argument (.json config file)
  - [X] Handle errors gracefully, no crash, no Python traceback

- [X] JSON Config file
  - [X] Handle comments
  - [X] Fallback to safe defaults in case of errors or invalid keys
  - [X] Update README.md to explain configuration in details

- [X] Views
  - [X] Menus
    - [X] Main menu
      - [X] Display highscore
      - [X] Instructions
      - [X] Exit

  - [X] Game view (HUD)
    - [X] Current score
    - [X] Remaining lives
    - [X] Remaining time
    - [ ] Correction checks
      - [X] You can move in the maze
      - [X] You can't cross walls
      - [X] You can eat pacgums and super pacgums
      - [X] You can die and re-spawn.

  - [X] Pause
    - [X] Resume the game
    - [X] Link to instructions
    - [X] Return to main (give up)

  - [X] Game over
    - [X] Display final score
    - [X] Highscore: enter player name
      - [X] Max 10 characters, alphanumeric and spaces only

  - [X] Victory
    - [X] Display final score
    - [X] Congratulation
    - [X] Highscore: enter player name
      - [X] Max 10 characters, alphanumeric and spaces only

- [ ] Deployment
  - [ ] Deployment to a public gaming platform (Itch.io)
  - [ ] as a free but unlisted/private build
  - [ ] Build as a standalone package
  - [ ] Provide minimal in-package instructions(controls, options, configuration)
  - [ ] Git repository must contain the full source and the packaging script/spec at the root

- [X] Integrate maze generation
  - [X] Use as-is
  - [X] PERFECT = False
  - [X] Handle errors gracefully

- [X] Highscore system
  - [X] JSON File management
    - [X] Player name: max 10 chars, only alphanumeric and spaces
    - [X] Score: Only non-negative integers
    - [X] Store max top 10 highscores
  - [X] Manage display on screen
  - [X] Handle empty file
  - [X] Handle adding new highscores (View, System)
  - [X] Allow players to enter their name and register new high score
  - [X] Do not update previous high score of the same name, add new entry

- [X] Game
  - [X] Player
    - [X] Create texture
    - [X] Player spawns in the middle
    - [X] Move with arrow keys or WASD
      - [X] If necessary, handle AZERTY preset (ZQSD) as an option
    - [X] Ghost touch player = player loses one life
      - [X] Player respawns in the middle
      - [X] For (re)spawning, check if the case is a valid position, if it isn't, find the first valid case to spawn on

  - [X] Pacgum
    - [X] Create texture
    - [X] Spawn in most corridors (3 out of 4 cases?)
    - [X] Manage counter

  - [X] Super-Pacgum
    - [X] Create texture
    - [X] 1 per corner
    - [X] Makes ghosts edible for a short time
    - [X] Eating an edible ghost increases the score by Z points

  - [X] Ghost
    - [X] Create algo to move them
      - [X] Different variants and behaviors
        - [X] Johnny: Chase the player
        - [X] Michael: Block the player
        - [X] Charlie: Follow the player with a delay
        - [X] ReverseMichael: Block the player but on the opposite direction
      - [X] Hunter on regular
      - [X] Run away when edible
      - [X] Variable speed ?
    - [X] 1 ghost per corner
    - [X] Respawn
      - [X] In their corner
      - [X] After 5 or 10 seconds (variable ?)

  - [ ] Cheat mode
    - [ ] Features
      - [X] Invincibility (no life lost; ghosts cannot eat the player)
      - [X] Level skip (immediately win the current level)
      - [ ] Ghost freeze (ghosts stop moving)
      - [X] Extra lives (add extra lives to the player)
      - [ ] Increased speed (player moves faster)

  - [ ] Game progression
    - [X] Fixed seed for first level
    - [X] Random seed for other levels
    - [X] At least 10 levels
    - [X] Time limit per level
      - [X] Display time left
      - [ ] Time ends
        - [ ] Kill Pacman ?
        - [ ] Restart Level ?
        - [ ] Game over ?
    - [X] Main Menu > start game > Win or Lose > Enter name for highscore > Back to Main Menu

  - [X] Entity system
    - [X] Common API for entities
    - [X] VEntityPlayer
    - [X] VEntityEnemyCommon
    - [X] VEntityPacgum
    - [X] VEntitySuperPacgum
