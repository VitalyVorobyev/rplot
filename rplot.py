#! /usr/bin/env python

import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 16})
# import mpld3

from rpredict import rew_v, rewqcd_v
from datafilter import rfilter
from loaddata import measurements_in_range
from tauxsec import tau_xsec, MTAU

def static_js_url():
    return '/static/sct/js'

def d3url():
    return '/'.join([static_js_url(), 'd3.v5.min.js'])

def mpld3url():
    return '/'.join([static_js_url(), 'mpld3.v0.5.1.min.js'])


def rbw(x, m, w):
    """
    Relativistic Breit-Wigner lineshape
    """
    return 


def rplot(data, lo=2, hi=7, deltaE=0.01, deltaSigma=2):
    fig, ax1 = plt.subplots(figsize=(18, 8))
    for meta, df in data:
        df = rfilter(df, deltaE, deltaSigma)
        ax1.errorbar(
            x=df.E, y=df.R, xerr=(df.dEn, df.dEp), yerr=(df.dRn, df.dRp),
            linestyle='none', markersize=5, marker='o',
            label=f'{meta.experiment} {meta.year%100:02d}')

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
    sqrts = np.concatenate([
        np.linspace(2*MTAU, 2*MTAU+0.3, 150),
        np.linspace(2*MTAU+0.3, 7, 50)
    ])
    taux = tau_xsec(sqrts)
    ax2.plot(sqrts, taux, label=r'$\sigma(e^+e^-\to\tau^+\tau^-)$')
    ax2.set_ylim((0, 10.5))
    ax2.set_ylabel(r'$\sigma$ (nb)', fontsize=20)
    ax2.legend()

    fig.tight_layout()

    for ext in ['pdf', 'png', 'svg']:
        plt.savefig(f'plots/rplot.{ext}')

    # handles, labels = ax1.get_legend_handles_labels() # return lines and labels
    # interactive_legend = mpld3.plugins.InteractiveLegendPlugin(
    #     zip(handles, ax1.collections), labels, alpha_unsel=0.5, alpha_over=1.5, start_visible=True)
    # mpld3.plugins.connect(fig, interactive_legend)

    # html = mpld3.fig_to_html(fig, figid='rplot', d3_url=d3url(), mpld3_url=mpld3url())
    # html = re.sub(r'(\d+\.\d{4})\d+', r'\1', html)
    # html = re.sub(r'el\d+(\d{5})', 'el' + r'\1', html)

    # with open('plots/rplot.html', 'w') as ofile:
        # ofile.write(html)

    plt.show()

def main():
    lo, hi = 2, 7
    rplot(measurements_in_range(lo, hi), lo=lo, hi=hi, deltaE=0.02, deltaSigma=2)

if __name__ == '__main__':
    main()
