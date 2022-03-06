""""4. Procedures that pertain only to the spherical (gamma,Omega) space."""
# ###########################################################################
# ####------------- Representations on the spherical space --------------####
# ###########################################################################
#
# # The following two give the dimensions of SO(3) and SO(5)
# # irreducible representations (symmetric).
#
# dimSO3:=(L::nonnegint) -> 2*L+1:                    # SO(3) irrep dimension
# dimSO5:=(v::nonnegint) -> (v+1)*(v+2)*(2*v+3)/6:    # SO(5) irrep dimension
#
# # The following returns the total number of SO(3) irreps
# # (some possibly equivalent) in the SO(5) irrep of seniority v.
#
# dimSO5r3_allL:=(v::nonnegint) -> iquo( v*(v+3), 6 ) + 1:
#
# # The following sums the previous over the range v_min...v_max of seniorities.
#
# dimSO5r3_rngVallL:=(v_min::nonnegint,v_max::nonnegint)
#     -> add(dimSO5r3_allL(v),v=v_min..v_max):
#
#
# # The following procedure gives the multiplicity of SO(3) irreps of
# # angular momentum L in the SO(5) irrep of seniority v. It uses (6).
# # It then provides the maximum value of the "missing" label alpha
# # (the minimum value is 1).
#
# dimSO5r3:=proc(v::integer,L::integer,$)
#   local b,d;
#
#   if v<0 or L<0 or L>2*v then
#     0:
#   else
#     b:=(L+3*irem(L,2))/2;
#     if v>=b then
#       d:=1+iquo(v-b,3);
#     else
#       d:=0;
#     fi:
#     if v>=L-2 then
#       d:=d-iquo(v-L+2,3);
#     fi:
#     d:
#   fi:
# end:
#
# # We now provide formulae similar to those above, counting SO(3) irreps,
# # but with L fixed or taking a range L_min,...,Lmax
# # (if Lmax is not given, then it is assumed that Lmin=Lmax).
#
# # The following counts SO(3) irreps for fixed v and a range of L.
#
# dimSO5r3_rngL:=(v::nonnegint,L_min::nonnegint,L_max::nonnegint)
#     -> add( dimSO5r3(v,j), j=L_min..L_max):
#
# # The following counts SO(3) irreps for a range of v and fixed L.
#
# dimSO5r3_rngV:=(v_min::nonnegint,v_max::nonnegint,L::nonnegint)
#     -> add( dimSO5r3(i,L),i=v_min..v_max):
#
# # The following counts SO(3) irreps for a range of v and a range of L.
#
# dimSO5r3_rngVrngL:=(v_min::nonnegint,v_max::nonnegint,
#                     L_min::nonnegint,L_max::nonnegint)
#     -> add(dimSO5r3_rngL(i,L_min,L_max),i=v_min..v_max):
#
# # The following also counts SO(3) irreps for a range of v and a range of L,
# # but if Lmax is not given, then it is assumed that Lmin=Lmax.
#
# dimSO5r3_rngVvarL:=(v_min::nonnegint,v_max::nonnegint,
#                     L_min::nonnegint,L_max::nonnegint)
#     -> `if`(_npassed>3,dimSO5r3_rngVrngL(_passed),
#                        dimSO5r3_rngV(_passed)):
#
# ###########################################################################
#
# # We now specify procedures which give lists of labels that correspond
# # to the above counting/dimension formulae. In all but the first,
# # the labels are triples [v,alpha,L], where L gives the SO(3) angular
# # momentum and alpha is the "missing label" which distinguishes
# # SO(3) irreps having identical L and seniority v.
# # (Note that these are "reduced" labels for the states:
# #  the magnetic quantum label M is not included ---
# #  it would vary over the 2L+1 values  -L,-L+1,-L+2,...,L.)
# # These lists are used to label the states between which representation
# # matrices are constructed. In these lists of states, L varies slowest,
# # then v, with the missing label alpha varying quickest.
#
# # The following returns a list of labels [alpha,L] for all the
# # SO(3) irreps in a single SO(5) irrep of seniority v.
#
# lbsSO5r3_allL:=proc(v::nonnegint,$)
#     [seq(seq([a,LL],a=1..dimSO5r3(v,LL)),LL=0..2*v)]:
# end:
#
#
# # The following returns a list of labels [v,alpha,L] for the
# # range v_min...v_max of seniorities.
#
# lbsSO5r3_rngVallL:=proc(v_min::nonnegint,v_max::nonnegint,$)
#   if v_min>v_max then
#     error("Seniority range invalid");
#   else
#     [seq(seq(seq([u,a,LL],a=1..dimSO5r3(u,LL)),u=v_min..v_max),
#                                                       LL=0..2*v_max)]:
#   fi:
# end:
#
# # The following returns a list of labels [v,alpha,L] for a fixed seniority
# # v, but L restricted to the range L_min...L_max of SO(3) angular momenta.
#
# lbsSO5r3_rngL:=proc(v::nonnegint,L_min::nonnegint,L_max::nonnegint,$)
#   if L_min>L_max then
#     error("Parameter range invalid");
#   else
#     [seq(seq([v,a,LL],a=1..dimSO5r3(v,LL)),LL=L_min..L_max)]:
#   fi:
# end:
#
# # The following returns a list of labels [v,alpha,L] for a range of
# # seniorities v_min,..,vmax, but fixed SO(3) angular momentum L.
#
# lbsSO5r3_rngV:=proc(v_min::nonnegint,v_max::nonnegint,L::nonnegint,$)
#   if v_min>v_max then
#     error("Seniority range invalid");
#   else
#     [seq(seq([u,a,L],a=1..dimSO5r3(u,L)),u=v_min..v_max)]:
#   fi:
# end:
#
# # The following returns a list of labels [v,alpha,L] for ranges of
# # seniorities v_min,..,vmax, and SO(3) angular momenta L_min,..,Lmax.
#
# lbsSO5r3_rngVrngL:=proc(v_min::nonnegint,v_max::nonnegint,
#                         L_min::nonnegint,L_max::nonnegint,$)
#   if v_min>v_max or L_min>L_max then
#     error("Seniority range invalid");
#   else
#     [seq(seq(seq([u,a,LL],a=1..dimSO5r3(u,LL)),u=v_min..v_max),
#                                   LL=L_min..L_max)]:
#   fi:
# end:
#
# # The following returns a list of labels [v,alpha,L] for ranges of
# # seniorities v_min,..,vmax, and SO(3) angular momenta L_min,..,Lmax,
# # but the final argument L_max may be omitted, in which case L_max=L_min
# # (it may be used instead of the previous two procedures).
#
# lbsSO5r3_rngVvarL:=proc(v_min::nonnegint,v_max::nonnegint,
#                         L_min::nonnegint,L_max::nonnegint,$)
#   if v_min>v_max then
#     error("Seniority range invalid");
#   elif _npassed>3 then
#     [seq(seq(seq([u,a,LL],a=1..dimSO5r3(u,LL)),u=v_min..v_max),
#                                   LL=L_min..L_max)]:
#   else
#     [seq(seq([u,a,L_min],a=1..dimSO5r3(u,L_min)),u=v_min..v_max)]:
#   fi:
# end:
#
#
