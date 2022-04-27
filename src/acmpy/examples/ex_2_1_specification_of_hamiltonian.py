from sympy import Expr, Rational, S
from acmpy.internal_operators import OperatorSum, ACM_Hamiltonian

B: int = 20


def make_RWC_ham_fig5a() -> OperatorSum:
    c2: Expr = Rational(3, 2)
    c1: Expr = 1 - 2 * c2
    chi: Expr = S(2)
    kappa: Expr = S.Zero

    x1: Expr = -Rational(1, 2) / B
    x3: Expr = B * c1 / 2
    x4: Expr = B * c2 / 2
    x6: Expr = -chi
    x10: Expr = kappa

    return ACM_Hamiltonian(x1, 0, x3, x4, 0, x6, 0, 0, 0, x10)


if __name__ == '__main__':
    RWC_ham_fig5a = make_RWC_ham_fig5a()
    print(f'RWC_ham_fig5a: {RWC_ham_fig5a}')
