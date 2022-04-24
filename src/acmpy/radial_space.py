"""2. Procedures that pertain only to the radial (beta) space."""

from typing import Callable
from functools import cache
from abc import ABC, abstractmethod

from sympy import Expr, S, sqrt, factorial, gamma, Rational, Matrix, simplify, Symbol, symbols, binomial, \
    diag, eye, zeros

from acmpy.compat import nonnegint, require_nonnegint, require_nonnegint_range, is_even, iquo, is_odd, require_int, irem
from acmpy.eigenvalues import Eigenfiddle

Nu = nonnegint


# # The following is a list containing the symbolic names for ten operators
# # that are the "basic" radial operators.
# # The way that they alter lambda is not fixed, but is determined
# # automatically.
#
# Radial_Operators:=[Radial_Sm, Radial_S0, Radial_Sp,
#                    Radial_b2, Radial_bm2, Radial_D2b, Radial_bDb,
#                    Radial_b, Radial_bm, Radial_Db]:
"""
Implement all Maple symbols as SymPy symbols.
These symbols are operators, so their multiplication should be noncommutative.
"""
Radial_Sm: Symbol = Symbol('Radial_Sm', commutative=False)
Radial_S0: Symbol = Symbol('Radial_S0', commutative=False)
Radial_Sp: Symbol = Symbol('Radial_Sp', commutative=False)
Radial_b2: Symbol = Symbol('Radial_b2', commutative=False)
Radial_bm2: Symbol = Symbol('Radial_bm2', commutative=False)
Radial_D2b: Symbol = Symbol('Radial_D2b', commutative=False)
Radial_bDb: Symbol = Symbol('Radial_bDb', commutative=False)
Radial_b: Symbol = Symbol('Radial_b', commutative=False)
Radial_bm: Symbol = Symbol('Radial_bm', commutative=False)
Radial_Db: Symbol = Symbol('Radial_Db', commutative=False)

"""
Radial_Operators is a Maple list.
A Maple list is an immutable sequence of objects.
It should be implemented in Python as a tuple.
Note that in some cases the results of a function are cached in a dict
so all the arguments must be immutable in which case tuples must be used
instead of list.
"""
Radial_Operators: tuple[Symbol, ...] = (
    Radial_Sm, Radial_S0, Radial_Sp,
    Radial_b2, Radial_bm2, Radial_D2b, Radial_bDb,
    Radial_b, Radial_bm, Radial_Db
)

# # They will eventually be exchanged for operators in which the shift
# # is specific. The first seven keep their names (for zero shift),
# # but each instance of the final three will be exchanged for a
# # symbolic name that indicates a shift by a shift of -1,0 or +1.
# # The following lists will be used to achieve that.
"""
Radial_pl, Radial_ml, and Radial_zl are Maple tables.
A Maple table should be implemented as a Python dictionary.
"""
# Radial_pl:=[Radial_b=Radial_b_pl,Radial_bm=Radial_bm_pl,
#             Radial_Db=Radial_Db_pl]:
Radial_b_pl: Symbol = Symbol('Radial_b_pl', commutative=False)
Radial_bm_pl: Symbol = Symbol('Radial_bm_pl', commutative=False)
Radial_Db_pl: Symbol = Symbol('Radial_Db_pl', commutative=False)
Radial_pl: dict[Symbol, Symbol] = {
    Radial_b: Radial_b_pl,
    Radial_bm: Radial_bm_pl,
    Radial_Db: Radial_Db_pl
}

# Radial_ml:=[Radial_b=Radial_b_ml,Radial_bm=Radial_bm_ml,
#             Radial_Db=Radial_Db_ml]:
Radial_b_ml: Symbol = Symbol('Radial_b_ml', commutative=False)
Radial_bm_ml: Symbol = Symbol('Radial_bm_ml', commutative=False)
Radial_Db_ml: Symbol = Symbol('Radial_Db_ml', commutative=False)
Radial_ml: dict[Symbol, Symbol] = {
    Radial_b: Radial_b_ml,
    Radial_bm: Radial_bm_ml,
    Radial_Db: Radial_Db_ml
}

# Radial_zl:=[Radial_b=Radial_b_zl,Radial_bm=Radial_bm_zl,
#             Radial_Db=Radial_Db_zl]:
Radial_b_zl: Symbol = Symbol('Radial_b_zl', commutative=False)
Radial_bm_zl: Symbol = Symbol('Radial_bm_zl', commutative=False)
Radial_Db_zl: Symbol = Symbol('Radial_Db_zl', commutative=False)
Radial_zl: dict[Symbol, Symbol] = {
    Radial_b: Radial_b_zl,
    Radial_bm: Radial_bm_zl,
    Radial_Db: Radial_Db_zl
}

"""Define a symbol for the radial identity operator."""
Radial_id: Symbol = Symbol('Radial_id', commutative=True)


# ###########################################################################
# ####--------------- Representations on the radial space ---------------####
# ###########################################################################
#
# # The next set of routines deal with representing operators in the
# # radial (beta) space. The bases for the radial Hilbert space are
# # dependent on two parameters (a,lambda). For each such pair,
# # the basis states are labelled by a single index nu=0,1,2,....
#
# # A truncated Hilbert space is indexed by states labelled
# #     nu_min, nu_min+1, nu_min+2, ... nu_max
# # (usually we would use nu_min=0).
# # The following two functions each take arguments nu_min and nu_max;
# # the first returns the dimension of the truncated space,
# # the second returns a list of all the labels.
#
# dimRadial:=(nu_min::nonnegint,nu_max::nonnegint)
#   -> `if`(nu_max>=nu_min,nu_max-nu_min+1,0):
def dimRadial(nu_min: nonnegint, nu_max: nonnegint) -> nonnegint:
    require_nonnegint('nu_min', nu_min)
    require_nonnegint('nu_max', nu_max)

    return nu_max - nu_min + 1 if nu_max >= nu_min else 0


# lbsRadial:=proc(nu_min::nonnegint,nu_max::nonnegint)
#   if nu_min>nu_max then
#     error("Radial range invalid");
#   else
#     [seq(i,i=nu_min..nu_max)];
#   fi:
# end:
def lbsRadial(nu_min: nonnegint, nu_max: nonnegint) -> list[Nu]:
    require_nonnegint_range('nu', nu_min, nu_max)

    return list(range(nu_min, nu_max + 1))


# ###########################################################################
#
# # The functions that follow calculate single matrix elements
# #     F^{(a)}_{lambda',mu_f}{lambda,mu_i}(Op),
# # as defined by (13), for various operators Op between two
# # radial space states labelled by non-negative integers mu_i and mu_f.
# # Note that lambda and lambda' might not be equal, and thus the states
# # belong to different bases (in each of the following procedures,
# # lambda'-lambda is a certain fixed value (mostly 0,+1 or -1);
# # also note that we require both lambda>1 and lambda'>1).
# # These routines return the matrix elements for a=1 (more general
# # values are obtained later by multiplying by a power of a).
# # The type of the return value is float only if that of lambda is.
#
# # The following three give matrix elements of the SU(1,1) operators S0,S+,S-.
# # These use eqns. (16)-(18).
#
# ME_Radial_S0:=proc(lambda::algebraic,mu_f::nonnegint,mu_i::nonnegint)
#   if mu_f=mu_i then
#     lambda/2 + mu_i;
#   else
#     0;
#   fi;
# end:
def ME_Radial_S0(lambdaa: Expr, mu_f: nonnegint, mu_i: nonnegint) -> Expr:
    require_nonnegint('mu_f', mu_f)
    require_nonnegint('mu_i', mu_i)

    return lambdaa / 2 + mu_i if mu_f == mu_i else S.Zero


# ME_Radial_Sp:=proc(lambda::algebraic,mu_f::nonnegint,mu_i::nonnegint)
#   if mu_f=mu_i+1 then
#     sqrt( (lambda + mu_i)*(mu_i+1) );
#   else
#     0;
#   fi;
# end:
def ME_Radial_Sp(lambdaa: Expr, mu_f: nonnegint, mu_i: nonnegint) -> Expr:
    require_nonnegint('mu_f', mu_f)
    require_nonnegint('mu_i', mu_i)

    return sqrt((lambdaa + mu_i) * (mu_i + 1)) if mu_f == mu_i + 1 else S.Zero


# ME_Radial_Sm:=proc(lambda::algebraic,mu_f::nonnegint,mu_i::nonnegint)
#   if mu_f=mu_i-1 then
#     sqrt( (lambda + mu_i - 1)*mu_i );
#   else
#     0;
#   fi;
# end:
def ME_Radial_Sm(lambdaa: Expr, mu_f: nonnegint, mu_i: nonnegint) -> Expr:
    require_nonnegint('mu_f', mu_f)
    require_nonnegint('mu_i', mu_i)

    return sqrt((lambdaa + mu_i - 1) * mu_i) if mu_f == mu_i - 1 else S.Zero


# # The following give matrix elements of beta^2 for lambda'=lambda
# # using (21).
#
# ME_Radial_b2:=proc(lambda::algebraic,mu_f::nonnegint,mu_i::nonnegint)
#   if mu_f=mu_i-1 then
#     sqrt( (lambda + mu_i - 1)*mu_i );
#   elif mu_f=mu_i then
#     lambda + 2*mu_i;
#   elif mu_f=mu_i+1 then
#     sqrt( (lambda + mu_i)*(mu_i+1) );
#   else
#     0;
#   fi;
# end:
def ME_Radial_b2(lambdaa: Expr, mu_f: nonnegint, mu_i: nonnegint) -> Expr:
    require_nonnegint('mu_f', mu_f)
    require_nonnegint('mu_i', mu_i)

    if mu_f == mu_i - 1:
        return sqrt((lambdaa + mu_i - 1) * mu_i)
    if mu_f == mu_i:
        return lambdaa + 2 * mu_i
    if mu_f == mu_i + 1:
        return sqrt((lambdaa + mu_i) * (mu_i + 1))

    return S.Zero


# # The following gives matrix elements of 1/beta^2 for lambda'=lambda
# # using (22). It uses the subsequent procedure for which mu_f >= mu_i.
# # (restriction to lambda>1).
#
# ME_Radial_bm2:=proc(lambda::algebraic,mu_f::nonnegint,mu_i::nonnegint)
#   if lambda=-1 then
#     error "Singular 1/beta^2 for lambda=1";
#   fi:
#   if frac(lambda)=0 and (lambda <= -mu_i or lambda <= -mu_f) then
#     error "cannot evaluate Gamma function at non-positive integer":
#   fi:
#
#   if mu_f>=mu_i then
#     ME_Radial_pt(lambda,mu_f,mu_i);
#   else
#     ME_Radial_pt(lambda,mu_i,mu_f);
#   fi:
# end:
def ME_Radial_bm2(lambdaa: Expr, mu_f: nonnegint, mu_i: nonnegint) -> Expr:
    require_nonnegint('mu_f', mu_f)
    require_nonnegint('mu_i', mu_i)
    if lambdaa == S.NegativeOne:
        raise ValueError('Singular 1/beta^2 for lambda=1')
    if lambdaa.is_integer and (lambdaa <= -mu_i or lambdaa <= -mu_f):
        raise ValueError('cannot evaluate Gamma function at non-positive integer')

    mu_1: nonnegint = max(mu_f, mu_i)
    mu_2: nonnegint = min(mu_f, mu_i)
    return ME_Radial_pt(lambdaa, mu_1, mu_2)


# ME_Radial_pt:=proc(lambda::algebraic,mu_f::nonnegint,mu_i::nonnegint)
#   (-1)^(mu_f-mu_i) * sqrt( (factorial(mu_f)*GAMMA(lambda+mu_i))
#                                /(factorial(mu_i)*GAMMA(lambda+mu_f)) )
#                   / (lambda-1);
# end:
def ME_Radial_pt(lambdaa: Expr, mu_f: nonnegint, mu_i: nonnegint) -> Expr:
    require_nonnegint('mu_f', mu_f)
    require_nonnegint('mu_i', mu_i)
    # TODO: check that lambdaa is not 1 since we divide by (lambdaa -1)

    return (-1) ** (mu_f - mu_i) * sqrt(factorial(mu_f) * gamma(lambdaa + mu_i) /
                                        (factorial(mu_i) * gamma(lambdaa + mu_f))) / (lambdaa - 1)


