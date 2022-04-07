"""6. Procedures that represent operators on the full (cross-product) Hilbert space."""

from typing import Optional
from functools import cache

from sympy import S, Symbol, Expr, Matrix, zeros, diag, eye, Rational, sqrt

from acmpy.compat import nonnegint, require_nonnegint, require_nonnegint_range, posint, require_posint
from acmpy.spherical_space import dimSO5r3_rngVvarL, lbsSO5r3_rngVvarL, lbsSO5r3_rngL, \
    Alpha, AngularMomentum, Seniority, SO5SO3Label, dimSO3
from acmpy.radial_space import dimRadial, Nu, lbsRadial, RepRadial, RepRadial_param, Matrix_sqrt, Matrix_sqrtInv, \
    RepRadial_bS_DS, RepRadialshfs_Prod, RepRadial_Prod_rem, RepRadial_LC_rem
from acmpy.internal_operators import OperatorSum, NUMBER, SENIORITY, ALFA, ANGMOM, RepSO5_Y_rem, RepSO5r3_Prod_rem, \
    Radial_Operators, Spherical_Operators, Xspace_PiqPi, Xspace_PiPi2, Xspace_PiPi4, Xspace_Pi, Convert_red, \
    NumSO5r3_Prod, Radial_Db, Radial_bm, Qred_p1, Qred_m1, Radial_bm2, Radial_D2b, Radial_bDb, Radial_b, \
    QxQred_p2, QxQred_m2, QxQred_0, QxQxQred_p3, QxQxQred_m3, QxQxQred_m1, ME_SO5red
from acmpy.so5_so3_cg import CG_SO5r3
import acmpy.globals as globals
from acmpy.globals import glb_lam_fun


# ###########################################################################
# ####-------------- Representing operators on full Xspace --------------####
# ###########################################################################
#
# # Here, we obtain representations on the full Hilbert space by
# # combining representations on the radial and spherical spaces
# # that are obtained using the procedures given above.
#
# # The following procedure dimXspace returns the dimension of the
# # truncated Hilbert space for the nu range of the radial space
# # nu_min,..,nu_max, and for the spherical space, the seniority range
# # v_min,..,v_max, and for the angular momentum range L_min,..,L_max.
# # If the L_max argument is omitted, then L_max=L_min.
#
# dimXspace:=proc(nu_min::nonnegint,nu_max::nonnegint,
#                 v_min::nonnegint,v_max::nonnegint,
#                 L_min::nonnegint,L_max::nonnegint,$)
#
#     dimRadial(nu_min,nu_max)*dimSO5r3_rngVvarL(_passed[3..-1]):
# end:
def dimXspace(nu_min: nonnegint, nu_max: nonnegint,
              v_min: nonnegint, v_max: nonnegint,
              L_min: nonnegint, L_max: Optional[nonnegint] = None
              ) -> nonnegint:
    require_nonnegint_range('nu', nu_min, nu_max)
    if L_max is None:
        L_max = L_min
    require_nonnegint_range('L', L_min, L_max)

    return dimRadial(nu_min, nu_max) * dimSO5r3_rngVvarL(v_min, v_max, L_min, L_max)


# # The following procedure lbsXspace returns a list of labels [nu,v,alpha,L]
# # for the basis states of the truncated Hilbert space:
# # nu takes the range nu_min,..,nu_max, v takes the range v_min,..,v_max,
# # while L is restricted to the range L_min,..,L_max.
# # If the L_max argument is omitted, then L_max=L_min.
# # The nu label varies fastest, then alpha, then v, and L is slowest
# # (as elsewhere).
# # If the L_max argument is omitted, then L_max=L_min.
#
# lbsXspace:=proc(nu_min::nonnegint,nu_max::nonnegint,
#                 v_min::nonnegint,v_max::nonnegint,
#                 L_min::nonnegint,L_max::nonnegint,$)
#     local rad_labels,sph_labels;
#
#   rad_labels:=lbsRadial(nu_min,nu_max);            # radial labels
#   sph_labels:=lbsSO5r3_rngVvarL(_passed[3..-1]):   # SO(5) labels
#
#   [seq( seq( [nu,op(s)], nu in rad_labels), s in sph_labels)];
# end:
XspaceLabel = tuple[Nu, Seniority, Alpha, AngularMomentum]


def lbsXspace(nu_min: nonnegint, nu_max: nonnegint,
              v_min: nonnegint, v_max: nonnegint,
              L_min: nonnegint, L_max: Optional[nonnegint]
              ) -> list[XspaceLabel]:
    require_nonnegint_range('nu', nu_min, nu_max)
    require_nonnegint_range('v', v_min, v_max)
    if L_max is None:
        L_max = L_min
    require_nonnegint_range('L', L_min, L_max)

    rad_labels: list[Nu] = lbsRadial(nu_min, nu_max)
    sph_labels: list[SO5SO3Label] = lbsSO5r3_rngVvarL(v_min, v_max, L_min, L_max)

    return [(nu,) + s for s in sph_labels for nu in rad_labels]


