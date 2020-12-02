#! /usr/bin/env python

x0 =  78.24
x1 = 389.70
delta = x1 - x0

dots = [
    ['lambda', 1.116       , 'uds'],
    ['sigma_minus', 1.197  , 'dds'],
    ['sigma_plus', 1.189   , 'uus'],
    ['xi_zero', 1.315      , 'uss'],
    ['xi_minus', 1.321     , 'dss'],
]

for name, mass, quarks in dots:
    print(f'{name:>15s} ({quarks}): {2*mass:.3f}: {x0 + delta * (2*mass - 2):.2f}')
