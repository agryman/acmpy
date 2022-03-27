"""
This file was seeded with the contents of the Maple code acm1.4.mpl which is the published version.
Each line of the Maple code has been commented with a Python line comment so the code is valid Python.
I will convert each Maple line into equivalent Python.
"""
from acmpy.globals import ACM_set_defaults


# # acm.mpl (version 1.4, 27 Sept 2015)
# #  - minor improvements over version 1.3 (details at end of file).
#
# ###########################################################################
#
# # This code implements the ACM version of the Bohr model of the
# # atomic nucleus. The manuscript
# #   "A computer code for calculations in the algebraic collective
# #    model of the atomic nucleus",
# # by T.A. Welsh and D.J. Rowe [WR2015],
# # describes the mathematical foundations of the code, and also
# # serves as a manual. The manuscript (version 1.2) is available from
# #   http://arxiv.org/abs/1408.3824 (v2).
# # (A slightly improved version 1.3 was submitted for publication;
# #  this is being updated to version 1.4 following referees' comments.)
#
# # In brief, the code makes use of the SU(1,1) x SO(5) dynamical
# # group of the model, which enables the factorisation of states
# # into a direct product of radial states (with parameters anorm
# # and lambda) labelled by (nu), and SO(5) spherical harmonics,
# # labelled by (v,alpha,L,M).
# # We ignore the M throughout by dealing with reduced matrix elements.
# # The equation numbers, section numbers and tables referred to in
# # this file are those of the manuscript (version 1.4).
# # Note that the code makes use of Clebsch-Gordan coefficients
# # that are supplied in three zip archives. The files contained
# # in these archives should be unzipped and placed in a specific
# # directory stucture, as detailed in the manuscript.
#
# # Most of the calculations for the following paper [RWC2009] were
# # carried out using an earlier version of this code:
# #   "Bohr model as an algebraic collective model"
# #   by D.J. Rowe, T.A. Welsh and M.A. Caprio,
# #   Phys. Rev. C79 (2009) 054304.
#
#
# # The model was formulated in previous publications:
#
# # A pretty full explanation in Chapter 4 of the book [RowanWood]
# #   "Fundamentals of Nuclear Models: Foundational Models"
# #   by D.J. Rowe and J.L. Wood,
# #   World Scientific (Singapore), 2010.
#
# # An important precursor to this is the paper [Rowe2004]
# #   "A computationally tractable version of the collective model"
# #   by D.J. Rowe, Nucl. Phys. A 735 (2004) 372-392.
#
# ###########################################################################
#
# # The code below is separated into eight parts:
# #   1. Specification of global constants, and procedures that
# #      can be used to set their values;
# #   2. Procedures that pertain only to the radial (beta) space;
# #   3. Procedures that access the SO(5)>SO(3) Clebsch-Gordon coefficients;
# #   4. Procedures that pertain only to the spherical (gamma,Omega) space;
# #   5. Procedures that obtain the internal representation of operators;
# #   6. Procedures that represent operators on the full (cross-product)
# #      Hilbert space;
# #   7. Procedures that perform calculations on the full Hilbert space:
# #      diagonalizing, basis transforming, and data displaying.
# #   8. Procedures that aid the production of the data for the
# #      particular Hamiltonians considered in [RWC2009].
#
# # Note that in the few occasions that I've used Maple's 'simplify'
# # function (usually to simplify expressions containing surds or GAMMA),
# # I've explicitly used the 'sqrt' or 'GAMMA' argument.
# # This has been necessary for some combinations of Maple version with
# # linux kernel (e.g. incompatibility between Maple15 and linux kernel 3.4.6).
#
# ###########################################################################
# ###########################################################################
#
# # Extensive use is made of the LinearAlgebra library.
# # In particular, this provides the diagonalisation procedure that we use.
#
# with(LinearAlgebra):
#
#
"""The intervening code has been moved to the following modules:

1. globals.py
2. radial_space.py
3. so5_so3_cg.py
4. spherical_space.py
5. internal_operators.py
6. full_operators.py
7. full_space.py
8. hamiltonian_data.py
"""
# ######################################################################
#
# # We now set default values for all the global parameters
#
# ACM_set_defaults(0):
ACM_set_defaults(0)


# ######################################################################
# ######################################################################
#
#
# ######################################################################
# ### Changes from version 1.3 to this version 1.4.
# ######################################################################
#
# #     1. New procedure MF_Radial_id_poly() to calculate the polynomial
# #        (34). Altered the procedures ME_Radial_id_pl() and
# #        ME_Radial_id_ml() to call it, and evaluate the return value.
# #     2. Altered the procedure load_CG_table() so that it
# #        now deals correctly with the v2=0 case: for this
# #        case only, it doesn't load data from a file but generates
# #        the coefficients: the non-zero ones all being 1.0.
# #     3. Made the variable 'A' local in procedures RWC_alam() etc.,
# #        in case it has been assigned non-locally
# #        (for then an error would occur).
# #     4. Changed the float[8] datatypes in the Matrix
# #        constructors to float so that things still work if
# #        Digits is increased beyond that for which hardware
# #        mathematical operations are possible (usually 15).
# #     5. Altered some procedure argument types numeric -> constant
# #        to make them more versatile. Then, to cope with surd arguments,
# #        the 'if c1<0' tests have been changed to 'if evalf(c1)<0'.
# #     6. Coding of RWC_dav has changed to call (new)
# #        procedures lam_dav and beta_dev, making extensions
# #        and testing easier. The functionality hasn't changed.
# #        Similarly, also added v argument to RWC_alam.
# #     7. Changed coding of RepRadial_Prod and RepRadial_Prod_rem
# #        to ensure that when the operator list contains SU(1,1)
# #        operators (Sm,Sp or S0), and a lambda-changing identity
# #        operator is required, it is multiplied on the left or right
# #        as appropriate (though such a calculation is probably
# #        meaningless, c.f. eqns. (19) & (20) ).
# #     8. The procedures RepRadial_Prod_rem, RepRadial_Prod_rem,
# #        and RepRadial_bS_DS now return errors if either of their
# #        lambda values are non-positive.
# #     9. Applied simplify to return values of RepRadial and
# #        RepRadial_param because Maple doesn't automatically
# #        perform GAMMA cancellations for large values (>100) of
# #        its arguments (one wonders why not just for large values!).
# #    10. Removed a couple of unnecessary Matrix assignments,
# #        because the calculations were carried out 'inplace'.
#
# ######################################################################
# ###  End of Maple code file acm1.4.mpl .
# ######################################################################