# ###########################################################################
#
#
# # The procedure RepXspace below returns the (alternative SO(3)-reduced)
# # Matrix of polynomials of the operators listed in tables I,II and III,
# # together with the diagonal operators SpDiag_sqLdim and SpDiag_sqLdiv,
# # on the truncated subspace of the full Hilbert space specified by
# # the ranges nu_min,..,nu_max of radial states, v_min,..,v_max of
# # seniorities, and L_min,..,L_max of SO(3) angular momentum.
# # The operator is specified in the argument x_oplc, whose format is
# # the ACM encoding of operators described above (or in Section 7.3).
# # The arguments anorm and lambda_base specify the parameters that
# # determine the radial basis.
# # The returned matrix elements are all floating point numbers
# # (if the list of operators is empty, the null matrix is returned).
# # The correct 4*Pi normalisation factors are included.
#
# # The final argument L_max is optional - if omitted then L_max=L_min,
# # so that a single angular momentum value is used.
#
# # By alternative, we mean that the matrix elements should be multiplied by
# # sqrt(2*L_f+1) to get the genuine SO(3)-reduced matrix elements of the
# # operator in question (see (37)). These are useful in practical use,
# # because this 1/sqrt(2*L_f+1) appears in the Wigner-Eckart theorem
# # (see (36)). In the case of Hamiltonians, then L=M=0 and
# # (L_i M_i 0 0 | L_f M_f)=1, and the returned matrix elements give
# # the required amplitudes directly.
#
# # With regard to labelling [nu,v,alpha,L] of the basis vectors of the
# # tensor product space, the index L varies slowest (if it varies at all),
# # v next slowest, then alpha, with the index nu varying quickest.
# # When L varies, it does so most slowest (so that the matrices formed
# # for a range of L values are obtained by simply adjoining those obtained
# # for the individual L values).
# # This corresponds to the order of the state labels output by lbsXspace.
#
# # The values of anorm and lambda_base help to determine the radial
# # basis states (they do not affect the SO(5) action).
# # The value of lambda associated with a particular state [nu,v,alpha,L]
# # in the cross product space is determined by lambda_base+glb_lam_fun(v),
# # where the function glb_lam_fun has been previously set
# # (by ACM_set_basis_type or ACM_set_lambda_fun).
# # The initial and final bases are identical.
#
# RepXspace:=proc(x_oplc::list, anorm::algebraic, lambda_base::algebraic,
#                      nu_min::nonnegint, nu_max::nonnegint,
#                      v_min::nonnegint, v_max::nonnegint,
#                      L::nonnegint, L_max::nonnegint,$)
#       local Rmat,Pmat,i,n,Xlabels;
#
#   n:=nops(x_oplc);
#
#   Xlabels:=lbsXspace(_passed[4..-1]):    # list of all states in X-space.
#
#   if n=0 then    # null sum: require zero matrix
#     Rmat:=Matrix( dimXspace(_passed[4..-1]), datatype=float ); #Null matrix
#   else
#
#     # first obtain rep matrix on X-space of 1st operator product
#
#     Rmat:=RepXspace_Prod(x_oplc[1][2],_passed[2..-1]);
#
#     if type(x_oplc[1][1],constant) then
#
#       # simply multiply by the coefficient (which is a numeric value)
#
#       MatrixScalarMultiply(Rmat,evalf(x_oplc[1][1]),inplace);
#     else
#
#       # post-multiply by a diagonal matrix that is formed by evaluating
#       # the coefficient (a function of number, seniority, alfa, angmom)
#       # at each state in the X_space
#
#       MatrixMatrixMultiply(Rmat,
#             Matrix(map(x->evalf(eval(x_oplc[1][1],
#                           [NUMBER=x[1],SENIORITY=x[2],ALFA=x[3],ANGMOM=x[4]])),
#                        Xlabels),
#                        shape=diagonal,scan=diagonal), inplace);
#     fi:
#
#     # now do similar for every other operator product - and sum results
#
#     for i from 2 to n do
#       if type(x_oplc[i][1],constant) then
#         MatrixAdd(Rmat, RepXspace_Prod(x_oplc[i][2],_passed[2..-1]),
#                                      1, evalf(x_oplc[i][1]),inplace);
#       else
#         Pmat:=RepXspace_Prod(x_oplc[i][2],_passed[2..-1]):
#         MatrixMatrixMultiply(Pmat,
#               Matrix(map(x->evalf(eval(x_oplc[i][1],
#                          [NUMBER=x[1],SENIORITY=x[2],ALFA=x[3],ANGMOM=x[4]])),
#                          Xlabels),
#                          shape=diagonal,scan=diagonal),inplace);
#         MatrixAdd(Rmat,Pmat,inplace);
#       fi:
#     od:
#
# #    for i from 2 to n do
# #      Pmat:=RepXspace_Prod(x_oplc[i][2],_passed[2..-1]):
# #      if type(x_oplc[i][1],constant) then
# #        MatrixScalarMultiply(Pmat,evalf(x_oplc[i][1]),inplace);
# #      else
# #        MatrixMatrixMultiply(Pmat,
# #              Matrix(map(x->evalf(eval(x_oplc[i][1],
# #                         [NUMBER=x[1],SENIORITY=x[2],ALFA=x[3],ANGMOM=x[4]])),
# #                         Xlabels),
# #                         shape=diagonal,scan=diagonal),inplace);
# #      fi:
# #      MatrixAdd(Rmat,Pmat,inplace);
# #    od:
#   fi:
#
#   # now clear all the remember tables used so that the next calculation
#   # can start afresh (with a different Xspace).
#   # (In this list, we have given each procedure a number, and following that
#   #  in parentheses, the numbers of these procedures that get called by it:
#   #  this is useful for debugging).
#
#   forget(RepRadial):               # 1.
#   forget(RepRadial_param):         # 2.
#   forget(Matrix_sqrt):             # 3.
#   forget(Matrix_sqrtInv):          # 4.
#   forget(RepRadial_bS_DS):         # 5.  (1,2,3,4)
#   forget(RepRadialshfs_Prod):      # 6.  (1,5)
#   forget(RepRadial_Prod_rem):      # 7.  (6)
#   forget(RepRadial_LC_rem):        # 8.  (7)
#   forget(RepXspace_Pi):            # 9.  (8)
#   forget(RepXspace_PiPi):          # 10. (8)
#   forget(RepXspace_PiqPi):         # 11. (8)
#   forget(RepSO5_Y_rem):            # 12.
#   forget(RepSO5r3_Prod_rem):       # 13. (12)
#
#   Rmat;
# end:
def RepXspace(x_oplc: OperatorSum, anorm: Expr, lambda_base: Expr,
              nu_min: nonnegint, nu_max: nonnegint,
              v_min: nonnegint, v_max: nonnegint,
              L: nonnegint, L_max: Optional[nonnegint] = None
              ) -> Matrix:
    require_nonnegint_range('nu', nu_min, nu_max)
    require_nonnegint_range('v', v_min, v_max)
    if L_max is None:
        L_max = L
    require_nonnegint_range('L', L, L_max)

    n: int = len(x_oplc)
    Xlabels: list[XspaceLabel] = lbsXspace(nu_min, nu_max, v_min, v_max, L, L_max)
    Rmat: Matrix
    if n == 0:
        Rmat = zeros(dimXspace(nu_min, nu_max, v_min, v_max, L, L_max))
    else:
        coeff, prod = x_oplc[0]
        Rmat = RepXspace_Prod(prod, anorm, lambda_base, nu_min, nu_max, v_min, v_max, L, L_max)
        if coeff.is_constant():
            Rmat = coeff.evalf() * Rmat
        else:
            Rmat = Rmat * diag(*[coeff.subs({NUMBER: nu,
                                             SENIORITY: v,
                                             ALFA: a,
                                             ANGMOM: L}).evalf()
                                 for (nu, v, a, L) in Xlabels])

        for coeff, prod in x_oplc[1:]:
            if coeff.is_constant():
                Rmat = Rmat + coeff.evalf() * \
                       RepXspace_Prod(prod, anorm, lambda_base, nu_min, nu_max, v_min, v_max, L, L_max)
            else:
                Pmat: Matrix = RepXspace_Prod(prod, anorm, lambda_base, nu_min, nu_max, v_min, v_max, L, L_max)
                Pmat = Pmat * diag(*[coeff.subs({NUMBER: nu,
                                                 SENIORITY: v,
                                                 ALFA: a,
                                                 ANGMOM: L}).evalf()
                                     for (nu, v, a, L) in Xlabels])
                Rmat = Rmat + Pmat

    RepRadial.cache_clear()
    RepRadial_param.cache_clear()
    Matrix_sqrt.cache_clear()
    Matrix_sqrtInv.cache_clear()
    RepRadial_bS_DS.cache_clear()
    RepRadialshfs_Prod.cache_clear()
    RepRadial_Prod_rem.cache_clear()
    RepRadial_LC_rem.cache_clear()
    RepXspace_Pi.cache_clear()
    RepXspace_PiPi.cache_clear()
    RepXspace_PiqPi.cache_clear()
    RepSO5_Y_rem.cache_clear()
    RepSO5r3_Prod_rem.cache_clear()

    return Rmat


# # MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
#
# # The procedure RepXspace_Prod below returns the (alternative SO(3)-reduced)
# # Matrix of a product of the operators listed in tables I,II and III,
# # together with the diagonal operators SpDiag_sqLdim and SpDiag_sqLdiv,
# # on the truncated subspace of the full Hilbert space specified by
# # the ranges nu_min,..,nu_max of radial states, v_min,..,v_max of
# # seniorities, and L_min,..,L_max of SO(3) angular momentum.
# # It is thus exactly as the procedure RepXspace above, but only applies
# # to products of operators (RepXspace calls this RepXspace_Prod).
# # The operator is specified in the argument x_ops, which is simply
# # a list of the symbolic names of the operators.
# # The arguments anorm and lambda_base specify the parameters that
# # determine the radial basis.
# # The returned matrix elements are all floating point numbers
# # (if the list of operators is empty, the identity matrix is returned).
# # The correct 4*Pi normalisation factors are included.
#
# # The final argument L_max is optional - if omitted then L_max=L_min,
# # so that a single angular momentum value is used.
#
#
# RepXspace_Prod:=proc(x_ops::list,
#                      anorm::algebraic,lambda_base::algebraic,
#                      nu_min::nonnegint,nu_max::nonnegint,
#                      v_min::nonnegint,v_max::nonnegint,
#                      L_min::nonnegint,L_max::nonnegint,$)
#     local sph_ops,nu_ops,run_Mat,xsp_Mat,this_op,up_running;
#     global Radial_Max,Spherical_Min,
#            Xspace_Pi,Xspace_PiPi2,Xspace_PiPi4,Xspace_PiqPi;
#
#   # Run through the list of operators left to right, storing
#   # independently those that act on the radial and spherical spaces.
#   # If/When we see the pi or [pi x pi] or [pi x q x pi] operators,
#   # we form the matrices and multiply them out.
#
#   up_running:=0:            # Flag to indicate that run_Mat contains summat
#   sph_ops:=[]: nu_ops:=[]:  # Accumulates operators from the left
#
#   for this_op in x_ops do
#
#     if member(this_op,Radial_Operators) then
#       nu_ops:=[op(nu_ops),this_op];     # store Radial Ops
#     elif member(this_op,Spherical_Operators) then
#       sph_ops:=[op(sph_ops),this_op];   # store Sph Ops
#     else
#
#       # we now expect an operator on the full Xspace, so we need to multiply
#       # out all those on the Radial and Spherical spaces so far accumulated.
#
#       if nu_ops<>[] or sph_ops<>[] then
#         xsp_Mat:=RepXspace_Twin(nu_ops,sph_ops,_passed[2..-1]):
#         nu_ops:=[]:   # used, so reset
#         sph_ops:=[]:  # ditto
#         if up_running>0 then
#           MatrixMatrixMultiply(run_Mat,xsp_Mat,inplace):
#         else          # nothing yet, so use xsp_Mat (not a copy)
#           run_Mat:=xsp_Mat:
#           up_running:=1:
#         fi:
#       fi:
#
#       # generate the Xspace operator as required
#
#       if this_op=Xspace_PiqPi then   # For operator  [pi x q x pi]_{v=3,L=0};
#           xsp_Mat:=RepXspace_PiqPi(_passed[2..-1]):
#
#       elif this_op=Xspace_PiPi2 then   # For operator  [pi x pi]_{v=2,L=2};
#           xsp_Mat:=RepXspace_PiPi(2,_passed[2..-1]):
#
#       elif this_op=Xspace_PiPi4 then   # For operator  [pi x pi]_{v=2,L=4};
#           xsp_Mat:=RepXspace_PiPi(4,_passed[2..-1]):
#
#       elif this_op=Xspace_Pi then   # For operator  [pi]_{v=1,L=2};
#           xsp_Mat:=RepXspace_Pi(_passed[2..-1]):
#
#       # could put other Xspace operators here!
#
#       else
#         error "Operator %1 undefined", this_op:
#       fi:
#
#       # Now multiply in this Xspace operator
#
#       if up_running>0 then
#         MatrixMatrixMultiply(run_Mat,xsp_Mat,inplace);
#       else
#         run_Mat:=copy(xsp_Mat):   # need a copy because of remember tables
#         up_running:=1:
#       fi:
#     fi:
#   od:
#
#   # And we must multiply out any remaining operators.
#
#   if nu_ops<>[] or sph_ops<>[] then
#     xsp_Mat:=RepXspace_Twin(nu_ops,sph_ops,_passed[2..-1]):
#
#     if up_running>0 then
#       MatrixMatrixMultiply(run_Mat,xsp_Mat,inplace):
#     else          # nothing yet, so use xsp_Mat (not a copy)
#       run_Mat:=xsp_Mat:
#       up_running:=1:
#     fi:
#   fi:
#
#   if up_running=0 then   # empty operator - need identity matrix
#     run_Mat:=Matrix([seq(1,i=1..dimXspace(_passed[4..-1]))],scan=diagonal):
#   fi:
#
#   run_Mat:
#
# end:
def RepXspace_Prod(x_ops: tuple[Symbol, ...],
                   anorm: Expr, lambda_base: Expr,
                   nu_min: nonnegint, nu_max: nonnegint,
                   v_min: nonnegint, v_max: nonnegint,
                   L_min: nonnegint, L_max: Optional[nonnegint]
                   ) -> Matrix:
    if L_max is None:
        L_max = L_min
    require_nonnegint_range('nu', nu_min, nu_max)
    require_nonnegint_range('v', v_min, v_max)
    require_nonnegint_range('L', L_min, L_max)

    run_Mat: Optional[Matrix] = None
    up_running: int = 0
    sph_ops: tuple[Symbol, ...] = ()
    nu_ops: tuple[Symbol, ...] = ()
    xsp_Mat: Matrix

    for this_op in x_ops:

        if this_op in Radial_Operators:
            nu_ops += (this_op,)
        elif this_op in Spherical_Operators:
            sph_ops += (this_op,)
        else:
            if nu_ops != () or sph_ops != ():
                xsp_Mat = RepXspace_Twin(nu_ops, sph_ops,
                                         anorm, lambda_base,
                                         nu_min, nu_max,
                                         v_min, v_max,
                                         L_min, L_max)
                nu_ops = ()
                sph_ops = ()
                if up_running > 0:
                    assert run_Mat is not None
                    run_Mat = run_Mat * xsp_Mat
                else:
                    assert run_Mat is None
                    run_Mat = xsp_Mat
                    up_running = 1

            if this_op == Xspace_PiqPi:
                xsp_Mat = RepXspace_PiqPi(anorm, lambda_base,
                                          nu_min, nu_max,
                                          v_min, v_max,
                                          L_min, L_max)
            elif this_op == Xspace_PiPi2:
                xsp_Mat = RepXspace_PiPi(2, anorm, lambda_base,
                                         nu_min, nu_max,
                                         v_min, v_max,
                                         L_min, L_max)
            elif this_op == Xspace_PiPi4:
                xsp_Mat = RepXspace_PiPi(4, anorm, lambda_base,
                                         nu_min, nu_max,
                                         v_min, v_max,
                                         L_min, L_max)
            elif this_op == Xspace_Pi:
                xsp_Mat = RepXspace_Pi(anorm, lambda_base,
                                       nu_min, nu_max,
                                       v_min, v_max,
                                       L_min, L_max)
            else:
                raise ValueError(f'Operator {this_op} undefined.')

            assert xsp_Mat is not None
            if up_running > 0:
                assert run_Mat is not None
                run_Mat = run_Mat * xsp_Mat
            else:
                assert run_Mat is None
                run_Mat = Matrix(xsp_Mat)
                up_running = 1

    if nu_ops != [] or sph_ops != []:
        xsp_Mat = RepXspace_Twin(nu_ops, sph_ops,
                                 anorm, lambda_base,
                                 nu_min, nu_max,
                                 v_min, v_max,
                                 L_min, L_max)

        if up_running > 0:
            assert run_Mat is not None
            run_Mat = run_Mat * xsp_Mat
        else:
            assert run_Mat is None
            run_Mat = xsp_Mat
            up_running = 1

    if up_running == 0:
        assert run_Mat is None
        run_Mat = eye(dimXspace(nu_min, nu_max,
                                v_min, v_max,
                                L_min, L_max))

    assert run_Mat is not None
    return run_Mat


# # The following procedure RepXspace_Twin does much of the work
# # for RepXspace_Prod above, and has similar arguments, except
# # that it takes two lists of operators, rad_ops and sph_ops.
# # The former is a product of the radial operators from Table I,
# # while the latter is a product of spherical operators from Table II
# # together with the diagonal operators SpDiag_sqLdim and SpDiag_sqLdiv.
# # The Matrix that is returned is the combined action on the truncated
# # cross-product Hilbert space that is determined by the remaining
# # arguments as above. The radial and spherical actions are independent,
# # although the radial states have a dependence on seniority (see (8)).
# # Note that the correct 4*Pi factors are applied here, so that the
# # matrix elements returned are genuine alternative SO(3)-reduced.
#
# # The final argument L_max is optional - if omitted then L_max=L_min,
# # so that a single angular momentum value is used.
#
# # Note that the matrix elements are all determined analytically if
# # and only if, the degree of the radial operator has the same parity
# # (odd or even) as the total seniority of the spherical operator.
# # Otherwise, they are determined non-analytically (through the taking
# # of a matrix square root).
#
# # It might be thought that constructing the representation matrix
# # directly from blocks coming from the tensor product, as follows,
# #  direct_Mat:=
# #  Matrix(
# #  [ seq( [ seq(
# #    `if`(sph_Mat[i2,j2]=0,Matrix(rad_dim,fill=0.0),
# #           sph_Mat[i2,j2]*evalf(RepRadial_Prod_rem(rad_ops,anorm,
# #                                  lambda_base+glb_lam_fun(sph_labels[j2][1]),
# #                                  glb_lam_fun(sph_labels[i2][1])-
# #                                              glb_lam_fun(sph_labels[j2][1]),
# #                                  nu_min,nu_max,glb_nu_lap))),
# #                j2=1..sph_dim ) ],
# #                i2=1..sph_dim ) ],
# #         datatype=float
# #        ):
# # would be more efficient, but it is actually a lot slower (over 10x).
# # It's even slower if we take out the 0 test.
#
#
# RepXspace_Twin:=proc(rad_ops::list, sph_ops::list,
#                      anorm::algebraic, lambda_base::algebraic,
#                      nu_min::nonnegint, nu_max::nonnegint,
#                      v_min::nonnegint, v_max::nonnegint,
#                      L_min::nonnegint, L_max::nonnegint,$)
#     local j2,i2,j1,i1,jdisp,idisp,lambda_disp_init,lambda_disp_fin,
#           rad_dim,rad_Mat,st,
#           sph_dim,sph_labels,sph_Mat,sph_ME,
#           direct_Mat;
#     global glb_lam_fun,glb_nu_lap:=0,glb_time:
#
#
#   # Obtain dim, labels, and representation matrix for the spherical operator
#
#   sph_dim:=dimSO5r3_rngVvarL(_passed[7..-1]);
#   sph_labels:=lbsSO5r3_rngVvarL(_passed[7..-1]);
#   sph_Mat:=RepSO5r3_Prod_rem(sph_ops,_passed[7..-1]);
#
#   # Now include the (4*Pi) factors in the latter:
#
#   sph_Mat:=MatrixScalarMultiply(sph_Mat,
#               evalf(Convert_red^NumSO5r3_Prod(sph_ops)));
#
#   # dimension of radial space:
#
#   rad_dim:=dimRadial(nu_min,nu_max);
#
#   # Now form the direct product representations on the space of
#   # dimension sph_dim*rad_dim.
#
#   direct_Mat:=Matrix(sph_dim*rad_dim,datatype=float);
#
#   # Place the entries one-by-one into the direct product matrix.
#   # (j1;j2) is initial state, (i1;i2) is final state
#   # 1st label is radial and varies quickest, 2nd is spherical and slowest.
#
#   # For the radial (nu) part, the rep matrix depends on the initial
#   # and final values of v: these determine the lambdas mapped between.
#
# #  st:=time():
#
#   for j2 to sph_dim do
#     jdisp:=(j2-1)*rad_dim:
#     lambda_disp_init:=glb_lam_fun(sph_labels[j2][1]):
#
#   for i2 to sph_dim do
#     idisp:=(i2-1)*rad_dim:
#     lambda_disp_fin:=glb_lam_fun(sph_labels[i2][1]):
#     sph_ME:=sph_Mat[i2,j2]:
#
#     if sph_ME=0 then  # skip zero cases of spherical MEs.
#       next
#     fi:
#
#     # Form representation on the radial space, taking account
#     # of the correct lambda variation. Use the version with the
#     # remember option because it might need to be reused here.
#
#     rad_Mat:=RepRadial_Prod_rem(rad_ops,anorm,
#                                   lambda_base+lambda_disp_init,
#                                   lambda_disp_fin-lambda_disp_init,
#                                   nu_min,nu_max,glb_nu_lap):
#
#     for i1 to rad_dim do
#     for j1 to rad_dim do
#       direct_Mat[idisp+i1,jdisp+j1]:=evalf(rad_Mat[i1,j1]*sph_ME);
#     od: od:
#   od: od:
#
#   direct_Mat;
# end:
def RepXspace_Twin(rad_ops: tuple[Symbol, ...], sph_ops: tuple[Symbol, ...],
                   anorm: Expr, lambda_base: Expr,
                   nu_min: nonnegint, nu_max: nonnegint,
                   v_min: nonnegint, v_max: nonnegint,
                   L_min: nonnegint, L_max: Optional[nonnegint]
                   ) -> Matrix:
    if L_max is None:
        L_max = L_min
    require_nonnegint_range('nu', nu_min, nu_max)
    require_nonnegint_range('v', v_min, v_max)
    require_nonnegint_range('L', L_min, L_max)

    globals.glb_nu_lap = 0

    sph_dim: int = dimSO5r3_rngVvarL(v_min, v_max, L_min, L_max)
    sph_labels: list[SO5SO3Label] = lbsSO5r3_rngVvarL(v_min, v_max, L_min, L_max)
    sph_Mat: Matrix = RepSO5r3_Prod_rem(sph_ops, v_min, v_max, L_min, L_max)

    sph_Mat = (Convert_red ** NumSO5r3_Prod(sph_ops)).evalf() * sph_Mat

    rad_dim: int = dimRadial(nu_min, nu_max)

    direct_Mat: Matrix = zeros(sph_dim * rad_dim)
    for j2 in range(1, sph_dim + 1):
        jdisp: int = (j2 - 1) * rad_dim
        lambda_disp_init = glb_lam_fun(sph_labels[j2 - 1][0])

        for i2 in range(1, sph_dim + 1):
            idisp: int = (i2 - 1) * rad_dim
            lambda_disp_fin = glb_lam_fun(sph_labels[i2 - 1][0])
            sph_ME: float = sph_Mat[i2 - 1][j2 - 1]

            if sph_ME == 0:
                continue

            rad_Mat: Matrix = RepRadial_Prod_rem(tuple(rad_ops), anorm,
                                                 lambda_base + lambda_disp_init,
                                                 lambda_disp_fin - lambda_disp_init,
                                                 nu_min, nu_max, globals.glb_nu_lap)

            for i1 in range(1, rad_dim + 1):
                for j1 in range(1, rad_dim + 1):
                    direct_Mat[idisp + i1 - 1, jdisp + j1 - 1] = (rad_Mat[i1 - 1, j1 - 1] * sph_ME).evalf()

    return direct_Mat


