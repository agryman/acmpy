from pstats import Stats


def read() -> Stats:
    return Stats('acm_scale_5_18_6_stats')


if __name__ == '__main__':
    p: Stats = read()
