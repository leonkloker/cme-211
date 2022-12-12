#include <fstream>
#include <iostream>
#include <string>

// maximum size of the maze
#define MAX_SIZE 201

int main(int argc, char **argv){

    // check if enough command line arguments are provided
    if (argc < 3){
        std::cout << "Usage: " << std::endl;
        std::cout << " ./mazesolver <maze file> <solution file> " << std::endl;
        return 0;
    }
    
    // initialize static bool array for the maze
    static bool maze[MAX_SIZE][MAX_SIZE] = {false};

    std::ifstream file (argv[1]);
    int nrow, ncol, row, col;

    // check the maze size
    file >> nrow >> ncol;
    if ((nrow > MAX_SIZE) || (ncol > MAX_SIZE)){
        std::cout << "Maze is too big!" << std::endl;
        return 0;
    }

    // construct the maze from file
    while (file >> row >> col){
        maze[row][col] = true;
    }

    file.close();

    // output file for the maze solution
    std::ofstream file_out (argv[2]);

    // declare current position, trial position,
    // old direction
    int pos[2];
    int trial_pos[2];
    int old_dir = 0;
    bool entrance = false;

    // find the entrance to the maze
    for (int i = 0; i < ncol; i++){
        if (!maze[0][i]){
            pos[0] = 0;
            pos[1] = i;
            entrance = true;
        }
    }

    // stop if maze doesnt have an entrance
    if (!entrance){
        std::cout << "Maze has no entrance!" << std::endl;
        return 0;
    }

    file_out << pos[0] << " " << pos[1] << std::endl;

    // define the order of directions to go given the old direction
    int trial_directions[4][4][2] = {{{0,-1},{1,0},{0,1},{-1,0}}, // when moving down
                        {{-1,0},{0,-1},{1,0},{0,1}}, // when moving left
                        {{0,1},{-1,0},{0,-1},{1,0}}, // when moving up
                        {{1,0},{0,1},{-1,0},{0,-1}}, // when moving right
						};

    // define the new direction you are going when not being blocked
    int new_directions[4][4] = {{1,0,3,2},{2,1,0,3},{3,2,1,0},{0,3,2,1}};

    // go as long as you are not at the bottom
    while (pos[0] < nrow-1){

        // check all 4 trial directions
        for (int trial_dir = 0 ; trial_dir < 4 ; trial_dir++) {
            trial_pos[0] = pos[0] + trial_directions[old_dir][trial_dir][0];
			trial_pos[1] = pos[1] + trial_directions[old_dir][trial_dir][1];
            
            // if a path is free, go there and update position and direction
			if (!maze[trial_pos[0]][trial_pos[1]]) {
				pos[0] = trial_pos[0];
                pos[1] = trial_pos[1];
                old_dir = new_directions[old_dir][trial_dir];
				file_out << pos[0] << " " << pos[1] << std::endl;
				break;
			}
		}
    }

    file_out.close();

    return 0;
}
