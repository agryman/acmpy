"""5. Procedures that obtain the internal representation of operators."""

from functools import cache
from typing import Optional

from sympy import Symbol, pi, sqrt, Integer, Rational, Expr, \
    S, factorial, Matrix, diag, eye

from acmpy.compat import nonnegint, require_nonnegint, is_odd, IntFloatExpr
from acmpy.so5_so3_cg import CG_SO5r3
from acmpy.spherical_space import lbsSO5r3_rngVvarL, dimSO3, dimSO5r3_rngVvarL, SO5SO3Label, \
    SpHarm_Table, SpHarm_Operators, \
    SpHarm_112, \
    SpHarm_310, SpHarm_313, SpHarm_314, SpHarm_316, \
    SpHarm_512, SpHarm_514, SpHarm_515, SpHarm_516, SpHarm_517, SpHarm_518, SpHarm_51A, \
    SpHarm_610, \
    SpDiag_sqLdiv, SpDiag_sqLdim
from acmpy.radial_space import Radial_b, Radial_b2, Radial_bm, Radial_bm2, \
    Radial_Db, Radial_D2b, \
    Radial_Sm, Radial_S0, Radial_Sp

OperatorProduct = tuple[Expr, tuple[Symbol, ...]]
OperatorSum = tuple[OperatorProduct, ...]

# # The four operators
# #       pi, [pi x pi]_{v=2,L=2}, [pi x pi]_{v=2,L=L}, [q x pi x pi]_{v=3,L=0}
# # intrinsically affect the whole product space:
#
# Xspace_Operators:=[ Xspace_Pi, Xspace_PiPi2, Xspace_PiPi4, Xspace_PiqPi ]:
Xspace_Pi: Symbol = Symbol('Xspace_Pi', commutative=False)
Xspace_PiPi2: Symbol = Symbol('Xspace_PiPi2', commutative=False)
Xspace_PiPi4: Symbol = Symbol('Xspace_PiPi4', commutative=False)
Xspace_PiqPi: Symbol = Symbol('Xspace_PiqPi', commutative=False)
Xspace_Operators: tuple[Symbol, ...] = (Xspace_Pi, Xspace_PiPi2, Xspace_PiPi4, Xspace_PiqPi)


# # The following provide useful conversion factors from the SO(5)
# # spherical harmonics to more physically relevant operators;
# # see Table IV.
# # (Note that often (e.g. by RepSO5_Y_rem), the operator will be represented
# # with the 4*Pi already incorporated - and the FourPi should be cancelled).
# # Note that evalf will need to be used somewhere further down the line
# # to convert from these symbolic values to actual floating point values.
#
# FourPi:=4*Pi;
"""Maple Pi corresponds to SymPy pi."""
FourPi: Expr = 4 * pi

# Convert_112:=FourPi/sqrt(15);       # multiplies Y112 to get Q
# Convert_212:=-FourPi*sqrt(2/105);   # multiplies Y212 to get [QxQ]_(L=4)
# Convert_310:=FourPi/3;              # multiplies Y310 to get cos(3*gamma)
# Convert_316:=FourPi/3*sqrt(2/35);   # multiplies Y316 to get [QxQxQ]_(L=6)
# Convert_610:=2*FourPi/sqrt(15);     # multiplies Y610 to get [3*cos(3*gamma)+1]
# Convert_red:=1/FourPi;              # converts ME_SO5red to <v3|||v2|||v1>
Convert_112: Expr = FourPi / sqrt(Integer(15))
Convert_212: Expr = -FourPi * sqrt(Rational(2, 105))
Convert_310: Expr = FourPi / 3
Convert_316: Expr = FourPi / 3 * sqrt(Rational(2, 35))
Convert_610: Expr = 2 * FourPi / sqrt(Integer(15))
Convert_red: Expr = 1 / FourPi

# # The following quad_op specifies, in internal format, the quadrupole
# # operator. quadRigid_op is more appropriate for rigid-beta models.
#
# quad_op:=[ [Convert_112, [Radial_b,SpHarm_112]] ]:
# quadRigid_op:=[ [Convert_112, [SpHarm_112]] ]:
"""Refer to: 7.3. Internal representation of Hamiltonians and other operators """
quad_op: OperatorSum = ((Convert_112, (Radial_b, SpHarm_112)),)
quadRigid_op: OperatorSum = ((Convert_112, (SpHarm_112,)),)


# ###########################################################################
# ################# Representations of spherical harmonics ##################
# ###########################################################################
#
# # The following procedure ME_SO5red returns the doubly reduced matrix
# # element <u|||w|||v>*4*Pi for SO(5) spherical harmonic tensor operators.
# # It uses (45).
# # The return value is algebraic and exact (and probably a surd).
#
# ME_SO5red:=proc(u::nonnegint,w::nonnegint,v::nonnegint)
#   local sigma,halfsigma;
#   if u+v<w or u+w<v or v+w<u or type(u+v+w,odd) then
#     RETURN(0);
#   fi:
#
#   sigma:=(v+w+u); halfsigma:=sigma/2;
#   (halfsigma+1)! / (halfsigma-u)! / (halfsigma-v)! / (halfsigma-w)!
#     * sqrt( (2*v+3) * (2*w+3) * (sigma+4) / (u+2) / (u+1)
#             * (sigma-2*u+1)! * (sigma-2*w+1)! * (sigma-2*v+1)! / (sigma+3)! );
# end:
def ME_SO5red(u: nonnegint, w: nonnegint, v: nonnegint) -> Expr:
    require_nonnegint('u', u)
    require_nonnegint('w', w)
    require_nonnegint('v', v)

    if u + v < w or u + w < v or v + w < u or is_odd(u + v + w):
        return S.Zero

    sigma: Expr = S(v + w + u)
    halfsigma: Expr = sigma / 2

    return factorial(halfsigma + 1) / \
           (factorial(halfsigma - u) * factorial(halfsigma - v) * factorial(halfsigma - w)) * \
           sqrt((2 * v + 3) * (2 * w + 3) * (sigma + 4) / (u + 2) / (u + 1) *
                factorial(sigma - 2 * u + 1) * factorial(sigma - 2 * w + 1) *
                factorial(sigma - 2 * v + 1) / factorial(sigma + 3))


