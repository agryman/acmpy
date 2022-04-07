"""This module tests the full_space.py module."""

import pytest

from sympy import Matrix, zeros, eye

from acmpy.full_space import Eigenfiddle


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
