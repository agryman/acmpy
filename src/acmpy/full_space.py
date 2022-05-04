"""7. Procedures that perform calculations on the full Hilbert space:

diagonalising, basis transforming, and data displaying.
"""

import numpy as np
from typing import Optional, Callable
from sympy import Expr, Matrix, shape, S

from acmpy.compat import nonnegint, require_nonnegint, require_algebraic, require_nonnegint_range, iquo, \
    Matrix_to_ndarray, ndarray_to_Matrix, ndarray_to_list, NDArrayFloat
from acmpy.internal_operators import OperatorSum, Op_Tame
from acmpy.spherical_space import dimSO5r3_rngV
from acmpy.full_operators import RepXspace, dimXspace
from acmpy.radial_space import dimRadial
from acmpy.eigenvalues import Eigenfiddle
from acmpy.globals import Designators
import acmpy.globals as g

# ###########################################################################
# ####---------- Diagonalisation and Eigenbasis transformation ----------####
# ###########################################################################
#
# # The following procedure DigXspace represents the operator encoded
# # in ham_op on the truncated Hilbert space specified by the other
# # arguments, and then diagonalises it.
# # The return value is a quartet of values
# #           [eigen_vals, eigen_bases, Xparams, Lvals].
# # Here Xparams lists the parameters [anorm,lambda,nu_min,nu_max,v_min,v_max]
# # (without L). Here, Lvals is a list of the values of angular momentum L
# # between L_min..L_max which are of non-zero dimension in the truncated
# # Hilbert space. The elements of the other two values pertain to these
# # values of L. eigen_vals is a list, each element of which contains a list
# # of eigenvalues in a constant L-space.
# # eigen_bases is the list of transformation matrices to the eigenspaces.
# # It's probably not a good idea to display this output!
# # The values in eigen_vals are probably best displayed using
# # the Show_Eigs procedure below.
# # The other output values may be directly used as input to the
# # procedure AmpXspeig to calculate transition rates/amplitudes.
#
# # Note that diagonalisation (via the procedure Eigenfiddle below)
# # is always carried out separately on each L-space.
# # However, the calculation of the representation itself might not be done
# # separately on these spaces if the Hamiltonian encoded by ham_op
# # makes use of the contraction features.
#
# DigXspace:=proc(ham_op::list,
#                      anorm::algebraic, lambda_base::algebraic,
#                      nu_min::nonnegint, nu_max::nonnegint,
#                      v_min::nonnegint, v_max::nonnegint,
#                      L_min::nonnegint, L_max::nonnegint,$)
#       local LL,LLM,eigen_bases,eigen_result,Lvals,
#             Xparams,eigen_vals,rep_matrix,L_matrix,
#             rad_dim,sph_dim,Lstart;
#
#   if _npassed<9 then  # no L_max
#     LLM:=L_min;
#   else
#     LLM:=L_max
#   fi:
#
#   Xparams:=[anorm,lambda_base,nu_min,nu_max,v_min,v_max];  # 6 params (no L)
#
#   # Use Lvals to store those L with non-zero dimension.
#   # Then only diagonalise on these spaces.
#
#   Lvals:=[]:
#   eigen_vals:=[];       # for eigenvalues for these L
#   eigen_bases:=[];      # corresponding matrices of column vectors
#
#   # We decide now whether to calculate the representation matrix on the
#   # whole (truncated) space, or individually on the component L-spaces.
#   # The latter is sufficient if the Hamiltonian (AM=0) contains no
#   # terms of non-zero angular momentum.
#   # However, in both cases, we still diagonalise only the individual
#   # L-spaces.
#
#   if Op_Tame(ham_op) then  # work on L-spaces separately...
#
#     for LL from L_min to LLM do
#       sph_dim:=dimSO5r3_rngV(v_min,v_max,LL):
#       if sph_dim>0 then
#         Lvals:=[op(Lvals),LL];
#
#         L_matrix:=RepXspace(ham_op,op(Xparams),LL);
#         eigen_result:=Eigenfiddle(L_matrix);
#
#         # store eigenvalue lists, one LL at a time.
#
#         eigen_vals:=[op(eigen_vals),eigen_result[1]];
#
#         # store matrix of eigenvectors (inverses to be obtained elsewhere)
#
#         eigen_bases:=[op(eigen_bases),eigen_result[2]];
#       fi:
#     od:
#
#   else
#     rep_matrix:=RepXspace(ham_op,op(Xparams),L_min,LLM);
#     rad_dim:=dimRadial(nu_min,nu_max);
#     Lstart:=1:
#
#     for LL from L_min to LLM do
#       sph_dim:=dimSO5r3_rngV(v_min,v_max,LL):
#       if sph_dim>0 then
#         Lvals:=[op(Lvals),LL];
#
#         L_matrix:=SubMatrix(rep_matrix,[Lstart..Lstart+rad_dim*sph_dim-1],
#                                      [Lstart..Lstart+rad_dim*sph_dim-1]):
#         eigen_result:=Eigenfiddle(L_matrix);
#
#         eigen_vals:=[op(eigen_vals),eigen_result[1]];
#
#         eigen_bases:=[op(eigen_bases),eigen_result[2]];
#         Lstart:=Lstart+rad_dim*sph_dim;
#       fi:
#     od:
#   fi:
#
#   [eigen_vals, eigen_bases, Xparams, Lvals];
# end;

EigenValues = list[list[float]]
EigenBases = list[Matrix]
XParams = tuple[Expr, Expr, nonnegint, nonnegint, nonnegint, nonnegint]
LValues = list[nonnegint]


