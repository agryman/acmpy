"""3. Procedures that access the SO(5)>SO(3) Clebsch-Gordon coefficients."""

from typing import ClassVar, Optional

from os.path import expanduser

from sympy import S, Expr, Rational, simplify, sqrt, factorial

from acmpy.compat import nonnegint, posint, require_nonnegint, require_posint, \
    is_odd, readdata_float
from acmpy.spherical_space import dimSO5r3, dimSO5, dimSO3


# ###########################################################################
# #### SO(5) Clebsch-Gordon coefficients and reps of spherical harmonics ####
# ###########################################################################
#
# # The files that contain the SO(5)>SO(3) CG coefficients
# # (v1,a1,L1,v2,a2,L2||v3,a3,L3) are assumed to lie below
# # the directory given in the global variable SO5CG_directory
# # (which must be set somewhere by the user).
# # The names of these files are of the form SO5CG_v1_v2-a2-L2_v3.
# # They are assumed to lie in directories named SO5CG_v1_v2_v3 which
# # themselves lie in directories named "v2=1/", "v2=2/", "v2=3/", etc.,
# # each a subdirectory of the directory specified in SO5CG_directory.
# # There are no v2=0 files because the data is easily generated
# # (and is done so in the procedure load_CG_table below).

SO5Quintet = tuple[nonnegint, nonnegint, posint, nonnegint, nonnegint]
"""An SO5 quintet is a tuple (v1, v2, a2, L2, v3) of irrep label components."""


def require_SO5Quintet(v1: nonnegint,
                       v2: nonnegint, a2: posint, L2: nonnegint,
                       v3: nonnegint) -> None:
    require_nonnegint('v1', v1)
    require_SO5Triple(v2, a2, L2)
    require_nonnegint('v3', v3)


def require_SO5Triple(v: nonnegint, a: posint, L: nonnegint) -> None:
    require_nonnegint('v', v)
    require_posint('a', a)
    require_nonnegint('L', L)


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
# # To examine which (v1,v2,a2,L2,v3) have been loaded, we can use:
# #   indices(CG_coeffs);
# # Initially, of course, this table will be empty.

class SO5CGConfig:
    """This class manages the configuration for the external SO5CG database."""

    base_directory: ClassVar[Optional[str]] = None
    """The base directory of the SO5CG database."""

    default_base_directory: ClassVar[str] = '~/so5cg-data/'
    """The default base directory to use when none is currently configured."""

    @staticmethod
    def set_base_directory(directory: str) -> None:
        """Set the base directory."""
        SO5CGConfig.base_directory = directory

    @staticmethod
    def get_base_directory() -> str:
        """Return the current base directory if not None, else the default."""
        return SO5CGConfig.base_directory \
            if SO5CGConfig.base_directory is not None \
            else expanduser(SO5CGConfig.default_base_directory)


# # The following procedure SO5CG_filename returns the full pathname of the
# # file that contains the SO(5)>SO(3) CG coefficients
# # (v1,a1,L1,v2,a2,L2||v3,a3,L3) for particular values of v1, v2, a2, L2, v3.
#
# SO5CG_filename:=proc(v1::nonnegint,
#                      v2::nonnegint,a2::posint,L2::nonnegint,
#                      v3::nonnegint)
#     cat(SO5CG_directory,"v2=",v2,"/SO5CG_",v1,"_",v2,"_",v3,
#     "/SO5CG_",v1,"_",v2,"-",a2,"-",L2,"_",v3);
# end:
def SO5CG_filename(v1: nonnegint,
                   v2: nonnegint, a2: posint, L2: nonnegint,
                   v3: nonnegint) -> str:
    require_SO5Quintet(v1, v2, a2, L2, v3)

    SO5CG_directory: str = SO5CGConfig.get_base_directory()
    return f'{SO5CG_directory}v2={v2}/SO5CG_{v1}_{v2}_{v3}/SO5CG_{v1}_{v2}-{a2}-{L2}_{v3}'


