"""This module tests the radial_space.py module."""

from acmpy.radial_space import Radial_Operators, Radial_Sm
from acmpy.radial_space import Parse_RadialOp_List, Radial_D2b, KTSOps, KTSOp, KTOp
from acmpy.radial_space import RepRadial_bS_DS
from acmpy.radial_space import Radial_b, Radial_b2, Radial_bm, Radial_bm2
from sympy import S, Expr, Rational, Matrix, shape
from math import isclose
import pytest


class TestRadial:
    """Tests the Radial operator symbols."""

    def test_ok(self):
        assert Radial_Sm in Radial_Operators


class TestParse_RadialOp_List:
    """Tests the Parse_RadialOp_List() function."""

    def test_Radial_D2b(self):
        parsed_ops: KTSOps = Parse_RadialOp_List([Radial_D2b])
        assert len(parsed_ops) == 1

        kts_op: KTSOp = parsed_ops[0]
        assert isinstance(kts_op, KTSOp)
        assert isinstance(kts_op, KTOp)

        kt_op: KTOp = kts_op
        assert kt_op.K == 0
        assert kt_op.T == 2

    @pytest.mark.parametrize(
        "rs_op, expected_K",
        [([Radial_b], 1),
         ([Radial_b2], 2),
         ([Radial_bm], -1),
         ([Radial_bm2], -2),
         ([Radial_b, Radial_b], 2),
         ([Radial_b, Radial_b, Radial_b], 3),
         ([Radial_b2, Radial_b2], 4),
         ([Radial_b2, Radial_b2, Radial_b2], 6)]
    )
    def test_Radial_bS(self, rs_op, expected_K):
        parsed_ops: KTSOps = Parse_RadialOp_List(rs_op)
        assert len(parsed_ops) == 1

        kts_op: KTSOp = parsed_ops[0]
        assert isinstance(kts_op, KTSOp)
        assert isinstance(kts_op, KTOp)

        kt_op: KTOp = kts_op
        assert kt_op.K == expected_K
        assert kt_op.T == 0


class TestRepRadial_bS_DS:
    """Tests the RepRadial_bS_DS() function."""

    @pytest.mark.parametrize(
        "K,T,expected",
        [(0, 0, 1),
         (1, 0, 1.581138830),
         (2, 0, 5 / 2),
         (3, 0, 3.952847075),
         (4, 0, 25 / 4),
         (0, 1, -0.3162277660),
         (0, 2, -7 / 6),
         (0, 3, 0.3689323937),
         (0, 4, 49 / 36),
         (-1, 0, 0.6324555320),
         (-2, 0, 2 / 3),
         (-3, 0, 0.4216370214),
         (-4, 0, 4 / 9),
         (1, 1, -1 / 2),
         (2, 2, -35 / 12),
         (3, 3, 35 / 24),
         (4, 4, 1225 / 144),
         (-1, 1, 1 / 3),
         (-2, 2, -7 / 9),
         (-3, 3, -7 / 27),
         (-4, 4, 49 / 81),
         (1, 4, 2.152105630),
         (2, 3, 0.9223309842),
         (3, 2, -4.611654921),
         (4, 1, -1.976423538)]
    )
    def test_KT(self, K, T, expected):
        anorm: Expr = S.One
        lambdaa: Expr = Rational(5, 2)
        R: int = 0
        nu_min: int = 0
        nu_max: int = 0

        rep: Matrix = RepRadial_bS_DS(K, T, anorm, lambdaa, R, nu_min, nu_max)
        assert shape(rep) == (1, 1)

        result: float = float(rep[0, 0])
        assert isclose(result, expected)