def DigXspace(ham_op: OperatorSum,
              anorm: Expr, lambda_base: Expr,
              nu_min: nonnegint, nu_max: nonnegint,
              v_min: nonnegint, v_max: nonnegint,
              L_min: nonnegint, L_max: Optional[nonnegint] = None
              ) -> tuple[EigenValues, EigenBases, XParams, LValues]:
    if L_max is None:
        L_max = L_min
    require_algebraic('anorm', anorm)
    require_algebraic('lambda_base', lambda_base)
    require_nonnegint_range('nu', nu_min, nu_max)
    require_nonnegint_range('v', v_min, v_max)
    require_nonnegint_range('L', L_min, L_max)

    LLM: nonnegint = L_max

    Xparams: XParams = anorm, lambda_base, nu_min, nu_max, v_min, v_max

    Lvals: LValues = []
    eigen_vals: EigenValues = []
    eigen_bases: EigenBases = []

    LL: int
    sph_dim: int
    L_matrix: Matrix
    eigen_vals_result: list[float]
    eigen_bases_result: Matrix

    L_matrix_np: np.ndarray
    eigen_vals_result_np: np.ndarray
    eigen_bases_result_np: np.ndarray

    if Op_Tame(ham_op):

        for LL in range(L_min, LLM + 1):
            sph_dim = dimSO5r3_rngV(v_min, v_max, LL)
            if sph_dim > 0:
                Lvals.append(LL)

                L_matrix_np = RepXspace(ham_op, anorm, lambda_base, nu_min, nu_max, v_min, v_max, LL)
                eigen_vals_result_np, eigen_bases_result_np = Eigenfiddle(L_matrix_np)
                eigen_vals_result = ndarray_to_list(eigen_vals_result_np)
                eigen_bases_result = ndarray_to_Matrix(eigen_bases_result_np)

                eigen_vals.append(eigen_vals_result)

                eigen_bases.append(eigen_bases_result)
    else:
        rep_matrix_np: NDArrayFloat = RepXspace(ham_op, anorm, lambda_base, nu_min, nu_max, v_min, v_max, L_min, LLM)
        # rep_matrix: Matrix = ndarray_to_Matrix(rep_matrix_np)
        rad_dim: int = dimRadial(nu_min, nu_max)
        Lstart: int = 1

        for LL in range(L_min, LLM + 1):
            sph_dim = dimSO5r3_rngV(v_min, v_max, LL)
            Lstop: int = Lstart + rad_dim * sph_dim
            if sph_dim > 0:
                Lvals.append(LL)

                # L_matrix = rep_matrix[(Lstart - 1):Lstop, (Lstart - 1):Lstop]

                # L_matrix_np = Matrix_to_ndarray(L_matrix)
                L_matrix_np = rep_matrix_np[(Lstart - 1):Lstop, (Lstart - 1):Lstop]
                eigen_vals_result_np, eigen_bases_result_np = Eigenfiddle(L_matrix_np)
                eigen_vals_result = ndarray_to_list(eigen_vals_result_np)
                eigen_bases_result = ndarray_to_Matrix(eigen_bases_result_np)

                eigen_vals.append(eigen_vals_result)

                eigen_bases.append(eigen_bases_result)
                Lstart = Lstop

    return eigen_vals, eigen_bases, Xparams, Lvals


# # The following procedure AmpXspeig represents the operator encoded
# # in tran_op on the truncated Hilbert space specified by the elements
# # of Xparams and Lvals, and then transforms it to the basis specified
# # in eigen_bases (which is possibly an eigenbasis of some other operator).
# # The return value is a "block matrix" of Matrices, each of which
# # gives the alternative SO(3)-reduced transition amplitudes
# #
# #           <n_f,L_f || W || n_i,L_i>
# #           -------------------------
# #                sqrt (2*L_f+1)
# #
# # between the set of states of angular momentum L_i and the set of states
# # of angular momentum L_f (the states are indexed by n_i & n_f respectively).
# # Note that the (i1,i2) block matrix element corresponds to the
# # angular momenta Lvals[i1] and Lvals[i2].
#
# # The output from this procedure is probably best displayed using the
# # Show_Rats and Show_Amps procedures below.
# # These apply the correct functions to the raw matrix elements,
# # and also apply current values of the scaling factors.
#
# AmpXspeig:=proc(tran_op::list, eigen_bases::list,
#                                            Xparams::list, Lvals::list)
#       local i,j,LL,L_min,L_max,L_dims,L_ends,L_count,
#             eigen_invs,tran_mat,block_tran_mat;
#
#   L_count:=nops(Lvals);
#
#   if Lcount=0 then return fi:   # nothing to do
#
#   L_min:=Lvals[1]:
#   L_max:=Lvals[L_count]:
#
#   # For the alternative SO(3)-reduced transition operator, form the
#   # transformation matrix encompassing all L values
#   # (we cut it into blocks below).
#
#   tran_mat:=RepXspace(tran_op,op(Xparams),L_min,L_max);
#
#   # Obtain the sizes of the blocks (one for each good L value).
#
#   L_dims:=[seq(dimXspace(op(3..6,Xparams),LL),LL in Lvals)];
#   L_ends:=[seq(dimXspace(op(3..6,Xparams),L_min,LL),LL in Lvals)];
#
#   # Form the block matrix, each element of which is itself a matrix.
#   # The (i,j) block is of size L_dims[i] x L_dims[j].
#
#   block_tran_mat:=Matrix(L_count,
#         (i,j)->SubMatrix(tran_mat,[L_ends[i]-L_dims[i]+1..L_ends[i]],
#                                   [L_ends[j]-L_dims[j]+1..L_ends[j]]) );
#
#   # Here we simply transform to the basis (an eigenbasis) specified in the
#   # matrices eigen_basis, after first forming inverse transition matrices.
#   # (calculating the inverse matrices each time this procedure is
#   #  called is probably not inefficient because this procedure will
#   #  usually only be called once for a given set of parameters.)
#
#   eigen_invs:=map(MatrixInverse,eigen_bases);
#
#   Matrix(L_count, (i,j)->eigen_invs[i].block_tran_mat[i,j].eigen_bases[j]);
#
# end;
def AmpXspeig(tran_op: OperatorSum, eigen_bases: list[Matrix], Xparams: XParams, Lvals: list[nonnegint]
              ) -> Optional[Matrix]:
    L_count: int = len(Lvals)

    if L_count == 0:
        return None

    anorm, lambda_base, nu_min, nu_max, v_min, v_max = Xparams

    L_min: nonnegint = Lvals[0]
    L_max: nonnegint = Lvals[-1]

    tran_mat_np: NDArrayFloat = RepXspace(tran_op, anorm, lambda_base, nu_min, nu_max, v_min, v_max, L_min, L_max)
    tran_mat: Matrix = ndarray_to_Matrix(tran_mat_np)

    L_dims: list[nonnegint] = [dimXspace(nu_min, nu_max, v_min, v_max, LL) for LL in Lvals]
    L_ends: list[nonnegint] = [dimXspace(nu_min, nu_max, v_min, v_max, L_min, LL) for LL in Lvals]

    block_tran_mat: Matrix = Matrix(L_count, L_count,
                                    lambda i, j: tran_mat[
                                                 (L_ends[i] - L_dims[i]):L_ends[i],
                                                 (L_ends[j] - L_dims[j]):L_ends[j]])
    eigen_invs: list[Matrix] = [P ** -1 for P in eigen_bases]

    return Matrix(L_count, L_count,
                  lambda i, j: eigen_invs[i] * block_tran_mat[i, j] * eigen_bases[j])


# ###########################################################################
#
# # The following procedure Show_Eigs displays in a convenient format
# # lists of eigenvalues. It is designed to use directly the
# # items "eigenvals" and "Lvals" of the lists returned by the
# # procedures DigXspace, ACM_Scale and ACM_Adapt.
# # The latter is a list of angular momentum values, and the former
# # is a list, each item of which pertains to the corresponding
# # angular momentum value, and itself is a list of eigenvalues.
# # The lowest eigenvalue across all angular momenta is obtained and
# # displayed, and all values displayed are taken with respect to it.
# # Eigenvalues are displayed for each angular momentum in the
# # range L_min..L_max, with those of constant angular momentum
# # displayed as a horizontal list. toshow restricts the maximum
# # number of eigenvalues displayed for each angular momentum.
# # The relative eigenvalues are displayed after being scaled (divided)
# # by the value of the global parameter glb_eig_sft.
# # The value returned is the lowest eigenvalue (unscaled).
#
# # If L_max is omitted then a single value L_min is used. If both
# # are omitted then all values are used (well, 0..1000000).
L_MAX_DEFAULT: int = 1000000


