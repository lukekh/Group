# This file is just to mess around with creating Groups in python

import re


class Gel:

    def __init__(self, name, perm):
        if (type(name) == str) & (type(perm) == tuple):
            self.name = name
            p = True
            for i, _ in enumerate(perm):
                p = p & (i+1 in perm)
            if p:
                self.perm = perm
            else:
                raise Exception("Bad permutation. A permutation tuple of length n must contain all numbers from 1 to n")
        else:
            raise Exception("Invalid inputs for Gel class")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.perm)

    def __eq__(self, other):
        if type(other) == Gel:
            p = True
            for i in range(max(len(self.perm), len(other.perm))):
                p = p & (self._gcycle(i+1) == other._gcycle(i+1))
            return p
        else:
            return False

    def __ne__(self, other):
        if type(other) == Gel:
            return not self == other
        else:
            return True

    def _gcycle(self, n):
        if n in self.perm:
            return self.perm[n-1]
        else:
            return n

    def _gmul(self, other):
        r = []
        for i in range(max(len(self.perm), len(other.perm))):
            r.append(self._gcycle(other._gcycle(i+1)))
        return tuple(r)

    def __mul__(self, other):
        if type(other) == Gel:
            return Gel(self.name+other.name, self._gmul(other))
        else:
            return other.__rmul__(self)

    def inv(self):
        r = []
        for i, _ in enumerate(self.perm):
            r.append(self.perm.index(i+1)+1)
        if len(re.sub(r'[^a-zA-Z]', '', self.name)) == 1:
            return Gel(self.name + u"\u207B\u00B9", tuple(r))
        else:
            return Gel("(" + self.name + u")\u207B\u00B9", tuple(r))

    def __pow__(self, n):
        if type(n) != int:
            raise Exception('You can only perform power operations with integers on Gel types.')
        if n == 1:
            return self
        if n == 0:
            return Gel('e', (self*self.inv()).perm)
        if n < 0:
            return Gel(self.name + '**{}'.format(n), (self.inv()*self.inv().__pow__(-n)).perm)
        else:
            return Gel(self.name + '**{}'.format(n), (self*self.__pow__(n-1)).perm)

    def cycle(self):
        s = "(1 "
        b = [1]
        i = 1
        while len(b) < len(self.perm):
            i = self._gcycle(i)
            if i not in b:
                s = s + "{} ".format(i)
                b.append(i)
            else:
                s = s[0:-1] + ")("
                i = min(set(self.perm)-set(b))
                s = s + "{} ".format(i)
                b.append(i)
        s = re.sub(r'\(\d+\)', '', s[:-1]+")")
        if s == "":
            return "e"
        else:
            return s

    def order(self):
        i = 1
        while self**i != Gel('e', ()):
            i += 1
        return i






# Institute what a group object is


class GroupLike:

    def __init__(self, name, elements):
        for g in elements:
            if type(g) != Gel:
                raise Exception('A GroupLike type can only contain Gel type elements.')
        self.elements = elements
        if type(name) != str:
            raise Exception('The name of a group must be a string, ya idiot.')
        self.name = name
        self._gelnamedict = {}
        self._gelpermdict = {}
        for g in self.elements:
            self._gelpermdict[g.perm] = g
            self._gelnamedict[g.name] = g

    def __str__(self):
        return self.name

    def __repr__(self):
        s = self.name + " = {"
        for g in self:
            s = s + str(g) + ", "
        s = s[:-2] + "}"
        return s

    def __iter__(self):
        return self.elements.__iter__()

    def __getitem__(self, item):
        if type(item) == int:
            return self.elements[item]
        elif type(item) == str:
            return self._gelnamedict[item]

    def __len__(self):
        return len(self.elements)

    def __contains__(self, item):
        return item in self.elements

    def __eq__(self, other):
        if (type(other) != GroupLike) & (type(other) != Group):
            return False
        else:
            p = True
            for g in self:
                p = p & (g in other)
            for h in other:
                p = p & (h in self)
            return p

    def __ne__(self, other):
        return not self == other

    def _hase(self):
        if Gel('e', ()) in self:
            return True
        else:
            return False

    def _isclosed(self):
        p = True
        for g in self:
            for h in self:
                p = p & (g*h in self)
        return p

    def _hasinv(self):
        p = True
        for g in self:
            p = p & (g.inv() in self)
        return p

    def _has_duplicates(self):
        p = False
        b = []
        for g in self:
            if g not in b:
                b.append(g)
            elif g in b:
                p = True
        return p

    def _remove_duplicates(self):
        b = []
        for g in self:
            if g not in b:
                b.append(g)
            elif g in b:
                self.elements.remove(g)

    def isGroup(self):
        return self._hase() & self._isclosed() & self._hasinv() & (not self._has_duplicates())

    def closure(self):
        __G = GroupLike(self.name, self.elements.copy())  # Assignment causes weird errors here without copy
        __G._remove_duplicates()
        e = Gel('e', ())
        if len(__G) == 0:
            return Group(__G.name, [e])
        if e not in __G:
            __G.elements.insert(0, e)
        for g in __G:
            i = 2
            while g**i != e:
                if g**i not in __G:
                    __G.elements.append(g**i)
                i += 1
        for g in __G:
            for h in __G:
                if g*h not in __G:
                    __G.elements.append(g*h)
        if __G.isGroup():
            return __G
        else:
            return __G.closure()

    def _lcoset(self, other):
        if type(other) != Gel:
            raise TypeError('Left Cosets can only be defined with a Gel and GroupLike')
        left = []
        for g in self:
            left.append(other*g)
        return GroupLike(other.name+self.name, left)

    def _rcoset(self, other):
        if type(other) != Gel:
            raise TypeError('Left Cosets can only be defined with a Gel and GroupLike')
        right = []
        for g in self:
            right.append(g*other)
        return GroupLike(self.name+other.name, right)

    def __rmul__(self, other):
        return self._lcoset(other)

    def __mul__(self, other):
        return self._rcoset(other)

    def isAbelian(self):
        p = True
        for g in self:
            for h in self:
                p = p & (g*h == h*g)
        return p

    # TODO: Find centre of group


