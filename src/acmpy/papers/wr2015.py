"""This module contains the mathematical objects defined in the paper WR2015."""

from sympy import Symbol, Eq, Rational, sqrt, Piecewise

a = Symbol('a', real=True, positive=True)
lambda0 = Symbol('lambda0', real=True, positive=True)
E = Symbol('E', real=True)
B = Symbol('B', real=True, positive=True)
c1 = Symbol('c1', real=True)
c2 = Symbol('c2', real=True, nonnegative=True)
beta0 = Symbol('beta0', real=True, nonnegative=True)
v = Symbol('v', integer=True, nonnegative=True)
lambdav = Symbol('lambda_v', real=True, positive=True)


def lambdav_61(lambda0, v):
    lambdav = lambda0 + v

    return lambdav


Eq_61 = Eq(lambdav, lambdav_61(lambda0, v))


def lambdav_62(lambda0, v):
    lambdav = lambda0 + v % 2

    return lambdav


Eq_62 = Eq(lambdav, lambdav_62(lambda0, v))


def lambdav_63(lambda0, v):
    return lambda0


Eq_63 = Eq(lambdav, lambdav_63(lambda0, v))


def lambda0_B11(a, beta0):
    lambda0 = 1 + sqrt(Rational(9, 4) + (a * beta0) ** 4)

    return lambda0


Eq_B11 = Eq(lambda0, lambda0_B11(a, beta0))


def beta0_B15(c1, c2):
    beta0 = Piecewise((sqrt(-c1 / (2 * c2)), c1 < 0), (0, c1 >= 0))

    return beta0


Eq_B15 = Eq(beta0, beta0_B15(c1, c2))


def E_B16(a, lambda0, B, c1, c2):
    E = a ** 2 / (2 * B) * (1 + 9 / (4 * (lambda0 - 1))) \
        + B / (2 * a ** 2) * c1 * lambda0 \
        + B / (2 * a ** 4) * c2 * lambda0 * (lambda0 + 1)

    return E


Eq_B16 = Eq(E, E_B16(a, lambda0, B, c1, c2))
