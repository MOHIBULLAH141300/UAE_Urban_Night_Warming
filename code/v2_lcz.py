"""Night and day warming by Local Climate Zone.

LCZ classes (Stewart and Oke, 2012) from the global map of Demuzere et al. (2022), 100 m,
aggregated to the 1 km analysis grid. Each analysis cell is assigned the built LCZ class
(1-10) that occupies most of its built sub-cells, and is analysed when built LCZ classes
cover at least 20% of the cell. Trends are differences from coast-matched rural land, as
elsewhere in the paper, with 95% spatial block-bootstrap intervals.
"""
import numpy as np, pandas as pd, rasterio, json
from rasterio.transform import from_origin

rng = np.random.default_rng(20260713)
L = np.load('layers.npz')
lat, lon = L['lat'], L['lon']
lat = lat if lat.ndim == 1 else lat[:, 0]
lon = lon if lon.ndim == 1 else lon[0, :]
ny, nx = len(lat), len(lon)
df = pd.read_pickle('pixels_v2.pkl')

NAMES = {1: 'Compact high-rise', 2: 'Compact mid-rise', 3: 'Compact low-rise',
         4: 'Open high-rise', 5: 'Open mid-rise', 6: 'Open low-rise',
         7: 'Lightweight low-rise', 8: 'Large low-rise', 9: 'Sparsely built',
         10: 'Heavy industry'}

src = rasterio.open('/mnt/user-data/uploads/ADAM DATA part2/GEE_UAE_urban/'
                    'UAE_LCZ_Demuzere2022_100m_UAE_masked.tif')
dy = lat[0] - lat[1]; dx = lon[1] - lon[0]
y_edge = np.concatenate([[lat[0] + dy / 2], lat - dy / 2])
x_edge = np.concatenate([[lon[0] - dx / 2], lon + dx / 2])

cnt = np.zeros((ny, nx, 11), 'i4'); tot = np.zeros((ny, nx), 'i4')
for j0 in range(0, src.height, 512):
    h = min(512, src.height - j0)
    a = src.read(1, window=((j0, j0 + h), (0, src.width)))
    rows = np.arange(j0, j0 + h) + 0.5; cols = np.arange(src.width) + 0.5
    xs, _ = rasterio.transform.xy(src.transform, np.zeros_like(cols), cols)
    _, ys = rasterio.transform.xy(src.transform, rows, np.zeros_like(rows))
    xi = np.searchsorted(x_edge, np.asarray(xs), 'right') - 1
    yi = np.searchsorted(-y_edge, -np.asarray(ys), 'right') - 1
    XI, YI = np.meshgrid(xi, yi)
    ok = (XI >= 0) & (XI < nx) & (YI >= 0) & (YI < ny) & (a > 0)
    np.add.at(tot, (YI[ok], XI[ok]), 1)
    b = ok & (a >= 1) & (a <= 10)
    np.add.at(cnt, (YI[b], XI[b], a[b].astype(int)), 1)
src.close()

built = cnt[:, :, 1:].sum(2)
with np.errstate(invalid='ignore', divide='ignore'):
    frac = np.where(tot > 0, built / np.maximum(tot, 1), np.nan)
dom = np.where(built > 0, cnt[:, :, 1:].argmax(2) + 1, 0)

yi = np.abs(df.lat.values[:, None] - lat[None, :]).argmin(1)
xi = np.abs(df.lon.values[:, None] - lon[None, :]).argmin(1)
df['lcz'] = dom[yi, xi]
df['lcz_frac'] = frac[yi, xi]

# ---- coast-matched rural difference, same machinery as the dose-response ----
rural = df.rural.values
blks = np.sort(df.blk.unique()); bi = np.searchsorted(blks, df.blk.values); nbk = len(blks)
W = rng.multinomial(nbk, np.ones(nbk) / nbk, size=2000).astype(float)

def SN(sel, var):
    S = np.zeros((nbk, 6)); N = np.zeros((nbk, 6))
    np.add.at(S, (bi[sel], df.dbin.values[sel]), df[var].values[sel])
    np.add.at(N, (bi[sel], df.dbin.values[sel]), 1)
    return S, N

def dfrom(Su, Nu, Sr, Nr):
    ok = (Nu > 0) & (Nr > 0); w = np.where(ok, Nu, 0.); w = w / w.sum(-1, keepdims=True)
    um = np.where(ok, Su / np.where(Nu > 0, Nu, 1), 0); rm = np.where(ok, Sr / np.where(Nr > 0, Nr, 1), 0)
    return (um * w).sum(-1) - (rm * w).sum(-1)

def mdiff(sel, var):
    sel = np.asarray(sel)
    Su, Nu = SN(sel, var); Sr, Nr = SN(rural, var)
    e = dfrom(Su.sum(0), Nu.sum(0), Sr.sum(0), Nr.sum(0))
    b = dfrom(W @ Su, W @ Nu, W @ Sr, W @ Nr)
    return [float(e), float(np.nanpercentile(b, 2.5)), float(np.nanpercentile(b, 97.5)), int(sel.sum())]

MIN_FRAC, MIN_N = 0.20, 40
rows = []
for c in sorted(NAMES):
    sel = (df.lcz == c).values & (df.lcz_frac >= MIN_FRAC).values & np.isfinite(df.tn.values)
    if sel.sum() < MIN_N:
        rows.append(dict(lcz=c, name=NAMES[c], n=int(sel.sum()), note='too few cells'))
        continue
    tn = mdiff(sel, 'tn'); td = mdiff(sel, 'td'); en = mdiff(sel, 'en')
    d = df[sel]
    rows.append(dict(lcz=c, name=NAMES[c], n=int(sel.sum()),
                     dbf=float(100 * d.dbf.mean()), H=float(d.H.mean()), lp=float(d.lp.mean()),
                     tn=tn[0], tn_lo=tn[1], tn_hi=tn[2],
                     td=td[0], td_lo=td[1], td_hi=td[2], en=en[0]))
R = pd.DataFrame(rows)
R.to_csv('lcz_v2.csv', index=False)
keep = R.dropna(subset=['tn'])
print(keep[['lcz', 'name', 'n', 'dbf', 'H', 'tn', 'tn_lo', 'tn_hi', 'td', 'en']].round(2).to_string(index=False))
print()
print('classes dropped for too few cells:',
      [f"{r['name']} (n={r['n']})" for _, r in R[R.n < MIN_N].iterrows()])
out = {'rows': rows, 'min_frac': MIN_FRAC, 'min_n': MIN_N,
       'n_cells_with_built_lcz': int(((df.lcz > 0) & (df.lcz_frac >= MIN_FRAC)).sum())}
json.dump(out, open('lcz_v2.json', 'w'), indent=1)
df.to_pickle('pixels_v2.pkl')
np.savez_compressed('lcz_grid.npz', dom=dom, frac=frac)
