"""1. Specification of global constants, and procedures that can be used to set their values."""

import math
from typing import Callable, Optional

from acmpy.internal_operators import OperatorSum, Op_AM, quad_op
from acmpy.spherical_space import dimSO3
from acmpy.so5_so3_cg import CG_SO3
from acmpy.compat import nonnegint, require_nonnegint, irem, is_odd, posint, require_posint

# ###########################################################################
# ####----------------------- Global Constants --------------------------####
# ###########################################################################
#
# # Here are specified various constants.
# # They should not be altered by the user.
# # They are mainly used to signify certain operators.
# # Hamiltonians and other operators will be expressed in terms of
# # these values.
#
# ACM_version:=1.4:

"""The version identifier should be implemented as a Python string, not a float."""
ACM_version: str = '1.4'


# # The following procedure definitions determine functions used for displaying
# # the transition rates and amplitudes (the particular procedures in force at
# # a given time are stored in the global variables glb_rat_fun & glb_amp_fun).
# # These are as listed in Table V.
# # In addition to the matrix element Mel, they make use of the angular
# # momenta of the initial state Li, and final state Lf.
# # (Maple doesn't allow me to specify a delimiting fourth argument $ here!)
#
# # In the first of these procedures, the value of glb_rat_TRopAM (default 2),
# # is used to access the appropriate SO(3) CG coefficient:
# # glb_rat_TRopAM is the known angular momentum of the transition operator.
#
# quad_amp_fun:=proc(Li,Lf,Mel)
#   global glb_rat_TRopAM;
#   Mel*CG_SO3(Li,Li,glb_rat_TRopAM,Lf-Li,Lf,Lf)
# end;
def quad_amp_fun(Li: nonnegint, Lf: nonnegint, Mel: float) -> float:
    return Mel * float(CG_SO3(Li, Li, glb_rat_TRopAM, Lf - Li, Lf, Lf))


# mel_amp_fun:=proc(Li,Lf,Mel)
#   Mel*sqrt(2*Lf+1)
# end;
def mel_amp_fun(_Li: nonnegint, Lf: nonnegint, Mel: float) -> float:
    return Mel * math.sqrt(2 * Lf + 1)


# unit_amp_fun:=proc(Li,Lf,Mel)
#   Mel
# end;
def unit_amp_fun(_Li: nonnegint, _Lf: nonnegint, Mel: float) -> float:
    return Mel


# quad_rat_fun:=proc(Li,Lf,Mel)
#   Mel^2*dimSO3(Lf)/dimSO3(Li)
# end;
def quad_rat_fun(Li: nonnegint, Lf: nonnegint, Mel: float) -> float:
    return Mel ** 2 * dimSO3(Lf) / dimSO3(Li)


# mel_rat_fun:=proc(Li,Lf,Mel)
#   Mel^2*dimSO3(Lf)
# end;
def mel_rat_fun(_Li: nonnegint, Lf: nonnegint, Mel: float) -> float:
    return Mel ** 2 * dimSO3(Lf)


# unit_rat_fun:=proc(Li,Lf,Mel)
#   Mel^2
# end;
def unit_rat_fun(_Li: nonnegint, _Lf: nonnegint, Mel: float) -> float:
    return Mel**2


# # The following was described in a previous version
#
# mix_amp_fun:=proc(Li,Lf,Mel)
#   global glb_rat_TRopAM;
#   Mel*gen_amp_mul(Li,Lf,glb_rat_TRopAM)
# end;
def mix_amp_fun(Li: nonnegint, Lf: nonnegint, Mel: float) -> float:
    return Mel * gen_amp_mul(Li, Lf, glb_rat_TRopAM)


# gen_amp_mul:=proc(Li,Lf,Lt,$)
#   if Li=Lf then CG_SO3(Lf,Lf,Lt,0,Lf,Lf)
#   else sqrt(2*Lf+1)
#   fi:
# end;
def gen_amp_mul(Li: nonnegint, Lf: nonnegint, Lt: nonnegint) -> float:
    if Li == Lf:
        return float(CG_SO3(Lf, Lf, Lt, 0, Lf, Lf))

    return math.sqrt(2 * Lf + 1)


# # The following procedure definitions determine functions used for
# # determining lambda as a function of seniority v
# # (the particular procedure in force at a given time is stored
# #  in the global variable glb_lam_fun: this is only accessed
# #  in the functions RepXspace_Twin, RepXspace_Pi, RepXspace_PiPi,
# #  RepXspace_PiqPi).
# # The first three are as listed in Table VI.
# # These functions return lambda_v-lambda_0 which must be an integer.
# # Analytic matrix elements result if the returned integer is of the
# # same parity as v (see Section 5.1).
#
# lambda_fix_fun:=proc(v::nonnegint)   # for fixed lambda
#   0
# end;
def lambda_fix_fun(v: nonnegint) -> nonnegint:
    require_nonnegint('v', v)

    return 0


# lambda_sho_fun:=proc(v::nonnegint)   # for SHO lambda variation
#   v
# end;
def lambda_sho_fun(v: nonnegint) -> nonnegint:
    require_nonnegint('v', v)

    return v


# lambda_acm_fun:=proc(v::nonnegint)   # for lambda varying with parity of v
#   irem(v,2)
# end;
def lambda_acm_fun(v: nonnegint) -> nonnegint:
    require_nonnegint('v', v)

    return irem(v, 2)


# lambda_jig_fun:=proc(v::nonnegint)   # A little mixture, used for testing
#   if v=0 then
#     0
#   else
#     2-irem(v,2)
#   fi
# end;
def lambda_jig_fun(v: nonnegint) -> nonnegint:
    require_nonnegint('v', v)

    return 0 if v == 0 else 2 - irem(v, 2)


# # Further procedures of a similar nature may be obtained using the
# # following procedure, which returns the name of a procedure that
# # itself returns the nearest integer to
# #    sqrt( (v+3/2)^2 + C ) - sqrt( 9/4 + C )
# # of the same parity as v.
# # This is described in Appendix B.3.
#
# lambda_davi_fun:=proc(C::constant)
#   local difffun:
#
#     difffun:=proc(v::nonnegint) option operator,arrow;
#        local diffint:
#        diffint:=floor(sqrt((v+1.5)^2+C)-sqrt(2.25+C)):
#        if type(diffint-v,odd) then
#          diffint+1:
#        else
#          diffint:
#        fi:
#     end:
#
#    difffun:
# end:
LambdaFunction = Callable[[nonnegint], int]


