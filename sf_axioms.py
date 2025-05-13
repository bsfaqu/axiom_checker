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
        pass

    def C(self, u, v, x, y):
        # If(u, v, x) ∈ T and (x, y, v) ∈ T
        # then(x, y, u) ∈ T;
        pass

    def D(self, u, v, x, y):
        # If(u, v, x) ∈ T and (x, y, v) ∈ T
        # then(u, v, y) ∈ T
        pass

    def F(self, u, v, x, y):
        # If(u, v, x) ∈ T, (v, u, y) ∈ T, and (x, y, y) ∈ T
        # then(x, y, u) ∈ T
        pass

    def G(self, u, v, x, y):
        # If(u, v, x) ∈ T and (x, y, y) ∈ T
        # then(x, y, u) ∈ T or (y, x, v) ∈ T or (u, v, y) ∈ T
        pass

    def E(self, u, v, x, y):
        # If(u, v, x) ∈ T and (u, y, v) ∈ T
        # then
        # y = v
        pass

    def Pt(self, u, v, x, y):
        # for any
        # four
        # vertices
        # u, v, x, y ∈ V, (u, v, x) ∈ T and (v, x, y) ∈ T
        # implies
        # that
        # (u, v, y) ∈ T.
        pass

    def Dd(self, u, v, w, x, y, z, d):
        # for any
        # seven
        # vertices
        # u, v, w, x, y, z, d ∈ V, (x, d, v) ∈ T, (u, d, v) ∈ T, (y, d, v) ∈ T,
        # (z, d, u) ∈ T, (v, d, u) ∈ T, (w, d, u) ∈ T
        # implies
        # that(x, u, y) /∈ T or (z, v, w) /∈ T
        pass

    def Dt(self, u, v, x, y, z):
        # For
        # any
        # five
        # vertices
        # u, v, x, y, z ∈ V, (x, u, v) ∈ T, (y, u, v) ∈ T and (z, u, v) ∈ T
        # implies
        # that(x, y, z) /∈ T
        pass

    def Cw(self, u, v, x, y):
        # For any
        # four
        # vertices
        # u, v, x, y, ∈ V, (u, v, x) ∈ T, (u, v, y) ∈ T
        # implies
        # that(x, v, y) /∈
        # T.
        pass

    def Cb(self, u, v, w, x, y):
        # For
        # any
        # five
        # vertices
        # u, v, w, x, y ∈ V, (u, x, v) ∈ T, (u, y, w) ∈ T, (w, y, x) ∈
        # T, (v, x, y) ∈ T
        # implies
        # that(x, u, y) ∈ T.
        pass

    def Dm(self, u, v, x, y):
        # for any
        # four
        # vertices
        # u, v, x, y ∈ V, (u, x, v) ∈ T, (v, x, u) ∈ T, (u, y, v) ∈ T, (v, y, u) ∈
        # T
        # implies
        # that(x, y, y) /∈ T
        pass

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
        pass

    def T2(self, x, y, z):
        # If(x, y, y) ∈ T, then(x, y, z) or (y, x, z) ∈ T
        pass

    def Tb2(self, x, y, z, w):
        # If(x, y, y) ∈ T, then(x, y, z), or (y, x, z) ∈ T, or there
        # exists
        # w
        # such
        # that(x, w, z) ∈
        # T and (y, w, z) ∈ T.
        pass

    def P4(self, u, v, x, y):
        # (u, x, y) ∈ T and (x, y, v) ∈ T
        # implies(u, v, v) ∈ T.
        pass