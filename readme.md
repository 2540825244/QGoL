# Quantum Game of Life

## What is this?

This is an attempt to use quantum annealing to process and evolve a Conway's Game of Life board.

The entire board is put as a constraint satisfaction problem using binary quadratic model (from dwave systems). And solved with multiple annealing methods (including dwave's quantum annealer).

## File Structure

I personally used a folder called working_folder to store all the input/output/image files (thus the reference in gitignore and some scripts)

labels.py is a library to supply uniform name generators for the variables in the BQM.

input_creator.py is designed to create input files for the QGOL.py

QGOL.py takes input file and solves it.

display_state_file.py is used to show the output, with both command line and graphical representation.

tool.py is just a random script file in case I want to test anything out.

non_annealing_solver.py is a legacy script to produce an output that simulates how a correct version of my old approach would work.

## What have I achieved

With 2 time steps only, forward evolution of the board.
Completely accurate solution with classical or hybrid solvers.
Completely accurate solution with quantum solver of Zephyr topology (tested on a small range of scenarios due to the size limit of the protoptype machines of this topology).
Coarse solution with quantum solver of Pegasus topology.

Anything else is just broken (basically).

## Misc

The problem formulation is by no means efficient, requiring 10 variables for a single cell on the board at a single time. Some variables can definitely be removed (I think).