# Show_Eigs:=proc(eigen_vals::list,Lvals::list,
#                      toshow::nonnegint:=glb_eig_num,
#                      L_min::nonnegint:=0, L_max::nonnegint:=1000000,$)
#       local LL,i,eigen_low,L_count,L_top;
#       global glb_low_pre,glb_rel_wid,glb_rel_pre,glb_eig_sft,glb_eig_rel;
#
#   if toshow=0 or nops(eigen_vals)=0 then return NULL fi:
#
#   if _npassed=4 then   # only in this case, use a single value.
#     L_top:=L_min:
#   else
#     L_top:=L_max:
#   fi:
#
#   L_count:=nops(Lvals):
#
#   # Count how many L to output in range
#
#   i:=0:
#   for LL to L_count do
#     if Lvals[LL]>=L_min and Lvals[LL]<=L_top then
#       i:=i+1:
#     fi:
#   od:
#
#   if i=0 then
#     return NULL
#   fi:
#
#
#   if glb_eig_rel then   # use relative eigenvalues
#
#       # Find smallest eigenvalue across all L spaces (assuming all are real!)
#       # Each sublist is assumed to be increasing.
#
#     eigen_low:=min_head(eigen_vals);
#
#     printf("Lowest eigenvalue is %.*f. Relative eigenvalues follow"
#              " (each divided by %.*f):\n",
#                        glb_low_pre,eigen_low,glb_low_pre,glb_eig_sft);
#   else
#     eigen_low:=0;
#
#     printf("Scaled eigenvalues follow (each divided by %.*f):\n",
#                        glb_low_pre,glb_eig_sft);
#
#   fi:
#
#
#   # display all required eigenvalues, with scaling given by glb_eig_sft.
#
#   for LL to L_count do
#     if Lvals[LL]>=L_min and Lvals[LL]<=L_top then
#       # print L and first relative eigenvalue
#       printf("  At L=%2d: [%*.*f",Lvals[LL],glb_rel_wid,glb_rel_pre,
#                         (eigen_vals[LL][1]-eigen_low)/glb_eig_sft);
#       # print remaining eigenvalues
#       for i from 2 to min(nops(eigen_vals[LL]),toshow) do
#         printf(",%*.*f",glb_rel_wid,glb_rel_pre,
#                         (eigen_vals[LL][i]-eigen_low)/glb_eig_sft);
#       od:
#       # finish writing line
#       printf("]\n");
#     fi:
#   od:
#
#   eigen_low;   # return smallest eigenvalue (in case it's needed!)
# end;
def Show_Eigs(eigen_vals: list[list[float]], Lvals: list[nonnegint],
              toshow: nonnegint = g.glb_eig_num,
              L_min: Optional[nonnegint] = None, L_max: Optional[nonnegint] = None
              ) -> Optional[float]:
    require_nonnegint('toshow', toshow)

    if toshow == 0 or len(eigen_vals) == 0:
        return None

    L_top: nonnegint
    if L_min is not None and L_max is None:
        L_max = L_MAX_DEFAULT
        L_top = L_min
    else:
        L_min = 0 if L_min is None else L_min
        L_max = L_MAX_DEFAULT if L_max is None else L_max
        L_top = L_max

    require_nonnegint_range('L', L_min, L_max)

    if not any(L_min <= L <= L_top for L in Lvals):
        return None

    low_pre: int = g.glb_low_pre
    rel_wid: int = g.glb_rel_wid
    eig_sft: float = g.glb_eig_sft

    eigen_low: float
    if g.glb_eig_rel:
        eigen_low = min_head(eigen_vals)
        print(f'Lowest eigenvalue is {eigen_low:.{low_pre}f}. Relative eigenvalues follow' +
              f' (each divided by {eig_sft:.{low_pre}f}):')
    else:
        eigen_low = 0
        print(f'Scaled eigenvalues follow (each divided by {eig_sft:.{low_pre}f}:')

    rel_pre: int = g.glb_rel_pre
    for L, vals in zip(Lvals, eigen_vals):
        if L_min <= L <= L_top:
            print(f'  At L={L:2d}: [' +
                  ','.join([f'{((val - eigen_low) / eig_sft):{rel_wid}.{rel_pre}f}'
                            for val in vals[:toshow]]) +
                  ']')

    return eigen_low


# # The following functions min_head and fsel are used to obtain,
# # within a list of lists, the minimal value amongst the first elements.
# # These procedures are only used within Show_Eigs above.
#
# min_head:=(alist)->min(op(map(fsel,alist)));
def min_head(alist: list[list[float]]) -> float:
    return min(nlist[0] for nlist in alist if len(nlist) > 0)


# fsel:=(nlist)->`if`(nops(nlist)>0,nlist[1],NULL);
def fsel(nlist: list[float]) -> Optional[float]:
    return nlist[0] if len(nlist) > 0 else None


