from time import process_time
import acmpy.examples.ex_1_0_preliminaries as preliminaries
from acmpy.examples.ex_2_1_specification_of_hamiltonian import B,RWC_ham_fig5a
from acmpy.acm1_4 import ACM_Scale, sqrt, Rational


def main() -> None:
    preliminaries.main()
    start: float = process_time()
    ACM_Scale(RWC_ham_fig5a, sqrt(B), Rational(5, 2), 0, 5, 0, 18, 0, 6)
    finish: float = process_time()
    elapsed: float = finish - start
    print(f'elapsed process time for ACM_Scale: {elapsed}')


if __name__ == '__main__':
    main()