# # The following nine functions are useful instances of the above,
# # with different normalisations: they provide SO(5) (doubly) reduced
# # matrix elements for Q and [QxQ]_(v=2) and [QxQxQ]_(v=3).
# # They may be obtained from ME_SO5red by using
# #     Q=4*Pi/sqrt(15) * Y_{112},
# #     [QxQ]^2_4=4*Pi*sqrt(2/105) * Y_{214}, and
# #     [QxQxQ]^3_6=4*Pi*sqrt(2/315) * Y_{316}
# # (we need to take care with different signs for
# #       [QxQ]^2_2=-4*Pi*sqrt(2/105) * Y_{212} and
# #       [QxQxQ]^3_0=-4*Pi*sqrt(2/315) * Y_{310} ).
#
# # The following gives <v+1|||Q|||v> and <v-1|||Q|||v>
#
# Qred_p1:=(v) -> sqrt((v+1)/(2*v+5)):
def Qred_p1(v: nonnegint) -> Expr:
    require_nonnegint('v', v)

    p: int = v + 1
    q: int = 2 * v + 5
    return sqrt(Rational(p, q))


# Qred_m1:=(v) -> sqrt((v+2)/(2*v+1)):
def Qred_m1(v: nonnegint) -> Expr:
    require_nonnegint('v', v)

    p: int = v + 2
    q: int = 2 * v + 1
    return sqrt(Rational(p, q))


# # The following gives <v+2|||QxQ|||v>, <v|||QxQ|||v> & <v-2|||QxQ|||v>
#
# QxQred_p2:=(v) -> sqrt((v+1)*(v+2)/(2*v+5)/(2*v+7)):
def QxQred_p2(v: nonnegint) -> Expr:
    require_nonnegint('v', v)

    p: int = (v + 1) * (v + 2)
    q: int = (2 * v + 5) * (2 * v + 7)
    return sqrt(Rational(p, q))


# QxQred_0:=(v)  -> sqrt(6*v*(v+3)/5/(2*v+1)/(2*v+5)):
def QxQred_0(v: nonnegint) -> Expr:
    require_nonnegint('v', v)

    p: int = 6 * v * (v + 3)
    q: int = 5 * (2 * v + 1) * (2 * v + 5)
    return sqrt(Rational(p, q))


# QxQred_m2:=(v) -> sqrt((v+1)*(v+2)/(2*v+1)/(2*v-1)):
def QxQred_m2(v: nonnegint) -> Expr:
    require_nonnegint('v', v)

    p: int = (v + 1) * (v + 2)
    q: int = (2 * v + 1) * (2 * v - 1)
    return sqrt(Rational(p, q))


# # The following gives <v+3|||QxQxQ|||v>, <v+1|||QxQxQ|||v>
# #                     <v-1|||QxQxQ|||v>, <v-3|||QxQxQ|||v>
#
# QxQxQred_p3:=(v) -> sqrt((v+1)*(v+2)*(v+3)/(2*v+5)/(2*v+7)/(2*v+9)):
def QxQxQred_p3(v: nonnegint) -> Expr:
    require_nonnegint('v', v)

    p: int = (v + 1) * (v + 2) * (v + 3)
    q: int = (2 * v + 5) * (2 * v + 7) * (2 * v + 9)
    return sqrt(Rational(p, q))


# QxQxQred_p1:=(v) -> 3*sqrt(v*(v+1)*(v+4)/7/(2*v+1)/(2*v+5)/(2*v+7)):
def QxQxQred_p1(v: nonnegint) -> Expr:
    require_nonnegint('v', v)

    p: int = v * (v + 1) * (v + 4)
    q: int = 7 * (2 * v + 1) * (2 * v + 5) * (2 * v + 7)
    return 3 * sqrt(Rational(p, q))


# QxQxQred_m1:=(v) -> 3*sqrt((v-1)*(v+2)*(v+3)/7/(2*v-1)/(2*v+1)/(2*v+5)):
def QxQxQred_m1(v: nonnegint) -> Expr:
    require_nonnegint('v', v)

    p: int = (v - 1) * (v + 2) * (v + 3)
    q: int = 7 * (2 * v - 1) * (2 * v + 1) * (2 * v + 5)
    return 3 * sqrt(Rational(p, q))


# QxQxQred_m3:=(v) -> sqrt(v*(v+1)*(v+2)/(2*v-3)/(2*v-1)/(2*v+1)):
def QxQxQred_m3(v: nonnegint) -> Expr:
    require_nonnegint('v', v)

    p: int = v * (v + 1) * (v * 2)
    q: int = (2 * v - 3) * (2 * v - 1) * (2 * v + 1)
    return sqrt(Rational(p, q))


# # The following procedure ME_SO5r3 returns the (alternative SO(3) reduced)
# # matrix element
# #
# #      4*Pi
# #   ------------- * <v_f,al_f,L_f || Y^v_{al,L} || v_i,al_i,L_i>
# #   sqrt (2*L_f+1)
# #
# # for the SO(5) spherical harmonic Y^v_{al,L}. It uses (37) & (39).
# # The return value might be (partly) algebraic, so it might be
# # necessary to apply evalf to it.
#
# # To obtain alternative reduced matrix elements of cos(3g), use
# #              Y310 = (3/4/Pi) cos(3g).
# # So to get the matrix element of cos(3g) from this, we must mult by (1/3).
#
# ME_SO5r3:=proc(v_f::integer,al_f::integer,L_f::integer,
#                v::integer,al::integer,L::integer,
#                v_i::integer,al_i::integer,L_i::integer)
#
#    CG_SO5r3(v_i,al_i,L_i,v,al,L,v_f,al_f,L_f) * ME_SO5red(v_f,v,v_i):
# end;
def ME_SO5r3(v_f: int, al_f: int, L_f: int,
             v: int, al: int, L: int,
             v_i: int, al_i: int, L_i: int) -> Expr:
    return CG_SO5r3(v_i, al_i, L_i, v, al, L, v_f, al_f, L_f) * ME_SO5red(v_f, v, v_i)


