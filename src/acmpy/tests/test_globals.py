"""This module tests the globals.py module."""
import pytest

from acmpy.globals import ACM_version, ACM_set_basis_type, ACM_show_lambda_fun


class TestACMVersion:
    """Tests ACM_version."""

    def test_ok(self):
        assert ACM_version == '1.4'


class TestACM_show_lambda_fun:
    """Tests the ACM_show_lambda_fun() function."""

    @pytest.mark.parametrize(
        "basis_type,expected", [
            (0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (1, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            (2, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]),
            (3, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        ]
    )
    def test_ok(self, basis_type, expected):
        ACM_set_basis_type(basis_type, 0.0, 0)
        lambda_v = ACM_show_lambda_fun()
        assert all(x == y for (x, y) in zip(lambda_v, expected))