# # The following gives matrix elements of d^2/d(beta)^2 for lambda'=lambda
# # using (23).
#
# ME_Radial_D2b:=proc(lambda::algebraic,mu_f::nonnegint,mu_i::nonnegint)
#   local stuff:
#   if mu_f=mu_i-1 then
#     stuff:=sqrt( (lambda + mu_i - 1)*mu_i );
#   elif mu_f=mu_i then
#     stuff:=-lambda - 2*mu_i;
#   elif mu_f=mu_i+1 then
#     stuff:=sqrt( (lambda + mu_i)*(mu_i+1) );
#   else
#     stuff:=0;
#   fi;
#
#   if mu_f>=mu_i then
#     stuff+(lambda-(3/2))*(lambda-(1/2))*ME_Radial_pt(lambda,mu_f,mu_i);
#   else
#     stuff+(lambda-(3/2))*(lambda-(1/2))*ME_Radial_pt(lambda,mu_i,mu_f);
#   fi:
# end:
def ME_Radial_D2b(lambdaa: Expr, mu_f: nonnegint, mu_i: nonnegint) -> Expr:
    require_nonnegint('mu_f', mu_f)
    require_nonnegint('mu_i', mu_i)

    if mu_f == mu_i - 1:
        stuff = sqrt((lambdaa + mu_i) * mu_f)
    elif mu_f == mu_i:
        stuff = -lambdaa - 2 * mu_i
    elif mu_f == mu_i + 1:
        stuff = sqrt((lambdaa + mu_i) * (mu_i + 1))
    else:
        stuff = 0

    mu_1: nonnegint = max(mu_f, mu_i)
    mu_2: nonnegint = min(mu_f, mu_i)
    return stuff + (lambdaa - Rational(3, 2)) * (lambdaa - Rational(1, 2)) * ME_Radial_pt(lambdaa, mu_1, mu_2)


# # The following gives matrix elements of beta*d/d(beta) for lambda'=lambda
# # using (24).
#
# ME_Radial_bDb:=proc(lambda::algebraic,mu_f::nonnegint,mu_i::nonnegint)
#   if mu_f=mu_i-1 then
#     sqrt( (lambda + mu_i - 1)*mu_i );
#   elif mu_f=mu_i then
#     -(1/2);
#   elif mu_f=mu_i+1 then
#     -sqrt( (lambda + mu_i)*(mu_i+1) );
#   else
#     0;
#   fi;
# end:
def ME_Radial_bDb(lambdaa: Expr, mu_f: nonnegint, mu_i: nonnegint
                  ) -> Expr:
    require_nonnegint('mu_f', mu_f)
    require_nonnegint('mu_i', mu_i)

    if mu_f == mu_i - 1:
        return sqrt((lambdaa + mu_i - 1) * mu_i)
    elif mu_f == mu_i:
        return Rational(-1, 2)
    elif mu_f == mu_i + 1:
        return -sqrt((lambdaa + mu_i) * (mu_i + 1))
    else:
        return S.Zero


# # The following gives matrix elements of beta for lambda'=lambda+1
# # using (26).
#
# ME_Radial_b_pl:=proc(lambda::algebraic,mu_f::nonnegint,mu_i::nonnegint)
#   if mu_f=mu_i-1 then
#     sqrt( mu_i );
#   elif mu_f=mu_i then
#     sqrt(lambda + mu_i);
#   else
#     0;
#   fi;
# end:
def ME_Radial_b_pl(lambdaa: Expr, mu_f: nonnegint, mu_i: nonnegint
                   ) -> Expr:
    require_nonnegint('mu_f', mu_f)
    require_nonnegint('mu_i', mu_i)

    if mu_f == mu_i - 1:
        return sqrt(mu_i)
    elif mu_f == mu_i:
        return sqrt(lambdaa + mu_i)
    else:
        return S.Zero


# # The following gives matrix elements of 1/beta for lambda'=lambda+1
# # using (28).
#
# ME_Radial_bm_pl:=proc(lambda::algebraic,mu_f::nonnegint,mu_i::nonnegint)
#   if frac(lambda)=0 and lambda <= -mu_i then
#     error "cannot evaluate Gamma function at non-positive integer":
#   fi:
#
#   if mu_f<mu_i then
#     0;
#   else
#     (-1)^(mu_f-mu_i)*sqrt( (factorial(mu_f)*GAMMA(lambda+mu_i))
#                            /(factorial(mu_i)*GAMMA(lambda+mu_f+1)) );
#   fi:
# end:
def ME_Radial_bm_pl(lambdaa: Expr, mu_f: nonnegint, mu_i: nonnegint
                    ) -> Expr:
    require_nonnegint('mu_f', mu_f)
    require_nonnegint('mu_i', mu_i)

    lambdaa = simplify(lambdaa)
    if lambdaa.is_integer and lambdaa <= -mu_i:
        raise ValueError('cannot evaluate Gamma function at non-positive integer')

    if mu_f < mu_i:
        return S.zero
    else:
        return (-1) ** (mu_f - mu_i) * sqrt((factorial(mu_f) * gamma(lambdaa + mu_i))
                                            / (factorial(mu_i) * gamma(lambdaa + mu_f + 1)) )


# # The following gives matrix elements of d/d(beta) for lambda'=lambda+1
# # using (30).
#
# ME_Radial_Db_pl:=proc(lambda::algebraic,mu_f::nonnegint,mu_i::nonnegint)
#   local res:
#   if mu_f=mu_i-1 then
#     res:=sqrt( mu_i );
#   elif mu_f=mu_i then
#     res:=-sqrt( lambda + mu_i );
#   else
#     res:=0;
#   fi;
#
#   if mu_f>=mu_i then
#     res:=res+(-1)^(mu_f-mu_i) * (lambda-1/2)
#                * sqrt( (factorial(mu_f)*GAMMA(lambda+mu_i))
#                           /(factorial(mu_i) * GAMMA(lambda+mu_f+1)) );
#   fi:
#   res:
# end:
def ME_Radial_Db_pl(lambdaa: Expr, mu_f: nonnegint, mu_i: nonnegint
                    ) -> Expr:
    require_nonnegint('mu_f', mu_f)
    require_nonnegint('mu_i', mu_i)

    res: Expr
    if mu_f == mu_i - 1:
        res = sqrt(mu_i)
    elif mu_f == mu_i:
        res = -sqrt(lambdaa + mu_i)
    else:
        res = S.Zero

    if mu_f > mu_i:
        res += (-1) ** (mu_f - mu_i) * (lambdaa - Rational(1, 2)) \
               * sqrt(((factorial(mu_f) * gamma(lambdaa + mu_i))
                       / (factorial(mu_i) * gamma(lambdaa + mu_f + 1))))

    return res


# # The following gives matrix elements of beta for lambda'=lambda-1
# # using (27).
#
# ME_Radial_b_ml:=proc(lambda::algebraic,mu_f::nonnegint,mu_i::nonnegint)
#   if mu_f=mu_i+1 then
#     sqrt( mu_f );
#   elif mu_f=mu_i then
#     sqrt(lambda + mu_i - 1);
#   else
#     0;
#   fi;
# end:
def ME_Radial_b_ml(lambdaa: Expr, mu_f: nonnegint, mu_i: nonnegint
                   ) -> Expr:
    require_nonnegint('mu_f', mu_f)
    require_nonnegint('mu_i', mu_i)

    if mu_f == mu_i + 1:
        return sqrt(mu_f)
    elif mu_f == mu_i:
        return sqrt(lambdaa + mu_i - 1)
    else:
        return S.Zero


# # The following gives matrix elements of 1/beta for lambda'=lambda-1
# # using (29).
#
# ME_Radial_bm_ml:=proc(lambda::algebraic,mu_f::nonnegint,mu_i::nonnegint)
#   if frac(lambda)=0 and lambda <= -mu_i then
#     error "cannot evaluate Gamma function at non-positive integer":
#   fi:
#
#   if mu_f>mu_i then
#     0;
#   else
#     (-1)^(mu_f-mu_i)*sqrt( (factorial(mu_i)*GAMMA(lambda+mu_f-1))
#                            /(factorial(mu_f)*GAMMA(lambda+mu_i)) );
#   fi:
# end:
def ME_Radial_bm_ml(lambdaa: Expr, mu_f: nonnegint, mu_i: nonnegint
                    ) -> Expr:
    require_nonnegint('mu_f', mu_f)
    require_nonnegint('mu_i', mu_i)

    lambdaa = simplify(lambdaa)
    if lambdaa.is_integer and lambdaa <= -mu_i:
        raise ValueError('cannot evaluate Gamma function at non-positive integer')

    if mu_f > mu_i:
        return S.Zero
    else:
        return (-1) ** (mu_f - mu_i) * sqrt((factorial(mu_i) * gamma(lambdaa + mu_f - 1))
                                            / (factorial(mu_f) * gamma(lambdaa + mu_i)))


# # The following gives matrix elements of d/d(beta) for lambda'=lambda-1
# # using (31).
#
# ME_Radial_Db_ml:=proc(lambda::algebraic,mu_f::nonnegint,mu_i::nonnegint) local res:
#   if mu_f=mu_i+1 then
#     res:=-sqrt( mu_f );
#   elif mu_f=mu_i then
#     res:=sqrt(lambda + mu_i - 1);
#   else
#     res:=0;
#   fi;
#
#   if mu_f<=mu_i then
#     res:=res+(-1)^(mu_f-mu_i) * (3/2-lambda)
#                * sqrt( (factorial(mu_i)*GAMMA(lambda+mu_f-1))
#                           /(factorial(mu_f)*GAMMA(lambda+mu_i)) );
#   fi:
#   res:
# end:
def ME_Radial_Db_ml(lambdaa: Expr, mu_f: nonnegint, mu_i: nonnegint
                    ) -> Expr:
    require_nonnegint('mu_f', mu_f)
    require_nonnegint('mu_i', mu_i)

    res: Expr
    if mu_f == mu_i + 1:
        res = -sqrt(mu_f)
    elif mu_f == mu_i:
        res = sqrt(lambdaa + mu_i - 1)
    else:
        res = S.Zero

    if mu_f <= mu_i:
        res += (-1) ** (mu_f - mu_i) * (Rational(3, 2) - lambdaa) \
               * sqrt((factorial(mu_i) * gamma(lambdaa + mu_f - 1))
                      / (factorial(mu_f) * gamma(lambdaa + mu_i)))

    return res


# # The following gives matrix elements of the identity operator
# # for lambda'=lambda+2r, for nonnegative r, using (33).
# # It makes use of MF_Radial_id_poly below.
#
# ME_Radial_id_pl:=proc(lambda::algebraic,mu_f::nonnegint,mu_i::nonnegint,
#                                   r::nonnegint)
#   if frac(lambda)=0 and lambda <= -mu_i then
#     error "cannot evaluate Gamma function at non-positive integer":
#   fi:
#
#   if mu_i<=mu_f+r then
#     eval(MF_Radial_id_poly(mu_f,mu_i,r),lamvar=lambda)
#             *sqrt( (factorial(mu_f)*GAMMA(lambda+mu_i))
#                        /(factorial(mu_i)*GAMMA(lambda+mu_f+2*r)) )
#   else
#     0
#   fi:
# end:
def ME_Radial_id_pl(lambdaa: Expr, mu_f: nonnegint, mu_i: nonnegint, r: nonnegint
                    ) -> Expr:
    require_nonnegint('mu_f', mu_f)
    require_nonnegint('mu_i', mu_i)
    require_nonnegint('r', r)

    lambdaa = simplify(lambdaa)
    if lambdaa.is_integer and lambdaa <= -mu_i:
        raise ValueError('cannot evaluate Gamma function at non-positive integer')

    # stopped here
    if mu_i < mu_f + r:
        return MF_Radial_id_poly(mu_f, mu_i, r).subs(lamvar, lambdaa) \
               * sqrt((factorial(mu_f) * gamma(lambdaa + mu_i))
                      / (factorial(mu_i) * gamma(lambdaa + mu_f + 2 * r)))
    else:
        return S.Zero