# # The following procedure CG_labels returns, for the given v1,L2,v3,
# # a list of all quartets [a1,L1,a3,L3], where [v1,a1,L1] and [v3,a3,L3] are
# # valid SO(5)>SO(3) state labels, and for which |L1-L2| <= L3 <= L1+L2.
# # In this list L1 varies slowest, then a1 next slowest, then L3,
# # with a3 quickest.
# # The ordering (and length) of the list then accords with the order of the
# # SO(5)>SO(3) CG coefficients in the data files SO5CG_v1_v2-a2-L2_v3 .
# # The output of this routine is then used to correctly label the data
# # from the data file.
# # (Note that the data files contain all nine labels v1,a1,L1,v2,a2,L2,
# #  v3,a3,L3 alongside the CG coefficient, but these nine labels are
# #  not read - they are assumed to accord with the labels given by
# #  CG_labels (we could thus make the data files smaller).)
#
# # (Note that the list returned here is generally smaller than the
# #  direct product of the sets obtained from calling
# #  lbsSO5r3_allL(v1) and lbsSO5r3_allL(v3).)
#
# CG_labels:=proc(v1::nonnegint,
#                 L2::nonnegint,
#                 v3::nonnegint)
#   local L1,L3,a1,a3,label_list;
#   label_list:=[]:
#
#   for L1 from 0 to 2*v1 do
#   for a1 to dimSO5r3(v1,L1) do
#     for L3 from abs(L1-L2) to min(L1+L2,2*v3) do
#     for a3 to dimSO5r3(v3,L3) do
#         label_list:=[op(label_list),[a1,L1,a3,L3]]:
#     od: od:
#   od: od:
#
#   label_list:
# end:
SO5Quartet = tuple[posint, nonnegint, posint, nonnegint]
"""An SO5 quartet is a tuple (a1, L1, a3, L3) of irrep label components."""
CGLabelList = list[SO5Quartet]


def CG_labels(v1: nonnegint, L2: nonnegint, v3: nonnegint) -> CGLabelList:
    require_nonnegint('v1', v1)
    require_nonnegint('L2', L2)
    require_nonnegint('v3', v3)

    label_list: CGLabelList = []
    for L1 in range(2 * v1 + 1):
        for a1 in range(1, dimSO5r3(v1, L1) + 1):
            for L3 in range(abs(L1 - L2), min(L1 + L2, 2 * v3) + 1):
                for a3 in range(1, dimSO5r3(v3, L3) + 1):
                    label_list.append((a1, L1, a3, L3))

    return label_list


# # The following procedure get_CG_file reads the
# # SO(5)>SO(3) CG coefficients from the data file SO5CG_v1_v2-a2-L2_v3 .
# # It returns a list of two values, the first of which is a list
# # of floats giving the coefficients, and the second of which is
# # the list of corresponding labels [a1,L1,a3,L3], the latter obtained
# # using the procedure CG_labels above.
# # It is only used by the subsequent procedure.
#
# get_CG_file:=proc(v1::nonnegint,
#                   v2::nonnegint,a2::posint,L2::nonnegint,
#                   v3::nonnegint)
#   local CG_data,CG_list:
#
#   if v1>v2+v3 or v2>v3+v1 or v3>v1+v2 or type(v1+v2+v3,odd)
#       or v3<v1        # data is obtained from v3>v1 cases
#       or a2>dimSO5r3(v2,L2) then
#     error "No CG file for these parameters!":
#   fi:
#
#   CG_data:=readdata( SO5CG_filename(v1,v2,a2,L2,v3), float):
#   CG_list:=CG_labels(v1,L2,v3):
#   [CG_data,CG_list]:
# end:
def get_CG_file(v1: nonnegint,
                v2: nonnegint, a2: posint, L2: nonnegint,
                v3: nonnegint) -> tuple[list[float], CGLabelList]:
    require_SO5Quintet(v1, v2, a2, L2, v3)

    CG_data: list[float]
    CG_list: CGLabelList

    if v1 > v2 + v3 or v2 > v3 + v1 or v3 > v1 + v2 \
            or is_odd(v1 + v2 + v3) \
            or v3 < v1 \
            or a2 > dimSO5r3(v2, L2):
        raise ValueError('No CG file for these parameters!')

    filename: str = SO5CG_filename(v1, v2, a2, L2, v3)
    CG_data = readdata_float(filename)
    CG_list = CG_labels(v1, L2, v3)

    return CG_data, CG_list


