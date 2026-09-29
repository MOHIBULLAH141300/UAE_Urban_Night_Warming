"""Event study with bootstrap inference on the pre- and post-conversion slopes.

The earlier version bootstrapped the event-time means but then fitted the pre- and post
slopes by weighted least squares, treating event years as independent. That understates
uncertainty because the event-time means share pixels and are serially dependent. Here the
whole estimation is repeated inside each spatial-block bootstrap replicate: the replicate's
event-time curve is formed and its pre- and post-slopes fitted, so the slope intervals and
p values come from the bootstrap distribution and carry the temporal covariance.

Dating. Conversion is dated at the first GHS epoch at which built-up surface rises 1
percentage point above the 1995 value. That threshold is set a priori as the smallest
increment the product resolves above zero, and therefore the earliest epoch at which the
surface has demonstrably begun to change; clearing and grading precede the built surface a
sensor detects. The 1 to 5 pp sweep is reported as a sensitivity, not as the basis for the
choice.
"""
import numpy as np, pandas as pd, json
from scipy.ndimage import uniform_filter

rng = np.random.default_rng(20260713)
L = np.load('layers.npz'); C = np.load('cci_annual30.npz')
mask = (L['uae'] & L['land']); ny, nx = mask.shape
years = C['years'].astype(int); idx = np.where(mask.reshape(-1))[0]
A = C['night_anom'].reshape(len(years), -1)[:, idx]
D = C['day_anom'].reshape(len(years), -1)[:, idx]
EPS = [1995, 2000, 2005, 2010, 2015, 2020]
bf = {e: L[f'bf{e}'].reshape(-1)[idx] for e in EPS}
dist = L['dist'].reshape(-1)[idx]; emi = np.nan_to_num(L['emi'].reshape(-1)[idx]).astype(int)
smod95 = L['smod1995'].reshape(-1)[idx]; smod20 = L['smod2020'].reshape(-1)[idx]
nb = uniform_filter(np.nan_to_num(L['bf2020']), size=11).reshape(-1)[idx]
control = ((smod95 == 11) & (smod20 == 11) & (bf[2020] < 0.01) & (nb < 0.01)
           & (bf[2020] - bf[1995] < 0.002))
eligible = (bf[2020] - bf[1995] >= 0.05) & (bf[1995] < 0.02)
dbin = np.digitize(dist, [5, 10, 20, 40, 80]); strata = dbin * 10 + emi
TAU = np.arange(-10, 13); COH = [2005, 2010, 2015]
lat2 = L['lat']; lon2 = L['lon']
lat2 = lat2 if lat2.ndim == 1 else lat2[:, 0]
lon2 = lon2 if lon2.ndim == 1 else lon2[0, :]
PRE = (TAU >= -10) & (TAU <= -1); POST = (TAU >= 1) & (TAU <= 10)
LEV = (TAU >= 3) & (TAU <= 10)
NB = 2000

def ctrl_means(V):
    M, n_used = {}, {}
    for s in np.unique(strata[control]):
        sel = control & (strata == s)
        if sel.sum() >= 20:
            with np.errstate(invalid='ignore'):
                M[s] = np.nanmean(V[:, sel], axis=1)
            n_used[s] = int(sel.sum())
    return M, n_used

def slope(x, y):
    ok = np.isfinite(y)
    if ok.sum() < 3:
        return np.nan
    xx = x[ok] - x[ok].mean(); yy = y[ok]
    return float((xx * (yy - yy.mean())).sum() / (xx ** 2).sum())

def build(V, thr):
    conv = np.full(len(idx), np.nan)
    for j in range(1, len(EPS)):
        e = EPS[j]
        newly = np.isnan(conv) & eligible & (bf[e] - bf[1995] >= thr)
        conv[newly] = e
    M, n_used = ctrl_means(V)
    rows, pix = [], []
    for i in np.where(np.isfinite(conv))[0]:
        if conv[i] not in COH or strata[i] not in M:
            continue
        diff = V[:, i] - M[strata[i]]
        r = np.full(len(TAU), np.nan)
        for t, dv in zip(years - conv[i], diff):
            k = np.where(TAU == int(t))[0]
            if len(k):
                r[k[0]] = dv
        rows.append(r); pix.append(i)
    S = np.array(rows); pix = np.array(pix)
    base_win = (TAU >= -5) & (TAU <= -1)
    with np.errstate(invalid='ignore'):
        base = np.nanmean(S[:, base_win], axis=1)
    ok = np.isfinite(base); S = S[ok] - base[ok, None]; pix = pix[ok]
    yy = idx[pix] // nx; xx = idx[pix] % nx
    b = np.floor(lat2[yy] / 0.25).astype(int) * 1000 + np.floor(lon2[xx] / 0.25).astype(int)
    ub = np.unique(b); bi = np.searchsorted(ub, b)
    groups = [np.where(bi == p)[0] for p in range(len(ub))]
    return S, groups, ub, n_used

