"""8. Procedures that aid the production of the data for the particular Hamiltonians considered in [RWC2009]."""

import math

from typing import Any
from sympy import S, Expr, sqrt, Symbol, nsolve, solveset, Reals, Set, FiniteSet
from scipy.optimize import root_scalar, RootResults

from acmpy.compat import IntFloatExpr, nonnegint, require_nonnegint
from acmpy.internal_operators import ACM_Hamiltonian, OperatorSum
from acmpy.globals import lambda_davi_fun, lambda_sho_fun, LambdaFunction


# ###########################################################################
# ####-------- Aiding calculations for Hamiltonians in [RWC2009] --------####
# ###########################################################################
#
# # Here we provide procedures that may be used instead of
# # ones above to calculate for Hamiltonians considered in [RWC2009].
#
# # The following procedure RWC_Ham obtains the ACM encoding of Hamiltonians
# # of the RWC form given in (B12) (see also (89) of [RWC2009], with
# # c1=1-2*alpha and c2=alpha, and eqns. (4.230) & (4.220) of [RowanWood].)
#
# RWC_Ham:=(B,c1,c2,chi,kappa)->
#   ACM_Hamiltonian(-1/2/B,0,B*c1/2,B*c2/2,0,-chi,0,0,0,kappa);
def RWC_Ham(B: IntFloatExpr, c1: IntFloatExpr, c2: IntFloatExpr, chi: IntFloatExpr, kappa: IntFloatExpr
            ) -> OperatorSum:
    B = S(B)
    c1 = S(c1)
    c2 = S(c2)
    chi = S(chi)
    kappa = S(kappa)

    return ACM_Hamiltonian(-1 / (2 * B), 0, B * c1 / 2, B * c2 / 2, 0, -chi, 0, 0, 0, kappa)


# # The following procedure RWC_expt gives the expectation value of the above
# # Hamiltonian on the |(anorm,lambda0)0;0100> basis state, given by (B16).
# # (Note that (76) of [RWC2009] contains typos.)
#
# RWC_expt:=proc(B::constant,c1::constant,c2::constant,kappa::constant,
#                           anorm::constant,lambda0::constant,$)
#   local aa:
#
#   aa:=anorm^2:
#   aa*(4+9/(lambda0-1))/8/B + B*lambda0*c1/2/aa
#               + B*lambda0*(lambda0+1)*c2/2/aa^2 + kappa/3:
# end:
def RWC_expt(B: float, c1: float, c2: float, kappa: float,
             anorm: float, lambda0: float
             ) -> float:
    if anorm == 0:
        raise ValueError('anorm must not equal 0.')
    if lambda0 == 1:
        raise ValueError('lambda0 must not equal 1.')

    aa: float = anorm ** 2
    return aa * (4 + 9 / (lambda0 - 1)) / 8 / B + B * lambda0 * c1 / 2 / aa \
           + B * lambda0 * (lambda0 + 1) * c2 / 2 / aa ** 2 + kappa / 3


# # The following procedure RWC_expt_link gives the same expectation value
# # (B16) as that above, but lambda0 is assumed to depend on anorm through
# # the function RWC_dav (see below).
#
# RWC_expt_link:=proc(B::constant,c1::constant,c2::constant,kappa::constant,
#                           anorm::constant,$)
#   RWC_expt(_passed,evalf(RWC_dav(c1,c2,anorm))):
# end:
def RWC_expt_link(B: float, c1: float, c2: float, kappa: float, anorm: float
                  ) -> float:
    return RWC_expt(B, c1, c2, kappa, anorm, RWC_dav(c1, c2, anorm))


# # The following procedure RWC_dav calculates lambda0 from anorm
# # (and c1 and c2) using (B11) via (B15).
#
# RWC_dav:=proc(c1::constant,c2::constant,anorm::constant,v::nonnegint:=0,$)
#   lam_dav(anorm,beta_dav(c1,c2),v)
# end:
def RWC_dav(c1: float, c2: float, anorm: float, v: nonnegint = 0
            ) -> float:
    return lam_dav(anorm, beta_dav(c1, c2), v)