# # The following procedure RepXpsace_Pi returns the Matrix representation
# # of the pi/(-i\hbar) operator on the truncated Hilbert space
# # determined by the arguments as above.
# # The returned matrix elements are alternative SO(3)-reduced matrix elements.
# # They are calculated using (53). The result should be antihermitian.
#
# # If an exotic coefficient (such as a function of NUMBER, SENIORITY,
# # ANGMOM or ALFA) is required, the procedure RepXspace can be used
# # (it calls this one).
#
# RepXspace_Pi:=proc( anorm::algebraic, lambda_base::algebraic,
#                     nu_min::nonnegint, nu_max::nonnegint,
#                     v_min::nonnegint, v_max::nonnegint,
#                     L_min::nonnegint, L_max::nonnegint,$)
#     option remember;
#     local j2,i2,j1,i1,jdisp,idisp,lambda_disp_init,lambda_disp_fin,
#           v_init,al_init,L_init,v_fin,al_fin,L_fin,v_chg,
#           sph_dim,sph_labels,
#           rad_dim,rad_Mat,direct_Mat,CG2;
#     global glb_lam_fun,Radial_Db,Radial_bm;
#
#   # dimension of radial space:
#
#   rad_dim:=dimRadial(nu_min,nu_max);
#
#   # Obtain dim and labels for S5 space.
#
#   sph_dim:=dimSO5r3_rngVvarL(_passed[5..-1]);
#   sph_labels:=lbsSO5r3_rngVvarL(_passed[5..-1]);
#
#   # Will form the representation on the sph_dim*rat_dim dimensional
#   # direct product space in the following Matrix, which is returned.
#
#   direct_Mat:=Matrix(sph_dim*rad_dim,datatype=float);
#
#   # Place the entries one-by-one into the direct product matrix.
#   # (j1;j2) is initial state, (i1;i2) is final state.
#   # 1st label is radial, 2nd is spherical, and varies slowest.
#
#   # For the radial (nu) part, the rep matrix depends on the initial
#   # and final values of v: these determine the lambdas mapped between.
#
#   for j2 to sph_dim do
#     v_init:=sph_labels[j2][1]:   # seniority of initial state
#     al_init:=sph_labels[j2][2]:  # alpha of same
#     L_init:=sph_labels[j2][3]:   # L of same
#     jdisp:=(j2-1)*rad_dim:
#     lambda_disp_init:=glb_lam_fun(v_init):
#
#   for i2 to sph_dim do
#     L_fin:=sph_labels[i2][3]:    # L of final state
#     if L_fin-L_init>2 or L_fin-L_init<-2 then next fi:  # zero because q has L=2.
#
#     v_fin:=sph_labels[i2][1]:    # seniority of final state
#     al_fin:=sph_labels[i2][2]:   # alpha of same
#     v_chg:=v_fin-v_init:         # change in seniority
#     idisp:=(i2-1)*rad_dim:
#     lambda_disp_fin:=glb_lam_fun(v_fin):
#
#
#     # Now obtain the (SO(5) reduced) representation matrix between these
#     # subspaces having constant spherical labels by treating separately
#     # the cases v_chg = 1 (using (53a)) and -1 (using (53b)).
#
#     if v_chg = 1 then
#
#        rad_Mat:=RepRadial_LC_rem(
#                        [ [1,[Radial_Db]],[-v_init-2,[Radial_bm]] ],
#                        anorm, lambda_base+lambda_disp_init,
#                        lambda_disp_fin-lambda_disp_init, nu_min, nu_max):
#
#       # multiply this rad_Mat radial action by the SO(5) reduced ME
#       # from (45).
#       # Note that we can't do this 'inplace' because this will affect the
#       # remember tables in RepRadial_LC_rem.
#
#       rad_Mat:=MatrixScalarMultiply(rad_Mat,evalf(Qred_p1(v_init)));
#
#     elif v_chg = -1 then
#
#        rad_Mat:=RepRadial_LC_rem(
#                        [ [1,[Radial_Db]],[v_init+1,[Radial_bm]] ],
#                        anorm, lambda_base+lambda_disp_init,
#                        lambda_disp_fin-lambda_disp_init, nu_min, nu_max):
#
#       # multiply this nu_Mat radial action by the SO(5) reduced ME
#
#       rad_Mat:=MatrixScalarMultiply(rad_Mat,evalf(Qred_m1(v_init)));
#
#     else
#       next           # skip this (j1,i1) case (because it is zero).
#     fi:
#
#     # The "alternative" SO(3)-reduced matrix element is obtained from the
#     # SO(5)-reduced ME calculated above by multiplying with the following
#     # (we could also multiply by sqrt(dimSO3(L_fin)) here to get genuine
#     #  SO(3)-reduced matrix elements):
#
#     CG2:=CG_SO5r3(v_init,al_init,L_init,1,1,2,v_fin,al_fin,L_fin):
#
#     # fill in the Xspace elements for these constant spherical
#     # parameters (i2,j2).
#
#     for i1 to rad_dim do
#     for j1 to rad_dim do
#       direct_Mat[idisp+i1,jdisp+j1]:=evalf(CG2*rad_Mat[i1,j1]);
#     od: od:
#   od: od:
#
#   direct_Mat:
# end:
@cache
def RepXspace_Pi(anorm: Expr, lambda_base: Expr,
                 nu_min: nonnegint, nu_max: nonnegint,
                 v_min: nonnegint, v_max: nonnegint,
                 L_min: nonnegint, L_max: nonnegint
                 ) -> Matrix:
    require_nonnegint_range('nu', nu_min, nu_max)
    require_nonnegint_range('v', v_min, v_max)
    require_nonnegint_range('L', L_min, L_max)

    rad_dim: int = dimRadial(nu_min, nu_max)

    sph_dim: int = dimSO5r3_rngVvarL(v_min, v_max, L_min, L_max)
    sph_labels: list[SO5SO3Label] = lbsSO5r3_rngVvarL(v_min, v_max, L_min, L_max)
    assert sph_dim == len(sph_labels)

    direct_Mat: Matrix = Matrix(sph_dim * rad_dim)
    for j2 in range(1, sph_dim + 1):
        v_init, al_init, L_init = sph_labels[j2 - 1]
        jdisp: int = (j2 - 1) * rad_dim
        lambda_disp_init: nonnegint = glb_lam_fun(v_init)

        for i2 in range(1, sph_dim + 1):
            v_fin, al_fin, L_fin = sph_labels[i2 - 1]
            if L_fin - L_init > 2 or L_fin - L_init < -2:
                continue
            v_chg: int = v_fin - v_init
            idisp: int = (i2 - 1) * rad_dim
            lambda_disp_fin: nonnegint = glb_lam_fun(v_fin)

            rad_Mat: Matrix
            if v_chg == 1:

                rad_Mat = RepRadial_LC_rem(((S.One, (Radial_Db,)),
                                            (S(-v_init - 2), (Radial_bm,))),
                                           anorm, lambda_base + lambda_disp_init,
                                           lambda_disp_fin - lambda_disp_init, nu_min, nu_max)
                rad_Mat = rad_Mat * (Qred_p1(v_init)).evalf()

            elif v_chg == -1:

                rad_Mat = RepRadial_LC_rem(((S.One, (Radial_Db,)),
                                            (S(v_init + 1), (Radial_bm,))),
                                           anorm, lambda_base + lambda_disp_init,
                                           lambda_disp_fin - lambda_disp_init, nu_min, nu_max)
                rad_Mat = rad_Mat * (Qred_m1(v_init)).evalf()

            else:
                continue

            CG2: float = CG_SO5r3(v_init, al_init, L_init,
                                  1, 1, 2,
                                  v_fin, al_fin, L_fin)

            for i1 in range(1, rad_dim + 1):
                for j1 in range(1, rad_dim + 1):
                    direct_Mat[idisp + i1 - 1, jdisp + j1 - 1] = (CG2 * rad_Mat[i1 - 1, j1 - 1]).evalf()

    return direct_Mat


