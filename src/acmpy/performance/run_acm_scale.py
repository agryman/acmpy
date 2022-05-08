from time import process_time

from sympy import sqrt, Rational

from acmpy.globals import ACM_set_defaults, ACM_set_output, ACM_set_datum, ACM_set_listln, \
    ACM_set_eig_fit, ACM_set_rat_fit, ACM_set_rat_lst, ACM_set_amp_lst, ACM_add_rat_lst, ACM_add_amp_lst
from acmpy.internal_operators import OperatorSum
from acmpy.full_space import ACM_Scale
from acmpy.examples.ex_2_1_specification_of_hamiltonian import make_RWC_ham_fig5a, B
from acmpy.compat import nonnegint


def set_default_output_format_1_2() -> None:
    ACM_set_defaults(0)
    ACM_set_output(2, 8, 5)
    ACM_set_datum(1)
    ACM_set_listln(6, 4)
    ACM_set_eig_fit(6.0, 2, 1)
    ACM_set_rat_fit(100.0, 2, 0, 1, 1)


def set_default_output_format_2_3_a() -> None:
    set_default_output_format_1_2()
    ACM_set_rat_lst(((2, 0, 1, 1), (4, 2, 1, 1), (6, 4, 1, 1), (8, 6, 1, 1)))
    ACM_set_amp_lst(((2, 2, 1, 1),))


def set_default_output_format_2_3_b() -> None:
    set_default_output_format_2_3_a()
    ACM_add_rat_lst(((2, 2, 1, 1), (4, 4, 1, 1), (6, 6, 1, 1), (8, 8, 1, 1)))
    ACM_add_amp_lst(((2, 2, 2, 2),))


def run_ACM_Scale(nu_max: nonnegint = 5, v_max: nonnegint = 18, L_max: nonnegint = 6) -> None:
    RWC_ham_fig5a: OperatorSum = make_RWC_ham_fig5a()

    print(f'nu_max: {nu_max}, v_max: {v_max}, L_max: {L_max}')

    start: float = process_time()
    ACM_Scale(RWC_ham_fig5a, sqrt(B), Rational(5, 2), 0, nu_max, 0, v_max, 0, L_max)
    finish: float = process_time()

    elapsed: float = finish - start
    print(f'elapsed process time for ACM_Scale: {elapsed}')


if __name__ == '__main__':
    set_default_output_format_2_3_a()
    run_ACM_Scale(10, 6, 6)