# # The following calculates lambda_v using (B7) - or using
# # B11 if the final argument is not given (it defaults to 0).
#
# lam_dav:=proc(a::constant,beta0::constant,v::nonnegint:=0,$)
#     1+sqrt( (v+3/2)^2 + a^4*beta0^4 )
# end:
def lam_dav(a: float, beta0: float, v: nonnegint = 0
            ) -> float:
    return 1 + math.sqrt((v + 1.5) ** 2 + (a * beta0) ** 4)


# # The following calculates beta_0 using (B15)
#
# beta_dav:=proc(c1::constant,c2::constant,$)
#   if evalf(c1)>=0 then
#     0
#   else
#     sqrt(-c1/c2/2)
#   fi;
# end:
def beta_dav(c1: float, c2: float
             ) -> float:
    return 0 if c1 >= 0 else sqrt(-c1 / (c2 * 2))


# # The following procedure RWC_alam returns values of the ACM parameters
# # (anorm,lambda), which are "optimal" in the cases of the RWC Hamiltonians.
# # This seeks the minimal value of RWC_expt, given above, by solving
# # for a turning point.
# # The fourth parameter is for seniority v, which is 0 for the
# # analysis given in [WR2015], but in the case of more general v,
# # (for L=0 (so 3\v) and no spherical dependence in the potential),
# # the 9/4 factor in the first term of (B.16) is replaced by
# # the more general (v+3/2)^2.
#
# RWC_alam:=proc(B::constant,c1::constant,c2::constant,v::nonnegint:=0,$)
#   local RWC1,RWC2,muf,aa0,vshft,A;
#
#   vshft:=(2*v+3)^2:  # This is 9 for the v=0 case.
#
#   if evalf(c1)<0 then
#           # Here lambda is a function of aa (i.e. a^2).
#           # There is always one positive solution in this case
#           # (in fact, I've never found other real solns).
#
#     # We use mu=2(lambda-1) where lambda is given by (B11) via (B15).
#
#     muf:=(aa) -> sqrt( vshft + (aa*c1/c2)^2 ):
#
#     # The following is the derivative of (B16) noting that
#     # d(mu)/d(aa)=aa*(c1/c2)^2/mu.  But multiplied by 4*aa^3*B*mu.
#
#     RWC2:=(aa,mu) -> (c1/c2)^2 * (-vshft*aa^5/mu^2
#                                     + aa^3*B^2*c1 + aa^2*B^2*c2*(mu+3))
#                        + aa^3*(2*mu+vshft)
#                        - B^2*mu*(mu+2)*(aa*c1+c2*(mu+4)):
#
#     aa0:=max(fsolve(RWC2(A,muf(A))=0,A)):
#     return [sqrt(aa0),1+muf(aa0)/2]:
#
#   else   # (Here lambda is constant)
#          # There is always 1 positive solution in this case
#          # (fsolve produces real solns.) and possibly two others that
#          # are negative. Use max to exclude them.
#
#     RWC1:=(aa) -> aa^3 - B^2*c1*aa - (2*v+7)*B^2*c2:
#
#     aa0:=max(fsolve(RWC1(A)=0,A)):
#     return [sqrt(aa0),2.5]:
#   fi:
#
# end:
def vshftf(v: nonnegint) -> int:
    return (2 * v + 3) ** 2


def muf(A: Expr, c1: float, c2: float, v: nonnegint) -> Expr:
    vshft: int = vshftf(v)
    return sqrt(vshft + (A * c1 / c2) ** 2)


def RWC1(A: Expr, B: float, c1: float, c2: float, v: nonnegint = 0) -> Expr:
    return A ** 3 - B ** 2 * c1 * A - (2 * v + 7) * B ** 2 * c2


def RWC2(A: Expr, mu: Expr, B: float, c1: float, c2: float, v: nonnegint = 0) -> Expr:
    vshft: int = vshftf(v)
    return (c1 / c2) ** 2 * (-vshft * A ** 5 / mu ** 2
                             + A ** 3 * B ** 2 * c1
                             + A ** 2 * B ** 2 * c2 * (mu + 3)) \
           + A ** 3 * (2 * mu + vshft) \
           - B ** 2 * mu * (mu + 2) * (A * c1 + c2 * (mu + 4))


