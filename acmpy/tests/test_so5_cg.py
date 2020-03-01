from acmpy.so5_cg import *
import pytest

class TestParse_v2:

    def test_valid(self):
        assert parse_v2('v2=7') == 7
        assert parse_v2('v2=42') == 42

    def test_invalid(self):
        assert parse_v2('v2=xxx') is None
        assert parse_v2('xxx') is None

    def test_type_error(self):
        with pytest.raises(TypeError):
            parse_v2(0)
