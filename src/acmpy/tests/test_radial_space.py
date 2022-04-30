"""This module tests the radial_space.py module."""

import pytest
import numpy as np
from math import isclose
from sympy import S, Expr, Rational, Matrix, shape, sqrt, ImmutableMatrix
from acmpy.compat import nonnegint, NDArrayFloat, list_to_ndarray, is_zeros, Matrix_to_ndarray, ndarray_to_Matrix, \
    is_nd_square, is_nd_zeros
from acmpy.radial_space import Radial_Operators, Radial_Sm, Parse_RadialOp_List, Radial_D2b, KTSOps, KTSOp, KTOp, \
    RepRadial_bS_DS, Radial_b, Radial_b2, Radial_bm, Radial_bm2, ME_Radial_D2b, Matrix_sqrt, Matrix_sqrtInv


class TestRadial:
    """Tests the Radial operator symbols."""

    def test_ok(self):
        assert Radial_Sm in Radial_Operators


class TestParse_RadialOp_List:
    """Tests the Parse_RadialOp_List() function."""

    def test_Radial_D2b(self):
        parsed_ops: KTSOps = Parse_RadialOp_List((Radial_D2b,))
        assert len(parsed_ops) == 1

        kts_op: KTSOp = parsed_ops[0]
        assert isinstance(kts_op, KTSOp)
        assert isinstance(kts_op, KTOp)

        kt_op: KTOp = kts_op
        assert kt_op.K == 0
        assert kt_op.T == 2

    @pytest.mark.parametrize(
        "rs_op, expected_K",
        [((Radial_b,), 1),
         ((Radial_b2,), 2),
         ((Radial_bm,), -1),
         ((Radial_bm2,), -2),
         ((Radial_b, Radial_b), 2),
         ((Radial_b, Radial_b, Radial_b), 3),
         ((Radial_b2, Radial_b2), 4),
         ((Radial_b2, Radial_b2, Radial_b2), 6)]
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
    def test_KT000(self, K, T, expected):
        rep: Matrix = RepRadial_bS_DS(K, T, S.One, Rational(5, 2), 0, 0, 0)
        assert shape(rep) == (1, 1)

        result: float = float(rep[0, 0])
        assert isclose(result, expected)

    def test_KT001(self):
        K: int = 0
        T: int = 2
        rep: Matrix = RepRadial_bS_DS(K, T, S.One, Rational(5, 2), 0, 0, 1)
        assert shape(rep) == (2, 2)

        expected: Matrix = Matrix([[-Rational(7, 6), 7 * sqrt(10) / 30],
                                   [7 * sqrt(10) / 30, -Rational(19, 6)]])
        for i in range(2):
            for j in range(2):
                a: float = rep[i, j].evalf()
                b: float = expected[i, j].evalf()
                assert isclose(a, b)


class TestME_Radial_D2b:
    """Tests ME_Radial_D2b() function."""

    @pytest.mark.parametrize(
        "mu_f,mu_i,expected",
        [(0, 0, -Rational(7, 6)),
         (0, 1, 7 * sqrt(10) / 30),
         (1, 0, 7 * sqrt(10) / 30),
         (1, 1, -Rational(19, 6))]
    )
    def test_fi(self, mu_f: nonnegint, mu_i: nonnegint, expected: Expr):
        ME: Expr = ME_Radial_D2b(Rational(5, 2), mu_f, mu_i)
        a: float = ME.evalf()
        b: float = expected.evalf()
        assert isclose(a, b)


def is_sqrt(A: NDArrayFloat, B: NDArrayFloat) -> bool:
    """Return True if and only if B is the square root of A."""
    return A.shape == B.shape and is_nd_square(A) and is_nd_square(B) and \
        is_nd_zeros(A - B @ B)


class TestMatrix_sqrt:
    """Tests the Matrix_sqrt() function."""

    @pytest.mark.parametrize(
        "A,B",
        [([[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]]),
         ([[4.0, 0.0], [0.0, 9.0]], [[2.0, 0.0], [0.0, 3.0]])]
    )
    def test_ok(self, A: list[list[float]], B: list[list[float]]):
        a: NDArrayFloat = list_to_ndarray(A)
        b: NDArrayFloat = list_to_ndarray(B)
        assert is_sqrt(a, b)

        a_matrix: Matrix = ndarray_to_Matrix(a)
        c_matrix: Matrix = Matrix_sqrt(ImmutableMatrix(a_matrix))
        c: NDArrayFloat = Matrix_to_ndarray(c_matrix)
        assert is_sqrt(a, c)


def is_sqrtInv(A: NDArrayFloat, B: NDArrayFloat) -> bool:
    """Return True if and only if B is inverse of the square root of A."""
    return A.shape == B.shape and is_nd_square(A) and is_nd_square(B) and \
        is_nd_zeros(A @ B @ B - np.eye(A.shape[0]))


class TestMatrix_sqrtInv:
    """Tests the Matrix_sqrtInv() function."""

    @pytest.mark.parametrize(
        "A,B",
        [([[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]]),
         ([[4.0, 0.0], [0.0, 9.0]], [[1 / 2.0, 0.0], [0.0, 1 / 3.0]])]
    )
    def test_ok(self, A: list[list[float]], B: list[list[float]]):
        a: NDArrayFloat = list_to_ndarray(A)
        b: NDArrayFloat = list_to_ndarray(B)
        assert is_sqrtInv(a, b)

        a_matrix: Matrix = ndarray_to_Matrix(a)
        c_matrix: Matrix = Matrix_sqrtInv(ImmutableMatrix(a_matrix))
        c: NDArrayFloat = Matrix_to_ndarray(c_matrix)
        assert is_sqrtInv(a, c)
