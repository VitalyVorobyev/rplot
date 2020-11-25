#! /usr/bin/env python

import os
import json

from datafilter import oplus
from bibinfo import metainfo
from readpdg import dat_to_df

DATAPATH = './data'
def flf(x, decimals=4):
    """ Format floats and list of floats """
    if isinstance(x, float):
        return round(x, decimals)
    elif isinstance(x, list):
        return list(map(flf, x))
    return x

def df_to_json(df, code, ofname):
    meta = metainfo.get(code, None)
    if meta is None:
        print(f'No meta info for {code}')
        return
    odict = {
        'meta': meta,
        'data': [
            {
                'E': item.Ecm,
                'dEp': item.EcmHi - item.Ecm,
                'dEn': item.Ecm - item.EcmLo,
                'R': item.R,
                'dRp': flf(oplus(item.statp, item.norm, *item.systp)),
                'dRn': flf(oplus(item.statn, item.norm, *item.systn)),
                'statp': item.statp,
                'statn': item.statn,
                'systp': flf(item.systp),
                'systn': flf(item.systn),
                'corrp': [flf(item.norm)],
                'corrn': [flf(item.norm)],
            }
            for _, item in df.iterrows()]
    }
    with open(os.path.join(DATAPATH, ofname), 'w') as ofile:
        json.dump(odict, ofile, indent=4)


def process_pdg(lo=0, hi=10000, codes=[]):
    df = dat_to_df(lo=lo, hi=hi)
    for code, data in df.groupby('code'):
        if codes and code not in codes:
            print(f'skipping {code}')
        else:
            ofname = f'{code.replace(" ", "_")}.json'
            print(f'{code}: {ofname}')
            df_to_json(data, code, ofname)


def anashin19(code='Anashin 19', ofname='anashin19.json'):
    data = [
        #  E      dE    R     stat   syst
        [3.0767, 0.0002, 2.188, 0.056, 0.042],
        [3.1196, 0.0004, 2.235, 0.042, 0.049],
        [3.2225, 0.0008, 2.195, 0.040, 0.035],
        [3.3147, 0.0006, 2.219, 0.035, 0.035],
        [3.4183, 0.0003, 2.185, 0.032, 0.035],
        [3.4996, 0.0004, 2.224, 0.054, 0.040],
        [3.5208, 0.0004, 2.201, 0.050, 0.044],
        [3.6182, 0.0010, 2.218, 0.038, 0.035],
        [3.7194, 0.0007, 2.228, 0.039, 0.042],
    ]

    odict = {
        'meta': {
            'code': code,
            'ref': 'Phys. Lett. B 788 (2019) 42',
            'doi': 'https://doi.org/10.1016/j.physletb.2018.11.012',
            'experiment': 'KEDR',
            'year': 2019,
            'comment': '',
        },
        'data': [
            {
                'E': E,
                'dEp': dE,
                'dEn': dE,
                'R': R,
                'dRp': oplus(stat, syst),
                'dRn': oplus(stat, syst),
                'statp': stat,
                'statn': stat,
                'systp': [syst],
                'systn': [syst],
                'corrp': [],
                'corrn': [],
            }
            for E, dE, R, stat, syst in data]
    }
    with open(os.path.join(DATAPATH, ofname), 'w') as ofile:
        json.dump(odict, ofile, indent=4)


def besson07(code='Besson 07', ofname='besson07.json'):
    """ Measurement of the total hadronic cross section in e+e− annihilation below 10.56 GeV
        D. Besson et al. (CLEO Collaboration)
        Phys. Rev. D 76, 072008 – Published 19 October 2007

        At each energy we
        divide the systematic uncertainty into a common uncer-
        tainty that correlated across all energy points and an un-
        correlated uncertainty that is independent for each energy
        point. The decrease of the uncorrelated systematic uncer-
        tainty with decreasing beam energy is mainly due to the
        energy dependence of the two-photon interaction back-
        ground cross section.
    """
    data = [
        #   E      R    stat   common  uncorr
        [10.538, 3.591, 0.003, 0.067, 0.049],
        [10.330, 3.491, 0.006, 0.058, 0.055],
        [ 9.996, 3.497, 0.004, 0.064, 0.043],
        [ 9.432, 3.510, 0.005, 0.066, 0.037],
        [ 8.380, 3.576, 0.024, 0.058, 0.025],
        [ 7.380, 3.550, 0.019, 0.058, 0.020],
        [ 6.964, 3.597, 0.033, 0.057, 0.020],
    ]

    odict = {
        'meta': {
            'code': code,
            'ref': 'Phys. Rev. D 76 (2007) 072008',
            'doi': 'https://doi.org/10.1103/PhysRevD.76.072008',
            'experiment': 'CLEO',
            'year': 2007,
            'comment': '',
        },
        'data': [
            {
                'E': E, 'dEp': 0, 'dEn': 0, 'R': R,
                'dRp': oplus(stat, syst, corr),
                'dRn': oplus(stat, syst, corr),
                'statp': stat,
                'statn': stat,
                'systp': [syst],
                'systn': [syst],
                'corrp': [corr],
                'corrn': [corr],
            }
            for E, R, stat, corr, syst in data]
    }
    with open(os.path.join(DATAPATH, ofname), 'w') as ofile:
        json.dump(odict, ofile, indent=4)


