"""Formal test of slope heterogeneity across satellite sensor eras.

The urban-minus-rural night-time difference series is fitted with a common slope and then
with era-specific slopes, and the two are compared with an F test. A significant result
would mean the apparent difference between era slopes is more than sampling noise.
"""
import numpy as np, pandas as pd, statsmodels.api as sm, statsmodels.formula.api as smf, json

TS = pd.read_csv('ts_v2.csv').dropna(subset=['night_diff'])
def era(y):
    return '1995-2002' if y <= 2002 else ('2003-2011' if y <= 2011 else '2013-2024')
TS['era'] = TS.year.map(era)
TS['t'] = TS.year - TS.year.mean()
out = {}
for var, lab in (('night_diff', 'night'), ('day_diff', 'day')):
    d = TS.dropna(subset=[var]).copy()
    # restricted model allows era-specific LEVELS; the test is on the slopes alone
    r = smf.ols(f'{var} ~ t + C(era)', data=d).fit()
    u = smf.ols(f'{var} ~ t * C(era)', data=d).fit()
    f = u.compare_f_test(r)
    slopes = {}
    for e in sorted(d.era.unique()):
        s = d[d.era == e]
        if len(s) >= 5:
            fe = smf.ols(f'{var} ~ t', data=s).fit()
            slopes[e] = [float(fe.params['t'] * 10), float(fe.bse['t'] * 10), int(len(s))]
    out[lab] = dict(common_slope=float(smf.ols(f'{var} ~ t', data=d).fit().params['t'] * 10), common_se=float(smf.ols(f'{var} ~ t', data=d).fit().bse['t'] * 10),
                    F=float(f[0]), p=float(f[1]), df=int(f[2]), era_slopes=slopes)
    c0 = smf.ols(f'{var} ~ t', data=d).fit()
    print(f'{lab}: common slope {c0.params["t"]*10:+.2f} +- {c0.bse["t"]*10:.2f} degC/decade')
    for e, v in slopes.items():
        print(f'   {e}: {v[0]:+.2f} +- {v[1]:.2f} (n={v[2]})')
    print(f'   slope heterogeneity (levels allowed to differ): F={f[0]:.2f}, p={f[1]:.3f}, df={int(f[2])}\n')
json.dump(out, open('era_v2.json', 'w'), indent=1)
