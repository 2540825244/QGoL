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

#label generator
def label(x, y, t):
    return f'x{x}y{y}t{t}'

#read special variables
board_size_x = 10 #number of steps in x axis
board_size_y = 10 #number of steps in x axis
time = 10 #number of steps in time axis
if sys.argv[1] == "#":
    print("No input file selected")
else:
    try:
        f_input = open(sys.argv[1], "r")
        dict_input = eval(f_input.read())
        board_size_x = dict_input["x"]
        board_size_y = dict_input["y"]
        time = dict_input["t"]
        del dict_input["x"]
        del dict_input["y"]
        del dict_input["t"]
        f_input.close()
    except:
        print("Error reading input file")

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
        f_input = open(sys.argv[1], "r")
        dict_input = eval(f_input.read())
        for var in dict_input:
            if dict_input[var] == 1:
                bqm.set_linear(var, 100)
            elif dict_input[var] == 0:
                bqm.set_linear(var, -100)
            else:
                bqm.set_linear(var, 0)
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
for t in range(time - 1):
    for x in range(board_size_x):
        for y in range(board_size_y):
            #get list of neighbours' label
            neighbour_list = []
            for x_offset in [-1, 0, 1]:
                for y_offset in [-1, 0, 1]:
                    neighbour_list.append(label((x + x_offset) % board_size_x, (y + y_offset) % board_size_y, t))
            neighbour_list.remove(label(x, y, t))
            
            #ideology, so for each scenario, have 3 constraints, tkae into account now, future and both
            #for 3 neighbours alive and current cell dead, future cell must be alive
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 4, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 3, strength=2))
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 4, strength=2))

            #for 2 neighbours alive and current cell alive, future cell must be alive
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 4, strength=2))
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 3, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 3, strength=2))

            #for 3 neighbours alive and current cell alive, future cell must be alive
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 5, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 4, strength=2))
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 4, strength=2))

            #for 0 neighbours alive and current cell alive, future cell must be dead
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 1, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 1, strength=2))
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 0, strength=2))

            #for 0 neighbours alive and current cell dead, future cell must be dead
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 0, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 0, strength=2))
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 0, strength=2))

            #for 1 neighbours alive and current cell alive, future cell must be dead
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 2, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 2, strength=2))
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 1, strength=2))

            #for 1 neighbours alive and current cell dead, future cell must be dead
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 1, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 1, strength=2))
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 1, strength=2))

            #for 2 neighbours alive and current cell dead, future cell must be dead
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 2, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 2, strength=2))
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 2, strength=2))

            #for 4 neighbours alive and current cell dead, future cell must be dead
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 4, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 4, strength=2))
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 4, strength=2))

            #for 4 neighbours alive and current cell alive, future cell must be dead
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 5, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 5, strength=2))
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 4, strength=2))

            #for 5 neighbours alive and current cell dead, future cell must be dead
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 5, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 5, strength=2))
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 5, strength=2))

            #for 5 neighbours alive and current cell alive, future cell must be dead
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 6, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 6, strength=2))
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 5, strength=2))

            #for 6 neighbours alive and current cell dead, future cell must be dead
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 6, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 6, strength=2))
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 6, strength=2))

            #for 6 neighbours alive and current cell alive, future cell must be dead
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 7, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 7, strength=2))
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 6, strength=2))

            #for 7 neighbours alive and current cell dead, future cell must be dead
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 7, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 7, strength=2))
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 7, strength=2))

            #for 7 neighbours alive and current cell alive, future cell must be dead
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 8, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 8, strength=2))
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 7, strength=2))

            #for 8 neighbours alive and current cell dead, future cell must be dead
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 8, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 8, strength=2))
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 8, strength=2))

            #for 8 neighbours alive and current cell alive, future cell must be dead
            bqm.update(combinations([label(x, y, t), label(x, y, t+1)] + neighbour_list, 9, strength=2))
            bqm.update(combinations([label(x, y, t)] + neighbour_list, 9, strength=2))
            bqm.update(combinations([label(x, y, t+1)] + neighbour_list, 8, strength=2))


#solve
time_start = datetime.datetime.now()
sampler = LeapHybridSampler()
sampleset = sampler.sample(bqm, time_limit=60)
time_end = datetime.datetime.now()
print(f"Time taken: {time_end - time_start}")
print(sampleset.first.sample)
print(f"Energy: {sampleset.first.energy}")

#save output to file
try:
    if sys.argv[2] == "#":
        f_output = open("working_folder/output.txt", "w")
    else:
        try:
            f_output = open(sys.argv[1], "w")
        except:
            print("Error writing output file")
            f_output = open("working_folder/output.txt", "w")
except:
    f_output = open("working_folder/output.txt", "w")
    
dict_output = {}
for var in sampleset.first.sample:
    dict_output[var] = sampleset.first.sample[var]
dict_output["x"] = board_size_x
dict_output["y"] = board_size_y
dict_output["t"] = time
f_output.write(str(dict_output))
f_output.close()

