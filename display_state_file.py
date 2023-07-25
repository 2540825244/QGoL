"""
read and display any state file as images
using system argument to select file and output folder
shown after one another
"""


def display_state_file(file_dir):
    # import modules
    import sys
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import numpy as np

    # label generator
    def label_cell(x, y, t):
        return f"x{x}y{y}t{t}"

    def label_reproduce(x, y, t):
        return f"x{x}y{y}t{t}r"

    def label_survive(x, y, t):
        return f"x{x}y{y}t{t}s"

    def label_death(x, y, t):
        return f"x{x}y{y}t{t}d"

    # read input
    try:
        if file_dir == "":
            print("No input file selected")
            sys.exit()
        else:
            try:
                f_input = open(file_dir, "r")
                dict_input = eval(f_input.read())
                f_input.close()
            except:
                print("Error reading input file")
                sys.exit()
    except:
        print("No input file selected")
        sys.exit()

    # set and remove special variables
    board_size_x = dict_input["x"]
    board_size_y = dict_input["y"]
    time = dict_input["t"]
    del dict_input["x"]
    del dict_input["y"]
    del dict_input["t"]

    # initialise the board
    board = np.zeros((time, board_size_y, board_size_x), dtype=np.int8)
    for t in range(time):
        for y in range(board_size_y):
            for x in range(board_size_x):
                board[t][y][x] = dict_input[label_cell(x, y, t)]

    # display like in OGOL.py
    # output the input and ask for confirmation
    print("Input:")
    print(f"Board size: {board_size_x}x{board_size_y}")
    print(f"Time: {time}")
    for t in range(time):
        print(f"Time step {t}:")
        for y in range(board_size_y):
            for x in range(board_size_x):
                print(dict_input[label_cell(x, y, t)], end=" ")
            print()
        print()
    print("Continue? (y/n) [n]")
    if input() != "y":
        exit()

    # display the board
    fig = plt.figure()
    ims = []

    # read output folder
    try:
        output_dir = sys.argv[2]
    except:
        output_dir = f"working_folder/"

    for t in range(time):
        im = plt.imshow(
            board[t],
            animated=True,
            extent=[0, board_size_x, 0, board_size_y],
            label=f"t={t}",
            aspect="equal",
            vmin=0,
            vmax=2,
            cmap="Greys",
        )
        # add grid at the edge of each cell
        for x in range(board_size_x + 1):
            plt.plot([x, x], [0, board_size_y], color="black")
        for y in range(board_size_y + 1):
            plt.plot([0, board_size_x], [y, y], color="black")
        ims.append([im])
        plt.title(f"t={t}")
        plt.savefig(f"{output_dir}frame_{t}.png")
        plt.show()


if __name__ == "__main__":
    import sys

    display_state_file(str(sys.argv[1]))
