import groupy as gp
from Rubik.rubiks_cube import *


class Datum:
    """
    A data point that has a cube state, number of moves from being solved and the optimum moves.
    """
    def __init__(self, state, n):
        self.state = state
        self.n = n
        self.optima = []

    def optimum(self, move):
        self.optima.append(move)
        return self


if __name__ == "__main__":

    R = construct_rubiks_group()

    layers = []




    for i in range(1,10):
