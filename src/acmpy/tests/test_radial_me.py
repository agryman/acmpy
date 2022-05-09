"""Test radial matrix element functions."""
import math
import pytest
from sympy import sqrt, Rational, Expr
from acmpy.radial_space import Nu, ME_Radial_S0, ME_Radial_Sp, ME_Radial_Sm, \
    ME_Radial_b2, ME_Radial_bm2, ME_Radial_pt, ME_Radial_D2b, ME_Radial_bDb, \
    ME_Radial_b_pl, ME_Radial_bm_pl, ME_Radial_Db_pl, ME_Radial_b_ml, ME_Radial_bm_ml, \
    ME_Radial_Db_ml, ME_Radial_id_pl, ME_Radial_id_ml, MF_Radial_id_poly, MF_Radial_id_pl


class TestME_Radial_S0:
    """Test the ME_Radial_S0() function."""

    @pytest.mark.parametrize(
        "mu_f,mu_i,expected", [
            (0, 0, 1.2500000000),
            (0, 1, 0.0000000000),
            (0, 2, 0.0000000000),
            (1, 0, 0.0000000000),
            (1, 1, 2.2500000000),
            (1, 2, 0.0000000000),
            (2, 0, 0.0000000000),
            (2, 1, 0.0000000000),
            (2, 2, 3.2500000000)
        ]
    )
    def test_ok(self, mu_f, mu_i, expected):
        ME: float = ME_Radial_S0(2.5, mu_f, mu_i)
        assert math.isclose(ME, expected)


class TestME_Radial_Sp:
    """Test the ME_Radial_Sp() function."""

    @pytest.mark.parametrize(
        "mu_f,mu_i,expected", [
            (0, 0, 0.0000000000),
            (0, 1, 0.0000000000),
            (0, 2, 0.0000000000),
            (1, 0, 1.5811388300),
            (1, 1, 0.0000000000),
            (1, 2, 0.0000000000),
            (2, 0, 0.0000000000),
            (2, 1, 2.6457513110),
            (2, 2, 0.0000000000)
        ]
    )
    def test_ok(self, mu_f, mu_i, expected):
        ME: float = ME_Radial_Sp(2.5, mu_f, mu_i)
        assert math.isclose(ME, expected)


class TestME_Radial_Sm:
    """Test the ME_Radial_Sm() function."""

    @pytest.mark.parametrize(
        "mu_f,mu_i,expected", [
            (0, 0, 0.0000000000),
            (0, 1, 1.5811388300),
            (0, 2, 0.0000000000),
            (1, 0, 0.0000000000),
            (1, 1, 0.0000000000),
            (1, 2, 2.6457513110),
            (2, 0, 0.0000000000),
            (2, 1, 0.0000000000),
            (2, 2, 0.0000000000)
        ]
    )
    def test_ok(self, mu_f, mu_i, expected):
        ME: float = ME_Radial_Sm(2.5, mu_f, mu_i)
        assert math.isclose(ME, expected)


class TestME_Radial_b2:
    """Test the ME_Radial_b2() function."""

    @pytest.mark.parametrize(
        "mu_f,mu_i,expected", [
            (0, 0, 2.5000000000),
            (0, 1, 1.5811388300),
            (0, 2, 0.0000000000),
            (1, 0, 1.5811388300),
            (1, 1, 4.5000000000),
            (1, 2, 2.6457513110),
            (2, 0, 0.0000000000),
            (2, 1, 2.6457513110),
            (2, 2, 6.5000000000)
        ]
    )
    def test_ok(self, mu_f, mu_i, expected):
        ME: float = ME_Radial_b2(2.5, mu_f, mu_i)
        assert math.isclose(ME, expected)


class TestME_Radial_bm2:
    """Test the ME_Radial_bm2() function."""

    @pytest.mark.parametrize(
        "mu_f,mu_i,expected", [
            (0, 0, 0.6666666667),
            (0, 1, -0.4216370213),
            (0, 2, 0.3187276291),
            (1, 0, -0.4216370213),
            (1, 1, 0.6666666667),
            (1, 2, -0.5039526306),
            (2, 0, 0.3187276291),
            (2, 1, -0.5039526306),
            (2, 2, 0.6666666667)
        ]
    )
    def test_ok(self, mu_f, mu_i, expected):
        ME: float = ME_Radial_bm2(2.5, mu_f, mu_i)
        assert math.isclose(ME, expected)


class TestME_Radial_pt:
    """Test the ME_Radial_pt() function."""

    @pytest.mark.parametrize(
        "mu_f,mu_i,expected", [
            (0, 0, 0.6666666667),
            (0, 1, -1.054092553),
            (0, 2, 1.394433378),
            (1, 0, -0.4216370213),
            (1, 1, 0.6666666667),
            (1, 2, -0.8819171040),
            (2, 0, 0.3187276291),
            (2, 1, -0.5039526306),
            (2, 2, 0.6666666667)
        ]
    )
    def test_ok(self, mu_f, mu_i, expected):
        ME: float = ME_Radial_pt(2.5, mu_f, mu_i)
        assert math.isclose(ME, expected)


