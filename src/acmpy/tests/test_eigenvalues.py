"""This module tests the eignevalues.py module."""
import pytest
import numpy as np
from sympy import Matrix, shape, diag
from acmpy.compat import is_zeros, is_close, is_sorted, ABS_TOL
from acmpy.eigenvalues import Eigenvectors, Eigenfiddle, Matrix_to_ndarray, ndarray_to_Matrix


def is_solution(M: Matrix, vals: list[float], P: Matrix, abs_tol: float = ABS_TOL) -> bool:
    """Return True if and only if the eigenvalues and eigenvectors of M are vals and P."""
    n: int = len(vals)
    if shape(M) == (n, n) == shape(P):
        D: Matrix = diag(*vals)

        # a solution must satisfy MP = PD, therefore MP - PD = 0
        return is_zeros(list(M * P - P * D))

    return False


def is_sorted_solution(M: Matrix, vals: list[float], P: Matrix, abs_tol: float = ABS_TOL) -> bool:
    """Return True if and only if (M, vals, P) is a solution, and vals is in ascending order."""
    if not is_sorted(vals):
        return False
    return is_solution(M, vals, P, abs_tol)


@pytest.fixture
def solution_4x4():
    M = [[3, -2, 4, -2],
         [5, 3, -3, -2],
         [5, -2, 2, -2],
         [5, -2, -3, 3]]
    vals = [-2, 3, 5, 5]
    P = [[0, 1, 1, 0],
         [1, 1, 1, -1],
         [1, 1, 1, 0],
         [1, 1, 0, 1]]
    return M, vals, P


def test_solution_4x4(solution_4x4):
    M, vals, P = solution_4x4
    assert is_solution(Matrix(M), vals, Matrix(P))


class TestMatrix_to_ndarray:
    """Tests the Matrix_to_ndarray() function."""

    def test_ok_solution_4x4(self, solution_4x4):
        M: list[list[float]] = solution_4x4[0]
        A: Matrix = Matrix(M)
        expected_B: np.ndarray = np.array(M)

        B: np.ndarray = Matrix_to_ndarray(A)
        assert B.shape == expected_B.shape
        assert is_zeros((B - expected_B).flat)


class TestNdarray_to_Matrix:
    """Tests the ndarray_to_Matrix() function."""

    def test_ok_solution_4x4(self, solution_4x4):
        M: list[list[float]] = solution_4x4[0]
        A: np.ndarray = np.array(M)
        expected_B: Matrix = Matrix(M)

        B: Matrix = ndarray_to_Matrix(A)
        assert shape(B) == shape(expected_B)
        assert is_zeros(list(B - expected_B))


class TestEigenvectors:
    """Test the Eigenvector function."""

    def test_ok_solution_4x4(self, solution_4x4):
        M: Matrix = Matrix(solution_4x4[0])

        values: list[float]
        P: Matrix
        values, P = Eigenvectors(M)
        assert is_solution(M, values, P)


@pytest.fixture
def c11_010101():
    M = [[-2.50000000000000, 1.58113883000000],
         [1.58113883000000, -4.50000000000000]]
    vals = [-5.37082869331582, -1.62917130668418]
    P = [[-0.482430055114118, -0.875934496365219],
         [0.875934496365219, -0.482430055114118]]
    return M, vals, P


def test_c11_010101(c11_010101):
    M = Matrix(c11_010101[0])
    vals = c11_010101[1]
    P = Matrix(c11_010101[2])
    assert is_sorted_solution(M, vals, P)


class TestEigenfiddle:
    """Tests the Eigenfiddle() function."""

    def test_ok_c11_010101(self, c11_010101):
        M: Matrix = Matrix(c11_010101[0])
        eigenvalues, P = Eigenfiddle(M)
        assert is_sorted_solution(M, eigenvalues, P)

        expected_eigenvalues: list[float] = c11_010101[1]
        assert is_close(eigenvalues, expected_eigenvalues)
