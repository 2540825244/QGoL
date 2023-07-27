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
from dimod.generators import and_gate
from dwave.system import LeapHybridSampler, DWaveSampler, EmbeddingComposite
import dwave.inspector
import datetime
import sys

from display_state_file import display_state_file
from neal import SimulatedAnnealingSampler

from labels import *

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
    for t in range(time - 1)
]
var_list_more_than_3_neighbours = [
    label_more_than_3_neighbours(x, y, t)
    for x in range(board_size_x)
    for y in range(board_size_y)
    for t in range(time - 1)
]
var_list_less_than_2_neighbours = [
    label_less_than_2_neighbours(x, y, t)
    for x in range(board_size_x)
    for y in range(board_size_y)
    for t in range(time - 1)
]
var_list_2_neighbours = [
    label_2_neighbours(x, y, t)
    for x in range(board_size_x)
    for y in range(board_size_y)
    for t in range(time - 1)
]
var_list_2_neighbours_helper_a = [
    label_2_neighbours_helper_a(x, y, t)
    for x in range(board_size_x)
    for y in range(board_size_y)
    for t in range(time - 1)
]
var_list_2_neighbours_helper_b = [
    label_2_neighbours_helper_b(x, y, t)
    for x in range(board_size_x)
    for y in range(board_size_y)
    for t in range(time - 1)
]
var_list_2_neighbours_helper_c = [
    label_2_neighbours_helper_c(x, y, t)
    for x in range(board_size_x)
    for y in range(board_size_y)
    for t in range(time - 1)
]
var_list_3_neighbours = [
    label_3_neighbours(x, y, t)
    for x in range(board_size_x)
    for y in range(board_size_y)
    for t in range(time - 1)
]
var_list_3_neighbours_helper_a = [
    label_3_neighbours_helper_a(x, y, t)
    for x in range(board_size_x)
    for y in range(board_size_y)
    for t in range(time - 1)
]
var_list_3_neighbours_helper_b = [
    label_3_neighbours_helper_b(x, y, t)
    for x in range(board_size_x)
    for y in range(board_size_y)
    for t in range(time - 1)
]
for var in var_list_cell:
    bqm.add_variable(var, 0)
for var in var_list_more_than_3_neighbours:
    bqm.add_variable(var, 0)
for var in var_list_less_than_2_neighbours:
    bqm.add_variable(var, 0)
for var in var_list_2_neighbours:
    bqm.add_variable(var, 0)
for var in var_list_2_neighbours_helper_a:
    bqm.add_variable(var, 0)
for var in var_list_2_neighbours_helper_b:
    bqm.add_variable(var, 0)
for var in var_list_2_neighbours_helper_c:
    bqm.add_variable(var, 0)
for var in var_list_3_neighbours:
    bqm.add_variable(var, 0)
for var in var_list_3_neighbours_helper_a:
    bqm.add_variable(var, 0)