def ablikim06(code='Ablikim 06', ofname='ablikim06.json'):
    data = [
        #  E       R     stat   syst
        [3.6500, 2.186, 0.035, 0.087],
        [3.6600, 2.185, 0.105, 0.087],
        [3.6920, 2.803, 0.092, 0.112],
        [3.7000, 2.240, 0.079, 0.089],
        [3.7080, 2.270, 0.083, 0.091],
        [3.7160, 2.224, 0.086, 0.089],
        [3.7240, 2.164, 0.086, 0.086],
        [3.7320, 2.170, 0.086, 0.087],
        [3.7400, 2.200, 0.099, 0.088],
        [3.7480, 2.380, 0.106, 0.116],
        [3.7500, 2.525, 0.085, 0.123],
        [3.7512, 2.644, 0.090, 0.129],
        [3.7524, 2.622, 0.095, 0.128],
        [3.7536, 2.659, 0.093, 0.130],
        [3.7548, 2.739, 0.093, 0.134],
        [3.7560, 2.591, 0.090, 0.127],
        [3.7572, 2.948, 0.107, 0.144],
        [3.7584, 3.031, 0.108, 0.148],
        [3.7596, 3.082, 0.102, 0.151],
        [3.7608, 3.143, 0.089, 0.154],
        [3.7620, 2.998, 0.110, 0.147],
        [3.7622, 3.213, 0.114, 0.157],
        [3.7634, 3.350, 0.122, 0.164],
        [3.7646, 3.590, 0.126, 0.176],
        [3.7658, 3.386, 0.119, 0.166],
        [3.7670, 3.764, 0.130, 0.184],
        [3.7682, 3.455, 0.124, 0.169],
        [3.7694, 3.615, 0.125, 0.177],
        [3.7706, 3.584, 0.123, 0.175],
        [3.7714, 3.543, 0.139, 0.173],
        [3.7716, 3.638, 0.146, 0.178],
        [3.7718, 3.943, 0.133, 0.193],
        [3.7720, 3.640, 0.134, 0.178],
        [3.7722, 3.656, 0.143, 0.179],
        [3.7726, 3.781, 0.145, 0.185],
        [3.7730, 3.567, 0.120, 0.175],
        [3.7742, 3.377, 0.113, 0.165],
        [3.7754, 3.645, 0.125, 0.178],
        [3.7766, 3.502, 0.119, 0.171],
        [3.7778, 3.574, 0.121, 0.175],
        [3.7790, 3.363, 0.117, 0.165],
        [3.7798, 3.480, 0.136, 0.170],
        [3.7802, 3.430, 0.125, 0.168],
        [3.7804, 3.385, 0.137, 0.166],
        [3.7808, 3.340, 0.129, 0.163],
        [3.7810, 3.468, 0.138, 0.170],
        [3.7812, 3.399, 0.130, 0.166],
        [3.7814, 3.518, 0.124, 0.172],
        [3.7816, 2.947, 0.137, 0.144],
        [3.7818, 3.143, 0.125, 0.154],
        [3.7822, 3.257, 0.124, 0.159],
        [3.7826, 3.329, 0.115, 0.163],
        [3.7838, 3.157, 0.114, 0.155],
        [3.7850, 2.882, 0.107, 0.141],
        [3.7862, 2.905, 0.105, 0.142],
        [3.7874, 2.960, 0.111, 0.145],
        [3.7886, 2.574, 0.097, 0.126],
        [3.7898, 2.579, 0.099, 0.126],
        [3.7900, 2.852, 0.106, 0.140],
        [3.7950, 2.754, 0.101, 0.135],
        [3.8000, 2.215, 0.091, 0.108],
        [3.8100, 2.173, 0.092, 0.087],
        [3.8200, 2.369, 0.109, 0.095],
        [3.8300, 2.355, 0.101, 0.094],
        [3.8400, 2.297, 0.104, 0.092],
        [3.8500, 2.373, 0.115, 0.095],
        [3.8600, 2.372, 0.105, 0.095],
        [3.8720, 2.309, 0.117, 0.092],
    ]
    
    odict = {
        'meta': {
            'code': code,
            'ref': 'Phys. Rev. Lett. 97 (2006) 262001',
            'doi': 'https://doi.org/10.1103/PhysRevLett.97.262001',
            'experiment': 'BES',
            'year': 2006,
            'comment': '',
        },
        'data': [
            {
                'E': E, 'dEp': 0, 'dEn': 0, 'R': R,
                'dRp': oplus(stat, syst),
                'dRn': oplus(stat, syst),
                'statp': stat,
                'statn': stat,
                'systp': [syst],
                'systn': [syst],
                'corrp': [],
                'corrn': [],
            }
            for E, R, stat, syst in data]
    }
    with open(os.path.join(DATAPATH, ofname), 'w') as ofile:
        json.dump(odict, ofile, indent=4)


def ablikim09(code='Ablikim 09', ofname='ablikim09.json'):
    data = [
        # E      R    stat syst
        [2.60, 2.18, 0.02, 0.08],
        [3.07, 2.13, 0.02, 0.07],
        [3.65, 2.14, 0.01, 0.07],
    ]
    odict = {
        'meta': {
            'code': code,
            'ref': 'Phys. Lett. B 677 (2009) 239',
            'doi': 'https://doi.org/10.1016/j.physletb.2009.05.055',
            'experiment': 'BES',
            'year': 2009,
            'comment': '',
        },
        'data': [
            {
                'E': E, 'dEp': 0, 'dEn': 0, 'R': R,
                'dRp': oplus(stat, syst),
                'dRn': oplus(stat, syst),
                'statp': stat,
                'statn': stat,
                'systp': [syst],
                'systn': [syst],
                'corrp': [],
                'corrn': [],
            }
            for E, R, stat, syst in data]
    }
    with open(os.path.join(DATAPATH, ofname), 'w') as ofile:
        json.dump(odict, ofile, indent=4)

def main():
    anashin19()
    besson07()
    ablikim06()
    ablikim09()
    process_pdg()

if __name__ == '__main__':
    main()
