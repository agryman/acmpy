"""This module defines radial operators."""

import math
import numpy as np
from abc import ABC, abstractmethod
from acmpy.radial_bases import Nu, RadialBasis, TruncatedRadialSpace
from acmpy.compat import NDArrayFloat


class RadialOperator(ABC):
    """This is the abstract base class for all radial operators."""

    basis: RadialBasis
    subspace: TruncatedRadialSpace

    def __init__(self, basis: RadialBasis) -> None:
        self.basis = basis

    @abstractmethod
    def matrix_element(self, mu_f: Nu, mu_i: Nu) -> float:
        """Return a matrix element of the operator."""
        ...

    def matrix(self, subspace: TruncatedRadialSpace) -> NDArrayFloat:
        labels: list[Nu] = subspace.labels()
        return np.array([[self.matrix_element(mu_f, mu_i)
                          for mu_i in labels]
                         for mu_f in labels])


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
def ME_Radial_b2(lambdaa: float, mu_f: Nu, mu_i: Nu) -> float:
    if mu_f == mu_i - 1:
        return math.sqrt((lambdaa + mu_i - 1) * mu_i)
    if mu_f == mu_i:
        return lambdaa + 2 * mu_i
    if mu_f == mu_i + 1:
        return math.sqrt((lambdaa + mu_i) * (mu_i + 1))

    return 0.0


class RadialOperator_b2(RadialOperator):
    """This class models the $\beta^2$ operator."""

    def matrix_element(self, mu_f: Nu, mu_i: Nu) -> float:
        return ME_Radial_b2(self.basis.lambdaa, mu_f, mu_i)

