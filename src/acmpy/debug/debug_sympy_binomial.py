"""This module demonstrates a sympy bug in the calculation of binomial(-1, -1)."""
import sympy as sp


def main():
    """For all a, b we should have binomial(a + b, a) = binomial(a + b, b).

    This invariant is violated for (a, b) = (-1, 0).
    """
    a = -1
    b = 0

    # The following assertion fails:
    # assert sp.binomial(a + b, a) == sp.binomial(a + b, b)

    y1 = sp.binomial(-1, -1)
    assert y1 == 0
    print(f'sympy binomial(-1, -1) = {y1}')

    y2 = sp.binomial(-1, 0)
    assert y2 == 1
    print(f'sympy binomial(-1, 0) = {y2}')


if __name__ == '__main__':
    main()
