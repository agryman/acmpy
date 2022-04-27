"""Tests the so5_so3_cg.py module."""

import pytest

from sympy import Rational, S

from acmpy.so5_so3_cg import CG_SO3, Wigner_3j


class TestWigner_3j:
    """Tests the Wigner_3j() function."""

    @pytest.mark.parametrize(
        "j1,j2,j3,m1,m2,m3,expected",
        [(0, 0, 0, 0, 0, 0, S.One),
         (1, 1, 1, 0, 0, 0, S.Zero)]
    )
    def test_ok(self, j1, j2, j3, m1, m2, m3, expected):
        assert Wigner_3j(j1, j2, j3, m1, m2, m3) == expected


class TestCG_SO3:
    """Tests the CG_SO3() function."""

    def test_error(self):
        with pytest.raises(ValueError):
            CG_SO3(Rational(1, 3), 0, 0, 0, 0, 0)

    @pytest.mark.parametrize(
        "j1,m1,j2,m2,j3,m3,expected",
        [(0, 0, 0, 0, 0, 0, S.One),
         (Rational(1, 2), Rational(1, 2), 0, 0, 0, 0, S.Zero)]
    )
    def test_ok(self, j1, m1, j2, m2, j3, m3, expected):
        assert CG_SO3(j1, m1, j2, m2, j3, m3) == expected
