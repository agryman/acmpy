"""8. Procedures that aid the production of the data for the particular Hamiltonians considered in [RWC2009]."""
# ###########################################################################
# ####-------- Aiding calculations for Hamitlonians in [RWC2009] --------####
# ###########################################################################
#
# # Here we provide procedures that may be used instead of
# # ones above to calculate for Hamiltonians considered in [RWC2009].
#
# # The following procedure RWC_Ham obtains the ACM encoding of Hamiltonians
# # of the RWC form given in (B12) (see also (89) of [RWC2009], with
# # c1=1-2*alpha and c2=alpha, and eqns. (4.230) & (4.220) of [RowanWood].)
#
# RWC_Ham:=(B,c1,c2,chi,kappa)->
#   ACM_Hamiltonian(-1/2/B,0,B*c1/2,B*c2/2,0,-chi,0,0,0,kappa);
#
#
# # The following procedure RWC_expt gives the expectation value of the above
# # Hamiltonian on the |(anorm,lambda0)0;0100> basis state, given by (B16).
# # (Note that (76) of [RWC2009] contains typos.)
#
# RWC_expt:=proc(B::constant,c1::constant,c2::constant,kappa::constant,
#                           anorm::constant,lambda0::constant,$)
#   local aa:
#
#   aa:=anorm^2:
#   aa*(4+9/(lambda0-1))/8/B + B*lambda0*c1/2/aa
#               + B*lambda0*(lambda0+1)*c2/2/aa^2 + kappa/3:
# end:
#
# # The following procedure RWC_expt_link gives the same expectation value
# # (B16) as that above, but lambda0 is assumed to depend on anorm through
# # the function RWC_dav (see below).
#
# RWC_expt_link:=proc(B::constant,c1::constant,c2::constant,kappa::constant,
#                           anorm::constant,$)
#   RWC_expt(_passed,evalf(RWC_dav(c1,c2,anorm))):
# end:
#
#
# # The following procedure RWC_dav calculates lambda0 from anorm
# # (and c1 and c2) using (B11) via (B15).
#
# RWC_dav:=proc(c1::constant,c2::constant,anorm::constant,v::nonnegint:=0,$)
#   lam_dav(anorm,beta_dav(c1,c2),v)
# end:
#
# # The following calculates lambda_v using (B7) - or using
# # B11 if the final argument is not given (it defaults to 0).
#
# lam_dav:=proc(a::constant,beta0::constant,v::nonnegint:=0,$)
#     1+sqrt( (v+3/2)^2 + a^4*beta0^4 )
# end:
#
# # The following calculates beta_0 using (B15)
#
# beta_dav:=proc(c1::constant,c2::constant,$)
#   if evalf(c1)>=0 then
#     0
#   else
#     sqrt(-c1/c2/2)
#   fi;
# end:
#
# # The following procedure RWC_alam returns values of the ACM parameters
# # (anorm,lambda), which are "optimal" in the cases of the RWC Hamiltonians.
# # This seeks the minimal value of RWC_expt, given above, by solving
# # for a turning point.
# # The fourth parameter is for seniority v, which is 0 for the
# # analysis given in [WR2015], but in the case of more general v,
# # (for L=0 (so 3\v) and no spherical dependence in the potential),
# # the 9/4 factor in the first term of (B.16) is replaced by
# # the more general (v+3/2)^2.
#
# RWC_alam:=proc(B::constant,c1::constant,c2::constant,v::nonnegint:=0,$)
#   local RWC1,RWC2,muf,aa0,vshft,A;
#
#   vshft:=(2*v+3)^2:  # This is 9 for the v=0 case.
#
#   if evalf(c1)<0 then
#           # Here lambda is a function of aa (i.e. a^2).
#           # There is always one positive solution in this case
#           # (in fact, I've never found other real solns).
#
#     # We use mu=2(lambda-1) where lambda is given by (B11) via (B15).
#
#     muf:=(aa) -> sqrt( vshft + (aa*c1/c2)^2 ):
#
#     # The following is the derivative of (B16) noting that
#     # d(mu)/d(aa)=aa*(c1/c2)^2/mu.  But multiplied by 4*aa^3*B*mu.
#
#     RWC2:=(aa,mu) -> (c1/c2)^2 * (-vshft*aa^5/mu^2
#                                     + aa^3*B^2*c1 + aa^2*B^2*c2*(mu+3))
#                        + aa^3*(2*mu+vshft)
#                        - B^2*mu*(mu+2)*(aa*c1+c2*(mu+4)):
#
#     aa0:=max(fsolve(RWC2(A,muf(A))=0,A)):
#     return [sqrt(aa0),1+muf(aa0)/2]:
#
#   else   # (Here lambda is constant)
#          # There is always 1 positive solution in this case
#          # (fsolve produces real solns.) and possibly two others that
#          # are negative. Use max to exclude them.
#
#     RWC1:=(aa) -> aa^3 - B^2*c1*aa - (2*v+7)*B^2*c2:
#
#     aa0:=max(fsolve(RWC1(A)=0,A)):
#     return [sqrt(aa0),2.5]:
#   fi:
#
# end:
#
# # The following procedure RWC_alam36 is a simplified algorithm
# # for obtaining "optimal" values of (anorm,lambda), obtained by
# # matching second derivatives at the turning point of the potential.
# # This only gives good results in certain cases.
#
# RWC_alam36:=proc(B::constant,c1::constant,c2::constant,$)
#   local RWC1,RWC2,muf,aa0;
#
#   if evalf(c1)<0 then
#
#     return evalf([sqrt(sqrt(-B^2*c1/2)),1+sqrt(36+B^2*c1^4/c2^2)/4]):
#
#   else
#
#     return evalf([sqrt(sqrt(B*c1/4)),2.5]):
#
#   fi:
#
# end:
#
# # The following procedure RWC_alam_clam is another alternative that
# # returns values of the ACM parameters (anorm,lambda), which are
# # obtained from the minimal value of the expectation value of RWC_expt,
# # given above, with lambda assumed to take the constant value of 2.5
#
# RWC_alam_clam:=proc(B::constant,c1::constant,c2::constant,$)
#   local RWC1,RWC2,muf,aa0,A;
#
#     RWC1:=(aa) -> aa^3 - B^2*c1*aa - 7*B^2*c2:
#     aa0:=max(fsolve(RWC1(A)=0,A)):
#     return [sqrt(aa0),2.5]:
#
# end:
#
#
# # The following procedure RWC_alam_fun returns a triple
# #                 [anorm,lambda0,lambda_fun]
# # where anorm and lambda0 are "optimal" values obtained as in
# # RWC_alam above, and lambda_fun is a procedure that takes an argument
# # v that gives the (optimal) value of lambda(v)-lambda(0),
# # an integer of same parity as v.
# # This is not used elsewhere.
#
# RWC_alam_fun:=proc(B::constant,c1::constant,c2::constant,$)
#   local RWC1,RWC2,muf,aa0,A;
#
#   if evalf(c1)<0 then
#           # Here lambda is a function of aa (i.e. a^2).
#           # There is always one positive solution in this case
#           # (in fact, I've never found other real solns).
#
#     # We use mu=2(lambda-1) where lambda is given by (B11) via (B15).
#
#     muf:=(aa) -> sqrt( 9+ (aa*c1/c2)^2 ):
#
#     # The following is the derivative of (B16) noting that
#     # d(mu)/d(aa)=aa*(c1/c2)^2/mu.  But multiplied by 4*A^3*B*mu.
#
#     RWC2:=(aa,mu) -> (c1/c2)^2 * (-9*aa^5/mu^2
#                                     + aa^3*B^2*c1 + aa^2*B^2*c2*(mu+3))
#                        + aa^3*(2*mu+9)
#                        - B^2*mu*(mu+2)*(aa*c1+c2*(mu+4)):
#
#     aa0:=max(fsolve(RWC2(A,muf(A))=0,A)):
#     return [sqrt(aa0),1+muf(aa0)/2,lambda_davi_fun((aa0*c1/c2/2)^2)]:
#
#   else   # (Here lambda is constant)
#          # There is always 1 positive solution in this case
#          # (fsolve produces real solns.) and possibly two others that
#          # are negative. Use max to exclude them.
#
#     RWC1:=(aa) -> aa^3 - B^2*c1*aa - 7*B^2*c2:
#
#     aa0:=max(fsolve(RWC1(A)=0,A)):
#     return [sqrt(aa0),2.5,lambda_sho_fun]:
#   fi:
#
# end:
#
#