# # The following procedure show_CG_file displays the
# # SO(5)>SO(3) CG coefficients from the data file SO5CG_v1_v2-a2-L2_v3 .
# # For each label [a1,v1,a3,L3], it prints the label followed by the
# # value of the corresponding CG coefficient.
# # The procedure is useful for testing that the CG coefficients are being
# # accessed correctly. It is not used subsequently.
#
# show_CG_file:=proc(v1::nonnegint,
#                    v2::nonnegint,a2::posint,L2::nonnegint,
#                    v3::nonnegint)
#   local cg_table,count,i:
#
#   cg_table:=get_CG_file(v1,v2,a2,L2,v3):
#   count:=nops(cg_table[1]):
#   if count=1 then
#     print(`This file contains ` || count || ` CG coefficient`):
#   else
#     print(`This file contains ` || count || ` CG coefficients`):
#   fi:
#
#   for i to count do
#     print(cg_table[2][i],cg_table[1][i]):
#   od:
# end:
def show_CG_file(v1: nonnegint,
                 v2: nonnegint, a2: posint, L2: nonnegint,
                 v3: nonnegint) -> None:
    require_SO5Quintet(v1, v2, a2, L2, v3)
    cg_table: tuple[list[float], CGLabelList] = get_CG_file(v1, v2, a2, L2, v3)
    count: int = len(cg_table[0])
    if count == 1:
        print(f'This file contains {count} CG coefficient')
    else:
        print(f'This file contains {count} CG coefficients')

    for coeff, label in zip(cg_table[0], cg_table[1]):
        print(label, coeff, sep=', ')


# # The following defines a table wherein the SO(5)>SO(3) Clebsch-Gordon
# # coefficients will be stored in memory. This table is initially empty.
# # The table is loaded from external files, as required.
# # For a particular (v1,v2,a2,L2,v3), this is done by calling
# # load_CG_table(v1,v2,a2,L2,v3).
# # When present, the SO(5)>SO(3) CG coefficient is given by
# # CG_coeffs[v1,v2,a2,L2,v3][a1,L1,a3,L3].
#
# CG_coeffs:=table():
CG_coeffs: dict[SO5Quintet, dict[SO5Quartet, float]] = {}


# # The following procedure load_CG_table loads all the
# # SO(5)>SO(3) CG coefficients for a particular (v1,v2,a2,L2,v3)
# # from the data file SO5CG_v1_v2-a2-L2_v3 .
# # They are loaded into the table CG_coeffs (which was initialised above),
# # from where they can be readily accessed.
# # Subsequent attempts to load the same data will be silently ignored.
# # Note that no checking is done here on the correct ranges of the
# # arguments (this is left to the functions that call this).
# # We should restrict to
# #   v1<=v2+v3 and v2<=v3+v1 and v3<=v1+v2 and type(v1+v2+v3,odd)
# #      and a2<=dimSO5r3(v2,L2).
# # We should also restrict to v values at most the maximal seniority
# # of that of the data files (currently 6), else a "file does not exist"
# # error will be generated.
#
# # Note that if v1>v3, then the data for (v3,v2,a2,L2,v1) is loaded instead
# # because the SO(5)>SO(3) CG coefficients for (v1,v2,a2,L2,v3) are easily
# # obtained from the former using (4.164) of [RowanWood].
# # Also note that for v2=0, no data is read, but each coefficient
# # is set correctly to 1.0.
#
# load_CG_table:=proc(v1::nonnegint,
#                     v2::nonnegint,a2::posint,L2::nonnegint,
#                     v3::nonnegint)
#   local CG_data,CG_list,vt1,vt3;
#   global CG_coeffs;
#
#   if v1>v3 then
#     vt1:=v3: vt3:=v1:
#   else
#     vt1:=v1: vt3:=v3:
#   fi:
#   if evalb([vt1,v2,a2,L2,vt3] in [indices(CG_coeffs)] ) then
#     return:
#   fi:
#
#   CG_list:=CG_labels(vt1,L2,vt3):
#   if v2>0 then  # read data from file
#     CG_data:=readdata( SO5CG_filename(vt1,v2,a2,L2,vt3), float):
#   else  # generate data
#     CG_data:=[1.0$nops(CG_list)]:
#   fi:
#
#   CG_coeffs[vt1,v2,a2,L2,vt3]:=table([seq( (op(CG_list[i]))=CG_data[i],
#                                  i=1..nops(CG_list) )]);
# end:
def load_CG_table(v1: nonnegint,
                  v2: nonnegint, a2: posint, L2: nonnegint,
                  v3: nonnegint) -> None:
    require_SO5Quintet(v1, v2, a2, L2, v3)

    if v1 > v3:
        v1, v3 = v3, v1

    key: SO5Quintet = (v1, v2, a2, L2, v3)
    if key in CG_coeffs:
        return

    CG_list: CGLabelList = CG_labels(v1, L2, v3)
    CG_data: list[float] = readdata_float(SO5CG_filename(*key)) if v2 > 0 else [1.0] * len(CG_list)

    CG_coeffs[key] = {label: data for label, data in zip(CG_list, CG_data)}


