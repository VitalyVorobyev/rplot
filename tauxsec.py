import numpy as np

MTAU = 1.77682

def tau_xsec(sqrts):
    mask = sqrts < 2*MTAU
    gamma = 0.5 * sqrts / MTAU
    gamma[mask] = 1
    beta = np.sqrt(1. - 1./gamma**2)
    coef = 86.8  # nb (4 * pi * alpha**2 / 3)
    return 0.5 * coef * beta * (3 - beta**2) / sqrts**2
