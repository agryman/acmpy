"""This module tests the full_space.py module."""

import pytest
from math import isclose

from sympy import Matrix, zeros, eye, Expr, S, Rational, shape

from acmpy.full_space import Eigenfiddle, DigXspace, EigenValues, EigenBases, XParams, LValues
from acmpy.internal_operators import OperatorSum, ACM_Hamiltonian


class TestEigenfiddle:
    """Test the Eigenfiddle function."""

    def test_error_not_square(self):
        M: Matrix = zeros(2, 3)
        with pytest.raises(ValueError):
            Eigenfiddle(M)

    def test_ok_identity(self):
        M: Matrix = eye(2)
        values: list[float]
        P: Matrix
        values, P = Eigenfiddle(M)
        assert values == [1, 1]
        assert P == M

    def test_ok_2_3(self):
        M: Matrix = Matrix([[2, 0], [0, 3]])
        values: list[float]
        P: Matrix
        values, P = Eigenfiddle(M)
        assert values == [2, 3]
        assert P == eye(2)

    def test_ok_3_2(self):
        M: Matrix = Matrix([[3, 0], [0, 2]])
        values: list[float]
        P: Matrix
        values, P = Eigenfiddle(M)
        assert values == [2, 3]
        assert P == Matrix([[0, 1], [1, 0]])


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
    def test_ham_op(self, ham_op: OperatorSum, expected: float):
        anorm: Expr = S.One
        lambda_base: Expr = Rational(5, 2)
        nu_min: int = 0
        nu_max: int = 0
        v_min: int = 0
        v_max: int = 0
        L_min: int = 0
        L_max: int = 0
        eigen_spaces: tuple[EigenValues, EigenBases, XParams, LValues] = \
            DigXspace(ham_op, anorm, lambda_base, nu_min, nu_max, v_min, v_max, L_min, L_max)

        eigen_vals: EigenValues = eigen_spaces[0]
        n: int = len(eigen_vals)
        assert n == 1

        eigen_val: list[float] = eigen_vals[0]
        m: int = len(eigen_val)
        assert m == 1

        assert isclose(eigen_val[0], expected)

        eigen_bases: EigenBases = eigen_spaces[1]
        assert n == len(eigen_bases)
        eigen_base: Matrix = eigen_bases[0]
        assert shape(eigen_base) == (m, m)

        Xparams: XParams = eigen_spaces[2]
        assert Xparams == (anorm, lambda_base, nu_min, nu_max, v_min, v_max)

        Lvals: LValues = eigen_spaces[3]
        assert n == len(Lvals)
        assert Lvals[0] == 0
