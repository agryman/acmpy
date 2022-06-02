import cProfile
from pstats import Stats, SortKey
from acmpy.examples.section_2 import Example_2_2_a
from acmpy.examples.section_4 import Example_4_5_d_050508


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
    profile(Example_2_2_a)
