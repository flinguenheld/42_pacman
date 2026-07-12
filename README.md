*This project has been created as part of the 42 curriculum by [yguardio](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.dogster.com%2Fwp-content%2Fuploads%2F2024%2F03%2FBelgian-Malinois-e1687773644653.jpeg&f=1&nofb=1&ipt=ca1a3f1c8be458d97acbcc912e6c039bae22087c69654d231ae137c8fa62bff8), [flinguen](https://linguenheld.net/)*

## 42_pacman
Ghosts! More ghosts!

### Todo list

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
  - [X] Use as-is
  - [X] PERFECT = False
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
    - [X] Create texture
    - [X] Player spawns in the middle
    - [ ] Move with arrow keys or WASD
      - [ ] If necessary, handle AZERTY preset (ZQSD) as an option
    - [ ] Ghost touch player = player loses one life
      - [ ] Player respawns in the middle
      - [ ] For (re)spawning, check if the case is a valid position, if it isn't, find the first valid case to spawn on

  - [ ] Pacgum
    - [X] Create texture
    - [X] Spawn in most corridors (3 out of 4 cases?)
    - [ ] Manage counter

  - [ ] Super-Pacgum
    - [X] Create texture
    - [X] 1 per corner
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

  - [] Entity system
    - [X] VEntity ABC, common API for entities
    - [X] VPlayerEntity
    - [] VGhostEntity
    - [] VPacgumEntity
    - [] VSuperPacgumEntity

### Description

### Instructions
This project uses [UV](https://docs.astral.sh/uv/) for automatic virtual environment management.
Once installed, you can use it with the Makefile with these commands:

```bash
    make install
    make clean
    make lint
```

Command to launch the game:
(a [configuration file](#Configuration) is mandatory)
```bash
uv run python pac-man.py [CONFIG_FILE]
uv run python pac-man.py --help
```

### Configuration

It allows you to override default values.
The file as to be a valid JSON.
All invalid values are ignored.
Here the available keys:
```json
{
  "highscore_filename": "test.txt",
  "lives": 15,
  "pacgum": 42,

  "points_per_ghost": 10,
  "points_per_pacgum": 50,
  "points_per_super_pacgum": 200,

  "seed": 42,
  "level_max_time": 90

  // Comment C
  /* Comment C */
  #  Comment Python
}
```
### Resources
[UV](https://docs.astral.sh/uv/)
[Arcade](https://api.arcade.academy/en/stable/index.html)


### Highscore

### Maze Generation

### Implementation

### General Software Architecture

### Project Management