# # The following procedure RepXpsace_PiPi returns Matrix representations
# # of the operators
# #            [pi x pi]_(v=2,L=2)          [pi x pi]_(v=2,L=4)
# #            -------------------   and    ------------------- ,
# #                  hbar^2                      hbar^2
# # for PiPi_L = 2 or 4 respectively, on the truncated Hilbert spaces
# # determined by the other arguments as above.
# # The returned matrix elements are alternative SO(3)-reduced matrix elements.
# # They are calculated using (D11), with (D3).
# # The result deviates slightly from being hermitian due to truncation effects.
#
# # If an exotic coefficient (such as a function of NUMBER, SENIORITY,
# # ANGMOM or ALFA) is required, the procedure RepXspace can be used
# # (it calls this one).
#
# RepXspace_PiPi:=proc(PiPi_L::nonnegint,
#                      anorm::algebraic, lambda_base::algebraic,
#                      nu_min::nonnegint, nu_max::nonnegint,
#                      v_min::nonnegint, v_max::nonnegint,
#                      L_min::nonnegint, L_max::nonnegint,$)
#     option remember;
#     local j2,i2,j1,i1,jdisp,idisp,lambda_disp_init,lambda_disp_fin,
#           v_init,al_init,L_init,v_fin,al_fin,L_fin,v_chg,
#           sph_dim,sph_labels,
#           rad_dim,rad_Mat,direct_Mat,CG2;
#     global glb_lam_fun,Radial_D2b,Radial_bm2,Radial_bDb;
#
#   # dimension of radial space:
#
#   rad_dim:=dimRadial(nu_min,nu_max);
#
#   # Obtain dim and labels for S5 space.
#
#   sph_dim:=dimSO5r3_rngVvarL(_passed[6..-1]);
#   sph_labels:=lbsSO5r3_rngVvarL(_passed[6..-1]);
#
#   # Will form the representation on the sph_dim*rat_dim dimensional
#   # direct product space in the following Matrix, which is returned.
#
#   direct_Mat:=Matrix(sph_dim*rad_dim,datatype=float);
#
#   # Place the entries one-by-one into the direct product matrix.
#   # (j1;j2) is initial state, (i1;i2) is final state.
#   # 1st label is radial, 2nd is spherical, and varies slowest.
#
#   # For the radial (nu) part, the rep matrix depends on the initial
#   # and final values of v: these determine the lambdas mapped between.
#
#   for j2 to sph_dim do
#     v_init:=sph_labels[j2][1]:   # seniority of initial state
#     al_init:=sph_labels[j2][2]:  # alpha of same
#     L_init:=sph_labels[j2][3]:   # L of same
#     jdisp:=(j2-1)*rad_dim:
#     lambda_disp_init:=glb_lam_fun(v_init):
#
#   for i2 to sph_dim do
#     L_fin:=sph_labels[i2][3]:    # L of final state
#     if L_fin-L_init>PiPi_L or L_fin-L_init<-PiPi_L then next fi: # zero
#
#     v_fin:=sph_labels[i2][1]:    # seniority of final state
#     al_fin:=sph_labels[i2][2]:   # alpha of same
#     v_chg:=v_fin-v_init:         # change in seniority
#     idisp:=(i2-1)*rad_dim:
#     lambda_disp_fin:=glb_lam_fun(v_fin):
#
#
#     # Now obtain the (SO(5) reduced) representation matrix on this
#     # subspace with constant spherical labels by treating separately
#     # the cases v_chg = 2 and -2 and 0 (all using (D11) ).
#
#     if v_chg = 2 then
#
#        rad_Mat:=RepRadial_LC_rem( [ [1,[Radial_D2b]],
#                                    [(v_init+2)*(v_init+4),[Radial_bm2]],
#                                    [-2*v_init-5,[Radial_bm2,Radial_bDb]] ],
#                                anorm, lambda_base+lambda_disp_init,
#                                lambda_disp_fin-lambda_disp_init,
#                                nu_min, nu_max):
#
#       # multiply this nu_Mat radial action by the SO(5) reduced ME
#       # from (D2) (the minus sign comes from the i^2 (*hbar^2) )
#       # Note that we can't do this 'inplace' because this will affect the
#       # remember tables in RepRadial_LC_rem.
#
#       rad_Mat:=MatrixScalarMultiply(rad_Mat,-evalf(QxQred_p2(v_init)));
#
#     elif v_chg = -2 then
#
#        rad_Mat:=RepRadial_LC_rem( [ [1,[Radial_D2b]],
#                                    [(v_init-1)*(v_init+1),[Radial_bm2]],
#                                    [2*v_init+1,[Radial_bm2,Radial_bDb]] ],
#                                anorm, lambda_base+lambda_disp_init,
#                                lambda_disp_fin-lambda_disp_init,
#                                nu_min, nu_max):
#
#       # multiply this nu_Mat radial action by the SO(5) reduced ME
#
#       rad_Mat:=MatrixScalarMultiply(rad_Mat,-evalf(QxQred_m2(v_init)));
#
#     elif v_chg = 0 then
#
#        rad_Mat:=RepRadial_LC_rem( [ [1,[Radial_D2b]],
#                                    [-(v_init+1)*(v_init+2),[Radial_bm2]] ],
#                                anorm, lambda_base+lambda_disp_init,
#                                lambda_disp_fin-lambda_disp_init,
#                                nu_min, nu_max):
#
#       # multiply this nu_Mat radial action by the SO(5) reduced ME
#
#       rad_Mat:=MatrixScalarMultiply(rad_Mat,-evalf(QxQred_0(v_init)));
#     else
#       next           # skip this (j1,i1) case (because it is zero).
#     fi:
#
#
#     # The "alternative" SO(3)-reduced matrix element is obtained from the
#     # SO(5)-reduced ME calculated above by multiplying with the following
#     # (we could multiply by sqrt(dimSO3(L_fin)) here to get genuine
#     #  SO(3)-reduced matrix elements)
#     # (PiPi_L should be 2 or 4 here, else we'll get 0):
#
#     CG2:=CG_SO5r3(v_init,al_init,L_init,2,1,PiPi_L,v_fin,al_fin,L_fin):
#
#     # fill in the Xspace elements for these constant spherical
#     # parameters (i2,j2).
#
#     for i1 to rad_dim do
#     for j1 to rad_dim do
#       direct_Mat[idisp+i1,jdisp+j1]:=evalf(CG2*rad_Mat[i1,j1]);
#     od: od:
#   od: od:
#
#   # This now correct for PiPi_L=4, but the sign needs to change for PiPi_L=2
#   # (see sign in (D3)).
#
#   if PiPi_L=2 then
#       MatrixScalarMultiply(direct_Mat,-1,inplace);
#   fi:
#
#   direct_Mat:
# end:
@cache
def RepXspace_PiPi(PiPi_L: nonnegint,
                   anorm: Expr, lambda_base: Expr,
                   nu_min: nonnegint, nu_max: nonnegint,
                   v_min: nonnegint, v_max: nonnegint,
                   L_min: nonnegint, L_max: nonnegint
                   ) -> Matrix:
    require_nonnegint('PiPi_L', PiPi_L)
    require_nonnegint_range('nu', nu_min, nu_max)
    require_nonnegint_range('v', v_min, v_max)
    require_nonnegint_range('L', L_min, L_max)

    rad_dim: int = dimRadial(nu_min, nu_max)

    sph_dim: int = dimSO5r3_rngVvarL(v_min, v_max, L_min, L_max)
    sph_labels: list[SO5SO3Label] = lbsSO5r3_rngVvarL(v_min, v_max, L_min, L_max)

    direct_Mat: Matrix = Matrix(sph_dim * rad_dim)

    for j2 in range(1, sph_dim + 1):
        v_init, al_init, L_init = sph_labels[j2 - 1]
        jdisp: int = (j2 - 1) * rad_dim
        lambda_disp_init: int = glb_lam_fun(v_init)

        for i2 in range(1, sph_dim + 1):
            v_fin, al_fin, L_fin = sph_labels[i2 - 1]
            if L_fin - L_init > PiPi_L or L_fin - L_init < -PiPi_L:
                continue

            v_chg: int = v_fin - v_init
            idisp: int = (i2 - 1) * rad_dim
            lambda_disp_fin: int = glb_lam_fun(v_fin)

            if v_chg == 2:

                rad_Mat = RepRadial_LC_rem(((S.One, (Radial_D2b,)),
                                            (S((v_init + 2) * (v_init + 4)), (Radial_bm2,)),
                                            (S(-2 * v_init - 5), (Radial_bm2, Radial_bDb))),
                                           anorm, lambda_base + lambda_disp_init,
                                           lambda_disp_fin - lambda_disp_init,
                                           nu_min, nu_max)

                rad_Mat = rad_Mat * (-QxQred_p2(v_init)).evalf()

            elif v_chg == -2:

                rad_Mat = RepRadial_LC_rem(((S.One, (Radial_D2b,)),
                                            (S((v_init - 1) * (v_init + 1)), (Radial_bm2,)),
                                            (S(2 * v_init + 1), (Radial_bm2, Radial_bDb))),
                                           anorm, lambda_base + lambda_disp_init,
                                           lambda_disp_fin - lambda_disp_init,
                                           nu_min, nu_max)

                rad_Mat = rad_Mat * (-QxQred_p2(v_init)).evalf()

            elif v_chg == 0:

                rad_Mat = RepRadial_LC_rem(((S.One, (Radial_D2b,)),
                                            (S(-(v_init + 1) * (v_init + 2)), (Radial_bm2,))),
                                           anorm, lambda_base + lambda_disp_init,
                                           lambda_disp_fin - lambda_disp_init,
                                           nu_min, nu_max)

                rad_Mat = rad_Mat * (-QxQred_0(v_init)).evalf()

            else:
                continue

            CG2: float = CG_SO5r3(v_init, al_init, L_init,
                                  2, 1, PiPi_L,
                                  v_fin, al_fin, L_fin)

            for i1 in range(1, rad_dim + 1):
                for j1 in range(1, rad_dim + 1):
                    direct_Mat[idisp + i1 - 1, jdisp + j1 - 1] = (CG2 * rad_Mat[i1 - 1, j1 - 1]).evalf()

            if PiPi_L == 2:
                direct_Mat = -direct_Mat

    return direct_Mat


