"""Tests the internal_operators.py module."""

import numpy as np
from acmpy.internal_operators import RepSO5r3_Prod_rem, SpHarm_310
from acmpy.compat import Matrix_to_ndarray


class TestRepSO5r3_Prod_rem:
    """Tests the RepSO5r3_Prod_rem() function."""

    def test_example_4_5(self, allclose):
        rep = RepSO5r3_Prod_rem((SpHarm_310,), 0, 5, 0, 0)
        expected = np.array([[0.,1.732050807],
                             [1.732050808,0.]])
        assert allclose(rep, expected)
