import numpy as np
import pandas as pd

def oplus(*args):
    return np.sqrt(sum(x**2 for x in args))

def joint_same(r1, r2):
    rjoin = r1.copy()
    rjoin.R = (r1.R * r2.statp**2 + r2.R * r1.statp**2) /\
        (r1.statp**2 + r2.statp**2)
    rjoin.systp = min(r1.systp, r2.systp)
    rjoin.systn = min(r1.systn, r2.systn)
    rjoin.statp = 1. / oplus(1. / r1.statp, 1. / r2.statp)
    rjoin.statn = 1. / oplus(1. / r1.statn, 1. / r2.statn)
    rjoin.errp = oplus(rjoin.statp, 0.01*rjoin.R*rjoin.systp, 0.01*rjoin.R*rjoin.norm)
    rjoin.errn = oplus(rjoin.statn, 0.01*rjoin.R*rjoin.systn, 0.01*rjoin.R*rjoin.norm)
    return rjoin

def join_records(r1, r2):
    if r1.Ecm == r2.Ecm:
        return joint_same(r1, r2)
    if r1.EcmHi == r2.EcmLo:
        elo, emi, ehi = r1.EcmLo, r1.EcmHi, r2.EcmHi
    else:
        emi, de = 0.5 * (r1.Ecm + r2.Ecm), 0.5 * np.abs(r2.Ecm - r1.Ecm)
        elo, ehi = emi - de, emi + de

    d1, d2, d = emi-elo, ehi-emi, ehi - elo
    rjoin = r1.copy()
    rjoin.R = (d1*r1.R + d2*r2.R) / d
    rjoin.Ecm, rjoin.EcmLo, rjoin.EcmHi = emi, elo, ehi
    rjoin.systp = max(r1.systp, r2.systp)
    rjoin.systn = max(r1.systn, r2.systn)
    rjoin.statp = oplus(d1*r1.statp, d2*r2.statp) / d
    rjoin.statn = oplus(d1*r1.statn, d2*r2.statn) / d
    rjoin.errp = oplus(rjoin.statp, 0.01 * rjoin.R * rjoin.systp)
    rjoin.errn = oplus(rjoin.statn, 0.01 * rjoin.R * rjoin.systn)
    return rjoin

def rfilter(data, deltaE=0.01, deltaSigma=2):
    new_entries = []
    for i in range(0, data.shape[0]-1, 2):
        deltaR = data.iloc[i+1].R - data.iloc[i].R
        statErr = oplus(data.iloc[i+1].statp, data.iloc[i].statp)
        if data.iloc[i+1].Ecm - data.iloc[i].Ecm < deltaE and deltaR/statErr < deltaSigma:
            new_entries.append(join_records(data.iloc[i], data.iloc[i+1]))
        else:
            new_entries.append(data.iloc[i])
            new_entries.append(data.iloc[i+1])
    if data.shape[0] % 2:
        new_entries.append(data.iloc[-1])

    odata = pd.DataFrame(new_entries)

    new_entries = [odata.iloc[0]]
    for i in range(1, odata.shape[0]-1, 2):
        deltaR = odata.iloc[i+1].R - odata.iloc[i].R
        statErr = oplus(odata.iloc[i+1].statp, odata.iloc[i].statp)
        if odata.iloc[i+1].Ecm - odata.iloc[i].Ecm < deltaE and deltaR/statErr < deltaSigma:
            new_entries.append(join_records(odata.iloc[i], odata.iloc[i+1]))
        else:
            new_entries.append(odata.iloc[i])
            new_entries.append(odata.iloc[i+1])
    if not odata.shape[0] % 2:
        new_entries.append(odata.iloc[-1])

    odata = pd.DataFrame(new_entries)

    print(f'filter iteration {data.shape} -> {odata.shape}')
    if odata.shape != data.shape:
        return rfilter(odata, deltaE)

    return odata

def main():
    from readdata import read

    df = read()
    # df = df[df.code == 'OSTERHELD 86']
    df = df[df.code == 'EDWARDS 90']
    print(df.head(11))
    fdf = rfilter(df, 0.01, 3)
    print(fdf.head(11))

if __name__ == '__main__':
    main()
