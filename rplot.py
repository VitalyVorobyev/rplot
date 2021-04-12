#! /usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 16})

from rpredict import rew_v, rewqcd_v
from datafilter import rfilter
from loaddata import measurements_in_range
from tauxsec import tau_xsec, MTAU
from colors import kelly_gen

MJPSI  = 3.09690
MPSI2S = 3.68610
WJPSI  =  92.9e-6
WPSI2S = 294.0e-6
GAMEEJPSI  = 5.550e-6 * 10**6
GAMEEPSI2S = 2.279e-6 * 10**6

def rbw(sqrts, mass, width, gammaee):
    """ Relativistic Breit-Wigner lineshape """
    return np.abs(gammaee * width / (sqrts**2 - mass**2 + 1j * sqrts * width))**2


def psi_lineshape(sqrts):
    return rbw(sqrts, MJPSI,WJPSI, GAMEEJPSI) +\
           rbw(sqrts, MPSI2S, WPSI2S, GAMEEPSI2S)


def plot_tau_xsec(ax, ylim=(0, 10.5)):
    sqrts = np.concatenate([
        np.linspace(2*MTAU, 2*MTAU+0.3, 150),
        np.linspace(2*MTAU+0.3, 7, 50)
    ])
    taux = tau_xsec(sqrts)
    ax.plot(sqrts, taux, label=r'$\sigma(e^+e^-\to\tau^+\tau^-)$')

    sqrtsJpsi = np.linspace(MJPSI - 1e-1, MJPSI + 1e-1, 1000)
    ax.plot(sqrtsJpsi, 30*rbw(sqrtsJpsi, MJPSI, 1e-3, GAMEEJPSI), 'k--', label=rf'$J/\psi$ (not in scale)')
    sqrtsPsi2s = np.linspace(MPSI2S - 1e-1, MPSI2S + 1e-1, 1000)
    ax.plot(sqrtsPsi2s, 100*rbw(sqrtsPsi2s, MPSI2S, 1e-3, GAMEEPSI2S), 'k:', label=rf'$\psi\left(2S\right)$ (not in scale)')

    ax.set_ylim(ylim)
    ax.set_ylabel(r'$\sigma$ (nb)', fontsize=20)
    ax.legend(fontsize=14)


def plot_rdata(ax, data, deltaE=0.01, deltaSigma=2, msize=5, keycol={}):
    colgen = kelly_gen()
    for meta, df in data:
        df = rfilter(df, deltaE, deltaSigma)
        color = keycol.get(meta.code, next(colgen))
        keycol[meta.code] = color
        ax.errorbar(
            x=df.E, y=df.R, xerr=(df.dEn, df.dEp), yerr=(df.dRn, df.dRp),
            linestyle='none', markersize=msize, marker='o',
            label=f'{meta.experiment} {meta.year%100:02d}', color=color)

    return keycol


def add_ticks(ax):
    ax.minorticks_on()
    ax.grid(which='major')
    ax.grid(which='minor', linestyle=':')


def rplot(ax, data, lo=2, hi=7, deltaE=0.01, deltaSigma=2,
          legend=True, legendsize=14, lblsize=20, predictions=True,
          xlbl=r'$\sqrt{s}$ (GeV)', msize=5):
    keycol = plot_rdata(ax, data, deltaE, deltaSigma, msize=msize)
    sqrts = np.concatenate([
        np.linspace(lo, 3.77 - 1.e-5, 10),
        np.linspace(3.77 + 1.e-5, hi, 10)
    ])
    if predictions:
        ax.plot(sqrts, rew_v(sqrts**2), '--', color='k', label='Naive model')
        ax.plot(sqrts, rewqcd_v(sqrts**2), color='k', label='3-loop pQCD')

    ax.set_ylim((0, 5.25))
    ax.set_xlim((lo, hi))
    ax.set_xlabel(xlbl, fontsize=lblsize)
    ax.set_ylabel('R', fontsize=lblsize)
    add_ticks(ax)
    if legend:
        ax.legend(fontsize=legendsize)
    
    return keycol


def simple_plot(lo=2, hi=7, deltaE=0.01, deltaSigma=2):
    fig, ax = plt.subplots(figsize=(18, 8))
    fil = lambda meta, df: df if meta.year > 1989 else pd.DataFrame([])
    data = measurements_in_range(lo, hi, fil)

    keycol = rplot(ax, data, lo, hi, deltaE, deltaSigma)
    plot_tau_xsec(ax.twinx())

    ax0 = plt.axes([.59, .25, .33, .30])
    data0 = measurements_in_range(3.6, 4, fil)
    plot_rdata(ax0, data0, deltaE, deltaSigma, keycol=keycol)
    add_ticks(ax0)

    fig.tight_layout()
    for ext in ['pdf', 'png', 'svg']:
        plt.savefig(f'plots/rplot.{ext}')
    plt.show()


if __name__ == '__main__':
    simple_plot()
