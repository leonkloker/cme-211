import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import sys

def load_data(file):
    """This function loads numerica data from a file.
    
    Args:
        - string file: File to be read from.
        
    Returns:
        - list data: List containing the rows in the file.
    """

    file = open(file, "r")
    data = []

    for line in file:
        row = [float(i) for i in line.split()]
        data.append(row)

    file.close()
    return data

if __name__ == "__main__":
    
    # Check if enough input arguments are given
    if len(sys.argv) < 3: 
        print("Usage:")
        print(" python3 {} <input file> <solution file> ".format(sys.argv[0]))
        sys.exit(0)

    # Read input arguments
    input_file = sys.argv[1]
    solution_file = sys.argv[2]
    print("Input file processed: " + input_file)

    # Load steady-state solution and parameters from files
    scalar_field = np.array(load_data(solution_file))
    scalar_field = np.append(scalar_field, np.reshape(scalar_field[:,0], (-1,1)), 1)
    parameters = load_data(input_file)

    # Calculate mean temperature
    mean_temperature = np.mean(scalar_field)
    print("Mean Temperature: {:.5f}".format(mean_temperature))

    # Define grids for visualization
    x = np.linspace(0, parameters[0][0], scalar_field.shape[1]+1)
    y = np.linspace(0, parameters[0][1], scalar_field.shape[0]+1)
    xv, yv = np.meshgrid(x, y)

    x = np.linspace(0, parameters[0][0], scalar_field.shape[1])
    y = np.linspace(0, parameters[0][1], scalar_field.shape[0])
    xv2, yv2 = np.meshgrid(x, y)

    # Visualize the steady-state solution
    plt.figure()
    plt.pcolor(xv, yv, scalar_field, cmap="jet")
    plt.colorbar()
    plt.xlim([0, parameters[0][0]])
    plt.ylim([0, parameters[0][1]])
    plt.xlabel("X")
    plt.ylabel("Y")

    # Plot the isoline of the mean temperature
    plt.contour(xv2, yv2, scalar_field, [mean_temperature], colors=["k"], linewidths=[3])
    plt.show()
    plt.savefig("visualization_{}_iteration{}.png".format(input_file[:-4], solution_file[-7:-4]))
