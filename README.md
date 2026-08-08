*This project has been created as part of the 42 curriculum by [yguardio](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.dogster.com%2Fwp-content%2Fuploads%2F2024%2F03%2FBelgian-Malinois-e1687773644653.jpeg&f=1&nofb=1&ipt=ca1a3f1c8be458d97acbcc912e6c039bae22087c69654d231ae137c8fa62bff8), [flinguen](https://linguenheld.net/)*

## 42_pacman
Ghosts! More ghosts!

### Todo list

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
    - [X] Main menu
      - [X] Display highscore
      - [ ] Instructions
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

- [ ] Game
  - [ ] Player
    - [X] Create texture
    - [X] Player spawns in the middle
    - [X] Move with arrow keys or WASD
      - [X] If necessary, handle AZERTY preset (ZQSD) as an option
    - [X] Ghost touch player = player loses one life
      - [X] Player respawns in the middle
      - [X] For (re)spawning, check if the case is a valid position, if it isn't, find the first valid case to spawn on

  - [ ] Pacgum
    - [X] Create texture
    - [X] Spawn in most corridors (3 out of 4 cases?)
    - [X] Manage counter

  - [ ] Super-Pacgum
    - [X] Create texture
    - [X] 1 per corner
    - [X] Makes ghosts edible for a short time
    - [X] Eating an edible ghost increases the score by Z points

  - [ ] Ghost
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
      - [ ] Level skip (immediately win the current level)
      - [ ] Ghost freeze (ghosts stop moving)
      - [X] Extra lives (add extra lives to the player)
      - [ ] Increased speed (player moves faster)

  - [ ] Game progression
    - [ ] Fixed seed for first level
    - [ ] Random seed for other levels
    - [ ] At least 10 levels
    - [ ] Time limit per level
      - [X] Display time left
      - [ ] Time ends
        - [ ] Kill Pacman ?
        - [ ] Restart Level ?
        - [ ] Game over ?
    - [ ] Main Menu > start game > Win or Lose > Enter name for highscore > Back to Main Menu

  - [] Entity system
    - [X] VEntity ABC, common API for entities
    - [X] VEntityPlayer
    - [ ] VEntityEnemyCommon
    - [ ] VEntityPacgum
    - [ ] VEntitySuperPacgum

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
Highscores work with a JSON file. The [HighScores]() class allows the program to create and open the file.  
To be JSON proof and simple, the file contains a list of dictionaries which contain two entries:
- name of the player
- its score

When the [VWelcome]() view is created, it simply creates a HighScores object, a str cast will return the list of players in a formated str.  
Checks are performed to avoid incorect entries. They are ignored and won't be used in the save process.  

To save a new entry, [VEndBase](), (which is the mother of [VGameOver]() & [VVictory]()) will use the [process_input]() method.  

It will create a HighScore object and save the new one in this process:  
- Open the file and get the current scores in the format: `list[dict[str, str | int]]`
- Add the new one
- Sort the list by name then by score
- Keep the tenth firsts
- Overwrite the JSON file

### Maze Generation

Maze generation is done with the [MazeGeneratorWrapper]() class.  
It's an interface between the maze generated by A-Maze-ing package and our Pacman.  

The purpose is to create a [Maze]() object.
Since we work with sprites and world coordinates, we opted to convert the maze into two set of coordinates:
- One set for walls
- One set for floors

So our interface perform the conversion from a raw maze (matrix of hexadecimal values): 

```
                  0   1   2   3   4

                ┏━━━┳━━━┳━━━┳━━━┳━━━┓
             0  ┃ 6 ┃ A ┃ 5 ┃ 2 ┃ 8 ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━┫
             1  ┃ 1 ┃ 2 ┃ 3 ┃ B ┃ C ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━┫
             2  ┃ 6 ┃ 8 ┃ 9 ┃ A ┃ 2 ┃
                ┗━━━┻━━━┻━━━┻━━━┻━━━┛
```
And:
- Splits all values into nine coordinates to get the walls and the angles and the floors.
- Get their coordinates according to the defined SpriteSize and their coordinates.
- Add add them either in walls or floors according to the hexadecimal value. (0b1111 -> Left|Bottom|Right|Top).
- Reverse the row/col logic to work in X/Y as Arcade does.

```
        raw  ->       0       1       2       3       4
         |
         v  maze  0   1   2   3   4   5   6   7   8   9  10

                ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
             0  ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
         0   1  ┃   ┃ H ┃   ┃ H ┃   ┃ H ┃   ┃ H ┃   ┃ H ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
             2  ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
         1   3  ┃   ┃ H ┃   ┃ H ┃   ┃ H ┃   ┃ H ┃   ┃ H ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
             4  ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
         2   5  ┃   ┃ H ┃   ┃ H ┃   ┃ H ┃   ┃ H ┃   ┃ H ┃   ┃
                ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
             6  ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃
                ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```

These sets are saved in a Maze object, thanks to them, we can create [SpriteLists]() and display our maze.  
Textures are saved in the [VAtlas]() class and contains entries such as:
- "wall_with_floor_on_top"
- "wall_with_floor_on_top_right"
- ...

By looping in the walls set, we can create sprites according to the current coordinate and its environement.  


The last step is used for our algorithm and specialised for floors:  
We create a [dict of neighbours]() `dict[Vec2, list[Vec2]]`.
Each floor entries will contain the list of floors it can access.  
Thanks to the hashmap system, the access of Neighbours has a O(1) complexity.  


### Implementation

What ?

### General Software Architecture



### Project Management
