'''
Quantum annealing game of life
using D-Wave's quantum annealer (BQM)
many binary variables, named in format x{i}y{j}t{k}, for the 3 axis, x and y are the coordinates, t is the time
each variable represent if the cell is alive or dead at that time
1 is alive, 0 is dead, (2 is unknown)
customisable board size and time
coordinates start from 0 to selected size - 1 (inclusive)
the edge cells are considered to be neighbours with the opposite edge cell
the input and output are done by a dictionary of {variable name: value} (value in 1, 0 or 2, not boolean), special variables of x and y and t are used to specify the board size and time
using system argument to select input and output file
first argument is input file, second argument is output file
use # to show no file selected for input or output
if no input file is selected, the states are all biased to 0
if no output file is selected, the states are saved to "output.txt"
'''

#import modules
from dimod import BinaryQuadraticModel
from dimod.generators.constraints import combinations
from dwave.system import LeapHybridSampler
import datetime
import sys

#customisable variables
board_size_x = 10 #number of steps in x axis
board_size_y = 10 #number of steps in x axis
time = 10 #number of steps in time axis

#label generator
def label(x, y, t):
    return f'x{x}y{y}t{t}'

#initialise model
bqm = BinaryQuadraticModel.empty('BINARY')
var_list = [label(x, y, t) for x in range(board_size_x) for y in range(board_size_y) for t in range(time)]
for var in var_list:
    bqm.add_variable(var, 0)

#read input (if any)
if sys.argv[1] == "#":
    print("No input file selected")
    for var in var_list:
        bqm.set_linear(var, -10)
else:
    try:
        f_input = open(sys.argv[2], "r")
        dict_input = eval(f_input.read())
        for var in dict_input:
            if var == "x":
                board_size_x = dict_input[var]
            elif var == "y":
                board_size_y = dict_input[var]
            elif var == "t":
                time = dict_input[var]
            else:
                bqm.set_linear(var, dict_input[var])
        f_input.close()
    except:
        print("Error reading input file")
        for var in var_list:
            bqm.set_linear(var, -10)

#output the input and ask for confirmation
print("Input:")
print(f"Board size: {board_size_x}x{board_size_y}")
print(f"Time: {time}")
for t in range(time):
    print(f"Time step {t}:")
    for y in range(board_size_y):
        for x in range(board_size_x):
            print(bqm.get_linear(label(x, y, t)), end=" ")
        print()
    print()
print("Confirm? (y/n) [n]")
if input() != "y":
    exit()


#add constraints
for t in range(time):
    for x in range(board_size_x):
        for y in range(board_size_y):
            #each cell must be alive or dead
            bqm.add_linear_equality_constraint([label(x, y, t)], constant=-1)
            #each cell must be alive or dead in the next time step
            bqm.add_linear_equality_constraint([label(x, y, t), label(x, y, (t + 1) % time)], constant=-1)
            #each cell must have 2 or 3 neighbours to be alive
            bqm.add_linear_inequality_constraint([label(x, y, t), label((x - 1) % board_size_x, y, t), label((x + 1) % board_size_x, y, t), label(x, (y - 1) % board_size_y, t), label(x, (y + 1) % board_size_y, t)], constant=-2)
            #each cell must have 3 neighbours to be alive in the next time step
            bqm.add_linear_inequality_constraint([label(x, y, t), label((x - 1) % board_size_x, y, t), label((x + 1) % board_size_x, y, t), label(x, (y - 1) % board_size_y, t), label(x, (y + 1) % board_size_y, t), label(x, y, (t + 1) % time)], constant=-3)
            #each cell with more than 3 neighbours must be dead in the next time step
            bqm.add_linear_inequality_constraint([label(x, y, t), label((x - 1) % board_size_x, y, t), label((x + 1) % board_size_x, y, t), label(x, (y - 1) % board_size_y, t), label(x, (y + 1) % board_size_y, t), label(x, y, (t + 1) % time)], constant=3)
            #each cell with less than 2 neighbours must be dead in the next time step
            bqm.add_linear_inequality_constraint([label(x, y, t), label((x - 1) % board_size_x, y, t), label((x + 1) % board_size_x, y, t), label(x, (y - 1) % board_size_y, t), label(x, (y + 1) % board_size_y, t), label(x, y, (t + 1) % time)], constant=2)

#solve
time_start = datetime.datetime.now()
sampler = LeapHybridSampler()
sampleset = sampler.sample(bqm, time_limit=60)
time_end = datetime.datetime.now()
print(f"Time taken: {time_end - time_start}")
print(sampleset.first.sample)
print(f"Energy: {sampleset.first.energy}")

#save output to file
if sys.argv[1] == "#":
    f_output = open("working_folder/output.txt", "w")
else:
    try:
        f_output = open(sys.argv[1], "w")
    except:
        print("Error writing output file")
        f_output = open("working_folder/output.txt", "w")

dict_output = {}
for var in sampleset.first.sample:
    dict_output[var] = sampleset.first.sample[var]
dict_output["x"] = board_size_x
dict_output["y"] = board_size_y
dict_output["t"] = time
f_output.write(str(dict_output))
f_output.close()

