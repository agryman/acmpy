import cProfile
from pstats import Stats, SortKey
from acmpy.compat import nonnegint
from acmpy.performance.run_acm_scale import run_ACM_Scale, set_default_output_format_2_3_a

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

    set_default_output_format_2_3_a()

    nu_max: nonnegint = 10
    v_max: nonnegint = 6
    L_max: nonnegint = 6

    # run without profiling
    run_ACM_Scale(nu_max, v_max, L_max)

    # run with profiling
    with cProfile.Profile() as pr:
        run_ACM_Scale(nu_max, v_max, L_max)

    filename: str = f'acm_scale_{nu_max}_{v_max}_{L_max}_stats'
    pr.dump_stats(filename)

    p: Stats = Stats(filename)
    p.sort_stats(SortKey.TIME).print_stats(30)