# # The following procedure RepSO5_Y_rem returns a Matrix of
# # (alternative SO(3) reduced) matrix elements
# #
# #      4*Pi
# #   ------------- * <v_f,al_f,L_f || Y^v_{al,L} || v_i,al_i,L_i>
# #   sqrt (2*L_f+1)
# #
# # for v_min <= v_i,v_f <= v_max and L_min <= L_i,L_f <= L_max.
# # It thus provides a representation of the spherical harmonic
# # Y^v_{al,L} (but lacking sqrt(2L_f+1)/4/Pi factors).
# # The elements of the returned Matrix are all floats (evalf used within).
#
# # If the L_max argument is omitted, then L_max=L_min, and thus
# # a single value of angular momentum is used.
# # If [v,al,L] doesn't label a spherical harmonic, then a matrix of 0s is
# # returned.
#
# # The remember option is used, but these stored values are cleared
# # each time the (much later) RepXspace() routine is invoked.
#
# RepSO5_Y_rem:=proc(v::integer,al::integer,L::integer,
#                     v_min::integer,v_max::integer,
#                     L_min::integer,L_max::integer,$)
#   option remember;
#   local states:
#
#   states:=lbsSO5r3_rngVvarL(_passed[4..-1]):
#   Matrix( nops(states), (i,j)->evalf(
#                  ME_SO5r3(op(states[i]),v,al,L,op(states[j])) )):
# end:
"""
The Maple remember option corresponds to the Python @cache decorator.
To forget the RepSO5_Y_rem cache call: RepSO5_Y_rem.cache_clear().
"""


@cache
def RepSO5_Y_rem(v: int, al: int, L: int,
                 v_min: int, v_max: int,
                 L_min: int, L_max: int) -> Matrix:
    states: list[SO5SO3Label] = lbsSO5r3_rngVvarL(v_min, v_max, L_min, L_max)
    return Matrix([[ME_SO5r3(*i, v, al, L, *j).evalf()
                    for j in states]
                   for i in states])


# # The following procedure RepSO5_Y_alg is the same as RepSO5_Y_rem
# # except that evalf is not used, and thus the elements of the
# # returned matrix come out (partially) algebraic.
# # Also, the remember option is not used.
# # This procedure is not used elsewhere.
#
# RepSO5_Y_alg:=proc(v::integer,al::integer,L::integer,
#                     v_min::integer,v_max::integer,
#                     L_min::integer,L_max::integer,$)
#   local states:
#
#   states:=lbsSO5r3_rngVvarL(_passed[4..-1]):
#   Matrix( nops(states), (i,j)->
#                  ME_SO5r3(op(states[i]),v,al,L,op(states[j])) ):
# end:
def RepSO5_Y_alg(v: int, al: int, L: int,
                 v_min: int, v_max: int,
                 L_min: int, L_max: int) -> Matrix:
    states: list[SO5SO3Label] = lbsSO5r3_rngVvarL(v_min, v_max, L_min, L_max)

    return Matrix([[ME_SO5r3(*i, v, al, L, *j)
                    for j in states]
                   for i in states])


# # The following procedure RepSO5_sqLdim returns a Matrix acting on
# # the states with v_min <= v_i,v_f <= v_max and L_min <= L_i,L_f <= L_max,
# # which is diagonal with entries (-1)^L_i*sqrt(2L_i+1).
#
# RepSO5_sqLdim:=proc(v_min::integer,v_max::integer,
#                     L_min::integer,L_max::integer,$)
#   local states:
#
#   states:=lbsSO5r3_rngVvarL(_passed):  # obtain labels for states
#   Matrix(map(x->evalf(eval((-1)^(x[3])*sqrt(dimSO3(x[3])))),states),
#                                shape=diagonal,scan=diagonal);
# end:
def RepSO5_sqLdim(v_min: int, v_max: int,
                  L_min: int, L_max: int) -> Matrix:
    states: list[SO5SO3Label] = lbsSO5r3_rngVvarL(v_min, v_max, L_min, L_max)

    return diag(*(((-1) ** L * sqrt(dimSO3(L))).evalf() for (_, _, L) in states))


# # The following procedure RepSO5_sqLdiv returns a Matrix acting on
# # the states with v_min <= v_i,v_f <= v_max and L_min <= L_i,L_f <= L_max,
# # which is diagonal with entries (-1)^L_i/sqrt(2L_i+1).
#
# RepSO5_sqLdiv:=proc(v_min::integer,v_max::integer,
#                     L_min::integer,L_max::integer,$)
#   local states:
#
#   states:=lbsSO5r3_rngVvarL(_passed):  # obtain labels for states
#   Matrix(map(x->evalf(eval((-1)^(x[3])/sqrt(dimSO3(x[3])))),states),
#                                shape=diagonal,scan=diagonal);
# end:
def RepSO5_sqLdiv(v_min: int, v_max: int,
                  L_min: int, L_max: int) -> Matrix:
    states: list[SO5SO3Label] = lbsSO5r3_rngVvarL(v_min, v_max, L_min, L_max)

    return diag(*(((-1) ** L / sqrt(dimSO3(L))).evalf() for (_, _, L) in states))


# # The following procedure RepSO5r3_Prod returns a Matrix that represents
# # (up to a normalisation given below) the product of spherical harmonics
# # on the space of states with v_min <= v_i,v_f <= v_max and
# # L_min <= L_i,L_f <= L_max. The Matrix has entries of type float.
# # If the L_max argument is omitted, then L_max=L_min.
# # The argument ys_op is a list, each element of which denotes
# # a single spherical harmonic. Each of these elements is either one of
# # the symbolic names
# #     SpHarm_112, SpHarm_212, SpHarm_214, ... , SpHarm_61C
# # (see SpHarm_Table above for the full list),
# # or is a triple [v,alpha,L] which designates the Spherical harmonic
# # explicitly. In addition, two other operators are also permitted: they are
# #   1) SpDiag_sqLdim, which provides a diagonal operator with entries
# #                       (-1)^{L_i}*sqrt(2L_i+1)
# #   2) SpDiag_sqLdiv, which provides a diagonal operator with entries
# #                       (-1)^{L_i}/sqrt(2L_i+1).
#
# # The returned Matrix is obtained simply by multiplying
# # together the individual Matrices for the entries of ys_op.
# # Therefore, the result is meaningful only for certain products:
# #   1. at most one entry having non-zero angular momentum;
# #   2. Same, but also with products of the form
# #            [..., SpDiag_sqLdim, Y1, SpDiag_sqLdiv, Y2, ...]
# #      with Y1 and Y2 having identical AM.
# # In these cases, on multiplying the returned Matrix by (4*Pi)^(-N),
# # where N is the number of genuine spherical harmonics in the list,
# # the result is a Matrix of alternative SO(3)-reduced matrix elements.
# # (N may be obtained using the procedure NumSO5r3_Prod below,
# # and is not necessarily the length of ys_op because this list may
# # contain non-harmonics such as SpDiag terms).
# # To obtain genuine SO(3)-reduced matrix elements, the result
# # needs to be further multiplied by (a matrix of) sqrt(2L_f+1).
#
# # This procedure clears the RepSO5_Y_rem remember tables.
#
# RepSO5r3_Prod:=proc(ys_op::list,v_min::integer,v_max::integer,
#                                 L_min::integer,L_max::integer,$)
#   local rep:
#   rep:=RepSO5r3_Prod_wrk(_passed):
#
#   forget(RepSO5_Y_rem):
#   rep:
# end:
def RepSO5r3_Prod(ys_op: list,
                  v_min: int, v_max: int,
                  L_min: int, L_max: int) -> Matrix:
    rep: Matrix = RepSO5r3_Prod_wrk(tuple(ys_op), v_min, v_max, L_min, L_max)

    RepSO5_Y_rem.cache_clear()
    return rep


