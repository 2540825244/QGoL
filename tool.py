"""
misc functions and tools, not a library
"""

import sympy as sp
import numpy as np


def expand_penalty_for_3_neighbours():
    E = sp.Symbol("E3")
    Ns = [sp.Symbol(f"N{i}") for i in range(9)]
    P = sp.Symbol("P")

    # penalty is P*(-E-(S_Ns)^2+6*S_Ns-8)^2
    # where S_Ns is sum of Ns
    # and P is a constant

    # expand the penalty
    penalty = sp.expand(P * (-E - (sum(Ns)) ** 2 + 6 * sum(Ns) - 8) ** 2)
    print(penalty)


if __name__ == "__main__":
    expand_penalty_for_3_neighbours()
