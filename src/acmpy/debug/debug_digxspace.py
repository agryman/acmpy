from acmpy.acm1_4 import ACM_Hamiltonian, OperatorSum, DigXspace, EigenBases, EigenValues, XParams, LValues
from sympy import S, Rational
from math import isclose


def main() -> None:
    ham_op: OperatorSum = ACM_Hamiltonian(c50=1)
    eigen_spaces: tuple[EigenValues, EigenBases, XParams, LValues] = \
        DigXspace(ham_op, S.One, Rational(5, 2), 0, 0, 0, 0, 0, 0)
    assert isclose(eigen_spaces[0][0][0], 0)


if __name__ == '__main__':
    main()
