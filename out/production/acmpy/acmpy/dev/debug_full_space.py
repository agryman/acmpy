from acmpy.full_space import Show_Eigs

eigen_vals = [[2.3, 3.1, 4.6]]
Lvals = [2]

Show_Eigs(eigen_vals, Lvals)

Show_Eigs(eigen_vals, Lvals, 4, 0, 10)

Show_Eigs([[2.1, 3.4, 5.9], [3.4, 5.7]], [0, 1], 3, 0, 10)
