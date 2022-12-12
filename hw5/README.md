The problem is to compute a path through a maze, which is given in a file,
by using the right-hand wall follower algorithm. The C++ code that calculates
the path through the maze starts by reading the maze from the file. A 2d boolean
array is used to save if there is a wall or not at every position in the maze.
Once the maze is read from the file, the input of the maze at the top is found.
After that, the code starts walking through the maze by just trying to turn
right if possible. If not, going straight, going left and turning around
are the next choices in that order. This is done until the bottom of the maze
is reached. At every step, the current position is written to the solution file.

The checksoln.py file can afterwards be used to check if the solution path is valid.
Therefore, the maze is loaded from the given file again. Then the solution path 
is checked step by step, starting with the starting position. If at any point of
the path, there is a vertical or horizontal jump or a diagonal move, the path
is invalid. Moreover, it is checked if every position of the path is actually
walkable and not occupied by a wall. At the end, the last position of the
path must be at the lower end of the maze. If all that is the case, the solution
path is deemed valid.

$ ./mazesolver cme211-hw5-files/maze1.txt solution1.txt
$ python3 checksoln.py cme211-hw5-files/maze1.txt solution1.txt
Solution is correct!

Time spent: 5 hours.
