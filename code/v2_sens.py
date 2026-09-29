"""Estimator and sub-period sensitivity of the night-time dose-response.

(a) ordinary least squares instead of Theil-Sen, same period 1995-2024
(b) Theil-Sen over 2001-2024 with the 2000-2020 built-up increment
Both are refitted with the same covariates and cluster-robust errors as the main model.
"""
import numpy as np, pandas as pd, statsmodels.api as sm, json

L = np.load('layers.npz'); C = np.load('cci_annual30.npz')
lat = L['lat']; lon = L['lon']
df = pd.read_pickle('pixels_v2.pkl')
yi = np.abs(df.lat.values[:, None] - lat[None, :]).argmin(1)
xi = np.abs(df.lon.values[:, None] - lon[None, :]).argmin(1)
yrs = C['years'].astype(float)

def ols_slope(A, years, minn=20):
    ok = np.isfinite(A)
    n = ok.sum(0)
    x = np.where(ok, years[:, None], np.nan)
    xm = np.nanmean(x, 0); ym = np.nanmean(A, 0)
    sxy = np.nansum((x - xm) * (A - ym), 0); sxx = np.nansum((x - xm) ** 2, 0)
    s = np.where(sxx > 0, sxy / np.maximum(sxx, 1e-9), np.nan) * 10
    s[n < minn] = np.nan
    return s

def sen_slope(A, years, minn=18):
    t = A.shape[0]; i, j = np.triu_indices(t, 1)
    with np.errstate(invalid='ignore'):
        sl = (A[j] - A[i]) / (years[j] - years[i])[:, None]
    s = np.nanmedian(sl, 0) * 10
    s[np.isfinite(A).sum(0) < minn] = np.nan
    return s

def reg(d, var, key='dbf'):
    X = pd.get_dummies(d[['dbin', 'emi']].astype(str), drop_first=True).astype(float)
    X[key] = d[key] * 10; X['b0'] = d.b0 * 10; X['lat'] = d.lat; X['lon'] = d.lon
    f = sm.OLS(d[var], sm.add_constant(X)).fit(cov_type='cluster', cov_kwds={'groups': d.blk})
    ci = f.conf_int()
    return [float(f.params[key]), float(ci.loc[key, 0]), float(ci.loc[key, 1])]

out = {}
# (a) OLS estimator, 1995-2024
sel = (yrs >= 1995) & (yrs <= 2024)
for v, nm in [('night_anom', 'tn'), ('day_anom', 'td')]:
    A = C[v][sel].reshape(sel.sum(), -1)
    df[nm + '_ols'] = ols_slope(A, yrs[sel])[yi * len(lon) + xi]
d = df.dropna(subset=['tn_ols', 'dbf', 'b0'])
out['tn_ols'] = reg(d, 'tn_ols'); out['td_ols'] = reg(d, 'td_ols')
print('OLS estimator      night %+.3f (%.3f, %.3f)   day %+.3f' % (*out['tn_ols'], out['td_ols'][0]))

# (b) 2001-2024 sub-period with the 2000-2020 built-up increment
sel = (yrs >= 2001) & (yrs <= 2024)
for v, nm in [('night_anom', 'tn'), ('day_anom', 'td')]:
    A = C[v][sel].reshape(sel.sum(), -1)
    df[nm + '_01'] = sen_slope(A, yrs[sel])[yi * len(lon) + xi]
dbf01 = np.nan_to_num(L['bf2020'] - L['bf2000'])
df['dbf01'] = dbf01[yi, xi]
d = df.dropna(subset=['tn_01', 'dbf01', 'b0'])
out['tn_2001_2024'] = reg(d, 'tn_01', 'dbf01')
dd = df.dropna(subset=['td_01', 'dbf01', 'b0'])
out['td_2001_2024'] = reg(dd, 'td_01', 'dbf01')
out['n_2001_2024'] = int(len(d))
print('2001-2024 period   night %+.3f (%.3f, %.3f)   day %+.3f  n=%d'
      % (*out['tn_2001_2024'], out['td_2001_2024'][0], len(d)))
json.dump(out, open('sens_v2.json', 'w'), indent=1)
df.to_pickle('pixels_v2.pkl')
