from sympy import Expr, Rational
from acmpy.radial_space import MF_Radial_id_pl, MF_Radial_id_poly, lamvar


def run_poly():
    poly: Expr = MF_Radial_id_poly(0, 0, 0)
    print(f'poly = {poly}')


def run_pl():
    pl: Expr = MF_Radial_id_pl(Rational(5, 2), 0, 0, 0)
    print(f'pl = {pl}')


if __name__ == '__main__':
    run_poly()
    run_pl()
