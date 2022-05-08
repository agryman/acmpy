
import numpy as np
from acmpy.eigenvalues import Eigenfiddle


def main() -> None:
    M: np.ndarray = np.array([[-2.50000000000000, 1.58113883000000],
                              [1.58113883000000, -4.50000000000000]])
    result: tuple[np.ndarray, np.ndarray] = Eigenfiddle(M)
    print(f'eigenvalues: {result[0]}')
    print(f'eigenbasis: {result[1]}')


if __name__ == '__main__':
    main()
