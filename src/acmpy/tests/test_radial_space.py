"""This module tests the radial_space.py module."""
import math

import pytest
import numpy as np
from sympy import Expr, Rational, Matrix, shape, sqrt
from acmpy.compat import nonnegint, NDArrayFloat, list_to_ndarray, Matrix_to_ndarray, \
    is_nd_square, is_nd_zeros, ndarray_to_Matrix
from acmpy.radial_space import Radial_Operators, Radial_Sm, Parse_RadialOp_List, Radial_D2b, KTSOps, KTSOp, KTOp, \
    RepRadial_bS_DS, Radial_b, Radial_b2, Radial_bm, Radial_bm2, ME_Radial_D2b, Matrix_sqrt, Matrix_sqrtInv, \
    RepRadial, ME_Radial_b2, RepRadial_b2_sqrt, RepRadial_b2_sqrtInv


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
        rep: Matrix = ndarray_to_Matrix(RepRadial_bS_DS(K, T, 1.0, 2.5, 0, 0, 0))
        assert shape(rep) == (1, 1)

        result: float = float(rep[0, 0])
        assert math.isclose(result, expected)

    def test_KT001(self):
        K: int = 0
        T: int = 2
        rep: Matrix = ndarray_to_Matrix(RepRadial_bS_DS(K, T, 1.0, 2.5, 0, 0, 1))
        assert shape(rep) == (2, 2)

        expected: Matrix = Matrix([[-Rational(7, 6), 7 * sqrt(10) / 30],
                                   [7 * sqrt(10) / 30, -Rational(19, 6)]])
        for i in range(2):
            for j in range(2):
                a: float = float(rep[i, j])
                b: float = float(expected[i, j])
                assert math.isclose(a, b)


def is_sqrt(A: NDArrayFloat, B: NDArrayFloat) -> bool:
    """Return True if and only if B is the square root of A."""
    return A.shape == B.shape and is_nd_square(A) and is_nd_square(B) and \
        is_nd_zeros(A - B @ B)


@pytest.fixture
def negative_eigenvalue():
    return [[1.0, 0.0], [0.0, -1.0]]


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

        c: NDArrayFloat = Matrix_sqrt(a)
        assert is_sqrt(a, c)

    def test_error(self, negative_eigenvalue):
        with pytest.raises(ValueError):
            Matrix_sqrt(list_to_ndarray(negative_eigenvalue))


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

        c: NDArrayFloat = Matrix_sqrtInv(a)
        assert is_sqrtInv(a, c)

    def test_error(self, negative_eigenvalue):
        with pytest.raises(ValueError):
            Matrix_sqrtInv(list_to_ndarray(negative_eigenvalue))


class TestRepRadial_b2:
    """Tests the function RepRadial(ME_Radial_b2,lambdaa,nu_min,nu_max)."""

    @pytest.mark.parametrize(
        "lambdaa,expected",
        [(1.5, [[1.5, 1.224744871, 0],
                [1.224744871, 3.5, 2.236067977],
                [0, 2.236067977, 5.5]]),
         (2.5, [[2.5, 1.581138830, 0],
                [1.581138830, 4.5, 2.645751311],
                [0, 2.645751311, 6.5]]),
         (3.5, [[3.5, 1.870828693, 0],
                [1.870828693, 5.5, 3.000000000],
                [0, 3.000000000, 7.5]])]
    )
    def test_ok_lambdaa_0_2(self, lambdaa, expected):
        M: NDArrayFloat = RepRadial(ME_Radial_b2, lambdaa, 0, 2)
        E: NDArrayFloat = list_to_ndarray(expected)
        assert is_nd_zeros(M - E, abs_tol=1e-8)


class TestRepRadial_b2_sqrt:
    """Tests the function RepRadial_b2_sqrt()."""

    @pytest.mark.parametrize(
        "lambdaa,expected",
        [(1.5, [[1.1399924967292594, 0.4416350979958686, -0.0733181261296921],
                [0.4416350979958685, 1.7273196202186405, 0.5668556869485478],
                [-0.0733181261296921, 0.5668556869485475, 2.2744887519077595]]),
         (2.5, [[1.5095567369200955, 0.465105189675075, -0.07011148662284702],
                [0.46510518967507464, 1.9805544807624136, 0.6009002506816244],
                [-0.07011148662284666, 0.6009002506816249, 2.4766920010720543]]),
         (3.5, [[1.8081231257144252, 0.47573443865408493, -0.06608711020447378],
                [0.47573443865408516, 2.2107294944926004, 0.6215720763185668],
                [-0.06608711020447351, 0.6215720763185667, 2.666323432707639]])]
    )
    def test_ok_lambdaa_0_2(self, lambdaa, expected):
        M_matrix: Matrix = RepRadial_b2_sqrt(lambdaa, 0, 2)
        M: NDArrayFloat = Matrix_to_ndarray(M_matrix)
        E: NDArrayFloat = list_to_ndarray(expected)
        assert is_nd_zeros(M - E, abs_tol=1e-8)


class TestRepRadial_b2_sqrtInv:
    """Tests the function RepRadial_b2_sqrtInv()."""

    @pytest.mark.parametrize(
        "lambdaa,expected",
        [(1.5, [[0.995749055010092, -0.28873857254624813, 0.10405835443216845],
                [-0.28873857254624824, 0.7142246336586133, -0.1873089352810563],
                [0.10405835443216849, -0.18730893528105635, 0.48969532067425214]]),
         (2.5, [[0.724171855619949, -0.19028873140113614, 0.06666848832931142],
                [-0.19028873140113617, 0.5950312523650533, -0.1497545332221874],
                [0.06666848832931148, -0.1497545332221874, 0.44198542366501603]]),
         (3.5, [[0.5918144360891456, -0.14070096400728224, 0.047468770908983014],
                [-0.14070096400728213, 0.5175181545494785, -0.12413098497731585],
                [0.047468770908983014, -0.1241309849773159, 0.40516218501861145]])]
    )
    def test_ok_lambdaa_0_2(self, lambdaa, expected):
        M_matrix: Matrix = RepRadial_b2_sqrtInv(lambdaa, 0, 2)
        M: NDArrayFloat = Matrix_to_ndarray(M_matrix)
        E: NDArrayFloat = list_to_ndarray(expected)
        assert is_nd_zeros(M - E, abs_tol=1e-8)
