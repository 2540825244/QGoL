'''
read and display any state file as images
using system argument to select file
also can save as image sequence
'''

#import modules
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

#label generator
def label(x, y, t):
    return f"{x}_{y}_{t}"

#read input
if sys.argv[0] == "":
    print("No input file selected")
    sys.exit()
else:
    try:
        f_input = open(sys.argv[0], "r")
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
for t in range(time):
    im = plt.imshow(board[t], animated=True)
    ims.append([im])
ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
plt.show()