# # The following procedure RepXspace_PiqPi returns the Matrix representation
# # of the operator
# #                         [pi x q x pi]_(v=3,L=0)
# #                         -----------------------
# #                                 hbar^2
# # on the truncated Hilbert space determined by the arguments as above.
# # The returned matrix elements are alternative SO(3)-reduced matrix elements.
# # They are calculated using (D12) & (D14).
# # The result deviates slightly from being hermitian due to truncation effects.
#
# # If an exotic coefficient (such as a function of NUMBER, SENIORITY,
# # ANGMOM or ALFA) is required, the procedure RepXspace can be used
# # (it calls this one).
#
#
# RepXspace_PiqPi:=proc( anorm::algebraic, lambda_base::algebraic,
#                        nu_min::nonnegint, nu_max::nonnegint,
#                        v_min::nonnegint, v_max::nonnegint,
#                        L_min::nonnegint, L_max::nonnegint,$)
#     option remember;
#     local j2,i2,j1,i1,jdisp,idisp,lambda_disp_init,lambda_disp_fin,
#           v_init,al_init,L_init,v_fin,al_fin,L_fin,v_chg,
#           sph_dim,sph_labels,
#           rad_dim,rad_Mat,rad_Mat2,direct_Mat,CG2;
#     global glb_lam_fun,Radial_bm2,Radial_D2b,Radial_bDb,
#                        Radial_b,Radial_Db,Radial_bm;
#
#   # dimension of radial space:
#
#   rad_dim:=dimRadial(nu_min,nu_max);
#
#   # Obtain dim and labels for S5 space.
#
#   sph_dim:=dimSO5r3_rngVvarL(_passed[5..-1]);
#   sph_labels:=lbsSO5r3_rngVvarL(_passed[5..-1]);
#
#   # Will form the representation on the sph_dim*rat_dim dimensional
#   # direct product space in the following Matrix, which is returned.
#
#   direct_Mat:=Matrix(sph_dim*rad_dim,datatype=float);
#
#   # Place the entries one-by-one into the direct product matrix.
#   # (j1;j2) is initial state, (i1;i2) is final state.
#   # 1st label is radial, 2nd is spherical, and varies slowest.
#
#   # For the radial (nu) part, the rep matrix depends on the initial
#   # and final values of v: these determine the lambdas mapped between.
#
#   for j2 to sph_dim do
#     v_init:=sph_labels[j2][1]:   # seniority of initial state
#     al_init:=sph_labels[j2][2]:  # alpha of same
#     L_init:=sph_labels[j2][3]:   # L of same
#     jdisp:=(j2-1)*rad_dim:
#     lambda_disp_init:=glb_lam_fun(v_init):
#
#   for i2 to sph_dim do
#     L_fin:=sph_labels[i2][3]:    # L of final state
#     if L_fin<>L_init then next fi:   # need L's equal for this operator
#     v_fin:=sph_labels[i2][1]:    # seniority of final state
#     al_fin:=sph_labels[i2][2]:   # alpha of same
#     v_chg:=v_fin-v_init:         # change in seniority
#     idisp:=(i2-1)*rad_dim:
#     lambda_disp_fin:=glb_lam_fun(v_fin):
#
#     # Now obtain the (SO(5) reduced) representation matrix on this
#     # subspace with constant spherical labels by treating separately
#     # the cases v_chg = 3 (using (D12a)) and -3 (using (D12b))
#     # and 1 (using (D14a)) and -1 (using (D14b)).
#     # The SO(5)>SO(3) CG coefficient is left until the end.
#     # (Note that here, we use a sixth parameter 1 to RepRadial_LC_rem:
#     # this temporarily expands the size of the radial space used -
#     # to get a more accurate matrix).
#
#     if v_chg = 3 then
#
#        rad_Mat:=RepRadial_LC_rem( [ [1,[Radial_b,Radial_D2b]],
#                                    [(v_init+2)*(v_init+4),[Radial_bm]],
#                                    [-2*v_init-5,[Radial_Db]] ],
#                                anorm, lambda_base+lambda_disp_init,
#                                lambda_disp_fin-lambda_disp_init,
#                                nu_min, nu_max,1):
#
#
#       # multiply this rad_Mat radial action by the SO(5) reduced ME
#       # from (D4) (the minus sign in (D4) cancels that in (D12), which
#       # comes from the i^2 (*hbar^2) ).
#       # Note that we can't do this 'inplace' because this will affect the
#       # remember tables in RepRadial_LC_rem.
#
#       rad_Mat:=MatrixScalarMultiply(rad_Mat,evalf(QxQxQred_p3(v_init)));
#
#     elif v_chg = -3 then
#
#        rad_Mat:=RepRadial_LC_rem( [ [1,[Radial_b,Radial_D2b]],
#                                    [(v_init-1)*(v_init+1),[Radial_bm]],
#                                    [2*v_init+1,[Radial_Db]] ],
#                                anorm, lambda_base+lambda_disp_init,
#                                lambda_disp_fin-lambda_disp_init,
#                                nu_min, nu_max,1):
#
#       # multiply this rad_Mat radial action by the SO(5) reduced ME
#
#       rad_Mat:=MatrixScalarMultiply(rad_Mat,evalf(QxQxQred_m3(v_init)));
#
#     elif v_chg = 1 then
#
#        rad_Mat:=RepRadial_LC_rem( [ [1,[Radial_b,Radial_D2b]],
#                                    [-(v_init+1)*(v_init+2),[Radial_bm]] ],
#                                anorm, lambda_base+lambda_disp_init,
#                                lambda_disp_fin-lambda_disp_init,
#                                nu_min, nu_max):
#        rad_Mat2:=RepRadial_LC_rem( [ [1,[Radial_Db]],
#                                  [-v_init-2,[Radial_bm]] ],
#                                anorm, lambda_base+lambda_disp_init,
#                                lambda_disp_fin-lambda_disp_init,
#                                nu_min, nu_max):
#
#       # combine rad_Mat and rad_Mat2 radials with appropriate SO(5) reduced MEs
#       # Note that for the first term, the minus sign in (D4) cancels one in (D14a).
#
#       rad_Mat:=MatrixAdd(rad_Mat,rad_Mat2,
#                  +evalf(QxQxQred_p1(v_init)),
#                  +evalf((2*v_init+5)*QixQxQred(v_init,v_fin,v_fin+1)))
#
#     elif v_chg = -1 then
#
#        rad_Mat:=RepRadial_LC_rem( [ [1,[Radial_b,Radial_D2b]],
#                                    [-(v_init+1)*(v_init+2),[Radial_bm]] ],
#                                anorm, lambda_base+lambda_disp_init,
#                                lambda_disp_fin-lambda_disp_init,
#                                nu_min, nu_max):
#        rad_Mat2:=RepRadial_LC_rem( [ [1,[Radial_Db]],
#                                  [v_init+1,[Radial_bm]] ],
#                                anorm, lambda_base+lambda_disp_init,
#                                lambda_disp_fin-lambda_disp_init,
#                                nu_min, nu_max):
#
#       # combine rad_Mat and rad_Mat2 radials with appropriate SO(5) reduced MEs
#
#       rad_Mat:=MatrixAdd(rad_Mat,rad_Mat2,
#                  +evalf(QxQxQred_m1(v_init)),
#                  -evalf((2*v_init+1)*QixQxQred(v_init,v_fin,v_fin-1)))
#
#     else
#       next           # skip this (j1,i1) case (because it is zero).
#     fi:
#
#     # The "alternative" SO(3)-reduced matrix element is obtained from the
#     # SO(5)-reduced ME calculated above by multiplying with the following
#     # (we could multiply by sqrt(dimSO3(L_fin)) here to get genuine
#     #  SO(3)-reduced matrix elements)
#
#     CG2:=CG_SO5r3(v_init,al_init,L_init,3,1,0,v_fin,al_fin,L_fin):
#
#     # fill up the Xspace elements for these constant spherical
#     # parameters (i2,j2).
#
#     for i1 to rad_dim do
#     for j1 to rad_dim do
#       direct_Mat[idisp+i1,jdisp+j1]:=evalf(CG2*rad_Mat[i1,j1]);
#     od: od:
#   od: od:
#
#   direct_Mat:
# end:
@cache
def RepXspace_PiqPi(anorm: Expr, lambda_base: Expr,
                    nu_min: nonnegint, nu_max: nonnegint,
                    v_min: nonnegint, v_max: nonnegint,
                    L_min: nonnegint, L_max: nonnegint
                    ) -> Matrix:
    print('Not implemented.')
    require_nonnegint_range('nu', nu_min, nu_max)
    require_nonnegint_range('v', v_min, v_max)
    require_nonnegint_range('L', L_min, L_max)

    rad_dim: int = dimRadial(nu_min, nu_max)

    sph_dim: int = dimSO5r3_rngVvarL(v_min, v_max, L_min, L_max)
    sph_labels: list[SO5SO3Label] = lbsSO5r3_rngVvarL(v_min, v_max, L_min, L_max)

    direct_Mat: Matrix = Matrix(sph_dim * rad_dim)

    for j2 in range(1, sph_dim + 1):
        v_init, al_init, L_init = sph_labels[j2 - 1]
        jdisp: int = (j2 - 1) * rad_dim
        lambda_disp_init: int = glb_lam_fun(v_init)

        for i2 in range(1, sph_dim + 1):
            v_fin, al_fin, L_fin = sph_labels[i2 - 1]
            if L_fin != L_init:
                continue
            v_chg: int = v_fin - v_init
            idisp: int = (i2 - 1) * rad_dim
            lambda_disp_fin = glb_lam_fun(v_fin)

            op_sum: OperatorSum
            op_sum2: OperatorSum
            rad_Mat: Matrix
            rad_Mat2: Matrix
            c: float
            c2: float
            if v_chg == 3:

                op_sum = ((S.One, (Radial_b, Radial_D2b)),
                          (S((v_init + 2) * (v_init + 4)), (Radial_bm,)),
                          (S(-2 * v_init - 5), (Radial_Db,)))
                rad_Mat = RepRadial_LC_rem(op_sum,
                                           anorm, lambda_base + lambda_disp_init,
                                           lambda_disp_fin - lambda_disp_init,
                                           nu_min, nu_max)
                c = QxQxQred_p3(v_init).evalf()
                rad_Mat = rad_Mat * c

            elif v_chg == -3:

                op_sum = ((S.One, (Radial_b, Radial_D2b)),
                          (S((v_init - 1) * (v_init + 1)), (Radial_bm,)),
                          (S(2 * v_init + 1), (Radial_Db,)))
                rad_Mat = RepRadial_LC_rem(op_sum,
                                           anorm, lambda_base + lambda_disp_init,
                                           lambda_disp_fin - lambda_disp_init,
                                           nu_min, nu_max)
                c = QxQxQred_m3(v_init).evalf()
                rad_Mat = rad_Mat * c

            elif v_chg == 1:

                op_sum = ((S.One, (Radial_b, Radial_D2b)),
                          (S(-(v_init + 1) * (v_init + 2)), (Radial_bm,)))
                op_sum2 = ((S.one, (Radial_Db,)),
                           (S(-v_init - 2), (Radial_bm,)))
                rad_Mat = RepRadial_LC_rem(op_sum,
                                           anorm, lambda_base + lambda_disp_init,
                                           lambda_disp_fin - lambda_disp_init,
                                           nu_min, nu_max)
                rad_Mat2 = RepRadial_LC_rem(op_sum2,
                                            anorm, lambda_base + lambda_disp_init,
                                            lambda_disp_fin - lambda_disp_init,
                                            nu_min, nu_max)
                c = QmxQxQred_p1(v_init).evalf()
                c2 = ((2 * v_init + 5) * QixQxQred(v_init, v_fin, v_fin + 1)).evalf()
                rad_Mat = rad_Mat * c + rad_Mat2 * c2

            elif v_chg == -1:

                op_sum = ((S.One, (Radial_b, Radial_D2b)),
                          (S(-(v_init + 1) * (v_init + 2)), (Radial_bm,)))
                op_sum2 = ((S.One, (Radial_Db,)),
                           (S(v_init + 1), (Radial_bm,)))
                rad_Mat = RepRadial_LC_rem(op_sum,
                                           anorm, lambda_base + lambda_disp_init,
                                           lambda_disp_fin - lambda_disp_init,
                                           nu_min, nu_max)
                rad_Mat2 = RepRadial_LC_rem(op_sum2,
                                            anorm, lambda_base + lambda_disp_init,
                                            lambda_disp_fin - lambda_disp_init,
                                            nu_min, nu_max)
                c = QxQxQred_m1(v_init).evalf()
                c2 = -(2 * v_init) * QixQxQred(v_init, v_fin, v_fin - 1).evalf()
                rad_Mat = rad_Mat * c + rad_Mat2 * c2

            else:
                continue

            CG2: float = CG_SO5r3(v_init, al_init, L_init,
                                  3, 1, 0,
                                  v_fin, al_fin, L_fin)

            for i1 in range(1, rad_dim + 1):
                for j1 in range(1, rad_dim + 1):
                    direct_Mat[idisp + i1 - 1, jdisp + j1 - 1] = (CG2 * rad_Mat[i1 - 1, j1 - 1]).evalf()

    return direct_Mat