# # The following procedure RepSO5r3_Prod_rem is exactly the same as
# # the above except that has the remember option, and doesn't clear
# # the remember tables for RepSO5_Y_rem.
#
# RepSO5r3_Prod_rem:=proc(ys_op::list,v_min::integer,v_max::integer,
#                                     L_min::integer,L_max::integer,$)
#     option remember;
#
#   RepSO5r3_Prod_wrk(_passed):
# end:
@cache
def RepSO5r3_Prod_rem(ys_op: tuple,
                      v_min: int, v_max: int,
                      L_min: int, L_max: int) -> Matrix:
    return RepSO5r3_Prod_wrk(ys_op, v_min, v_max, L_min, L_max)


# # The following procedure RepSO5r3_Prod_wrk is as the above two,
# # but does all the work for those, without being concerned by
# # remembering stuff.
# # Note the use of "copy" in this procedure. This is necessary otherwise
# # the remember table for RepSO5_Y_rem gets messed up!
#
# RepSO5r3_Prod_wrk:=proc(ys_op::list,v_min::integer,v_max::integer,
#                                     L_min::integer,L_max::integer,$)
#     local i,n,Mats,Mat_product,this_op;
#     global SpHarm_Operators,SpHarm_Table;
#
#   n:=nops(ys_op);
#
#   if n=0 then   # require identity matrix
#     return Matrix([seq(1,i=1..dimSO5r3_rngVvarL(_passed[2..-1]))],
#                                    scan=diagonal):
#   else
#
#     for i from 1 to n do
#
#       if type(ys_op[i],list(nonnegint)) and nops(ys_op[i])=3 then
#         this_op:=ys_op[i];
#       elif member(ys_op[i],SpHarm_Operators) then
#         this_op:=SpHarm_Table[ys_op[i]];
#       elif ys_op[i]=SpDiag_sqLdim then
#         if i=1 then  # cannot make copy because that'd force diag data matrix
#           Mat_product:=Matrix(RepSO5_sqLdim(_passed[2..-1]));
#         else
#           MatrixMatrixMultiply(Mat_product,
#                                RepSO5_sqLdim(_passed[2..-1]),inplace);
#         fi:
#         next;     # tackle next i in for loop
#       elif ys_op[i]=SpDiag_sqLdiv then
#         if i=1 then
#           Mat_product:=Matrix(RepSO5_sqLdiv(_passed[2..-1]));
#         else
#           MatrixMatrixMultiply(Mat_product,
#                                RepSO5_sqLdiv(_passed[2..-1]),inplace);
#         fi:
#         next;     # tackle next i in for loop
#
#       else
#         error "Invalid SO(5) harmonic designator %1", ys_op[i]:
#       fi:
#
#
#       # Now multiply in the spherical harmonic denoted by this_op.
#
#       if i=1 then
#         Mat_product:=copy(RepSO5_Y_rem( op(this_op), _passed[2..-1]));
#       else
#         MatrixMatrixMultiply(
#                    Mat_product,
#                    RepSO5_Y_rem( op(this_op), _passed[2..-1]),
#                    inplace);
#       fi:
#
#     od:
#   fi:
#
# #  To get genuine alternative reduced matrix elements, we now need to
# #  multiply by (4*Pi)^(-N) for N the number of SpHarms in the list
#
#    Mat_product;
# end:
def RepSO5r3_Prod_wrk(ys_op: tuple,
                      v_min: int, v_max: int,
                      L_min: int, L_max: int) -> Matrix:
    n: int = len(ys_op)

    if n == 0:
        return eye(dimSO5r3_rngVvarL(v_min, v_max, L_min, L_max))

    Mat_product: Optional[Matrix] = None
    for ys_op_i in ys_op:
        M: Matrix

        if isinstance(ys_op_i, tuple) and len(ys_op_i) == 3:
            M = RepSO5_Y_rem(*ys_op_i, v_min, v_max, L_min, L_max)
        elif ys_op_i in SpHarm_Table:
            M = RepSO5_Y_rem(*SpHarm_Table[ys_op_i], v_min, v_max, L_min, L_max)
        elif ys_op_i == SpDiag_sqLdim:
            M = RepSO5_sqLdim(v_min, v_max, L_min, L_max)
        elif ys_op_i == SpDiag_sqLdiv:
            M = RepSO5_sqLdiv(v_min, v_max, L_min, L_max)
        else:
            raise ValueError(f'Invalid SO(5) harmonic designator {ys_op_i}')

        assert M is not None
        Mat_product = Matrix(M) if Mat_product is None else Mat_product * M

    assert Mat_product is not None
    return Mat_product


# # The following procedure NumSO5r3_Prod examines the list ys_op, and
# # determines how many of its entries denote spherical harmonics,
# # either from
# #     SpHarm_112, SpHarm_212, SpHarm_214, ... , SpHarm_61C
# # (see SpHarm_Table above for the full list),
# # or a triple [v,alpha,L] (but no checking that the entries actually
# # correspond to a genuine spherical harmonic).
#
# # This is useful for getting the correct 4*Pi normalisation in the
# # previous few procedures.
#
# NumSO5r3_Prod:=proc(ys_op::list,$)
#   local i,ct:
#
#   ct:=0:
#
#   for i from 1 to nops(ys_op) do
#     if type(ys_op[i],list(nonnegint)) and nops(ys_op[i])=3 then
#         ct:=ct+1:
#     elif member(ys_op[i],SpHarm_Operators) then
#         ct:=ct+1:
#     fi:
#   od:
#
#   ct;
# end:
def NumSO5r3_Prod(ys_op: tuple) -> int:
    ct: int = 0

    for ys_op_i in ys_op:
        if isinstance(ys_op_i, tuple) and len(ys_op_i) == 3:
            ct += 1
        elif ys_op_i in SpHarm_Table:
            ct += 1

    return ct


