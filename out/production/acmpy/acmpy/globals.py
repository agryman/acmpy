"""1. Specification of global constants, and procedures that can be used to set their values."""

from sympy import Symbol, pi, sqrt, Integer, Rational

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

# the version should be mapped to a Python string, not a float
ACM_version = '1.4'

#
# # The following is a list containing the symbolic names for ten operators
# # that are the "basic" radial operators.
# # The way that they alter lambda is not fixed, but is determined
# # automatically.
#
# Radial_Operators:=[Radial_Sm, Radial_S0, Radial_Sp,
#                    Radial_b2, Radial_bm2, Radial_D2b, Radial_bDb,
#                    Radial_b, Radial_bm, Radial_Db]:

# map all Maple symbols to SymPy symbols
# these are operators, so their multiplication should be assumed to be noncommutative

Radial_Sm = Symbol('Radial_Sm', commutative=False)
Radial_S0 = Symbol('Radial_S0', commutative=False)
Radial_Sp = Symbol('Radial_Sp', commutative=False)
Radial_b2 = Symbol('Radial_b2', commutative=False)
Radial_bm2 = Symbol('Radial_bm2', commutative=False)
Radial_D2b = Symbol('Radial_D2b', commutative=False)
Radial_bDb = Symbol('Radial_bDb', commutative=False)
Radial_b = Symbol('Radial_b', commutative=False)
Radial_bm = Symbol('Radial_bm', commutative=False)
Radial_Db = Symbol('Radial_Db', commutative=False)

# Radial_Operators is a Maple list.
# A Maple list is an ordered sequence of objects.
# It maps naturally to either a Python list (mutable) or tuple (immutable).
# Map Radial_Operators to a Python tuple since I assume it is immutable.
Radial_Operators = (Radial_Sm, Radial_S0, Radial_Sp,
                    Radial_b2, Radial_bm2, Radial_D2b, Radial_bDb,
                    Radial_b, Radial_bm, Radial_Db)

#
# # They will eventually be exchanged for operators in which the shift
# # is specific. The first seven keep their names (for zero shift),
# # but each instance of the final three will be exchanged for a
# # symbolic name that indicates a shift by a shift of -1,0 or +1.
# # The following lists will be used to achieve that.
#
# Radial_pl:=[Radial_b=Radial_b_pl,Radial_bm=Radial_bm_pl,
#             Radial_Db=Radial_Db_pl]:
# Radial_ml:=[Radial_b=Radial_b_ml,Radial_bm=Radial_bm_ml,
#             Radial_Db=Radial_Db_ml]:
# Radial_zl:=[Radial_b=Radial_b_zl,Radial_bm=Radial_bm_zl,
#             Radial_Db=Radial_Db_zl]:

# Radial_pl, Radial_ml, and Radial_zl are Maple tables.
# A Maple table maps naturally to a Python dictionary.

Radial_b_pl = Symbol('Radial_b_pl', commutative=False)
Radial_bm_pl = Symbol('Radial_bm_pl', commutative=False)
Radial_Db_pl = Symbol('Radial_Db_pl', commutative=False)
Radial_pl = {
    Radial_b: Radial_b_pl,
    Radial_bm: Radial_bm_pl,
    Radial_Db: Radial_Db_pl
}

Radial_b_ml = Symbol('Radial_b_ml', commutative=False)
Radial_bm_ml = Symbol('Radial_bm_ml', commutative=False)
Radial_Db_ml = Symbol('Radial_Db_ml', commutative=False)
Radial_ml = {
    Radial_b: Radial_b_ml,
    Radial_bm: Radial_bm_ml,
    Radial_Db: Radial_Db_ml
}

Radial_b_zl = Symbol('Radial_b_zl', commutative=False)
Radial_bm_zl = Symbol('Radial_bm_zl', commutative=False)
Radial_Db_zl = Symbol('Radial_Db_zl', commutative=False)
Radial_zl = {
    Radial_b: Radial_b_zl,
    Radial_bm: Radial_bm_zl,
    Radial_Db: Radial_Db_zl
}

