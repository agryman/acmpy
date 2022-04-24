"""This module tests the internal_operators.py module."""

from acmpy.internal_operators import Radial_Operators, Radial_Sm


class TestRadial:
    """Tests the Radial operator symbols."""

    def test_ok(self):
        assert Radial_Sm in Radial_Operators