# ###########################################################################
# ####------------------- Specification of Operators --------------------####
# ###########################################################################
#
# # In the ACM, operators on the full Hilbert space are encoded using
# # a particular list structure. These lists are each of the form
# #      [ [co1, [op11,op12,...] ],
# #        [co2, [op21,op22,...] ],
# #        [co3, [op31,op32,...] ],
# #        ...
# #        [coN, [opN1,opN2,...] ] ]
# # where each co# is a constant, and each op## is a symbolic name
# # from table I,II or III, or SpDiag_sqLdim or SpDiag_sqLdiv.
# # This then corresponds to the operator which is the sum of operators
# #                co# * Op#1 * Op#2 * Op#3 * ...
# # where Op#i is the operator denoted by the symbolic name op#i,
# # and SpDiag_sqLdim and SpDiag_sqLdiv are diagonal operators that
# # multiply the basis state [nu;v,alpha,L] by
# #            (-1)^L*sqrt(2L+1) and (-1)^L/sqrt(2L+1)
# # respectively.
# # (The full list of acceptable symbolic names is given in the variables
# #  Radial_Operators, Spherical_Operators, Xspace_Operators.)
#
# # In addition to simple numerical constants, the coefficients
# # can be functions of SENIORITY, ANGMOM, NUMBER, ALFA
# # (anything else will cause problems!) -
# # these will be substituted for according to the [nu;v,alpha,L] values
# # of the state being operated on by setting SENIORITY=v, ANGMOM=L,
# # NUMBER=nu, ALFA=alpha.
#
# # See Section 7.3 for more details.
SENIORITY: Symbol = Symbol('SENIORITY')
ANGMOM: Symbol = Symbol('ANGMOM')
NUMBER: Symbol = Symbol('NUMBER')
ALFA: Symbol = Symbol('ALFA')


# ###########################################################################
#
# # The procedure ACM_Hamiltonian below produces the encoding of
# # operators of certain (rational) types. Thus for these operators,
# # the user doesn't need to know anything about the encoding method.
# # This procedure takes up to 14 parameters that specify coefficients
# # of (b denotes beta, g denotes gamma)
# #    Laplacian, 1, b^2, b^4, b^(-2),
# #      b*cos(3g), b^3*cos(3g), b^5*cos(3g), b^(-1)*cos(3g),
# #      cos(3g)^2, b^2*cos(3g)^2, b^4*cos(3g)^2, b^(-2)*cos(3g)^2,
# #      [pi x q x pi]_(v=3,L=0).
# # Each of the arguments is a numeric value, or a function of
# # SENIORITY, ANGMOM, NUMBER, ALFA, as described above.
#
# ACM_Hamiltonian:=proc(c11:=0,c20:=0,c21:=0,c22:=0,c23:=0,
#                            c30:=0,c31:=0,c32:=0,c33:=0,
#                            c40:=0,c41:=0,c42:=0,c43:=0,
#                            c50:=0,$)
#     local our_op:
#
#   if c11<>0 then   # build laplacian using eqn (57)
#     our_op:=[ [c11,[Radial_D2b]],
#               [-c11*(2+SENIORITY*(SENIORITY+3)),[Radial_bm2]] ]:
#   else
#     our_op:=[]:
#   fi:
#
#   if c20<>0 then our_op:=[ op(our_op),
#                [c20,[]] ]: fi:
#   if c21<>0 then our_op:=[ op(our_op),
#                [c21,[Radial_b2]] ]: fi:
#   if c22<>0 then our_op:=[ op(our_op),
#                [c22,[Radial_b2,Radial_b2]] ]: fi:
#   if c23<>0 then our_op:=[ op(our_op),
#                [c23,[Radial_bm2]] ]: fi:
#   if c30<>0 then our_op:=[ op(our_op),
#                [c30*Convert_310,[Radial_b,SpHarm_310]] ]: fi:
#   if c31<>0 then our_op:=[ op(our_op),
#                [c31*Convert_310, [Radial_b2,Radial_b,SpHarm_310]] ]: fi:
#   if c32<>0 then our_op:=[ op(our_op),
#                [c32*Convert_310, [Radial_b2,Radial_b2,
#                                   Radial_b,SpHarm_310]] ]: fi:
#   if c33<>0 then our_op:=[ op(our_op),
#                [c33*Convert_310, [Radial_bm,SpHarm_310]] ]: fi:
#   if c40<>0 then our_op:=[ op(our_op),
#                [c40*Convert_310^2, [SpHarm_310,SpHarm_310]] ]: fi:
#   if c41<>0 then our_op:=[ op(our_op),
#                [c41*Convert_310^2, [Radial_b2,SpHarm_310,SpHarm_310]] ]: fi:
#   if c42<>0 then our_op:=[ op(our_op),
#                [c42*Convert_310^2, [Radial_b2,Radial_b2,
#                                     SpHarm_310,SpHarm_310]] ]: fi:
#   if c43<>0 then our_op:=[ op(our_op),
#                [c43*Convert_310^2,[Radial_bm2,SpHarm_310,SpHarm_310]] ]: fi:
#   if c50<>0 then our_op:=[ op(our_op),
#                [c50,[Xspace_PiqPi]] ]: fi:
#
#   our_op:
# end:
def ACM_Hamiltonian(c11: IntFloatExpr = 0,
                    c20: IntFloatExpr = 0,
                    c21: IntFloatExpr = 0,
                    c22: IntFloatExpr = 0,
                    c23: IntFloatExpr = 0,
                    c30: IntFloatExpr = 0,
                    c31: IntFloatExpr = 0,
                    c32: IntFloatExpr = 0,
                    c33: IntFloatExpr = 0,
                    c40: IntFloatExpr = 0,
                    c41: IntFloatExpr = 0,
                    c42: IntFloatExpr = 0,
                    c43: IntFloatExpr = 0,
                    c50: IntFloatExpr = 0) -> OperatorSum:
    c11 = S(c11)
    c20 = S(c20)
    c21 = S(c21)
    c22 = S(c22)
    c23 = S(c23)
    c30 = S(c30)
    c31 = S(c31)
    c32 = S(c32)
    c33 = S(c33)
    c40 = S(c40)
    c41 = S(c41)
    c42 = S(c42)
    c43 = S(c43)
    c50 = S(c50)

    our_op: OperatorSum = () if c11 == 0 \
        else ((c11, (Radial_D2b,)),
              (-c11 * (2 + SENIORITY * (SENIORITY + 3)), (Radial_bm2,)))
    if c20 != 0:
        our_op += ((c20, ()),)
    if c21 != 0:
        our_op += ((c21, (Radial_b2,)),)
    if c22 != 0:
        our_op += ((c22, (Radial_b2, Radial_b2)),)
    if c23 != 0:
        our_op += ((c23, (Radial_bm2,)),)
    if c30 != 0:
        our_op += ((c30 * Convert_310, (Radial_b, SpHarm_310)),)
    if c31 != 0:
        our_op += ((c31 * Convert_310, (Radial_b2, Radial_b, SpHarm_310)),)
    if c32 != 0:
        our_op += ((c32 * Convert_310, (Radial_b2, Radial_b2, Radial_b, SpHarm_310)),)
    if c33 != 0:
        our_op += ((c33 * Convert_310, (Radial_bm, SpHarm_310)),)
    if c40 != 0:
        our_op += ((c40 * Convert_310 ** 2, (SpHarm_310, SpHarm_310)),)
    if c41 != 0:
        our_op += ((c41 * Convert_310 ** 2, (Radial_b2, SpHarm_310, SpHarm_310)),)
    if c42 != 0:
        our_op += ((c42 * Convert_310 ** 2, (Radial_b2, Radial_b2, SpHarm_310, SpHarm_310)),)
    if c43 != 0:
        our_op += ((c43 * Convert_310 ** 2, (Radial_bm2, SpHarm_310, SpHarm_310)),)
    if c50 != 0:
        our_op += ((c50, (Xspace_PiqPi,)),)

    return our_op


