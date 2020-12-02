#! /usr/bin/env python

from operator import le
import os
import itertools
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 16})
import mpld3

from rpredict import rew_v, rewqcd_v
from datafilter import rfilter
from loaddata import measurements_in_range
from tauxsec import tau_xsec, MTAU
from colors import kelly_gen

def static_js_url():
    return '/static/sct/js'

def d3url():
    return os.path.join(static_js_url(), 'd3.v5.min.js')

def mpld3url():
    return os.path.join(static_js_url(), 'mpld3.v0.5.1.min.js')


def rbw(x, m, w):
    """
    Relativistic Breit-Wigner lineshape
    """
    return 

def plot_tau_xsec(ax, ylim=(0, 10.5)):
    sqrts = np.concatenate([
        np.linspace(2*MTAU, 2*MTAU+0.3, 150),
        np.linspace(2*MTAU+0.3, 7, 50)
    ])
    taux = tau_xsec(sqrts)
    ax.plot(sqrts, taux, label=r'$\sigma(e^+e^-\to\tau^+\tau^-)$')
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
            linestyle='none', markersize=5, marker='o',
            label=f'{meta.experiment} {meta.year%100:02d}', color=color)
    return keycol

def add_ticks(ax):
    ax.minorticks_on()
    ax.grid(which='major')
    ax.grid(which='minor', linestyle=':')

def rplot(ax, data, lo=2, hi=7, deltaE=0.01, deltaSigma=2,
          legend=True, legendsize=14, lblsize=20, predictions=True,
          xlbl=r'$\sqrt{s}$ (GeV)', msize=5):
    keycol = plot_rdata(ax, data, deltaE, deltaSigma, msize=5)
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

def interactive_r(lo=2, hi=7, deltaE=0.01, deltaSigma=2, opath='plots/rplotd3.html'):
    fig, ax = plt.subplots(figsize=(12, 8))
    data = measurements_in_range(lo, hi)
    rplot(ax, data, lo, hi, deltaE, deltaSigma, legendsize=14,
          xlbl='Energy (GeV)', lblsize=20, msize=3)
    fig.tight_layout()

    html = mpld3.fig_to_html(fig, figid='rplot', d3_url=d3url(), mpld3_url=mpld3url())
    html = re.sub(r'(\d+\.\d{4})\d+', r'\1', html)
    html = re.sub(r'el\d+(\d{5})', 'el' + r'\1', html)
    
    with open(opath, 'w') as ofile:
        ofile.write(html)

    for ext in ['pdf', 'png', 'svg']:
        plt.savefig(f'plots/rplotd3.{ext}')

    plt.show()

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))

    lo, hi = 2, 7
    simple_plot(lo=lo, hi=hi, deltaE=0.02, deltaSigma=2)

if __name__ == '__main__':
    # main()
    simple_plot()
    # interactive_r()