class RwcOptimizationError(Exception):
    """Raised when RWC_alam() is unable to find optimum values for (a, lambda)."""

    B: float
    c1: float
    c2: float
    v: nonnegint
    result: Any

    def __init__(self, B: float, c1: float, c2: float, v: nonnegint, result: Any):
        self.B = B
        self.c1 = c1
        self.c2 = c2
        self.v = v
        self.result = result
        super().__init__('Unable to find optimum values for (a, lambda)')


def RWC_alam(B: float, c1: float, c2: float, v: nonnegint = 0
             ) -> tuple[float, float]:
    require_nonnegint('v', v)

    if c1 >= 0.0:
        return RWC_alam_clam(B, c1, c2, v)

    assert c1 < 0.0
    if c2 <= 0.0:
        raise ValueError(f'c2 must be positive when c1 is negative: c1={c1}, c2={c2}')
    A: Symbol = Symbol('A', real=True, positive=True)
    mu_A: Expr = muf(A, c1, c2, v)
    F2_A: Expr = RWC2(A, mu_A, B, c1, c2, v)

    def F2(A_value: float) -> float:
        return float(F2_A.subs(A, A_value))

    # find the bracket interval [0, A_pos] where F2(A) changes sign

    # F2(0.0) is negative
    # F2(0.0) = -B ** 2 * c2 * (2 * v + 3) * (2 * v + 5) * (2 * v + 7)
    assert F2(0.0) < 0.0

    # F2(A) becomes positive for large A
    # F2(A) -> (2 * abs(c1) / c2) * A ** 4
    A_pos: float = 1.0
    while F2(A_pos) <= 0:
        A_pos *= 2.0
    assert F2(A_pos) > 0.0

    result: RootResults = root_scalar(F2, bracket=(0.0, A_pos))
    if not result.converged:
        raise RwcOptimizationError(B, c1, c2, v, result)

    aa0: float = result.root

    return math.sqrt(aa0), float(1 + muf(S(aa0), c1, c2, v) / 2)


# # The following procedure RWC_alam36 is a simplified algorithm
# # for obtaining "optimal" values of (anorm,lambda), obtained by
# # matching second derivatives at the turning point of the potential.
# # This only gives good results in certain cases.
#
# RWC_alam36:=proc(B::constant,c1::constant,c2::constant,$)
#   local RWC1,RWC2,muf,aa0;
#
#   if evalf(c1)<0 then
#
#     return evalf([sqrt(sqrt(-B^2*c1/2)),1+sqrt(36+B^2*c1^4/c2^2)/4]):
#
#   else
#
#     return evalf([sqrt(sqrt(B*c1/4)),2.5]):
#
#   fi:
#
# end:
def RWC_alam36(B: float, c1: float, c2: float
               ) -> tuple[float, float]:
    if c1 < 0:

        return math.sqrt(math.sqrt(-B ** 2 * c1 / 2)), (1 + math.sqrt(36 + B ** 2 * c1 ** 4 / c2 ** 2) / 4)

    else:

        return math.sqrt(math.sqrt(B * c1 / 4)), 2.5


# # The following procedure RWC_alam_clam is another alternative that
# # returns values of the ACM parameters (anorm,lambda), which are
# # obtained from the minimal value of the expectation value of RWC_expt,
# # given above, with lambda assumed to take the constant value of 2.5
#
# RWC_alam_clam:=proc(B::constant,c1::constant,c2::constant,$)
#   local RWC1,RWC2,muf,aa0,A;
#
#     RWC1:=(aa) -> aa^3 - B^2*c1*aa - 7*B^2*c2:
#     aa0:=max(fsolve(RWC1(A)=0,A)):
#     return [sqrt(aa0),2.5]:
#
# end:
def A0_case1(B: float, c1: float) -> float:
    if B <= 0:
        raise ValueError(f'B must be positive: {B}')
    if c1 <= 0:
        raise ValueError(f'c1 must be positive: {c1}')
    return B * math.sqrt(c1)


