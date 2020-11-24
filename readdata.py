#! /usr/bin/env python

import re
import numpy as np
import pandas as pd
from datafilter import oplus

linere = re.compile(r"^ *(\d+\.\d+)  *(\d+\.\d+) *(\d+\.\d+) *(\d+\.\d+) *\+(\d+\.\d+) *-(\d+\.\d+) *(\d+\.\d+) *'([\S ]*)' *'([\S ]*)' *\+(\d+\.\d+) *[+-](\d+\.\d+)* '([\S ]*)'$")
systre = re.compile(r"^ *\+(\d+\.\d+) *[+-](\d+\.\d+)* '([\S ]*)'$")

def parse_item(line):
    if line.startswith(('*', "'")):
        return None
    main_item = linere.findall(line)
    if main_item:
        item = list(main_item[0][:-1])
        for i in list(range(7)) + [9, 10]:
            item[i] = float(item[i])
        for i in [7, 8]:
            item[i] = item[i].strip()
        return ('main', item)
    
    syst_item = systre.findall(line)
    if not syst_item:
        print(f"Can't parse {line}")
        return None

    item = list(map(float, syst_item[0][:-1]))
    return ('syst', item)

def read(fname='rpp2018-hadronicrpp_page1001.dat.txt', lo=2., hi=7.,
         exclude=[
            #  'SCHINDLER 79',
            #  'OSTERHELD 86',
            #  'BAI 00C',
            #  'BAI 01',
            # 'RAPIDIS 77',
            'ANASHIN 16A',
             ]):
    with open(fname, 'r') as ifile:
        data = []
        for line in ifile:
            parsed = parse_item(line)
            if not parsed:
                continue
            itype, item = parsed
            if itype == 'main':
                data.append(item)
            else:
                data[-1][-1] = oplus(data[-1][-1], item[-1])
                data[-1][-2] = oplus(data[-1][-2], item[-2])

    df = pd.DataFrame(data)
    df.columns = ['Ecm', 'EcmLo', 'EcmHi', 'R', 'statp', 'statn', 'norm', 'code', 'ref', 'systp', 'systn']
    df['norm'] = df.apply(lambda x: 1 if x.norm < 0.001 else x.norm, axis=1)
    df['errp'] = oplus(df.statp, 0.01*df.R*df.systp, 0.01*df.R*df.norm)
    df['errn'] = oplus(df.statn, 0.01*df.R*df.systn, 0.01*df.R*df.norm)
    df = df[(df.Ecm < hi) & (df.Ecm > lo)]
    df = df[df.apply(lambda x: x.code not in exclude, axis=1)]
    print(df.head())
    print(df.shape)
    return df

def todysh():
    data = np.array([
        #  E      dE    R     stat   syst
        [3076.7, 0.2, 2.188, 0.056, 0.042],
        [3119.6, 0.4, 2.235, 0.042, 0.049],
        [3222.5, 0.8, 2.195, 0.040, 0.035],
        [3314.7, 0.6, 2.219, 0.035, 0.035],
        [3418.3, 0.3, 2.185, 0.032, 0.035],
        [3499.6, 0.4, 2.224, 0.054, 0.040],
        [3520.8, 0.4, 2.201, 0.050, 0.044],
        [3618.2, 1.0, 2.218, 0.038, 0.035],
        [3719.4, 0.7, 2.228, 0.039, 0.042],
    ])
    for E, dE, R, stat, syst in data:
        print(f'{E / 1000:.5f} {(E - dE) / 1000:.5f} {(E + dE) / 1000:.5f} {R:.5f} {stat:.3f} {syst / R * 100:.2f}')

if __name__ == '__main__':
    todysh()
    # read()
