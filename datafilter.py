import numpy as np
import pandas as pd

def oplus(*args):
    return np.sqrt(sum(x**2 for x in args))

def joint_same(r1, r2):
    rjoin = r1.copy()
    rjoin.R = (r1.R * r2.statp**2 + r2.R * r1.statp**2) /\
        (r1.statp**2 + r2.statp**2)
    rjoin.systp = [min(oplus(*r1.systp), oplus(*r2.systp))]
    rjoin.systn = [min(oplus(*r1.systn), oplus(*r2.systn))]
    rjoin.corrp = [min(oplus(*r1.corrp), oplus(*r2.corrp))]
    rjoin.corrn = [min(oplus(*r1.corrn), oplus(*r2.corrn))]
    rjoin.statp = 1. / oplus(1. / r1.statp, 1. / r2.statp)
    rjoin.statn = 1. / oplus(1. / r1.statn, 1. / r2.statn)
    rjoin.dRp = oplus(rjoin.statp, *rjoin.systp, *rjoin.corrp)
    rjoin.dRn = oplus(rjoin.statn, *rjoin.systn, *rjoin.corrn)
    return rjoin

def join_records(r1, r2):
    if r1.E == r2.E:
        return joint_same(r1, r2)
    
    elo = r1.E - r1.dEn
    ehi = r2.E + r2.dEp
    emi = 0.5 * (ehi + elo)
    de  = 0.5 * np.abs(ehi - elo)

    if r1.dEp + r1.dEn > 1.e-7 and r2.dEp + r2.dEn > 1.e-7:
        d1 = r1.dEp + r1.dEn
        d2 = r2.dEp + r2.dEn
    else:
        d1 = emi - elo
        d2 = ehi - emi

    d = d1 + d2

    rjoin = r1.copy()
    rjoin.R = (d1*r1.R + d2*r2.R) / d
    rjoin.E, rjoin.dEp, rjoin.dEn = emi, de, de
    rjoin.statp = oplus(d1*r1.statp, d2*r2.statp) / d
    rjoin.statn = oplus(d1*r1.statn, d2*r2.statn) / d
    rjoin.systp = [max(oplus(*r1.systp), oplus(*r2.systp))]
    rjoin.systn = [max(oplus(*r1.systn), oplus(*r2.systn))]
    rjoin.corrp = [max(oplus(*r1.corrp), oplus(*r2.corrp))]
    rjoin.corrn = [max(oplus(*r1.corrn), oplus(*r2.corrn))]
    rjoin.dRp = oplus(rjoin.statp, *rjoin.systp, *rjoin.corrp)
    rjoin.dRn = oplus(rjoin.statn, *rjoin.systn, *rjoin.corrn)
    return rjoin

def compare_items(it1, it2, olist, deltaE, deltaSigma):
    if it2.E - it1.E < deltaE and\
        (it2.R - it1.R) / oplus(it2.statp, it1.statp) < deltaSigma:
        olist.append(join_records(it1, it2))
    else:
        olist.append(it1)
        olist.append(it2)

def rfilter(data, deltaE=0.01, deltaSigma=2):
    new_entries = []
    for i in range(0, data.shape[0]-1, 2):
        compare_items(data.iloc[i], data.iloc[i+1], new_entries, deltaE, deltaSigma)
    if data.shape[0] % 2:
        new_entries.append(data.iloc[-1])
    odata = pd.DataFrame(new_entries)

    new_entries = [odata.iloc[0]]
    for i in range(1, odata.shape[0]-1, 2):
        compare_items(odata.iloc[i], odata.iloc[i+1], new_entries, deltaE, deltaSigma)
    if not odata.shape[0] % 2:
        new_entries.append(odata.iloc[-1])
    odata = pd.DataFrame(new_entries)

    print(f'filter iteration {data.shape} -> {odata.shape}')
    if odata.shape != data.shape:
        return rfilter(odata, deltaE)

    return odata

def main():
    from readpdg import dat_to_df

    df = dat_to_df()
    # df = df[df.code == 'OSTERHELD 86']
    df = df[df.code == 'EDWARDS 90']
    print(df.head(11))
    fdf = rfilter(df, 0.01, 3)
    print(fdf.head(11))

if __name__ == '__main__':
    main()
