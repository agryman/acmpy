"""This module tests the full_space.py module."""

import math
from math import isclose
import numpy as np
import pytest

from sympy import Matrix, Expr, S, Rational, shape, sqrt

from acmpy.compat import nonnegint, is_close, NDArrayFloat, ndarray_to_list
from acmpy.full_space import Eigenfiddle, DigXspace, EigenValues, EigenBases, XParams, LValues, \
    LBlockFullSpace, LBlockNDFloatArray, LBlocks, validate_Lvals
from acmpy.internal_operators import OperatorSum, ACM_Hamiltonian
from acmpy.globals import ACM_set_defaults


class TestEigenfiddle:
    """Test the Eigenfiddle function."""

    def test_error_not_square(self):
        M: np.ndarray = np.zeros((2, 3))
        with pytest.raises(ValueError):
            Eigenfiddle(M)

    def test_ok_identity(self):
        M: np.ndarray = np.eye(2)
        values: np.ndarray
        P: np.ndarray
        values, P = Eigenfiddle(M)
        assert all(values == np.array([1, 1]))

    def test_ok_2_3(self):
        M: np.ndarray = np.array([[2, 0], [0, 3]])
        values: np.ndarray
        P: np.ndarray
        values, P = Eigenfiddle(M)
        assert all(values == np.array([2, 3]))
        assert all(P.flat == np.eye(2).flat)

    def test_ok_3_2(self):
        M: np.ndarray = np.array([[3, 0], [0, 2]])
        values: np.ndarray
        P: np.ndarray
        values, P = Eigenfiddle(M)
        assert all(values.flat == np.array([2, 3]).flat)
        assert all(P.flat == np.array([[0, 1], [1, 0]]).flat)


@pytest.fixture
def RWC_ham_fig5a() -> tuple[OperatorSum, int]:
    B: int = 20
    c2: Expr = Rational(3, 2)
    c1: Expr = 1 - 2 * c2
    chi: Expr = S(2)

    x1: Expr = -Rational(1, 2) / B
    x3: Expr = B * c1 / 2
    x4: Expr = B * c2 / 2
    x6: Expr = -chi

    return ACM_Hamiltonian(x1, 0, x3, x4, 0, x6), B