def lambda_davi_fun(C: float) -> LambdaFunction:
    def difffun(v: nonnegint) -> int:
        require_nonnegint('v', v)

        diffint: int = math.floor(math.sqrt((v + 1) ** 2 + C) - math.sqrt(2.25 + C))

        return diffint + 1 if is_odd(diffint - v) else diffint

    return difffun


# # We supply our own version of the square root that has `procedure` type.
# # It is necessary to use such a procedure to pass as an argument
# # when the type is being tested, because sqrt itself is not a `procedure`!
# # glb_amp_sft_fun:=sqrt:
#
# sqrt_fun:=proc(sft)
#   sqrt(evalf(sft)):
# end;
ScalingFactorFunction = Callable[[float], float]

sqrt_fun: ScalingFactorFunction = math.sqrt


# # The following determine values used to set the defaults for how the
# # transition rates and amplitudes of the quadrupole operator are
# # displayed by the procedures Show_Rats and Show_Amps.
#
# def_rat_desg:="transition rates":
# def_rat_format:="  B(E2: %s) = %s":
# def_amp_desg:="transition amplitudes":
# def_amp_format:="  Amp( %s ) = %s":
def_rat_desg: str = "transition rates"
def_rat_format: str = "  B(E2: {}) = {}"
def_amp_desg: str = "transition amplitudes"
def_amp_format: str = "  Amp( {} ) = {}"


# # If the Show_Mels procedure is used directly (Show_Rats and
# # Show_Amps call Show_Mels), the following two values can be used
# # (in fact, they are used by default).
# # These can also be used for the rates and amplitudes of other operators,
# # if the user hasn't defined anything else.
#
# def_mel_desg:="matrix elements":
# def_mel_format:="  ME( %s ) = %s":
def_mel_desg: str = "matrix elements"
def_mel_format: str = "  ME( %{0!s} ) = {1!s}"


# # The data that is produced by the main procedures is displayed
# # according to the values of various global parameters.
# # These are listed here, along with some initial values.
# # The values here should not be set directly, but by using the
# # ACM_set_ routines below.
# # Below, we use the ACM_set_defaults procedure which calls all
# # of the ACM_set_ procedures to set default values, overriding
# # the values given here.
# # (it may also be convenient to call ACM_set_ procedures from
# #  a file (acm-user.mpl) and read that into a Maple session.)
#
# # The following store the current factors used to divide
# # eigenvalues, transition rates and amplitudes displayed
# # respectively by the procedures Show_Eigs(), Show_Rats() and
# # Show_Amps(); and via these, by the procedures ACM_Scale()
# # and ACM_Adapt():
#
# glb_eig_sft:=1.0:
# glb_rat_sft:=1.0:
# glb_amp_sft:=1.0:
glb_eig_sft: float = 1.0
glb_rat_sft: float = 1.0
glb_amp_sft: float = 1.0


# # The following store the precision for floating point values that
# # are displayed by the procedures Show_Eigs(), Show_Rats() and
# # Show_Amps(); and via these, by the procedures ACM_Scale()
# # and ACM_Adapt():
#
# glb_rel_pre:=2:
# glb_rel_wid:=7:
# glb_low_pre:=4:
glb_rel_pre: int = 2
glb_rel_wid: int = 7
glb_low_pre: int = 4


# # The following store the maximal number of entries for horizontal
# # lists of eigenvalues, transition rates and amplitudes that are
# # respectively displayed by the procedures Show_Eigs(), Show_Rats()
# # and Show_Amps(); and via these, by the procedures ACM_Scale()
# # and ACM_Adapt():
#
# glb_eig_num:=4:
# glb_rat_num:=4:
# glb_amp_num:=4:
glb_eig_num: int = 4
glb_rat_num: int = 4
glb_amp_num: int = 4


# # The following specify how ACM_Adapt() determines the scale factor
# # glb_eig_sft. This factor is determined such that the energy of
# # the (glb_eig_idx)th state of AM glb_eig_L comes out to be glb_eig_fit.
#
# glb_eig_fit:=6.0:
# glb_eig_L:=2:
# glb_eig_idx:=1:
glb_eig_fit: float = 6.0
glb_eig_L: int = 2
glb_eig_idx: int = 1


# # The following specify how ACM_Adapt() determines the scale factor
# # glb_rat_sft. This factor is determined such that the transition rate
# # from the (glb_rat_1dx)th state of AM glb_eig_L1 to the
# # (glb_rat_2dx)th state of AM glb_eig_L2 comes out to be glb_rat_fit.
#
# glb_rat_fit:=100.0:
# glb_rat_L1:=2:
# glb_rat_L2:=0:
# glb_rat_1dx:=1:
# glb_rat_2dx:=1:
glb_rat_fit: float = 100.0
glb_rat_L1: int = 2
glb_rat_L2: int = 0
glb_rat_1dx: int = 1
glb_rat_2dx: int = 1


# # The following specifies a procedure which determines the basis type.
# # This is a function which gives the value of lambda_v-lambda_0.
#
# glb_lam_fun:=lambda_acm_fun:
glb_lam_fun: LambdaFunction = lambda_acm_fun


# # The following store the current transition operator and its
# # angular momentum.
# # The former is the operator for which transition rates and
# # amplitudes are calculated in the procedures ACM_Scale() and ACM_Adapt().
# # The latter is used in two (minor) ways:
# #   1. by Show_Mels() (via Show_Rats & Show_Amps) so that only those
# #      lists for which |Lf-Li| <= glb_rat_TRopAM are
# #      output, for otherwise the MEs are zero;
# #   2. in a couple of the predefined procedures above
# #      (mix_amp_fun & quad_amp_fun).
#
# glb_rat_TRop:=quad_op:
# glb_rat_TRopAM:=2:
glb_rat_TRop: OperatorSum = quad_op
glb_rat_TRopAM: nonnegint = 2


# # The following determine how "transition rates" are displayed in the
# # procedure Show_Rats (which is called by ACM_Scale and ACM_Adapt).
# # The first specifies the formula used, the second the format used to
# # display each value, the third the phrase used to designate the values.
# # (e.g. "transition rates")
#
# glb_rat_fun:=quad_rat_fun:
# glb_rat_format:=def_rat_format:
# glb_rat_desg:=def_rat_desg:
MatrixElementFunction = Callable[[nonnegint, nonnegint, float], float]

glb_rat_fun: MatrixElementFunction = quad_rat_fun
glb_rat_format: str = def_rat_format
glb_rat_desg: str = def_rat_desg


