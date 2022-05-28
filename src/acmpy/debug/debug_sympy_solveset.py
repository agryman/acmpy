"""This module illustrates a bug in solveset."""

from sympy import S, sqrt, Rational, Expr, Symbol

a: Symbol = Symbol('a', real=True, positive=True)
lambda0: Symbol = Symbol('lambda0', real=True, positive=True)
beta0: Symbol = Symbol('beta0', real=True, nonnegative=True)
B: Symbol = Symbol('B', real=True, positive=True)
c1: Symbol = Symbol('c1', real=True, negative=True)
c2: Symbol = Symbol('c2', real=True, positive=True)

beta0_c1_c2: Expr = sqrt(-c1 / (2 * c2))

c1_DEFAULT: Expr = S(-3)
c2_DEFAULT: Expr = S(2)
beta0_DEFAULT: Expr = beta0_c1_c2.subs([(c1, c1_DEFAULT), (c2, c2_DEFAULT)])

lambda0_a: Expr = 1 + sqrt(Rational(9, 4) + (a * beta0_DEFAULT) ** 4)

E1_a_lambda0: Expr = a ** 2 / (2 * B) * (1 + 9 / (4 * (lambda0 - 1)))

E2_a_lambda0: Expr = -3 * B / (2 * a ** 2) * lambda0

E3_a_lambda_0: Expr = B / (2 * a ** 4) * lambda0 * (lambda0 + 1)

E_a_lambda0: Expr = E1_a_lambda0 + E2_a_lambda0 + E3_a_lambda_0

E_a: Expr = E_a_lambda0.subs(lambda0, lambda0_a)