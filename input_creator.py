'''
CLI to create input files for the simulation
system argument for output file name
start with inputting the board size and time
then all cells are initialised to 2
then you can change the value of each cell using commands
commands:
    set x y t value
    fill t original_value new_value
    save
'''

import sys

def label(x, y, t):
    return f"{x}_{y}_{t}"

def main():
    #create the input dictionary
    dict_input = {}
    #set the board size
    print("Input board size:")
    board_size_x = int(input("x: "))
    board_size_y = int(input("y: "))
    dict_input["x"] = board_size_x
    dict_input["y"] = board_size_y
    #set the time
    print("Input time:")
    time = int(input("t: "))
    dict_input["t"] = time
    #set all cells to 2
    for t in range(time):
        for x in range(board_size_x):
            for y in range(board_size_y):
                dict_input[label(x, y, t)] = 2
    #print the input
    print("Input:")
    print(f"Board size: {board_size_x}x{board_size_y}")
    print(f"Time: {time}")
    for t in range(time):
        print(f"Time step {t}:")
        for y in range(board_size_y):
            for x in range(board_size_x):
                print(dict_input[label(x, y, t)], end=" ")
            print()
        print()
    #command loop
    while True:
        command = input(">")
        if command == "save":
            break
        elif command.split(" ")[0] == "set":
            try:
                x = int(command.split(" ")[1])
                y = int(command.split(" ")[2])
                t = int(command.split(" ")[3])
                value = int(command.split(" ")[4])
                dict_input[label(x, y, t)] = value
            except:
                print("Invalid command")
        elif command.split(" ")[0] == "fill":
            try:
                t = int(command.split(" ")[1])
                original_value = int(command.split(" ")[2])
                new_value = int(command.split(" ")[3])
                for x in range(board_size_x):
                    for y in range(board_size_y):
                        if dict_input[label(x, y, t)] == original_value:
                            dict_input[label(x, y, t)] = new_value
            except:
                print("Invalid command")

    #write the input to file
    f_input = open(sys.argv[0], "w")
    f_input.write(str(dict_input))
    f_input.close()