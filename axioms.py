from math_strings import *

class axioms:

    tf = {}

    def __init__(self, transit_function):
        self.tf = transit_function

    def R(self, u, v):
        return sstr(self.tf[(u, v)])

    def b1_1(self, u, v, x):
        cond_0 = x in self.tf[(u, v)] and x != v

        impl_0 = v not in self.tf[(u, x)]

        if cond_0 and not impl_0:
            print("VIOLATE (b1_1)")
            print("u ->", u, ", x ->", x, ", v ->", v)
            print(x, elem(), r(u, v), nimplies(), v, nelem(), r(u, x))
            print(x, elem(), self.R(u, v), nimplies(), v, nelem(), self.R(u, x))
            print("---")
            return False
        return True

    def b1_2(self, u, v, x):
        cond_0 = x in self.tf[(u, v)] and x != u

        impl_0 = u not in self.tf[(x, v)]

        if (cond_0) and not impl_0:
            print("VIOLATE (b1_2)")
            print("u ->", u, ", x ->", x, ", v ->", v)
            print(x, elem(), r(u, v), nimplies(), u, nelem(), r(x, v))
            print(x, elem(), self.R(u, v), nimplies(), u, nelem(), self.R(x, v))
            print("---")
            return False
        return True

    def b2(self, u, v, w):
        cond_0 = w in self.tf[(u, v)]

        impl_0 = self.tf[(u, w)].union(self.tf[(w, v)]).issubset(self.tf[(u, v)])

        if cond_0 and not impl_0:
            print("VIOLATE (b2)")
            print("u ->", u, ", w ->", w, ", v ->", v)
            print(w, elem(), r(u, v), nimplies(), r(u, w), cup(), r(w, v), subseteq(), r(u, v))
            print(w, elem(), self.R(u, v), nimplies(), self.R(u, w), cup(), self.R(w, v), subseteq(), self.R(u, v))
            print("---")
            return False
        return True

    def b3_1(self, u, v, x, y):
        cond_0 = x in self.tf[(u, v)]
        cond_1 = y in self.tf[(u, x)]

        impl_0 = x in self.tf[(y, v)]

        ret_dic = {}

        if (cond_0 and cond_1) and not impl_0:
            print("VIOLATE (b3_1")
            print("u ->", u, ", x ->", x, ", y ->", y, ", v ->", v)
            print(x, elem(), r(u, v), aand(), y, elem(), r(u, x), nimplies(), x, elem(), r(y, v))
            print(x, elem(), self.R(u, v), aand(), y, elem(), self.R(u, x), nimplies(), x, elem(), self.R(y, v))
            ret_dic[(y, v)] = self.tf[(y, v)].union({x})
            print("---")
            return False
        return True


    def b3_2(self, u, v, x, y):
        cond_0 = x in self.tf[(u, v)]
        cond_1 = y in self.tf[(x, v)]

        impl_0 = x in self.tf[(u, y)]

        ret_dic = {}

        if (cond_0 and cond_1) and not impl_0:
            print("VIOLATE (b3_2)")
            print("u ->", u, ", x ->", x, ", y ->", y, ", v ->", v)
            print(x, elem(), r(u, v), aand(), y, elem(), r(x, v), nimplies(),
                  x, elem(), r(u, y))
            print(x, elem(), self.R(u, v), aand(), y, elem(), self.R(x, v), nimplies(),
                  x, elem(), self.R(u, y))
            ret_dic[(u, y)] = self.tf[(u, y)].union({x})
            print("---")
            return False
        return True

    def b5(self, u, v, w):
        cond_0 = self.tf[(u, v)].intersection(self.tf[(v, w)]) == {v}

        impl_0 = self.tf[(u, v)].union(self.tf[(v, w)]).issubset(self.tf[(u, w)])

        if cond_0 and not impl_0:
            print("VIOLATE b5")
            print("u ->", u, ", w ->", w, ", v ->", v)
            print(r(u, v), cap(), r(v, w), eq(), sstr({v}), nimplies(), r(u, v), cup(), r(v, w), subseteq(), r(u, w))
            print(self.R(u, v), cap(), self.R(v, w), eq(), sstr({v}), nimplies(), self.R(u, v), cup(), self.R(v, w), subseteq(), self.R(u, w))
            print("---")
            return False
        return True

    def b6_1(self, u, v, w):
        cond_0 = self.tf[(v, u)] != set() and self.tf[(u, w)] != set()

        impl_0 = False

        for x in self.tf[(v, u)].intersection(self.tf[(u, w)]):
            if self.tf[(v, x)].intersection(self.tf[(x, w)]) == {x}:
                impl_0 = True

        if cond_0 and not impl_0:
            print("VIOLATE (b6_1)")
            print("u ->", u, ", w ->", w, ", v ->", v)
            print(r(v, u), neq(), emptyset(), aand(), r(u, w), neq(), emptyset(), nimplies(), exists(), "x such that",
                  r(v, "x"), cap(), r("x", w), eq(), sstr({"x"}))
            print(self.R(v, u), neq(), emptyset(), aand(), self.R(u, w), neq(), emptyset(), nimplies(), exists(), "x such that",
                  r(v, "x"), cap(), r("x", w), eq(), sstr({"x"}))
            print("---")
            return False
        return True

    def b6_2(self, u, v, w):
        cond_0 = self.tf[(u, v)] != set() and self.tf[(u, w)] != set()

        impl_0 = False

        for x in self.tf[(u, v)].intersection(self.tf[(u, w)]):
            if self.tf[(x, v)].intersection(self.tf[(x, w)]) == {x}:
                impl_0 = True

        if cond_0 and not impl_0:
            print("VIOLATE (b6_2)")
            print("u ->", u, ", w ->", w, ", v ->", v)
            print(r(u, v), neq(), emptyset(), aand(), r(u, w), neq(), emptyset(), nimplies(), exists(), "x",
                  "such that", r("x", v), cap(), r("x", w), eq(), sstr({"x"}))
            print(self.R(u, v), neq(), emptyset(), aand(), self.R(u, w), neq(), emptyset(), nimplies(), exists(), "x",
                  "such that", r("x", v), cap(), r("x", w), eq(), sstr({"x"}))
            print("---")
            return False
        return True

    def b6_3(self, u, v, w):
        cond_0 = self.tf[(v, u)] != set() and self.tf[(w, u)] != set()

        impl_0 = False

        for x in self.tf[(v, u)].intersection(self.tf[(w, u)]):
            if self.tf[(v, x)].intersection(self.tf[(w, x)]) == {x}:
                impl_0 = True

        if cond_0 and not impl_0:
            print("VIOLATE (b6_3)")
            print("u ->", u, ", w ->", w, ", v ->", v)
            print(r(v, u), neq(), emptyset(), aand(), r(w, u), neq(), emptyset(), nimplies(), exists(), "x'",
                  "such that", r(v, "x'"), cap(), r(w, "x'"), eq(), sstr({"x'"}))
            print(self.R(v, u), neq(), emptyset(), aand(), self.R(w, u), neq(), emptyset(), nimplies(), exists(), "x",
                  "such that", r(v, "x'"), cap(), r(w, "x'"), eq(), sstr({"x'"}))
            print("---")
            return False
        return True

    def tr2(self, u, v, w):
        cond_0 = self.tf[(u, w)] == set() or self.tf[(w, v)] == set()

        impl_0 = w not in self.tf[(u, v)]

        if cond_0 and not impl_0:
            print("VIOLATE (tr2)")
            print("u ->", u, ", w ->", w, ", v ->", v)
            print(r(u, w), eq(), emptyset(), oor(), r(w, v), eq(), emptyset(), nimplies(), w, nelem(), r(u, v))
            print(self.R(u, w), eq(), emptyset(), oor(), self.R(w, v), eq(), emptyset(), nimplies(), w, nelem(), self.R(u, v))
            print("---")
            return False
        return True

    def j2(self, u, v, x):
        cond_0 = self.tf[(u, x)] == {u, x}
        cond_1 = self.tf[(x, v)] == {x, v}
        cond_2 = self.tf[(u, v)] != {u, v}

        impl_0 = x in self.tf[(u, v)]

        if (cond_0 and cond_1 and cond_2) and not impl_0:
            print("VIOLATE (j2)")
            print("u ->", u, ", x ->", x, ", v ->", v)
            print(r(u, x), eq(), sstr({u, x}), ",", r(x, v), eq(), sstr({x, v}), ", and", r(u, v), neq(), sstr({u, v}),
            nimplies(), x, elem(), r(u, v))
            print(r(u, x), eq(), self.R(u, x), ",", r(x, v), eq(), self.R(x, v), ", and", r(u, v), eq(), self.R(u,v),
                  neq(), sstr({u, v}), nimplies(), x, elem(), r(u, v), eq(), self.R(u, v))
            print("---")
            return False
        return True

    def t0(self, u, v, w):
        cond_0 = self.tf[(u, w)] == {u, w}
        cond_1 = self.tf[(w, v)] == {w, v}

        impl_0 = self.tf[(u, v)] != set()

        if (cond_0 and cond_1) and not impl_0:
            print("VIOLATE (t0)")
            print("u ->", u, ", w ->", w, ", v ->", v)
            print(r(u, w), neq(), emptyset(), aand(), r(w, v), neq(), emptyset(),
                  nimplies(), r(u, v), neq(), emptyset())
            print("---")
            return False
        return True

    def t2s(self, u, v):
        cond_0 = self.tf[(u, v)] == self.tf[(v, u)]

        if not cond_0:
            print("VIOLATE (t2s)")
            print("u ->", u, ", v ->", v)
            print(r(u, v), neq(), r(v, u))
            print(self.R(u,v), neq(), self.R(v, u))
            print("---")
            return False
        return True

    def t2a(self, u, v):
        cond_0 = self.tf[(u, v)] != self.tf[(v, u)]

        if not cond_0:
            print("VIOLATE (t2a)")
            print("u ->", u, ", v ->", v)
            print(r(u, v), eq(), r(v, u))
            print(self.R(u, v), eq(), self.R(v, u))
            print("---")
            return False
        return True

    def t3(self, u):
        cond_0 = self.tf[(u, u)] == {u}

        if not cond_0:
            print("VIOLATE (t3)")
            print("u -> ", u)
            print(r(u, u), neq(), sstr({u}))
            print(self.R(u, u), neq(), sstr({u}))
            print("---")
            return False
        return True

    def b4(self, u, v, x):
        cond_0 = x in self.tf[(u, v)]

        impl_0 = self.tf[(u, x)].intersection(self.tf[(x, v)]) == {x}

        if cond_0 and not impl_0:
            print("VIOLATE (t3)")
            print("u -> ", u, "x -> ", x, "v -> ", v)
            print(x, elem(), r(u, v), nimplies(), r(u, x), cap(), r(x, v), eq(), sstr({x}))
            print("---")
            return False
        return True


    def F(self, u, v, x, y):
        cond_0 = self.tf[(u, v)] == {u, v} == self.tf[(v, u)]
        cond_1 = self.tf[(x, y)] == {x, y} == self.tf[(y, x)]
        cond_2 = v in self.tf[(u, x)]
        cond_3 = u in self.tf[(v, y)]

        impl_0 = x in self.tf[(v, y)]
        impl_1 = y in self.tf[(u, x)]

        if (cond_0 and cond_1 and cond_2 and cond_3) and not (impl_0 and impl_1):
            print("VIOLATE (F)")
            print("u -> ", u, "v -> ", v, "x -> ", x, "y -> ", y)
            print(r(u, v), eq(), r(v, u), eq(), sstr({u, v}), aand(),
                  r(x, y), eq(), r(y, x), eq(), sstr({x, y}), aand(),
                  v, elem(), r(u, x), aand(),
                  u, elem(), r(v, y), nimplies(),
                  x, elem(), r(v, y), aand(), y, elem(), r(u, x)
                  )
            print(self.R(u, v), eq(), self.R(v, u), eq(), sstr({u, v}), aand(),
                  self.R(x, y), eq(), self.R(y, x), eq(), sstr({x, y}), aand(),
                  v, elem(), self.R(u, x), aand(),
                  u, elem(), self.R(v, y), nimplies(),
                  x, elem(), self.R(v, y), aand(), y, elem(), self.R(u, x)
                  )
            print("---")
            return False
        return True

    def G(self, u, v, x, y):
        cond_0 = self.tf[(u, v)] == {u, v}
        cond_1 = self.tf[(x, y)] == {x, y} == self.tf[(y, x)]
        cond_2 = v in self.tf[(u, x)]

        impl_0 = x in self.tf[(v, y)]
        impl_1 = y in self.tf[(u, x)]
        impl_2 = v in self.tf[(u, y)]

        # Check if only one of the implications is true (cheesy xor)
        xor_impl_list = [b for b in [impl_0, impl_1, impl_2] if b == True]
        if len(xor_impl_list) == 1:
            xor_impl = True
        else:
            xor_impl = False

        if (cond_0 and cond_1 and cond_2) and not xor_impl:
            print("VIOLATE (G)")
            print("u -> ", u, "v -> ", v, "x -> ", x, "y -> ", y)
            print(
                r(u, v), eq(), sstr({u, v}), aand(),
                r(x, y), eq(), r(y, x), eq(), sstr({x, y}), aand(),
                v, elem(), r(u, x), nimplies(),
                "either", x, elem(), r(v, y), oor(),
                y, elem(), r(u, x), oor(),
                v, elem(), r(u, y)
            )
            print(
                self.R(u, v), eq(), sstr({u, v}), aand(),
                self.R(x, y), eq(), self.R(y, x), eq(), sstr({x, y}), aand(),
                v, elem(), self.R(u, x), nimplies(),
                "either", x, elem(), self.R(v, y), oor(),
                y, elem(), self.R(u, x), oor(),
                v, elem(), self.R(u, y)
            )
            print("---")
            return False
        return True


    def co0(self, u, v, x):
        cond_0 = x in self.tf[(u, v)]

        impl_0 = self.tf[(u, x)] == {u, x}
        impl_1 = self.tf[(x, v)] == {x, v}

        if cond_0 and not (impl_0 and impl_1):
            print("VIOLATE (co0)")
            print("u -> ", u, "v -> ", v, "x -> ", x)
            print(
                x, elem(), r(u, v), nimplies(),
                r(u, x), eq(), sstr({u, x}), aand(),
                r(x, v), eq(), sstr({x, v})
            )
            print(
                x, elem(), self.R(u, v), nimplies(),
                self.R(u, x), eq(), sstr({u, x}), aand(),
                self.R(x, v), eq(), sstr({x, v})
            )
            print("---")
            return False
        return True


    def co1(self, u, v, x):
        cond_0 = self.tf[(u, x)] == {u, x}
        cond_1 = self.tf[(x, v)] == {x, v}
        cond_2 = x in self.tf[(u, v)]
        cond_3 = u != v and u != x and v != x

        impl_0 = self.tf[(x, u)] == {x, u}
        impl_1 = self.tf[(v, x)] == {v, x}

        if (cond_0 and cond_1 and cond_2 and cond_3) and not (impl_0 and impl_1):
            print("VIOLATE (co1)")
            print(
                r(u, x), eq(), sstr({u, x}), aand(),
                r(x, v), eq(), sstr({x, v}), aand(),
                x, elem(), r(u, v), nimplies(),
                r(x, u), eq(), sstr({x, u}), oor(),
                r(v, x), eq(), sstr({v, x})
            )
            print(
                self.R(u, x), eq(), sstr({u, x}), aand(),
                self.R(x, v), eq(), sstr({x, v}), aand(),
                x, elem(), self.R(u, v), nimplies(),
                self.R(x, u), eq(), sstr({x, u}), oor(),
                self.R(v, x), eq(), sstr({v, x})
            )
            print("---")
            return False
        return True

    def co2(self, u, v, x, y):
        cond_0 = self.tf[(u, x)] == {u, x}
        cond_1 = self.tf[(u, y)] == {u, y}
        cond_2 = self.tf[(v, x)] == {v, x}
        cond_3 = len({u, v, x, y}) == len([u, v, x, y])

        impl_0 = self.tf[(v, y)] == {v, y}
        impl_1 = self.tf[(y, x)] == {y, x}
        impl_2 = self.tf[(u, v)] == {u, v}

        if (cond_0 and cond_1 and cond_2 and cond_3) and not (impl_0 or impl_1 or impl_2):
            print("Violate (co2)")
            print("u", rarrow(), u, com(), "v", rarrow(), v, com(),
                  "x", rarrow(), x, "y", rarrow(), y)
            print(r(u, x), eq(), sstr({u, x}), aand(),
                  r(u, y), eq(), sstr({u, y}), aand(),
                  r(v, x), eq(), sstr({v, x}), nimplies(),
                  r(v, y), eq(), sstr({v, y}), oor(),
                  r(y, x), eq(), sstr({y, x}), oor(),
                  r(u, v), eq(), sstr({u, v})
                  )
            print(self.R(u, x), eq(), sstr({u, x}), aand(),
                  self.R(u, y), eq(), sstr({u, y}), aand(),
                  self.R(v, x), eq(), sstr({v, x}), nimplies(),
                  self.R(v, y), eq(), sstr({v, y}), oor(),
                  self.R(y, x), eq(), sstr({y, x}), oor(),
                  self.R(u, v), eq(), sstr({u, v})
                  )
            print("--")
            return False
        return True


    def co3(self, u, v, x, y):
        cond_0 = len({u, v, x, y}) == len([u, v, x, y])
        cond_1 = x in self.tf[(u, y)]
        cond_2 = y in self.tf[(x, v)]
        cond_3 = self.tf[(y, u)] == {y, u}
        cond_4 = self.tf[(v, x)] == {v, x}

        impl_0 = self.tf[(u, v)] == {u, v}
        impl_1 = self.tf[(v, u)] == {v, u}

        if (cond_0 and cond_1 and cond_2 and cond_3 and cond_4) and not (impl_0 and impl_1):
            print("Violate (co3)")
            print("u", rarrow(), u, com(), "v", rarrow(), v, com(),
                  "x", rarrow(), x, "y", rarrow(), y)
            print(x, elem(), r(u, y), aand(),
                  y, elem(), r(x, v), aand(),
                  r(y, u), eq(), sstr({y, u}), aand(),
                  r(v, x), eq(), sstr({v, x}), nimplies(),
                  r(u, v), eq(), sstr({u, v}), aand(),
                  r(v, u), eq(), sstr({v, u}))
            print(x, elem(), self.R(u, y), aand(),
                  y, elem(), self.R(x, v), aand(),
                  self.R(y, u), eq(), sstr({y, u}), aand(),
                  self.R(v, x), eq(), sstr({v, x}), nimplies(),
                  self.R(u, v), eq(), sstr({u, v}), aand(),
                  self.R(v, u), eq(), sstr({v, u}))
            print("--")
            return False
        return True

    def g(self, u, v, x, y):
        cond_0 = x in self.tf[(u, v)]
        cond_1 = y in self.tf[(u, v)]

        impl_0 = x in self.tf[(u, y)] and y in self.tf[(x, v)]
        impl_1 = y in self.tf[(u, x)] and x in self.tf[(y, v)]

        if (cond_0 and cond_1) and not (impl_0 or impl_1):
            print("Violate (g)")
            print("u", rarrow(), u, com(), "v", rarrow(), v, com(),
                  "x", rarrow(), x, "y", rarrow(), y)
            print(
                x, elem(), r(u, v), aand(),
                y, elem(), r(u, v), nimplies(),
                x, elem(), r(u, y), aand(), y, elem(), r(x, v), oor(),
                y, elem(), r(u, x), aand(), x, elem(), r(y, v)
            )
            print(
                x, elem(), self.R(u, v), aand(),
                y, elem(), self.R(u, v), nimplies(),
                x, elem(), self.R(u, y), aand(), y, elem(), self.R(x, v), oor(),
                y, elem(), self.R(u, x), aand(), x, elem(), self.R(y, v)
            )
            print("--")
            return False
        return True


    def p(self, u, v, x):
        cond_0 = x in self.tf[(u, v)]

        impl_0 = self.tf[(u, x)].union(self.tf[(x, v)]) == self.tf[(u, v)]

        if cond_0 and not impl_0:
            print("Violate (p)")
            print("u", rarrow(), u, com(), "v", rarrow(), v, com(), "x", rarrow(), x)
            print(x, elem(), r(u, v), nimplies(),
                  r(u, x), cup(), r(x, v), eq(), r(u, v))
            print(x, elem(), self.R(u, v), nimplies(),
                  self.R(u, x), cup(), self.R(x, v), eq(), self.R(u, v))

    def med(self, u, v, w):
        cond_0 = self.tf[(u, w)] != set() and self.tf[(w, v)] != set()

        impl_0 = len(self.tf[(u, v)].intersection(self.tf[(u, w)]).intersection(self.tf[(w, v)])) == 1

        if cond_0 and not impl_0:
            print("VIOLATE (Med)")
            print("u ->", u, ", w ->", w, ", v ->", v)
            print(r(u, w), neq(), emptyset(), aand(), r(w, v), neq(), emptyset(), nimplies(),
                  r(u, v), cap(), r(u, w), cap(), r(w, v), neq(), sstr({"x"}), "for some x")
            print(self.R(u, w), neq(), emptyset(), aand(), self.R(w, v), neq(), emptyset(), nimplies(),
                  self.R(u, v), cap(), self.R(u, w), cap(), self.R(w, v), eq(),
                  sstr(self.tf[(u, v)].intersection(self.tf[(u, w)]).intersection(self.tf[(w, v)])), neq(),
                  sstr({"x"}), "for some x")
            print("---")
            return False
        return True

    def mod(self, u, v, w):
        cond_0 = self.tf[(u, w)] != set() and self.tf[(w, v)] != set()

        impl_0 = self.tf[(u, v)].intersection(self.tf[(u, w)]).intersection(self.tf[(w, v)]) != set()

        if cond_0 and not impl_0:
            print("VIOLATE (Mod)")
            print("u ->", u, ", w ->", w, ", v ->", v)
            print(r(u, w), neq(), emptyset(), aand(), r(w, v), neq(), emptyset(), nimplies(),
                  r(u, v), cap(), r(u, w), cap(), r(w, v), neq(), emptyset())
            print(self.R(u, w), neq(), emptyset(), aand(), self.R(w, v), neq(), emptyset(), nimplies(),
                  self.R(u, v), cap(), self.R(u, w), cap(), self.R(w, v), neq(), emptyset())
            print("---")
            return False
        return True

    def ta1(self, u, w, v):
        cond_0 = self.tf[(u, v)].intersection(self.tf[(u, w)]) == {u}
        cond_1 = self.tf[(u, v)].intersection(self.tf[(w, v)]) == {v}
        cond_2 = self.tf[(u, w)].intersection(self.tf[(w, v)]) == {w}
        cond_3 = self.tf[(w, v)] == {w, v}

        impl_0 = self.tf[(u, v)] == {u, v}
        impl_1 = self.tf[(u, w)] == {u, w}

        ret_dic = {}

        if (cond_0 and cond_1 and cond_2 and cond_3) and not (impl_0 and impl_1):
            print("VIOLATE (ta1)")
            print("u ->", u, ", w ->", w, ", v ->", v)
            print(r(u, v), cap(), r(u, w), eq(), sstr({u}), aand(),
                  r(u, v), cap(), r(w, v), eq(), sstr({v}), aand(),
                  r(u, w), cap(), r(w, v), eq(), sstr({w}), nimplies(),
                  r(u, v), eq(), sstr({u, v}), aand(),
                  r(u, w), eq(), sstr({u, w}))
            print(self.R(u, v), cap(), self.R(u, w), eq(), sstr({u}), aand(),
                  self.R(u, v), cap(), self.R(w, v), eq(), sstr({v}), aand(),
                  self.R(u, w), cap(), self.R(w, v), eq(), sstr({w}), nimplies(),
                  self.R(u, v), eq(), sstr({u, v}), aand(),
                  self.R(u, w), eq(), sstr({u, w}))
            ret_dic[(u, v)] = {u, v}
            ret_dic[(u, w)] = {u, w}
            print("---")
            return False
        return True

    def ta2(self, u, w, v):
        cond_0 = self.tf[(v, u)].intersection(self.tf[(w, u)]) == {u}
        cond_1 = self.tf[(v, u)].intersection(self.tf[(w, v)]) == {v}
        cond_2 = self.tf[(w, u)].intersection(self.tf[(w, v)]) == {w}
        cond_3 = self.tf[(w, v)] == {w, v}

        impl_0 = self.tf[(v, u)] == {v, u}
        impl_1 = self.tf[(w, u)] == {w, u}

        ret_dic = {}

        if (cond_0 and cond_1 and cond_2 and cond_3) and not (impl_0 and impl_1):
            print("VIOLATE (ta2)")
            print("u ->", u, ", w ->", w, ", v ->", v)
            print(r(v, u), cap(), r(w, u), eq(), sstr({u}),
                  r(v, u), cap(), r(w, v), eq(), sstr({v}),
                  r(w, u), cap(), r(w, v), eq(), sstr({w}), nimplies(),
                  r(v,u), eq(), sstr({v, u}), aand(),
                  r(w, u), eq, sstr({w,u}))
            print(self.R(v, u), cap(), self.R(w, u), eq(), sstr({u}),
                  self.R(v, u), cap(), self.R(w, v), eq(), sstr({v}),
                  self.R(w, u), cap(), self.R(w, v), eq(), sstr({w}), nimplies(),
                  self.R(v, u), eq(), sstr({v, u}), aand(),
                  self.R(w, u), eq, sstr({w, u}))
            ret_dic[(v, u)] = {v, u}
            ret_dic[(w, u)] = {w, u}
            print("---")
            return False
        return True

    def rv(self, u, x, y, v):
        cond_0 = self.tf[(u, x)] == {u, x}
        cond_1 = self.tf[(y, v)] == {y, v}
        cond_2 = x in self.tf[(u, v)] and y in self.tf[(u, v)]
        cond_3 = y not in self.tf[(x, v)]
        cond_4 = x not in self.tf[(u, y)]

        impl_0 = self.tf[(x, u)] == {x, u}
        impl_1 = self.tf[(v, y)] == {v, y}

        ret_dic = {}

        if (cond_0 and cond_1 and cond_2 and cond_3 and cond_4) and not (impl_0 and impl_1):
            print("VIOLATE (rv)")
            print("u ->", u, ", x ->", x, ", y ->", y, ", v ->", v)
            print(r(u, x), eq(), sstr({u, x}), aand(),
                  r(y, v), eq(), sstr({y, v}), aand(),
                  x, elem(), )
            if not impl_0:
                print("VIOLATE (rv): R", (x, u), "!=", {x, u}, "|", "R", (x, u), "=", self.tf[(x, u)])
                ret_dic[(x, u)] = {x, u}
            if not impl_1:
                print("VIOLATE (rv): R", (v, y), "!=", {v, y}, "|", "R", (v, y), "=", self.tf[(v, y)])
                ret_dic[(v, y)] = {v, y}
            print("---")
            return False
        return True