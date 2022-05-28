"""This module is a small testcase that is used for debugging ACM_Scale()."""

from time import process_time

from sympy import S, Rational

from acmpy.acm1_4 import ACM_set_defaults, ACM_Hamiltonian, ACM_Scale, nonnegint


def main() -> None:
    ACM_set_defaults(0)
    ham11 = ACM_Hamiltonian(c11=1)
    ham20 = ACM_Hamiltonian(c20=1)
    ham21 = ACM_Hamiltonian(c21=1)
    ham22 = ACM_Hamiltonian(c22=1)
    ham23 = ACM_Hamiltonian(c23=1)
    ham30 = ACM_Hamiltonian(c30=1)
    ham31 = ACM_Hamiltonian(c31=1)
    ham32 = ACM_Hamiltonian(c32=1)
    ham33 = ACM_Hamiltonian(c33=1)
    ham40 = ACM_Hamiltonian(c40=1)
    ham41 = ACM_Hamiltonian(c41=1)
    ham42 = ACM_Hamiltonian(c42=1)
    ham43 = ACM_Hamiltonian(c43=1)
    ham50 = ACM_Hamiltonian(c50=1)
    ham_list = [ham11,
                ham20, ham21, ham22, ham23,
                ham30, ham31, ham32, ham33,
                ham40, ham41, ham42, ham43,
                ham50]

    anorm: float = 1.0
    lambda_base: float = 2.5
    nu_min: nonnegint = 0
    nu_max: nonnegint = 1
    v_min: nonnegint = 0
    v_max: nonnegint = 1
    L_min: nonnegint = 0
    L_max: nonnegint = 1

    for ham in ham_list:

        print(f'Hamiltonian: {ham}')

        start: float = process_time()
        ACM_Scale(ham, anorm, lambda_base, nu_min, nu_max, v_min, v_max, L_min, L_max)
        finish: float = process_time()

        elapsed: float = finish - start
        print(f'elapsed time: {elapsed}')


if __name__ == '__main__':
    main()