#
#
# # The following indicates the SO(5) spherical harmonics for which
# # SO(5)>SO(3) Clebsch-Gordon coefficients are available,
# # and enables the v,alpha,L quantum numbers to be readily
# # obtained from the symbolic names.
#
# SpHarm_Table:=table([
#   SpHarm_010=[0,1,0],
#   SpHarm_112=[1,1,2],
#   SpHarm_212=[2,1,2], SpHarm_214=[2,1,4],
#   SpHarm_310=[3,1,0], SpHarm_313=[3,1,3], SpHarm_314=[3,1,4],
#   SpHarm_316=[3,1,6],
#   SpHarm_412=[4,1,2], SpHarm_414=[4,1,4], SpHarm_415=[4,1,5],
#   SpHarm_416=[4,1,6], SpHarm_418=[4,1,8],
#   SpHarm_512=[5,1,2], SpHarm_514=[5,1,4], SpHarm_515=[5,1,5],
#   SpHarm_516=[5,1,6], SpHarm_517=[5,1,7], SpHarm_518=[5,1,8],
#   SpHarm_51A=[5,1,10],
#   SpHarm_610=[6,1,0], SpHarm_613=[6,1,3], SpHarm_614=[6,1,4],
#   SpHarm_616=[6,1,6], SpHarm_626=[6,2,6], SpHarm_617=[6,1,7],
#   SpHarm_618=[6,1,8], SpHarm_619=[6,1,9], SpHarm_61A=[6,1,10],
#   SpHarm_61C=[6,1,12]
# ]):

# Map SpHarm_Table to a Python dictionary whose keys are symbols
# and whose values are (v, alpha, L) integer tuples

SpHarm_010 = Symbol('SpHarm_010', commutative=False)
SpHarm_112 = Symbol('SpHarm_112', commutative=False)
SpHarm_212 = Symbol('SpHarm_212', commutative=False)
SpHarm_214 = Symbol('SpHarm_214', commutative=False)
SpHarm_310 = Symbol('SpHarm_310', commutative=False)
SpHarm_313 = Symbol('SpHarm_313', commutative=False)
SpHarm_314 = Symbol('SpHarm_314', commutative=False)
SpHarm_316 = Symbol('SpHarm_316', commutative=False)
SpHarm_412 = Symbol('SpHarm_412', commutative=False)
SpHarm_414 = Symbol('SpHarm_414', commutative=False)
SpHarm_415 = Symbol('SpHarm_415', commutative=False)
SpHarm_416 = Symbol('SpHarm_416', commutative=False)
SpHarm_418 = Symbol('SpHarm_418', commutative=False)
SpHarm_512 = Symbol('SpHarm_512', commutative=False)
SpHarm_514 = Symbol('SpHarm_514', commutative=False)
SpHarm_515 = Symbol('SpHarm_515', commutative=False)
SpHarm_516 = Symbol('SpHarm_516', commutative=False)
SpHarm_517 = Symbol('SpHarm_517', commutative=False)
SpHarm_518 = Symbol('SpHarm_518', commutative=False)
SpHarm_51A = Symbol('SpHarm_51A', commutative=False)
SpHarm_610 = Symbol('SpHarm_610', commutative=False)
SpHarm_613 = Symbol('SpHarm_613', commutative=False)
SpHarm_614 = Symbol('SpHarm_614', commutative=False)
SpHarm_616 = Symbol('SpHarm_616', commutative=False)
SpHarm_626 = Symbol('SpHarm_626', commutative=False)
SpHarm_617 = Symbol('SpHarm_617', commutative=False)
SpHarm_618 = Symbol('SpHarm_618', commutative=False)
SpHarm_619 = Symbol('SpHarm_619', commutative=False)
SpHarm_61A = Symbol('SpHarm_61A', commutative=False)
SpHarm_61C = Symbol('SpHarm_61C', commutative=False)

SpHarm_Table = {
    SpHarm_010: (0,1,0),
    SpHarm_112: (1,1,2),
    SpHarm_212: (2,1,2),
    SpHarm_214: (2,1,4),
    SpHarm_310: (3,1,0),
    SpHarm_313: (3,1,3),
    SpHarm_314: (3,1,4),
    SpHarm_316: (3,1,6),
    SpHarm_412: (4,1,2),
    SpHarm_414: (4,1,4),
    SpHarm_415: (4,1,5),
    SpHarm_416: (4,1,6),
    SpHarm_418: (4,1,8),
    SpHarm_512: (5,1,2),
    SpHarm_514: (5,1,4),
    SpHarm_515: (5,1,5),
    SpHarm_516: (5,1,6),
    SpHarm_517: (5,1,7),
    SpHarm_518: (5,1,8),
    SpHarm_51A: (5,1,10),
    SpHarm_610: (6,1,0),
    SpHarm_613: (6,1,3),
    SpHarm_614: (6,1,4),
    SpHarm_616: (6,1,6),
    SpHarm_626: (6,2,6),
    SpHarm_617: (6,1,7),
    SpHarm_618: (6,1,8),
    SpHarm_619: (6,1,9),
    SpHarm_61A: (6,1,10),
    SpHarm_61C: (6,1,12)
}

