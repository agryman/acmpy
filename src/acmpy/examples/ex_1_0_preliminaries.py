""" Maple Examples: 1. Preliminaries """

from acmpy.acm1_4 import *


def main():
    # 1.1 Essentials
    ACM_set_defaults(0)
    print(ACM_version)
    show_CG_file(2, 3, 1, 0, 5)

    # 1.2 Setting the default output format
    ACM_set_output(2, 8, 5)
    ACM_set_datum(1)
    ACM_set_listln(6, 4)
    ACM_set_eig_fit(6.0, 2, 1)
    ACM_set_rat_fit(100.0, 2, 0, 1, 1)


if __name__ == '__main__':
    main()