def estimate(V, thr, nboot=NB):
    S, groups, ub, n_used = build(V, thr)
    with np.errstate(invalid='ignore'):
        m = np.nanmean(S, axis=0)
    est = dict(pre=slope(TAU[PRE].astype(float), m[PRE]),
               post=slope(TAU[POST].astype(float), m[POST]),
               level=float(np.nanmean(m[LEV])))
    bm = np.full((nboot, len(TAU)), np.nan)
    bs = np.full((nboot, 3), np.nan)
    for it in range(nboot):
        sel = np.concatenate([groups[p] for p in rng.integers(0, len(ub), len(ub))])
        with np.errstate(invalid='ignore'):
            mb = np.nanmean(S[sel], axis=0)
        bm[it] = mb
        bs[it] = [slope(TAU[PRE].astype(float), mb[PRE]),
                  slope(TAU[POST].astype(float), mb[POST]),
                  np.nanmean(mb[LEV])]
    def ci(col):
        v = bs[:, col][np.isfinite(bs[:, col])]
        p = 2 * min((v <= 0).mean(), (v >= 0).mean())      # two-sided bootstrap p
        return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5)), float(max(p, 1 / len(v)))
    out = dict(n=int(S.shape[0]), nblocks=int(len(ub)), tau=TAU.tolist(),
               mean=m.tolist(),
               lo=np.nanpercentile(bm, 2.5, axis=0).tolist(),
               hi=np.nanpercentile(bm, 97.5, axis=0).tolist(),
               n_control_strata=len(n_used), n_control_pixels=int(sum(n_used.values())))
    for nm, col in (('pre', 0), ('post', 1), ('level', 2)):
        lo, hi, p = ci(col)
        out[nm + '_slope' if nm != 'level' else 'level'] = est[nm]
        out[nm + '_lo'], out[nm + '_hi'], out[nm + '_p'] = lo, hi, p
    return out

res = {'dating_threshold_pp': 1.0, 'note': 'threshold set a priori; sweep reported as sensitivity'}
for V, lab in ((A, 'night'), (D, 'day')):
    r = estimate(V, 0.01)
    res[lab] = r
    print(f"{lab}: n={r['n']} pixels in {r['nblocks']} blocks; "
          f"controls {r['n_control_pixels']} pixels in {r['n_control_strata']} strata")
    print(f"   pre-slope  {r['pre_slope']:+.4f} degC/yr  (95% {r['pre_lo']:+.4f}, {r['pre_hi']:+.4f})  p={r['pre_p']:.3f}")
    print(f"   post-slope {r['post_slope']:+.4f} degC/yr  (95% {r['post_lo']:+.4f}, {r['post_hi']:+.4f})  p={r['post_p']:.4f}")
    print(f"   level 3-10 {r['level']:+.3f} degC     (95% {r['level_lo']:+.3f}, {r['level_hi']:+.3f})  p={r['level_p']:.4f}")

sweep = []
for thr in (0.01, 0.02, 0.03, 0.05):
    r = estimate(A, thr, nboot=NB)
    sweep.append(dict(thr_pp=thr * 100, n=r['n'], pre=r['pre_slope'], pre_p=r['pre_p'],
                      post=r['post_slope'], post_p=r['post_p'], level=r['level']))
    print(f"sweep {thr*100:.0f} pp: n={r['n']:4d}  pre {r['pre_slope']:+.4f} (p={r['pre_p']:.3f})"
          f"  post {r['post_slope']:+.4f} (p={r['post_p']:.3f})  level {r['level']:+.3f}")
res['sweep'] = sweep
json.dump(res, open('event_v5.json', 'w'), indent=1)
pd.DataFrame({'tau': TAU, 'night': res['night']['mean'], 'night_lo': res['night']['lo'],
              'night_hi': res['night']['hi'], 'day': res['day']['mean'],
              'day_lo': res['day']['lo'], 'day_hi': res['day']['hi']}).to_csv('event_v5.csv', index=False)
