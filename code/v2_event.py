"""Matched event study: what happens to night-time LST when desert is built on.

Design. A pixel is treated in the first GHS epoch at which its built-up fraction has risen
at least 5 percentage points above its 1995 value, provided it was essentially unbuilt in
1995 (<2%). Controls are never-built pixels: rural in the Degree of Urbanisation in both
1995 and 2020, below 1% built-up in the pixel and its 10 km neighbourhood, and with no
detectable built-up growth. Each treated pixel is compared with the mean of controls in the
same coastal-distance band and emirate, year by year, which removes the regional signal and
any coastal moderation. Event time is the year minus the conversion epoch.

The test that matters is the pre-trend: if treated and control pixels track one another
before conversion and separate after it, the divergence is attributable to the conversion
rather than to a pre-existing difference between the two groups.

Outputs: event_v2.csv (event-time coefficients with bootstrap intervals), event_v2.json.
"""
import numpy as np, pandas as pd, json

rng = np.random.default_rng(20260713)
L = np.load('layers.npz'); C = np.load('cci_annual30.npz')
mask = (L['uae'] & L['land'])
years = C['years'].astype(int)
A = C['night_anom'].reshape(len(years), -1)           # (t, npix)
D = C['day_anom'].reshape(len(years), -1)
flat = mask.reshape(-1)
idx = np.where(flat)[0]
A = A[:, idx]; D = D[:, idx]

bf = {e: L[f'bf{e}'].reshape(-1)[idx] for e in (1995, 2000, 2005, 2010, 2015, 2020)}
dist = L['dist'].reshape(-1)[idx]
emi = L['emi'].reshape(-1)[idx]
smod95 = L['smod1995'].reshape(-1)[idx]; smod20 = L['smod2020'].reshape(-1)[idx]
from scipy.ndimage import uniform_filter
nb = uniform_filter(np.nan_to_num(L['bf2020']), size=11).reshape(-1)[idx]

EP = [2000, 2005, 2010, 2015, 2020]
THRESH, BASE_MAX = 0.05, 0.02
conv = np.full(len(idx), -1)
for e in EP:
    newly = (conv < 0) & (bf[e] - bf[1995] >= THRESH) & (bf[1995] < BASE_MAX)
    conv[newly] = e
treated = conv > 0
control = ((smod95 == 11) & (smod20 == 11) & (bf[2020] < 0.01) & (nb < 0.01)
           & (bf[2020] - bf[1995] < 0.002))
print('treated pixels %d  (by epoch %s)' % (treated.sum(),
      {e: int((conv == e).sum()) for e in EP}))
print('control pixels %d' % control.sum())

dbin = np.digitize(dist, [5, 10, 20, 40, 80])
emi_i = np.nan_to_num(emi, nan=0).astype(int)
strata = dbin * 10 + emi_i

# ---- control mean per stratum per year -------------------------------------------------
ctrl_mean = {}
for v, nm in ((A, 'n'), (D, 'd')):
    M = {}
    for s in np.unique(strata[control]):
        sel = control & (strata == s)
        if sel.sum() < 20:
            continue
        M[s] = np.nanmean(v[:, sel], axis=1)
    ctrl_mean[nm] = M

# ---- treated minus matched control, by event time --------------------------------------
TAU = np.arange(-10, 13)
COHORTS = [2005, 2010, 2015]        # enough pre- and post-years inside 1995-2024
rows_pix, blk_pix = [], []
blk = (np.floor(L['lat'][:, None] if L['lat'].ndim == 1 else L['lat']).astype(int) * 0)  # placeholder
df_pix = pd.read_pickle('pixels_v2.pkl')

def series(v, nm):
    out = np.full((treated.sum(), len(TAU)), np.nan)
    tre = np.where(treated)[0]
    keep = []
    for r, i in enumerate(tre):
        e = conv[i]
        if e not in COHORTS:
            continue
        s = strata[i]
        if s not in ctrl_mean[nm]:
            continue
        diff = v[:, i] - ctrl_mean[nm][s]
        tau = years - e
        pos = np.searchsorted(TAU, tau)
        ok = (tau >= TAU[0]) & (tau <= TAU[-1])
        out[r, pos[ok]] = diff[ok]
        keep.append(r)
    return out[keep], np.array(keep), tre[keep]