# # The procedure ACM_HamRigidBeta below produces the encoding of
# # certain Hamiltonians that are appropriate for rigid-beta models
# # (they don't involve beta). There are up to eight numerical
# # arguments that stipulate the coefficients of
# #    SO(5) Casimir, 1, cos(3g)
# #    cos(3g)^2, cos(3g)^3, cos(3g)^4, cos(3g)^5, cos(3g)^6.
# # The final argument (0 or 1, the former the default) indicates whether
# # to encode using only the spherical harmonic SpHarm_310 (for 0), or use
# # the spherical harmonic SpHarm_610 as much as possible (for 1).
#
# ACM_HamRigidBeta:=proc(cas:=0,con:=0,c1:=0,c2:=0,c3:=0,
#                                      c4:=0,c5:=0,c6:=0,flag::integer:=0,$)
#     local our_op:
#
#
#   if flag=0 then
#     our_op:=ACM_HamSH3(_params[2..8]):
#   elif flag=1 then
#     our_op:=ACM_HamSH6(_params[2..8]):
#   else
#     error "Unrecognised flag %1", flag:
#   fi:
#
#   if cas<>0 then   # build casimir using eqn (58)
#     if our_op<>[] then
#       our_op:=[ [cas*SENIORITY*(SENIORITY+3),[]], op(our_op) ]:
#     else
#       our_op:=[ [cas*SENIORITY*(SENIORITY+3),[]] ]:
#     fi:
#   fi:
#
#   our_op:
# end:
def ACM_HamRigidBeta(cas: IntFloatExpr = 0,
                     con: IntFloatExpr = 0,
                     c1: IntFloatExpr = 0,
                     c2: IntFloatExpr = 0,
                     c3: IntFloatExpr = 0,
                     c4: IntFloatExpr = 0,
                     c5: IntFloatExpr = 0,
                     c6: IntFloatExpr = 0,
                     flag: int = 0) -> OperatorSum:
    if flag not in {0, 1}:
        raise ValueError(f'Unrecognised flag: {flag}')

    cs: list[Expr] = [S(c) for c in [con, c1, c2, c3, c4, c5, c6]]
    our_op: OperatorSum = ACM_HamSH3(*cs) if flag == 0 else ACM_HamSH6(*cs)

    cas = S(cas)
    if cas != 0:
        cas_op: OperatorProduct = (cas * SENIORITY * (SENIORITY + 3), ())
        if len(our_op) > 0:
            our_op = (cas_op,) + our_op
        else:
            our_op = (cas_op,)

    return our_op


# # The procedure ACM_HamSH3 below provides the ACM encoding for linear
# # combinations of
# #    1, cos(3g), cos(3g)^2, cos(3g)^3, cos(3g)^4, cos(3g)^5, cos(3g)^6,
# #    cos(3g)^7, cos(3g)^8,
# # in terms of the spherical harmonic SpHarm_310.
# # Its nine arguments give the coefficients of these terms.
# # It's used by the above procedure ACM_HamRigidBeta.
#
# ACM_HamSH3:=proc(c0:=0,c1:=0,c2:=0,c3:=0,c4:=0,c5:=0,c6:=0,c7:=0,c8:=0,$)
#     local our_op:
#
#   if c0<>0 then
#        our_op:=[ [c0,[]] ]:
#   else
#        our_op:=[]:
#   fi:
#
#
#   if c1<>0 then our_op:=[ op(our_op),
#               [c1*Convert_310,[SpHarm_310]] ]: fi:
#   if c2<>0 then our_op:=[ op(our_op),
#               [c2*Convert_310^2,[SpHarm_310,SpHarm_310]] ]: fi:
#   if c3<>0 then our_op:=[ op(our_op),
#               [c3*Convert_310^3,[SpHarm_310,SpHarm_310,SpHarm_310]] ]: fi:
#   if c4<>0 then our_op:=[ op(our_op),
#               [c4*Convert_310^4,[SpHarm_310,SpHarm_310,SpHarm_310,
#                                  SpHarm_310]] ]: fi:
#   if c5<>0 then our_op:=[ op(our_op),
#               [c5*Convert_310^5,[SpHarm_310,SpHarm_310,SpHarm_310,
#                                  SpHarm_310,SpHarm_310]] ]: fi:
#   if c6<>0 then our_op:=[ op(our_op),
#               [c6*Convert_310^6,[SpHarm_310,SpHarm_310,SpHarm_310,
#                                  SpHarm_310,SpHarm_310,SpHarm_310]] ]: fi:
#   if c7<>0 then our_op:=[ op(our_op),
#               [c7*Convert_310^7,[SpHarm_310,SpHarm_310,SpHarm_310,
#                                  SpHarm_310,SpHarm_310,SpHarm_310,
#                                  SpHarm_310]] ]: fi:
#   if c8<>0 then our_op:=[ op(our_op),
#               [c8*Convert_310^8,[SpHarm_310,SpHarm_310,SpHarm_310,
#                                  SpHarm_310,SpHarm_310,SpHarm_310,
#                                  SpHarm_310,SpHarm_310]] ]: fi:
#   our_op:
# end:
def ACM_HamSH3(c0: Expr = S.Zero,
               c1: Expr = S.Zero,
               c2: Expr = S.Zero,
               c3: Expr = S.Zero,
               c4: Expr = S.Zero,
               c5: Expr = S.Zero,
               c6: Expr = S.Zero,
               c7: Expr = S.Zero,
               c8: Expr = S.Zero) -> OperatorSum:
    our_op: OperatorSum = () if c0 == 0 else ((c0, ()),)

    for n, c in zip(range(1, 9), [c1, c2, c3, c4, c5, c6, c7, c8]):
        if c != 0:
            our_op += ((c * Convert_310 ** n, (SpHarm_310,) * n),)

    return our_op


