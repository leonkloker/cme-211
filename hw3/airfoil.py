import math
import os

from glob import glob
from re import findall

class Airfoil:
    """This class can be used to handle airfoil data and compute
    key properties such as lift coefficient and stagnation point.
    """

    def __init__(self, inputdir):
        """This function is the constuctor of the Airfoil class.

        Args:
            inputdir (str): Name of the input directory containing
            the xy and pressure date of the airfoil.

        Raises:
            RuntimeError: If the input directory does not exist.
        """

        # check if the given input directory exists
        if not os.path.exists(inputdir):
            raise RuntimeError("Directory {} does not exist!".format(inputdir))
        
        # add trailing backslash
        if inputdir[-1] != "/":
            inputdir = inputdir + "/"

        self._inputdir = inputdir

        # the data is read from the position and pressure files
        self.read_xy_data()
        self.read_pressure_data()

        # the data is used to calculate resulting forces, 
        # lift coefficients and stagnation points
        self.calculate_chord_length()
        self.integrate_pressures()
        self.calculate_lift()
        self.calculate_stagnation_points()

    def read_xy_data(self):  
        """
        This function reads the airfoil geometry from the xy.dat file
        in the input directory.

        Raises:
            RuntimeError: If there is no xy.dat file in the input directory.
        """

        filepath = self._inputdir + "xy.dat"

        if not os.path.exists(filepath):
            raise RuntimeError("""File xy.dat does not exist in directory \
            {} !""".format(self._inputdir))
        
        self._xy = []

        # read xy data from file
        file = open(filepath, "r")
        next(file)
        for line in file:
            self._xy.append([float(elem) for elem in line.split()])
    
    def read_pressure_data(self):
        """
        This function reads the pressure field from the data files
        in the input directory.

        Raises:
            RuntimeError: If there is no pressure data file in the input directory.
                          If there are not as many pressure values as required
                          by the airfoil geometry in the file.
        """

        self._pressures = {}

        # iterate over all pressure files
        for filename in glob(self._inputdir + "alpha*", recursive=False):

            # find the value of the angle of attack in the filename
            alpha = float(findall(r"[-+]?(?:\d*\.\d+|\d+)", filename)[-1])

            # open file and skip first line
            file = open(filename, "r")
            next(file)

            pressures = []
            
            for line in file:
                pressures.append(float(line))

            # save pressures for this alpha
            self._pressures[alpha] = pressures

            if len(self._pressures[alpha]) < len(self._xy)-1:
                raise RuntimeError("""More panels than pressure coefficients \
                specified for alpha = {}!""".format(alpha))

            if len(self._pressures[alpha]) > len(self._xy)-1:
                raise RuntimeError("""More pressure coefficients than panels \
                specified for alpha = {}!""".format(alpha))
                
        if len(self._pressures) == 0:
            raise RuntimeError("""No pressure files found in directory {} !\
            """.format(self._inputdir))
    
    def calculate_chord_length(self):
        """
        This function calculates the chord length of the airfoil.
        """

        # initialize max and min x values
        max_x = self._xy[0][0]
        min_x = max_x

        # iterate over all points in the triangulation
        for point in self._xy:
            if point[0] > max_x:
                max_x = point[0]
            if point[0] < min_x:
                min_x = point[0]
        
        self._chord_length = max_x - min_x


    def calculate_force(self, p1, p2, c_p):
        """
        This function calculates the resulting forces of one panel
        of the airfoil geometry.

        Args:
            p1 (list): x and y values of first point.
            p2 (list): x and y values of second point.
            c_p (float): Pressure coefficient at panel.
        """

        return [-(p2[1] - p1[1]) * c_p / self._chord_length, 
        (p2[0] - p1[0]) * c_p / self._chord_length]

    def integrate_pressures(self):
        """
        This function integrates the pressure forces along the airfoil boundary.
        """

        self._cx = {}
        self._cy = {}

         # iterate over all alpha
        for alpha in self._pressures:
            self._cx[alpha] = 0
            self._cy[alpha] = 0

            # calculate the resulting pressure forces by integrating
            # over the airfoil boundary
            for i in range(0, len(self._pressures[alpha])):
                force = self.calculate_force(self._xy[i], self._xy[i+1], 
                self._pressures[alpha][i])
                self._cx[alpha] += force[0]
                self._cy[alpha] += force[1]

    def calculate_lift(self):
        """
        This function calculates the lift coefficient for each angle of attack.
        """

        self._cl = {}
        for alpha in self._pressures:
            self._cl[alpha] = self._cy[alpha] * math.cos((alpha/360)*2*math.pi) \
            - self._cx[alpha] * math.sin((alpha/360)*2*math.pi)

    def calculate_stagnation_points(self):
        """
        This function finds the stagnation point for each angle of attack.
        """

        self._stagnation_points = {}


        for alpha in self._pressures:

            # find the panel of maximal pressure
            max_pressure = max(self._pressures[alpha])
            index = self._pressures[alpha].index(max_pressure)

            # calculate the stagnation point as the center of the panel
            stagnation_point = [(self._xy[index][0] + self._xy[index+1][0])/2, 
            (self._xy[index][1] + self._xy[index+1][1])/2, max_pressure]
            self._stagnation_points[alpha] = stagnation_point

    def get_xy_data(self):
        """This function is a getter for the airfoil geometry.
        
        Returns:
            list: Contains all the points defining the airfoil boundary.
        """
        return self._xy

    def get_pressure_data(self):
        """This function is a getter for the pressure distribution along
        the airfoil boundary for varying angles of attack.
        
        Returns:
            dict: Contains list of pressure values for each alpha.
        """
        return self._pressures

    def get_stagnation_points(self):
        """This function is a getter for the stagnation points for
        each angle of attack.
        
        Returns:
            dict: Contains stagnation point position and pressure value
            for each alpha.
        """
        return self._stagnation_points
    
    def get_lift_coefficients(self):
        """This function is a getter for the lift coefficient for each alpha.
        
        Returns:
            dict: Contains c_l for each alpha.
        """
        return self._cl

    def __repr__(self):
        representation = "alpha     cl           stagnation pt\n"
        representation += "-----  -------  -----------------------------\n"""
         
        # add relevant information for each angle of attack to output
        for alpha in sorted(self._cl.keys()):
            representation += """{: .2f}  {: .4f}  ( {: .4f},  {: .4f})  {: .4f}\n""".format(
                float(alpha), self._cl[alpha], *self._stagnation_points[alpha])

        return representation