# ###########################################################################
#
# # The procedure Show_Mels below is a very versatile procedure for
# # displaying functions of (alternative) SO(3)-reduced matrix elements,
# # in a convenient format, with the actual elements displayed
# # specified in the list mel_lst of "designators". NULL is returned.
# # This procedure is called directly by the procedures Show_Rats
# # and Show_Amps, which are intended to display transition rates
# # and transition amplitudes respectively (but can do otherwise)
# # calculated from the matrix elements.
# # The argument Lvals is a list of angular momenta. The argument
# # Melements is a Matrix of which each element is itself a Matrix
# # which pertains to a particular pair of angular momenta.
# # Specifically, if ki and kf are such that Li=Lvals[ki] and Lf=Lvals[kf]
# # then Melements[kf,ki][nf,ni] is assumed to be the alternative
# # SO(3)-reduced matrix element
# #
# #           <nf,Lf || W || ni,Li>
# #           ---------------------
# #               sqrt (2*Lf+1)
# #
# # If we denote such a value by Mele, then the value actually
# # displayed is mel_fun(Li,Lf,Mele)/scale
# # (the argument mel_fun should itself be a procedure taking three arguments).
#
# # The values of Li, Lf, ni and nf for which values are displayed
# # is determined by the list showlist, each element of which should
# # itself be a list of up to five integers:
# #   1. A quartet [Li,Lf,ni,nf] designates the output of a single value;
# #   2. A triple of the form [Li,Lf,nf] outputs a vector of values
# #      formed from all possible values of ni (note strange order).
# #   3. A pair of the form [Li,Lf].
# #      Then a sequence of vectors of the above form is displayed
# #      for all possible values of nf.
# #   4. A single value [Lf]. Then sequence of vectors for
# #      [Li,Lf,nf] is output for all possible Li and nf.
# #   5. An empty list []. Then sequence of vectors for
# #      [Li,Lf,nf] is output for all possible Li, Lf and nf.
# #   6. A quintet of the form [Li,Lf,ni,nf,L_mod].
# #      This produces all quartets [LiX,LfX,ni,nf]
# #      with LiX=Li+k*L_mod and LfX=Lf+k*L_mod for k>=0.
# # Note that if either Li and Lf vary, then only those values are used
# # that differ by at most the value of the global variable glb_rat_TRopAM.
# # This is because glb_rat_TRopAM is (intended to be) the angular
# # momentum of the operator which produced the matrix elements Melements,
# # and therefore other angular momenta would give zero matrix elements.
#
# # The argument toshow gives the maximum number of values to be shown
# # in the case of lists produced by the designators with 3 or fewer items.
# # The argument mel_format is a C-style format specification,
# # which should contain two "%s" specifiers. The first will be
# # substituted for by a string that gives the two states mapped between
# # (this is determined by the global variable glb_tran_format which,
# # in the default implementation, takes the form "#(#) -> #(#)"),
# # and the second by the value of the function of the matrix element,
# # calculated as above.
# # The argument mel_desg contains a simple phrase (such as "matrix elements")
# # used to introduce the output.
#
# # Note that the default values are determined each time the procedure
# # is invoked, and not when it is initially defined.
#
# # Also note that if the 3rd argument is not a list of lists,
# # or the 5th argument is not a procedure then an error will result
# # (with that argument taken to be the 7th and an excess of arguments
# # being flagged).
#
#
# Show_Mels:=proc(Melements::Matrix, Lvals::list,
#                   mel_lst::list(list),
#                   toshow::integer:=glb_rat_num,
#                   mel_fun::procedure:=def_mel_fun,
#                   scale::constant:=1.0,
#                   mel_format::string:=def_mel_format,
#                   mel_desg::string:=def_mel_desg,$)
#
#       local L1,L2,n1,n2,L1_off,L2_off,rate_ent,TR_matrix,
#             TR_cols,TR_rows,Lmod,Lcount,item_preformat,tran_fmat1,tran_fmat2:
#       global glb_low_pre,glb_rel_wid,glb_rel_pre,
#              glb_rat_TRopAM,
#              glb_tran_format,glb_tran_fill,  # for "#(#) -> #(#)"
#              glb_mel_f1,glb_mel_f2,  # These three are set here
#              glb_item_format:        #  "
#
#
#   if nops(mel_lst)=0 then return NULL fi:
#
#   if ColumnDimension(Melements)=0 then
#     error "No matrix elements available!"
#   fi:
#
#   printf("Selected %s follow"
#          " (each divided by %.*f):\n", mel_desg,glb_low_pre,evalf(scale));
#
#   # Specify format for the printing of each transition rate/amplitude.
#   # Two stages - first sets the width and precision for values to output.
#
#   item_preformat:= "%%%d.%df":
#   glb_item_format:=sprintf(item_preformat,glb_rel_wid,glb_rel_pre):
#
#   # Change the %s specifications in glb_tran_fmat to either
#   # "%d" for integers, or a filler which is required for the lists.
#
#   tran_fmat1:=sprintf(glb_tran_format,"%d","%d","%d","%d"):
#   glb_mel_f1:=sprintf(mel_format,tran_fmat1,glb_item_format):
#
#   tran_fmat2:=sprintf(glb_tran_format,"%d",glb_tran_fill,"%d","%d"):
#   glb_mel_f2:=sprintf(mel_format,tran_fmat2,"%s"):
#
#   # Now output the (scaled) matrix elements designated in mel_lst.
#   # Note that those in the list that are not in the
#   # range of those calculated are silently ignored.
#
#   for rate_ent in mel_lst do
#
#     if nops(rate_ent)>5 then
#       printf("  Bad matrix element specification: %a\n",rate_ent):
#       next:
#     fi:
#
#     if nops(rate_ent)>1 then
#       L1:=rate_ent[1]:
#       L2:=rate_ent[2]:
#
#       if L1<0 or L2<0 then next fi:
#     fi:
#
#
#     if nops(rate_ent)=4         # output 4-index specifiers
#         then
#
#       # Locate indices in Lvals for these Ls.
#
#       if member(L1,Lvals,'L1_off') and member(L2,Lvals,'L2_off') then
#         TR_matrix:=Melements[L2_off,L1_off];
#         TR_cols:=ColumnDimension(TR_matrix);
#         TR_rows:=RowDimension(TR_matrix);
#
#         n1:=rate_ent[3]:
#         n2:=rate_ent[4]:
#
#         if n1>0 and n2>0 and n1<=TR_cols and n2<=TR_rows then
#             printf(glb_mel_f1,L1,n1,L2,n2,
#                    evalf(mel_fun(L1,L2,TR_matrix[n2,n1])/scale)):
#             printf("\n"):
#         fi:
#       fi:      # L1 & L2 members
#
#
#     elif nops(rate_ent)=5         # output 5-index specifiers
#          then
#
#       n1:=rate_ent[3]:
#       n2:=rate_ent[4]:
#       if n1<=0 or n2<=0 then next fi:
#       Lmod:=rate_ent[5]:
#
#       if Lmod>0 then    # Put Lcount+1 as number of rates required
#           Lcount:=iquo(Lvals[-1]-max(L1,L2),Lmod):
#       elif Lmod<0 then
#           Lmod:=-Lmod:
#           Lcount:=iquo(min(L1,L2),Lmod):
#           L1:=L1-Lcount*Lmod:
#           L2:=L2-Lcount*Lmod:
#       else
#           Lcount:=0:
#       fi:
#
#       while Lcount>=0 do    # loop through all Lcount+1 cases
#
#         if member(L1,Lvals,'L1_off') and member(L2,Lvals,'L2_off') then
#
#           TR_matrix:=Melements[L2_off,L1_off];
#           TR_cols:=ColumnDimension(TR_matrix);
#           TR_rows:=RowDimension(TR_matrix);
#
#           if n1<=TR_cols and n2<=TR_rows then
#               printf(glb_mel_f1,L1,n1,L2,n2,
#                    evalf(mel_fun(L1,L2,TR_matrix[n2,n1])/scale)):
#               printf("\n"):
#           fi:
#         fi:
#
#         L1:=L1+Lmod:
#         L2:=L2+Lmod:
#         Lcount:=Lcount-1;
#       od
#
#
#     elif nops(rate_ent)=3    # output 3-index specifiers
#         then
#
#       Show_Mels_Row(Melements,Lvals,L1,L2,rate_ent[3],toshow,mel_fun,scale):
#                                                        # 5th arg -> n2
#
#     elif nops(rate_ent)=2    # output 2-index specifiers
#         then
#
#       for n2 from 1 to toshow while
#         Show_Mels_Row(Melements,Lvals,L1,L2,n2,toshow,mel_fun,scale)>0 do
#       od:  # keep increasing n2 until no output
#
#     elif nops(rate_ent)=1    # output 1-index specifiers
#         then
#
#       L2:=rate_ent[1]:   # note switch
#       if L2<0 then next fi:
#
#       # now loop through all possible L1 for |L1-L2] in TR range.
#
#       for L1 from max(0,L2-glb_rat_TRopAM) to L2+glb_rat_TRopAM do
#       for n2 from 1 to toshow while
#         Show_Mels_Row(Melements,Lvals,L1,L2,n2,toshow,mel_fun,scale)>0 do
#       od:  # keep increasing n2 until no output
#       od:
#
#     elif nops(rate_ent)=0   # output 0-index specifiers
#         then
#
#       for L2 in Lvals do
#
#       # now loop through all possible L1 for |L1-L2] in TR range.
#
#       for L1 from max(0,L2-glb_rat_TRopAM) to L2+glb_rat_TRopAM do
#       for n2 from 1 to toshow while
#         Show_Mels_Row(Melements,Lvals,L1,L2,n2,toshow,mel_fun,scale)>0 do
#       od:  # keep increasing n2 until no output
#       od:
#       od:
#
#     fi:
#   od:
#   NULL;
# end;
glb_mel_f1: str = ''
glb_mel_f2: str = ''
glb_item_format: str = ''