# # The following procedure CG_SO5r3 returns the SO(5)>SO(3) CG coefficient
# # (v1,a1,L1;v2,a2,L2||v3,a3,L3)  [no renormalisation required].
# # The return value is a float.
# # If not already present in CG_coeffs, the data file for
# # (v1,v2,a2,L2,v3) is loaded.
# # Note that if v1>v3, then the data for (v3,v2,a2,L2,v1) is used instead,
# # and a factor is included (see (4.164) of [RowanWood]).
# # (A faster version that does no testing of indices could be written).
#
# CG_SO5r3:=proc(v1::nonnegint,a1::posint,L1::nonnegint,
#                v2::nonnegint,a2::posint,L2::nonnegint,
#                v3::nonnegint,a3::posint,L3::nonnegint)
#   global CG_coeffs;
#   if v1+v2<v3 or v1+v3<v2 or v2+v3<v1 or
#      L1+L2<L3 or L1+L3<L2 or L2+L3<L1 or
#      a1>dimSO5r3(v1,L1) or a2>dimSO5r3(v2,L2)
#                         or a3>dimSO5r3(v3,L3) or type(v1+v2+v3,odd) then
#         0;
#   else
#      load_CG_table(v1,v2,a2,L2,v3);
#      if v1<=v3 then
#        CG_coeffs[v1,v2,a2,L2,v3][a1,L1,a3,L3]:
#      else
#        CG_coeffs[v3,v2,a2,L2,v1][a3,L3,a1,L1]
#          * (-1)^(L3+L2-L1)
#          * sqrt( dimSO5(v3) * dimSO3(L1) / dimSO5(v1) / dimSO3(L3) ):
#      fi:
#   fi:
# end:
def CG_SO5r3(v1: nonnegint, a1: posint, L1: nonnegint,
             v2: nonnegint, a2: posint, L2: nonnegint,
             v3: nonnegint, a3: posint, L3: nonnegint) -> float:
    require_SO5Triple(v1, a1, L1)
    require_SO5Triple(v2, a2, L2)
    require_SO5Triple(v3, a3, L3)

    if v1 + v2 < v3 or v1 + v3 < v2 or v2 + v3 < v1 or \
            L1 + L2 < L3 or L1 + L3 < L2 or L2 + L3 < L1 or \
            a1 > dimSO5r3(v1, L1) or a2 > dimSO5r3(v2, L2) or a3 > dimSO5r3(v3, L3) or \
            is_odd(v1 + v2 + v3):
        return 0.0
    else:
        load_CG_table(v1, v2, a2, L2, v3)
        if v1 <= v3:
            return CG_coeffs[(v1, v2, a2, L2, v3)][(a1, L1, a3, L3)]
        else:
            return CG_coeffs[(v3, v2, a2, L2, v1)][(a3, L3, a1, L1)] \
                   * (-1) ** (L3 + L2 - L1) \
                   * sqrt(dimSO5(v3) * dimSO3(L1) / dimSO5(v1) / dimSO3(L3))