# # The procedure ACM_HamSH6 below provides the ACM encoding for linear
# # combinations of
# #    1, cos(3g), cos(3g)^2, cos(3g)^3, cos(3g)^4, cos(3g)^5, cos(3g)^6,
# #    cos(3g)^7, cos(3g)^8,
# # in terms of the spherical harmonics SpHarm_310 and SpHarm_610,
# # preferring the latter as much as possible.
# # Its nine arguments give the coefficients of these terms.
# # It's used by the above procedure ACM_HamRigidBeta.
#
# ACM_HamSH6:=proc(c0:=0,c1:=0,c2:=0,c3:=0,c4:=0,c5:=0,c6:=0,c7:=0,c8:=0,$)
#     local our_op,d0,d1,d2,d3,d4,d5,d6,d7,d8:
#
#   # First convert into coefficients d[2n+m] of
#   #   (Convert_310*SpHarm_310)^m * (Convert_610*SpHarm_610)^n
#   # where m=0 or 1, and n>=0.
#
#   d0:=c0+c2/3+c4/9+c6/27+c8/81:
#   d1:=c1+c3/3+c5/9+c7/27:
#   d2:=c2/3+c4*2/9+c6/9+c8*4/81:
#   d3:=c3/3+c5*2/9+c7/9:
#   d4:=c4/9+c6/9+c8*2/27:
#   d5:=c5/9+c7/9:
#   d6:=c6/27+c8*4/81:
#   d7:=c7/27:
#   d8:=c8/81:
#
#
#   if d0<>0 then
#        our_op:=[ [d0,[]] ]:
#   else
#        our_op:=[]:
#   fi:
#
#   if d1<>0 then our_op:=[ op(our_op),
#               [d1*Convert_310, [SpHarm_310]] ]: fi:
#   if d2<>0 then our_op:=[ op(our_op),
#               [d2*Convert_610, [SpHarm_610]] ]: fi:
#   if d3<>0 then our_op:=[ op(our_op),
#               [d3*Convert_610*Convert_310, [SpHarm_610,SpHarm_310]] ]: fi:
#   if d4<>0 then our_op:=[ op(our_op),
#               [d4*Convert_610^2, [SpHarm_610,SpHarm_610]] ]: fi:
#   if d5<>0 then our_op:=[ op(our_op),
#               [d5*Convert_610^2*Convert_310,
#                           [SpHarm_610,SpHarm_610,SpHarm_310]] ]: fi:
#   if d6<>0 then our_op:=[ op(our_op),
#               [d6*Convert_610^3,
#                           [SpHarm_610,SpHarm_610,SpHarm_610]] ]: fi:
#   if d7<>0 then our_op:=[ op(our_op),
#               [d7*Convert_610^3*Convert_310,
#                           [SpHarm_610,SpHarm_610,SpHarm_610,SpHarm_310]] ]: fi:
#   if d8<>0 then our_op:=[ op(our_op),
#               [d8*Convert_610^4,
#                           [SpHarm_610,SpHarm_610,SpHarm_610,SpHarm_610]] ]: fi:
#   our_op:
# end:
def ACM_HamSH6(c0: Expr = S.Zero,
               c1: Expr = S.Zero,
               c2: Expr = S.Zero,
               c3: Expr = S.Zero,
               c4: Expr = S.Zero,
               c5: Expr = S.Zero,
               c6: Expr = S.Zero,
               c7: Expr = S.Zero,
               c8: Expr = S.Zero) -> OperatorSum:
    d0: Expr = c0 + c2 / 3 + c4 / 9 + c6 / 27 + c8 / 81
    d1: Expr = c1 + c3 / 3 + c5 / 9 + c7 / 27
    d2: Expr = c2 / 3 + c4 * 2 / 9 + c6 / 9 + c8 * 4 / 81
    d3: Expr = c3 / 3 + c5 * 2 / 9 + c7 / 9
    d4: Expr = c4 / 9 + c6 / 9 + c8 * 2 / 27
    d5: Expr = c5 / 9 + c7 / 9
    d6: Expr = c6 / 27 + c8 * 4 / 81
    d7: Expr = c7 / 27
    d8: Expr = c8 / 81

    our_op: OperatorSum = () if d0 == 0 else ((d0, ()),)

    if d1 != 0:
        our_op += ((d1 * Convert_310, (SpHarm_310,)),)
    if d2 != 0:
        our_op += ((d2 * Convert_610, (SpHarm_610,)),)
    if d3 != 0:
        our_op += ((d3 * Convert_610 * Convert_310, (SpHarm_610, SpHarm_310)),)
    if d4 != 0:
        our_op += ((d4 * Convert_610 ** 2, (SpHarm_610, SpHarm_610)),)
    if d5 != 0:
        our_op += ((d5 * Convert_610 ** 2 * Convert_310,
                    (SpHarm_610,) * 2 + (SpHarm_310,)),)
    if d6 != 0:
        our_op += ((d6 * Convert_610 ** 3, (SpHarm_610,) * 3),)
    if d7 != 0:
        our_op += ((d7 * Convert_610 ** 3 * Convert_310,
                    (SpHarm_610,) * 3 + (SpHarm_310,)),)
    if d8 != 0:
        our_op += ((d8 * Convert_610 ** 4, (SpHarm_610,) * 4),)

    return our_op