def Show_Mels(Melements: Matrix, Lvals: list[nonnegint],
              mel_lst: Designators,
              toshow: int = g.glb_rat_num,
              mel_fun: Callable = g.glb_rat_fun,
              scale: float | Expr = 1.0,
              mel_format: str = g.def_mel_format,
              mel_desg: str = g.def_mel_desg
              ) -> None:

    global glb_mel_f1, glb_mel_f2, glb_item_format

    if len(mel_lst) == 0:
        return

    r, c = shape(Melements)
    if c == 0:
        raise ValueError('No matrix elements available!')

    scale = S(scale)

    low_pre: int = g.glb_low_pre
    print(f'Selected {mel_desg} follow' +
          f' (each divided by {scale.evalf():.{low_pre}f}):')

    rel_wid: int = g.glb_rel_wid
    rel_pre: int = g.glb_rel_pre
    glb_item_format = f'{{:{rel_wid}.{rel_pre}f}}'

    num: str = '{:d}'
    tran_fmat1: str = g.glb_tran_format.format(num, num, num, num)
    glb_mel_f1 = mel_format.format(tran_fmat1, glb_item_format)

    fill: str = g.glb_tran_fill
    tran_fmat2: str = g.glb_tran_format.format(num, fill, num, num)
    glb_mel_f2 = mel_format.format(tran_fmat2, '{:s}')

    for rate_ent in mel_lst:

        if len(rate_ent) > 5:
            print(f'  Bad matrix element specification: {rate_ent}')
            continue

        L1: int = -1
        L2: int = -1
        n1: int
        n2: int
        Lmod: int
        L1_off: int
        L2_off: int
        TR_matrix: Matrix
        TR_rows: int
        TR_cols: int
        mel: float

        if len(rate_ent) > 1:
            L1 = rate_ent[0]
            L2 = rate_ent[1]

            if L1 < 0 or L2 < 0:
                continue

        if len(rate_ent) == 4:
            assert L1 >= 0 and L2 >= 0

            if L1 in Lvals and L2 in Lvals:
                L1_off = Lvals.index(L1)
                L2_off = Lvals.index(L2)
                TR_matrix = Melements[L2_off, L1_off]
                TR_rows, TR_cols = shape(TR_matrix)

                n1 = rate_ent[2]
                n2 = rate_ent[3]

                if 0 < n1 <= TR_cols and 0 < n2 <= TR_rows:
                    mel = (mel_fun(L1, L2, TR_matrix[n2 - 1, n1 - 1]) / scale).evalf()
                    print(glb_mel_f1.format(L1, n1, L2, n2, mel))

        elif len(rate_ent) == 5:
            assert L1 >= 0 and L2 >= 0

            n1 = rate_ent[2]
            n2 = rate_ent[3]
            if n1 <= 0 or n2 <= 0:
                continue
            Lmod = rate_ent[4]

            Lcount: int
            if Lmod > 0:
                Lcount = iquo(Lvals[-1] - max(L1, L2), Lmod)
            elif Lmod < 0:
                Lmod = -Lmod
                Lcount = iquo(min(L1, L2), Lmod)
                L1 -= Lcount * Lmod
                L2 -= Lcount * Lmod
            else:
                Lcount = 0

            while Lcount >= 0:

                if L1 in Lvals and L2 in Lvals:
                    L1_off = Lvals.index(L1)
                    L2_off = Lvals.index(L2)

                    TR_matrix = Melements[L2_off, L1_off]
                    TR_rows, TR_cols = shape(TR_matrix)

                    if n1 <= TR_cols and n2 <= TR_rows:
                        assert n1 > 0 and n2 > 0
                        mel = (mel_fun(L1, L2, TR_matrix[n2 - 1, n1 - 1]) / scale).evalf()
                        print(glb_mel_f1.format(L1, n1, L2, n2, mel))

                L1 += Lmod
                L2 += Lmod
                Lcount -= 1

        elif len(rate_ent) == 3:

            Show_Mels_Row(Melements, Lvals, L1, L2, rate_ent[2], toshow, mel_fun, scale)

        elif len(rate_ent) == 2:

            for n2 in range(1, toshow + 1):
                if Show_Mels_Row(Melements, Lvals, L1, L2, n2, toshow, mel_fun, scale) <= 0:
                    break

        elif len(rate_ent) == 1:

            L2 = rate_ent[0]
            if L2 < 0:
                continue

            Show_Mels_Rows(Melements, Lvals, L2, toshow, mel_fun, scale)

        elif len(rate_ent) == 0:
            for L2 in Lvals:

                Show_Mels_Rows(Melements, Lvals, L2, toshow, mel_fun, scale)


def Show_Mels_Rows(Melements: Matrix, Lvals: list[nonnegint],
                   L2: nonnegint, toshow: int, mel_fun: Callable, scale: Expr) -> None:
    """Show matrix element rows for the values of L1 and n2 that correspond to L2."""
    TRopAM: nonnegint = g.glb_rat_TRopAM
    for L1 in range(max(0, L2 - TRopAM), L2 + TRopAM + 1):
        for n2 in range(1, toshow + 1):
            if Show_Mels_Row(Melements, Lvals, L1, L2, n2, toshow, mel_fun, scale) <= 0:
                break


# # The following procedure Show_Mels_Row is used by the above procedure
# # Show_Mels to display, for the fixed values L1,L2,n2, the functions
# # of the matrix elements calculated for [L1,L2,n1,n2].
# # These are displayed as a horizontal list.
# # The arguments are the same as for Show_Mels.
#
# Show_Mels_Row:=proc(Melements::Matrix, Lvals::list,
#                     L1::nonnegint,L2::nonnegint,n2::integer,
#                     toshow::nonnegint,
#                     mel_fun::procedure,
#                     scale::constant,$)
#       local n1,L1_off,L2_off,col_count,
#             TR_matrix,TR_cols,TR_rows:
#       global glb_mel_f2,glb_item_format: # These two are set in Show_Mels.
#
#
#   if not member(L1,Lvals,'L1_off') or not member(L2,Lvals,'L2_off') then
#     return 0:
#   fi:
#
#   TR_matrix:=Melements[L2_off,L1_off];
#   TR_cols:=ColumnDimension(TR_matrix);
#   TR_rows:=RowDimension(TR_matrix);
#
#   if n2>TR_rows or TR_cols=0 then
#     return 0:
#   fi:
#
#   col_count:=min(TR_cols,toshow):
#
#   printf(glb_mel_f2,L1,L2,n2,
#            cat("[", sprintf(glb_item_format,
#                  evalf(mel_fun(L1,L2,TR_matrix[n2,1])/scale)),
#            seq(cat(",", sprintf(glb_item_format,
#                  evalf(mel_fun(L1,L2,TR_matrix[n2,n1])/scale))),
#                                         n1=2..col_count),"]")):
#
#   printf("\n"):
#
#   return 1:
#
# end:
def Show_Mels_Row(Melements: Matrix, Lvals: list[nonnegint],
                  L1: nonnegint, L2: nonnegint, n2: int,
                  toshow: nonnegint,
                  mel_fun: Callable,
                  scale: Expr) -> int:

    if L1 not in Lvals or L2 not in Lvals:
        return 0

    L1_off: int = Lvals.index(L1)
    L2_off: int = Lvals.index(L2)

    TR_matrix: Matrix = Melements[L2_off - 1, L1_off - 1]
    TR_rows: int
    TR_cols: int
    TR_rows, TR_cols = shape(TR_matrix)

    if n2 > TR_rows or TR_cols == 0:
        return 0

    col_count: int = min(TR_cols, toshow)

    mels: list[str] = [glb_item_format.format((mel_fun(L1, L2, TR_matrix[n2 - 1, n1 - 1]) / scale).evalf())
                       for n1 in range(1, col_count + 1)]
    print(glb_mel_f2.format(L1, L2, n2, '[' + ','.join(mels) + ']'))

    return 1