# # The following procedure QixQxQred returns the genuine SO(5) reduced
# # matrix elements
# #          <v_f ||| [[Q^+ x Q x Q]]^3 ||| v_i>,             (**)
# #          <v_f ||| [[Q^- x Q x Q]]^3 ||| v_i>,             (***)
# # for v_f=v_i +/- 1, calculated by making use of (D15) & (D17)
# # (Note that (D15) is independent of L and alpha_i and alpha_f,
# #  which (D17) exploits by choosing particular values of these.)
# # Because v_f=v_i +/- 1, there are actually four cases,
# # where, for (**), the "intermediate" seniority v_int=v_f-1,
# # and for (***), v_int=v_f+1.
# # However, only two cases are required in the ACM. These are
# # those considered in (D17), which are for which v_f-v_i=v_int-v_f.
# # The return value is a mixture of surds and floats, and should
# # be acted upon by evalf to give a sensible value.
#
# # Summing over the two possible v_int should give the SO(5) reduced
# # matrix element - <v_f||| [QxQxQ]^3 |||v_i>  ( [QxQxQ]^3 prop to Y^3_610 )
#
# QixQxQred:=proc(v_i::nonnegint,v_f::nonnegint,v_int::nonnegint)
#   local mediates,L_i;
#
#   L_i:=2*min(v_i,v_f):  # initial and final value of L
#
#   # obtain the list of intermediate states with seniority v_int
#
#   mediates:=lbsSO5r3_rngL(v_int,L_i-2,L_i+2):
#
#   # Using (D16), sum over them to get a SO(3) reduced matrix element.
#   # Note that Q=4*Pi/sqrt(15) * Y112; [QxQ]_2=-4*Pi*sqrt(2/105) * Y212.
#   # (note that a factor of sqrt(dimSO3(L_i)) is cancelled with below.)
#
#   - ME_SO5red(v_f,1,v_int) * ME_SO5red(v_int,2,v_i) * sqrt(2/7) / 15
#     * add( CG_SO5r3(v_int,m[2],m[3],1,1,2,v_f,1,L_i)
#              * CG_SO5r3(v_i,1,L_i,2,1,2,v_int,m[2],m[3])
#              * sqrt(dimSO3(m[3]))  * (-1)^m[3], m in mediates)
#
#   # then convert this to a SO(5) reduced matrix element by dividing
#
#     /CG_SO5r3(v_i,1,L_i,3,1,0,v_f,1,L_i)/sqrt(5*dimSO3(L_i)):
#
# end;
def QixQxQred(v_i: nonnegint, v_f: nonnegint, v_int: nonnegint) -> Expr:
    require_nonnegint('v_i', v_i)
    require_nonnegint('v_f', v_f)
    require_nonnegint('v_int', v_int)

    L_i: int = 2 * min(v_i, v_f)

    mediates: list[SO5SO3Label] = lbsSO5r3_rngL(v_int, L_i - 2, L_i + 2)
    return -ME_SO5red(v_f, 1, v_int) * ME_SO5red(v_int, 2, v_i) * sqrt(Rational(2, 7)) / 15 * \
           sum(CG_SO5r3(v_int, a, L, 1, 1, 2, v_f, 1, L_i) *
               CG_SO5r3(v_i, 1, L_i, 2, 1, 2, v_int, a, L) *
               sqrt(dimSO3(L)) * (-1) ** L for (_, a, L) in mediates) / \
           CG_SO5r3(v_i, 1, L_i, 3, 1, 0, v_f, 1, L_i) / sqrt(5 * dimSO3(L_i))


