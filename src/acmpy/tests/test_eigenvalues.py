"""This module tests the eignevalues.py module."""

from sympy import Matrix

from acmpy.eigenvalues import Eigenvectors


class TestEigenvectors:
    """Test the Eigenvector function."""

    def test_ok_4x4(self):
        M: Matrix = Matrix([[3, -2, 4, -2],
                            [5, 3, -3, -2],
                            [5, -2, 2, -2],
                            [5, -2, -3, 3]])
        values: list[float]
        P: Matrix
        values, P = Eigenvectors(M)
        assert values == [-2, 3, 5, 5]
        assert P == Matrix([[0, 1, 1, 0],
                            [1, 1, 1, -1],
                            [1, 1, 1, 0],
                            [1, 1, 0, 1]])
