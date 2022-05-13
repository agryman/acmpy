"""This module contains examples from Section 3 of the Maple worksheet acm1.4a-examples.mw."""

import math
from typing import ClassVar
from acmpy.globals import ACM_set_listln, ACM_set_rat_lst, ACM_set_amp_lst
from acmpy.internal_operators import OperatorSum
from acmpy.full_space import ACM_Adapt, Show_Eigs, Show_Rats, Show_Amps, dimXspace
from acmpy.full_operators import lbsXspace
from acmpy.spherical_space import lbsSO5r3_rngVvarL, dimSO5r3_rngVvarL
from acmpy.examples.example import Example
from acmpy.examples.section_1 import Example_1_2
from acmpy.examples.section_2 import make_RWC_ham

B: int = 40


def make_RWC_ham_fig4c() -> OperatorSum:
    c2: float = 1.0
    c1: float = 1 - 2 * c2
    chi: float = 0.5
    kappa: float = 0.0

    return make_RWC_ham(B, c1, c2, chi, kappa)


class Fig4cExample(Example):
    ham: ClassVar[OperatorSum] = make_RWC_ham_fig4c()
    B: ClassVar[int] = B


class Example_3_2_a(Fig4cExample):
    predecessor = Example_1_2

    @classmethod
    def set(cls):
        ACM_set_listln(4)
        ACM_set_rat_lst()
        ACM_set_amp_lst()

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 5, 0, 12, 0, 7)


class Example_3_2_b(Fig4cExample):
    predecessor = Example_3_2_a

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 10, 0, 12, 0, 7)


class Example_3_2_c(Fig4cExample):
    predecessor = Example_3_2_b

    @classmethod
    def exec(cls):
        ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 15, 0, 12, 0, 7)


class Example_3_3_a(Fig4cExample):
    predecessor = Example_3_2_c

    @classmethod
    def set(cls):
        ACM_set_rat_lst(((2, 0, 1, 1, 2),))
        ACM_set_amp_lst(((2, 2, 1, 1),))

    @classmethod
    def exec(cls):
        EML = ACM_Adapt(cls.ham, math.sqrt(cls.B), 2.5, 0, 15, 0, 12, 0, 12)
        Show_Eigs(EML[0], EML[2], 6, 6)
        Show_Eigs(EML[0], EML[2], 6, 0, 2)
        Show_Rats(EML[1], EML[2], ((4, 2, 2, 2, 2), (2, 2, 2, 1), (3, 2, 1, 2), (5, 3, 1, 1, 2)))
        Show_Rats(EML[1], EML[2], ((4, 4, 3, 2), (5, 4, 2, 3), (7, 5, 2, 2), (4, 3, 3, 1), (6, 4, 3, 3), (8, 6, 3, 3)))
        Show_Rats(EML[1], EML[2], ((6, 6, 4, 3), (6, 6, 5, 3), (6, 5, 4, 2), (6, 5, 5, 2)))
        Show_Rats(EML[1], EML[2], ((0, 2, 3, 1), (0, 2, 4, 1)))
        Show_Amps(EML[1], EML[2], ((2, 2),), 6)


class Example_3_4_a(Example):
    predecessor = Example_3_3_a

    @classmethod
    def exec(cls):
        print(lbsSO5r3_rngVvarL(0, 12, 0, 7))


class Example_3_4_b(Example):
    predecessor = Example_3_4_a

    @classmethod
    def exec(cls):
        print(dimSO5r3_rngVvarL(0, 12, 0, 7))


class Example_3_4_c(Example):
    predecessor = Example_3_4_b

    @classmethod
    def exec(cls):
        print(lbsXspace(0, 3, 0, 12, 0, 7))


class Example_3_4_d(Example):
    predecessor = Example_3_4_c

    @classmethod
    def exec(cls):
        print(dimXspace(0, 3, 0, 12, 0, 7))