# # The following procedure Op_AM returns the SO(3) AM of an operator.
# # This operator is given in the form described above.
# # If the operator doesn't have definite AM then minus the largest value
# # is returned.
# # This procedure is only used by the procedure ACM_set_transition
# # to set glb_rat_TRopAM to be the AM of the transition operator.
#
# Op_AM:=proc(WOp::list(list))
#     local am,first,i,t,Wterm:
#
#     if nops(WOp)=0 then return 0 fi:
#
#     for i to nops(WOp) do
#       Wterm:=WOp[i][2]:
#       am:=0:
#       for t in Wterm do
#         if t in SpHarm_Operators then
#           am:=am+SpHarm_Table[t][3]:
#         elif t in [Xspace_Pi,Xspace_PiPi2] then
#           am:=am+2:
#         elif t = Xspace_PiPi4 then
#           am:=am+4:
#         fi:
#       od:
#
#       if i=1 then
#         first:=am:
#       elif first>=0 and am<>first then   #there are terms of different AM
#         first:=-max(first,am):
#       elif first<0 and am>-first then
#         first:=-am:
#       fi:
#     od:
#
#     first:
# end:
def Op_AM(WOp: OperatorSum) -> int:
    if len(WOp) == 0:
        return 0

    first: int = 0

    for i in range(1, len(WOp) + 1):
        Wterm = WOp[i - 1][1]
        am: int = 0
        for t in Wterm:
            if t in SpHarm_Operators:
                am += SpHarm_Table[t][2]
            elif t in {Xspace_Pi, Xspace_PiPi2}:
                am += 2
            elif t == Xspace_PiPi4:
                am += 4

        if i == 1:
            first = am
        elif 0 <= first != am:
            first = -max(first, am)
        elif first < 0 and am > -first:
            first = -am

    return first


# # The following procedure Op_Parity returns the parity of an operator.
# # This operator is given in the form described above.
# # It returns 0 or 1 accordingly. If the operator has indeterminate
# # parity then -1 is returned.
# # This procedure is not used elsewhere.
#
# Op_Parity:=proc(WOp::list(list))
#     local parity,first,i,t,Wterm:
#
#     if nops(WOp)=0 then return 0 fi:
#
#     for i to nops(WOp) do
#       Wterm:=WOp[i][2]:
#       parity:=0:
#       for t in Wterm do
#         if t in [ Radial_b, Radial_bm, Radial_Db, Xspace_Pi,
#                   SpHarm_112, SpHarm_310, SpHarm_313, SpHarm_314, SpHarm_316,
#                   SpHarm_512, SpHarm_514, SpHarm_515, SpHarm_516, SpHarm_517,
#                   SpHarm_518, SpHarm_51A ] then
#           parity:=parity+1:
#         fi:
#       od:
#
#       if i=1 then
#         first:=irem(parity,2):
#       elif type(parity-first,odd) then    #terms of different parity
#         return -1
#       fi:
#     od:
#
#     first:
# end:
def Op_Parity(WOp: OperatorSum) -> int:
    if len(WOp) == 0:
        return 0

    first: int = 0
    for i0, WOp_i in enumerate(WOp):
        i: int = i0 + 1
        Wterm: tuple[Symbol, ...] = WOp_i[1]
        parity: int = 0
        for t in Wterm:
            if t in {Radial_b, Radial_bm, Radial_Db, Xspace_Pi,
                     SpHarm_112, SpHarm_310, SpHarm_313, SpHarm_314, SpHarm_316,
                     SpHarm_512, SpHarm_514, SpHarm_515, SpHarm_516, SpHarm_517,
                     SpHarm_518, SpHarm_51A}:
                parity += 1

        if i == 1:
            first = parity % 2
        elif (parity - first) % 2 == 1:
            return -1

    return first


# # The following procedure Op_Tame determines whether an operator
# # doesn't contain any of
# #           Xspace_Pi, Xspace_PiPi2, Xspace_PiPi4.
# # If not, it returns true (boolean), otherwise false.
# # Later, this is used, in the case of a Hamiltonian, to indicate whether
# # we need only to calculate representation matrices on individual L-spaces.
# # (Otherwise, we need to use the full truncated Hilbert space).
#
# Op_Tame:=proc(WOp::list(list))
#     local parity,first,i,t,Wterm:
#
#     if nops(WOp)=0 then return 0 fi:
#
#     for i to nops(WOp) do
#       Wterm:=WOp[i][2]:
#       parity:=0:
#       for t in Wterm do
#         if t in [ Xspace_Pi, Xspace_PiPi2, Xspace_PiPi4 ] then
#           return false:
#         fi:
#       od:
#     od:
#
#     true:
# end:
def Op_Tame(WOp: OperatorSum) -> bool:
    if len(WOp) == 0:
        return True

    for WOp_i in WOp:
        Wterm: tuple[Symbol, ...] = WOp_i[1]
        for t in Wterm:
            if t in {Xspace_Pi, Xspace_PiPi2, Xspace_PiPi4}:
                return False

    return True


# # The following three values specify particular (linear combinations of)
# # operators.
# # laplacian_op encodes the SO(5) Laplacian.
# # The latter two may be used as a check on commutation relations:
# # comm_su11_op encodes a sum of three SU(1,1) operators
# # which should produce a zero matrix;
# # comm_bdb_op encodes [d/d(beta) * beta, beta * d/d(beta)] - id.
# # which should also produce a zero matrix (note that an empty operator
# # product [] denotes the identity operator).
#
#
# laplacian_op:=[ [1,[Radial_D2b]],
#                      [-(2+SENIORITY*(SENIORITY+3)),[Radial_bm2]] ]:
laplacian_op: OperatorSum = ((S.One, (Radial_D2b,)),
                             (-(2 + SENIORITY * (SENIORITY + 3)), (Radial_bm2,)))

# comm_su11_op:=[ [ 1,[Radial_Sm,Radial_Sp]],
#                      [-1,[Radial_Sp,Radial_Sm]],
#                      [-2,[Radial_S0]] ]:
comm_su11_op: OperatorSum = ((S.One, (Radial_Sm, Radial_Sp)),
                             (S.NegativeOne, (Radial_Sp, Radial_Sm)),
                             (-S(2), (Radial_S0,)))
# comm_bdb_op:=[ [-1,[Radial_b,Radial_Db]],
#                     [1,[Radial_Db,Radial_b]],
#                     [-1,[]] ]:
comm_bdb_op: OperatorSum = ((S.NegativeOne, (Radial_b, Radial_Db)),
                            (S.One, (Radial_Db, Radial_b)),
                            (S.NegativeOne, ()))
