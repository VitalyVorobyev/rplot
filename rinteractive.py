#! /usr/bin/env python

import os
import numpy as np
import matplotlib
matplotlib.rcParams.update({'font.size': 16})
import matplotlib.pyplot as plt
import mpld3
import re

from loaddata import measurements_in_range
from rplot import rplot

def static_js_url():
    return '/static/sct/js'

def d3url():
    return os.path.join(static_js_url(), 'd3.v5.min.js')

def mpld3url():
    return os.path.join(static_js_url(), 'mpld3.v0.5.1.min.js')

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


if __name__ == '__main__':
    interactive_r()
