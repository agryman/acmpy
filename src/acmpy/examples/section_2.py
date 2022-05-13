"""This module contains examples from Section 2 of the Maple worksheet acm1.4a-examples.mw."""

import math
from typing import ClassVar
from sympy import Expr, Rational, S
from acmpy.globals import ACM_set_listln, ACM_set_eig_fit, ACM_set_rat_fit, ACM_set_rat_lst, ACM_set_amp_lst, \
    ACM_add_rat_lst, ACM_add_amp_lst, ACM_set_scales, ACM_show_scales
from acmpy.internal_operators import OperatorSum, ACM_Hamiltonian
from acmpy.full_space import ACM_Scale, ACM_Adapt
from acmpy.examples.example import Example
from acmpy.examples.section_1 import Example_1_2

B: int = 20


def make_RWC_ham_fig5a() -> OperatorSum:
    c2: Expr = Rational(3, 2)
    c1: Expr = 1 - 2 * c2
    chi: Expr = S(2)
    kappa: Expr = S.Zero

    return make_RWC_ham(B, c1, c2, chi, kappa)


def make_RWC_ham(B, c1, c2, chi, kappa) -> OperatorSum:
    x1: Expr = -Rational(1, 2) / B
    x3: Expr = B * c1 / 2
    x4: Expr = B * c2 / 2
    x6: Expr = -chi
    x10: Expr = kappa

    return ACM_Hamiltonian(x1, 0, x3, x4, 0, x6, 0, 0, 0, x10)


class Fig5aExample(Example):
    ham: ClassVar[OperatorSum] = make_RWC_ham_fig5a()
    B: ClassVar[int] = B


class Example_2_2_a(Fig5aExample):
    predecessor = Example_1_2

    @classmethod
    def exec(cls):
        ACM_Scale(cls.ham, math.sqrt(cls.B), 2.5, 0, 5, 0, 18, 0, 6)


class Example_2_2_b(Fig5aExample):
    predecessor = Example_2_2_a

    @classmethod
    def exec(cls):
        ACM_Scale(cls.ham, math.sqrt(cls.B), 2.5, 0, 10, 0, 18, 0, 6)


class Example_2_2_c(Fig5aExample):
    predecessor = Example_2_2_b

    @classmethod
    def exec(cls):
        ACM_Scale(cls.ham, math.sqrt(cls.B), 2.5, 0, 15, 0, 18, 0, 6)


class Example_2_2_d(Fig5aExample):
    predecessor = Example_2_2_c

    @classmethod
    def exec(cls):
        ACM_Scale(cls.ham, math.sqrt(cls.B), 2.5, 0, 10, 0, 6, 0, 6)


class Example_2_3_a(Fig5aExample):
    predecessor = Example_2_2_d

    @classmethod
    def set(cls):
        ACM_set_rat_lst(((2, 0, 1, 1), (4, 2, 1, 1), (6, 4, 1, 1), (8, 6, 1, 1)))
        ACM_set_amp_lst(((2, 2, 1, 1),))

    @classmethod
    def exec(cls):
        ACM_Scale(cls.ham, math.sqrt(cls.B), 2.5, 0, 10, 0, 18, 0, 6)


class Example_2_3_b(Fig5aExample):
    predecessor = Example_2_3_a

    @classmethod
    def set(cls):
        ACM_add_rat_lst(((2, 2, 1, 1), (4, 4, 1, 1), (6, 6, 1, 1), (8, 8, 1, 1)))
        ACM_add_amp_lst(((2, 2, 2, 2),))

    @classmethod
    def exec(cls):
        ACM_Scale(cls.ham, math.sqrt(cls.B), 2.5, 0, 10, 0, 18, 0, 6)


class Example_2_3_c(Fig5aExample):
    predecessor = Example_2_3_b

    @classmethod
    def set(cls):
        ACM_set_rat_lst(((2, 0, 1, 1, 2), (3, 2, 1, 2, 1)))
        ACM_set_amp_lst(((6, 6, 1, 1, -1),))

    @classmethod
    def exec(cls):
        ACM_Scale(cls.ham, math.sqrt(cls.B), 2.5, 0, 10, 0, 18, 0, 6)


class Example_2_4_a(Fig5aExample):
    predecessor = Example_2_3_c

    @classmethod
    def set(cls):
        ACM_set_scales(0.018, 0.0015)
        ACM_set_rat_lst(((2, 0, 1, 1, 2), (3, 2, 1, 2, 2), (4, 3, 2, 1, 2)))
        ACM_set_amp_lst(((2, 2, 1, 1), (2, 2, 2, 2)))

    @classmethod
    def exec(cls):
        ACM_Scale(cls.ham, math.sqrt(cls.B), 2.5, 0, 10, 0, 18, 0, 6)


class Example_2_4_b(Fig5aExample):
    predecessor = Example_2_4_a

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 10, 0, 18, 0, 6)
        ACM_show_scales(1)


class Example_2_4_c(Fig5aExample):
    predecessor = Example_2_4_b

    @classmethod
    def set(cls):
        ACM_set_eig_fit(100.0, 0, 2)
        ACM_set_rat_fit(100.0, 2, 2, 2, 1)

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 10, 0, 18, 0, 6)


class Example_2_4_d(Fig5aExample):
    predecessor = Example_2_4_c

    @classmethod
    def set(cls):
        ACM_set_eig_fit(6.0, 2, 1)
        ACM_set_rat_fit(100.0, 2, 0, 1, 1)
        ACM_set_rat_lst(((2, 0, 1, 1, 2), (3, 2, 1, 2, 2), (4, 3, 2, 1, 2), (4, 2, 2, 2, 2), (2, 2, 2, 1, 2)))
        ACM_add_rat_lst(((2, 0, 3, 2), (4, 2, 4, 3), (6, 4, 4, 4), (5, 4, 2, 3), (6, 5, 3, 2)))
        ACM_add_rat_lst(((2, 0, 2, 1), (0, 2, 2, 2), (0, 2, 2, 1), (4, 2, 3, 2)))
        ACM_add_rat_lst(((2, 0, 4, 3), (4, 2, 5, 4), (0, 2, 3, 1), (2, 0, 4, 1), (4, 4, 5, 1)))

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 10, 0, 12, 0, 12)


class Example_2_5_a(Fig5aExample):
    predecessor = Example_2_4_d

    @classmethod
    def set(cls):
        ACM_set_rat_lst(((2, 0), (2, 2)))
        ACM_set_amp_lst()

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 10, 0, 18, 0, 6)


class Example_2_5_b(Fig5aExample):
    predecessor = Example_2_5_a

    @classmethod
    def set(cls):
        ACM_set_rat_lst(((2,), (2, 0, 1)))

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 10, 0, 18, 0, 6)


class Example_2_5_c(Fig5aExample):
    predecessor = Example_2_5_b

    @classmethod
    def set(cls):
        ACM_set_listln(3, 6)

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 10, 0, 18, 0, 6)

    @classmethod
    def unset(cls):
        ACM_set_listln(6, 4)