# # The procedures Show_Rats and Show_Amps below call Show_Mels
# # above with its final four arguments (of eight) taking
# # particular values specified by certain global variables.
# # Thus the description of Show_Mels applies here.
# # For Show_Rats, the alternative SO(3)-reduced matrix element
# #
# #           <nf,Lf || W || ni,Li>
# #           ---------------------
# #               sqrt (2*Lf+1)
# #
# # is displayed after being acted on by the function given by
# # the procedure glb_rat_fun, and then divided by the scale factor
# # glb_rat_sft. Each value output is displayed using the format
# # given in glb_rat_format; and the phrase given in glb_rat_desg
# # is used to introduce the output.
# # The procedure Show_Amps is similar, except using different
# # global values: the procedure glb_amp_fun is the function,
# # glb_amp_sft is the scaling factor, glb_amp_format is the format,
# # and glb_amp_desg is the phrase.
#
# # Both Show_Rats and Show_Amps take the required arguments Melements
# # and Lvals, which are as for Show_Mels. Their third arguments are
# # lists of format designators: if not given, the global variables
# # glb_rat_lst and glb_amp_lst respectively are used instead.
# # Their fourth arguments specify the maximum number of values to
# # display in a list: if not given, the global variables glb_rat_num
# # and glb_rat_num respectively are used instead.
# # Both these procedures return NULL.
#
# Show_Rats:=proc(Melements::Matrix, Lvals::list,
#                   rat_lst::list(list):=glb_rat_lst,
#                   toshow::integer:=glb_rat_num,$)
#
#       global glb_rat_sft, glb_rat_fun, glb_rat_format, glb_rat_desg;
#
#   Show_Mels(Melements,Lvals,
#                rat_lst,
#                toshow,
#                glb_rat_fun,
#                glb_rat_sft,
#                glb_rat_format,
#                glb_rat_desg):
# end:
def Show_Rats(Melements: Matrix, Lvals: list[nonnegint],
              rat_lst: Designators = g.glb_rat_lst,
              toshow: int = g.glb_rat_num) -> None:
    Show_Mels(Melements, Lvals,
              rat_lst,
              toshow,
              g.glb_rat_fun,
              g.glb_rat_sft,
              g.glb_rat_format,
              g.glb_rat_desg)


# Show_Amps:=proc(Melements::Matrix, Lvals::list,
#                   amp_lst::list(list):=glb_amp_lst,
#                   toshow::integer:=glb_amp_num,$)
#
#       global glb_amp_sft, glb_amp_fun, glb_amp_format, glb_amp_desg;
#
#   Show_Mels(Melements,Lvals,
#                amp_lst,
#                toshow,
#                glb_amp_fun,
#                glb_amp_sft,
#                glb_amp_format,
#                glb_amp_desg):
# end:
def Show_Amps(Melements: Matrix, Lvals: list[nonnegint],
              amp_lst: Designators = g.glb_amp_lst,
              toshow: int = g.glb_amp_num) -> None:
    Show_Mels(Melements, Lvals,
              amp_lst,
              toshow,
              g.glb_amp_fun,
              g.glb_amp_sft,
              g.glb_amp_format,
              g.glb_amp_desg)