for var in var_list_3_neighbours_helper_b:
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
            this_2_neighbours_helper_a = label_2_neighbours_helper_a(x, y, t)
            this_2_neighbours_helper_b = label_2_neighbours_helper_b(x, y, t)
            this_2_neighbours_helper_c = label_2_neighbours_helper_c(x, y, t)
            this_3_neighbours = label_3_neighbours(x, y, t)
            this_3_neighbours_helper_a = label_3_neighbours_helper_a(x, y, t)
            this_3_neighbours_helper_b = label_3_neighbours_helper_b(x, y, t)

            overall_strength_factor = 1

            # temp combination constraint
            bqm.update(
                combinations(
                    [
                        this_more_than_3_neighbours,
                        this_less_than_2_neighbours,
                        this_2_neighbours,
                        this_3_neighbours,
                    ],
                    1,
                    strength=50 * overall_strength_factor,
                )
            )

            # same as next time constraint
            # penalty function in the form

            # if a cell has more than 3 neighbours
            bqm.add_linear_equality_constraint(
                [(neighbour, 1) for neighbour in neighbour_list]
                + [(this_more_than_3_neighbours, -1)],
                constant=-3 * overall_strength_factor,
                lagrange_multiplier=100 * overall_strength_factor,
            )

            # if a cell has less than 2 neighbours
            bqm.add_linear_equality_constraint(
                [(neighbour, -1) for neighbour in neighbour_list]
                + [(this_less_than_2_neighbours, -1)],
                constant=2 * overall_strength_factor,
                lagrange_multiplier=100 * overall_strength_factor,
            )

            # if a cell has 3 neighbours
            # more than 2 neighbours
            bqm.add_linear_equality_constraint(
                [(neighbour, 1) for neighbour in neighbour_list]
                + [(this_3_neighbours_helper_a, -1)],
                constant=-2 * overall_strength_factor,
                lagrange_multiplier=70 * overall_strength_factor,
            )
            # less than 4 neighbours
            bqm.add_linear_equality_constraint(
                [(neighbour, -1) for neighbour in neighbour_list]
                + [(this_3_neighbours_helper_b, -1)],
                constant=4 * overall_strength_factor,
                lagrange_multiplier=70 * overall_strength_factor,
            )
            # using and gate, get the 3 neighbours flag
            bqm.update(
                and_gate(
                    this_3_neighbours_helper_a,
                    this_3_neighbours_helper_b,
                    this_3_neighbours,
                    strength=100 * overall_strength_factor,
                )
            )

            # if a cell has 2 neighbours
            # more than 1 neighbours
            bqm.add_linear_equality_constraint(
                [(neighbour, 1) for neighbour in neighbour_list]
                + [(this_2_neighbours_helper_a, -1)],
                constant=-1 * overall_strength_factor,
                lagrange_multiplier=70 * overall_strength_factor,
            )
            # less than 3 neighbours
            bqm.add_linear_equality_constraint(
                [(neighbour, -1) for neighbour in neighbour_list]
                + [(this_2_neighbours_helper_b, -1)],
                constant=3 * overall_strength_factor,
                lagrange_multiplier=70 * overall_strength_factor,
            )
            # using and gate, get the 2 neighbours flag
            bqm.update(
                and_gate(
                    this_2_neighbours_helper_a,
                    this_2_neighbours_helper_b,
                    this_2_neighbours,
                    strength=100 * overall_strength_factor,
                )
            )

            # # for more than 3 neighbours and less than 2 neighbours, the cell is dead the next time step
            bqm.add_quadratic(
                this_more_than_3_neighbours, next_cell, 50 * overall_strength_factor
            )
            bqm.add_quadratic(
                this_less_than_2_neighbours, next_cell, 50 * overall_strength_factor
            )

            # for 3 neighbours, the cell is alive the next time step
            bqm.add_quadratic(
                this_3_neighbours, next_cell, -75 * overall_strength_factor
            )

            # for 2 neighbours, the cell is the same as this time step the next time step
            # penalty function is: -E2+E2T+E2N-2E2TN
            # TN is reduced to helper c by and gate
            # so final penalty function is: -E2+E2T+E2N-2E2C
            two_neighbours_penalty_factor = 25
            bqm.update(
                and_gate(
                    this_cell,
                    next_cell,
                    this_2_neighbours_helper_c,
                    strength=2
                    * two_neighbours_penalty_factor
                    * overall_strength_factor,
                )
            )
            bqm.add_linear(
                this_2_neighbours,
                -two_neighbours_penalty_factor * overall_strength_factor,
            )
            bqm.add_quadratic(
                this_2_neighbours,
                this_cell,
                two_neighbours_penalty_factor * overall_strength_factor,
            )
            bqm.add_quadratic(
                this_2_neighbours,
                next_cell,
                two_neighbours_penalty_factor * overall_strength_factor,
            )
            bqm.add_quadratic(
                this_2_neighbours,
                this_2_neighbours_helper_c,
                -two_neighbours_penalty_factor * 2 * overall_strength_factor,
            )

            # make helper c only true when the E2 is true
            # penalty function is: C-E2C
            helper_c_penalty_factor = 25
            bqm.add_linear(
                this_2_neighbours_helper_c,
                helper_c_penalty_factor * overall_strength_factor,
            )
            bqm.add_quadratic(
                this_2_neighbours_helper_c,
                this_2_neighbours,
                -helper_c_penalty_factor * overall_strength_factor,
            )


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
    # print(f"Solution: {solution}")
    print(f"Energy: {sampleset.first.energy}")
    time_end = datetime.datetime.now()
    print(f"Time taken: {time_end - time_start}")
    return sampleset


def quantum_solve(bqm):
    print("Solving...")
    time_start = datetime.datetime.now()
    sampler = EmbeddingComposite(DWaveSampler(solver={"topology__type": "zephyr"}))
    sampleset = sampler.sample(bqm, label="QGOL - Q", num_reads=1000)
    solution = sampleset.first.sample
    print("Solved")
    # print(f"Solution: {solution}")
    print(f"Energy: {sampleset.first.energy}")
    time_end = datetime.datetime.now()
    print(f"Time taken: {time_end - time_start}")
    # calls inspector
    dwave.inspector.show(sampleset)
    return sampleset


def classical_solve(bqm):
    print("Solving...")
    time_start = datetime.datetime.now()
    sampler = SimulatedAnnealingSampler()
    sampleset = sampler.sample(bqm, label="QGOL - C")
    solution = sampleset.first.sample
    print("Solved")
    # print(f"Solution: {solution}")
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