res = {}
for v, nm, lab in ((A, 'n', 'night'), (D, 'd', 'day')):
    S, keep, pix = series(v, nm)
    # normalise each pixel to its mean over tau in [-5, -1]
    pre = (TAU >= -5) & (TAU <= -1)
    base = np.nanmean(S[:, pre], axis=1)
    S = S - base[:, None]
    m = np.nanmean(S, axis=0)
    # block bootstrap over 0.25 deg blocks
    lat2 = L['lat']; lon2 = L['lon']
    lat2 = lat2 if lat2.ndim == 1 else lat2[:, 0]
    lon2 = lon2 if lon2.ndim == 1 else lon2[0, :]
    ny, nx = mask.shape
    yy = idx[pix] // nx; xx = idx[pix] % nx
    b = (np.floor(lat2[yy] / 0.25).astype(int) * 1000 + np.floor(lon2[xx] / 0.25).astype(int))
    ub = np.unique(b); bi = np.searchsorted(ub, b)
    boot = np.full((1000, len(TAU)), np.nan)
    for it in range(1000):
        pick = rng.integers(0, len(ub), len(ub))
        sel = np.concatenate([np.where(bi == p)[0] for p in pick])
        boot[it] = np.nanmean(S[sel], axis=0)
    lo = np.nanpercentile(boot, 2.5, axis=0); hi = np.nanpercentile(boot, 97.5, axis=0)
    res[lab] = dict(tau=TAU.tolist(), mean=m.tolist(), lo=lo.tolist(), hi=hi.tolist(),
                    n=int(S.shape[0]), nblocks=int(len(ub)))
    print(f'\n{lab}: {S.shape[0]} treated pixels in {len(ub)} blocks')
    for t, mm, l, h in zip(TAU, m, lo, hi):
        if t % 2 == 0:
            print(f'   tau {t:+3d}  {mm:+.3f}  ({l:+.3f}, {h:+.3f})')

# ---- pre-trend test --------------------------------------------------------------------
import statsmodels.api as sm
out = {'design': dict(threshold_pp=THRESH * 100, base_max_pp=BASE_MAX * 100,
                      cohorts=COHORTS, n_treated_all=int(treated.sum()),
                      n_control=int(control.sum()))}
for lab in ('night', 'day'):
    m = np.array(res[lab]['mean']); lo = np.array(res[lab]['lo']); hi = np.array(res[lab]['hi'])
    pre = (TAU >= -10) & (TAU <= -1)
    x = sm.add_constant(TAU[pre].astype(float))
    w = 1.0 / np.maximum(((hi - lo) / 3.92)[pre], 1e-6) ** 2
    f = sm.WLS(m[pre], x, weights=w).fit()
    post = (TAU >= 1) & (TAU <= 10)
    xp = sm.add_constant(TAU[post].astype(float))
    wp = 1.0 / np.maximum(((hi - lo) / 3.92)[post], 1e-6) ** 2
    g = sm.WLS(m[post], xp, weights=wp).fit()
    out[lab] = dict(pre_slope=float(f.params[1]), pre_p=float(f.pvalues[1]),
                    post_slope=float(g.params[1]), post_p=float(g.pvalues[1]),
                    post_minus_pre=float(np.nanmean(m[(TAU >= 5) & (TAU <= 10)])),
                    curve=res[lab])
    print(f'\n{lab}: pre-trend slope {f.params[1]:+.4f} degC/yr (p={f.pvalues[1]:.2f});'
          f' post slope {g.params[1]:+.4f} (p={g.pvalues[1]:.1e});'
          f' mean level at tau 5-10 {out[lab]["post_minus_pre"]:+.3f} degC')
json.dump(out, open('event_v2.json', 'w'), indent=1)
pd.DataFrame({'tau': TAU, 'night': res['night']['mean'], 'night_lo': res['night']['lo'],
              'night_hi': res['night']['hi'], 'day': res['day']['mean'],
              'day_lo': res['day']['lo'], 'day_hi': res['day']['hi']}).to_csv('event_v2.csv', index=False)