# ###########################################################################
#
# # The following procedure ACM_ScaleOrAdapt combines many of those
# # previously described to provide a versatile user-friendly
# # means of analysing Hamlitonians, displaying their eigenvalues,
# # and calculating and displaying transition rates and amplitudes
# # of the operator in the global variable glb_rat_TRop (which is
# # the quadrapole operator in the default implementation).
# # This procedure is conveniently used through the procedures ACM_Scale
# # and ACM_Adapt, given below, which simply set the arguments fit_eig
# # and fit_rat, and thus work in the same way.
# # Much of the functionality is controlled by values of the
# # global parameters.
#
# # The Hamiltonian is specified in ham_op; the truncated Hilbert space
# # is specified by the arguments anorm, lambda_base, nu_min, nu_max,
# # v_min, v_max, L_min, L_max as above.
# # The final argument L_max is optional - if omitted then L_max=L_min,
# # so that a single angular momentum value is used.
# # The values of fit_eig and fit_rat determine how the values that are
# # displayed are scaled.
# # If the argument fit_eig is zero then the relative eigenvalues
# # (relative to the lowest value) are divided by the current values of
# # the global parameter glb_eig_sft. If fit_eig is non-zero then the
# # value of glb_eig_sft is first determined so that the relative eigenvalue
# # of the (glb_eig_idx)th state of angular momentum glb_eig_L comes out
# # to be glb_eig_fit.
# # If the argument fit_rat is zero then the transition rates are divided
# # by the current values of the global parameter glb_rat_sft, and the
# # transition amplitudes are divided by the global parameter glb_amp_sft.
# # If fit_rat is non-zero then the value of glb_rat_sft is first determined
# # so that the transition rate from the (glb_rat_1dx)th state of
# # angular momentum glb_eig_L1 to the (glb_rat_2dx)th state of angular
# # momentum glb_eig_L2 comes out to be glb_rat_fit. In this latter case,
# # the scale parameter glb_amp_sft is then determined from glb_rat_sft
# # using the procedure given in glb_amp_sft_fun (it is the square root
# # by default).
#
# # Eigenvalues of the Hamiltonian are displayed using the procedure
# # Show_Eigs, and is thus of the format described for that procedure
# # above. The number of eigenvalues displayed for each angular momentum
# # is restricted to glb_eig_num.
# # Transition rates and amplitudes are displayed using the procedures
# # Show_Rats and Show_Amps, and thus have the format described above for
# # these procedures, the values displayed being determined by functions
# # given in the procedures glb_rat_fun and glb_amp_fun respectively.
# # The transition rates that are displayed are determined by the
# # designations listed in the global variable glb_rat_lst.
# # When lists of values are designated, the maximum number of states
# # for each angular momentum is restricted to glb_rat_num.
# # The transition amplitudes that are displayed are determined by the
# # designations listed in the global variable glb_amp_lst.
# # When lists of values are designated, the maximum number of states
# # for each angular momentum is restricted to glb_amp_num.
#
# # The return value is the triple
# #                 [eigen_vals,Melements,Lvals],
# # where eigen_vals is a list of lists of eigenvalues (one list for each
# # L-space in Lvals), and Melements are the alternative SO(3)-reduced matrix
# # elements of transition rates of the operator glb_rat_TRop
# # (calculated in AmpXspeig) stored as a block matrix.
# # This latter is only calculated when either of the lists glb_rat_lst
# # (of transition rate designators) or glb_amp_lst (or transition
# # amplitude designators) is non-empty. Otherwise, Melements is set
# # to be a 0x0 Matrix, indicating that none are available.
# # The first and third elements of the return value may be used as the
# # first two arguments to Show_Eigs and the second and third as the first
# # two arguments to Show_Rats and Show_Amps to display further eigenenergies,
# # transition rates/amplitudes without the need for recalculation.
#
#
# ACM_ScaleOrAdapt:=proc(fit_eig::nonnegint,fit_rat::nonnegint,
#                      ham_op::list,
#                      anorm::algebraic, lambda_base::algebraic,
#                      nu_min::nonnegint, nu_max::nonnegint,
#                      v_min::nonnegint, v_max::nonnegint,
#                      L_min::nonnegint, L_max::nonnegint,$)
#       local eigen_quin,tran_mat,Lvals,eigen_low,L_mx,L1_off,L2_off;
#       global glb_eig_num, glb_rat_lst, glb_amp_lst,
#              glb_eig_fit, glb_eig_L, glb_eig_idx, glb_eig_rel,
#              glb_rat_TRop, glb_rat_fun,
#              glb_rat_num, glb_amp_num,
#              glb_rat_fit, glb_rat_L1, glb_rat_1dx, glb_rat_L2, glb_rat_2dx,
#              glb_amp_sft_fun,
#              glb_eig_sft, glb_rat_sft, glb_amp_sft; # these might be set here
#
#   if _npassed<11 then  # no L_max
#     L_mx:=L_min;
#   else
#     L_mx:=L_max
#   fi:
#
#   # When fitting values (if either fit_eig or fit_rat is non-zero)
#   # we must ensure that the eigenvalue or transition rate with
#   # respect to which we fit, and thus choose scaling parameters,
#   # will actually be obtained. If not, we exit with an error message.
#   # Note that we only perform this check when values of each variety
#   # will actually be output (glb_eig_num>0 and nops(glb_rat_lst)>0 resp.)
#
#   # First check the eigenenergy parameters
#
#   if fit_eig>0 and glb_eig_num>0 then
#     if glb_eig_L<L_min or glb_eig_L>L_mx or
#          glb_eig_idx>dimXspace(nu_min,nu_max,v_min,v_max,glb_eig_L) then
#       error "Reference state %1(%2) not available", glb_eig_L, glb_eig_idx;
#     fi:
#   fi:
#
#   # Now check the parameters for the transition rates
#
#   if fit_rat>0 and nops(glb_rat_lst)>0 then
#     if glb_rat_L1<L_min or glb_rat_L1>L_mx or
#          glb_rat_1dx>dimXspace(nu_min,nu_max,v_min,v_max,glb_rat_L1) then
#       error "Reference state %1(%2) not available", glb_rat_L1, glb_rat_1dx;
#     fi:
#
#     if glb_rat_L2<L_min or glb_rat_L2>L_mx or
#          glb_rat_2dx>dimXspace(nu_min,nu_max,v_min,v_max,glb_rat_L2) then
#       error "Reference state %1(%2) not available", glb_rat_L2, glb_rat_2dx;
#     fi:
#   fi:
#
#   # diagonalise the Hamiltonian on the specified space.
#   # output is [ eigenval_list, Lvals, Ps, Xparams ].
#
#   eigen_quin:=DigXspace(ham_op,_passed[4..-1]):
#   Lvals:=eigen_quin[4]:
#
#   if glb_eig_num>0 then    # require eigenvalue output
#
#     if fit_eig>0 then   # determine global scale factor for eigenvalues
#
#       if glb_eig_rel then  # take eigenvalues relative to smallest
#         eigen_low:=min_head(eigen_quin[1]);   # smallest eigenvalue
#       else              # take relative to 0
#         eigen_low:=0;
#       fi:
#
#       member(glb_eig_L,Lvals,'LL'):   # find index for required L
#       glb_eig_sft:=(eigen_quin[1][LL][glb_eig_idx]-eigen_low)/glb_eig_fit:
#
#       if glb_eig_sft=0 then
#         error "Cannot scale: reference state %1(%2) has lowest energy",
#                                                     glb_eig_L, glb_eig_idx;
#       fi
#     fi:
#
#     # display all required eigenvalues, with scaling given by glb_eig_sft.
#
#     Show_Eigs(eigen_quin[1],Lvals,glb_eig_num):
#   fi:
#
#   # Now turn attention to the transition rates, if any are required...
#
#   if nops(glb_rat_lst)>0 or nops(glb_amp_lst)>0 then
#
#     # obtain raw transition amplitudes
#
#     tran_mat:=AmpXspeig(glb_rat_TRop,op(2..-1,eigen_quin)):
#
#     if fit_rat>0 then   # determine global scale factor for transition rates
#       member(glb_rat_L1,Lvals,'L1_off'):   # find indices for required Ls
#       member(glb_rat_L2,Lvals,'L2_off'):
#
#       glb_rat_sft:=abs(glb_rat_fun(glb_rat_L1,glb_rat_L2,
#              tran_mat[L2_off,L1_off][glb_rat_2dx,glb_rat_1dx]))/glb_rat_fit;
#
#       if glb_rat_sft=0 then
#         error "Cannot scale zero transition rate B(E2: %1(%2) -> %3(%4))",
#                    glb_rat_L1,glb_rat_1dx,glb_rat_L2,glb_rat_2dx,glb_rat_fit;
#       fi:
#
#       # and set scaling factor for amplitudes
#
#       glb_amp_sft:=glb_amp_sft_fun(glb_rat_sft);
#     fi:
#
#     # display required transition rates with scaling factor given
#     # by glb_rat_sft, and then that for amplitudes with scaling factor
#     # given by glb_amp_sft (these are global variables).
#
#     Show_Rats(tran_mat, Lvals, glb_rat_lst, glb_rat_num):
#     Show_Amps(tran_mat, Lvals, glb_amp_lst, glb_amp_num):
#
#     # return the raw data in case more are required.
#
#   else # set tran_mat to a NULL matrix to indicate that there are no
#        # matrix elements available (cannot simply set to NULL).
#
#     tran_mat:=Matrix(0,0):
#
#   fi:
#
#   [eigen_quin[1],tran_mat,Lvals]:
#
# end;
def ACM_ScaleOrAdapt(fit_eig: nonnegint, fit_rat: nonnegint,
                     ham_op: OperatorSum,
                     anorm: Expr, lambda_base: Expr,
                     nu_min: nonnegint, nu_max: nonnegint,
                     v_min: nonnegint, v_max: nonnegint,
                     L_min: nonnegint, L_max: Optional[nonnegint] = None
                     ) -> tuple[EigenValues, Matrix, LValues]:
    require_nonnegint('fit_eig', fit_eig)
    require_nonnegint('fit_rat', fit_rat)
    require_nonnegint_range('nu', nu_min, nu_max)
    require_nonnegint_range('v', v_min, v_max)

    L_mx: nonnegint = L_min if L_max is None else L_max
    require_nonnegint_range('L', L_min, L_mx)

    if fit_eig > 0 and g.glb_eig_num > 0:
        if g.glb_eig_L < L_min or g.glb_eig_L > L_mx or \
                g.glb_eig_idx > dimXspace(nu_min, nu_max, v_min, v_max, g.glb_eig_L):
            raise ValueError(f'Reference state {g.glb_eig_L}({g.glb_eig_idx}) not available')

    if fit_rat > 0 and len(g.glb_rat_lst) > 0:
        if g.glb_rat_L1 < L_min or g.glb_rat_L1 > L_mx or \
                g.glb_rat_1dx > dimXspace(nu_min, nu_max, v_min, v_max, g.glb_rat_L1):
            raise ValueError(f'Reference state {g.glb_rat_L1}({g.glb_rat_1dx}) not available')

        if g.glb_rat_L2 < L_min or g.glb_rat_L2 > L_mx or \
                g.glb_rat_2dx > dimXspace(nu_min, nu_max, v_min, v_max, g.glb_rat_L2):
            raise ValueError(f'Reference state {g.glb_rat_L2}({g.glb_rat_2dx}) not available')

    eigen_quin: tuple[EigenValues, EigenBases, XParams, LValues] = \
        DigXspace(ham_op, anorm, lambda_base, nu_min, nu_max, v_min, v_max, L_min, L_max)
    eigen_vals: EigenValues = eigen_quin[0]
    eigen_bases: EigenBases = eigen_quin[1]
    Xparams: XParams = eigen_quin[2]
    Lvals: LValues = eigen_quin[3]

    if g.glb_eig_num > 0:

        if fit_eig > 0:

            eigen_low: float = min_head(eigen_vals) if g.glb_eig_rel else 0

            if g.glb_eig_L not in Lvals:
                raise ValueError(f'glb_eig_L ({g.glb_eig_L}) is not in list of L values.')
            LL: int = Lvals.index(g.glb_eig_L)
            g.glb_eig_sft = (eigen_vals[LL][g.glb_eig_idx - 1] - eigen_low) / g.glb_eig_fit

            if g.glb_eig_sft == 0:
                raise ValueError(f'Cannot scale: reference state {g.glb_eig_L}({g.glb_eig_idx}) has lowest energy')

        Show_Eigs(eigen_vals, Lvals, g.glb_eig_num)

    trans_mat: Matrix
    if len(g.glb_rat_lst) > 0 or len(g.glb_amp_lst) > 0:

        trans_mat = AmpXspeig(g.glb_rat_TRop, eigen_bases, Xparams, Lvals)

        if fit_rat > 0:
            L1: int = g.glb_rat_L1
            L2: int = g.glb_rat_L2
            i1: int = g.glb_rat_1dx
            i2: int = g.glb_rat_2dx

            if L1 not in Lvals:
                raise ValueError(f'glb_rat_L1 ({L1}) is not in list of L values.')
            L1_off: int = Lvals.index(L1)

            if L2 not in Lvals:
                raise ValueError(f'glb_rat_L2 ({L2}) is not in list of L values.')
            L2_off: int = Lvals.index(L2)

            mel: float = trans_mat[L2_off, L1_off][i2 - 1, i1 - 1]
            g.glb_rat_sft = abs(g.glb_rat_fun(L1, L2, mel)) / g.glb_rat_fit

            if g.glb_rat_sft == 0:
                raise ValueError(f'Cannot scale zero transition rate B(E2: {L1}({i1}) -> {L2}({i2}))')

            g.glb_amp_sft = g.glb_amp_sft_fun(g.glb_rat_sft)

        Show_Rats(trans_mat, Lvals, g.glb_rat_lst, g.glb_rat_num)
        Show_Amps(trans_mat, Lvals, g.glb_amp_lst, g.glb_amp_num)

    else:

        trans_mat = Matrix()

    return eigen_vals, trans_mat, Lvals


