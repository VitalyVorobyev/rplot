#! /usr/bin/env python

import re
import pandas as pd
from datafilter import oplus
from bibinfo import metainfo

linere = re.compile(r"^ *(\d+\.\d+)  *(\d+\.\d+) *(\d+\.\d+) *(\d+\.\d+) *\+(\d+\.\d+) *-(\d+\.\d+) *(\d+\.\d+) *'([\S ]*)' *'([\S ]*)' *\+(\d+\.\d+) *[+-](\d+\.\d+)* '([\S ]*)'$")
systre = re.compile(r"^ *\+(\d+\.\d+) *[+-](\d+\.\d+)* '([\S ]*)'$")

def parse_item(line):
    if line.startswith(('*', "'")):
        return None
    main_item = linere.findall(line)
    if main_item:
        item = list(main_item[0][:-1])
        for i in list(range(7)):
            item[i] = float(item[i])
        for i in [7, 8]:
            item[i] = item[i].strip()
        for i in [9, 10]:
            item[i] = [float(item[i])]
        return ('main', item)

    syst_item = systre.findall(line)
    if not syst_item:
        print(f"Can't parse {line}")
        return None

    item = list(map(float, syst_item[0][:-1]))
    return ('syst', item)

def dat_to_json(fname='rpp2018-hadronicrpp_page1001.dat', lo=2., hi=7.,
         exclude=[]):
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
                for i in [-1, -2]:
                    data[-1][i].append(item[i])

    df = pd.DataFrame(data)
    df.columns = ['Ecm', 'EcmLo', 'EcmHi', 'R', 'statp', 'statn', 'norm', 'code', 'ref', 'systp', 'systn']
    df['norm']  = 0.01 * df.R * df.norm
    df['systp'] = df.apply(lambda x: [0.01 * x.R * item for item in x.systp], axis=1)
    df['systn'] = df.apply(lambda x: [0.01 * x.R * item for item in x.systn], axis=1)
    df['errp']  = df.apply(lambda x: oplus(x.statp, x.norm, *x.systp), axis=1)
    df['errn']  = df.apply(lambda x: oplus(x.statn, x.norm, *x.systn), axis=1)
    df = df[(df.Ecm < hi) & (df.Ecm > lo)]
    df = df[df.apply(lambda x: x.code not in exclude, axis=1)]
    print(df.head(50))
    print(df.shape)
    return df

if __name__ == '__main__':
    dat_to_json()