class TestME_Radial_D2b:
    """Test the ME_Radial_D2b() function."""

    @pytest.mark.parametrize(
        "mu_f,mu_i,expected",
        [(0, 0, -Rational(7, 6)),
         (0, 1, 7 * sqrt(10) / 30),
         (1, 0, 7 * sqrt(10) / 30),
         (1, 1, -Rational(19, 6))]
    )
    def test_Expr(self, mu_f: Nu, mu_i: Nu, expected: Expr):
        ME: float = ME_Radial_D2b(2.5, mu_f, mu_i)
        assert math.isclose(ME, float(expected))

    @pytest.mark.parametrize(
        "mu_f,mu_i,expected",
        [(0, 0, -1.1666666670),
         (0, 1, 0.7378647874),
         (0, 2, 0.6374552582),
         (1, 0, 0.7378647874),
         (1, 1, -3.1666666670),
         (1, 2, 1.6378460500),
         (2, 0, 0.6374552582),
         (2, 1, 1.6378460500),
         (2, 2, -5.1666666670)
         ]
    )
    def test_ok(self, mu_f: Nu, mu_i: Nu, expected: float):
        ME: float = ME_Radial_D2b(2.5, mu_f, mu_i)
        assert math.isclose(ME, expected)


class TestME_Radial_bDb:
    """Test the ME_Radial_bDb() function."""

    @pytest.mark.parametrize(
        "mu_f,mu_i,expected", [
            (0, 0, -0.5000000000),
            (0, 1, 1.5811388300),
            (0, 2, 0.0000000000),
            (1, 0, -1.5811388300),
            (1, 1, -0.5000000000),
            (1, 2, 2.6457513110),
            (2, 0, 0.0000000000),
            (2, 1, -2.6457513110),
            (2, 2, -0.5000000000)
        ]
    )
    def test_ok(self, mu_f, mu_i, expected):
        ME: float = ME_Radial_bDb(2.5, mu_f, mu_i)
        assert math.isclose(ME, expected)


class TestME_Radial_b_pl:
    """Test the ME_Radial_b_pl() function."""

    @pytest.mark.parametrize(
        "mu_f,mu_i,expected", [
            (0, 0, 1.5811388300),
            (0, 1, 1.0000000000),
            (0, 2, 0.0000000000),
            (1, 0, 0.0000000000),
            (1, 1, 1.8708286930),
            (1, 2, 1.4142135620),
            (2, 0, 0.0000000000),
            (2, 1, 0.0000000000),
            (2, 2, 2.1213203440)
        ]
    )
    def test_ok(self, mu_f, mu_i, expected):
        ME: float = ME_Radial_b_pl(2.5, mu_f, mu_i)
        assert math.isclose(ME, expected)


class TestME_Radial_bm_pl:
    """Test the ME_Radial_bm_pl() function."""

    @pytest.mark.parametrize(
        "mu_f,mu_i,expected", [
            (0, 0, 0.6324555320),
            (0, 1, 0.0000000000),
            (0, 2, 0.0000000000),
            (1, 0, -0.3380617018),
            (1, 1, 0.5345224837),
            (1, 2, 0.0000000000),
            (2, 0, 0.2253744679),
            (2, 1, -0.3563483226),
            (2, 2, 0.4714045209)
        ]
    )
    def test_ok(self, mu_f, mu_i, expected):
        ME: float = ME_Radial_bm_pl(2.5, mu_f, mu_i)
        assert math.isclose(ME, expected)


class TestME_Radial_Db_pl:
    """Test the ME_Radial_Db_pl() function."""

    @pytest.mark.parametrize(
        "mu_f,mu_i,expected", [
            (0, 0, -0.3162277660),
            (0, 1, 1.0000000000),
            (0, 2, 0.0000000000),
            (1, 0, -0.6761234036),
            (1, 1, -0.8017837260),
            (1, 2, 1.4142135620),
            (2, 0, 0.4507489358),
            (2, 1, -0.7126966452),
            (2, 2, -1.1785113020)
        ]
    )
    def test_ok(self, mu_f, mu_i, expected):
        ME: float = ME_Radial_Db_pl(2.5, mu_f, mu_i)
        assert math.isclose(ME, expected)


class TestME_Radial_b_ml:
    """Test the ME_Radial_b_ml() function."""

    @pytest.mark.parametrize(
        "mu_f,mu_i,expected", [
            (0, 0, 1.2247448710),
            (0, 1, 0.0000000000),
            (0, 2, 0.0000000000),
            (1, 0, 1.0000000000),
            (1, 1, 1.5811388300),
            (1, 2, 0.0000000000),
            (2, 0, 0.0000000000),
            (2, 1, 1.4142135620),
            (2, 2, 1.8708286930)
        ]
    )
    def test_ok(self, mu_f, mu_i, expected):
        ME: float = ME_Radial_b_ml(2.5, mu_f, mu_i)
        assert math.isclose(ME, expected)


