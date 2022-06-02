"""This module contains examples from Section 3 of the Maple worksheet acm1.4a-examples.mw."""

import math
from typing import ClassVar
from sympy import Expr, Rational, S
from acmpy.globals import ACM_set_listln, ACM_set_amp_lst, \
    ACM_show_lambda_fun, ACM_set_basis_type, ACM_set_rat_lst
from acmpy.internal_operators import OperatorSum, ACM_Hamiltonian
from acmpy.full_space import ACM_Scale, ACM_Adapt, Show_Eigs, Show_Rats, Show_Amps, dimXspace
from acmpy.hamiltonian_data import RWC_alam
from acmpy.examples.example import Example
from acmpy.examples.section_1 import Example_1_2
from acmpy.examples.section_2 import make_RWC_ham


class Example_4_1_ham(Example):
    B: ClassVar[int] = 50
    c2: ClassVar[float] = 2.0
    c1: ClassVar[float] = 1 - 2 * c2
    chi: ClassVar[float] = 1.5
    kappa: ClassVar[float] = 1.0
    ham: ClassVar[OperatorSum] = make_RWC_ham(B, c1, c2, chi, kappa)


class Example_4_1_a(Example_4_1_ham):
    predecessor = Example_1_2

    @classmethod
    def exec(cls):
        print(cls.ham)


class Example_4_2_a(Example_4_1_ham):
    predecessor = Example_4_1_a

    @classmethod
    def set(cls):
        ACM_set_listln(4, 3)
        print(ACM_set_rat_lst(((2, 2, 2, 1), (4, 4, 2, 1), (4, 4, 3, 2), (4, 4, 4, 3),
                               (6, 6, 2, 1), (6, 6, 3, 2), (6, 6, 4, 3))))
        print(ACM_set_amp_lst(((2, 2, 1, 1),)))


class Example_4_3_a(Example_4_1_ham):
    predecessor = Example_4_2_a

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 11, 0, 21, 0, 8)


class Example_4_3_b(Example_4_1_ham):
    predecessor = Example_4_3_a

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 13, 0, 21, 0, 8)


class Example_4_3_c(Example_4_1_ham):
    predecessor = Example_4_3_b

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 15, 0, 21, 0, 8)


class Example_4_3_d(Example_4_1_ham):
    predecessor = Example_4_3_c

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 17, 0, 21, 0, 8)


class Example_4_3_e(Example_4_1_ham):
    predecessor = Example_4_3_d

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 19, 0, 21, 0, 8)


class Example_4_3_f(Example_4_1_ham):
    predecessor = Example_4_3_e

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 21, 0, 21, 0, 8)


class Example_4_4_alam(Example_4_1_ham):
    alam: ClassVar[tuple[float, float]] = RWC_alam(Example_4_1_ham.B,
                                                   Example_4_1_ham.c1,
                                                   Example_4_1_ham.c2)


class Example_4_4_a(Example_4_4_alam):
    predecessor = Example_4_3_f

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, cls.alam[0], cls.alam[1], 0, 3, 0, 21, 0, 8)


class Example_4_4_b(Example_4_4_alam):
    predecessor = Example_4_4_a

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, cls.alam[0], cls.alam[1], 0, 5, 0, 21, 0, 8)


class Example_4_4_c(Example_4_4_alam):
    predecessor = Example_4_4_b

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, cls.alam[0], cls.alam[1], 0, 7, 0, 21, 0, 8)


class Example_4_4_d(Example_4_4_alam):
    predecessor = Example_4_4_c

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, cls.alam[0], cls.alam[1], 0, 9, 0, 21, 0, 8)


class Example_4_4_e(Example_4_4_alam):
    predecessor = Example_4_4_d

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, cls.alam[0], cls.alam[1], 0, 11, 0, 21, 0, 8)


class Example_4_4_f(Example_4_4_alam):
    predecessor = Example_4_4_e

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, cls.alam[0], cls.alam[1], 0, 13, 0, 21, 0, 8)


class Example_4_5_a(Example_4_4_alam):
    predecessor = Example_4_4_f

    @classmethod
    def exec(cls):
        print(ACM_show_lambda_fun())


class Example_4_5_b(Example_4_4_alam):
    predecessor = Example_4_5_a

    @classmethod
    def set(cls):
        print(ACM_set_basis_type(1))

    @classmethod
    def exec(cls):
        print(ACM_show_lambda_fun())


class Example_4_5_c(Example_4_4_alam):
    predecessor = Example_4_5_b
    rat_lst = ((2, 0, 1, 1, 2),
               (2, 2, 2, 1),
               (4, 4, 2, 1),
               (4, 4, 3, 2),
               (4, 4, 4, 3),
               (6, 6, 2, 1),
               (6, 6, 3, 2),
               (6, 6, 4, 3))

    @classmethod
    def set(cls):
        print(ACM_set_rat_lst(cls.rat_lst))


class Example_4_5_d(Example_4_4_alam):
    predecessor = Example_4_5_c

    @classmethod
    def exec(cls):
        result = ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 5, 0, 5, 0, 8)
        # ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 11, 0, 21, 0, 8)
