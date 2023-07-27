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
    from labels import (label_cell, label_same_as_next_time, label_more_than_3_neighbours, label_less_than_2_neighbours, label_2_neighbours, label_2_neighbours_helper_a, label_2_neighbours_helper_b, label_3_neighbours, label_3_neighbours_helper_a, label_3_neighbours_helper_b)

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
        print("Cell        N>3         N<2         N=2         N=3")
        for y in range(board_size_y):
            for x in range(board_size_x):
                print(dict_input[label_cell(x, y, t)], end=" ")
            print("  ", end="")
            for x in range(board_size_x):
                try:
                    print(dict_input[label_more_than_3_neighbours(x, y, t)], end=" ")
                except:
                    print("0", end=" ")
            print("  ", end="")
            for x in range(board_size_x):
                try:
                    print(dict_input[label_less_than_2_neighbours(x, y, t)], end=" ")
                except:
                    print("0", end=" ")
            print("  ", end="")
            for x in range(board_size_x):
                try:
                    print(dict_input[label_2_neighbours(x, y, t)], end=" ")
                except:
                    print("0", end=" ")
            print("  ", end="")
            for x in range(board_size_x):
                try:
                    print(dict_input[label_3_neighbours(x, y, t)], end=" ")
                except:
                    print("0", end=" ")
            print()
        print()
        print("N=2 Helper A and B      N=3 Helper A and B      Same")
        for y in range(board_size_y):
            for x in range(board_size_x):
                try:
                    print(dict_input[label_2_neighbours_helper_a(x, y, t)], end=" ")
                except:
                    print("0", end=" ")
            print("  ", end="")
            for x in range(board_size_x):
                try:
                    print(dict_input[label_2_neighbours_helper_b(x, y, t)], end=" ")
                except:
                    print("0", end=" ")
            print("  ", end="")
            for x in range(board_size_x):
                try:
                    print(dict_input[label_3_neighbours_helper_a(x, y, t)], end=" ")
                except:
                    print("0", end=" ")
            print("  ", end="")
            for x in range(board_size_x):
                try:
                    print(dict_input[label_3_neighbours_helper_b(x, y, t)], end=" ")
                except:
                    print("0", end=" ")
            print("  ", end="")
            for x in range(board_size_x):
                try:
                    print(dict_input[label_same_as_next_time(x, y, t)], end=" ")
                except:
                    print("0", end=" ")
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