class TestME_Radial_bm_ml:
    """Test the ME_Radial_bm_ml() function."""

    @pytest.mark.parametrize(
        "mu_f,mu_i,expected", [
            (0, 0, 0.8164965810),
            (0, 1, -0.5163977795),
            (0, 2, 0.3903600291),
            (1, 0, 0.0000000000),
            (1, 1, 0.6324555320),
            (1, 2, -0.4780914437),
            (2, 0, 0.0000000000),
            (2, 1, 0.0000000000),
            (2, 2, 0.5345224837)
        ]
    )
    def test_ok(self, mu_f, mu_i, expected):
        ME: float = ME_Radial_bm_ml(2.5, mu_f, mu_i)
        assert math.isclose(ME, expected)


class TestME_Radial_Db_ml:
    """Test the ME_Radial_Db_ml() function."""

    @pytest.mark.parametrize(
        "mu_f,mu_i,expected", [
            (0, 0, 0.4082482900),
            (0, 1, 0.5163977795),
            (0, 2, -0.3903600291),
            (1, 0, -1.0000000000),
            (1, 1, 0.9486832980),
            (1, 2, 0.4780914437),
            (2, 0, 0.0000000000),
            (2, 1, -1.4142135620),
            (2, 2, 1.3363062090)
        ]
    )
    def test_ok(self, mu_f, mu_i, expected):
        ME: float = ME_Radial_Db_ml(2.5, mu_f, mu_i)
        assert math.isclose(ME, expected, abs_tol=1e-09)


class TestME_Radial_id_pl:
    """Test the ME_Radial_id_pl() function."""

    @pytest.mark.parametrize(
        "mu_f,mu_i,r,expected", [
            (0, 0, 0, 1.0000000000),
            (0, 0, 1, 0.8451542545),
            (0, 0, 2, 0.5945883899),
            (0, 1, 0, 0.0000000000),
            (0, 1, 1, 0.5345224837),
            (0, 1, 2, 0.7521014333),
            (0, 2, 0, 0.0000000000),
            (0, 2, 1, 0.0000000000),
            (0, 2, 2, 0.2842676218),
            (1, 0, 0, 0.0000000000),
            (1, 0, 1, -0.3984095365),
            (1, 0, 2, -0.4664335081),
            (1, 1, 0, 1.0000000000),
            (1, 1, 1, 0.6299407882),
            (1, 1, 2, 0.0737496131),
            (1, 2, 0, 0.0000000000),
            (1, 2, 1, 0.6666666670),
            (1, 2, 2, 0.7804925428),
            (2, 0, 0, 0.0000000000),
            (2, 0, 1, 0.2402499900),
            (2, 0, 2, 0.3612978419),
            (2, 1, 0, 0.0000000000),
            (2, 1, 1, -0.3798685882),
            (2, 1, 2, -0.2285048188),
            (2, 2, 0, 1.0000000000),
            (2, 2, 1, 0.5025189078),
            (2, 2, 2, -0.1511417310)
        ]
    )
    def test_ok(self, mu_f, mu_i, r, expected):
        ME: float = ME_Radial_id_pl(2.5, mu_f, mu_i, r)
        assert math.isclose(ME, expected)


class TestME_Radial_id_ml:
    """Test the ME_Radial_id_ml() function."""

    @pytest.mark.parametrize(
        "mu_f,mu_i,r,expected", [
            (0, 0, 0, 1.0000000000),
            (0, 0, 1, 0.8819171036),
            (0, 0, 2, 0.4879500364),
            (0, 1, 0, 0.0000000000),
            (0, 1, 1, -0.3760507166),
            (0, 1, 2, -0.4161251894),
            (0, 2, 0, 0.0000000000),
            (0, 2, 1, 0.2085954062),
            (0, 2, 2, 0.3462370863),
            (1, 0, 0, 0.0000000000),
            (1, 0, 1, 0.4714045209),
            (1, 0, 2, 0.7968190730),
            (1, 1, 0, 1.0000000000),
            (1, 1, 1, 0.7035264708),
            (1, 1, 2, -0.0849411986),
            (1, 2, 0, 0.0000000000),
            (1, 2, 1, -0.3902462714),
            (1, 2, 2, -0.0942337990),
            (2, 0, 0, 0.0000000000),
            (2, 0, 1, 0.0000000000),
            (2, 0, 2, 0.3563483226),
            (2, 1, 0, 0.0000000000),
            (2, 1, 1, 0.6030226892),
            (2, 1, 2, 0.7597371764),
            (2, 2, 0, 1.0000000000),
            (2, 2, 1, 0.5853694070),
            (2, 2, 2, -0.2633914755)
        ]
    )
    def test_ok(self, mu_f, mu_i, r, expected):
        ME: float = ME_Radial_id_ml(2.5, mu_f, mu_i, r)
        assert math.isclose(ME, expected)
