from pathlib import Path
import pytest
from acmpy.compat import require_int, require_nonnegint, require_posint, \
    parse_line_float, readdata_float


class TestRequireInt:
    """Tests require_int(name, value)."""

    def test_ok(self):
        require_int('x', -1)
        require_int('y', 0)
        require_int('z', 1)

    def test_type_error(self):
        with pytest.raises(TypeError):
            require_int('x', 1.0)
        with pytest.raises(TypeError):
            require_int('y', '1')


class TestRequireNonNegInt:
    """Tests require_nonnegint(name, value)."""

    def test_ok(self):
        require_nonnegint('y', 0)
        require_nonnegint('z', 1)

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
        require_posint('z', 1)

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


class TestParseLineFloat:
    """Tests parse_line_float(line)."""

    def test_ok(self):
        line: str = ' +1.000000e+00      0    1    0      1    1    2      1    1    2'
        value: float = parse_line_float(line)
        assert value == 1.0

    def test_error(self):
        line: str = 'abc'
        with pytest.raises(ValueError):
            parse_line_float(line)


class TestReadDataFloat:
    """Tests readdata_float(filename)."""

    def test_ok(self, tmp_path: Path):
        filepath: Path = tmp_path / "data"
        filepath.write_text('1.0 1 1\n2.0 2 2\n3.0 3 3\n')
        filename: str = str(filepath)
        data: list[float] = readdata_float(filename)
        assert len(data) == 3
        assert data[0] == 1.0
        assert data[1] == 2.0
        assert data[2] == 3.0
