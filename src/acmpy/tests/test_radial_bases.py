"""Tests the module radial_bases.py."""

import pytest
from acmpy.radial_bases import Nu, RadialBasis, TruncatedRadialSpace


class TestRadialBasis:
    """Tests the class RadialBasis."""

    def test_ok(self):
        lambdaa: float = 2.5
        basis: RadialBasis = RadialBasis(lambdaa)
        assert lambdaa == basis.lambdaa

    def test_bad_lambdaa(self):
        lambdaa: float = 0.0
        with pytest.raises(ValueError):
            RadialBasis(lambdaa)


class TestTruncatedRadialSpace:
    """Tests the class TruncatedRadialSpace."""

    def test_ok(self):
        nu_min: Nu = 0
        nu_max: Nu = 10
        space: TruncatedRadialSpace = TruncatedRadialSpace(nu_min, nu_max)
        assert space.nu_min == nu_min
        assert space.nu_max == nu_max

    def test_trivial(self):
        nu_min: Nu = 10
        nu_max: Nu = 0
        space: TruncatedRadialSpace = TruncatedRadialSpace(nu_min, nu_max)
        assert space.dim() == 0

    def test_dim(self):
        space: TruncatedRadialSpace = TruncatedRadialSpace(0, 10)
        assert space.dim() == 11

    def test_labels(self):
        space: TruncatedRadialSpace = TruncatedRadialSpace(0, 3)
        assert space.labels() == [0, 1, 2, 3]