# # The following procedure ACM_Scale invokes the procedure ACM_ScaleOrAdapt
# # above with fit_eig=0 and fit_rat=0 so that the values of the scaling
# # parameters glb_eig_sft, glb_rat_sft and glb_amp_sft are used unchanged
# # to scale the displayed values of the eigenenergies, transition rates
# # and amplitudes.
# # For details, see the description of ACM_ScaleOrAdapt above.
#
# ACM_Scale:=proc(ham_op::list,
#                  anorm::algebraic, lambda_base::algebraic,
#                  nu_min::nonnegint, nu_max::nonnegint,
#                  v_min::nonnegint, v_max::nonnegint,
#                  L_min::nonnegint, L_max::nonnegint,$)
#
#   ACM_ScaleOrAdapt(0,0,_passed):
# end;


def ACM_Scale(ham_op: OperatorSum,
              anorm: Expr, lambda_base: Expr,
              nu_min: nonnegint, nu_max: nonnegint,
              v_min: nonnegint, v_max: nonnegint,
              L_min: nonnegint, L_max: Optional[nonnegint] = None
              ) -> tuple[EigenValues, Matrix, LValues]:
    return ACM_ScaleOrAdapt(0, 0, ham_op, anorm, lambda_base,
                            nu_min, nu_max, v_min, v_max, L_min, L_max)

# # The following procedure ACM_Adapt invokes the procedure ACM_ScaleOrAdapt
# # above with fit_eig=1 and fit_rat=1 so that the values of the scaling
# # parameters glb_eig_sft, glb_rat_sft and glb_amp_sft are recalculated
# # before being used to scale the displayed values of the eigenenergies,
# # transition rates and amplitudes.
# # For details, see the description of ACM_ScaleOrAdapt above.
#
# ACM_Adapt:=proc(ham_op::list,
#                  anorm::algebraic, lambda_base::algebraic,
#                  nu_min::nonnegint,nu_max::nonnegint,
#                  v_min::nonnegint,v_max::nonnegint,
#                  L_min::nonnegint,L_max::nonnegint,$)
#
#   ACM_ScaleOrAdapt(1,1,_passed):
# end;


def ACM_Adapt(ham_op: OperatorSum,
              anorm: Expr, lambda_base: Expr,
              nu_min: nonnegint, nu_max: nonnegint,
              v_min: nonnegint, v_max: nonnegint,
              L_min: nonnegint, L_max: Optional[nonnegint] = None
              ) -> tuple[EigenValues, Matrix, LValues]:
    return ACM_ScaleOrAdapt(1, 1, ham_op, anorm, lambda_base,
                            nu_min, nu_max, v_min, v_max, L_min, L_max)
