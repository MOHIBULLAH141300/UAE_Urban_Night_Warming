"""Does the pre-trend reflect conversion beginning before GHS records 5 pp of built-up?

Land clearing, grading and infrastructure precede the built surface that GHS detects, so
dating conversion at a 5 pp crossing may place the true onset inside the pre-window. Here
the dating threshold is swept from 1 to 5 pp while the treatment sample is held fixed
(pixels that eventually gain at least 5 pp from a base below 2%), so only the event date
changes. A dating threshold that yields a flat pre-trend identifies when the surface
actually begins to change.
"""
import numpy as np, pandas as pd, json, statsmodels.api as sm
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
TAU = np.arange(-10, 13)
lat2 = L['lat']; lon2 = L['lon']
lat2 = lat2 if lat2.ndim == 1 else lat2[:, 0]
lon2 = lon2 if lon2.ndim == 1 else lon2[0, :]
COH = [2005, 2010, 2015]

M = {}
for s in np.unique(strata[control]):
    sel = control & (strata == s)
    if sel.sum() >= 20:
        with np.errstate(invalid='ignore'):
            M[s] = np.nanmean(A[:, sel], axis=1)
Md = {}
for s in np.unique(strata[control]):
    sel = control & (strata == s)
    if sel.sum() >= 20:
        with np.errstate(invalid='ignore'):
            Md[s] = np.nanmean(D[:, sel], axis=1)

def curve(V, CM, conv):
    rows, pix = [], []
    for i in np.where(np.isfinite(conv))[0]:
        if conv[i] not in COH or strata[i] not in CM:
            continue
        diff = V[:, i] - CM[strata[i]]
        r = np.full(len(TAU), np.nan)
        for t, dv in zip(years - conv[i], diff):
            k = np.where(TAU == int(t))[0]
            if len(k):
                r[k[0]] = dv
        rows.append(r); pix.append(i)
    S = np.array(rows); pix = np.array(pix)
    pre = (TAU >= -5) & (TAU <= -1)
    with np.errstate(invalid='ignore'):
        base = np.nanmean(S[:, pre], axis=1)
    ok = np.isfinite(base); S = S[ok] - base[ok, None]; pix = pix[ok]
    yy = idx[pix] // nx; xx = idx[pix] % nx
    b = np.floor(lat2[yy] / 0.25).astype(int) * 1000 + np.floor(lon2[xx] / 0.25).astype(int)
    ub = np.unique(b); bi = np.searchsorted(ub, b)
    groups = [np.where(bi == p)[0] for p in range(len(ub))]
    with np.errstate(invalid='ignore'):
        m = np.nanmean(S, axis=0)
    boot = np.full((600, len(TAU)), np.nan)
    for it in range(600):
        sel = np.concatenate([groups[p] for p in rng.integers(0, len(ub), len(ub))])
        with np.errstate(invalid='ignore'):
            boot[it] = np.nanmean(S[sel], axis=0)
    lo = np.nanpercentile(boot, 2.5, axis=0); hi = np.nanpercentile(boot, 97.5, axis=0)
    se = np.maximum((hi - lo) / 3.92, 1e-6)
    pm = (TAU >= -10) & (TAU <= -1); qm = (TAU >= 1) & (TAU <= 10)
    fp = sm.WLS(m[pm], sm.add_constant(TAU[pm].astype(float)), weights=1 / se[pm] ** 2).fit()
    fq = sm.WLS(m[qm], sm.add_constant(TAU[qm].astype(float)), weights=1 / se[qm] ** 2).fit()
    return m, lo, hi, fp, fq, S.shape[0], len(ub)

print(f"{'dating':>8} {'n':>5} {'blocks':>7} {'pre slope':>11} {'pre p':>8} {'post slope':>11} {'post p':>9} {'level 3-10':>11}")
best = None
for thr in (0.01, 0.02, 0.03, 0.05):
    conv = np.full(len(idx), np.nan)
    for j in range(1, len(EPS)):
        e = EPS[j]
        newly = np.isnan(conv) & eligible & (bf[e] - bf[1995] >= thr)
        conv[newly] = e
    m, lo, hi, fp, fq, n, nb_ = curve(A, M, conv)
    lev = float(np.nanmean(m[(TAU >= 3) & (TAU <= 10)]))
    print(f"{thr*100:>6.0f}pp {n:>5} {nb_:>7} {fp.params[1]:>+11.4f} {fp.pvalues[1]:>8.3f}"
          f" {fq.params[1]:>+11.4f} {fq.pvalues[1]:>9.1e} {lev:>+11.3f}")
    if best is None or fp.pvalues[1] > best[1]:
        best = (thr, fp.pvalues[1], m, lo, hi, fp, fq, n, nb_)

thr, pp, m, lo, hi, fp, fq, n, nb_ = best
print(f"\nflattest pre-trend at a {thr*100:.0f} pp dating threshold (p={pp:.3f})")
conv = np.full(len(idx), np.nan)
for j in range(1, len(EPS)):
    e = EPS[j]
    newly = np.isnan(conv) & eligible & (bf[e] - bf[1995] >= thr)
    conv[newly] = e
md, lod, hid, fpd, fqd, nd, nbd = curve(D, Md, conv)
print(f"day at the same dating: pre {fpd.params[1]:+.4f} (p={fpd.pvalues[1]:.3f}), "
      f"post {fqd.params[1]:+.4f} (p={fqd.pvalues[1]:.2f}), level {np.nanmean(md[(TAU>=3)&(TAU<=10)]):+.3f}")
out = dict(dating_threshold_pp=thr*100, n=n, nblocks=nb_,
           night=dict(tau=TAU.tolist(), mean=m.tolist(), lo=lo.tolist(), hi=hi.tolist(),
                      pre_slope=float(fp.params[1]), pre_p=float(fp.pvalues[1]),
                      post_slope=float(fq.params[1]), post_p=float(fq.pvalues[1]),
                      level_3_10=float(np.nanmean(m[(TAU >= 3) & (TAU <= 10)]))),
           day=dict(tau=TAU.tolist(), mean=md.tolist(), lo=lod.tolist(), hi=hid.tolist(),
                    pre_slope=float(fpd.params[1]), pre_p=float(fpd.pvalues[1]),
                    post_slope=float(fqd.params[1]), post_p=float(fqd.pvalues[1]),
                    level_3_10=float(np.nanmean(md[(TAU >= 3) & (TAU <= 10)]))))
json.dump(out, open('event_v4.json', 'w'), indent=1)
pd.DataFrame({'tau': TAU, 'night': m, 'night_lo': lo, 'night_hi': hi,
              'day': md, 'day_lo': lod, 'day_hi': hid}).to_csv('event_v4.csv', index=False)
print('\nnight curve at the chosen dating:')
for t, a_, l, h in zip(TAU, m, lo, hi):
    if t % 2 == 0:
        print(f'   tau {t:+3d}  {a_:+.3f} ({l:+.3f}, {h:+.3f})')
