#! /usr/bin/env python

import os
import json
import pandas as pd

DATAPATH = './data'

def get_jsons(exclude=[]):
    for item in os.listdir(DATAPATH):
        if item.endswith('.json'):
            yield os.path.join(DATAPATH, item)

def json_to_df(ijson):
    with open(ijson, 'r') as ij:
        data = json.load(ij)
    return (pd.Series(data['meta']),
            pd.DataFrame(pd.Series(item) for item in data['data']))

def measurements_in_range(lo, hi):
    meas = []
    for meta, df in map(json_to_df, get_jsons()):
        df = df[(df.E > lo) & (df.E < hi)]
        if df.size:
            print(f'{meta.experiment:>16s} {meta.year % 100:02d}: {df.shape[0]:2d} points')
            meas.append([meta, df])
    return sorted(meas, key=lambda x: -x[0].year)

def main():
    measurements_in_range(2, 7)

if __name__ == '__main__':
    main()
