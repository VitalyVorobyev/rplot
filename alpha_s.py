import numpy as np

# Chetyrkin, Kniehl, Steinhauser, Nucl. Phys. B 510 (1998) 61
#
# "Decoupling Relations to O(α_s^3) and their Connection to Low-Energy Theorems"
#

zeta3 = 1.202057  # Reimann's zeta function of 3
def get_beta0(nf):
    return (11 - 2/3 * nf) / 4

def get_beta1(nf):
    return (102 - 38/3 * nf) / 16

def get_beta2(nf):
    return (2857/2 - 5033/18*nf + 325/54*nf**2) / 64

def get_beta3(nf):
    return ((149753/6 + 3564*zeta3 + (-1078361/162 - 6508/27*zeta3))*nf +
        (50065/162 + 6472/81*zeta3)*nf**2 + 1093/729*nf**3) / 256

betas = {nf : np.array([get_beta0(nf), get_beta1(nf), get_beta2(nf), get_beta3(nf)])
    for nf in range(1, 7)}

omegas = {nf: (b / b[0])[1:] for nf, b in betas.items()}

def alpha_s_over_pi(s, nf, lam=0.25):
    beta0, (b1, b2, b3) = betas[nf][0], omegas[nf]
    L = np.log(s / lam**2)
    logL = np.log(L)
    beta0LInv = 1 / (beta0 * L)

    return beta0LInv * (
        1 - beta0LInv * b1 * logL +
        beta0LInv**2 * (b1**2 * ( logL**2 - logL - 1) + b2) +
        beta0LInv**3 * (
            b1**3 * (-logL**3 + 5/2*logL**2 + 2*logL - 1/2) -
            3*b1*b2*logL + b3/2
        )
    )

def as_b0(nf):
    return (33 - 2*nf) / (12*np.pi)

def as_b1(nf):
    return (153 - 19*nf) / (24*np.pi**2)

def as_b2(nf):
    return (2857 - 5033/9*nf + 325/27*nf**2) / (128*np.pi**3)

def as_b3(nf):
    return (149753/6 + 3564*zeta3 + (-1078361/162 - 6508/27*zeta3)*nf +\
        (50065/162 + 6472/81*zeta3)*nf**2 + 1093/729*nf**3) / (256*np.pi**4)

bees = {nf: (as_b0(nf), as_b1(nf), as_b2(nf), as_b3(nf)) for nf in range(1, 7)}

def alpha_s_over_pi_v1(s, nf, lamb=0.25):
    t = np.log(s / lamb**2)
    l = np.log(t)
    lsq, lcube = l**2, l**3
    b0, b1, b2, b3 = bees[nf]
    b0sq_t = b0**2 * t
    return (
        1 - b1*l / b0sq_t + 
        (b1**2 * (lsq - l - 1) + b0*b2) / b0sq_t**2 +
        (b1**3*(-2*lcube + 2*lsq + 4*l - 1) - 6*b0*b2*b1*l + b0**2*b3) / (2*b0sq_t**3)
    ) / (b0 * t)

