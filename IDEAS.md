- Maze class (MazeGenerator wrapper)
    - Store maze data as Set of 2D coordinates

- Find a good way to deal with sprite size / window size according to the resolution ?

- Add a 'path' ??
    -> A set which contains all coordinates where the player can go ?
    -> Can be useful for enemy algo
    -> Can be useful to add sprites
    -> But maybe strange to have a dict of wall and a set of path ??
    -> Finally we have saved all points like in a list[list[Vec2]] -_-'
                -> But it separates the logic and can be faster for algos...
                -> What do you think about ?
