"""
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
"""

# import modules
from dimod import BinaryQuadraticModel
from dimod.generators.constraints import combinations
from dwave.system import LeapHybridSampler, DWaveSampler, EmbeddingComposite
import datetime
import sys
from display_state_file import display_state_file
from neal import SimulatedAnnealingSampler


# label generator
def label_cell(x, y, t):
    return f"x{x}y{y}t{t}"


def label_more_than_3_neighbours(x, y, t):
    return f"x{x}y{y}t{t}m3"

def label_less_than_2_neighbours(x, y, t):
    return f"x{x}y{y}t{t}l2"

def label_2_neighbours(x, y, t):
    return f"x{x}y{y}t{t}2"

def label_3_neighbours(x, y, t):
    return f"x{x}y{y}t{t}3"


# read special variables
board_size_x = 10  # number of steps in x axis
board_size_y = 10  # number of steps in x axis
time = 10  # number of steps in time axis
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

# initialise model
bqm = BinaryQuadraticModel.empty("BINARY")
var_list_cell = [
    label_cell(x, y, t)
    for x in range(board_size_x)
    for y in range(board_size_y)
    for t in range(time)
]
var_list_more_than_3_neighbours = [
    label_more_than_3_neighbours(x, y, t)
    for x in range(board_size_x)
    for y in range(board_size_y)
    for t in range(time)
]
var_list_less_than_2_neighbours = [
    label_less_than_2_neighbours(x, y, t)
    for x in range(board_size_x)
    for y in range(board_size_y)
    for t in range(time)
]
var_list_2_neighbours = [
    label_2_neighbours(x, y, t)
    for x in range(board_size_x)
    for y in range(board_size_y)
    for t in range(time)
]
var_list_3_neighbours = [
    label_3_neighbours(x, y, t)
    for x in range(board_size_x)
    for y in range(board_size_y)
    for t in range(time)
]
for var in var_list_cell:
    bqm.add_variable(var, 0)
for var in var_list_more_than_3_neighbours:
    bqm.add_variable(var, 0)
for var in var_list_less_than_2_neighbours:
    bqm.add_variable(var, 0)
for var in var_list_2_neighbours:
    bqm.add_variable(var, 0)
for var in var_list_3_neighbours:
    bqm.add_variable(var, 0)


# add constraints
for t in range(time - 1):
    for x in range(board_size_x):
        for y in range(board_size_y):
            # get list of neighbours' label
            neighbour_list = []
            for x_offset in [-1, 0, 1]:
                for y_offset in [-1, 0, 1]:
                    neighbour_list.append(
                        label_cell(
                            (x + x_offset) % board_size_x,
                            (y + y_offset) % board_size_y,
                            t,
                        )
                    )
            neighbour_list.remove(label_cell(x, y, t))
            this_cell = label_cell(x, y, t)
            next_cell = label_cell(x, y, t + 1)
            this_more_than_3_neighbours = label_more_than_3_neighbours(x, y, t)
            this_less_than_2_neighbours = label_less_than_2_neighbours(x, y, t)
            this_2_neighbours = label_2_neighbours(x, y, t)
            this_3_neighbours = label_3_neighbours(x, y, t)

            # temp combination constraint
            # bqm.update(combinations([this_more_than_3_neighbours, this_less_than_2_neighbours, this_2_neighbours, this_3_neighbours], 1, strength=1000))

            # if a cell has more than 3 neighbours
            bqm.add_linear_equality_constraint(
                [(neighbour, 1) for neighbour in neighbour_list] +
                [(this_more_than_3_neighbours, -1)],
                constant=-3,
                lagrange_multiplier=100,
            )

            # if a cell has less than 2 neighbours
            bqm.add_linear_inequality_constraint(
                [(neighbour, 1) for neighbour in neighbour_list] +
                [(this_less_than_2_neighbours, -3)],
                constant=2,
                ub=0,
                lagrange_multiplier=100,
                label=f"lonely_{this_cell}",
            )

            # if a cell has 3 neighbours
            bqm.add_linear_equality_constraint(
                [(neighbour, 6) for neighbour in neighbour_list] +
                [(this_3_neighbours, -1)],
                constant=-17,
                lagrange_multiplier=100,
            )

            # if a cell has 2 neighbours
            bqm.add_linear_equality_constraint(
                [(neighbour, 4) for neighbour in neighbour_list] + 
                [(this_2_neighbours, -1)],
                constant=-7,
                lagrange_multiplier=100,
            )

            # # weakly presist the state
            # bqm.add_linear_equality_constraint(
            #     [(next_cell, 1), (this_cell, -1)],
            #     constant=0,
            #     lagrange_multiplier=10,
            # )



