"""Does night-time warming scale with building volume, not just footprint?

Merges the morphometric variables onto the pixel table and fits cluster-robust models
with a built-up-growth x building-height interaction. Height is a 2018 snapshot, so the
interaction is cross-sectional and is reported as such.
"""
import numpy as np, pandas as pd, statsmodels.api as sm, json

d = np.load('layers.npz'); m = np.load('morph.npz')
lat = d['lat']; lon = d['lon']
lat = lat if lat.ndim == 1 else lat[:, 0]
lon = lon if lon.ndim == 1 else lon[0, :]
df = pd.read_pickle('pixels_v2.pkl')

yi = np.abs(df.lat.values[:, None] - lat[None, :]).argmin(1)
xi = np.abs(df.lon.values[:, None] - lon[None, :]).argmin(1)
assert np.allclose(lat[yi], df.lat.values) and np.allclose(lon[xi], df.lon.values)

df['H'] = m['hnet'][yi, xi]            # mean building height where built (m)
df['V'] = m['vol'][yi, xi]             # building volume per unit ground area (m3 m-2)
df['lp'] = d['bf2020'][yi, xi]         # plan area fraction 2020
df['H'] = df['H'].fillna(0.0); df['V'] = df['V'].fillna(0.0)

def reg(dd, var, terms):
    X = pd.get_dummies(dd[['dbin', 'emi']].astype(str), drop_first=True).astype(float)
    X['dbf'] = dd.dbf * 10; X['b0'] = dd.b0 * 10; X['lat'] = dd.lat; X['lon'] = dd.lon
    for t in terms: X[t] = dd[t]
    return sm.OLS(dd[var], sm.add_constant(X)).fit(cov_type='cluster', cov_kwds={'groups': dd.blk})

dd = df.dropna(subset=['tn', 'td', 'en', 'dbf', 'b0', 'H']).copy()
dd['H10'] = dd.H / 10.0
dd['dbfH'] = dd.dbf * 10 * dd.H10
dd['V10'] = dd.V / 10.0
out = {'n': int(len(dd))}
print('n =', len(dd))
for var, lab in [('tn', 'night LST'), ('td', 'day LST'), ('en', 'ERA5-Land Tmin')]:
    f = reg(dd, var, ['H10', 'dbfH']); ci = f.conf_int()
    out[var + '_int'] = {k: [float(f.params[k]), float(ci.loc[k, 0]), float(ci.loc[k, 1]), float(f.pvalues[k])]
                         for k in ['dbf', 'H10', 'dbfH']}
    g = reg(dd, var, ['V10']); cg = g.conf_int()
    out[var + '_vol'] = {k: [float(g.params[k]), float(cg.loc[k, 0]), float(cg.loc[k, 1]), float(g.pvalues[k])]
                         for k in ['dbf', 'V10']}
    print(f'{lab:15s} dbf {f.params["dbf"]:+.3f}  H10 {f.params["H10"]:+.3f}  dbf:H {f.params["dbfH"]:+.3f} '
          f'(p={f.pvalues["dbfH"]:.1e}) | volume model: dbf {g.params["dbf"]:+.3f} V10 {g.params["V10"]:+.3f} '
          f'(p={g.pvalues["V10"]:.1e})')

# dose-response by height class among growing pixels
gro = dd[(dd.dbf > 0.02) & (dd.H > 0)].copy()
edges = [0, 5, 10, 1e9]; labs = ['<5 m', '5-10 m', '>=10 m']
gro['hc'] = pd.cut(gro.H, edges, labels=labs)
rows = []
for c in labs:
    s = gro[gro.hc == c]
    if len(s) < 50: continue
    f = reg(s, 'tn', []); ci = f.conf_int()
    rows.append(dict(cls=c, n=int(len(s)), H=float(s.H.median()), lp=float(s.lp.median()),
                     slope=float(f.params['dbf']), lo=float(ci.loc['dbf', 0]), hi=float(ci.loc['dbf', 1])))
out['height_classes'] = rows
print(pd.DataFrame(rows).round(3).to_string(index=False))
out['morph_summary'] = {k: [float(np.nanpercentile(dd[k][dd.lp > 0.05], q)) for q in (25, 50, 75, 95)]
                        for k in ['H', 'V', 'lp']}
json.dump(out, open('morph_v2.json', 'w'), indent=1)
df.to_pickle('pixels_v2.pkl')

# --- is the negative height interaction just saturation of already-built cells? ---
extra = {}
dd['b0dbf'] = dd.b0 * 10 * dd.dbf * 10
f = reg(dd, 'tn', ['H10', 'dbfH', 'b0dbf']); ci = f.conf_int()
extra['tn_sat'] = {k: [float(f.params[k]), float(ci.loc[k, 0]), float(ci.loc[k, 1]), float(f.pvalues[k])]
                   for k in ['dbf', 'H10', 'dbfH', 'b0dbf']}
print('with b0 x dbf: dbf %+.3f H10 %+.3f dbf:H %+.3f (p=%.2g) b0:dbf %+.3f (p=%.2g)'
      % (f.params['dbf'], f.params['H10'], f.params['dbfH'], f.pvalues['dbfH'],
         f.params['b0dbf'], f.pvalues['b0dbf']))
fr = dd[dd.b0 < 0.10]
g = reg(fr, 'tn', ['H10', 'dbfH']); cg = g.conf_int()
extra['tn_frontier'] = {k: [float(g.params[k]), float(cg.loc[k, 0]), float(cg.loc[k, 1]), float(g.pvalues[k])]
                        for k in ['dbf', 'H10', 'dbfH']}
extra['tn_frontier_n'] = int(len(fr))
print('frontier only (b0<0.10, n=%d): dbf %+.3f H10 %+.3f (p=%.2g) dbf:H %+.3f (p=%.2g)'
      % (len(fr), g.params['dbf'], g.params['H10'], g.pvalues['H10'], g.params['dbfH'], g.pvalues['dbfH']))
o = json.load(open('morph_v2.json')); o.update(extra); json.dump(o, open('morph_v2.json', 'w'), indent=1)
