from acmpy.acm1_4 import Rational, ACM_Hamiltonian

B = 20
c2 = 1.5
c1 = 1 - 2 * c2
chi = 2.0
kappa = 0.0

x1 = -Rational(1, 2) / B
x3 = B * c1 / 2
x4 = B * c2 / 2
x6 = -chi
x10 = kappa

RWC_ham_fig5a = ACM_Hamiltonian(x1, 0, x3, x4, 0, x6, 0, 0, 0, x10)

if __name__ == '__main__':
    print(f'RWC_ham_fig5a: {RWC_ham_fig5a}')