# # The following determine how "transition rates" are displayed in the
# # procedure Show_Amps (which is called by ACM_Scale and ACM_Adapt).
# # The first specifies the formula used, the second the format used to
# # display each value, the third the phrase used to designate the values.
# # (e.g. "transition amplitudes")
#
# glb_amp_fun:=quad_amp_fun:
# glb_amp_format:=def_amp_format:
# glb_amp_desg:=def_amp_desg:
glb_amp_fun: MatrixElementFunction = quad_amp_fun
glb_amp_format: str = def_amp_format
glb_amp_desg: str = def_amp_desg


# # The following specifies the function by which the scaling factor
# # for transition amplitudes (glb_amp_sft) is obtained from that
# # (glb_rat_sft) for transition rates:
#
# glb_amp_sft_fun:=sqrt:
glb_amp_sft_fun: ScalingFactorFunction = math.sqrt


# # The following determines how the matrix element labels are displayed:
#
# glb_tran_format:="%s(%s) -> %s(%s)":
# glb_tran_fill:="#":
glb_tran_format: str = '{}({}) -> {}({})'
glb_tran_fill: str = '#'


# # The following store the lists of transition rate and transition amplitude
# # designators (each initially empty):
#
# glb_rat_lst:=[]:
# glb_amp_lst:=[]:
Designator = tuple[int, ...]
Designators = tuple[Designator, ...]
glb_rat_lst: Designators = ()
glb_amp_lst: Designators = ()


# # The following flag indicates whether, in ACM_Scale, ACM_Adapt
# # and Show_Eigs, eigenvalues are displayed relative to their
# # lowest value (true), or absolute (false).
#
# glb_eig_rel:=true:
glb_eig_rel: bool = True


# # The following parameter, if positive, specifies a temporary
# # increase to the size of the radial space, to improve accuracy
# # of radial reps.
# # It is used only by the procedure RepXspace_Twin (which is called
# # by RepXspace).
#
# glb_nu_lap:=0:
glb_nu_lap: int = 0


# ###########################################################################
#
# # We now give a set of procedures that specify values of the above
# # parameters. The last of these, ACM_set_defaults, uses the others
# # to set values for all of the above parameters.
# # In each of these procedures, if the final passed argument is 1
# # then the procedure prints out a brief description of its effect.
# # The return value contains the now current values of all the
# # parameters that the procedure can set.
#
# # The following sets the values of glb_eig_sft, glb_rat_sft, glb_amp_sft
# # Note that the scaling factor glb_amp_sft is obtained from glb_rat_sft
# # using the procedure given by glb_amp_sft_fun.
#
# ACM_set_scales:=proc(eig_sft::constant,rat_sft::constant,
#                       show::integer:=1,$)
#       global glb_eig_sft,glb_rat_sft,glb_amp_sft,glb_amp_sft_fun;
#
#   if _npassed>0 then
#     glb_eig_sft:=evalf(eig_sft);
#   fi:
#   if _npassed>1 then
#     glb_rat_sft:=evalf(rat_sft);
#   fi:
#
#   glb_amp_sft:=glb_amp_sft_fun(glb_rat_sft);  #default is square root
#
#   ACM_show_scales(show):
# end;
def ACM_set_scales(eig_sft: Optional[float] = None,
                   rat_sft: Optional[float] = None,
                   show: int = 1) -> None:
    global glb_eig_sft, glb_rat_sft, glb_amp_sft

    if eig_sft is not None:
        glb_eig_sft = eig_sft

    if rat_sft is not None:
        glb_rat_sft = rat_sft

    glb_amp_sft = glb_amp_sft_fun(glb_rat_sft)  # default is square root

    ACM_show_scales(show)


# # The following displays and returns the values of the scaling factors
# # glb_eig_sft, glb_rat_sft, glb_amp_sft.
#
# ACM_show_scales:=proc(show::integer:=1,$)
#       global glb_eig_sft,glb_rat_sft,glb_amp_sft,
#              glb_rat_desg,glb_amp_desg:
#
#   if show>0 then
#     printf("Relative eigenenergies to be multiplied by %f;\n",
#                  evalf(1/glb_eig_sft));
#     printf("\"%s\" to be multiplied by %f;\n",
#                  glb_rat_desg,evalf(1/glb_rat_sft));
#     printf("\"%s\" to be multiplied by %f.\n",
#                  glb_amp_desg,evalf(1/glb_amp_sft));
#   fi:
#
#   [glb_eig_sft,glb_rat_sft,glb_amp_sft]:
# end;
def ACM_show_scales(show: int) -> tuple[float, float, float]:
    if show > 0:
        print(f'Relative eigenenergies to be multiplied by {1 / glb_eig_sft};')
        print(f'"{glb_rat_desg}" to be multiplied by {1 / glb_rat_sft};')
        print(f'"{glb_amp_desg}" to be multiplied by {1 / glb_amp_sft}.')

    return glb_eig_sft, glb_rat_sft, glb_amp_sft


# # The following sets glb_amp_sft_fun, and returns NULL:
#
# ACM_set_sft_fun:=proc(amp_fun::procedure:=glb_amp_sft_fun,
#                          show::integer:=1,$)
#     global glb_amp_sft_fun,glb_amp_desg;
#
#   glb_amp_sft_fun:=amp_fun;
#
#   if show>0 then
#       printf("\"%s\" scaling factor calculated"
#                  " using the procedure: \"%a\".\n",
#                     glb_amp_desg,
#                     glb_amp_sft_fun):
#   fi:
#
#   glb_amp_sft_fun:
# end;
def ACM_set_sft_fun(amp_fun: Callable = glb_amp_sft_fun,
                    show: int = 1) -> Callable:
    global glb_amp_sft_fun

    glb_amp_sft_fun = amp_fun
    if show > 0:
        print(f'"{glb_amp_desg}" scaling factor calculated' +
              f' using the procedure: {glb_amp_sft_fun.__name__}.')

    return glb_amp_sft_fun


