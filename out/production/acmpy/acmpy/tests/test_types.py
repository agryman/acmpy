import pytest
from acmpy.types import require_int, require_nonnegint, require_posint


class TestRequireInt:
    """Tests require_int(name, value)."""

    def test_ok(self):
        assert require_int('x', -1)
        assert require_int('y', 0)
        assert require_int('z', 1)

    def test_type_error(self):
        with pytest.raises(TypeError):
            require_int('x', 1.0)
        with pytest.raises(TypeError):
            require_int('y', '1')


class TestRequireNonNegInt:
    """Tests require_nonnegint(name, value)."""

    def test_ok(self):
        assert require_nonnegint('y', 0)
        assert require_nonnegint('z', 1)

    def test_type_error(self):
        with pytest.raises(TypeError):
            require_nonnegint('x', 1.0)
        with pytest.raises(TypeError):
            require_nonnegint('y', '1')

    def test_value_error(self):
        with pytest.raises(ValueError):
            require_nonnegint('x', -1)


class TestRequirePosInt:
    """Tests require_posint(name, value)."""

    def test_ok(self):
        assert require_posint('z', 1)

    def test_type_error(self):
        with pytest.raises(TypeError):
            require_posint('x', 1.0)
        with pytest.raises(TypeError):
            require_posint('y', '1')

    def test_value_error(self):
        with pytest.raises(ValueError):
            require_posint('x', -1)
        with pytest.raises(ValueError):
            require_posint('y', 0)