# ###########################################################################
#
# # The following procedure CG_SO3 returns the usual SO(3) Clebsch-Gordon
# # coefficients CG(j1,m1,j2,m2;j3,m3). Here the arguments are each
# # 1/2 integers (rationals). The return value is expressed as a surd.
# # The formula used is that of eqn. (3.6.10) of Edmond's book.
#
# # In the ACM code, this procedure is only used, in some instances,
# # to calculate transition amplitudes from transition rates.
# # It's not used elsewhere.
#
# # We could use it, for example, via (36) to get full matrix
# # elements of spherical harmonics Y^v_{aLM}, by
# #   CG_SO3(L_i,M_i,0,0,L_f,M_f)*ME_SO5r3(v_f,al_f,L_f,v,a,L,,v_i,al_i,L_i):
#
# CG_SO3:=proc(j1::rational,m1::rational,j2::rational,m2::rational,
#                                        j3::rational,m3::rational)
#
#   if abs(m1)>j1 or abs(m2)>j2 or abs(m3)>j3 then RETURN (0) fi;
#   if not(type(j1+m1,integer) and type(j2+m2,integer)
#                                and type (j3+m3,integer)) then RETURN (0) fi;
#   if m1+m2 <> m3 then RETURN (0) fi;
#   if j3 < abs(j1-j2) or j3 > j1+j2 then RETURN (0) fi;
#
#   (-1)^(j1-j2+m3)*
#       simplify(Wigner_3j(j1,j2,j3,m1,m2,-m3)*sqrt(2*j3+1),sqrt);
# end:
def CG_SO3(j1: nonnegint | Rational, m1: int | Rational,
           j2: nonnegint | Rational, m2: int | Rational,
           j3: nonnegint | Rational, m3: int | Rational) -> Expr:
    j1, m1, j2, m2, j3, m3 = S((j1, m1, j2, m2, j3, m3))

    if not((2 * j1).is_integer and (2 * m1).is_integer and
           (2 * j2).is_integer and (2 * m2).is_integer and
           (2 * j3).is_integer and (2 * m3).is_integer):
        raise ValueError(f'all arguments must be half-integers: {j1}, {m1}, {j2}, {m2}, {j3}, {m3}')

    if abs(m1) > j1 or abs(m2) > j2 or abs(m3) > j3:
        return S.Zero

    if not ((j1 + m1).is_integer and
            (j2 + m2).is_integer and
            (j3 + m3).is_integer):
        return S.Zero

    if m1 + m2 != m3:
        return S.Zero

    if j3 < abs(j1 - j2) or j3 > j1 + j2:
        return S.Zero

    return S.NegativeOne ** (j1 - j2 + m3) * \
        simplify(Wigner_3j(j1, j2, j3, m1, m2, -m3) * sqrt(2 * j3 + 1))


# Wigner_3j:=proc(j1,j2,j3,m1,m2,m3)
#      (-1)^(2*j1-j2+m2)
#        * sqrt((j1+j2-j3)!*(j1-m1)!*(j2-m2)!*(j3-m3)!*(j3+m3)!/
#               ((j1+j2+j3+1)!*(j1-j2+j3)!*(-j1+j2+j3)!*(j1+m1)!*(j2+m2)!))
#        * add((-1)^s*(j1+m1+s)!*(j2+j3-m1-s)!/
#                     (s!*(j1-m1-s)!*(j2-j3+m1+s)!*(j3+m3-s)!),
#              s=max(0,j3-j2-m1)..min(j3+m3,j1-m1))
# end:
def Wigner_3j(j1: nonnegint | Rational, j2: nonnegint | Rational, j3: nonnegint | Rational,
              m1: int | Rational, m2: int | Rational, m3: int | Rational) -> Expr:
    j1, j2, j3, m1, m2, m3 = S((j1, j2, j3, m1, m2, m3))

    return S.NegativeOne ** (2 * j1 - j2 + m2) * \
        sqrt(factorial(j1 + j2 - j3) *
             factorial(j1 - m1) *
             factorial(j2 - m2) *
             factorial(j3 - m3) *
             factorial(j3 + m3) /
             (factorial(j1 + j2 + j3 + 1) *
              factorial(j1 - j2 + j3) *
              factorial(-j1 + j2 + j3) *
              factorial(j1 + m1) *
              factorial(j2 + m2))) * \
        sum(S.NegativeOne ** s *
            factorial(j1 + m1 + s) *
            factorial(j2 + j3 - m1 - s) /
            (factorial(s) *
             factorial(j1 - m1 - s) *
             factorial(j2 - j3 + m1 + s) *
             factorial(j3 + m3 - s)) for s in range(max(0, j3 - j2 - m1),
                                                    min(j3 + m3, j1 - m1) + 1))
