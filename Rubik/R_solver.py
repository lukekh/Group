import pickle
import pandas as pd
import rubiks_cube
import scramble_generator


if __name__ == "__main__":

    def minindex(l):
        # finds index of minimum of a list
        return l.index(min(l))

    import pickle
    from sklearn.neural_network import MLPRegressor

    R = rubiks_cube.construct_rubiks_group()

    M = pickle.load(open("Rubik_scramble_heuristic.sav", 'rb'))

    Rc = rubiks_cube.Cube()
    scramble = scramble_generator.Scramble(10).scramble
    for move in scramble:
        Rc * R[move]

    unscramble = []

    count = 0

    while 1 == 1:
        n = 5
        cube_state = Rc.state
        x = []
        new_state = []
        scrambles = []
        for i in range(n):
            Rc.state = cube_state

            x.append(M.predict([cube_state]))
            new_state.append(cube_state)
            scrambles.append([])

            moves = scramble_generator.Scramble(int(M.predict([Rc.state]))+1).scramble
            for move in moves:
                Rc * R[move]
            x.append(M.predict([Rc.state]))
            new_state.append(Rc.state)
            scrambles.append(moves)
        Rc.state = new_state[minindex(x)]
        unscramble = unscramble + scrambles[minindex(x)]
        if Rc.solved():
            break
        count += 1
        print(count)
        print(min(x))
        print(Rc.state)

    print(scramble)
    print(unscramble)

