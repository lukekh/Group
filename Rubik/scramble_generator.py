import random


class Scramble:

    def __init__(self, n):

        def scramble_inv_reduce(s):
            sr = []
            i = 0
            while i < len(s) - 1:
                if (s[i] == f"{s[i + 1]}i") or (s[i + 1] == f"{s[i]}i"):
                    i += 2
                    if i == len(s) - 1:
                        sr.append(s[i])
                        i += 1
                else:
                    sr.append(s[i])
                    i += 1
                    if i == len(s) - 1:
                        sr.append(s[i])
                        i += 1
            return sr

        def scramble_reorder(s):

            def indep(op):
                # We only put U, L and F in the condition to avoid an infinite loop
                if (op == 'U') or (op == 'Ui'):
                    return ['D', 'Di']
                elif (op == 'L') or (op == 'Li'):
                    return ['R', 'Ri']
                elif (op == 'F') or (op == 'Fi'):
                    return ['B', 'Bi']
                else:
                    return []

            sr = s.copy()
            for i, move in enumerate(sr):
                k = 0
                for j in range(1, i):
                    if sr[i - j] in indep(sr[i]):
                        k += 1
                    else:
                        break
                sr.insert(i - k, sr[i])
                del sr[i + 1]
            return sr

        def scramble_triples(s):

            def _inv(op):
                if op[-1] == "i":
                    return op[0]
                else:
                    return f"{op}i"

            st = s.copy()

            for i, move in enumerate(st):
                k = 1
                j = 1
                while k == 1:
                    if i + j < len(st):
                        if st[i + j] == st[i]:
                            j += 1
                        else:
                            k = 0
                    else:
                        k = 0
                if j > 2:
                    del st[i:i + j]
                    if j % 4 == 3:
                        st.insert(i, _inv(move))
                    if j % 4 == 2:
                        st.insert(i, move)
                        st.insert(i, move)
                    elif j % 4 == 1:
                        st.insert(i, move)
            return st

        def scramble_small(scram):
            repeat = 1
            while repeat == 1:
                s_temp = scramble_inv_reduce(scram)
                s_temp = scramble_reorder(s_temp)
                s_temp = scramble_triples(s_temp)
                if s_temp == scram:
                    repeat = 0
                else:
                    scram = s_temp
            return scram

        self.n = n
        self.ops = [
            'U', 'D', 'L', 'R', 'F', 'B',
            'Ui', 'Di', 'Li', 'Ri', 'Fi', 'Bi',
        ]
        big_scramble = []
        r = random.randint(0, n - 1)
        for _ in range(r):
            big_scramble.append(self.ops[random.randint(0, len(self.ops) - 1)])
        self.scramble = scramble_small(big_scramble)

    def __str__(self):
        return str(self.scramble)

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.scramble)


if __name__ == "__main__":
    pass
