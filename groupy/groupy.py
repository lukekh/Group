# This file is just to mess around with creating Groups in python

import re


class Gel:
    """
    A group element.

    The Gel object consists of a name and a permutation. The permutation is some bijection from the set of numbers from
    1 to n onto itself in the form of a tuple. Since any group element of a finite group can be thought of a member of
    the symmetric group, every group element can be realised as one of these tuples.

    Parameters
    ----------
    :type g: object,
        The object you wish to assign a group meaning to.
    :type perm: tuple,
        if tuple : The mathematical definition of the group element. If it is of length n, it must contain the numbers
                   1 to n.

    Examples
    --------
    >>> g = Gel('g', (2,1,4,3))
    >>> identity = Gel('e', ())
    """
    def __init__(self, g, perm):

        def valid_tuple(tup):
            """Checks the tuple adheres to the Gel standard"""
            return set(tup) == set(range(1, len(tup)+1))

        self.g = g

        if valid_tuple(perm):
            self.perm = perm
        else:
            raise Exception("Bad permutation. A permutation tuple of length n must contain all numbers from 1 to n")

    def __str__(self):
        return str(self.g)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.g)

    def __eq__(self, other):
        """
        Boolean equality

        A bijection from 1 to n can be thought of as a bijection from the natural numbers onto itself where m -> m
        for any m > n. In this way, this equality robustly allows us to compare group elements even if they do not
        strictly have the same tuple.

        :param other: another Gel object
        :return: True/False
        """
        if type(other) == Gel:
            p = True
            for i in range(max(len(self.perm), len(other.perm))):
                p = p & (self.gcycle(i + 1) == other.gcycle(i + 1))
            return p
        else:
            return False

    def __ne__(self, other):
        if type(other) == Gel:
            return not self == other
        else:
            return True

    def gcycle(self, n):
        # Find the image of the number n under the group element self
        if n in self.perm:
            return self.perm[n-1]
        else:
            return n

    def gmul(self, other):
        # Group multiplication between the permutations of self*other
        r = []
        for i in range(max(len(self.perm), len(other.perm))):
            r.append(self.gcycle(other.gcycle(i + 1)))
        return tuple(r)

    def __mul__(self, other):
        # Create group object (element/coset/etc) through multiplication
        if type(other) == Gel:
            return Gel(str(self) + str(other), self.gmul(other))
        else:
            return other.__rmul__(self)

    def inv(self):
        # Calculate the inverse of a group element
        r = []
        for i, _ in enumerate(self.perm):
            r.append(self.perm.index(i+1)+1)
        if len(re.sub(r'[^a-zA-Z]', '', str(self))) == 1:
            # Adds inverse symbol to the end of string
            return Gel(str(self) + u"\u207B\u00B9", tuple(r))
        else:
            # Puts complex name in brackets first to avoid confusion
            return Gel("(" + str(self) + u")\u207B\u00B9", tuple(r))

    def __pow__(self, n):
        if type(n) != int:
            raise Exception('You can only perform power operations with integers on Gel types.')
        if n == 1:
            return self
        if n == 0:
            return Gel('e', ())
        if n < 0:
            return Gel(f'{self}**{n}', (self.inv()*self.inv().__pow__(-n)).perm)
        else:
            return Gel(f'{self}**{n}', (self*self.__pow__(n-1)).perm)

    def cycle(self):
        # Prints cycle notation of group element
        s = "(1 "
        b = [1]
        i = 1
        while len(b) < len(self.perm):
            i = self.gcycle(i)
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
        # Calculates order of group element
        i = 1
        while self**i != Gel('e', ()):
            i += 1
        return i

    def is_identity(self):
        p = True
        for i in range(len(self.perm)):
            p = p & (self.gcycle(i) == i)
        return p


