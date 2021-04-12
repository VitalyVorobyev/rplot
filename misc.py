#! /usr/bin/env python

x0 =  58.7
x1 = 292.2
delta = x1 - x0

baryons = [
    ['lambda', 1.116          , 'uds'],
    ['sigma_minus', 1.197     , 'dds'],
    ['sigma_plus', 1.189      , 'uus'],
    ['xi_zero', 1.315         , 'uss'],
    ['xi_minus', 1.321        , 'dss'],
    ['omega_minus', 1.67245   , 'sss'],
    ['lambda_c_minus', 2.28646, 'udc'],
    ['xi_c_plus', 2.46794     , 'usc'],
    ['xi_c_zero', 2.47090     , 'dsc'],
    ['omega_c_zero', 2.6852   , 'ssc'],
]

print('baryons:')
for name, mass, quarks in baryons:
    print(f'{name:>15s} ({quarks}): {2*mass:.3f}: {x0 + delta * (2*mass - 2):.2f}')

charmonium = [
    ['jpsi', 3.096, 92.9e-6],
    ['psi2s', 3.68610, 294e-6],
    ['psi3770', 3.7737, 0.0272],
    ['psi4040', 4.039, 0.080],
    ['psi4160', 4.191, 0.070],
    ['y4230', 4.220, 0.050],
]

print('ccbar:')
for name, mass, width in charmonium:
    print(f'{name:>15s}: {mass:.3f}: {x0 + delta * (mass - 2):.2f}')


print(f'tau: {2*1.77682:.3f}: {x0 + delta * (2*1.77682 - 2):.2f}')
