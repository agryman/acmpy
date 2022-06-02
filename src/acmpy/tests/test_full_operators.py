"""Tests the full_operators.py module."""
import os.path

import pytest
import math
import numpy as np
from pathlib import Path
from sympy import shape
from acmpy.compat import NDArrayFloat, list_to_ndarray, is_nd_zeros
from acmpy.internal_operators import OperatorSum, ACM_Hamiltonian
from acmpy.full_operators import RepXspace, RepXspace_Prod
from acmpy.radial_space import Radial_b, Radial_b2, Radial_bm2, Radial_D2b
from acmpy.spherical_space import SpHarm_310
from acmpy.globals import ACM_set_basis_type, ACM_set_rat_lst, ACM_show_lambda_fun, ACM_eval_lambda_fun
from acmpy.examples.section_4 import Example_4_1_ham, Example_4_5_c


def read_csv(filename: str) -> NDArrayFloat:
    """Read a generated test data CSV file into a NumPy matrix.

    Assume the following directory layout:
    acmpy/ - the repository root
    - generated/ - the directory containing generated files
    -- CSV files containing test data
    - src/ - the directory containing source files
    -- acmpy/ - the package directory
    --- tests/ - the directory containing test files
    ---- Python modules containing test cases
    """

    tests_dir = Path(__file__).parent
    while tests_dir.name != 'tests':
        tests_dir = tests_dir.parent
    assert tests_dir.name == 'tests'

    package_dir = tests_dir.parent
    assert package_dir.name == 'acmpy'

    src_dir = package_dir.parent
    assert src_dir.name == 'src'

    root_dir = src_dir.parent
    assert root_dir.name == 'acmpy'

    data_path = os.path.join(root_dir, 'generated', filename)
    matrix = np.loadtxt(data_path, delimiter=',')

    return matrix


@pytest.fixture
def example_4_5():
    return list_to_ndarray([
        [-1.991666667, -2.940918224, 0.083666003, 0.000000000, 0.000000000, 0.000000000, -0.170782513, 0.072821908,
         -0.040394327, 0.025547615, -0.017525520, 0.012714348],
        [-2.940918224, -3.571666666, -4.709437334, 0.194422221, 0.000000000, 0.000000000, -0.216024690,
         -0.115141547,
         0.063869038, -0.040394327, 0.027710279, -0.020103150],
        [0.083666003, -4.709437334, -4.911666666, -6.246198844, 0.344673759, 0.000000000, -0.081649658,
         -0.278524249,
         -0.084490796, 0.053436671, -0.036657254, 0.026593967],
        [0.000000000, 0.194422221, -6.246198844, -6.011666667, -7.598473531, 0.534789679, 0.000000000, -0.127920430,
         -0.319308694, -0.065446289, 0.044895784, -0.032570825],
        [0.000000000, 0.000000000, 0.344673759, -7.598473531, -6.871666667, -8.779350773, 0.000000000, 0.000000000,
         -0.166410059, -0.350823208, -0.052644973, 0.038192678],
        [0.000000000, 0.000000000, 0.000000000, 0.534789679, -8.779350773, -8.391666665, 0.000000000, 0.000000000,
         0.000000000, -0.200000000, -0.377296887, -0.043546353],
        [-0.170782513, -0.216024690, -0.081649658, 0.000000000, 0.000000000, 0.000000000, -4.451666667,
         -4.080661711,
         0.169115345, 0.000000000, 0.000000000, -0.000000000],
        [0.072821908, -0.115141547, -0.278524250, -0.127920430, 0.000000000, 0.000000000, -4.080661711,
         -5.671666667,
         -5.985215117, 0.342052627, 0.000000000, 0.000000000],
        [-0.040394327, 0.063869038, -0.084490796, -0.319308694, -0.166410059, 0.000000000, 0.169115345,
         -5.985215117,
         -6.651666667, -7.494598054, 0.553172667, -0.000000000],
        [0.025547615, -0.040394327, 0.053436671, -0.065446289, -0.350823208, -0.200000000, 0.000000000, 0.342052627,
         -7.494598054, -7.391666667, -8.746427842, 0.803741252],
        [-0.017525520, 0.027710280, -0.036657254, 0.044895784, -0.052644973, -0.377296887, 0.000000000, 0.000000000,
         0.553172667, -8.746427842, -7.891666667, -9.786674613],
        [0.012714348, -0.020103150, 0.026593967, -0.032570825, 0.038192678, -0.043546353, -0.000000000, 0.000000000,
         -0.000000000, 0.803741252, -9.786674613, -9.411666665]])


