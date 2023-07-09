'''
read and display any state file as images
using system argument to select file and output folder
shown after one another
'''

#import modules
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

#label generator
def label(x, y, t):
    return f'x{x}y{y}t{t}'

#read input
if sys.argv[1] == "":
    print("No input file selected")
    sys.exit()
else:
    try:
        f_input = open(sys.argv[1], "r")
        dict_input = eval(f_input.read())
        f_input.close()
    except:
        print("Error reading input file")
        sys.exit()

#set and remove special variables
board_size_x = dict_input["x"]
board_size_y = dict_input["y"]
time = dict_input["t"]
del dict_input["x"]
del dict_input["y"]
del dict_input["t"]

#initialise the board
board = np.zeros((time, board_size_y, board_size_x), dtype=np.int8)
for t in range(time):
    for y in range(board_size_y):
        for x in range(board_size_x):
            board[t][y][x] = dict_input[label(x, y, t)]

#display the board
fig = plt.figure()
ims = []

#read output folder
try:
    output_dir = sys.argv[2]
except:
    output_dir = f"working_folder/"


for t in range(time):
    im = plt.imshow(board[t], animated=True, extent=[0, board_size_x, 0, board_size_y], label=f"t={t}", aspect="equal", vmin=0, vmax=2, cmap="Greys")
    #add grid at the edge of each cell
    for x in range(board_size_x + 1):
        plt.plot([x, x], [0, board_size_y], color="black")
    for y in range(board_size_y + 1):
        plt.plot([0, board_size_x], [y, y], color="black")
    ims.append([im])
    plt.title(f"t={t}")
    plt.savefig(f"{output_dir}frame_{t}.png")
    plt.show()
