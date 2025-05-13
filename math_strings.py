
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

def tstr(t):
    tuple_string = "("
    for e in t:
        tuple_string += str(e) + ", "
    tuple_string = tuple_string[0:-2] + ")"
    return tuple_string

def tp(u, v, w):
    return tstr((u, v, w))

def T():
    return "T"


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

def print_axiom_info(axiom):
    u = "u"
    v = "v"
    x = "x"
    y = "y"
    w = "w"

    if axiom == "t0":
        print("(t0) ", r(u, w), neq(), emptyset(), aand(), r(w, v), neq(), emptyset(),
              implies(), r(u, v), neq(), emptyset())

    if axiom == "t1":
        print("(t1) ", r(u, v), neq(), emptyset(), implies(), sstr({u, v}), subseteq(), r(u, v))

    if axiom == "t2s":
        print("(t2s) ", r(u, v), eq(), r(v, u))

    if axiom == "t2a":
        print("(t2a) ", r(u, v), neq(), r(v, u))

    if axiom == "t3":
        print("(t3) ", r(u, u), eq(), sstr({u}))

    if axiom == "tr2":
        print("(tr2) ", r(u, w), eq(), emptyset(), oor(), r(w, v), eq(), emptyset(),
              implies(), w, nelem(), r(u, v))

    if axiom == "b1":
        #b11
        print("(b1_1) ", x, elem(), r(u, v), implies(), v, nelem(), r(u, x))

    if axiom == "b1":
        #b12
        print("(b1_2) ", x, elem(), r(u, v), implies(), u, nelem(), r(x, v))

    if axiom == "b2":
        print("(b2) ", w, elem(), r(u, v), implies(), r(u, w), cup(), r(w, v), subseteq(), r(u, v))

    if axiom == "b3":
        #b31
        print("(b3_1) ", x, elem(), r(u, v), aand(), y, elem(), r(u, x), implies(), x, elem(), r(y, v))

    if axiom == "b3":
        #b32
        print("(b3_2) ", x, elem(), r(u, v), aand(), y, elem(), r(x, v), implies(),
              x, elem(), r(u, y))

    if axiom == "b4":
        print("(b4) ", x, elem(), r(u, v), implies(), r(u, x), cap(), r(x, v), eq(), sstr({x}))

    if axiom == "b6":
        #b61
        print("(b6_1) ", r(v, u), neq(), emptyset(), aand(), r(u, w), neq(), emptyset(), implies(), exists(), "x such that",
              r(v, "x"), cap(), r("x", w), eq(), sstr({"x"}))

    if axiom == "b6":
        #b62
        print("(b6_2) ", r(u, v), neq(), emptyset(), aand(), r(u, w), neq(), emptyset(), implies(), exists(), "x",
              "such that", r("x", v), cap(), r("x", w), eq(), sstr({"x"}))

    if axiom == "b6":
        #b63
        print("(b6_3) ", r(v, u), neq(), emptyset(), aand(), r(w, u), neq(), emptyset(), implies(), exists(), "x'",
              "such that", r(v, "x'"), cap(), r(w, "x'"), eq(), sstr({"x'"}))

    if axiom == "j2":
        print("(j2) ", r(u, x), eq(), sstr({u, x}), ",", r(x, v), eq(), sstr({x, v}), ", and", r(u, v), neq(), sstr({u, v}),
              implies(), x, elem(), r(u, v))

    if axiom == "F":
        print("(F) ", r(u, v), eq(), r(v, u), eq(), sstr({u, v}), aand(),
              r(x, y), eq(), r(y, x), eq(), sstr({x, y}), aand(),
              v, elem(), r(u, x), aand(),
              u, elem(), r(v, y), implies(),
              x, elem(), r(v, y), aand(), y, elem(), r(u, x)
              )

    if axiom == "G":
        print(
            "(G) ", r(u, v), eq(), sstr({u, v}), aand(),
            r(x, y), eq(), r(y, x), eq(), sstr({x, y}), aand(),
            v, elem(), r(u, x), implies(),
            "either", x, elem(), r(v, y), oor(),
            y, elem(), r(u, x), oor(),
            v, elem(), r(u, y)
        )

    if axiom == "co0":
        print(
            "(co0) ", x, elem(), r(u, v), implies(),
            r(u, x), eq(), sstr({u, x}), aand(),
            r(x, v), eq(), sstr({x, v})
        )

    if axiom == "co1":
        print(
            "(co1) ", r(u, x), eq(), sstr({u, x}), aand(),
            r(x, v), eq(), sstr({x, v}), aand(),
            x, elem(), r(u, v), implies(),
            r(x, u), eq(), sstr({x, u}), oor(),
            r(v, x), eq(), sstr({v, x})
        )

    if axiom == "co2":
        print(

              "(co2) ", r(u, x), eq(), sstr({u, x}), aand(),
              r(u, y), eq(), sstr({u, y}), aand(),
              r(v, x), eq(), sstr({v, x}), implies(),
              r(v, y), eq(), sstr({v, y}), oor(),
              r(y, x), eq(), sstr({y, x}), oor(),
              r(u, v), eq(), sstr({u, v})
              )

    if axiom == "co3":
        print("(co3) ", x, elem(), r(u, y), aand(),
              y, elem(), r(x, v), aand(),
              r(y, u), eq(), sstr({y, u}), aand(),
              r(v, x), eq(), sstr({v, x}), implies(),
              r(u, v), eq(), sstr({u, v}), aand(),
              r(v, u), eq(), sstr({v, u}))

    if axiom == "g":
        print(
            "(g) ", x, elem(), r(u, v), aand(),
            y, elem(), r(u, v), implies(),
            x, elem(), r(u, y), aand(), y, elem(), r(x, v), oor(),
            y, elem(), r(u, x), aand(), x, elem(), r(y, v)
        )

    if axiom == "p":
        print("(p) ", x, elem(), r(u, v), implies(),
              r(u, x), cup(), r(x, v), eq(), r(u, v))

    if axiom == "mod":
        print("(Mod) ", r(u, w), neq(), emptyset(), aand(), r(w, v), neq(), emptyset(), implies(),
              r(u, v), cap(), r(u, w), cap(), r(w, v), neq(), emptyset())

    if axiom == "med":
        print("(Med) ", r(u, w), neq(), emptyset(), aand(), r(w, v), neq(), emptyset(), implies(),
              r(u, v), cap(), r(u, w), cap(), r(w, v), neq(), sstr({"x"}), "for some x")

    if axiom == "b5":
        print("(b5) ", r(u, v), cap(), r(v, w), eq(), sstr({v}), implies(), r(u, v), cup(), r(v, w), subseteq(), r(u, w))