# # The following gives matrix elements of the identity operator
# # for lambda'=lambda-2r, for nonnegative r, using (33).
# # It makes use of MF_Radial_id_poly below.
#
# ME_Radial_id_ml:=proc(lambda::algebraic,mu_f::nonnegint,mu_i::nonnegint,
#                                   r::nonnegint)
#   if frac(lambda)=0 and lambda <= -mu_f+2*r then
#     error "cannot evaluate Gamma function at non-positive integer":
#   fi:
#
#   if mu_f<=mu_i+r then
#     eval(MF_Radial_id_poly(mu_i,mu_f,r),lamvar=lambda-2*r)
#             *sqrt( (factorial(mu_i)*GAMMA(lambda+mu_f-2*r))
#                        /(factorial(mu_f)*GAMMA(lambda+mu_i)) )
#   else
#     0
#   fi:
# end:
def ME_Radial_id_ml(lambdaa: Expr, mu_f: nonnegint, mu_i: nonnegint, r: nonnegint
                    ) -> Expr:
    require_nonnegint('mu_f', mu_f)
    require_nonnegint('mu_i', mu_i)
    require_nonnegint('r', r)

    lambdaa = simplify(lambdaa)
    if lambdaa.is_integer and lambdaa <= -mu_f + 2 * r:
        raise ValueError('cannot evaluate Gamma function at non-positive integer')

    if mu_f <= mu_i + r:
        return MF_Radial_id_poly(mu_i, mu_f, r).subs(lamvar, lambdaa - 2 * r) \
               * sqrt((factorial(mu_i) * gamma(lambdaa + mu_f - 2 * r))
                      / (factorial(mu_f) * gamma(lambdaa + mu_i)))
    else:
        return S.Zero


# # The following, used by the above two procedures, calculates (33)
# # for all non-negative integer r. It returns a polynomial in lamvar.
# # Note that this works for r=0 (giving delta_{mu,nu}, as required).
lamvar: Symbol = symbols('lamvar', real=True)


# MF_Radial_id_poly:=proc(mu::nonnegint,nu::nonnegint,r::nonnegint)
#   local res:
#
#   if nu>mu+r then
#     return(0):
#   fi:
#
#   res:=add( (-1)^j * binomial(r,j) * binomial(r+mu-nu+j-1,r-1)
#               * GAMMA(lamvar+mu+2*r)/GAMMA(lamvar+mu+r+j)
#               * GAMMA(mu+j+1)/GAMMA(mu+1),
#                                               j=max(0,nu-mu)..r):
#
#   simplify(res,GAMMA)*(-1)^(mu+nu):
# end;
def MF_Radial_id_poly(mu: nonnegint, nu: nonnegint, r: nonnegint
                      ) -> Expr:
    require_nonnegint('mu', mu)
    require_nonnegint('nu', nu)
    require_nonnegint('r', r)

    if nu > mu + r:
        return S.Zero

    res: Expr = sum((-1) ** j * binomial(r, j) * binomial(r + mu - nu + j - 1, r - 1)
                    * gamma(lamvar + mu + 2 * r) / gamma(lamvar + mu + r + j)
                    * gamma(mu + j + 1) / gamma(mu + 1)
                    for j in range(max(0, nu - mu), r + 1))

    return simplify(res) * (-1) ** (mu + nu)


# # Old version of above, which evaluates at the particular value
# # of lambda.
#
# MF_Radial_id_pl:=proc(lambda::algebraic,mu::nonnegint,nu::nonnegint,
#                                   r::nonnegint)
#   local res:
#
#   if nu>mu+r then
#     return(0):
#   fi:
#
#   res:=add( (-1)^j * binomial(r,j) * binomial(r+mu-nu+j-1,r-1)
#               * GAMMA(lambda+mu+2*r)/GAMMA(lambda+mu+r+j)
#               * GAMMA(mu+j+1)/GAMMA(mu+1),
#                                               j=max(0,nu-mu)..r):
#
#   simplify(res,GAMMA)*(-1)^(mu+nu):
# end;
def MF_Radial_id_pl(lambdaa: Expr, mu: nonnegint, nu: nonnegint, r: nonnegint
                    ) -> Expr:
    require_nonnegint('mu', mu)
    require_nonnegint('nu', nu)
    require_nonnegint('r', r)

    if nu > mu + r:
        return S.Zero

    res: Expr = sum((-1) ** j * binomial(r, j) * binomial(r + mu - nu + j - 1, r - 1)
                    * gamma(lambdaa + mu + 2 * r) / gamma(lambdaa + mu + r + j)
                    * gamma(mu + j + 1) / gamma(mu + 1)
                    for j in range(max(0, nu - mu), r + 1))

    return simplify(res) * (-1) ** (mu + nu)


# # Same result, but done in a different way.
#
# MF_Radial_id_pl2:=proc(lambda::algebraic,mu::nonnegint,nu::nonnegint,
#                                    r::nonnegint)
#   local res:
#
#   if nu>mu+r then
#     return(0):
#   fi:
#
#   res:=add( (-1)^j * binomial(r,j) * binomial(2*r+mu-nu-j-1,r+mu-nu)
#               * GAMMA(lambda+2*r+mu)/GAMMA(lambda+r-1)
#               * GAMMA(lambda+2*r-j-1)/GAMMA(lambda+2*r+mu-j),
#                                               j=0..k-1):
#
#   if nu=mu+r then
#     res:=res+ (-1)^r * GAMMA(lambda+2*r+mu)/GAMMA(lambda+r+mu):
#   fi:
#
#   simplify(res,GAMMA)*(-1)^(mu+nu):
# end;
def MF_Radial_id_pl2(lambdaa: Expr, mu: nonnegint, nu: nonnegint, r: nonnegint
                     ) -> Expr:
    require_nonnegint('mu', mu)
    require_nonnegint('nu', nu)
    require_nonnegint('r', r)

    if nu > mu + r:
        return S.Zero

    assert r + mu - nu >= 0
    k: int = r + mu - nu + 1 # TODO: verify this is the correct value of k
    assert k >= 1

    res: Expr = sum((-1) ** j * binomial(r, j) * binomial(2 * r + mu - nu - j - 1, r + mu - nu)
                    * gamma(lambdaa + 2 * r + mu) / gamma(lambdaa + r - 1)
                    * gamma(lambdaa + 2 * r - j - 1) / gamma(lambdaa + 2 * r + mu - j)
                    for j in range(k))

    if nu == mu + r:
        res += (-1) ** r * gamma(lambdaa + 2 * r + mu) / gamma(lambdaa + r + mu)

    return simplify(res) * (-1) ** (mu + nu)


