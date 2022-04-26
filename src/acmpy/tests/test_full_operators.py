"""Tests the full_operators.py module."""

from math import isclose
from sympy import Matrix, S, Rational, shape
from acmpy.internal_operators import OperatorSum, ACM_Hamiltonian
from acmpy.full_operators import RepXspace


class TestRepXSpace:
    """Tests the RepXSpace() function."""
    def test_ham11_01010(self):
        ham11: OperatorSum = ACM_Hamiltonian(c11=1)
        L_matrix: Matrix = RepXspace(ham11, S.One, Rational(5, 2), 0, 1, 0, 1, 0)
        assert shape(L_matrix) == (2, 2)
        L_matrix_expected: Matrix = Matrix([[-2.50000000000000, 1.58113883000000],
                                            [1.58113883000000, -4.50000000000000]])
        for i in range(2):
            for j in range(2):
                assert isclose(L_matrix[i, j], L_matrix_expected[i, j])
