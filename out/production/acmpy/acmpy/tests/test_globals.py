"""This module tests the globals.py module."""

from acmpy.globals import ACM_version


class TestACMVersion:
    """Tests ACM_version."""

    def test_ok(self):
        assert ACM_version == '1.4'
