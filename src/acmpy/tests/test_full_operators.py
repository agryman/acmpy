"""Tests the full_operators.py module."""

from sympy import S, Rational, shape
from acmpy.compat import NDArrayFloat, list_to_ndarray, is_nd_zeros
from acmpy.internal_operators import OperatorSum, ACM_Hamiltonian
from acmpy.full_operators import RepXspace


class TestRepXSpace:
    """Tests the RepXSpace() function."""
    def test_ham11_01010(self):
        ham11: OperatorSum = ACM_Hamiltonian(c11=1)
        L_matrix: NDArrayFloat = RepXspace(ham11, S.One, Rational(5, 2), 0, 1, 0, 1, 0)
        assert shape(L_matrix) == (2, 2)
        L_matrix_expected: NDArrayFloat = \
            list_to_ndarray([[-2.5, 1.58113883],
                             [1.58113883, -4.5]])
        assert is_nd_zeros(L_matrix - L_matrix_expected, abs_tol=1e-8)
