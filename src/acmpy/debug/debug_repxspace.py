from acmpy.compat import NDArrayFloat
from acmpy.internal_operators import OperatorSum, ACM_Hamiltonian
from acmpy.full_operators import RepXspace


def main():
    ham11: OperatorSum = ACM_Hamiltonian(c11=1)
    L_matrix: NDArrayFloat = RepXspace(ham11, 1.0, 2.5, 0, 1, 0, 1, 0)
    print(L_matrix)


if __name__ == '__main__':
    main()
