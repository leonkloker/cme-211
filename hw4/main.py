import sys

import truss

if len(sys.argv) < 3: 
    print("Usage:")
    print(" python3 {} <joints file> <beams file> "\
        "[optional plot output file]".format(sys.argv[0]))
    sys.exit(0)

joints_dir = sys.argv[1]
beams_dir = sys.argv[2]

try:
    t = truss.Truss(joints_dir, beams_dir)
except RuntimeError as e: 
    print('ERROR: {}'.format(e)) 
    sys.exit(2)

if len(sys.argv) > 3:
    t.PlotGeometry(sys.argv[3])
    
print(t)