class TestDigXspace:
    """Tests the DigXspace() function."""

    @pytest.mark.parametrize(
        "ham_op,expected",
        [(ACM_Hamiltonian(c11=1), -2.5),
         (ACM_Hamiltonian(c20=1), 1),
         (ACM_Hamiltonian(c21=1), 2.5),
         (ACM_Hamiltonian(c22=1), 6.25),
         (ACM_Hamiltonian(c23=1), 2 / 3),
         (ACM_Hamiltonian(c30=1), 0),
         (ACM_Hamiltonian(c31=1), 0),
         (ACM_Hamiltonian(c32=1), 0),
         (ACM_Hamiltonian(c33=1), 0),
         (ACM_Hamiltonian(c40=1), 0),
         (ACM_Hamiltonian(c41=1), 0),
         (ACM_Hamiltonian(c42=1), 0),
         (ACM_Hamiltonian(c43=1), 0),
         (ACM_Hamiltonian(c50=1), 0)]
    )
    def test_ham_op_000000(self, ham_op: OperatorSum, expected: float):
        eigen_spaces: tuple[EigenValues, EigenBases, XParams, LValues] = \
            DigXspace(ham_op, 1.0, 2.5, 0, 0, 0, 0, 0, 0)

        eigen_vals: EigenValues = eigen_spaces[0]
        n: int = len(eigen_vals)
        assert n == 1

        eigen_val: NDArrayFloat = eigen_vals[0]
        m: int = len(eigen_val)
        assert m == 1

        assert isclose(eigen_val[0], expected)

        eigen_bases: EigenBases = eigen_spaces[1]
        assert n == len(eigen_bases)
        eigen_base: Matrix = eigen_bases[0]
        assert shape(eigen_base) == (m, m)

        Xparams: XParams = eigen_spaces[2]
        assert Xparams == (1.0, 2.5, 0, 0, 0, 0)

        Lvals: LValues = eigen_spaces[3]
        assert n == len(Lvals)
        assert Lvals[0] == 0

    @pytest.mark.parametrize(
        "ham_op,expected",
        [(ACM_Hamiltonian(c11=1), [-5.37082869331582, -1.62917130668418]),
         (ACM_Hamiltonian(c20=1), [1, 1]),
         (ACM_Hamiltonian(c21=1), [1.62917130668418, 5.37082869331582]),
         (ACM_Hamiltonian(c22=1), [2.65419914678928, 28.8458008532107]),
         (ACM_Hamiltonian(c23=1), [0.245029645333333, 1.08830368800000]),
         (ACM_Hamiltonian(c30=1), [0.0, 0.0]),
         (ACM_Hamiltonian(c31=1), [0.0, 0.0]),
         (ACM_Hamiltonian(c32=1), [0.0, 0.0]),
         (ACM_Hamiltonian(c33=1), [0.0, 0.0]),
         (ACM_Hamiltonian(c40=1), [0.0, 0.0]),
         (ACM_Hamiltonian(c41=1), [0.0, 0.0]),
         (ACM_Hamiltonian(c42=1), [0.0, 0.0]),
         (ACM_Hamiltonian(c43=1), [0.0, 0.0]),
         (ACM_Hamiltonian(c50=1), [0.0, 0.0])]
    )
    def test_ham_op_010101(self, ham_op: OperatorSum, expected: list[float]):
        eigen_spaces: tuple[EigenValues, EigenBases, XParams, LValues] = \
            DigXspace(ham_op, 1.0, 2.5, 0, 1, 0, 1, 0, 1)

        eigen_vals: EigenValues = eigen_spaces[0]
        n: int = len(eigen_vals)
        assert n == 1

        eigen_val: NDArrayFloat = eigen_vals[0]
        m: int = len(eigen_val)
        assert m == 2

        for actual_val, expected_val in zip(eigen_val, expected):
            assert isclose(actual_val, expected_val)

    def test_RWC_ham_fig5a(self, RWC_ham_fig5a: tuple[OperatorSum, int]):
        ACM_set_defaults(0)

        ham_op: OperatorSum
        B: int
        ham_op, B = RWC_ham_fig5a

        anorm: float = math.sqrt(B)
        lambda_base: float = 2.5
        nu_max: nonnegint = 5
        v_max: nonnegint = 18
        L_max: nonnegint = 6

        eigenvalues: EigenValues
        eigenbases: EigenBases
        Xparams: XParams
        Lvalues: LValues
        eigenvalues, eigenbases, Xparams, Lvalues = \
            DigXspace(ham_op, anorm, lambda_base, 0, nu_max, 0, v_max, 0, L_max)
        assert len(eigenvalues) == len(eigenbases) == len(Lvalues)
        assert Xparams == (anorm, lambda_base, 0, nu_max, 0, v_max)
        assert Lvalues == [0, 2, 3, 4, 5, 6]
        expected_eigenvalues0 = \
            [-6.34375707499380, -4.78545798998482, -4.35747748405318, -3.48850681486454, -2.73134974998671,
             -2.25842037137952, -1.73459666025923, -1.13462248733653, -0.736777010494252, 0.160419162784534,
             0.521734783125385, 0.970033490381626, 1.95787532379122, 2.42764405036288, 3.00581475182882,
             3.18486516213996, 4.64346770256370, 5.05068078949680, 6.40881513104548, 6.84697423641121,
             7.20544375346920, 7.51749874359587, 8.31750292121193, 12.1843362699147, 12.4710174136258,
             14.0657418485429, 15.8072046367031, 17.2409316641216, 20.8190503413780, 26.5388079991238,
             27.5820693590971, 27.8399026988631, 31.1136235176620, 55.3686357370119, 63.0177158483787,
             65.8797570627707, 79.8590667187793, 81.0625504949505, 129.522857254927, 196.283915332330,
             251.523252295420, 521.303008835543]
        eigenvalues0: list[float] = ndarray_to_list(eigenvalues[0])
        assert len(eigenvalues0) == len(expected_eigenvalues0)
        assert is_close(eigenvalues0, expected_eigenvalues0, abs_tol=1e-6)


class TestLBlockFullSpace:
    """Tests the LBlockFullSpace class."""

    @pytest.mark.parametrize(
        "nu_max,expected",
        [(10, [(0, 33), (33, 77), (77, 99), (99, 154), (154, 176), (176, 231)]),
         (18, [(0, 57), (57, 133), (133, 171), (171, 266), (266, 304), (304, 399)])]
    )
    def test_ok(self, nu_max, expected):
        Lvals: list[nonnegint] = [0, 2, 3, 4, 5, 6]
        full_space: LBlockFullSpace = LBlockFullSpace(0, nu_max, 0, 6, Lvals)
        Lblocks: LBlocks = full_space.Lblocks
        for i, L in enumerate(Lvals):
            assert Lblocks[L] == expected[i]


class TestValidateLvals:
    """Tests the validate_Lvals() function."""

    def test_ok(self):
        validate_Lvals([0, 2, 3, 4, 5, 6])

    def test_empty(self):
        with pytest.raises(ValueError):
            validate_Lvals([])

    def test_negative(self):
        with pytest.raises(ValueError):
            validate_Lvals([-1])

    def test_not_strictly_increasing(self):
        with pytest.raises(ValueError):
            validate_Lvals([0, 0])
