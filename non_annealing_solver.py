"""
simulates game of life from a given initial state
"""

# import modules
import sys


# label generator
def label_cell(x, y, t):
    return f"x{x}y{y}t{t}"


def label_reproduce(x, y, t):
    return f"x{x}y{y}t{t}r"


def label_survive(x, y, t):
    return f"x{x}y{y}t{t}s"


def label_death(x, y, t):
    return f"x{x}y{y}t{t}d"


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
question_space = dict_input
for x in range(board_size_x):
    for y in range(board_size_y):
        for t in range(time):
            question_space[label_reproduce(x, y, t)] = 0
            question_space[label_survive(x, y, t)] = 0
            question_space[label_death(x, y, t)] = 0

# iterate through time
for t in range(time - 1):
    for x in range(board_size_x):
        for y in range(board_size_y):
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
            this_reproduce = label_reproduce(x, y, t)
            this_survive = label_survive(x, y, t)
            this_death = label_death(x, y, t)

            neighbour_alive_sum = 0
            for neighbour in neighbour_list:
                neighbour_alive_sum += question_space[neighbour]

            if question_space[this_cell] == 0 and neighbour_alive_sum == 3:
                question_space[this_reproduce] = 1
                question_space[next_cell] = 1
            elif question_space[this_cell] == 1 and neighbour_alive_sum in [2, 3]:
                question_space[this_survive] = 1
                question_space[next_cell] = 1
            else:
                question_space[this_death] = 1
                question_space[next_cell] = 0

# output the result
try:
    if sys.argv[2] == "#":
        f_output = open("working_folder/output_c.txt", "w")
    else:
        try:
            f_output = open(sys.argv[2], "w")
        except:
            print("Error writing output file")
            f_output = open("working_folder/output_c.txt", "w")
except:
    f_output = open("working_folder/output_c.txt", "w")

dict_output = {}
for var in question_space:
    dict_output[var] = question_space[var]
dict_output["x"] = board_size_x
dict_output["y"] = board_size_y
dict_output["t"] = time
print(dict_output)
f_output.write(str(dict_output))
f_output.close()
