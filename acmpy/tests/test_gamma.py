from acmpy.gamma import norm

class TestNorm:

    def test_zero(self):
        assert 0.0 == norm(0, 0)

    def test_unit(self):
        assert 1.0 == norm(1, 0)

    def test_345(self):
        assert 5.0 == norm(3, 4)

    def test_symmetric(self):
        assert norm(1, 2) == norm(2, 1)