#
# # Form a list of the available operator symbols in this table.
#
# SpHarm_Operators:=map(op,[indices(SpHarm_Table)]):

# The indices of a Maple table is a sequence of lists of keys.
# The key value is the operand of the list constructor so the op function must be applied to it.
# In Python we can simply turn the dictionary keys into a list of keys.
SpHarm_Operators = list(SpHarm_Table.keys())

#
# # We also make use of SpDiag_sqLdim and SpDiag_sqLdiv which
# # denote operators represented by diagonal matrices with entries
# #     (-1)^{L_i}*sqrt(2L_i+1)
# # and (-1)^{L_i}/sqrt(2L_i+1) respectively.
#
# Spherical_Operators:=[op(SpHarm_Operators),SpDiag_sqLdim,SpDiag_sqLdiv]:

# Map SpDiag_sqLdim and SpDiag_sqLdiv to noncommutative symbols.
SpDiag_sqLdim = Symbol('SpDiag_sqLdim', commutative=False)
SpDiag_sqLdiv = Symbol('SpDiag_sqLdiv', commutative=False)
Spherical_Operators = SpHarm_Operators + [SpDiag_sqLdim, SpDiag_sqLdiv]

#
# # The four operators
# #       pi, [pi x pi]_{v=2,L=2}, [pi x pi]_{v=2,L=L}, [q x pi x pi]_{v=3,L=0}
# # intrinsically affect the whole product space:
#
# Xspace_Operators:=[ Xspace_Pi, Xspace_PiPi2, Xspace_PiPi4, Xspace_PiqPi ]:

Xspace_Pi = Symbol('Xspace_Pi', commutative=False)
Xspace_PiPi2 = Symbol('Xspace_PiPi2', commutative=False)
Xspace_PiPi4 = Symbol('Xspace_PiPi4', commutative=False)
Xspace_PiqPi = Symbol('Xspace_PiqPi', commutative=False)
Xspace_Operators = [Xspace_Pi, Xspace_PiPi2, Xspace_PiPi4, Xspace_PiqPi]

#
#
# # The following quad_op specifies, in internal format, the quadrupole
# # operator. quadRigid_op is more appropriate for rigid-beta models.
#
# quad_op:=[ [Convert_112, [Radial_b,SpHarm_112]] ]:
# quadRigid_op:=[ [Convert_112, [SpHarm_112]] ]:

Convert_112 = Symbol('Convert_112', commutative=False)
quad_op = [[Convert_112, [Radial_b,SpHarm_112]]]
quadRigid_op =[[Convert_112, [SpHarm_112]]]

#
#
#
# # The following provide useful conversion factors from the SO(5)
# # spherical harmonics to more physically relevant operators;
# # see Table IV.
# # (Note that often (e.g. by RepSO5_Y_rem), the operator will be represented
# # with the 4*Pi already incorporated - and the FourPi should be cancelled).
# # Note that evalf will need to be used somewhere further down the line
# # to convert from these symbolic values to actual floating point values.
#
# FourPi:=4*Pi;
# Convert_112:=FourPi/sqrt(15);       # multiplies Y112 to get Q
# Convert_212:=-FourPi*sqrt(2/105);   # multiplies Y212 to get [QxQ]_(L=4)
# Convert_310:=FourPi/3;              # multiplies Y310 to get cos(3*gamma)
# Convert_316:=FourPi/3*sqrt(2/35);   # multiplies Y316 to get [QxQxQ]_(L=6)
# Convert_610:=2*FourPi/sqrt(15);     # multiplies Y610 to get [3*cos(3*gamma)+1]
# Convert_red:=1/FourPi;         # converts ME_SO5red to <v3|||v2|||v1>

# Maple Pi maps to SymPy pi
FourPi = 4 * pi

# I am not sure about the semantic difference between Maple and SymPy with respect to
# changing the value of a symbol after it has been used.
# In this case, Convert_112 was defined above to be a Symbol but is
# now being redefined to be a numeric expression.
# I believe Maple and SymPy are similar in that the new value of the Symbol is
# not immediately substituted in any expression that references it.
# Not that any Python numeric expression must be wrapped in SymPy constructors
# such as Integer and Rational is order to preserve exact precision.
Convert_112 = FourPi / sqrt(Integer(15))
Convert_212 = -FourPi * sqrt(Rational(2, 105))
Convert_310 = FourPi / 3
Convert_316 = FourPi / 3 * sqrt(Rational(2, 35))
Convert_610 = 2 * FourPi / sqrt(Integer(15))
Convert_red = 1 / FourPi

