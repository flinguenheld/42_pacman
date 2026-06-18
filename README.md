*This project has been created as part of the 42 curriculum by [yguardio](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.dogster.com%2Fwp-content%2Fuploads%2F2024%2F03%2FBelgian-Malinois-e1687773644653.jpeg&f=1&nofb=1&ipt=ca1a3f1c8be458d97acbcc912e6c039bae22087c69654d231ae137c8fa62bff8), [flinguen](https://linguenheld.net/)*

### 42_pacman
Ghosts! More ghosts!

#### Description

#### Instructions

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

#### Configuration

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
#### Resources
[UV](https://docs.astral.sh/uv/)  
[Arcade](https://api.arcade.academy/en/stable/index.html)


#### Highscore

#### Maze Generation

#### Implementation

#### General Software Architecture

#### Project Management