# # The following sets the values of glb_rel_pre, glb_rel_wid, and glb_low_pre
#
# ACM_set_output:=proc(rel_pre::nonnegint,rel_wid::nonnegint,low_pre::nonnegint,
#                       show::integer:=1,$)
#     global glb_low_pre,glb_rel_wid,glb_rel_pre;
#
#   if _npassed>0 then
#     glb_rel_pre:=rel_pre;
#   fi:
#   if _npassed>1 then
#     glb_rel_wid:=rel_wid;
#   fi:
#   if _npassed>2 then
#     glb_low_pre:=low_pre;
#   fi:
#
#   if show>0 then
#   printf("%d decimal places for each displayed value,\n",glb_rel_pre);
#   printf("%d total digits for each displayed value,\n",glb_rel_wid);
#   printf("except %d decimal places for lowest (absolute) eigenvalue.\n",
#                                                        glb_low_pre);
#   fi:
#
#   [glb_rel_pre, glb_rel_wid, glb_low_pre]:
# end;
def ACM_set_output(rel_pre: Optional[nonnegint] = None,
                   rel_wid: Optional[nonnegint] = None,
                   low_pre: Optional[nonnegint] = None,
                   show: int = 1) -> tuple[nonnegint, nonnegint, nonnegint]:
    global glb_low_pre, glb_rel_wid, glb_rel_pre

    if rel_pre is not None:
        require_nonnegint('rel_pre', rel_pre)
        glb_rel_pre = rel_pre

    if rel_wid is not None:
        require_nonnegint('rel_wid', rel_wid)
        glb_rel_wid = rel_wid

    if low_pre is not None:
        require_nonnegint('low_pre', low_pre)
        glb_low_pre = low_pre

    if show > 0:
        print(f'{glb_rel_pre} decimal places for each displayed value,')
        print(f'{glb_rel_wid} total digits for each displayed value,')
        print(f'except {glb_low_pre} decimal places for lowest (absolute) eigenvalue.')

    return glb_rel_pre, glb_rel_wid, glb_low_pre


# # The following sets the values of glb_eig_num, glb_rat_num, and
# # glb_amp_num. For simplicity, the latter two are set equal.
#
# ACM_set_listln:=proc(eig_num::nonnegint,rat_num::nonnegint,
#                       show::integer:=1,$)
#       global glb_eig_num,glb_rat_num,glb_amp_num;
#
#   if _npassed>0 then
#     glb_eig_num:=eig_num;
#   fi:
#   if _npassed>1 then
#     glb_rat_num:=rat_num;
#     glb_amp_num:=rat_num;
#   fi:
#
#   if show>0 then
#   printf("Display lowest %d eigenvalue(s) at each L.\n",glb_eig_num);
#   printf("Display lowest %d rate/amplitude(s) in each list.\n",glb_rat_num);
#   fi:
#
#   [glb_eig_num, glb_rat_num, glb_amp_num]:
# end;
def ACM_set_listln(eig_num: Optional[nonnegint] = None,
                   rat_num: Optional[nonnegint] = None,
                   show: int = 1) -> tuple[nonnegint, nonnegint, nonnegint]:
    global glb_eig_num, glb_rat_num, glb_amp_num

    if eig_num is not None:
        require_nonnegint('eig_num', eig_num)
        glb_eig_num = eig_num

    if rat_num is not None:
        require_nonnegint('rat_num', rat_num)
        glb_rat_num = rat_num
        glb_amp_num = rat_num

    if show > 0:
        print(f'Display lowest {glb_eig_num} eigenvalue(s) at each L.')
        print(f'Display lowest {glb_rat_num} rate/amplitude(s) in each list.')

    return glb_eig_num, glb_rat_num, glb_amp_num


# # The following sets the boolean value of glb_eig_rel.
#
# ACM_set_datum:=proc(datflag::nonnegint:=1,
#                       show::integer:=1,$)
#       global glb_eig_rel:
#
#   glb_eig_rel:=evalb(datflag>0):
#
#   if show>0 then
#     if glb_eig_rel then
#       printf("Eigenvalues displayed relative to minimal value.\n")
#     else
#       printf("Absolute eigenvalues displayed.\n")
#     fi:
#   fi:
#
#   glb_eig_rel:
# end;
def ACM_set_datum(datflag: nonnegint = 1,
                  show: int = 1) -> bool:
    global glb_eig_rel

    require_nonnegint('datflag', datflag)
    glb_eig_rel = datflag > 0

    if show > 0:
        if glb_eig_rel:
            print('Eigenvalues displayed relative to minimal value.')
        else:
            print('Absolute eigenvalues displayed.')

    return glb_eig_rel


# # The following sets the values of glb_eig_fit, glb_eig_L, glb_eig_idx,
# # which are used by ACM_Adapt to determine the factor glb_eig_sft.
#
# ACM_set_eig_fit:=proc(eig_fit::constant:=glb_eig_fit,
#                       eig_L::nonnegint:=glb_eig_L,
#                       eig_idx::posint:=1, show::integer:=1,$)
#       global glb_eig_fit, glb_eig_L, glb_eig_idx;
#
#   glb_eig_fit:=evalf(eig_fit);
#   glb_eig_L:=eig_L;
#   glb_eig_idx:=eig_idx;
#
#   if show>0 then
#     printf("In ACM_Adapt, the scaling factor for relative eigenvalues "
#            "is chosen such that\nthat for the %d(%d) state is %f\n",
#                                        glb_eig_L,glb_eig_idx,glb_eig_fit);
#   fi:
#
#   [glb_eig_fit, glb_eig_L, glb_eig_idx]:
# end;
def ACM_set_eig_fit(eig_fit: float = glb_eig_fit,
                    eig_L: nonnegint = glb_eig_L,
                    eig_idx: posint = 1,
                    show: int = 1) -> tuple[float, nonnegint, posint]:
    global glb_eig_fit, glb_eig_L, glb_eig_idx

    require_nonnegint('eig_L', eig_L)
    require_posint('eig_idx', eig_idx)

    glb_eig_fit = eig_fit
    glb_eig_L = eig_L
    glb_eig_idx = eig_idx

    if show > 0:
        print('In ACM_Adapt, the scaling factor for relative eigenvalues ' +
              f'is chosen such that\nthat for the {glb_eig_L}({glb_eig_idx}) state is {glb_eig_fit:f}')

    return glb_eig_fit, glb_eig_L, glb_eig_idx


