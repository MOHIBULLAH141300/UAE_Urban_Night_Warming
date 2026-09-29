"""Event study with a sharp-conversion definition.

The first design dated conversion to the epoch at which cumulative growth first exceeded
5 pp. Because GHS epochs are five years apart and construction is gradual, that dating
smears the treatment and can put genuine conversion inside the pre-window. Here treatment is
restricted to pixels that switch abruptly: essentially unbuilt through the epoch before
conversion, less than 1 pp of growth in every earlier interval, and at least 5 pp gained in
the single interval that defines the event. Conversion is dated to the midpoint of that
interval. If the pre-trend is flat under this definition and a step follows, the divergence
is attributable to the conversion.
"""
import numpy as np, pandas as pd, json, statsmodels.api as sm
from scipy.ndimage import uniform_filter

rng = np.random.default_rng(20260713)
L = np.load('layers.npz'); C = np.load('cci_annual30.npz')
mask = (L['uae'] & L['land']); ny, nx = mask.shape
years = C['years'].astype(int)
idx = np.where(mask.reshape(-1))[0]
A = C['night_anom'].reshape(len(years), -1)[:, idx]
D = C['day_anom'].reshape(len(years), -1)[:, idx]
EPS = [1995, 2000, 2005, 2010, 2015, 2020]
bf = {e: L[f'bf{e}'].reshape(-1)[idx] for e in EPS}
dist = L['dist'].reshape(-1)[idx]; emi = np.nan_to_num(L['emi'].reshape(-1)[idx]).astype(int)
smod95 = L['smod1995'].reshape(-1)[idx]; smod20 = L['smod2020'].reshape(-1)[idx]
nb = uniform_filter(np.nan_to_num(L['bf2020']), size=11).reshape(-1)[idx]

JUMP, QUIET, BASE = 0.05, 0.01, 0.02
conv_mid = np.full(len(idx), np.nan)
for j in range(1, len(EPS)):
    e0, e1 = EPS[j - 1], EPS[j]
    gain = bf[e1] - bf[e0]
    quiet_before = np.ones(len(idx), bool)
    for k in range(1, j):
        quiet_before &= (bf[EPS[k]] - bf[EPS[k - 1]]) < QUIET
    sharp = np.isnan(conv_mid) & (gain >= JUMP) & (bf[e0] < BASE) & quiet_before
    conv_mid[sharp] = (e0 + e1) / 2.0
treated = np.isfinite(conv_mid)
control = ((smod95 == 11) & (smod20 == 11) & (bf[2020] < 0.01) & (nb < 0.01)
           & (bf[2020] - bf[1995] < 0.002))
print('sharp-conversion treated pixels: %d' % treated.sum())
print('  by mid-year:', {int(m): int((conv_mid == m).sum()) for m in np.unique(conv_mid[treated])})

dbin = np.digitize(dist, [5, 10, 20, 40, 80]); strata = dbin * 10 + emi
TAU = np.arange(-10, 13)
lat2 = L['lat']; lon2 = L['lon']
lat2 = lat2 if lat2.ndim == 1 else lat2[:, 0]
lon2 = lon2 if lon2.ndim == 1 else lon2[0, :]

def run(V, nm):
    M = {}
    for s in np.unique(strata[control]):
        sel = control & (strata == s)
        if sel.sum() >= 20:
            with np.errstate(invalid='ignore'):
                M[s] = np.nanmean(V[:, sel], axis=1)
    rowsS, pix = [], []
    for i in np.where(treated)[0]:
        s = strata[i]
        if s not in M:
            continue
        diff = V[:, i] - M[s]
        tau = years - conv_mid[i]
        r = np.full(len(TAU), np.nan)
        for t, dv in zip(tau, diff):
            k = np.where(TAU == int(round(t)))[0]
            if len(k):
                r[k[0]] = dv
        rowsS.append(r); pix.append(i)
    S = np.array(rowsS); pix = np.array(pix)
    pre = (TAU >= -5) & (TAU <= -1)
    with np.errstate(invalid='ignore'):
        base = np.nanmean(S[:, pre], axis=1)
    ok = np.isfinite(base)
    S = S[ok] - base[ok, None]; pix = pix[ok]
    yy = idx[pix] // nx; xx = idx[pix] % nx
    b = np.floor(lat2[yy] / 0.25).astype(int) * 1000 + np.floor(lon2[xx] / 0.25).astype(int)
    ub = np.unique(b); bi = np.searchsorted(ub, b)
    groups = [np.where(bi == p)[0] for p in range(len(ub))]
    with np.errstate(invalid='ignore'):
        m = np.nanmean(S, axis=0)
    boot = np.full((1000, len(TAU)), np.nan)
    for it in range(1000):
        pick = rng.integers(0, len(ub), len(ub))
        sel = np.concatenate([groups[p] for p in pick])
        with np.errstate(invalid='ignore'):
            boot[it] = np.nanmean(S[sel], axis=0)
    lo = np.nanpercentile(boot, 2.5, axis=0); hi = np.nanpercentile(boot, 97.5, axis=0)
    se = (hi - lo) / 3.92
    prem = (TAU >= -10) & (TAU <= -1); postm = (TAU >= 1) & (TAU <= 10)
    fpre = sm.WLS(m[prem], sm.add_constant(TAU[prem].astype(float)),
                  weights=1 / np.maximum(se[prem], 1e-6) ** 2).fit()
    fpost = sm.WLS(m[postm], sm.add_constant(TAU[postm].astype(float)),
                   weights=1 / np.maximum(se[postm], 1e-6) ** 2).fit()
    print(f'\n{nm}: n={S.shape[0]} pixels, {len(ub)} blocks')
    for t, mm, l, h in zip(TAU, m, lo, hi):
        if t % 2 == 0:
            print(f'   tau {t:+3d}  {mm:+.3f} ({l:+.3f}, {h:+.3f})')
    print(f'   pre-trend  {fpre.params[1]:+.4f} degC/yr  p={fpre.pvalues[1]:.3f}')
    print(f'   post-trend {fpost.params[1]:+.4f} degC/yr  p={fpost.pvalues[1]:.2e}')
    step = float(np.nanmean(m[(TAU >= 3) & (TAU <= 10)]))
    print(f'   mean level tau 3-10: {step:+.3f} degC')
    return dict(tau=TAU.tolist(), mean=m.tolist(), lo=lo.tolist(), hi=hi.tolist(),
                n=int(S.shape[0]), nblocks=int(len(ub)),
                pre_slope=float(fpre.params[1]), pre_p=float(fpre.pvalues[1]),
                post_slope=float(fpost.params[1]), post_p=float(fpost.pvalues[1]),
                level_3_10=step)

out = {'design': dict(jump_pp=JUMP*100, quiet_pp=QUIET*100, base_pp=BASE*100,
                      n_treated=int(treated.sum()), n_control=int(control.sum()))}
out['night'] = run(A, 'night')
out['day'] = run(D, 'day')
json.dump(out, open('event_v3.json', 'w'), indent=1)
pd.DataFrame({'tau': TAU, 'night': out['night']['mean'], 'night_lo': out['night']['lo'],
              'night_hi': out['night']['hi'], 'day': out['day']['mean'],
              'day_lo': out['day']['lo'], 'day_hi': out['day']['hi']}).to_csv('event_v3.csv', index=False)
