import cProfile
from pstats import Stats, SortKey
from acmpy.performance.run_example import Example_2_2_c


def profile(example):
    # run without profiling
    print('Profiling: off')
    example.run()

    # run with profiling
    print('Profiling: on')
    with cProfile.Profile() as pr:
        example.run()

    filename: str = f'{example.__name__}_stats'
    pr.dump_stats(filename)

    p: Stats = Stats(filename)
    p.sort_stats(SortKey.TIME).print_stats(30)


if __name__ == '__main__':
    # ACM_Scale performance measured on v1-1-1

    # (nu_max, v_max, L_max) times are in seconds, with and without cProfile

    # bottleneck is sympy
    # (5, 3, 3) 5, 11
    # (5, 3, 6) 8, 15

    # bottleneck is mpmath
    # (5, 6, 6) 26, 56
    # (5, 9, 6) 76, 163
    # (5, 12, 6) 186, 410
    # (5, 15, 6) 394, 823
    # (5, 18, 6) 702, 1600

    Example_2_2_c.run()