class GroupLike:
    """
    A class that resembles a group but need not meet all of the group axioms.

    A GroupLike class consists of a name and a list of group elements. The elements of a GroupLike need not abide by
    the axioms of a Group and can be used as a set of group elements (e.g. a coset).

    Parameters
    -----------
    name : str,
        The name of your GroupLike object.
    elements : list,
        List of group elements.

    Examples
    --------
    >>> G = GroupLike('V_4', [Gel('e', () ), Gel('V', (2,1) ), Gel('H', (1,2,4,3) ), Gel('R', (2,1,4,3) )])
    """
    def __init__(self, name, elements):
        for g in elements:
            if type(g) != Gel:
                raise Exception('A GroupLike type can only contain Gel type elements.')
        self.elements = elements
        if type(name) != str:
            raise Exception('The name of a GroupLike must be a string, ya idiot.')
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

    def append(self, g):
        if type(g) == Gel:
            self.elements.append(g)
            self._gelpermdict[g.perm] = g
            self._gelnamedict[g.name] = g
        else:
            raise Exception(f"You may only append Gel class elements to a {type(self)} class.")

    def _hase(self):
        return Gel('e', ()) in self

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
    """
    A class that resembles a mathematical group.

    A Group class consists of a name list of group elements. The elements of a Group needs to abide by the axioms of a
    Group and will force the closure of the group if force_group is True (which is the default). The main structure is
    inherited from GroupLike but certain methods have been added/altered.

    Parameters
    -----------
    name : str,
        The name of your Group object.
    elements : list,
        List of group elements.
    force_group : bool, default=True,
        Boolean representing whether or not the group should be automatically completed so that it abides by the group
        axioms. True will construct the closure of the list of elements, false will allow the user to attempt to submit
        a group and raise an exception if it does not meet the axioms of a group.

    Examples
    --------
    >>> G = Group('V_4', [Gel('e', () ), Gel('V', (2,1) ), Gel('H', (1,2,4,3) )])
    >>> G
    G = {e, V, H, VH}
    """
    def __init__(self, name, elements, force_group=True):
        super().__init__(name, elements)
        __G = GroupLike(name, elements)
        self.name = name
        if __G.isGroup():
            self.elements = elements
        else:
            if not force_group:
                raise Exception('The elements of this set do not form a groupy.')
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

    def __rmul__(self, other):
        if type(other) == Gel:
            return self._lcoset(other)
        elif type(other) == Group:
            return other._groupprod(self)

    def __mul__(self, other):
        if type(other) == Gel:
            return self._rcoset(other)
        elif type(other) == Group:
            return self._groupprod(other)

    def _groupprod(self, other):
        Gperms = [g.perm for g in self]
        Gmax = max([max(t) if len(t) > 1 else 0 for t in Gperms])
        Hels = [Gel(f"{h.name}'", tuple(list(range(1, Gmax+1))+[i+Gmax for i in h.perm])) for h in other]
        return Group(f"{self.name}x{other.name}", self.elements+Hels)

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
            raise Exception('One of the rows in the matrix input does not describe valid groupy multiplication')
    try:
        return Group(name, elements, force_group=False)
    except Exception:
        raise Exception('The matrix does not describe a groupy. Try mat_to_GroupLike.')


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

class HomLike:

    def __init__(self, name, G, H, homlist):
        if type(name) != str:
            raise TypeError('The name of this object should be a string')
        self.name = name
        if type(G) != (Group or GroupLike):
            raise TypeError(f'{G} must be a Group or GroupLike object for a HomLike class')
        if type(H) != (Group or GroupLike):
            raise TypeError(f'{G} must be a Group or GroupLike object for a HomLike class')
        self.domain = G
        self.range = H
        self.hom = homlist
        self._flatdomain = [item[0] for item in homlist]
        self._flatrange = [item[1] for item in homlist]
        for tup in homlist:     # I think I actually want this to be part of the Hom class, not HomLike
            i = 1
            while tup[0]**i != Gel('e', ()):
                if tup[0]**i not in self._flatdomain:
                    self.hom.append((tup[0]**i, tup[1]**i))
                    self._flatdomain.append(tup[0]**i)
                i += 1

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name}: {self.domain.name} -> {self.range.name}"

    def __getitem__(self, item):
        try:
            return self._flatrange[self._flatdomain.index(item)]
        except:
            raise Exception('This does not appear in the domain of your function')

    def _hasdomainG(self):
        p = True
        for g in self.domain:
            p = p & (g in self._flatdomain)
        return p


def constructGroup(groupname):

    # This function cleans up symbols people might use
    def _namestd(s):
        return s.lower().replace('_', '').replace('-', '').replace(' ', '')

    # Some regex strings for matching
    rcycle = r'^[cz]\d+$'  # regex for cycles
    rklein = r'(v4)|(^(klein)(4|four)?(group)?$)|(^z2(\*\*|\^)2$)' # regex for klein group
    rquaternions = r'(^(quaternion)(s)?(group)?$)|(^h$)'

    # Allows user to input a groupname string and returns some of the more well known groups
    if re.match(rcycle, _namestd(groupname)):
        n = int(re.findall(r'\d+', _namestd(groupname))[0])
        if n > 200:
            raise Exception('Are you trying to break your computer?')
        g = Gel('g', tuple(list(range(2, n+1))+[1]))
        glist = []
        for i in range(n):
            glist.append(Gel((g**i).cycle(), (g**i).perm))
        return Group(groupname, glist, force_group=False)

    if re.match(rklein, _namestd(groupname)):
        return Group(groupname, [
            Gel('e', ()), Gel('(1 2)', (2, 1)), Gel('(3 4)', (1, 2, 4, 3)), Gel('(1 2)(3 4)', (2, 1, 4, 3))
        ])

    if re.match(rquaternions, _namestd(groupname)):
        return mat_to_group(groupname, ['1', '-1', 'i', '-i', 'j', '-j', 'k', '-k'],
                            [['1', '-1', 'i', '-i', 'j', '-j', 'k', '-k'],
                             ['-1', '1', '-i', 'i', '-j', 'j', '-k', 'k'],
                             ['i', '-i', '-1', '1', 'k', '-k', '-j', 'j'],
                             ['-i', 'i', '1', '-1', '-k', 'k', 'j', '-j'],
                             ['j', '-j', '-k', 'k', '-1', '1', 'i', '-i'],
                             ['-j', 'j', 'k', '-k', '1', '-1', '-i', 'i'],
                             ['k', '-k', 'j', '-j', '-i', 'i', '-1', '1'],
                             ['-k', 'k', '-j', 'j', 'i', '-i', '1', '-1']]
                            )


if __name__ == "__main__":
    pass
