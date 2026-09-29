"""Put the station (air) and pixel (surface) dose-responses on the same predictor.

The station regression uses the built-up increment averaged over a 5 km radius, the pixel
regression uses the pixel's own increment. Smoothing the predictor changes the slope, so
the two are not comparable as they stand. Here the 5 km neighbourhood increment is
computed on the grid and the pixel model refitted on it.
"""
import numpy as np, pandas as pd, statsmodels.api as sm, json
from scipy.ndimage import uniform_filter

d = np.load('layers.npz'); u = d['uae'].astype(bool)
lat = d['lat']; lon = d['lon']
lat = lat if lat.ndim == 1 else lat[:, 0]
lon = lon if lon.ndim == 1 else lon[0, :]
dlp = np.nan_to_num(d['bf2020'] - d['bf1995'])
# 5 km radius ~ 5 cells at ~1 km; circular kernel
yy, xx = np.mgrid[-5:6, -5:6]
ker = ((yy ** 2 + xx ** 2) <= 25).astype(float); ker /= ker.sum()
from scipy.signal import fftconvolve
dlp5 = fftconvolve(dlp, ker, mode='same')

df = pd.read_pickle('pixels_v2.pkl')
yi = np.abs(df.lat.values[:, None] - lat[None, :]).argmin(1)
xi = np.abs(df.lon.values[:, None] - lon[None, :]).argmin(1)
df['dbf5'] = dlp5[yi, xi]

def reg(dd, var, key):
    X = pd.get_dummies(dd[['dbin', 'emi']].astype(str), drop_first=True).astype(float)
    X[key] = dd[key] * 10; X['b0'] = dd.b0 * 10; X['lat'] = dd.lat; X['lon'] = dd.lon
    f = sm.OLS(dd[var], sm.add_constant(X)).fit(cov_type='cluster', cov_kwds={'groups': dd.blk})
    ci = f.conf_int()
    return float(f.params[key]), float(ci.loc[key, 0]), float(ci.loc[key, 1]), float(f.pvalues[key])

dd = df.dropna(subset=['tn', 'td', 'en', 'dbf', 'dbf5', 'b0'])
out = {}
for var, lab in [('tn', 'night LST'), ('td', 'day LST'), ('en', 'ERA5-Land Tmin')]:
    a = reg(dd, var, 'dbf'); b = reg(dd, var, 'dbf5')
    out[var] = {'pixel': a, 'nbhd5km': b}
    print('%-15s pixel %+.3f (%.3f,%.3f)   5 km mean %+.3f (%.3f,%.3f)'
          % (lab, a[0], a[1], a[2], b[0], b[1], b[2]))

st = pd.read_csv('station_v2.csv'); full = st[st.n_x >= 29]
from scipy import stats
sl, ic, r, p, se = stats.linregress(full.dbf5.values * 10, full.excess.values)
rho, prho = stats.spearmanr(st.dbf5.values, st.excess.values)
out['station'] = dict(slope=float(sl), se=float(se), r=float(r), p=float(p), n=int(len(full)),
                      spearman_all7=[float(rho), float(prho)])
print('station air     slope %+.3f +- %.3f  (r=%.2f, p=%.3f, n=%d); Spearman all 7: rho=%.2f p=%.3f'
      % (sl, se, r, p, len(full), rho, prho))
ratio = sl / out['tn']['nbhd5km'][0]
out['air_over_surface'] = float(ratio)
print('air / surface response on the same 5 km predictor: %.2f' % ratio)
np.savez_compressed('dlp5.npz', dlp5=dlp5)
json.dump(out, open('scale_v2.json', 'w'), indent=1)
df.to_pickle('pixels_v2.pkl')
