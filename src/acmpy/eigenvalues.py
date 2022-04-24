"""This module computes eigenvalues and eigenbases."""

from sympy import Matrix, shape


def Eigenvectors(M: Matrix) -> tuple[list[float], Matrix]:
    """Return the eigenvalues and eigenvectors as in Maple."""
    P: Matrix
    D: Matrix
    P, D = M.diagonalize()
    eigenvalues: list[float] = [float(D[i, i]) for i in range(D.shape[0])]

    return eigenvalues, P


# # The following procedure Eigenfiddle diagonalises the Matrix which is
# # passed to it, and returns a pair
# #                          [eigs_list,basis_Mat].
# # The first element of this pair is a list of the eigenvalues in
# # ascending order, and the second element of the pair is the matrix P
# # which transforms the original matrix H to the diagonal matrix P^{-1}HP
# # whose diagonal elements are those given in the first element of the pair.
# # Thus, its columns are the eigenvectors corresponding to those eigenvalues.
#
# # The matrix (H) that is passed to Eigenfiddle is diagonalised using
# # Maple's Eigenvectors procedure.
# # This matrix ought to be Hermitian but might not be because of truncation
# # effects. Thus, before being diagonalised, it is averaged with its transpose
# # to ensure that it is symmetric, and therefore yields real eigenvalues.
#
# # Note that Maple attempts to diagonalise retaining the datatype
# # of the passed Matrix. If this datatype is not a float, then
# # the procedure is very slow. For ACM calculations, we should
# # therefore ensure that Hmatrix has float entries.
#
#
# Eigenfiddle:=proc(Hmatrix::Matrix,$)
#     local i,n,real_eigens,eigenstuff,eigen_order;
#
#   n:=RowDimension(Hmatrix);
#
#   # The Maple function Eigenvectors returns a pair, the first of
#   # which is a list of eigenvalues, and the second is a matrix
#   # whose columns are the corresponding eigenvectors.
#   # We ensure that the Matrix being processed is diagonal by
#   # averaging it with its transpose.
#
#   eigenstuff:=Eigenvectors(Matrix(n,n,(i,j)->(Hmatrix[i,j]+Hmatrix[j,i])/2,
#                                     scan=diagonal[upper],shape=symmetric));
#
#   # The following list contains pairs [eig,i], where i is the index
#   # in the list. The idea is to sort the eigenvalues into increasing
#   # order, but keep track of their original i's, so that we can
#   # then use the same order for the eigenvectors.
#
#   real_eigens:=[seq([eigenstuff[1][i],i],i=1..n)];
#
#   # Now sort these into increasing values of the eigenvalues using
#   # the pair_order function defined below.
#
#   real_eigens:=sort(real_eigens,pair_order);
#
#   # Get the index order - to be applied to the eigenvectors below.
#
#   eigen_order:=map2(op,2,real_eigens);
#
#   # Return pair,
#   #   element 1 lists all (real) e-values
#   #   element 2 is a transformation matrix, with the
#   #              columns e-vectors of above e-values.
#
#   [ map2(op,1,real_eigens), Matrix([Column(eigenstuff[2],eigen_order)]) ];
# end:
def Eigenfiddle(Hmatrix: Matrix) -> tuple[list[float], Matrix]:

    n, m = shape(Hmatrix)
    if n != m:
        raise ValueError(f'Matrix is not square: {n}, {m}')

    H: Matrix = ((Hmatrix + Hmatrix.T) / 2).evalf()

    eigen_values: list[float]
    P: Matrix
    eigen_values, P = Eigenvectors(H)

    real_eigens: list[tuple[float, int]] = [(value, i) for i, value in enumerate(eigen_values)]
    real_eigens.sort()

    eigen_values = [p[0] for p in real_eigens]
    eigen_order: list[int] = [p[1] for p in real_eigens]
    eigen_vectors: Matrix = Matrix(n, n, lambda i, j: P[i, eigen_order[j]])

    return eigen_values, eigen_vectors

