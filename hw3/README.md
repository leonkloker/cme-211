The airfoil class can be used to read and process data from airfoils. The constructor
takes a directory as input, which should contain a xy.dat and at least one alpha3.0.dat
files which contain a triangulation of the airfoil boundary and the pressure coefficient 
distribution on this triangulation, respectively. The class than automatically calculates 
the resulting forces on the airfoil, the lift coefficient and the stagnation point based 
on this data. In order to do so, the functionality of the class is decomposed into two
data reading and several calculation methods, representing the logical steps in calculating 
the lift coefficient and stagnation points. Moreover, the calculated quantities and the 
data can be accessed via getter methods.

$ python3 main.py naca0012
alpha     cl           stagnation pt
-----  -------  -----------------------------
-3.00  -0.3622  (  0.0030,   0.0094)   0.9906
 0.00   0.0000  (  0.0000,   0.0000)   0.9944
 3.00   0.3622  (  0.0030,  -0.0094)   0.9906
 6.00   0.7234  (  0.0099,  -0.0170)   0.9967
 9.00   1.0827  (  0.0219,  -0.0246)   0.9977

Time spent 6 hours.
