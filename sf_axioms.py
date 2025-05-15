from math_strings import *

class axioms:

    stepfunction_set = set()

    def __init__(self, stepfunction):
        self.stepfunction_set = stepfunction

    # axiom_strings_stepfunctions = [
    #     "A", "B", "H", "C", "D", "F", "G", "E",
    #     "Pt", "Dd", "Dt", "Cw", "Cb", "Dm", "T1",
    #     "T2", "Tb2", "P4"
    # ]

    def A(self, u, v, x):
        # If(u, v, x) ∈ T
        # then(v, u, u) ∈ T
        # for all u, v, x ∈ V
        cond_0 = (u, v, x) in self.stepfunction_set

        impl_0 = (v, u, u) in self.stepfunction_set

        if cond_0 and not impl_0:
            print("VIOLATE (A)")
            print("u ->", u, ", x ->", x, ", v ->", v)
            print(tp(u, v, x), elem(), T(), nimplies(), tp(v, u, u), elem(), T())
            print("---")
            return False
        return True

    def B(self, u, v, x):
        # If(u, v, x) ∈ T
        # then(v, u, x) /∈ T
        # for all u, v, x ∈ V
        cond_0 = (u, v, x) in self.stepfunction_set

        impl_0 = (v, u, x) not in self.stepfunction_set

        if cond_0 and not impl_0:
            print("VIOLATE (B)")
            print("u ->", u, ", x ->", x, ", v ->", v)
            print(tp(u, v, x), elem(), T(), nimplies(), tp(v, u, x), nelem(), T())
            print("---")
            return False
        return True


    def H(self, u, v):
        # If
        # u̸ = v
        # then
        # there
        # exists
        # an
        # x ∈ V
        # such
        # that(u, x, v) ∈ T
        # for all u, v ∈ V
        cond_0 = u != v

        x_set = [t[1] for t in self.stepfunction_set if t[0] == u and t[2] == v]
        impl_0 = len(x_set) >= 1

        if cond_0 and not impl_0:
            print("VIOLATE (H)")
            print("u ->", u, ", v", "->", v)
            print(u, neq(), v, nimplies(), exists(), "x", "such that", tp(u, "x", v), elem(), T())
            print("---")
            return False
        return True

    def C(self, u, v, x, y):
        # If(u, v, x) ∈ T and (x, y, v) ∈ T
        # then(x, y, u) ∈ T;
        cond_0 = (u, v, x) in self.stepfunction_set
        cond_1 = (x, y, v) in self.stepfunction_set

        impl_0 = (x, y, u) in self.stepfunction_set

        if (cond_0 and cond_1) and not impl_0:
            print("VIOLATE (C)")
            print("u ->", u, ", v", "->", v, ", x", "->", x, ", y", "->", y)
            print(tp(u, v, x), elem(), T(), aand(), tp(x, y, v), elem(), T(),
                  nimplies(), tp(x, y, u), elem(), T())
            print("---")
            return False
        return True


    def D(self, u, v, x, y):
        # If(u, v, x) ∈ T and (x, y, v) ∈ T
        # then(u, v, y) ∈ T

        cond_0 = (u, v, x) in self.stepfunction_set
        cond_1 = (x, y, v) in self.stepfunction_set

        impl_0 = (u, v, y) in self.stepfunction_set

        if (cond_0 and cond_1) and not impl_0:
            print("VIOLATE (D)")
            print("u ->", u, ", v", "->", v, ", x", "->", x, ", y", "->", y)
            print(tp(u, v, x), elem(), T(), aand(), tp(x, y, v), elem(), T(),
                  nimplies(), tp(u, v, y), elem(), T())
            print("---")
            return False
        return True

    def F(self, u, v, x, y):
        # If(u, v, x) ∈ T, (v, u, y) ∈ T, and (x, y, y) ∈ T
        # then(x, y, u) ∈ T
        cond_0 = (u, v, x) in self.stepfunction_set
        cond_1 = (v, u, y) in self.stepfunction_set
        cond_2 = (x, y, y) in self.stepfunction_set

        impl_0 = (x, y, u) in self.stepfunction_set

        if (cond_0 and cond_1 and cond_2) and not impl_0:
            print("VIOLATE (F)")
            print("u ->", u, ", v", "->", v, ", x", "->", x, ", y", "->", y)
            print(tp(u, v, x), elem(), T(), aand(), tp(v, u, y), aand(), tp(x, y, y), elem(), T(),
                  nimplies(), tp(x, y, u), elem(), T())
            print("---")
            return False
        return True


    def G(self, u, v, x, y):
        # If(u, v, x) ∈ T and (x, y, y) ∈ T
        # then(x, y, u) ∈ T or (y, x, v) ∈ T or (u, v, y) ∈ T
        cond_0 = (u, v, x) in self.stepfunction_set
        cond_1 = (x, y, y) in self.stepfunction_set

        impl_0 = (x, y, u) in self.stepfunction_set
        impl_1 = (y, x, v) in self.stepfunction_set
        impl_2 = (u, v, y) in self.stepfunction_set

        if (cond_0 and cond_1) and not (impl_0 or impl_1 or impl_2):
            print("VIOLATE (G)")
            print("u ->", u, ", v", "->", v, ", x", "->", x, ", y", "->", y)
            print(tp(u, v, x), elem(), T(), aand(), tp(x, y, y), elem(), T(),
                  nimplies(), tp(x, y, y), elem(), T(),
                  oor(), tp(y, x, v), elem(), T(),
                  oor(), tp(u, v, y), elem(), T())
            print("---")
            return False
        return True

    def E(self, u, v, x, y):
        # If(u, v, x) ∈ T and (u, y, v) ∈ T
        # then
        # y = v
        cond_0 = (u, v, x) in self.stepfunction_set
        cond_1 = (u, y, v) in self.stepfunction_set

        impl_0 = y == v

        if (cond_0 and cond_1) and not impl_0:
            print("VIOLATE (E)")
            print("u ->", u, ", v", "->", v, ", x", "->", x, ", y", "->", y)
            print(tp(u, v, x), elem(), T(), aand(), tp(u, y, v), elem(), T(),
                  nimplies(), y, eq(), v)
            print("---")
            return False
        return True

    def Pt(self, u, v, x, y):
        # (u, v, x) ∈ T and (v, x, y) ∈ T
        # implies
        # that
        # (u, v, y) ∈ T.
        cond_0 = (u, v, x) in self.stepfunction_set
        cond_1 = (v, x, y) in self.stepfunction_set

        impl_0 = (u, v, y) in self.stepfunction_set

        if (cond_0 and cond_1) and not impl_0:
            print("VIOLATE (Pt)")
            print("u ->", u, ", v", "->", v, ", x", "->", x, ", y", "->", y)
            print(tp(u, v, x), elem(), T(), aand(), tp(v, x, y), elem(), T(),
                  nimplies(), tp(u, v, y), elem(), T())
            print("---")
            return False
        return True


    def Dd(self, u, v, w, x, y, z, d):
        # (x, d, v) ∈ T, (u, d, v) ∈ T, (y, d, v) ∈ T,
        # (z, d, u) ∈ T, (v, d, u) ∈ T, (w, d, u) ∈ T
        # implies
        # that(x, u, y) /∈ T or (z, v, w) /∈ T
        cond_0 = (x, d, v) in self.stepfunction_set
        cond_1 = (u, d, v) in self.stepfunction_set
        cond_2 = (y, d, v) in self.stepfunction_set

        cond_3 = (z, d, u) in self.stepfunction_set
        cond_4 = (v, d, u) in self.stepfunction_set
        cond_5 = (w, d, u) in self.stepfunction_set

        impl_0 = (x, u, y) not in self.stepfunction_set
        impl_1 = (z, v, w) not in self.stepfunction_set

        if (cond_0 and cond_1 and cond_2 and cond_3 and cond_4 and cond_5) and not (impl_0 or impl_1):
            print("VIOLATE (Dd)")
            print("u ->", u, ", v", "->", v, ", x", "->", x, ", y", "->", y, ", z", "->", z, ", d", "->", d)
            print(tp(x, d, v), elem(), T(), aand(), tp(u, d, v), elem(), T(),
                  tp(y, d, v), elem(), T(), aand(), tp(z, d, u), elem(), T(),
                  tp(v, d, u), elem(), T(), aand(), tp(w, d, u), elem(), T(),
                  nimplies(), tp(x, u, y), nelem(), T(), oor(), tp(z, v, w), nelem(), T())
            print("---")
            return False
        return True

    def Dt(self, u, v, x, y, z):
        # (x, u, v) ∈ T, (y, u, v) ∈ T and (z, u, v) ∈ T
        # implies
        # that(x, y, z) /∈ T
        cond_0 = (x, u, v) in self.stepfunction_set
        cond_1 = (y, u, v) in self.stepfunction_set
        cond_2 = (z, u, v) in self.stepfunction_set

        impl_0 = (x, z, v) not in self.stepfunction_set

        if (cond_0 and cond_1 and cond_2) and not impl_0:
            print("VIOLATE (Dt)")
            print("u ->", u, ", v", "->", v, ", x", "->", x, ", y", "->", y, ", z", "->", z)
            print(tp(x, u, v), elem(), T(), aand(), tp(y, u, v), elem(), T(), tp(z, u, v), elem(), T(),
                  nimplies(), tp(x, z, v), nelem(), T())
            print("---")
            return False
        return True

    def Cw(self, u, v, x, y):
        # (u, v, x) ∈ T, (u, v, y) ∈ T
        # implies
        # that(x, v, y) /∈ T.
        cond_0 = (u, v, x) in self.stepfunction_set
        cond_1 = (u, v, y) in self.stepfunction_set

        impl_0 = (x, v, y) not in self.stepfunction_set

        if (cond_0 and cond_1) and not impl_0:
            print("VIOLATE (Cw)")
            print("u ->", u, ", v", "->", v, ", x", "->", x, ", y", "->", y)
            print(tp(u, v, x), elem(), T(), aand(), tp(u, v, y), elem(), T(),
                  nimplies(), tp(x, y, v), nelem(), T())
            print("---")
            return False
        return True


    def Cb(self, u, v, w, x, y):
        # (u, x, v) ∈ T, (u, y, w) ∈ T, (w, y, x) ∈
        # T, (v, x, y) ∈ T
        # implies
        # that(x, u, y) ∈ T.
        cond_0 = (u, x, v) in self.stepfunction_set
        cond_1 = (u, y, w) in self.stepfunction_set
        cond_2 = (w, y, x) in self.stepfunction_set
        cond_3 = (v, x, y) in self.stepfunction_set

        impl_0 = (x, u, y) in self.stepfunction_set

        if (cond_0 and cond_1 and cond_2 and cond_3) and not (impl_0):
            print("VIOLATE (Cb)")
            print("u ->", u, ", v", "->", v, ", x", "->", x, ", y", "->", y, ", w ->", w)
            print(tp(u, x, v), elem(), T(), aand(), tp(u, y, w), elem(), T(),
                  aand(), tp(w, y, x), elem(), T(), aand(), tp(v, x, y), elem(), T(),
                  nimplies(), tp(x, u, y), elem(), T())
            print("---")
            return False
        return True


    def Dm(self, u, v, x, y):
        # (u, x, v) ∈ T, (v, x, u) ∈ T,
        # (u, y, v) ∈ T, (v, y, u) ∈ T
        # implies
        # that(x, y, y) /∈ T
        cond_0 = (u, x, v) in self.stepfunction_set
        cond_1 = (v, x, u) in self.stepfunction_set
        cond_2 = (u, y, v) in self.stepfunction_set
        cond_3 = (v, y, u) in self.stepfunction_set

        impl_0 = (x, y, y) not in self.stepfunction_set

        if (cond_0 and cond_1 and cond_2 and cond_3) and not (impl_0):
            print("VIOLATE (Dm)")
            print("u ", "->", u, ", v", "->", v, ", x", "->", x, ", y", "->", y)
            print(tp(u, x, v), elem(), T(), aand(), tp(v, x, u), elem(), T(),
                  aand(), tp(u, y, v), elem(), T(), aand(), tp(v, y, u), elem(), T(),
                  nimplies(), tp(x, y, y), nelem(), T())
            print("---")
            return False
        return True

    def T1(self, x, y, t):
        # If
        # x̸ = y
        # then
        # there
        # exists
        # at
        # most
        # one
        # t ∈ V
        # such
        # that(x, t, y) ∈ T.
        cond_0 = x != y

        impl_0_set = set([t[1] for t in self.stepfunction_set if t[0] == x and t[2] == y])
        impl_0 = len(impl_0_set) <= 1

        if cond_0 and not impl_0:
            print("VIOLATE (T1)")
            print("x", "->", x, ", y", "->", y)
            print(x, neq(), y, nimplies(), exists() + "!", "t such that", tp(x, "t", y), elem(), T())
            print("---")
            return False
        return True

    def T2(self, x, y, z):
        # If(x, y, y) ∈ T, then(x, y, z) or (y, x, z) ∈ T
        cond_0 = (x, y, y) in self.stepfunction_set

        impl_0 = (x, y, z) in self.stepfunction_set
        impl_1 = (y, x, z) in self.stepfunction_set

        if (cond_0) and not (impl_0 or impl_1):
            print("VIOLATE (T2)")
            print("x ", "->", x, ", y", "->", y, ", z", "->", z)
            print(tp(x, y, y), elem(), T(),
                  nimplies(), tp(x, y, z), elem(), T(), oor(), tp(y, x, z), elem(), T())
            print("---")
            return False
        return True

    def Tb2(self, x, y, z, vertices):
        # If(x, y, y) ∈ T, then(x, y, z), or (y, x, z) ∈ T, or there
        # exists
        # w
        # such
        # that(x, w, z) ∈
        # T and (y, w, z) ∈ T.
        cond_0 = (x, y, y) in self.stepfunction_set

        impl_0 = (x, y, z) in self.stepfunction_set
        impl_1 = (y, x, z) in self.stepfunction_set
        impl_2 = False

        for w in vertices:
            if (x, w, z) in self.stepfunction_set and (y, w, z) in self.stepfunction_set:
                impl_2 = True

        if (cond_0) and not (impl_0 or impl_1 or impl_2):
            print("VIOLATE (Tb2)")
            print("x ", "->", x, ", y", "->", y, ", z", "->", z)
            print(tp(x, y, y), elem(), T(),
                  nimplies(), tp(x, y, z), elem(), T(), oor(), tp(y, x, z), elem(), T(),
                  oor(), exists(), "w", "such that", tp(x, "w", y), elem(), T(),
                  aand(), tp(x, "w", x), elem(), T())
            print("---")
            return False
        return True

    def P4(self, u, v, x, y):
        # (u, x, y) ∈ T and (x, y, v) ∈ T
        # implies(u, v, v) ∈ T.
        cond_0 = (u, x, y) in self.stepfunction_set
        cond_1 = (x, y, v) in self.stepfunction_set

        impl_0 = (u, v, v) in self.stepfunction_set

        if (cond_0 and cond_1) and not (impl_0):
            print("VIOLATE (Tb2)")
            print("u ", "->", u, ", x", "->", x, ", y", "->", y, ", v", "->", v)
            print(tp(u, x, y), elem(), T(), aand(), tp(x, y, v), elem(), T(),
                  nimplies(), tp(u, v, v), elem(), T())
            print("---")
            return False
        return True

    def Sm(self, u, v, w, x, y, z):
        #         (v, w, x) in T, (v, w, z) in T, (x, y, z) in T
        #         implies (v, w, y) in T
        cond_0 = (v, w, x) in self.stepfunction_set
        cond_1 = (v, w, z) in self.stepfunction_set
        cond_2 = (x, y, z) in self.stepfunction_set

        impl_0 = (v, w, y) in self.stepfunction_set

        if (cond_0 and cond_1 and cond_2) and not (impl_0):
            print("VIOLATE (Sm)")
            print("u ", "->", u, ", v", "->", v, ", w", "->", w, ", x", "->", x, ", y", "->", y, ", z", "->", z)
            print(tp(v, w, x), elem(), T(), aand(), tp(v, w, z), elem(), T(), aand(), tp(x, y, z), elem(), T(),
                  nimplies(), tp(v, w, y), elem(), T())
            print("---")
            return False
        return True




