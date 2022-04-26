from sympy import Matrix
from acmpy.eigenvalues import Eigenfiddle


def main() -> None:
    M: Matrix = Matrix([[-2.50000000000000, 1.58113883000000],
                        [1.58113883000000, -4.50000000000000]])
    result: tuple[list[float], Matrix] = Eigenfiddle(M)
    print(f'eigenvalues: {result[0]}')
    print(f'eigenbasis: {result[1]}')


if __name__ == '__main__':
    main()