# # Similarly, the following sets the values of
# #      glb_rat_fit, glb_rat_L1, glb_rat_1dx, glb_rat_L2, glb_rat_2dx:
# # which are used by ACM_Adapt to scale the transition rates output.
#
# ACM_set_rat_fit:=proc(rat_fit::constant:=glb_rat_fit,
#                       rat_L1::nonnegint:=glb_rat_L1,
#                       rat_L2::nonnegint:=glb_rat_L2,
#                       rat_1dx::posint:=1,
#                       rat_2dx::posint:=1,
#                       show::integer:=1,$)
#       local tran_fmat,rat_fmat,rat_this:
#       global glb_rat_fit, glb_rat_L1, glb_rat_1dx, glb_rat_L2, glb_rat_2dx,
#              glb_rat_format, glb_rat_desg, glb_tran_format:
#
#     glb_rat_fit:=evalf(rat_fit);
#     glb_rat_L1:=rat_L1;
#     glb_rat_L2:=rat_L2;
#
#     glb_rat_1dx:=rat_1dx;
#     glb_rat_2dx:=rat_2dx;
#
#   if show>0 then
#
#   # Change the %s specifications in glb_tran_fmat to "%d" for integers.
#
#     tran_fmat:=sprintf(glb_tran_format,"%d","%d","%d","%d"):
#     rat_fmat:=sprintf(glb_rat_format,tran_fmat,"%f"):
#     rat_this:=sprintf(rat_fmat,glb_rat_L1,glb_rat_1dx,
#                              glb_rat_L2,glb_rat_2dx,glb_rat_fit):
#
#     printf("In ACM_Adapt, the scaling factor for \"%s\" "
#                               "is chosen such that\n%s\n",
#            glb_rat_desg,rat_this);
#   fi:
#
#   [glb_rat_fit, glb_rat_L1, glb_rat_L2, glb_rat_1dx, glb_rat_2dx]:
# end;
def ACM_set_rat_fit(rat_fit: float = glb_rat_fit,
                    rat_L1: nonnegint = glb_rat_L1,
                    rat_L2: nonnegint = glb_rat_L2,
                    rat_1dx: posint = 1,
                    rat_2dx: posint = 1,
                    show: int = 1) -> tuple[float, nonnegint, nonnegint, posint, posint]:
    global glb_rat_fit, glb_rat_L1, glb_rat_L2, glb_rat_1dx, glb_rat_2dx

    require_nonnegint('rat_L1', rat_L1)
    require_nonnegint('rat_L2', rat_L2)
    require_posint('rat_1dx', rat_1dx)
    require_posint('rat_2dx', rat_2dx)

    glb_rat_fit = rat_fit
    glb_rat_L1 = rat_L1
    glb_rat_L2 = rat_L2
    glb_rat_1dx = rat_1dx
    glb_rat_2dx = rat_2dx

    if show > 0:
        tran_fmat: str = glb_tran_format.format('{:d}', '{:d}', '{:d}', '{:d}')
        rat_fmt: str = glb_rat_format.format(tran_fmat, '{:f}')
        rat_this: str = rat_fmt.format(glb_rat_L1, glb_rat_1dx,
                                       glb_rat_L2, glb_rat_2dx, glb_rat_fit)

        print(f'In ACM_Adapt, the scaling factor for "{glb_rat_desg}" ' +
              f'is chosen such that\n{rat_this}')

    return glb_rat_fit, glb_rat_L1, glb_rat_L2, glb_rat_1dx, glb_rat_2dx


# # The following three functions respectively set, augment or display the
# # list rat_lst, which determines which transition rates are flagged
# # for display. If no argument is given for the first two, an empty list
# # is assumed.
#
# ACM_set_rat_lst:=proc(rat_lst::list(list(integer)):=[],$)
#     global glb_rat_lst;
#
#   glb_rat_lst:=[];
#   ACM_add_rat_lst(rat_lst):
# end;
def ACM_set_rat_lst(rat_lst: Designators = ()) -> int:
    global glb_rat_lst

    glb_rat_lst = ()
    return ACM_add_rat_lst(rat_lst)


# ACM_add_rat_lst:=proc(rat_lst::list(list(integer)):=[],$)
#     local rat_ent;
#     global glb_rat_lst;
#
#   for rat_ent in rat_lst do
#     if nops(rat_ent)>5 then
#       printf("  Bad transition rate specification: %a\n",rat_ent):
#     else
#       glb_rat_lst:=[op(glb_rat_lst),rat_ent]:
#     fi:
#   od:
#
#   return nops(glb_rat_lst);
# end;
def ACM_add_rat_lst(rat_lst: Designators) -> int:
    global glb_rat_lst

    for rat_ent in rat_lst:
        if len(rat_ent) > 5:
            print(f'  Bad transition rate specification: {rat_ent}')
        else:
            glb_rat_lst = glb_rat_lst + (rat_ent,)

    return len(glb_rat_lst)


# ACM_show_rat_lst:=proc(show::integer:=1,$)
#       local rate_ent,rat_format4,rat_format5;
#       global glb_rat_lst,glb_tran_format,glb_rat_desg;
#
#   if show>0 then
#
#     if nops(glb_rat_lst)>0 then
#       rat_format4:=sprintf(glb_tran_format,"%d","%d","%d","%d"):
#
#       printf("Following \"%s\" are set to be displayed:\n", glb_rat_desg):
#       for rate_ent in glb_rat_lst do
#
#         if nops(rate_ent)=4 or (nops(rate_ent)=5 and rate_ent[5]=0) then
#             printf("  "):
#             printf(rat_format4,
#                rate_ent[1], rate_ent[3], rate_ent[2], rate_ent[4]):
#             printf("\n"):
#         elif nops(rate_ent)=5 then
#             printf("  "):
#             rat_format5:=sprintf(glb_tran_format,
#                             "%d%+dk","%d","%d%+dk","%d"):
#             printf(rat_format5, rate_ent[1], rate_ent[5], rate_ent[3],
#                                 rate_ent[2], rate_ent[5], rate_ent[4]):
#             printf("\n"):
#         elif nops(rate_ent)=3 then
#             rat_format5:=sprintf(glb_tran_format, "%d","j_i","%d","%d"):
#             printf("  "):
#             printf(rat_format5, rate_ent[1], rate_ent[2], rate_ent[3]):
#             printf("\n"):
#         elif nops(rate_ent)=2 then
#             printf("  "):
#             rat_format5:=sprintf(glb_tran_format, "%d","j_i","%d","j_f"):
#             printf(rat_format5, rate_ent[1], rate_ent[2]):
#             printf("\n"):
#         elif nops(rate_ent)=1 then
#             printf("  "):
#             rat_format5:=sprintf(glb_tran_format, "L_i","j_i","%d","j_f"):
#             printf(rat_format5, rate_ent[1]):
#         elif nops(rate_ent)=0 then
#             printf("  "):
#             printf(glb_tran_format, "L_i","j_i","L_f","j_f"):
#             printf("\n"):
#         fi
#
#       od
#     else
#       printf("Currently, no \"%s\" are set to be displayed.\n", glb_rat_desg):
#     fi:
#   fi:
#
#   return glb_rat_lst;
# end;
def ACM_show_lst(lst: Designators, desg: str, show: int = 1) -> Designators:
    if show > 0:

        if len(lst) > 0:
            format5: str = glb_tran_format.format('{:d}{:+d}k', '{:d}', '{:d}{:+d}k', '{:d}')
            format4: str = glb_tran_format.format('{:d}', '{:d}', '{:d}', '{:d}')
            format3: str = glb_tran_format.format('{:d}', 'j_i', '{:d}', '{:d}')
            format2: str = glb_tran_format.format('{:d}', 'j_i', '{:d}', 'j_f')
            format1: str = glb_tran_format.format('L_i', 'j_i', '{:d}', 'j_f')
            format0: str = glb_tran_format.format('L_i', 'j_i', 'L_f', 'j_f')

            print(f'Following "{desg}" are set to be displayed:')
            for ent in lst:
                if len(ent) > 5:
                    continue

                print('  ', end='')
                if len(ent) == 5 and ent[4] != 0:
                    print(format5.format(ent[0], ent[4], ent[2], ent[1], ent[4], ent[3]))
                elif len(ent) >= 4:
                    print(format4.format(*ent[:4]))
                elif len(ent) == 3:
                    print(format3.format(*ent[:3]))
                elif len(ent) == 2:
                    print(format2.format(*ent[:2]))
                elif len(ent) == 1:
                    print(format1.format(ent[0]))
                else:
                    assert len(ent) == 0
                    print(format0)

        else:
            print(f'Currently, no "{desg}" are set to be displayed.')

    return lst


