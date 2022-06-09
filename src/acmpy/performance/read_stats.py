from pstats import Stats, SortKey


def read() -> Stats:
    return Stats('Example_4_5_d_050508_stats')


if __name__ == '__main__':
    p: Stats = read()
    p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(30)
