from acmpy.acm1_4 import ACM_Hamiltonian, OperatorSum, DigXspace, EigenBases, EigenValues, XParams, LValues
from sympy import S, Rational
from math import isclose


def main() -> None:
    keywords: list[str] = [f'c{i}' for i in [11, 20, 21, 22, 23, 30, 31, 32, 33, 40, 41, 42, 43, 50]]
    for keyword in keywords:
        if keyword != 'c11':
            continue
        ham_op: OperatorSum = ACM_Hamiltonian(**{keyword: 1})
        eigen_spaces: tuple[EigenValues, EigenBases, XParams, LValues] = \
            DigXspace(ham_op, S.One, Rational(5, 2), 0, 1, 0, 1, 0, 1)
        print(f'{keyword}: {eigen_spaces[0]}')


if __name__ == '__main__':
    main()