def ACM_show_rat_lst(show: int = 1) -> Designators:
    return ACM_show_lst(glb_rat_lst, glb_rat_desg, show)


# # The following three functions respectively set, augment or display the
# # list amp_lst, which determines which transition amplitudes are flagged
# # for display. If no argument is given for the first two, an empty list
# # is assumed.
#
# ACM_set_amp_lst:=proc(amp_lst::list(list(integer)):=[],$)
#     global glb_amp_lst;
#
#   glb_amp_lst:=[];
#   ACM_add_amp_lst(amp_lst):
# end;
def ACM_set_amp_lst(amp_list: Designators = ()) -> int:
    global glb_amp_lst

    glb_amp_lst = ()
    return ACM_add_amp_lst(amp_list)


# ACM_add_amp_lst:=proc(amp_lst::list(list(integer)):=[],$)
#     local amp_ent;
#     global glb_amp_lst;
#
#   for amp_ent in amp_lst do
#     if nops(amp_ent)>5 then
#       printf("  Bad amplitude specification: %a\n",amp_ent):
#     else
#       glb_amp_lst:=[op(glb_amp_lst),amp_ent]:
#     fi:
#   od:
#
#   return nops(glb_amp_lst);
# end;
def ACM_add_amp_lst(amp_lst: Designators = ()) -> int:
    global glb_amp_lst

    for amp_ent in amp_lst:
        if len(amp_ent) > 5:
            print(f'  Bad amplitude specification: {amp_ent}')
        else:
            glb_amp_lst = glb_amp_lst + (amp_ent,)

    return len(glb_amp_lst)


# ACM_show_amp_lst:=proc(show::integer:=1,$)
#       local amp_ent,amp_format4,amp_format5;
#       global glb_amp_lst,glb_tran_format,glb_amp_desg;
#
#   if show>0 then
#
#     if nops(glb_amp_lst)>0 then
#       amp_format4:=sprintf(glb_tran_format,"%d","%d","%d","%d"):
#
#       printf("Following \"%s\" are set to be displayed:\n", glb_amp_desg):
#       for amp_ent in glb_amp_lst do
#
#         if nops(amp_ent)=4 or (nops(amp_ent)=5 and amp_ent[5]=0) then
#             printf("  "):
#             printf(amp_format4,
#                 amp_ent[1], amp_ent[3], amp_ent[2], amp_ent[4]):
#             printf("\n"):
#         elif nops(amp_ent)=5 then
#             printf("  "):
#             amp_format5:=sprintf(glb_tran_format,
#                             "%d%+dk","%d","%d%+dk","%d"):
#             printf(amp_format5, amp_ent[1], amp_ent[5], amp_ent[3],
#                                 amp_ent[2], amp_ent[5], amp_ent[4]):
#             printf("\n"):
#         elif nops(amp_ent)=3 then
#             printf("  "):
#             amp_format5:=sprintf(glb_tran_format,
#                             "%d","j_i","%d","%d"):
#             printf(amp_format5, amp_ent[1], amp_ent[2], amp_ent[3]):
#             printf("\n"):
#         elif nops(amp_ent)=2 then
#             printf("  "):
#             amp_format5:=sprintf(glb_tran_format,
#                             "%d","j_i","%d","j_f"):
#             printf(amp_format5, amp_ent[1], amp_ent[2]):
#             printf("\n"):
#         elif nops(amp_ent)=1 then
#             printf("  "):
#             amp_format5:=sprintf(glb_tran_format,
#                             "L_i","j_i","%d","j_f"):
#             printf(amp_format5, amp_ent[1]):
#         elif nops(amp_ent)=0 then
#             printf("  "):
#             printf(glb_tran_format, "L_i","j_i","L_f","j_f"):
#             printf("\n"):
#         fi
#
#       od
#     else
#       printf("Currently, no \"%s\" are set to be displayed.\n", glb_amp_desg):
#     fi:
#   fi:
#
#   return glb_amp_lst;
# end;
def ACM_show_amp_lst(show: int = 1) -> Designators:
    return ACM_show_lst(glb_amp_lst, glb_amp_desg, show)


# # The following specifies the transition rate operator glb_rat_TRop.
# # It also attempts to determine its angular momentum glb_rat_TRopAM.
#
# ACM_set_transition:=proc(TR_op::list(list):=glb_rat_TRop,
#                          show::integer:=1,$)
#     local rat_AM:
#     global glb_rat_TRop,glb_rat_TRopAM,glb_rat_desg;
#
#   glb_rat_TRop:=TR_op;
#   rat_AM:=Op_AM(TR_op):
#   glb_rat_TRopAM:=abs(rat_AM):   # this is the largest value of AM, if LC.
#
#   if show>0 then
# #      printf("In ACM_Scale and ACM_Adapt, \"%s\" "
#       printf("In ACM_Scale and ACM_Adapt, transition matrix elements "
#                  "now calculated for the operator:\n",glb_rat_desg):
#       print( glb_rat_TRop):
#
#       if rat_AM>=0 then
#         printf("(This has angular momentum %a).\n\n",rat_AM):
#       else
#         printf("(This has indeterminate angular momentum: "
#                                   "maximum %a).\n\n",-rat_AM):
#       fi:
#   fi:
#
#   [glb_rat_TRop,glb_rat_TRopAM]:
# end;
def ACM_set_transition(TR_op: OperatorSum = glb_rat_TRop,
                       show: int = 1) -> tuple[OperatorSum, int]:
    global glb_rat_TRop, glb_rat_TRopAM

    glb_rat_TRop = TR_op
    rat_AM: int = Op_AM(TR_op)
    glb_rat_TRopAM = abs(rat_AM)

    if show > 0:
        print('In ACM_Scale and ACM_Adapt, transition matrix elements ' +
              'now calculated for the operator:\n' + glb_rat_desg, end='')
        print(glb_rat_TRop)

        if rat_AM >= 0:
            print(f'(This has angular momentum {rat_AM}).\n')
        else:
            print(f'(This has indeterminate angular momentum: maximum {-rat_AM}).\n')

    return glb_rat_TRop, glb_rat_TRopAM