# read input (if any)
for var in dict_input:
    if dict_input[var] == 1:
        bqm.fix_variable(var, 1)
        # bqm.add_linear(var, -5000)
    elif dict_input[var] == 0:
        bqm.fix_variable(var, 0)
        # bqm.add_linear(var, 5000)
    # elif dict_input[var] == 2:
    #     bqm.set_linear(var, 0)


# solve
def hybrid_solve(bqm):
    print("Solving...")
    time_start = datetime.datetime.now()
    sampler = LeapHybridSampler()
    sampleset = sampler.sample(bqm, label="QGOL - H")
    solution = sampleset.first.sample
    print("Solved")
    #print(f"Solution: {solution}")
    print(f"Energy: {sampleset.first.energy}")
    time_end = datetime.datetime.now()
    print(f"Time taken: {time_end - time_start}")
    return sampleset


def quantum_solve(bqm):
    print("Solving...")
    time_start = datetime.datetime.now()
    sampler = EmbeddingComposite(DWaveSampler())
    sampleset = sampler.sample(bqm, label="QGOL - Q", num_reads=1000)
    solution = sampleset.first.sample
    print("Solved")
    #print(f"Solution: {solution}")
    print(f"Energy: {sampleset.first.energy}")
    time_end = datetime.datetime.now()
    print(f"Time taken: {time_end - time_start}")
    return sampleset


def classical_solve(bqm):
    print("Solving...")
    time_start = datetime.datetime.now()
    sampler = SimulatedAnnealingSampler()
    sampleset = sampler.sample(bqm, label="QGOL - C")
    solution = sampleset.first.sample
    print("Solved")
    #print(f"Solution: {solution}")
    print(f"Energy: {sampleset.first.energy}")
    time_end = datetime.datetime.now()
    print(f"Time taken: {time_end - time_start}")
    return sampleset


# output the input and ask for confirmation as well as choice of solver
print("Input:")
print(f"Board size: {board_size_x}x{board_size_y}")
print(f"Time: {time}")
# for t in range(time):
#     print(f"Time step {t}:")
#     print("Cell: ")
#     for y in range(board_size_y):
#         for x in range(board_size_x):
#             print(bqm.get_linear(label_cell(x, y, t)), end=" ")
#         print()
#     print()
#     if t != time - 1:
#         print("Reproduction: ")
#         for y in range(board_size_y):
#             for x in range(board_size_x):
#                 print(bqm.get_linear(label_reproduce(x, y, t)), end=" ")
#             print()
#         print()
#         print("Survive: ")
#         for y in range(board_size_y):
#             for x in range(board_size_x):
#                 print(bqm.get_linear(label_survive(x, y, t)), end=" ")
#             print()
#         print()
#         print("Death: ")
#         for y in range(board_size_y):
#             for x in range(board_size_x):
#                 print(bqm.get_linear(label_death(x, y, t)), end=" ")
#             print()
#     print()
choice = input(
    "Select solver or quit (h for hybrid, q for quantum, c for classic, quit to quit) [quit]: "
)
if choice == "q":
    sampleset = quantum_solve(bqm)
elif choice == "h":
    sampleset = hybrid_solve(bqm)
elif choice == "c":
    sampleset = classical_solve(bqm)
else:
    exit()


# save output to file
try:
    if sys.argv[2] == "#":
        f_output = open("working_folder/output.txt", "w")
    else:
        try:
            f_output = open(sys.argv[2], "w")
        except:
            print("Error writing output file")
            f_output = open("working_folder/output.txt", "w")
except:
    f_output = open("working_folder/output.txt", "w")

dict_output = dict_input
for var in sampleset.first.sample:
    dict_output[var] = sampleset.first.sample[var]
dict_output["x"] = board_size_x
dict_output["y"] = board_size_y
dict_output["t"] = time
# print(dict_output)
f_output.write(str(dict_output))
f_output.close()
display_state_file(f_output.name)