#
# ###########################################################################
#
#
# # The following procedure definitions determine functions used for displaying
# # the transition rates and amplitudes (the particular procedures in force at
# # a given time are stored in the global variables glb_rat_fun & glb_amp_fun).
# # These are as listed in Table V.
# # In addition to the matrix element Mel, they make use of the angular
# # momenta of the intitial state Li, and final state Lf.
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
#
# mel_amp_fun:=proc(Li,Lf,Mel)
#   Mel*sqrt(2*Lf+1)
# end;
#
# unit_amp_fun:=proc(Li,Lf,Mel)
#   Mel
# end;
#
# quad_rat_fun:=proc(Li,Lf,Mel)
#   Mel^2*dimSO3(Lf)/dimSO3(Li)
# end;
#
# mel_rat_fun:=proc(Li,Lf,Mel)
#   Mel^2*dimSO3(Lf)
# end;
#
# unit_rat_fun:=proc(Li,Lf,Mel)
#   Mel^2
# end;
#
# # The following was described in a previous version
#
# mix_amp_fun:=proc(Li,Lf,Mel)
#   global glb_rat_TRopAM;
#   Mel*gen_amp_mul(Li,Lf,glb_rat_TRopAM)
# end;
#
# gen_amp_mul:=proc(Li,Lf,Lt,$)
#   if Li=Lf then CG_SO3(Lf,Lf,Lt,0,Lf,Lf)
#   else sqrt(2*Lf+1)
#   fi:
# end;
#
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
#
# lambda_sho_fun:=proc(v::nonnegint)   # for SHO lambda variation
#   v
# end;
#
# lambda_acm_fun:=proc(v::nonnegint)   # for lambda varying with parity of v
#   irem(v,2)
# end;
#
# lambda_jig_fun:=proc(v::nonnegint)   # A little mixture, used for testing
#   if v=0 then
#     0
#   else
#     2-irem(v,2)
#   fi
# end;
#
# # Further procedures of a similar nature may be obtained using the
# # following procedure, which returns the name of a procedure that
# # itself returns the nearest integer to
# #    sqrt( (v+3/2)^2 + C ) - sqrt( 9/4 + C )
# # of the same partity as v.
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
#
#
# # We supply our own version of the square root that has `procedure` type.
# # It is necessary to use such a procedure to pass as an argument
# # when the type is being tested, because sqrt itself is not a `procedure`!
# # glb_amp_sft_fun:=sqrt:
#
# sqrt_fun:=proc(sft)
#   sqrt(evalf(sft)):
# end;
#
#
# ###########################################################################
#
# # The SO(5)>SO(3) CG coefficients are initially obtained from external files.
# # The value of the Maple variable SO5CG_directory determines the directory
# # below which are to be found files containing SO(5)>SO(3) CG coefficients.
# # It may be specified at the start of a worksheet.
# # Or, if a acm-user.mpl file is used, it may be specified there.
# # A sample definition is (the final "/" is necessary):
# #     SO5CG_directory:="/home/username/maple/acm/so5cg-data/":  # sample
#
# # The procedure call
# #     show_CG_file(2,3,1,0,5):   # test
# # would test the directory specified in SO5CG_directory
# # (it is used by the procedure show_CG_file), and, somewhat, the data
# # therein (it should return two values: 0.522,0.431).
#
# # The following defines a table wherein the SO(5)>SO(3) Clebsch-Gordon
# # coefficients will be stored in memory. This table is intially empty.
# # The table is loaded from external files, as required.
# # For a particular (v1,v2,a2,L2,v3), this is done by calling
# # load_CG_table(v1,v2,a2,L2,v3).
# # When present, the SO(5)>SO(3) CG coefficient is given by
# # CG_coeffs[v1,v2,a2,L2,v3][a1,L1,a3,L3].
#
# CG_coeffs:=table():
#
# # To examine which (v1,v2,a2,L2,v3) have been loaded, we can use:
# #   indices(CG_coeffs);
# # Initially, of course, this table will be empty.
#
# ###########################################################################
#
# # The following determine values used to set the defaults for how the
# # transition rates and amplitudes of the quadrupole operator are
# # displayed by the procedures Show_Rats and Show_Amps.
#
# def_rat_desg:="transition rates":
# def_rat_format:="  B(E2: %s) = %s":
# def_amp_desg:="transition amplitudes":
# def_amp_format:="  Amp( %s ) = %s":
#
# # If the Show_Mels procedure is used directly (Show_Rats and
# # Show_Amps call Show_Mels), the following two values can be used
# # (in fact, they are used by default).
# # These can also be used for the rates and amplitudes of other operators,
# # if the user hasn't defined anything else.
#
# def_mel_desg:="matrix elements":
# def_mel_format:="  ME( %s ) = %s":
#
# ###########################################################################
#
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
#
# # The following store the precision for floating point values that
# # are displayed by the procedures Show_Eigs(), Show_Rats() and
# # Show_Amps(); and via these, by the procedures ACM_Scale()
# # and ACM_Adapt():
#
# glb_rel_pre:=2:
# glb_rel_wid:=7:
# glb_low_pre:=4:
#
# # The following store the maximal number of entries for horizontal
# # lists of eigenvalues, transition rates and amplitudes that are
# # respectively displayed by the procedures Show_Eigs(), Show_Rats()
# # and Show_Amps(); and via these, by the procedures ACM_Scale()
# # and ACM_Adapt():
#
# glb_eig_num:=4:
# glb_rat_num:=4:
# glb_amp_num:=4:
#
# # The following specify how ACM_Adapt() determines the scale factor
# # glb_eig_sft. This factor is determined such that the energy of
# # the (glb_eig_idx)th state of AM glb_eig_L comes out to be glb_eig_fit.
#
# glb_eig_fit:=6.0:
# glb_eig_L:=2:
# glb_eig_idx:=1:
#
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
#
# # The following specifies a procedure which determines the basis type.
# # This is a function which gives the value of lambda_v-lambda_0.
#
# glb_lam_fun:=lambda_acm_fun:
#
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
#
# # The following determine how "transition rates" are displayed in the
# # procedure Show_Rats (which is called by ACM_Scale and ACM_Adapt).
# # The first specifies the formula used, the second the format used to
# # display each value, the third the phrase used to designate the values.
# # (e.g. "transition rates")
#
# glb_rat_fun:=quad_rat_fun:
# glb_rat_format:=def_rat_format:
# glb_rat_desg:=def_rat_desg:
#
# # The following determine how "transition rates" are displayed in the
# # procedure Show_Amps (which is called by ACM_Scale and ACM_Adapt).
# # The first specifies the formula used, the second the format used to
# # display each value, the third the phrase used to designate the values.
# # (e.g. "transition amplitudes")
#
# glb_amp_fun:=quad_amp_fun:
# glb_amp_format:=def_amp_format:
# glb_amp_desg:=def_amp_desg:
#
# # The following specifies the function by which the scaling factor
# # for transition amplitudes (glb_amp_sft) is obtained from that
# # (glb_rat_sft) for transition rates:
#
# glb_amp_sft_fun:=sqrt:
#
# # The following determines how the matrix element labels are displayed:
#
# glb_tran_format:="%s(%s) -> %s(%s)":
# glb_tran_fill:="#":
#
# # The following store the lists of transition rate and transition amplitude
# # designators (each initially empty):
#
# glb_rat_lst:=[]:
# glb_amp_lst:=[]:
#
# # The following flag indicates whether, in ACM_Scale, ACM_Adapt
# # and Show_Eigs, eigenvalues are displayed relative to their
# # lowest value (true), or absolute (false).
#
# glb_eig_rel:=true:
#
#
# # The following parameter, if positive, specifies a temporary
# # increase to the size of the radial space, to improve accuracy
# # of radial reps.
# # It is used only by the procedure RepXspace_Twin (which is called
# # by RepXspace).
#
# glb_nu_lap:=0:
#
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
#
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
#
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
#
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
#
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
#
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
#
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
#
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
#
#
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
#
# #
#
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
#
# #
#
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
#
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
#
# #
#
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
#
# #
#
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
#
#
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
#   glb_rat_TRopAM:=abs(rat_AM):   # this is largest value of AM, if LC.
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
#
#
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
#
#
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
#
#
# # The following specfies the "basis type" procedure glb_lam_fun.
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
#
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
#
#
# # For the currently defined basis stored in glb_lam_fun, the following
# # returns lambda_v-lambda_0 for v=vmin...vmax.
#
# ACM_show_lambda_fun:=proc(vmin::nonnegint:=0,vmax::nonnegint:=10)
#   global glb_lam_fun;
#   [seq(glb_lam_fun(v),v=vmin..vmax)]:
# end;
#
#
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
#
#
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
#
#
#
