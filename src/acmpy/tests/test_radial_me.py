"""Test radial matrix element functions."""
import math
import pytest
from sympy import sqrt, Rational, Expr, S, simplify
from acmpy.radial_space import Nu, ME_Radial_S0, ME_Radial_Sp, ME_Radial_Sm, \
    ME_Radial_b2, ME_Radial_bm2, ME_Radial_pt, ME_Radial_D2b, ME_Radial_bDb, \
    ME_Radial_b_pl, ME_Radial_bm_pl, ME_Radial_Db_pl, ME_Radial_b_ml, ME_Radial_bm_ml, \
    ME_Radial_Db_ml, ME_Radial_id_pl, ME_Radial_id_ml, MF_Radial_id_poly, MF_Radial_id_pl, lamvar


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
            (0, 0, 1, 0.9198662110),
            (0, 0, 2, 0.7488553354),
            (0, 1, 0, 0.0000000000),
            (0, 1, 1, 0.3922322702),
            (0, 1, 2, 0.6386259759),
            (0, 2, 0, 0.0000000000),
            (0, 2, 1, 0.0000000000),
            (0, 2, 2, 0.1771229771),
            (1, 0, 0, 0.0000000000),
            (1, 0, 1, -0.3358876491),
            (1, 0, 2, -0.4859215070),
            (1, 1, 0, 1.0000000000),
            (1, 1, 1, 0.7877263614),
            (1, 1, 2, 0.3625958468),
            (1, 2, 0, 0.0000000000),
            (1, 2, 1, 0.5163977796),
            (1, 2, 2, 0.7470616676),
            (2, 0, 0, 0.0000000000),
            (2, 0, 1, 0.1629294418),
            (2, 0, 2, 0.3181102984),
            (2, 1, 0, 0.0000000000),
            (2, 1, 1, -0.3821034109),
            (2, 1, 2, -0.4069280609),
            (2, 2, 0, 1.0000000000),
            (2, 2, 1, 0.6888467201),
            (2, 2, 2, 0.1222666658)
        ]
    )
    def test_ok(self, mu_f, mu_i, r, expected):
        ME: float = ME_Radial_id_pl(5.5, mu_f, mu_i, r)
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
        ME: float = ME_Radial_id_ml(5.5, mu_f, mu_i, r)
        assert math.isclose(ME, expected)


class TestMF_Radial_id_poly:
    """Test the MF_Radial_id_poly() function."""

    @pytest.mark.parametrize(
        "mu,nu,r,expected", [
            (0, 0, 0, 1),
            (1, 0, 0, 0),
            (1, 1, 0, 1),
            (2, 0, 0, 0),
            (2, 1, 0, 0),
            (2, 2, 0, 1),
            (3, 0, 0, 0),
            (3, 1, 0, 0),
            (3, 2, 0, 0),
            (3, 3, 0, 1),
            (4, 0, 0, 0),
            (4, 1, 0, 0),
            (4, 2, 0, 0),
            (4, 3, 0, 0),
            (4, 4, 0, 1),
            (0, 0, 1, lamvar),
            (0, 1, 1, 1),
            (1, 0, 1, -lamvar),
            (1, 1, 1, lamvar),
            (1, 2, 1, 2),
            (2, 0, 1, lamvar),
            (2, 1, 1, -lamvar),
            (2, 2, 1, lamvar),
            (2, 3, 1, 3),
            (3, 0, 1, -lamvar),
            (3, 1, 1, lamvar),
            (3, 2, 1, -lamvar),
            (3, 3, 1, lamvar),
            (3, 4, 1, 4),
            (4, 0, 1, lamvar),
            (4, 1, 1, -lamvar),
            (4, 2, 1, lamvar),
            (4, 3, 1, -lamvar),
            (4, 4, 1, lamvar),
            (4, 5, 1, 5),
            (0, 0, 2, lamvar**2+lamvar),
            (0, 1, 2, 2+2*lamvar),
            (0, 2, 2, 2),
            (1, 0, 2, -2*lamvar**2-2*lamvar),
            (1, 1, 2, lamvar**2-lamvar-2),
            (1, 2, 2, 4+4*lamvar),
            (1, 3, 2, 6),
            (2, 0, 2, 3*lamvar**2+3*lamvar),
            (2, 1, 2, -2*lamvar**2+2),
            (2, 2, 2, lamvar**2-3*lamvar-4),
            (2, 3, 2, 6+6*lamvar),
            (2, 4, 2, 12),
            (3, 0, 2, -4*lamvar**2-4*lamvar),
            (3, 1, 2, 3*lamvar**2+lamvar-2),
            (3, 2, 2, -2*lamvar**2+2*lamvar+4),
            (3, 3, 2, lamvar**2-5*lamvar-6),
            (3, 4, 2, 8+8*lamvar),
            (3, 5, 2, 20),
            (4, 0, 2, 5*lamvar**2+5*lamvar),
            (4, 1, 2, -4*lamvar**2-2*lamvar+2),
            (4, 2, 2, 3*lamvar**2-lamvar-4),
            (4, 3, 2, -2*lamvar**2+4*lamvar+6),
            (4, 4, 2, lamvar**2-7*lamvar-8),
            (4, 5, 2, 10+10*lamvar),
            (4, 6, 2, 30)
        ]
    )
    def test_ok(self, mu, nu, r, expected):
        poly: Expr = MF_Radial_id_poly(mu, nu, r)
        assert simplify(poly - expected) == 0