class Group(GroupLike):

    def __init__(self, name, elements, force_group=True):
        super().__init__(name, elements)
        __G = GroupLike(name, elements)
        self.name = name
        if __G.isGroup():  # TODO: Check if element appears more than once
            self.elements = elements
        else:
            if not force_group:
                raise Exception('The elements of this set do not form a group.')
            self.elements = __G.closure().elements
        self._gelnamedict = {}
        self._gelpermdict = {}
        for g in self.elements:
            self._gelpermdict[g.perm] = g
            self._gelnamedict[g.name] = g

    def __lt__(self, other):
        if type(other) != Group:
            raise TypeError("'<' not supported between instances of '{}' and 'Group'".format(type(other)))
        p = True
        for g in self:
            p = p & (g in other)
            if not p:
                break
        return p

    def __gt__(self, other):
        if type(other) != Group:
            return TypeError("'<' not supported between instances of '{}' and 'Group'".format(type(other)))
        p = True
        for h in other:
            p = p & (h in self)
            if not p:
                break
        return p

    def __eq__(self, other):
        return (self < other) & (self > other)

    def hasNormal(self, other):
        if type(other) == Group:
            if self > other:
                p = True
                for g in self:
                    p = p & ((g*other*g.inv()).__eq__(other))
                return p
            else:
                return False
        else:
            return False

    def __truediv__(self, other):
        if (type(other) == Group) & (self.hasNormal(other)):
            cosets = []
            reps = []
            for g in self:
                if g*other not in cosets:
                    cosets.append(g*other)
            perm = list(range(len(cosets)))
            for X in cosets:
                g = X[0]
                for i, Yi in enumerate(cosets):
                    for j, Yj in enumerate(cosets):
                        if g*Yi == Yj:
                            perm[i] = j+1
                            break
                reps.append(Gel(X.name, tuple(perm)))
            return Group(self.name+'/'+other.name, reps, force_group=False)
        else:
            raise Exception('{} must be a normal subgroup of {} to compute G/H.'.format(other, self))

    def hasGenerators(self, generators):
        return self == Group('', generators)


def mat_to_group(name, columns, matrix):

    def _row_to_element(dictionary, _row):
        element = []
        for item in _row:
            element.append(dictionary[item])
        return tuple(element)

    d = {}
    elements = []
    for i, g in enumerate(columns):
        d[g] = i+1
        d[i+1] = i+1
    for i, row in enumerate(matrix):
        try:
            elements.append(Gel(columns[i], _row_to_element(d, row)))
        except Exception:
            raise Exception('One of the rows in the matrix input does not describe valid group multiplication')
    try:
        return Group(name, elements, force_group=False)
    except Exception:
        raise Exception('The matrix does not describe a group. Try mat_to_GroupLike.')


def group_to_mat(G, use_name=False):

    if type(G) != Group:
        raise TypeError('This function can only be applied to a Group object')

    def _element_to_row_num(_g, _G):
        row = []
        for _h in _G:
            for _i, _k in enumerate(_G):
                if _g*_h == _k:
                    row.append(_i+1)
                    break
        return row

    def _element_to_row_str(_g, _G):
        row = []
        for _h in _G:
            for _i, _k in enumerate(_G):
                if _g*_h == _k:
                    row.append(_k.name)
                    break
        return row

    matrix = []
    if use_name:
        for i, g in enumerate(G):
            matrix.append(_element_to_row_str(g, G))
    else:
        for i, g in enumerate(G):
            matrix.append(_element_to_row_num(g, G))
    return matrix


def cycle_to_perm(cycle):

    split = re.findall(r'\([\d\s]+\)', cycle)
    for i, chunk in enumerate(split):
        temp = re.findall(r'\d+', chunk)
        split[i] = [int(j) for j in temp]
    m = max([max(item) for item in split])
    perm = []
    for i in range(m):
        im = i+1
        for chunk in reversed(split):
            if im in chunk:
                im = chunk[(chunk.index(im)+1) % len(chunk)]
        perm.append(im)
    return tuple(perm)


# TODO: HomLike and Hom

