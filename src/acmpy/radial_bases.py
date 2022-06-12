"""The module contains classes that model bases and subspaces of the radial beta Hilbert space."""

from acmpy.compat import nonnegint, require_nonnegint_range, posint

# ###########################################################################
# ####--------------- Representations on the radial space ---------------####
# ###########################################################################
#
# # The next set of routines deal with representing operators in the
# # radial (beta) space. The bases for the radial Hilbert space are
# # dependent on two parameters (a,lambda). For each such pair,
# # the basis states are labelled by a single index nu=0,1,2,....


class RadialBasis:
    """This class models a basis for the radial beta Hilbert space."""
    lambdaa: float

    def __init__(self, lambdaa: float) -> None:
        if lambdaa <= 0.0:
            raise ValueError(f'lambdaa must be positive. Got: {lambdaa}')
        self.lambdaa = lambdaa


# # A truncated Hilbert space is indexed by states labelled
# #     nu_min, nu_min+1, nu_min+2, ... nu_max
# # (usually we would use nu_min=0).
# # The following two functions each take arguments nu_min and nu_max;
# # the first returns the dimension of the truncated space,
# # the second returns a list of all the labels.
#
# dimRadial:=(nu_min::nonnegint,nu_max::nonnegint)
#   -> `if`(nu_max>=nu_min,nu_max-nu_min+1,0):
Nu = nonnegint
"""The basis vectors are labelled by nonnegative integers, typically denoted by the symbols $nu$ or $mu$."""


def dimRadial(nu_min: Nu, nu_max: Nu) -> nonnegint:
    return nu_max - nu_min + 1 if nu_max >= nu_min else 0


# lbsRadial:=proc(nu_min::nonnegint,nu_max::nonnegint)
#   if nu_min>nu_max then
#     error("Radial range invalid");
#   else
#     [seq(i,i=nu_min..nu_max)];
#   fi:
# end:
def lbsRadial(nu_min: Nu, nu_max: Nu) -> list[Nu]:
    return list(range(nu_min, nu_max + 1))


class TruncatedRadialSpace:
    """This class models a truncated radial beta Hilbert space."""
    nu_min: nonnegint
    nu_max: nonnegint

    def __init__(self, nu_min: nonnegint, nu_max: nonnegint) -> None:
        require_nonnegint_range('nu', nu_min, nu_max)
        self.nu_min = nu_min
        self.nu_max = nu_max

    def dim(self) -> posint:
        """Return the dimension of the truncated space."""
        return dimRadial(self.nu_min, self.nu_max)

    def labels(self) -> list[Nu]:
        """Return the ordered list of basis vector labels."""
        return lbsRadial(self.nu_min, self.nu_max)
