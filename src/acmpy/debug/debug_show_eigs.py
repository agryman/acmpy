from acmpy.acm1_4 import ACM_set_defaults, Show_Eigs, nonnegint, NDArrayFloat, list_to_ndarray


def main() -> None:
    ACM_set_defaults(0)

    Lvals: list[nonnegint] = list(range(10))
    eigen_vals: list[NDArrayFloat] = [list_to_ndarray([val + L / 2 for val in range(10)]) for L in Lvals]
    Show_Eigs(eigen_vals, Lvals)


if __name__ == '__main__':
    main()