class TestReadCSV:
    """Tests the read_csv() function."""

    def test_read_csv(self, example_4_5, allclose):
        L_matrix = read_csv('example-4-5/05050/1/repxspace/rwc-ham.csv')
        assert allclose(L_matrix, example_4_5, atol=1e-8)


class TestRepXspace:
    """Tests the RepXspace() function."""

    def test_ham11_01010(self, allclose):
        ham11: OperatorSum = ACM_Hamiltonian(c11=1)
        L_matrix: NDArrayFloat = RepXspace(ham11, 1.0, 2.5, 0, 1, 0, 1, 0)
        assert shape(L_matrix) == (2, 2)
        L_matrix_expected: NDArrayFloat = \
            list_to_ndarray([[-2.5, 1.58113883],
                             [1.58113883, -4.5]])
        assert allclose(L_matrix, L_matrix_expected, atol=1e-8)

    @pytest.mark.parametrize(
        "basis_type", [basis_type for basis_type in range(4)]
    )
    def test_example_4_5_basis_type(self, basis_type, allclose):
        ACM_set_basis_type(basis_type, 0.0, 0)

        ham = Example_4_1_ham.ham
        B = Example_4_1_ham.B
        anorm = math.sqrt(B)
        lambda_base = 2.5
        L_matrix = RepXspace(ham, anorm, lambda_base, 0, 5, 0, 5, 0)

        path = f'example-4-5/05050/{basis_type}/repxspace/rwc-ham.csv'
        L_matrix_expected = read_csv(path)

        assert allclose(L_matrix, L_matrix_expected)


RepXspace_Prod_cases = \
    [((Radial_D2b,), 'radial-d2b'),
     ((Radial_b,), 'radial-b'),
     ((Radial_b2,), 'radial-b2'),
     ((Radial_bm2,), 'radial-bm2'),
     ((SpHarm_310,), 'spharm-310')]


class TestRepXspace_Prod:
    """Tests the RepXspace_Prod() function."""

    @pytest.mark.parametrize(
        "basis_type,prod,filename",
        [(basis_type, prod, filename)
         for basis_type in range(4)
         for (prod, filename) in RepXspace_Prod_cases]
    )
    def test_example_4_5(self, basis_type, prod, filename, allclose):
        ACM_set_basis_type(basis_type, 0.0, 0)
        # ACM_set_rat_lst(Example_4_5_c.rat_lst)
        B = Example_4_1_ham.B
        anorm = math.sqrt(B)
        lambda_base = 2.5
        rep = RepXspace_Prod(prod, anorm, lambda_base, 0, 5, 0, 5, 0, 0)
        path = f'example-4-5/05050/{basis_type}/repxspace-prod/{filename}.csv'
        expected = read_csv(path)
        assert allclose(rep, expected, atol=1e-8)


class Test_glb_lam_fun:
    """Tests the glb_lam_fun variable."""

    @pytest.mark.parametrize(
        "basis_type,v",
        [(basis_type, v) for basis_type in range(4) for v in range(10)]
    )
    def test_ok(self, basis_type, v):
        ACM_set_basis_type(basis_type, 0.0, 0)
        lambda_disp = ACM_eval_lambda_fun(v)
        expected = ACM_show_lambda_fun(v, v)
        assert lambda_disp == expected[0]