# # The following procedure returns a single matrix element
# #     F^{(anorm)}_{lambda_var,mu_f}{lambda,mu_i}(Op),
# # for Op one of the operators from Table I with symbolic name radial_op.
# # The identity operator is also available using symbolic name Radial_id.
# # If possible, the matrix element is obtained using one of the
# # above procedures. If not, it is obtained by matrix multiplication
# # where one matrix is obtained non-analytically.
# # This procedure is not used elsewhere.
#
# ME_Radial:=proc(radial_op::algebraic, anorm::algebraic,
#                    lambda::algebraic, lambda_var::integer,
#                    mu_f::nonnegint, mu_i::nonnegint)
#   local MM:
#
#   if radial_op=Radial_b2 and lambda_var=0 then
#     ME_Radial_b2(lambda,mu_f,mu_i)/anorm^2;
#   elif radial_op=Radial_bm2 and lambda_var=0 then
#     ME_Radial_bm2(lambda,mu_f,mu_i)*anorm^2;
#   elif radial_op=Radial_D2b and lambda_var=0 then
#     ME_Radial_D2b(lambda,mu_f,mu_i)*anorm^2;
#   elif radial_op=Radial_bDb and lambda_var=0 then
#     ME_Radial_bDb(lambda,mu_f,mu_i);
#
#   elif radial_op=Radial_b and lambda_var=1 then
#     ME_Radial_b_pl(lambda,mu_f,mu_i)/anorm;
#   elif radial_op=Radial_bm and lambda_var=1 then
#     ME_Radial_bm_pl(lambda,mu_f,mu_i)*anorm;
#   elif radial_op=Radial_Db and lambda_var=1 then
#     ME_Radial_Db_pl(lambda,mu_f,mu_i)*anorm;
#
#   elif radial_op=Radial_b and lambda_var=-1 then
#     ME_Radial_b_ml(lambda,mu_f,mu_i)/anorm;
#   elif radial_op=Radial_bm and lambda_var=-1 then
#     ME_Radial_bm_ml(lambda,mu_f,mu_i)*anorm;
#   elif radial_op=Radial_Db and lambda_var=-1 then
#     ME_Radial_Db_ml(lambda,mu_f,mu_i)*anorm;
#
#   elif radial_op=Radial_S0 and lambda_var=0 then
#     ME_Radial_S0(lambda,mu_f,mu_i);
#   elif radial_op=Radial_Sp and lambda_var=0 then
#     ME_Radial_Sp(lambda,mu_f,mu_i);
#   elif radial_op=Radial_Sm and lambda_var=0 then
#     ME_Radial_Sm(lambda,mu_f,mu_i);
#
#
#   elif radial_op=Radial_id and type(lambda_var,even) then
#     if lambda_var>=0 then
#       ME_Radial_id_pl(lambda,mu_f,mu_i,lambda_var/2):
#     else
#       ME_Radial_id_ml(lambda,mu_f,mu_i,-lambda_var/2):
#     fi:
#
#   else  # form a matrix
#         # might be a good idea to check that we have a valid radial operator
#       if radial_op=Radial_id then
#         MM:=RepRadial_Prod([],_passed[2..4],0,max(mu_f,mu_i),
#                                      iquo(abs(lambda_var)+3,2)):
#       else
#         MM:=RepRadial_Prod([radial_op],_passed[2..4],0,max(mu_f,mu_i),
#                                      iquo(abs(lambda_var)+3,2)):
#       fi:
#       MM[mu_f+1,mu_i+1]:  # matrices start at mu=nu=0!
#   fi:
#
# end:
def ME_Radial(radial_op: Expr, anorm: Expr,
              lambdaa: Expr, lambda_var: int,
              mu_f: nonnegint, mu_i: nonnegint
              ) -> Expr:
    require_nonnegint('mu_f', mu_f)
    require_nonnegint('mu_i', mu_i)

    if radial_op == Radial_b2 and lambda_var == 0:
        return ME_Radial_b2(lambdaa, mu_f, mu_i) / anorm ** 2
    elif radial_op == Radial_bm2 and lambda_var == 0:
        return ME_Radial_bm2(lambdaa, mu_f, mu_i) * anorm ** 2
    elif radial_op == Radial_D2b and lambda_var == 0:
        return ME_Radial_D2b(lambdaa, mu_f, mu_i) * anorm ** 2
    elif radial_op == Radial_bDb and lambda_var == 0:
        return ME_Radial_bDb(lambdaa, mu_f, mu_i)

    elif radial_op == Radial_b and lambda_var == 1:
        return ME_Radial_b_pl(lambdaa, mu_f, mu_i) / anorm
    elif radial_op == Radial_bm and lambda_var == 1:
        return ME_Radial_bm_pl(lambdaa, mu_f, mu_i) * anorm
    elif radial_op == Radial_Db and lambda_var == 1:
        return ME_Radial_Db_pl(lambdaa, mu_f, mu_i) * anorm

    elif radial_op == Radial_b and lambda_var == -1:
        return ME_Radial_b_ml(lambdaa, mu_f, mu_i) / anorm
    elif radial_op == Radial_bm and lambda_var == -1:
        return ME_Radial_bm_ml(lambdaa, mu_f, mu_i) * anorm
    elif radial_op == Radial_Db and lambda_var == -1:
        return ME_Radial_Db_ml(lambdaa, mu_f, mu_i) * anorm

    elif radial_op == Radial_S0 and lambda_var == 0:
        return ME_Radial_S0(lambdaa, mu_f, mu_i)
    elif radial_op == Radial_Sp and lambda_var == 0:
        return ME_Radial_Sp(lambdaa, mu_f, mu_i)
    elif radial_op == Radial_Sm and lambda_var == 0:
        return ME_Radial_Sm(lambdaa, mu_f, mu_i)

    elif radial_op == Radial_id and is_even(lambda_var):
        if lambda_var >= 0:
            return ME_Radial_id_pl(lambdaa, mu_f, mu_i, lambda_var // 2)
        else:
            return ME_Radial_id_ml(lambdaa, mu_f, mu_i, -lambda_var // 2)

    else:
        op_prod: list[Symbol] = [] if radial_op == Radial_id else [radial_op]
        MM: Matrix = RepRadial_Prod(op_prod, anorm, lambdaa, lambda_var, 0, max(mu_f, mu_i),
                                    iquo(abs(lambda_var) + 3, 2))
        return MM[mu_f, mu_i]


# ###########################################################################
#
# # The following uses one of the above procedures
# #    ME_Radial_S0, ME_Radial_Sp, ME_Radial_Sm,
# #    ME_Radial_b2, ME_Radial_bm2, ME_Radial_D2b, ME_Radial_bDb,
# #    ME_Radial_b_pl, ME_Radial_bm_pl, ME_Radial_Db_pl,
# #    ME_Radial_b_ml, ME_Radial_bm_ml, ME_Radial_Db_ml
# # above, this being specified in the first argument, to construct an
# # explicit representation matrix from the elements
# #     F^{(a)}_{lambda',mu_f}{lambda,mu_i}(Op),
# # nu_min <= mu_i,mu_f <= nu_max, where Op is the corresponding operator,
# # and lambda'-lambda is as above. This is for a=1: the general a case
# # is obtained later by multiplying by some power of a.
#
# # Note that the datatype of the resulting matrix is not fixed:
# # Maple chooses it depending on the type of lambda
# # (e.g. lambda=5/2 gives algebraic, lambda=2.5 gives floats;
# #  these may be tested for using the Maple commands
# #          type(MM,'Matrix'(datatype=anything));
# #          type(MM,'Matrix'(datatype=float));
# # ).
# # It'd thus be a good idea to apply evalf to all the matrix elements
# # obtained before diagonalisation etc.
#
# # Typically, this procedure and the two that follow will get called
# # many times during the construction of an operator (Hamiltonian) for
# # various values of lambda, but the same range of nu_min & nu_max.
# # Each use the remember option, and these remember tables are cleared
# # at the end of the procedures RepXspace and RepRadial_Prod.
#
# RepRadial:=proc(ME::procedure,lambda::algebraic,
#                               nu_min::nonnegint,nu_max::nonnegint)
#     option remember;
#
#   simplify(Matrix(nu_max-nu_min+1,(i,j)->ME(lambda,nu_min-1+i,nu_min-1+j)),
#        GAMMA,radical):
# end:
@cache
def RepRadial(ME: Callable, lambdaa: Expr,
              nu_min: nonnegint, nu_max: nonnegint
              ) -> Matrix:
    require_nonnegint_range('nu', nu_min, nu_max)

    n: int = nu_max - nu_min + 1
    M: Matrix = Matrix(n, n, lambda i, j: ME(lambdaa, nu_min + int(i), nu_min + int(j)))

    return simplify(M)


# # The following works similarly to RepRadial above, but takes an additional
# # parameter which is passed to the procedure ME which calculates the
# # matrix elements. This enables the construction of representations of
# # the identity operator using the procedures ME_Radial_id_pl and
# # ME_Radial_id_ml.
#
# RepRadial_param:=proc(ME::procedure,lambda::algebraic,
#                            nu_min::nonnegint,nu_max::nonnegint,param::integer)
#     option remember;
#
#   simplify(Matrix(nu_max-nu_min+1,
#                   (i,j)->ME(lambda,nu_min-1+i,nu_min-1+j,param)),
#        GAMMA,radical):
# end:
@cache
def RepRadial_param(ME: Callable, lambdaa: Expr,
                    nu_min: nonnegint, nu_max: nonnegint, param: int
                    ) -> Matrix:
    require_nonnegint_range('nu', nu_min, nu_max)

    n: int = nu_max - nu_min + 1
    M: Matrix = Matrix(n, n, lambda i, j: ME(lambdaa, nu_min + int(i), nu_min + int(j), param))

    return simplify(M)


# # The following returns the square root of the matrix obtained above.
# # The arguments are as above, and the return matrix contain float entries.
# # (This has severe problems dealing with Matrices larger than about 20x20 -
# #  the problem is in Maple's MatrixPower).
# # This has now been replaced by Matrix_sqrt below
#
# #RepRadial_sq:=proc(ME::procedure,lambda::algebraic,
# #                                 nu_min::nonnegint,nu_max::nonnegint)
# #    option remember;
# #
# #  MatrixPower(evalf(RepRadial(ME,lambda,nu_min,nu_max)),1/2):
# #end:
@cache
def RepRadial_sq(ME: Callable, lambdaa: Expr,
                    nu_min: nonnegint, nu_max: nonnegint
                    ) -> Matrix:
    require_nonnegint_range('nu', nu_min, nu_max)

    M: Matrix = RepRadial(ME, lambdaa, nu_min, nu_max).evalf()

    return M ** Rational(1, 2)


# # The following returns the positive definite square root of a
# # symmetric Matrix, using my Eigenfiddle procedure (defined later)
# # which provides a convenient interface to Maple's Eigenvectors procedure.
#
# Matrix_sqrt:=proc(Amatrix::Matrix,$)
#     option remember;
#     local Edata,Diag_sq:
#
#     # first obtain (real) eigenvalues and eigenvectors
#
#     Edata:=Eigenfiddle(evalf(Amatrix)):
#
#     # then form diagonal Matrix from square roots of eigenvalues
#
#     Diag_sq:=Matrix(map(sqrt,Edata[1]),scan=diagonal);
#
#     # transform back into the original (non eigen) basis
#
#     Edata[2].Diag_sq.MatrixInverse(Edata[2])
# end:
@cache
def Matrix_sqrt(Amatrix: Matrix) -> Matrix:

    eigen_vals: list[float]
    P: Matrix
    eigen_vals, P = Eigenfiddle(Amatrix.evalf())

    Diag_sq: Matrix = diag(*[sqrt(val) for val in eigen_vals])

    return P * Diag_sq * P ** -1


# # The following is similar to the above to produce the inverse of
# # the square root of a Matrix.
#
# Matrix_sqrtInv:=proc(Amatrix::Matrix,$)
#     option remember;
#     local Edata,Diag_sq:
#
#     # first obtain (real) eigenvalues and eigenvectors
#
#     Edata:=Eigenfiddle(evalf(Amatrix)):
#
#     # then form diagonal Matrix from square roots of eigenvalues
#
#     Diag_sq:=Matrix(map(x->1/sqrt(x),Edata[1]),scan=diagonal);
#
#     # transform back into the original (non eigen) basis
#
#     Edata[2].Diag_sq.MatrixInverse(Edata[2])
# end:
@cache
def Matrix_sqrtInv(Amatrix: Matrix) -> Matrix:

    eigen_vals, P = Eigenfiddle(Amatrix.evalf())

    Diag_sq: Matrix = diag(*[1 / sqrt(val) for val in eigen_vals])

    return P * Diag_sq * P ** -1


# ###########################################################################
#
# # The following represents the radial operator beta^K * d^T/d(beta)^T,
# # with a specific lambda shift (for K integer, T nonneg integer, R integer).
# # It returns the explicit matrix of elements
# #     F^{(anorm)}_{lambda+R,mu_f}{lambda,mu_i}(beta^K * d^T/d(beta)^T),
# # nu_min <= mu_i,mu_f <= nu_max. It is only used by RepRadialshfs_Prod().
# # The values lambda and lambda+R should be positive (an error
# # results if this is not the case).
#
# # This is implemented by forming a product between matrices for
# # the terms beta and d/d(beta) (some are paired, e.g. beta^2),
# # and splitting R amongst these terms in a certain judicious way,
# # with each getting a lambda shift of +1,0,-1,
# # and also using the identity operator with a shift if required
# # (this splitting is determined by the procedure Lambda_Splits below).
#
# # The matrix elements of the result are analytic (exact expressions
# # involving surds) unless anorm or lambda are floats, or K+T+R is odd,
# # in which cases the matrix elements might be a mix of floats and surds.
#
# RepRadial_bS_DS:=proc(K::integer, T::nonnegint, anorm::algebraic,
#                           lambda::algebraic, R::integer,
#                           nu_min::nonnegint, nu_max::nonnegint)
#   option remember;
#   local i,n,imm,Mat,Mat_product,lambda_run,lamX,lam_splits;
#
#   if evalf(lambda)<=0 or evalf(lambda+R)<=0 then
#      error("Non-positive lambda shift for operator [%1,%2]",K,T):
#   fi:
#
#   # deal first with the special case that K=T=0 and R is odd:
#
#   if K=0 and T=0 and type(R,odd) then
#     if R<0 then  # beta[0] * (1/beta)[-1] * id[-even]
#
#       Mat_product:=RepRadial(ME_Radial_b2,lambda+R,nu_min,nu_max):
#       Mat_product:=Matrix_sqrt(Mat_product):
#
#       Mat:=RepRadial(ME_Radial_bm_ml,lambda+R+1,nu_min,nu_max);
#       Mat_product:=MatrixMatrixMultiply(Mat_product,Mat):
#
#       if R<-1 then
#         Mat:=RepRadial_param(ME_Radial_id_ml,lambda,nu_min,nu_max,-(R+1)/2);
#         Mat_product:=MatrixMatrixMultiply(Mat_product,Mat):
#       fi:
#
#     else  # id[even] * (1/beta)[-1] * beta[0]
#
#       Mat_product:=RepRadial(ME_Radial_b2,lambda,nu_min,nu_max):
#       Mat_product:=Matrix_sqrt(Mat_product):
#
#       Mat:=RepRadial(ME_Radial_bm_pl,lambda,nu_min,nu_max);
#       Mat_product:=MatrixMatrixMultiply(Mat,Mat_product):
#
#       if R>1 then
#         Mat:=RepRadial_param(ME_Radial_id_pl,lambda+1,nu_min,nu_max,(R-1)/2);
#         Mat_product:=MatrixMatrixMultiply(Mat,Mat_product):
#       fi:
#
#     fi:
#
#     return (Mat_product):
#   fi:
#
#
#   # determine how to partition the lambda shift R amongst the individual terms
#   # (we could do this in-line)
#
#   lam_splits:=Lambda_Splits(K,T,R):
#
#   # note that we have to account for there possibly being excess variation,
#   # this being the case if there are more entries in lam_splits than |K|+T.
#   # In such a case, lam_splits[1] should be even because the only possible
#   # odd case (see Lambda_Splits() above) arises for K=T=0 and R odd,
#   # and this has already been dealt with.
#
#   n:=abs(K)+T:
#
#   if nops(lam_splits)>n then
#     lamX:=lam_splits[1]:            # even extra variation - for identity op
#     lam_splits:=lam_splits[2..-1]:  # remove first element
#
#     # below we then prepend or append the identity operator;
#
#   else
#     lamX:=0:
#   fi:
#
#   # we now work right to left building up the product, with the
#   # current value of lambda being carried along
#   # (the procedure Lambda_Splits better deals with R->L).
#
#   lambda_run:=lambda:
#
#   # We put an identity op on the right if lamX<0 (on left for lamX>0 below)
#
#   if lamX<0 then
#     Mat_product:=RepRadial_param(ME_Radial_id_ml,lambda_run,nu_min,nu_max,
#                                                      -lamX/2);
#     lambda_run:=lambda_run+lamX:
#   fi:
#
#   # form required product, multiplying from the right, and changing the
#   # lambdas as we go. First set up loop.
#
#
#   i:=n:
#
#   while i>0 do
#
#     if lam_splits[i]>0 then
#
#       if i<=K then  # then K is +ve
#         Mat:=RepRadial(ME_Radial_b_pl,lambda_run,nu_min,nu_max);
#         Mat:=MatrixScalarMultiply(Mat,1/anorm);
#
#       elif i<=-K then  # then K is -ve
#         Mat:=RepRadial(ME_Radial_bm_pl,lambda_run,nu_min,nu_max);
#         Mat:=MatrixScalarMultiply(Mat,anorm);
#
#       else # then i>|K|
#         Mat:=RepRadial(ME_Radial_Db_pl,lambda_run,nu_min,nu_max);
#         Mat:=MatrixScalarMultiply(Mat,anorm);
#       fi:
#
#       imm:=1:
#
#     elif lam_splits[i]<0 then
#
#       if i<=K then  # then K is +ve => beta
#         Mat:=RepRadial(ME_Radial_b_ml,lambda_run,nu_min,nu_max);
#         Mat:=MatrixScalarMultiply(Mat,1/anorm);
#
#       elif i<=-K then  # then K is -ve => beta^{-1}
#         Mat:=RepRadial(ME_Radial_bm_ml,lambda_run,nu_min,nu_max);
#         Mat:=MatrixScalarMultiply(Mat,anorm);
#
#       else # then i>|K|
#         Mat:=RepRadial(ME_Radial_Db_ml,lambda_run,nu_min,nu_max);
#         Mat:=MatrixScalarMultiply(Mat,anorm);
#       fi:
#
#       imm:=1:
#
#     elif i>1 and lam_splits[i-1]=0 then   # pair 00 of lambda changers
#
#       if i<=K then # then K is +ve => beta^2
#         Mat:=RepRadial(ME_Radial_b2,lambda_run,nu_min,nu_max);
#         Mat:=MatrixScalarMultiply(Mat,1/anorm^2);
#
#       elif i<=-K then  # then K is -ve => beta^{-2}
#         Mat:=RepRadial(ME_Radial_bm2,lambda_run,nu_min,nu_max);
#         Mat:=MatrixScalarMultiply(Mat,anorm^2);
#
#       elif i=K+1 then # then K is +ve => beta*d/d(beta)
#         Mat:=RepRadial(ME_Radial_bDb,lambda_run,nu_min,nu_max);
#
#       elif i=-K-1 then # then K is -ve => beta^{-1}*d/d(beta)
#         error("This shouldn't arise!"):
#
#       else # d^2/d(beta)^2
#         Mat:=RepRadial(ME_Radial_D2b,lambda_run,nu_min,nu_max);
#         Mat:=MatrixScalarMultiply(Mat,anorm^2);
#       fi:
#
#       imm:=2:
#
#     else # an isolated 0 lambda change
#
#       if i<=K then  # then K is +ve => beta
#         # obtain a matrix representing beta by taking the positive
#         # definite square root of that representing beta^2.
#         Mat:=RepRadial(ME_Radial_b2,lambda_run,nu_min,nu_max):
#         Mat:=Matrix_sqrt(Mat):
#         Mat:=MatrixScalarMultiply(Mat,1/anorm);
#
#       elif i<=-K then  # then K is -ve => beta^{-1}
#         # obtain a matrix representing 1/beta by taking the
#         # inverse of the positive definite square root of that
#         # representing beta^2.
#         Mat:=RepRadial(ME_Radial_b2,lambda_run,nu_min,nu_max):
#         Mat:=Matrix_sqrtInv(Mat):
#         Mat:=MatrixScalarMultiply(Mat,anorm);
#
#       else # then i>|K| => d/d(beta)
#         # obtain a matrix representing d/d(beta) by taking the inverse
#         # of the positive definite square root of that representing beta^2
#         # multiplied by that for beta*d/d(beta).
#         Mat:=RepRadial(ME_Radial_b2,lambda_run,nu_min,nu_max):
#         Mat:=MatrixMatrixMultiply( Matrix_sqrtInv(Mat),
#                 evalf(RepRadial(ME_Radial_bDb,lambda_run,nu_min,nu_max))):
#         Mat:=MatrixScalarMultiply(Mat,anorm);
#       fi:
#
#       imm:=1:
#
#     fi:
#
#     # multiply this term into product
#
#     if i=n and lamX>=0 then  # first in product
#       Mat_product:=Mat:
#         # These matrices now have the same storage: but Mat_product is not
#         # then changed when Mat is reassigned to another Matrix in the next
#         # instance of loop.
#     else
#         # It would be nice to use inplace multiplication here, but this
#         # fails when the two matrices have entries of different types.
#       Mat_product:=MatrixMatrixMultiply(Mat,Mat_product):
#     fi:
#
#     lambda_run:=lambda_run+lam_splits[i]:   # update lambda along product
#     i:=i-imm: # skip index to next op
#
#   od:
#
#
#   # We still might need to multiply on the left by an even lambda>0 shifted
#   # identity operator.
#
#   if lamX>0 then
#     Mat:=RepRadial_param(ME_Radial_id_pl,lambda_run,nu_min,nu_max,lamX/2);
#     if n>0 then
#       Mat_product:=MatrixMatrixMultiply(Mat,Mat_product):
#     else
#       Mat_product:=Mat:
#     fi:
#   fi:
#
#   # In the following case, nothing has yet been formed:
#
#   if n=0 and lamX=0 then
#     Mat_product:=Matrix([seq(1,i=nu_min..nu_max)],scan=diagonal):
#   fi:
#
#   # Maple sometimes has problems unless we specify the type of combine...
#
#   combine(simplify(Mat_product, sqrt),radical):
#
# end:
@cache
def RepRadial_bS_DS(K: int, T: nonnegint, anorm:Expr,
                    lambdaa: Expr, R: int,
                    nu_min: nonnegint, nu_max: nonnegint
                    ) -> Matrix:
    require_nonnegint('T', T)
    require_nonnegint_range('nu', nu_min, nu_max)

    if lambdaa.evalf() <= 0 or (lambdaa + R).evalf() <= 0:
        raise ValueError(f'Non-positive lambda shift for operator [{K},{T}]')

    Mat_product: Matrix
    Mat: Matrix
    if K == 0 and T == 0 and is_odd(R):
        if R < 0:
            Mat_product = RepRadial(ME_Radial_b2, lambdaa + R, nu_min, nu_max)
            Mat_product = Matrix_sqrt(Mat_product)

            Mat = RepRadial(ME_Radial_bm_ml, lambdaa + R + 1, nu_min, nu_max)
            Mat_product *= Mat

            if R < -1:
                Mat = RepRadial_param(ME_Radial_id_ml, lambdaa, nu_min, nu_max, -(R + 1) // 2)
                Mat_product *= Mat

        else:

            Mat_product = RepRadial(ME_Radial_b2, lambdaa, nu_min, nu_max)
            Mat_product = Matrix_sqrt(Mat_product)

            Mat = RepRadial(ME_Radial_bm_pl, lambdaa, nu_min, nu_max)
            Mat_product = Mat * Mat_product

            if R > 1:
                Mat = RepRadial_param(ME_Radial_id_pl, lambdaa + 1, nu_min, nu_max, (R - 1) // 2)
                Mat_product = Mat * Mat_product

        return Mat_product

    lam_splits: list[int] = Lambda_Splits(K, T, R)

    n: int = abs(K) + T

    lamX: int
    if len(lam_splits) > n:
        lamX = lam_splits[0]
        lam_splits = lam_splits[1:]
    else:
        lamX = 0

    assert len(lam_splits) == n

    lambda_run: Expr = lambdaa

    if lamX < 0:
        assert is_even(lamX)
        Mat_product = RepRadial_param(ME_Radial_id_ml, lambda_run, nu_min, nu_max, -lamX // 2)

        lambda_run += lamX

    i: int = n

    while i > 0:

        imm: int
        if lam_splits[i - 1] > 0:

            if i <= K:
                assert K > 0
                Mat = RepRadial(ME_Radial_b_pl, lambda_run, nu_min, nu_max)
                Mat *= 1 / anorm

            elif i <= -K:
                assert K < 0
                Mat = RepRadial(ME_Radial_bm_pl, lambda_run, nu_min, nu_max)
                Mat *= anorm

            else:
                assert i > abs(K)
                Mat = RepRadial(ME_Radial_Db_pl, lambda_run, nu_min, nu_max)
                Mat *= anorm

            imm = 1

        elif lam_splits[i - 1] < 0:

            if i <= K:
                assert K > 0
                Mat = RepRadial(ME_Radial_b_ml, lambda_run, nu_min, nu_max)
                Mat *= 1 / anorm

            elif i <= -K:
                assert K < 0
                Mat = RepRadial(ME_Radial_bm_ml, lambda_run, nu_min, nu_max)
                Mat *= anorm

            else:
                assert i > abs(K)
                Mat = RepRadial(ME_Radial_Db_ml, lambda_run, nu_min, nu_max)
                Mat *= anorm

            imm = 1

        elif i > 1 and lam_splits[i - 2] == 0:

            if i <= K:
                assert K > 0
                Mat = RepRadial(ME_Radial_b2, lambda_run, nu_min, nu_max)
                Mat *= 1 / anorm ** 2

            elif i <= -K:
                assert K < 0
                Mat = RepRadial(ME_Radial_bm2, lambda_run, nu_min, nu_max)
                Mat *= anorm ** 2

            elif i == K + 1:
                assert K > 0
                Mat = RepRadial(ME_Radial_bDb, lambda_run, nu_min, nu_max)

            elif i == -K - 1:
                raise ValueError("This shouldn't arise!")

            else:
                Mat = RepRadial(ME_Radial_D2b, lambda_run, nu_min, nu_max)
                Mat *= anorm ** 2

            imm = 2

        else:

            if i <= K:
                assert K > 0
                Mat = RepRadial(ME_Radial_b2, lambda_run, nu_min, nu_max)
                Mat = Matrix_sqrt(Mat)
                Mat *= 1 / anorm

            elif i <= -K:
                assert K < 0
                Mat = RepRadial(ME_Radial_b2, lambda_run, nu_min, nu_max)
                Mat = Matrix_sqrtInv(Mat)
                Mat *= anorm

            else:
                assert i > abs(K)
                Mat = RepRadial(ME_Radial_b2, lambda_run, nu_min, nu_max)
                Mat = Matrix_sqrtInv(Mat) * RepRadial(ME_Radial_bDb, lambda_run, nu_min, nu_max).evalf()
                Mat *= anorm

            imm = 1

        if i == n and lamX >= 0:
            Mat_product = Mat
        else:
            Mat_product = Mat * Mat_product

        lambda_run += lam_splits[i - 1]
        i -= imm

    if lamX > 0:
        assert is_even(lamX)
        Mat = RepRadial_param(ME_Radial_id_pl, lambda_run, nu_min, nu_max, lamX // 2)
        if n > 0:
            Mat_product = Mat * Mat_product
        else:
            Mat_product = Mat

    if n == 0 and lamX == 0:
        Mat_product = eye(nu_max - nu_min + 1)

    return simplify(Mat_product)


# # The following procedure is (only) called by the above RepRadial_bS_DS:
# # it considers a term of the form beta^K * d^T/d(beta)^T, and for
# # a specific overall lambda shift R, indicates how to sensibly assign
# # lambda shifts of 0,+1 or -1 to each term
# # (there are various constraints - for one, the zero shifts should
# # be paired apart from one case which we put at start; another is
# # that a beta*d/d(beta) is split first (because the beta might be beta^(-1)).
# # The return is a list of integers of length |K|+T or |K|+T+1.
# # In the former case, it is just the list of shifts;
# # in the latter case, an extra entry is put at the start:
# # the calling procedure is required to test for this.
# # This value is the shift required for an extra identity operator
# # (it is even in as many cases as possible -
# #          but is odd in only one case: iff K=T=0 and R is odd).
#
# Lambda_Splits:=proc(K::integer, T::nonnegint, R::integer)
#   local KT,IR,Z,ZT,shifts:
#
#   KT:=abs(K)+T:  # shiftings to be assigned
#   IR:=abs(R)-KT: # +ve if we need extra lambda shift
#
#   if IR>0 then   # put extra shift at start
#     if type(IR,even) then
#       shifts:=[IR,1$KT]:
#     elif KT>0 then # cannot do this if KT=0
#       shifts:=[IR+1,0,1$(KT-1)]:
#     else
#       shifts:=[IR]: # odd flag - extra processsing needed later
#     fi:
#   else
#     Z:=iquo(-IR,2):  # no of zero pairs to be assigned
#     ZT:=min(Z,iquo(T,2)):  # no of these for the Ts
#     shifts:=[0$(KT-abs(R)-2*ZT),1$abs(R),0$(2*ZT)]:
#     # special case to prevent beta^(-1)*d/d(beta) being assigned 00.
#     if K<0 and R=0 and type(T,odd) then
#       shifts[-K]:=1:
#       shifts[-K+1]:=-1:
#     fi:
#   fi:
#
#   if R<0 then
#     -shifts
#   else
#     shifts
#   fi:
#
# end:
def Lambda_Splits(K: int, T: nonnegint, R: int
                  ) -> list[int]:
    require_int('K', K)
    require_nonnegint('T', T)
    require_int('R', R)

    KT: int = abs(K) + T
    IR: int = abs(R) - KT

    shifts: list[int]
    if IR > 0:
        if is_even(IR):
            shifts = [IR] + [1] * KT
        elif KT > 0:
            shifts = [IR + 1, 0] + [1] * (KT - 1)
        else:
            shifts = [IR]
    else:
        Z: int = iquo(-IR, 2)
        ZT: int = min(Z, iquo(T, 2))
        shifts = [0] * (KT - abs(R) - 2 * ZT) + [1] * abs(R) + [0] * (2 * ZT)
        if K < 0 and R == 0 and is_odd(T):
            shifts[-K - 1] = 1
            shifts[-K] = -1

    if R < 0:
        return [-s for s in shifts]
    else:
        return shifts


# # The following returns, for a certain Op determined by rps_op,
# # the explicit matrix of elements
# #     F^{(anorm)}_{lambda+R,mu_f}{lambda,mu_i}(Op),
# # nu_min <= mu_i,mu_f <= nu_max.
#
# # Here Op is a product formed from beta, d/d(beta), and the su(1,1)
# # operators Sp,Sm,S0. In rps_op, it is given as a list of elements
# # of types [K,T] and S, the former obtained using RepRadial_bS_DS below
# # and the latter directly from RepRadial (here K,T and S are integers,
# # with T nonnegative, and S=+1,-1,0).


class KTSOp(ABC):
    """Abstract base class for KTOp and SOp."""

    @abstractmethod
    def representation(self, anorm: Expr,
                       lambdaa: Expr, R: int,
                       nu_min: nonnegint, nu_max: nonnegint
                       ) -> Matrix:
        ...


class KTOp(KTSOp):
    K: int
    T: nonnegint

    def __init__(self, K: int, T: nonnegint) -> None:
        require_int('K', K)
        require_nonnegint('T', T)

        self.K = K
        self.T = T

    def __eq__(self, other) -> bool:
        return self.K == other.K and self.T == other.T if isinstance(other, KTOp) else False

    def __hash__(self) -> int:
        return hash((self.K, self.T))

    def representation(self, anorm: Expr,
                       lambdaa: Expr, R: int,
                       nu_min: nonnegint, nu_max: nonnegint
                       ) -> Matrix:
        return RepRadial_bS_DS(self.K, self.T, anorm, lambdaa, R, nu_min, nu_max)


class SOp(KTSOp):
    S: int

    def __init__(self, S: int) -> None:
        if S not in {-1, 0, 1}:
            raise ValueError(f'S must be -1, 0, or 1. Got: {S}')

        self.S = S

    def __eq__(self, other) -> bool:
        return self.S == other.S if isinstance(other, SOp) else False

    def __hash__(self) -> int:
        return hash(self.S)

    def representation(self, anorm: Expr,
                       lambdaa: Expr, R: int,
                       nu_min: nonnegint, nu_max: nonnegint
                       ) -> Matrix:
        if R != 0:
            raise ValueError("Non-zero lambda shift for S operator (this shouldn't arise!)")

        ME: Callable = [ME_Radial_Sm, ME_Radial_S0, ME_Radial_Sp][self.S + 1]
        return RepRadial(ME, lambdaa, nu_min, nu_max)


KTSOps = tuple[KTSOp, ...]


# # For each element in the list rps_op, the lambda shift is specified
# # by the corresponding element of lambda_shfs (the two lists should
# # then be the same size).
#
# RepRadialshfs_Prod:=proc(rps_op::list, anorm::algebraic,
#                           lambda::algebraic, lambda_shfs::list,
#                           nu_min::nonnegint, nu_max::nonnegint)
#
#   option remember;
#   local i,n,Mat,Mat_product,lambda_run,r_op;
#
#   n:=nops(rps_op);
#
#   if n=0 then    # null product: require identity matrix
#     Mat_product:=Matrix([seq(1,i=nu_min..nu_max)],scan=diagonal):
#
#   else
#     lambda_run:=lambda:
#
#     # form required product, multiplying from the right
#     # with inplace multiplications ...
#
#     for i from n to 1 by -1 do
#
#       r_op:=rps_op[i]:
#
#       if type(r_op,integer) then
#         if lambda_shfs[i]<>0 then
#           error(
#             "Non-zero lambda shift for S operator (this shouldn't arise!)"):
#         fi:
#
#         if r_op=0 then
#           Mat:=RepRadial(ME_Radial_S0,lambda_run,nu_min,nu_max);
#         elif r_op=1 then
#           Mat:=RepRadial(ME_Radial_Sp,lambda_run,nu_min,nu_max);
#         elif r_op=-1 then
#           Mat:=RepRadial(ME_Radial_Sm,lambda_run,nu_min,nu_max);
#         else
#           error("Unrecognised S operator"):
#         fi:
#       elif type(r_op,list(integer)) then
#         # r_op[1]:   integer exponent of beta
#         # r_op[2]:   non-neg integer, order of d/d(beta)
#
#         Mat:=RepRadial_bS_DS(r_op[1],r_op[2],anorm,lambda_run,lambda_shfs[i],
#                                    nu_min,nu_max):
#         lambda_run:=lambda_run+lambda_shfs[i]:
#       else
#           error "radial operator %1 undefined", r_op;
#       fi:
#
#       if i=n then
#         Mat_product:=Mat:
#           # These matrices now have the same storage: but Mat_product is not
#           # then changed when Mat is reassigned to another Matrix in the next
#           # instance of loop.
#       else
#         Mat_product:=MatrixMatrixMultiply(Mat,Mat_product):
#       fi:
#
#     od:
#
#   fi:
#
#   # Maple sometimes has problems unless we specify the type of combine...
#
#   combine(simplify(Mat_product, sqrt),radical):
#
# end;
@cache
def RepRadialshfs_Prod(rps_op: KTSOps, anorm: Expr,
                       lambdaa: Expr, lambda_shfs: tuple[int],
                       nu_min: nonnegint, nu_max: nonnegint
                       ) -> Matrix:
    require_nonnegint_range('nu', nu_min, nu_max)

    n: int = len(rps_op)

    Mat_product: Matrix
    Mat: Matrix
    if n == 0:
        Mat_product = eye(nu_max - nu_min + 1)

    else:
        lambda_run: Expr = lambdaa

        for i in range(n, 0, -1):

            r_op: KTSOp = rps_op[i - 1]
            R: int = lambda_shfs[i - 1]
            Mat = r_op.representation(anorm, lambda_run, R, nu_min, nu_max)
            lambda_run += R

            if i == n:
                Mat_product = Mat
            else:
                Mat_product = Mat * Mat_product

    return simplify(Mat_product)


# # The following represents a product Op of radial operators, specified by a
# # list rbs_op, between two bases with the difference between their lambda
# # values given by lambda_var. It returns the explicit matrix of
# # elements
# #     F^{(anorm)}_{lambda+lambda_var,mu_f}{lambda,mu_i}(Op),
# # for nu_min <= mu_i,mu_f <= nu_max.
# # rbs_op is a list of symbolic names of the "basic" Radial_Operators
# #     Radial_b2, Radial_bm2, Radial_D2b, Radial_bDb,
# #     Radial_b,  Radial_bm, Radial_Db,
# #     Radial_S0, Radial_Sp, Radial_Sm,
# # (for beta^2; 1/beta^2; d^2/d(beta)^2; beta*d/d(beta);
# #  beta; 1/beta; d/d(beta); S0; S+; S-; respectively).
#
# # The result might need evalf operating on it to ensure that the returned
# # matrix has float entries.
# # The matrix elements of the result are analytic (exact expressions
# # involving surds) unless anorm or lambda are floats, or the parity
# # of the operator rbs_op is opposite to that of lambda_var,
# # in which cases the matrix elements might be a mix of floats and surds.
#
# # This procedure might, via RepRadialshfs_Prod, eventually call any
# # of the procedures
# #      RepRadial, RepRadial_param, RepRadial_bS_DS,
# #      Matrix_sqrt and Matrix_sqrtInv,
# # each of which uses a remember option.
# # We provide two versions, the first of which clears those remember table:
# # this is the one described in the manual (it is called only by ME_Radial
# # in this code.)
# # Note that they use Parse_RadialOp_List and Lambda_RadialOp_List below.
#
# # Implementation details:
# # The list rbs_op is parsed to split it up (using the procedure
# # Parse_RadialOp_List) into sequences of operators of the form
# # (beta^K * d/d(beta)^T) and S+, S-, S0.
# # Then, the variation lambda_var in lambda is split (using the
# # procedure Lambda_RadialOp_List) amongst these operators
# # (an extra operator 1 might get prepended at this point).
# # The representations of the operators with these lambda
# # variations is then obtained using RepRadialshfs_Prod
# # (this gets reps for S+, S-, S0 directly, but calls
# # RepRadial_bS_DS for (beta^K * d/d(beta)^T) ).
# # If lambda_var is of the same parity as rbs_op, then
# # the result will be analytic (however truncation effects
# # during matrix multiplication might affect the accuracy of the
# # outlying matrix elements). Otherwise, somewhere along the
# # line, a matrix square root is taken and this results in
# # floating point matrix elements, or combinations of such and surds.
#
#
# RepRadial_Prod:=proc(rbs_op::list, anorm::algebraic,
#                           lambda::algebraic, lambda_var::integer,
#                           nu_min::nonnegint, nu_max::nonnegint,
#                           nu_lap::nonnegint:=0,$)
#     local parsed_ops,lambda_shfs,rep,nu_min_shift:
#
#     if evalf(lambda)<=0 then
#        error("Non-positive lambda value %1",lambda):
#     elif evalf(lambda+lambda_var)<=0 then
#        error("Non-positive lambda value %1",lambda+lambda_var):
#     fi:
#
#     # parse into a list of [K,T] and S ops (S=0,+1,-1)
#
#     parsed_ops:=Parse_RadialOp_List(rbs_op):
#
#     # assign lambda shifts to each of [K,T] and S.
#
#     lambda_shfs:=Lambda_RadialOp_List(parsed_ops,lambda_var):
#
#     # if resulting list is one larger than given, then need to
#     # prepend or append a [0,0] operator depending on whether
#     # the extra variation is positive or negative
#
#     if nops(lambda_shfs)>nops(parsed_ops) then
#       if lambda_shfs[1]>0 then
#         parsed_ops:=[ [0,0], op(parsed_ops) ]:
#       else
#         parsed_ops:=[ op(parsed_ops), [0,0] ]:
#         lambda_shfs:=[op(2..-1,lambda_shfs),lambda_shfs[1]]:
#       fi:
#     fi:
#
#     # the indices of the matrix must be extended by at most nu_lap in
#     # both directions
#
#     nu_min_shift:=min(nu_lap,nu_min):
#
#     # now find representation of this product, with given lambda_shifts
#
#     rep:=RepRadialshfs_Prod(parsed_ops,anorm,lambda,lambda_shfs,
#                                 nu_min-nu_min_shift,nu_max+nu_lap):
#
#     forget(RepRadial):
#     forget(RepRadial_param):
#     forget(RepRadialshfs_Prod):
#     forget(RepRadial_bS_DS):
#     forget(Matrix_sqrt):
#     forget(Matrix_sqrtInv):
#
#     # we need to return the matrix with index range nu_min..nu_max
#
#     if nu_lap=0 then
#       rep
#     else
#       SubMatrix(rep,1+nu_min_shift..1+nu_max-nu_min+nu_min_shift,
#                     1+nu_min_shift..1+nu_max-nu_min+nu_min_shift)
#     fi:
#
# end;
def RepRadial_Prod(rbs_op: list[Symbol], anorm: Expr,
                   lambdaa: Expr, lambda_var: int,
                   nu_min: nonnegint, nu_max: nonnegint,
                   nu_lap: nonnegint
                   ) -> Matrix:
    rep: Matrix = RepRadial_Prod_common(rbs_op, anorm, lambdaa, lambda_var, nu_min, nu_max, nu_lap)

    RepRadial.cache_clear()
    RepRadial_param.cache_clear()
    RepRadialshfs_Prod.cache_clear()
    RepRadial_bS_DS.cache_clear()
    Matrix_sqrt.cache_clear()
    Matrix_sqrtInv.cache_clear()

    return rep


def RepRadial_Prod_common(rbs_op: list[Symbol], anorm: Expr,
                          lambdaa: Expr, lambda_var: int,
                          nu_min: nonnegint, nu_max: nonnegint,
                          nu_lap: nonnegint
                          ) -> Matrix:
    require_int('lambda_var', lambda_var)
    require_nonnegint_range('nu', nu_min, nu_max)
    require_int('nu_lap', nu_lap)

    if lambdaa.evalf() <= 0:
        raise ValueError(f'Non-positive lambda value {lambdaa}')
    elif (lambdaa + lambda_var).evalf() <= 0:
        raise ValueError(f'Non-positive lambda value {lambdaa + lambda_var}')

    parsed_ops: KTSOps = Parse_RadialOp_List(rbs_op)

    lambda_shfs: tuple[int, ...] = Lambda_RadialOp_List(parsed_ops, lambda_var)

    if len(lambda_shfs) > len(parsed_ops):
        if lambda_shfs[0] > 0:
            parsed_ops = (KTOp(0, 0),) + parsed_ops
        else:
            parsed_ops += (KTOp(0, 0),)
            lambda_shfs = lambda_shfs[1:] + (lambda_shfs[0],)

    nu_min_shift: int = min(nu_lap, nu_min)

    rep: Matrix = RepRadialshfs_Prod(parsed_ops, anorm, lambdaa, lambda_shfs,
                                     nu_min - nu_min_shift, nu_max + nu_lap)

    if nu_lap == 0:
        return rep
    else:
        return rep[nu_min_shift:(1 + nu_max - nu_min + nu_min_shift),
                   nu_min_shift:(1 + nu_max - nu_min + nu_min_shift)]


# # As above, but continues to remember everything.
#
# RepRadial_Prod_rem:=proc(rbs_op::list, anorm::algebraic,
#                           lambda::algebraic, lambda_var::integer,
#                           nu_min::nonnegint, nu_max::nonnegint,
#                           nu_lap::nonnegint:=0,$)
#     option remember;
#     local parsed_ops,lambda_shfs,nu_min_shift:
#
#     if evalf(lambda)<=0 then
#        error("Non-positive lambda value %1",lambda):
#     elif evalf(lambda+lambda_var)<=0 then
#        error("Non-positive lambda value %1",lambda+lambda_var):
#     fi:
#
#     # parse into a list of [K,T] and S ops (S=0,+1,-1)
#
#     parsed_ops:=Parse_RadialOp_List(rbs_op):
#
#     # assign lambda shifts to each of [K,T] and S.
#
#     lambda_shfs:=Lambda_RadialOp_List(parsed_ops,lambda_var):
#
#     # if resulting list is one larger than given, then need to
#     # prepend or append a [0,0] operator depending on whether
#     # the extra variation is positive or negative
#
#     if nops(lambda_shfs)>nops(parsed_ops) then
#       if lambda_shfs[1]>0 then
#         parsed_ops:=[ [0,0], op(parsed_ops) ]:
#       else
#         parsed_ops:=[ op(parsed_ops), [0,0] ]:
#         lambda_shfs:=[op(2..-1,lambda_shfs),lambda_shfs[1]]:
#       fi:
#     fi:
#
#     # now find representation of this product, with given lambda_shifts
#     # (we need to return the matrix with index range nu_min..nu_max)
#
#     if nu_lap=0 then
#       RepRadialshfs_Prod(parsed_ops,anorm,lambda,lambda_shfs,
#                                 nu_min,nu_max):
#     else
#       nu_min_shift:=min(nu_lap,nu_min):  # shift for lower index
#
#       SubMatrix(
#           RepRadialshfs_Prod(parsed_ops,anorm,lambda,lambda_shfs,
#                                 nu_min-nu_min_shift,nu_max+nu_lap),
#           1+nu_min_shift..1+nu_max-nu_min+nu_min_shift,
#           1+nu_min_shift..1+nu_max-nu_min+nu_min_shift)
#     fi:
#
# end;
@cache
def RepRadial_Prod_rem(rbs_op: list[Symbol], anorm: Expr,
                       lambdaa: Expr, lambda_var: int,
                       nu_min: nonnegint, nu_max: nonnegint,
                       nu_lap: nonnegint = 0
                       ) -> Matrix:

    return RepRadial_Prod_common(rbs_op, anorm, lambdaa, lambda_var, nu_min, nu_max, nu_lap)


# # The following parses a list of the basic radial operators
# #     Radial_b2, Radial_bm2, Radial_D2b, Radial_bDb,
# #     Radial_b,  Radial_bm, Radial_Db,
# #     Radial_S0, Radial_Sp, Radial_Sm,
# # (for beta^2; 1/beta^2; d^2/d(beta)^2; beta*d/d(beta);
# #  beta; 1/beta; d/d(beta); S0; S+; S-; respectively).
#
# # The return is a list of integers (-1,0 or 1) and pairs [K,T],
# # where the integers denote Radial_Sm, Radial_S0, Radial_Sp resp.,
# # and [K,T] denotes (beta^K * d/d(beta)^T).
#
# Parse_RadialOp_List:=proc(rs_op::list)
#
#   global Radial_Operators:
#   local i,T,K,POp_List,Pstate,idx:
#
#   POp_List:=[]:
#   T:=0:  # d^T/d(beta)^T
#   K:=0:  # (beta)^K
#
#   for i from nops(rs_op) to 1 by -1 do
#     if member(rs_op[i],[Radial_Sm,Radial_S0,Radial_Sp],'idx') then
#       if K<>0 or T>0 then
#         POp_List:=[ [K,T],op(POp_List) ]:   # write out [K,T]
#         K:=0:
#         T:=0:
#       fi:
#       POp_List:=[ idx-2,op(POp_List) ]:   # write out -1,0,1 for Sm,S0,Sp resp.
#     elif member(rs_op[i],[Radial_Db,Radial_D2b],'idx') then
#       if K<>0 then
#         POp_List:=[ [K,T],op(POp_List) ]:   # write out [K,T]
#         K:=0:
#         T:=0:
#       fi:
#       T:=T+idx:
#     elif rs_op[i]=Radial_bDb then
#       if K<>0 then
#         POp_List:=[ [K,T],op(POp_List) ]:   # write out [K,T]
#         T:=0:
#       fi:
#       T:=T+1:
#       K:=1:
#     elif member(rs_op[i],[Radial_b,Radial_b2],'idx') then
#       K:=K+idx:
#     elif member(rs_op[i],[Radial_bm,Radial_bm2],'idx') then
#       K:=K-idx:
#     else
#       error "operator %1 undefined", rs_op[i];
#     fi:
#   od:
#
#   if K<>0 or T>0 then
#     POp_List:=[ [K,T],op(POp_List) ]:   # write out any remaining [K,T]
#   fi:
#
#   POp_List:
#
# end:
def Parse_RadialOp_List(rs_op: list[Symbol]) -> KTSOps:
    POp_List: KTSOps = ()
    T: nonnegint = 0
    K: int = 0

    idx: int
    Radial_S_ops: list[Symbol] = [Radial_Sm, Radial_S0, Radial_Sp]
    Radial_D_ops: list[Symbol] = [Radial_Db, Radial_D2b]
    Radial_b_ops: list[Symbol] = [Radial_b, Radial_b2]
    Radial_bm_ops: list[Symbol] = [Radial_bm, Radial_bm2]
    for op in rs_op[::-1]:
        if op in Radial_S_ops:
            idx = 1 + Radial_S_ops.index(op)
            if K != 0 or T > 0:
                POp_List = (KTOp(K, T),) + POp_List
                K = 0
                T = 0
            POp_List = (SOp(idx - 2),) + POp_List
        elif op in Radial_D_ops:
            idx = 1 + Radial_D_ops.index(op)
            if K != 0:
                POp_List = (KTOp(K, T),) + POp_List
                K = 0
                T = 0
            T += idx
        elif op == Radial_bDb:
            if K != 0:
                POp_List = (KTOp(K, T),) + POp_List
                T = 0
            T += 1
            K = 1
        elif op in Radial_b_ops:
            idx = 1 + Radial_b_ops.index(op)
            K += idx
        elif op in Radial_bm_ops:
            idx = 1 + Radial_bm_ops.index(op)
            K -= idx
        else:
            raise ValueError(f'operator {op} undefined')

        if K != 0 or T > 0:
            POp_List = (KTOp(K, T),) + POp_List

    return POp_List


# # Takes a list obtained from above, and assigns a lambda variation
# # to each term, so that we get the correct overall lambda change.
# # The elements of rsp_op are either integers (-1,0 or 1) or pairs [K,T].
# #
# # The returned list is usually the same size as that passed.
# # Otherwise, the returned list will be one longer, with the
# # first element corresponding to an extra [0,0] (i.e. identity op)
# # that should be prepended or appended to the list being passed.
#
# # This is implemented by partitioning lambda_var amongst the elements
# # of rsp_op, each of which has a nominal maximal value which is 0
# # for the integers (-1,0 or 1) and (|K|+T) for pairs [K,T].
# # We permit at most only one value exceeding the nominal maximal
# # value, and at most one that is of opposite parity.
# # The parity violation is in the leftmost possible position,
# # while the violation over the max is leftmost for lambda_var>0 and
# # rightmost for lambda_var<0.
#
# # Beware that having lambda variation on the Sm, S0, Sp operators is
# # open to confusion in that it doesn't change the lambda of the
# # SU(1,1) operators.
#
#
# Lambda_RadialOp_List:=proc(rsp_op::list,lambda_var::integer)
#   local i,n,var,oddin,max_vars,max_count,odd_vars,odd_count,
#         lambda_rem,lambda_list:
#
#   lambda_rem:=abs(lambda_var):
#   n:=nops(rsp_op):
#   lambda_list:=[0$n]:   # variations to be determined: initially all 0.
#   max_vars:=[0$n]:      # nominal maximal variations: determined in loop below
#
#   for i to n do
#     if type(rsp_op[i],list(integer)) then
#       max_vars[i]:=abs(rsp_op[i][1])+rsp_op[i][2]:
#     elif not type(rsp_op[i],integer) then
#       error "operator %1 undefined", rsp_op[i];
#     fi:
#   od:
#
#   max_count:=add(i,i in max_vars):
#   odd_vars:=map(irem,max_vars,2):  # take remainders mod 2
#   odd_count:=add(i,i in odd_vars): # number of odd entries
#   # set position of first odd (only needed for odd difference)
#   if type(lambda_rem-max_count,even) or not member(1,odd_vars,'oddin') then
#     oddin:=0
#   fi:
#
#   if lambda_rem<odd_count then
#     # set all odd entries to +/- 1 to get sum to be close to lambda_rem
#     lambda_list:=odd_vars:  # initially set all odd positions to 1
#     # then change first few to -1
#     for i to n while lambda_rem<odd_count do
#       if lambda_list[i]=1 then
#         lambda_list[i]:=-1:
#         odd_count:=odd_count-2:
#       fi:
#     od:
#
#     # if difference is odd, then need to set first odd position var to zero.
#
#     if oddin>0 then
#       lambda_list[oddin]:=0:
#     fi:
#
#     # entries in lambda_list here now add up to odd count.
#
#     # There is a small benefit in working from left to right above,
#     # in that if a d/d(beta) precedes a beta, they appear in rsp_op
#     # in separate terms. If lambda_var is 0, then the first gets
#     # -1 and the second +1. The resulting matrix for beta is
#     # then upper diagonal and the natural truncation in the product
#     # automatically gives the correct result.
#
#   elif lambda_rem<max_count then
#     lambda_list:=odd_vars:  # initially set all odd positions to 1
#     lambda_rem:=lambda_rem-odd_count:
#     for i to n while lambda_rem>0 do
#       # ensure we only add even values to each (perhaps 1 too much)
#       var:=2*iquo(min(lambda_rem+1,max_vars[i]-odd_vars[i]),2):
#       lambda_list[i]:=lambda_list[i]+var:
#       lambda_rem:=lambda_rem-var:
#     od:
#
#     if lambda_rem<0 then # 1 too many added, but no max is exceeded
#       if oddin>0 then
#         lambda_list[oddin]:=lambda_list[oddin]-1:
#       else # remove 1 from previous addition
#         lambda_list[i-1]:=lambda_list[i-1]-1:
#       fi
#     fi:
#
#   else
#     # put all values at maximum, with any excess going on the
#     # first, although if that excess is odd, increase it by 1
#     # and decrease the first odd maximum by 1.
#     lambda_list:=max_vars:
#     lambda_rem:=lambda_rem-max_count:
#     if oddin>0 then
#       # reduce first odd case by 1 (making lambda_rem even)
#       lambda_list[oddin]:=lambda_list[oddin]-1:
#       lambda_rem:=lambda_rem+1:
#     fi:
#     if lambda_rem>0 then # deal with excess lambda variation
#       if lambda_var>0 and n>0 and type(rsp_op[1],list(integer)) then
#         # put remaining lambda_rem on first, which is [K,T]
#         lambda_list[1]:=lambda_list[1]+lambda_rem:
#       elif lambda_var<0 and n>0 and type(rsp_op[n],list(integer)) then
#         # put remaining lambda_rem on last, which is [K,T]
#         lambda_list[n]:=lambda_list[n]+lambda_rem:
#       else # extend list at start (calling routine needs to test this)
#         lambda_list:=[lambda_rem,op(lambda_list)]:
#       fi:
#     fi:
#   fi:
#
#   if lambda_var>=0 then
#     lambda_list:
#   else
#     -lambda_list:
#   fi:
#
# end:
def Lambda_RadialOp_List(rsp_op: KTSOps, lambda_var: int) -> tuple[int, ...]:
    require_int('lambda_var', lambda_var)

    lambda_rem: int = abs(lambda_var)
    n: int = len(rsp_op)
    lambda_list: list[int] = [0] * n
    max_vars: list[int] = [0] * n

    for i0, op in enumerate(rsp_op):
        if isinstance(op, KTOp):
            K = op.K
            T = op.T
            max_vars[i0] = abs(K) + T
        elif not isinstance(op, SOp):
            raise ValueError(f'operator {op} undefined')

    max_count: int = sum(max_vars)
    odd_vars: list[int] = [irem(max_var, 2) for max_var in max_vars]
    odd_count: int = sum(odd_vars)

    oddin: int = 0
    if is_odd(lambda_rem - max_count) and 1 in odd_vars:
        oddin = 1 + odd_vars.index(1)

    if lambda_rem < odd_count:
        lambda_list = odd_vars.copy()
        for i0 in range(n):
            if lambda_rem >= odd_count:
                break
            if lambda_list[i0] == 1:
                lambda_list[i0] = -1
                odd_count -= 2

        if oddin > 0:
            lambda_list[oddin - 1] = 0

        # TODO: The following assertion failed. Why? - Add logging.
        # assert sum(lambda_list) == odd_count

    elif lambda_rem < max_count:
        lambda_list = odd_vars.copy()
        lambda_rem -= odd_count
        for i0 in range(n):
            if lambda_rem <= 0:
                break
            var: int = 2 * iquo(min(lambda_rem + 1, max_vars[i0] - odd_vars[i0]), 2)
            lambda_list[i0] += var
            lambda_rem -= var

        if lambda_rem < 0:
            if oddin > 0:
                lambda_list[oddin - 1] -= 1
            else:
                lambda_list[i0] -= 1

    else:
        lambda_list = max_vars.copy()
        lambda_rem -= max_count
        if oddin > 0:
            lambda_list[oddin - 1] -= 1
            lambda_rem += 1

        if lambda_rem > 0:
            if lambda_var > 0 and n > 0 and isinstance(rsp_op[0], KTOp):
                lambda_list[0] += lambda_rem
            elif lambda_var < 0 < n and isinstance(rsp_op[-1], KTOp):
                lambda_list[-1] += lambda_rem
            else:
                lambda_list = [lambda_rem] + lambda_list

    if lambda_var >= 0:
        return tuple(lambda_list)
    else:
        return tuple([-lambdaa for lambdaa in lambda_list])


# # The following procedure is similar to RepRadial_Prod above, but is able to
# # represent linear combinations of products of the basic radial operators.
# # The arguments anorm, lambda, lambda_var, nu_min, nu_max are same as above,
# # the first, rlc_op, is of the form
# #         [ [coeff1,rs_op1], [coeff2,rs_op2], ...],
# # where rs_op1, rs_op2 are lists of basic radial operators, as in the first
# # argument above.
# # The return value is a Matrix, whose elements might need to be acted
# # upon by evalf to ensure that they are floats.
#
# # This procedure might eventually call any of the procedures
# #   RepRadial_Prod_rem, RepRadialshfs_Prod, RepRadial,
# #   RepRadial_param, Matrix_sqrt, Matrix_sqrtInv,
# # each of which uses a remember option.
#
# # We provide two versions, which differ only in that the first clears the
# # remember tables, while the second doesn't.
# # The first is the one described in the manual: it is not called by
# # anything in this code. The second is called only by the procedures
# # RepXspace_Pi, RepXspace_PiPi and RepXspace_PiqPi.
#
# RepRadial_LC:=proc(rlc_op::list(list), anorm::algebraic,
#                           lambda::algebraic, lambda_var::integer,
#                           nu_min::nonnegint, nu_max::nonnegint,
#                           nu_lap::nonnegint:=0)
#     local i,n,Mat;
#
#   n:=nops(rlc_op);
#
#   if n=0 then
#     Mat:=Matrix(nu_max-nu_min+1);  #Null matrix
#   else
#     Mat:=MatrixScalarMultiply(
# #            evalf(RepRadial_Prod_rem(rlc_op[1][2],anorm,
# #                                   lambda,lambda_var,nu_min,nu_max,nu_lap)),
#             RepRadial_Prod_rem(rlc_op[1][2],anorm,
#                                    lambda,lambda_var,nu_min,nu_max,nu_lap),
#             rlc_op[1][1]);
#     for i from 2 to n do
#       MatrixAdd(Mat,         # removed assignment (4/8/2015: unnecessary)
# #            evalf(RepRadial_Prod_rem(rlc_op[i][2],anorm,
# #                                   lambda,lambda_var,nu_min,nu_max,nu_lap)),
#             RepRadial_Prod_rem(rlc_op[i][2],anorm,
#                                    lambda,lambda_var,nu_min,nu_max,nu_lap),
#             1,rlc_op[i][1],inplace);
#     od:
#   fi:
#
#   # forget all possible remembered procedures this has called:
#
#   forget(RepRadial_Prod_rem):
#   forget(RepRadialshfs_Prod):
#   forget(RepRadial):
#   forget(RepRadial_param):
#   forget(Matrix_sqrt):
#   forget(Matrix_sqrtInv):
#
#   Mat;
# end:
def RepRadial_LC(rlc_op: list[tuple[Expr, KTSOps]], anorm: Expr,
                 lambdaa: Expr, lambda_var: int,
                 nu_min: nonnegint, nu_max: nonnegint,
                 nu_lap: nonnegint = 0
                 ) -> Matrix:
    M: Matrix = RepRadial_LC_common(rlc_op, anorm, lambdaa, lambda_var, nu_min, nu_max, nu_lap)

    RepRadial_Prod_rem.cache_clear()
    RepRadialshfs_Prod.cache_clear()
    RepRadial.cache_clear()
    RepRadial_param.cache_clear()
    Matrix_sqrt.cache_clear()
    Matrix_sqrtInv.cache_clear()

    return M


def RepRadial_LC_common(rlc_op: list[tuple[Expr, KTSOps]], anorm: Expr,
                        lambdaa: Expr, lambda_var: int,
                        nu_min: nonnegint, nu_max: nonnegint,
                        nu_lap: nonnegint = 0
                        ) -> Matrix:
    require_int('lambda_var', lambda_var)
    require_nonnegint_range('nu', nu_min, nu_max)
    require_nonnegint('nu_lap', nu_lap)

    n: int = len(rlc_op)

    M: Matrix
    if n == 0:
        M = zeros(nu_max - nu_min + 1)
    else:
        coeff, op = rlc_op[0]
        M = RepRadial_Prod_rem(op, anorm, lambdaa, lambda_var, nu_min, nu_max, nu_lap) * coeff

        for coeff, op in rlc_op[1:]:
            M += RepRadial_Prod_rem(op, anorm, lambdaa, lambda_var, nu_min, nu_max, nu_lap) * coeff

    return M


# # As above, but everything is remembered.
#
# RepRadial_LC_rem:=proc(rlc_op::list(list), anorm::algebraic,
#                           lambda::algebraic, lambda_var::integer,
#                           nu_min::nonnegint, nu_max::nonnegint,
#                           nu_lap::nonnegint:=0)
#     option remember;
#     local i,n,Mat;
#
#   n:=nops(rlc_op);
#
#   if n=0 then
#     Mat:=Matrix(nu_max-nu_min+1);  #Null matrix
#   else
#     Mat:=MatrixScalarMultiply(
#             evalf(RepRadial_Prod_rem(rlc_op[1][2],anorm,
#                                    lambda,lambda_var,nu_min,nu_max,nu_lap)),
#             rlc_op[1][1]);
#     for i from 2 to n do
#       MatrixAdd(Mat,         # removed assignment (4/8/2015: unnecessary)
#             evalf(RepRadial_Prod_rem(rlc_op[i][2],anorm,
#                                    lambda,lambda_var,nu_min,nu_max,nu_lap)),
#             1,rlc_op[i][1],inplace);
#     od:
#   fi:
#
#   Mat;
# end:
@cache
def RepRadial_LC_rem(rlc_op: list[tuple[Expr, KTSOps]], anorm: Expr,
                     lambdaa: Expr, lambda_var: int,
                     nu_min: nonnegint, nu_max: nonnegint,
                     nu_lap: nonnegint = 0) -> Matrix:

    return RepRadial_LC_common(rlc_op, anorm, lambdaa, lambda_var, nu_min, nu_max, nu_lap)
