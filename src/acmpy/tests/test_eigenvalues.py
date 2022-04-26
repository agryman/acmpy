"""This module tests the eignevalues.py module."""

from math import isclose
from sympy import Matrix, shape, diag
from acmpy.eigenvalues import Eigenvectors, Eigenfiddle


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


class TestEigenfiddle:
    """Tests the Eigenfiddle() function."""

    def test_c11_010101(self):
        M: Matrix = Matrix([[-2.50000000000000, 1.58113883000000],
                            [1.58113883000000, -4.50000000000000]])
        expected_eigenvalues: list[float] = [-5.37082869331582, -1.62917130668418]
        expected_P: Matrix = Matrix([[-0.482430055114118, -0.875934496365219],
                                     [0.875934496365219, -0.482430055114118]])
        absolute_tolerance: float = 1e-14

        # verify that the expected result is correct
        expected_D: Matrix = diag(*expected_eigenvalues)
        expected_E: Matrix = M * expected_P - expected_P * expected_D
        for i in range(2):
            for j in range(2):
                assert isclose(expected_E[i, j], 0, abs_tol=absolute_tolerance)

        result: tuple[list[float], Matrix] = Eigenfiddle(M)

        eigenvalues: list[float] = result[0]
        assert len(eigenvalues) == 2

        # verify that the eigenvalues are correct and in the sorted order
        for i in range(2):
            assert isclose(eigenvalues[i], expected_eigenvalues[i])

        P: Matrix = result[1]
        assert shape(P) == (2, 2)

        # verify that the result is correct
        # note that the eigenbasis is only determined up to multiples of the eigenvectors
        D: Matrix = diag(*eigenvalues)
        E: Matrix = M * P - P * D
        for i in range(2):
            for j in range(2):
                assert isclose(E[i, j], 0, abs_tol=absolute_tolerance)
