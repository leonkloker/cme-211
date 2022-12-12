import numpy as np
import sys

if __name__ == "__main__":

    # check if enough command line arguments are provided
    if len(sys.argv) < 3: 
        print('Usage:')
        print('$python3 {} <maze file> <solution file>'.format(sys.argv[0]))
        sys.exit(0)

    maze_filename = sys.argv[1]
    sol_filename = sys.argv[2]

    # read maze size from first line
    maze_file = open(maze_filename, "r")
    maze_size = [int(elem) for elem in maze_file.readline().split()]
    maze = np.zeros(maze_size)

    # intialize maze array
    for line in maze_file:
        data = [int(elem) for elem in line.split()]
        maze[data[0], data[1]] = 1
    
    maze_file.close()

    sol_file = open(sol_filename, "r")

    # get starting position of the solution
    pos = [int(elem) for elem in sol_file.readline().split()]
    old_pos = pos

    # if start isnt at the top, solution is incorrect
    if (pos[0] != 0):
        print("Maze solution path does not start at the top!")
        sys.exit(0)
    
    # iterate over all steps of the solution path
    for line in sol_file:

        pos = [int(elem) for elem in line.split()]

        # calculate the vertical and horizontal movement
        vertical_move = abs(old_pos[0] - pos[0])
        horizontal_move = abs(old_pos[1] - pos[1])

        # check for all possible failure cases of the solution path
        if vertical_move > 1:
            print("Solution includes vertical jumps!")
            sys.exit(0)

        if horizontal_move > 1:
            print("Solution includes horizontal jumps!")
            sys.exit(0)

        if horizontal_move == 1 and vertical_move == 1:
            print("Solution includes diagonal steps!")
            sys.exit(0)

        if maze[pos[0],pos[1]] == 1:
            print("Solution includes walking through walls!")
            sys.exit(0)
        
        old_pos = pos
    
    sol_file.close()

    # check if the solution path ends at the bottom of the maze
    if pos[0] < maze_size[0]-1:
        print("Solution doesnt end at the bottom of the maze!")
    
    print("Solution is correct!")
