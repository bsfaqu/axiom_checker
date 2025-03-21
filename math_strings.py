
# unequals symbol
def neq():
    return u'\u2260'


# equal sign
def eq():
    return "="


# is element of symbol
def elem():
    return u'\u2208'


# is not element of symbol
def nelem():
    return u'\u2209'


# is subset of symbol
def subseteq():
    return u'\u2286'


# is not subset of symbol
def nsubseteq():
    return u'\u2288'


# intersection symbol
def cap():
    return u'\u2229'


# union symbol
def cup():
    return u'\u222A'


# implication symbol
def implies():
    return u'\u21D2'


# negated implication symbol
def nimplies():
    return u'\u21CF'


# empty set symbol
def emptyset():
    return u'\u2205'


# transit function string of R(u, v)
def r(u, v):
    return "R(" + str(u) + ", " + str(v) + ")"


# set string-ifyer
def sstr(A):
    list_A = list(A)
    list_A = sorted(list_A)
    if A == set():
        return emptyset()
    set_string = "{"
    for elem in A:
        set_string += str(elem) + ", "
    set_string = set_string[0:-2]
    set_string += "}"
    return set_string


# and string
def aand():
    return "and"


# or string
def oor():
    return "or"


# exists symbol
def exists():
    return u'\u2203'


# not exists symbol
def nexists():
    return u'\u2204'


# for all symbol
def forall():
    return u'\u2200'


# right arrow symbol
def rarrow():
    return u'\u2192'


# comma symbol
def com():
    return ","