def A0_case2_approx(B: float, c2: float, v: nonnegint) -> float:
    if B <= 0:
        raise ValueError(f'B must be positive: {B}')
    if c2 <= 0:
        raise ValueError(f'c2 must be positive: {c2}')
    require_nonnegint('v', v)

    return (c2 * B ** 2 * (2 * v + 7)) ** (1 / 3)


def A0_case3_approx(B: float, c1: float, c2: float, v: nonnegint) -> float:
    if B <= 0:
        raise ValueError(f'B must be positive: {B}')
    if c1 >= 0:
        raise ValueError(f'c1 must be negative: {c1}')
    if c2 <= 0:
        raise ValueError(f'c2 must be positive: {c2}')
    require_nonnegint('v', v)

    return math.sqrt(B * c2) * ((2 * v + 3) * (2 * v + 5) * (2 * v + 7) / (-2 * c1)) ** (1 / 4)


def RWC_alam_clam(B: float, c1: float, c2: float, v: nonnegint = 0
                  ) -> tuple[float, float]:

    A: Symbol = Symbol('A', real=True, positive=True)
    F1: Expr = RWC1(A, B, c1, c2, v)
    A0_set: Set = solveset(F1, A, domain=Reals)
    assert isinstance(A0_set, FiniteSet)
    A0_pos = [float(A0) for A0 in A0_set if A0 > 0]

    # assume that the smallest positive zero if the one that minimizes energy
    aa0: float = A0_pos[0]

    return math.sqrt(aa0), 2.5


# # The following procedure RWC_alam_fun returns a triple
# #                 [anorm,lambda0,lambda_fun]
# # where anorm and lambda0 are "optimal" values obtained as in
# # RWC_alam above, and lambda_fun is a procedure that takes an argument
# # v that gives the (optimal) value of lambda(v)-lambda(0),
# # an integer of same parity as v.
# # This is not used elsewhere.
#
# RWC_alam_fun:=proc(B::constant,c1::constant,c2::constant,$)
#   local RWC1,RWC2,muf,aa0,A;
#
#   if evalf(c1)<0 then
#           # Here lambda is a function of aa (i.e. a^2).
#           # There is always one positive solution in this case
#           # (in fact, I've never found other real solns).
#
#     # We use mu=2(lambda-1) where lambda is given by (B11) via (B15).
#
#     muf:=(aa) -> sqrt( 9+ (aa*c1/c2)^2 ):
#
#     # The following is the derivative of (B16) noting that
#     # d(mu)/d(aa)=aa*(c1/c2)^2/mu.  But multiplied by 4*A^3*B*mu.
#
#     RWC2:=(aa,mu) -> (c1/c2)^2 * (-9*aa^5/mu^2
#                                     + aa^3*B^2*c1 + aa^2*B^2*c2*(mu+3))
#                        + aa^3*(2*mu+9)
#                        - B^2*mu*(mu+2)*(aa*c1+c2*(mu+4)):
#
#     aa0:=max(fsolve(RWC2(A,muf(A))=0,A)):
#     return [sqrt(aa0),1+muf(aa0)/2,lambda_davi_fun((aa0*c1/c2/2)^2)]:
#
#   else   # (Here lambda is constant)
#          # There is always 1 positive solution in this case
#          # (fsolve produces real solns.) and possibly two others that
#          # are negative. Use max to exclude them.
#
#     RWC1:=(aa) -> aa^3 - B^2*c1*aa - 7*B^2*c2:
#
#     aa0:=max(fsolve(RWC1(A)=0,A)):
#     return [sqrt(aa0),2.5,lambda_sho_fun]:
#   fi:
#
# end:
def RWC_alam_fun(B: float, c1: float, c2: float
                 ) -> tuple[float, float, LambdaFunction]:
    a0: float
    lam: float
    a0, lam = RWC_alam(B, c1, c2)

    if c1 >= 0:
        return a0, lam, lambda_sho_fun

    assert c1 < 0
    aa0: float = a0 ** 2
    return a0, lam, lambda_davi_fun((aa0 * c1 / (c2 * 2)) ** 2)