# # The following sets glb_rat_fun, glb_rat_format, and glb_rat_desg
# # which determine how "transition rates" are displayed in the
# # procedure Show_Rats (which is called by ACM_Scale and ACM_Adapt).
# # These values are displayed if the final fourth argument is 1 (default).
#
# ACM_set_rat_form:=proc(rat_fun::procedure:=glb_rat_fun,
#                          rat_format::string:=glb_rat_format,
#                          rat_desg::string:=glb_rat_desg,
#                          show::integer:=1,$)
#
#       global glb_rat_fun,glb_rat_format,glb_rat_desg,glb_tran_format;
#       local tran_fmat1;
#
#   glb_rat_fun:=rat_fun:
#   glb_rat_format:=rat_format:
#   glb_rat_desg:=rat_desg:
#
#   if show>0 then
#     printf("ACM_Scale and ACM_Adapt now set to display \"%s\" first.\n",
#                 glb_rat_desg):
#     printf("These are calculated from the (alternative reduced) transition"
#              " matrix elements\nusing the procedure: \"%a\".\n",
#                 glb_rat_fun):
#
#     tran_fmat1:=sprintf(glb_tran_format,"L_i","j_i","L_f","j_f");
#     printf("Each will be output using the format:\n  ");
#     printf(glb_rat_format,tran_fmat1,"*"):
#     printf("\n");
#   fi:
#
#   [glb_rat_fun,glb_rat_format,glb_rat_desg]:
# end;
def ACM_set_rat_form(rat_fun: Callable = glb_rat_fun,
                     rat_format: str = glb_rat_format,
                     rat_desg: str = glb_rat_desg,
                     show: int = 1) -> tuple[Callable, str, str]:
    global glb_rat_fun, glb_rat_format, glb_rat_desg

    glb_rat_fun = rat_fun
    glb_rat_format = rat_format
    glb_rat_desg = rat_desg

    if show > 0:
        print('These are calculated from the (alternative reduced) transition' +
              f' matrix elements\nusing the procedure: "{glb_rat_fun}"')

        tran_fmat1: str = glb_tran_format.format('L_i', 'j_i', 'L_f', 'j_f')
        print('Each will be output using the format:\n  ', end='')
        print(glb_rat_format, tran_fmat1, '*')

    return glb_rat_fun, glb_rat_format, glb_rat_desg


# # The following sets glb_amp_fun, glb_amp_format, and glb_amp_desg
# # which determine how "transition amplitudes" are displayed in the
# # procedure Show_Amps (which is called by ACM_Scale and ACM_Adapt).
# # These values are displayed if the final fourth argument is 1 (default).
#
# ACM_set_amp_form:=proc(amp_fun::procedure:=glb_amp_fun,
#                          amp_format::string:=glb_amp_format,
#                          amp_desg::string:=glb_amp_desg,
#                          show::integer:=1,$)
#
#       global glb_amp_fun,glb_amp_format,glb_amp_desg,glb_tran_format;
#       local tran_fmat1;
#
#   glb_amp_fun:=amp_fun:
#   glb_amp_format:=amp_format:
#   glb_amp_desg:=amp_desg:
#
#   if show>0 then
#     printf("ACM_Scale and ACM_Adapt now set to display \"%s\" second.\n",
#                 glb_amp_desg):
#     printf("These are calculated from the (alternative reduced) transition"
#              " matrix elements\nusing the procedure: \"%a\".\n",
#                 glb_amp_fun):
#
#     tran_fmat1:=sprintf(glb_tran_format,"L_i","j_i","L_f","j_f");
#     printf("Each will be output using the format:\n  ");
#     printf(glb_amp_format,tran_fmat1,"*"):
#     printf("\n");
#   fi:
#
#   [glb_amp_fun,glb_amp_format,glb_amp_desg]:
# end;
def ACM_set_amp_form(amp_fun: Callable = glb_amp_fun,
                     amp_format: str = glb_amp_format,
                     amp_desg: str = glb_amp_desg,
                     show: int = 1) -> tuple[Callable, str, str]:
    global glb_amp_fun, glb_amp_format, glb_amp_desg

    glb_amp_fun = amp_fun
    glb_amp_format = amp_format
    glb_amp_desg = amp_desg

    if show > 0:
        print(f'ACM_Scale and ACM_Adapt now set to display "{glb_amp_desg}" second.')
        print('These are calculated from the (alternative reduced) transition' +
              f' matrix elements\nusing the procedure: "{glb_amp_fun}".')

        tran_fmat1: str = glb_tran_format.format('L_i', 'j_i', 'L_f', 'j_f')
        print('Each will be output using the format:\n  ', end='')
        print(glb_amp_format, tran_fmat1, '*')

    return glb_amp_fun, glb_amp_format, glb_amp_desg


# # The following specifies the "basis type" procedure glb_lam_fun.
# # (see also next procedure).
#
# ACM_set_lambda_fun:=proc(lambda_fun::procedure, show::integer:=1,$)
#     global glb_lam_fun;
#   glb_lam_fun:=lambda_fun:
#
#   if show>0 then
#       printf("lambda values calculated from v using the "
#                   "procedure: \"%a\",\n", glb_lam_fun):
#   fi:
#
#   glb_lam_fun:
# end;
def ACM_set_lambda_fun(lambda_fun: Callable, show: int = 1) -> Callable:
    global glb_lam_fun

    glb_lam_fun = lambda_fun

    if show > 0:
        print('lambda values calculated from v using the ' +
              f'procedure: "{glb_lam_fun}",')

    return glb_lam_fun


