import numpy as np

from alpha_s import alpha_s_over_pi

charges = np.array([2, -1, -1, 2, -1, 2]) / 3
xi   = {idx : 3*np.sum(charges[:idx]**2) for idx in range(2, charges.size+1)}
zeta = {idx : charges[:idx].sum()**2 for idx in xi.keys()}
eta  = {idx : b / a for (idx, a), (_, b) in zip(xi.items(), zeta.items())}

for nf, r in xi.items():
    print(f'{nf}: {r:.3f}')

def nflav(s):
    if s < 1.02**2:
        return 2
    if s < 3.77**2:
        return 3
    if s < 10.58**2:
        return 4
    return 5

def as_c2(nf):
    return 1.9857 - 0.1152*nf

def as_c3(nf):
    return -6.63694 - 1.20013*nf - 0.00518*nf**2 - 1.240 * eta[nf]

def as_c4(nf):
    return -155.61 + 18.775*nf - 0.7974*nf**2 + 0.0215*nf**3 + (17.828-0.575*nf) * eta[nf]

cees = {nf: (1, as_c2(nf), as_c3(nf), as_c4(nf)) for nf in xi.keys()}

def rew(s):
    return xi[nflav(s)]

def rewqcd(s):
    nf = nflav(s)
    return xi[nf] * (1 + np.dot(cees[nf], alpha_s_over_pi(s, nf)**np.arange(1, 5)))

rew_v = np.vectorize(rew)
rewqcd_v = np.vectorize(rewqcd)

def main():
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.rcParams.update({'font.size': 16})

    sqrts = np.linspace(2, 7, 500)

    fig = plt.figure(figsize=(9, 6))
    plt.plot(sqrts, rewqcd_v(sqrts**2) - rew_v(sqrts**2))
    plt.xlim((2, 7))
    plt.ylim((0, 0.3))
    plt.minorticks_on()
    plt.grid(which='major')
    plt.grid(which='minor', linestyle=':')
    plt.xlabel(r'$\sqrt{s}$ (GeV)')
    plt.ylabel('QCD correction to R')
    plt.savefig('plots/r-correction.pdf')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
