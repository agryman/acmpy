"""This module tests the radial_space.py module."""

from acmpy.radial_space import Radial_Operators, Radial_Sm
from acmpy.radial_space import Parse_RadialOp_List, Radial_D2b, KTSOps, KTSOp, KTOp


class TestRadial:
    """Tests the Radial operator symbols."""

    def test_ok(self):
        assert Radial_Sm in Radial_Operators


class TestParse_RadialOp_List:
    """Tests the Parse_RadialOp_List() function."""

    def test_Radial_D2b(self):
        parsed_ops: KTSOps = Parse_RadialOp_List([Radial_D2b])
        assert len(parsed_ops) == 1

        kts_op: KTSOp = parsed_ops[0]
        assert isinstance(kts_op, KTSOp)
        assert isinstance(kts_op, KTOp)

        kt_op: KTOp = kts_op
        print(f'K={kt_op.K}, T={kt_op.T}')
        assert kt_op.K == 0
        assert kt_op.T == 2