# # The following uses the above procedure to set glb_lam_fun to one of
# # four particular basis types, using procedures defined elsewhere.
# # These basis types are those specified in (63), (61), (62), (B17) resp.
# # For choice=0, lambda_v=lambda_0,
# #     choice=1, lambda_v=lambda_0 + v,
# #     choice=2, lambda_v=lambda_0 + (v mod 2),
# #     choice=3, lambda_v=lambda_0 + "integer Davidson variation",
# # the latter obtained using lambda_davi_fun().
# # The second argument is used only if the first is 3.
#
# ACM_set_basis_type:=proc(choice::nonnegint, abeta0::constant:=0.0,
#                                                   show::integer:=1,$)
#   local new_fun:
#   global glb_lam_fun, lambda_fix_fun, lambda_sho_fun,
#                           lambda_acm_fun, lambda_jig_fun:
#   if choice=0 then
#     if show>0 then
#       printf("Using the constant lambda basis.\n"):
#     fi:
#     ACM_set_lambda_fun(lambda_fix_fun,0):
#   elif choice=1 then
#     if show>0 then
#       printf("Using the harmonic oscillator basis with "
#                 "lambda_v = lambda_0 + v.\n"):
#     fi:
#     ACM_set_lambda_fun(lambda_sho_fun,0):
#   elif choice=2 then
#     if show>0 then
#       printf("Using the ACM parity basis.\n"):
#     fi:
#     ACM_set_lambda_fun(lambda_acm_fun,0):
#   elif choice=3 then
#     if show>0 then
#       printf("Using integer Davidson basis for potential with "
#              "minimum at %a (dimensionless).\n",abeta0):
#     fi:
#     new_fun:=lambda_davi_fun(abeta0^4):
#     ACM_set_lambda_fun(new_fun,0):
#   else
#     error "There is no basis %1 defined!", choice:
#   fi:
#
# end;
def ACM_set_basis_type(choice: nonnegint,
                       abeta0: float = 0.0,
                       show: int = 1) -> Callable:
    require_nonnegint('choice', choice)

    if choice == 0:
        if show > 0:
            print('Using the constant lambda basis.')
        ACM_set_lambda_fun(lambda_fix_fun, 0)
    elif choice == 1:
        if show > 0:
            print('Using the harmonic oscillator basis with ' +
                  'lambda_v = lambda_0 + v.')
        ACM_set_lambda_fun(lambda_sho_fun, 0)
    elif choice == 2:
        if show > 0:
            print('Using the ACM parity basis.')
        ACM_set_lambda_fun(lambda_acm_fun, 0)
    elif choice == 3:
        if show > 0:
            print('Using integer Davidson basis for potential with ' +
                  f'minimum at {abeta0} (dimensionless).')
        new_fun: Callable = lambda_davi_fun(abeta0 ** 4)
        ACM_set_lambda_fun(new_fun, 0)
    else:
        raise ValueError(f'There is no basis {choice} defined!')

    return glb_lam_fun


# # For the currently defined basis stored in glb_lam_fun, the following
# # returns lambda_v-lambda_0 for v=vmin...vmax.
#
# ACM_show_lambda_fun:=proc(vmin::nonnegint:=0,vmax::nonnegint:=10)
#   global glb_lam_fun;
#   [seq(glb_lam_fun(v),v=vmin..vmax)]:
# end;
def ACM_show_lambda_fun(vmin: nonnegint = 0, vmax: nonnegint = 10) -> tuple[int, ...]:
    require_nonnegint('vmin', vmin)
    require_nonnegint('vmax', vmax)

    return tuple(glb_lam_fun(v) for v in range(vmin, vmax + 1))


# # Following tests that lambda only shifts by +/-1 as we change v,
# # returning boolean true if so, false if not.
# # (This procedure is not used elsewhere.)
#
# # ACM_test_lambda_fun:=proc(vmin::nonnegint,vmax::nonnegint)
# #   local v,lam,lamv:
# #   global glb_lam_fun:
# #   lam:=glb_lam_fun(vmin):
# #   for v from vmin+1 to vmax do
# #     lamv:=glb_lam_fun(v):
# #     if lamv-lam=1 or lamv-lam=-1 then
# #       lam:=lamv:
# #     else
# #       return false:
# #     fi:
# #   od:
# #
# #   true:
# # end;
def ACM_test_lambda_fun(vmin: nonnegint, vmax: nonnegint) -> bool:
    require_nonnegint('vmin', vmin)
    require_nonnegint('vmax', vmax)

    global glb_lam_fun
    lam: nonnegint = glb_lam_fun(vmin)
    for v in range(vmin + 1, vmax + 1):
        lamv: nonnegint = glb_lam_fun(v)
        if lamv - lam == 1 or lamv - lam == -1:
            lam = lamv
        else:
            return False

    return True


# # The following procedure calls the above procedures to set the
# # default values for all of the global parameters described above.
# # Note that the location of the SO(5)>SO(3) Clebsch-Gordon coefficients
# # must also be specified somewhere by setting the variable SO5CG_directory.
#
# ACM_set_defaults:=proc(show::integer:=1)
#
#   ACM_set_output(2,7,4,show):
#   ACM_set_listln(4,4,show):
#   ACM_set_datum(1,show):
#   ACM_set_basis_type(2,0.0,show):
#
#   ACM_set_transition(quad_op,show):
#   ACM_set_rat_form(quad_rat_fun,def_rat_format,def_rat_desg,show):
#   ACM_set_amp_form(quad_amp_fun,def_amp_format,def_amp_desg,show):
#   ACM_set_sft_fun(sqrt_fun,show):
#   ACM_set_eig_fit(6.0,2,1,show):
#   ACM_set_rat_fit(100.0,2,0,1,1,show):
#   ACM_set_rat_lst( [] ):
#   ACM_set_amp_lst( [] ):
#   ACM_show_rat_lst(show):
#   ACM_show_amp_lst(show):
#   ACM_set_scales(1.0,1.0,show):
#
#   if show>0 then
#     printf("\n"):
#   fi:
#
# end:
def ACM_set_defaults(show: int = 1) -> None:

    ACM_set_output(2, 7, 4, show)
    ACM_set_listln(4, 4, show)
    ACM_set_datum(1, show)
    ACM_set_basis_type(2, 0.0, show)

    ACM_set_transition(quad_op, show)
    ACM_set_rat_form(quad_rat_fun, def_rat_format, def_rat_desg, show)
    ACM_set_amp_form(quad_amp_fun, def_amp_format, def_amp_desg, show)
    ACM_set_sft_fun(sqrt_fun, show)
    ACM_set_eig_fit(6.0, 2, 1, show)
    ACM_set_rat_fit(100.0, 2, 0, 1, 1, show)
    ACM_set_rat_lst(())
    ACM_set_amp_lst(())
    ACM_show_rat_lst(show)
    ACM_show_amp_lst(show)
    ACM_set_scales(1.0, 1.0, show)

    if show > 0:
        print()