# # The four cases are also implemented separately by the following
# # procedures (we don't use these procedures, but they are instructive!)
# # The correspondence is
# #    QpxQxQred_p1(v)  <->  QixQxQred(v,v+1,v)
# #    QmxQxQred_p1(v)  <->  QixQxQred(v,v+1,v+2)
# #    QpxQxQred_m1(v)  <->  QixQxQred(v,v-1,v-2)
# #    QmxQxQred_m1(v)  <->  QixQxQred(v,v-1,v)
#
# # Note that, although all v>=0 are accepted as arguments for each,
# # the first two don't make physical sense for v=0,
# # and the last two don't make physical sense for v<=1 (both give errors).
# # However, these exceptional values aren't required.
#
# QpxQxQred_p1:=proc(v::nonnegint)
#   local mediates,L1;
#
#   L1:=2*v:  # initial value of L
#
#   # obtain the list of intermediate states
#
#   mediates:=lbsSO5r3_rngL(v,L1-2,L1):
#
#   # sum over them to get a singly reduced matrix element
#
#   Qred_p1(v) * QxQred_0(v) *
#     add( CG_SO5r3(v,m[2],m[3],1,1,2,v+1,1,L1)
#           * CG_SO5r3(v,1,L1,2,1,2,v,m[2],m[3])
#           * sqrt(dimSO3(m[3]))  * (-1)^m[3], m in mediates)
#
#   # then convert this to a doubly reduced matrix element by dividing
#
#     /CG_SO5r3(v,1,L1,3,1,0,v+1,1,L1)/sqrt(5*dimSO3(L1)):
#
# end;
def QpxQxQred_p1(v: nonnegint) -> Expr:
    require_nonnegint('v', v)

    L1: int = 2 * v

    mediates: list[SO5SO3Label] = lbsSO5r3_rngL(v, L1 - 2, L1)

    return Qred_p1(v) * QxQred_0(v) * \
           sum(CG_SO5r3(v, a, L, 1, 1, 2, v + 1, 1, L1) *
               CG_SO5r3(v, 1, L1, 2, 1, 2, v, a, L) *
               sqrt(dimSO3(L)) * (-1) ** L for (_, a, L) in mediates) / \
           CG_SO5r3(v, 1, L1, 3, 1, 0, v + 1, 1, L1) / sqrt(5 * dimSO3(L1))


# QmxQxQred_p1:=proc(v::nonnegint)
#   local mediates,L1;
#
#   L1:=2*v:  # initial value of L
#
#   # obtain the list of intermediate states
#
#   mediates:=lbsSO5r3_rngL(v+2,L1-2,L1+2):
#
#   # sum over them to get a singly reduced matrix element
#
#   Qred_m1(v+2) * QxQred_p2(v) *
#     add( CG_SO5r3(v+2,m[2],m[3],1,1,2,v+1,1,L1)
#           * CG_SO5r3(v,1,L1,2,1,2,v+2,m[2],m[3])
#           * sqrt(dimSO3(m[3])) * (-1)^m[3] , m in mediates)
#
#   # then convert this to a doubly reduced matrix element by dividing
#
#     /CG_SO5r3(v,1,L1,3,1,0,v+1,1,L1)/sqrt(5*dimSO3(L1)):
#
# end;
def QmxQxQred_p1(v: nonnegint) -> Expr:
    require_nonnegint('v', v)

    L1: int = 2 * v

    mediates: list[SO5SO3Label] = lbsSO5r3_rngL(v + 2, L1 - 2, L1 + 2)

    return Qred_m1(v + 2) * QxQred_p2(v) * \
           sum(CG_SO5r3(v + 2, a, L, 1, 1, 2, v + 1, 1, L1) *
               CG_SO5r3(v, 1, L1, 2, 1, 2, v + 2, a, L) *
               sqrt(dimSO3(L)) * (-1) ** L for (_, a, L) in mediates) / \
           CG_SO5r3(v, 1, L1, 3, 1, 0, v + 1, 1, L1) / sqrt(5 * dimSO3(L1))


# QpxQxQred_m1:=proc(v::posint)
#   local mediates,L1;
#
#   L1:=2*v-2:  # initial value of L
#
#   # this case has only one intermediate state [v-1,1,2v-4]
#
#   # get singly reduced matrix element
#
#   Qred_p1(v-2) * QxQred_m2(v)
#           * CG_SO5r3(v-2,1,L1-2,1,1,2,v-1,1,L1)
#           * CG_SO5r3(v,1,L1,2,1,2,v-2,1,L1-2)
#           * sqrt(dimSO3(L1-2))
#
#   # then convert this to a doubly reduced matrix element by dividing
#
#     /CG_SO5r3(v,1,L1,3,1,0,v-1,1,L1)/sqrt(5*dimSO3(L1)):
#
# end;
def QpxQxQred_m1(v: posint) -> Expr:
    require_posint('v', v)

    L1: int = 2 * v - 2

    return Qred_p1(v - 2) * QxQred_m2(v) * \
           CG_SO5r3(v - 2, 1, L1 - 2, 1, 1, 2, v - 1, 1, L1) * \
           CG_SO5r3(v, 1, L1, 2, 1, 2, v - 2, 1, L1 - 2) * \
           sqrt(dimSO3(L1 - 2))


# QmxQxQred_m1:=proc(v::posint)
#   local mediates,L1;
#
#   L1:=2*v-2:  # initial value of L
#
#   # obtain the list of intermediate states
#
#   mediates:=lbsSO5r3_rngL(v,L1-2,L1+2):
#
#   # sum over them to get a singly reduced matrix element
#
#   Qred_m1(v) * QxQred_0(v) *
#     add( CG_SO5r3(v,m[2],m[3],1,1,2,v-1,1,L1)
#           * CG_SO5r3(v,1,L1,2,1,2,v,m[2],m[3])
#           * sqrt(dimSO3(m[3])) * (-1)^m[3] , m in mediates)
#
#   # then convert this to a doubly reduced matrix element by dividing
#
#     /CG_SO5r3(v,1,L1,3,1,0,v-1,1,L1)/sqrt(5*dimSO3(L1)):
#
# end;
def QmxQxQred_m1(v: posint) -> Expr:
    require_posint('v', v)

    L1: int = 2 * v - 2

    mediates: list[SO5SO3Label] = lbsSO5r3_rngL(v, L1 - 2, L1 + 2)

    return Qred_m1(v) * QxQred_0(v) * \
           sum(CG_SO5r3(v, a, L, 1, 1, 2, v - 1, 1, L1) *
               CG_SO5r3(v, 1, L1, 2, 1, 2, v, a, L) *
               sqrt(dimSO3(L)) * (-1) ** L for (_, a, L) in mediates) / \
           CG_SO5r3(v, 1, L1, 3, 1, 0, v - 1, 1, L1) / \
           sqrt(5 * dimSO3(L1))
