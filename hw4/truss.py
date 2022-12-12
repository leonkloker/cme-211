import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
import warnings

class Truss:
    """This class can be used to calculate beam forces in
    statically determined trusses."""

    def __init__(self, file_joints, file_beams):
        """This function is the constuctor of the Truss class.

        Args:
            file_joints (str): Name of the input directory containing
            the joint position and external forces.
            file_beams (str): Name of the input directory containing
            the beams of the truss.
        """

        self.read_beams(file_beams)
        self.read_joints(file_joints)
        self.statical_determinancy()
        self.calculate_forces()

    def read_beams(self, filename):
        """This function reads data from the beam data file.

        Args:
            filename (str): Name of the input directory containing
            the beams of the truss.
        """

        # open the file and skip the header line
        file = open(filename, "r")
        next(file)

        # create a dictionary of beams
        self._beams = {}
        for line in file:
            data = line.split()
            data = [int(elem) for elem in data]

            # add a new entry for every beam
            self._beams[data[0]] = data[1:]

        file.close()
        self._nbeams = len(self._beams)

    def read_joints(self, filename):
        """This function reads data from the beam data file.

        Args:
            filename (str): Name of the input directory containing
            the joint position and external forces.
        """

        # open the file and skip the header line
        file = open(filename, "r")
        next(file)

        # create a dictionary of joints
        self._joints = {}
        for line in file:
            data = line.split()
            data = [float(elem) for elem in data]
            data[0] = int(data[0])
            data[-1] = bool(data[-1])

            # add a new entry for every joint
            self._joints[data[0]] = data[1:]

            # add a set of containing beams that
            # are connected to this joint
            self._joints[data[0]].append(set())
            for beam_inx, beam in self._beams.items():
                if data[0] in beam:
                    self._joints[data[0]][-1].add(beam_inx)

        file.close()
        self._njoints = len(self._joints)

    def statical_determinancy(self):
        """This function checks if the truss is statically
        determined, i.e. if the method of joints can be used to
        calculate all beam forces.

        Raises:
            RuntimeError: If the truss is statically indetermined.
        """

        # calculate amount of unknowns
        unknowns = self._nbeams
        for joint in self._joints.values():
            if joint[-2] == 1:
                unknowns += 2
        
        # amount of available equations
        equations = 2 * self._njoints

        if unknowns != equations:
            raise RuntimeError("Truss geometry not suitable for static "\
                "equilibrium analysis")

    def __repr__(self):
        representation = " Beam       Force\n"
        representation += "-----------------\n"""

        # add a new line containing the force in every beam
        for beam_inx in self._beams:
            representation += "    {}      {: .3f}\n".format(beam_inx, self._forces[beam_inx-1])

        return representation

    def calculate_forces(self):
        """This function calculates the forces in all the beams and
        the reaction forces.

        Raises:
            RuntimeError: If the linear equation system resulting from the 
            method of joints is singular.
        """

        # initialize lists for creation of
        # sparse matrix and load vector
        matrix_entries = []
        row_indices = []
        column_indices = []
        load_vector = np.zeros((2*self._njoints, 1))

        # count the amount of supports in the truss
        nsupports = 0

        for joint_inx, joint in self._joints.items():

            # iterate over all beams connected to this joint
            for beam_inx in joint[-1]:

                # calculate the x and y components of the normal
                # beam force
                x_proj, y_proj = self.get_xy_component(beam_inx, joint_inx)

                # add the beam forces to the sparse matrix
                matrix_entries.append(x_proj)
                matrix_entries.append(y_proj)

                row_indices.append(2*(joint_inx-1))
                column_indices.append(beam_inx-1)
                row_indices.append(2*(joint_inx-1)+1)
                column_indices.append(beam_inx-1)
                    
            # get the external forces at the joint and add
            # them to the load vector
            f_x, f_y = joint[2], joint[3]

            load_vector[2*(joint_inx-1)] = -f_x
            load_vector[2*(joint_inx-1)+1] = -f_y

            # if the joint has zero displacement, add the 
            # reaction forces to the sparse matrix
            if joint[4] == 1:
                matrix_entries.append(1)
                matrix_entries.append(1)

                row_indices.append(2*(joint_inx-1))
                column_indices.append(self._nbeams + 2*nsupports)
                row_indices.append(2*(joint_inx-1)+1)
                column_indices.append(self._nbeams + 2*nsupports+1)

                nsupports += 1

        # create the sparse matrix from the data and index lists
        self._A = csr_matrix((matrix_entries, (row_indices, column_indices)))
        self._b = load_vector

        # solve the equation system if possible
        try:
            warnings.filterwarnings('error')
            self._forces = spsolve(self._A, self._b)
        except:
            raise RuntimeError("Cannot solve the linear system, unstable truss?")
            
    def get_xy_component(self, beam_inx, joint_inx):
        """This function calculates the component of normal
        beam force in beam beam_inx in the x and y direction.

        Args:
            beam_inx (int): Index of the beam whose force
            should be calculated.
            joint_inx (int): Index of the joint at which the
            equilibrium equations are currently considered.

        Returns:
            x_proj (float): x component of the beam force.
            y_proj (float): y component of the beam force.
        """

        # save the x and y positions of the joints the beam is attached to
        J_x = []
        J_y = []

        for joint in self._beams[beam_inx]:
            J_x.append(self._joints[joint][0])
            J_y.append(self._joints[joint][1])

        # calculate the x and y component of the beam normal force vector
        x_proj = (J_x[1] - J_x[0]) / math.sqrt((J_x[1] - J_x[0])**2 +
        (J_y[1] - J_y[0])**2)
        y_proj = (J_y[1] - J_y[0]) / math.sqrt((J_x[1] - J_x[0])**2 +
        (J_y[1] - J_y[0])**2)

        # if the equilibirum equations are considered at the first 
        # joint the beam is connected to, change the signs of the projection
        if joint_inx != self._beams[beam_inx][1]:
            x_proj, y_proj = -x_proj, -y_proj

        return x_proj, y_proj

    def PlotGeometry(self, figure_name):
        """This function plots the truss geometry and saves it 
        to a file.

        Args:
            figure_name (str): Name of the output directory in which
            the figure is saved.
        """

        plt.figure()

        # add every beam to the plot
        for beam in self._beams.values():
            plt.plot([self._joints[beam[0]][0], self._joints[beam[1]][0]],
            [self._joints[beam[0]][1], self._joints[beam[1]][1]], color='blue')

        plt.margins(0.1)
        plt.savefig(figure_name)
