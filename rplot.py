#! /usr/bin/env python

import mpld3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 16})

from readpdg import dat_to_json
from rpredict import rew_v, rewqcd_v
from datafilter import rfilter

TAUMASS = 1.77682

def tau_xsec(sqrts):
    mask = sqrts < 2*TAUMASS
    gamma = 0.5 * sqrts / TAUMASS
    gamma[mask] = 1
    beta = np.sqrt(1. - 1./gamma**2)
    coef = 86.8  # nb (4 * pi * alpha**2 / 3)
    return 0.5 * coef * beta * (3 - beta**2) / sqrts**2

def rplot(df, lo=2, hi=7, deltaE=0.01, deltaSigma=2):
    fig, ax1 = plt.subplots(figsize=(18, 8))
    for key, data in df.groupby('code'):
        print(key, data.shape)
        df = rfilter(data, deltaE, deltaSigma)
        ax1.errorbar(
            x=df.Ecm, y=df.R,
            xerr=(df.Ecm - df.EcmLo, df.EcmHi - df.Ecm),
            yerr=(df.errn, df.errp),
            linestyle='none', label=key,
            markersize=5, marker='o')

    sqrts = np.concatenate([
        np.linspace(lo, 3.77 - 1.e-5, 20),
        np.linspace(3.77 + 1.e-5, hi, 20)
    ])
    ax1.plot(sqrts, rew_v(sqrts**2), '--', color='k', label='EW prediction')
    ax1.plot(sqrts, rewqcd_v(sqrts**2), color='k', label='EW + pQCD prediction')

    ax1.set_ylim((0, 5.25))
    ax1.set_xlim((lo, hi))
    ax1.set_xlabel(r'$\sqrt{s}$ (GeV)', fontsize=20)
    ax1.set_ylabel('R', fontsize=20)
    ax1.minorticks_on()
    ax1.grid(which='major')
    ax1.grid(which='minor', linestyle=':')
    ax1.legend(fontsize=14)

    ax2 = ax1.twinx()
    sqrts = np.linspace(2*TAUMASS, 7, 1000)
    taux = tau_xsec(sqrts)
    ax2.plot(sqrts, taux, label=r'$\sigma(e^+e^-\to\tau^+\tau^-)$')
    ax2.set_ylim((0, 10.5))
    ax2.set_ylabel(r'$\sigma$ (nb)', fontsize=20)
    ax2.legend()

    fig.tight_layout()

    for ext in ['pdf', 'png', 'svg']:
        plt.savefig(f'plots/rplot.{ext}')

    plt.show()

def main():
    df = dat_to_json()
    rplot(df, deltaE=0.02, deltaSigma=2)

if __name__ == '__main__':
    main()
