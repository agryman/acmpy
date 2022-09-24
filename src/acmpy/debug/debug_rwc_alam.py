"""This module debugs the RWC_alam() function."""

from sympy import S, Symbol, Expr, solveset, sqrt, Set, EmptySet, simplify, nsolve, N


def RWC_alam_simplified(B: float) -> None:

    c1: float = -3.0
    c2: float = 2.0

    # set up the equation
    A: Symbol = Symbol('A', real=True)
    mu: Expr = sqrt(9 + (A * c1 / c2) ** 2)
    E: Expr = (c1 / c2) ** 2 * (-9 * A ** 5 / mu ** 2
                                + A ** 3 * B ** 2 * c1
                                + A ** 2 * B ** 2 * c2 * (mu + 3)) \
              + A ** 3 * (2 * mu + 9) \
              - B ** 2 * mu * (mu + 2) * (A * c1 + c2 * (mu + 4))

    # try to solve the equation three ways

    print(f'{"=" * 10} Solving equation for B = {B} {"=" * 10}')

    solutions_num: float = float(nsolve(E, A, 20))
    print(f'Success: nsolve solution = {solutions_num}')

    solutions: Set = solveset(E, A, domain=S.Reals)
    if solutions == EmptySet:
        print(f'Error: solveset returns EmptySet')
    else:
        A0: float = float(N(solutions.args[0]))
        print(f'Success: first solveset solution = {A0}')

    E_simp: Expr = simplify(E)
    solutions_simp: Set = solveset(E_simp, A, domain=S.Reals)
    if solutions_simp == EmptySet:
        print(f'Error: solveset returns EmptySet after simplification')
    else:
        A0_simp: float = float(N(solutions_simp.args[0]))
        print(f'Success: first solveset solution after simplification = {A0_simp}')


if __name__ == '__main__':
    RWC_alam_simplified(14)
    RWC_alam_simplified(15)