class TestMF_Radial_id_pl:
    """Test the MF_Radial_id_pl() function."""

    @pytest.mark.parametrize(
        "mu,nu,r,expected", [
            (0, 0, 0, 1.000000000),
            (1, 0, 0, -0.),
            (1, 1, 0, 1.000000000),
            (2, 0, 0, 0.),
            (2, 1, 0, -0.),
            (2, 2, 0, 1.000000000),
            (3, 0, 0, -0.),
            (3, 1, 0, 0.),
            (3, 2, 0, -0.),
            (3, 3, 0, 1.000000000),
            (4, 0, 0, 0.),
            (4, 1, 0, -0.),
            (4, 2, 0, 0.),
            (4, 3, 0, -0.),
            (4, 4, 0, 1.000000000),
            (0, 0, 1, 5.500000001),
            (0, 1, 1, 1.000000000),
            (1, 0, 1, -5.499999997),
            (1, 1, 1, 5.499999997),
            (1, 2, 1, 2.000000000),
            (2, 0, 1, 5.500000000),
            (2, 1, 1, -5.500000000),
            (2, 2, 1, 5.500000000),
            (2, 3, 1, 3.000000000),
            (3, 0, 1, -5.500000000),
            (3, 1, 1, 5.500000000),
            (3, 2, 1, -5.500000000),
            (3, 3, 1, 5.500000000),
            (3, 4, 1, 4.000000000),
            (4, 0, 1, 5.500000000),
            (4, 1, 1, -5.500000000),
            (4, 2, 1, 5.500000000),
            (4, 3, 1, -5.500000000),
            (4, 4, 1, 5.500000000),
            (4, 5, 1, 5.000000000),
            (0, 0, 2, 35.74999999),
            (0, 1, 2, 13.00000000),
            (0, 2, 2, 2.000000000),
            (1, 0, 2, -71.50000000),
            (1, 1, 2, 22.75000002),
            (1, 2, 2, 26.00000000),
            (1, 3, 2, 6.000000000),
            (2, 0, 2, 107.2500000),
            (2, 1, 2, -58.49999990),
            (2, 2, 2, 9.74999995),
            (2, 3, 2, 38.99999995),
            (2, 4, 2, 12.00000000),
            (3, 0, 2, -142.9999999),
            (3, 1, 2, 94.2500000),
            (3, 2, 2, -45.49999980),
            (3, 3, 2, -3.25000020),
            (3, 4, 2, 52.00000003),
            (3, 5, 2, 20.00000000),
            (4, 0, 2, 178.7500000),
            (4, 1, 2, -130.0000004),
            (4, 2, 2, 81.2500004),
            (4, 3, 2, -32.5000001),
            (4, 4, 2, -16.24999990),
            (4, 5, 2, 65.00000000),
            (4, 6, 2, 30.00000000)
        ]
    )
    def test_ok(self, mu, nu, r, expected):
        pl: Expr = MF_Radial_id_pl(S(5.5), mu, nu, r)
        assert math.isclose(float(pl), expected, rel_tol=1e-07)
