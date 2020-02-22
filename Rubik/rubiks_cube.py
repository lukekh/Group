import groupy as gp
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np


def perm_01_conversion(perm):
    return tuple(x+1 for x in perm)


class Cube:

    def __init__(self):
        self.state = tuple(range(1, 49))
        self.default_face_colors = ["w", "#cf0000",
                                    "#00008f", "#ff6f00",
                                    "#ffcf00", "#009f0f",
                                    "black"  # background
                                    ]
        self.fig = None
        self.ax = None

    def _colour(self, i):
        return self.default_face_colors[int(i/8)]

    def __mul__(self, other):
        self.state = (gp.Gel('', self.state)*other).perm
        return self

    def __str__(self):
        return str(self.state)

    def solved(self):
        if gp.Gel('state', self.state).is_identity():
            return True
        else:
            return False

    def perm_map(self):
        return [
            [0o61, 0o61, 0o61, self.state[0o00], self.state[0o01], self.state[0o02], 0o61, 0o61, 0o61],
            [0o61, 0o61, 0o61, self.state[0o03], 0o01, self.state[0o04], 0o61, 0o61, 0o61],
            [0o61, 0o61, 0o61, self.state[0o05], self.state[0o06], self.state[0o07], 0o61, 0o61, 0o61],
            [self.state[0o10], self.state[0o11], self.state[0o12],
             self.state[0o20], self.state[0o21], self.state[0o22],
             self.state[0o30], self.state[0o31], self.state[0o32]],
            [self.state[0o13], 0o11, self.state[0o14],
             self.state[0o23], 0o21, self.state[0o24],
             self.state[0o33], 0o31, self.state[0o34]],
            [self.state[0o15], self.state[0o16], self.state[0o17],
             self.state[0o25], self.state[0o26], self.state[0o27],
             self.state[0o35], self.state[0o36], self.state[0o37]],
            [0o61, 0o61, 0o61, self.state[0o40], self.state[0o41], self.state[0o42], 0o61, 0o61, 0o61],
            [0o61, 0o61, 0o61, self.state[0o43], 0o41, self.state[0o44], 0o61, 0o61, 0o61],
            [0o61, 0o61, 0o61, self.state[0o45], self.state[0o46], self.state[0o47], 0o61, 0o61, 0o61],
            [0o61, 0o61, 0o61, self.state[0o50], self.state[0o51], self.state[0o52], 0o61, 0o61, 0o61],
            [0o61, 0o61, 0o61, self.state[0o53], 0o51, self.state[0o54], 0o61, 0o61, 0o61],
            [0o61, 0o61, 0o61, self.state[0o55], self.state[0o56], self.state[0o57], 0o61, 0o61, 0o61],
        ]

    def perm_colour(self):
        a = []
        for l in self.perm_map():
            c = []
            for n in l:
                c.append(int((n-1)/8)-1)
            a.append(c)
        return a

    def plot(self):

        if self.fig is not None:
            plt.clf()
            plt.close(self.fig)
        else:
            plt.ion()

        bounds = [-1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
        self.fig, self.ax = plt.subplots()
        cmap = colors.ListedColormap(self.default_face_colors)
        norm = colors.BoundaryNorm(bounds, cmap.N)
        self.ax.imshow(self.perm_colour(), cmap=cmap, norm=norm)

        # draw grid-lines
        self.ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
        self.ax.set_xticks(np.arange(-.5, 9, 1))
        self.ax.set_yticks(np.arange(-.5, 12, 1))

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.clf()


def construct_rubiks_group():
    R_dict = {

        'e': perm_01_conversion((
            0o00, 0o01, 0o02, 0o03, 0o04, 0o05, 0o06, 0o07,
            0o10, 0o11, 0o12, 0o13, 0o14, 0o15, 0o16, 0o17,
            0o20, 0o21, 0o22, 0o23, 0o24, 0o25, 0o26, 0o27,
            0o30, 0o31, 0o32, 0o33, 0o34, 0o35, 0o36, 0o37,
            0o40, 0o41, 0o42, 0o43, 0o44, 0o45, 0o46, 0o47,
            0o50, 0o51, 0o52, 0o53, 0o54, 0o55, 0o56, 0o57
        )),
        'U': perm_01_conversion((
            0o05, 0o03, 0o00, 0o06, 0o01, 0o07, 0o04, 0o02,
            0o20, 0o21, 0o22, 0o13, 0o14, 0o15, 0o16, 0o17,
            0o30, 0o31, 0o32, 0o23, 0o24, 0o25, 0o26, 0o27,
            0o57, 0o56, 0o55, 0o33, 0o34, 0o35, 0o36, 0o37,
            0o40, 0o41, 0o42, 0o43, 0o44, 0o45, 0o46, 0o47,
            0o50, 0o51, 0o52, 0o53, 0o54, 0o12, 0o11, 0o10
        )),
        'D': perm_01_conversion((
            0o00, 0o01, 0o02, 0o03, 0o04, 0o05, 0o06, 0o07,
            0o10, 0o11, 0o12, 0o13, 0o14, 0o52, 0o51, 0o50,
            0o20, 0o21, 0o22, 0o23, 0o24, 0o15, 0o16, 0o17,
            0o30, 0o31, 0o32, 0o33, 0o34, 0o25, 0o26, 0o27,
            0o45, 0o43, 0o40, 0o46, 0o41, 0o47, 0o44, 0o42,
            0o37, 0o36, 0o35, 0o53, 0o54, 0o55, 0o56, 0o57
        )),
        'L': perm_01_conversion((
            0o50, 0o01, 0o02, 0o53, 0o04, 0o55, 0o06, 0o07,
            0o15, 0o13, 0o10, 0o16, 0o11, 0o17, 0o14, 0o12,
            0o00, 0o21, 0o22, 0o03, 0o24, 0o05, 0o26, 0o27,
            0o30, 0o31, 0o32, 0o33, 0o34, 0o35, 0o36, 0o37,
            0o20, 0o41, 0o42, 0o23, 0o44, 0o25, 0o46, 0o47,
            0o40, 0o51, 0o52, 0o43, 0o54, 0o45, 0o56, 0o57
        )),
        'R': perm_01_conversion((
            0o00, 0o01, 0o22, 0o03, 0o24, 0o05, 0o06, 0o27,
            0o10, 0o11, 0o12, 0o13, 0o14, 0o15, 0o16, 0o17,
            0o20, 0o21, 0o42, 0o23, 0o44, 0o25, 0o26, 0o47,
            0o35, 0o33, 0o30, 0o36, 0o31, 0o37, 0o34, 0o32,
            0o40, 0o41, 0o52, 0o43, 0o54, 0o45, 0o46, 0o57,
            0o50, 0o51, 0o02, 0o53, 0o04, 0o55, 0o56, 0o07
        )),
        'F': perm_01_conversion((
            0o00, 0o01, 0o02, 0o03, 0o04, 0o17, 0o14, 0o12,
            0o10, 0o11, 0o40, 0o13, 0o41, 0o15, 0o16, 0o42,
            0o25, 0o23, 0o20, 0o26, 0o21, 0o27, 0o24, 0o22,
            0o05, 0o31, 0o32, 0o06, 0o34, 0o07, 0o36, 0o37,
            0o35, 0o33, 0o30, 0o43, 0o44, 0o45, 0o46, 0o47,
            0o50, 0o51, 0o52, 0o53, 0o54, 0o55, 0o56, 0o57
        )),
        'B': perm_01_conversion((
            0o32, 0o34, 0o37, 0o03, 0o04, 0o05, 0o06, 0o07,
            0o02, 0o11, 0o12, 0o01, 0o14, 0o00, 0o16, 0o17,
            0o20, 0o21, 0o22, 0o23, 0o24, 0o25, 0o26, 0o27,
            0o30, 0o31, 0o47, 0o33, 0o46, 0o35, 0o36, 0o45,
            0o40, 0o41, 0o42, 0o43, 0o44, 0o10, 0o13, 0o15,
            0o55, 0o53, 0o50, 0o56, 0o51, 0o57, 0o54, 0o52
        ))

    }

    R = gp.GroupLike('R_ops',
                     [gp.Gel(key, R_dict[key]) for key in R_dict]
                     )

    for g in R:
        if not g.is_identity():
            if g.inv() not in R:
                R.append(gp.Gel(f"{g.name}i", g.inv().perm))

    return R


# Sandbox
#
if __name__ == "__main__":

    import pickle
    from sklearn.neural_network import MLPRegressor

    R = construct_rubiks_group()

    M = pickle.load(open("Rubik_scramble_heuristic.sav", 'rb'))

    Rc = Cube()
    #Rc.state = (1, 2, 6, 7, 13, 35, 26, 48, 9, 18, 30, 15, 28, 22, 34, 25, 24, 5, 3, 21, 37, 19, 42, 43, 27, 20, 11, 31, 4, 40, 12, 14, 8, 39, 32, 23, 44, 33, 45, 41, 16, 29, 38, 36, 10, 46, 47, 17)
    while 1 == 1:
        user_input = input()
        Rc*R[user_input]
        Rc.plot()
        print(M.predict([Rc.state]))
