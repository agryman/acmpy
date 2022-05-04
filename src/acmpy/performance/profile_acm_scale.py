import cProfile
from pstats import Stats, SortKey

from time import process_time

from sympy import sqrt, Rational

from acmpy.globals import ACM_set_defaults, ACM_set_output, ACM_set_datum, ACM_set_listln, \
    ACM_set_eig_fit, ACM_set_rat_fit
from acmpy.internal_operators import OperatorSum
from acmpy.full_space import ACM_Scale
from acmpy.examples.ex_2_1_specification_of_hamiltonian import make_RWC_ham_fig5a, B
from acmpy.compat import nonnegint


def run_ACM_Scale(nu_max: nonnegint = 5, v_max: nonnegint = 18, L_max: nonnegint = 6) -> None:
    ACM_set_defaults(0)
    ACM_set_output(2, 8, 5)
    ACM_set_datum(1)
    ACM_set_listln(6, 4)
    ACM_set_eig_fit(6.0, 2, 1)
    ACM_set_rat_fit(100.0, 2, 0, 1, 1)

    RWC_ham_fig5a: OperatorSum = make_RWC_ham_fig5a()

    print(f'nu_max: {nu_max}, v_max: {v_max}, L_max: {L_max}')

    start: float = process_time()
    ACM_Scale(RWC_ham_fig5a, sqrt(B), Rational(5, 2), 0, nu_max, 0, v_max, 0, L_max)
    finish: float = process_time()

    elapsed: float = finish - start
    print(f'elapsed process time for ACM_Scale: {elapsed}')


if __name__ == '__main__':
    # (nu_max, v_max, L_max) times are in seconds, with and without cProfile

    # measured on v1-1-1

    # bottleneck is sympy
    # (5, 3, 3) 5, 11
    # (5, 3, 6) 8, 15

    # bottleneck is mpmath
    # (5, 6, 6) 26, 56
    # (5, 9, 6) 76, 163
    # (5, 12, 6) 186, 410
    # (5, 15, 6) 394, 823
    # (5, 18, 6) 702, 1600

    nu_max: nonnegint = 5
    v_max: nonnegint = 18
    L_max: nonnegint = 6

    # run without profiling
    run_ACM_Scale(nu_max, v_max, L_max)

    # run with profiling
    # command: str = f'run_ACM_Scale({nu_max}, {v_max}, {L_max})'
    # cProfile.run(command, filename)

    with cProfile.Profile() as pr:
        run_ACM_Scale(nu_max, v_max, L_max)

    filename: str = f'acm_scale_{nu_max}_{v_max}_{L_max}_stats'
    pr.dump_stats(filename)

    p: Stats = Stats(filename)
    p.sort_stats(SortKey.TIME).print_stats(30)
