"""Urban morphology on the analysis grid from GHS-BUILT-H ANBH (100 m, 2018).

Produces, per 1 km analysis cell:
  hnet  mean net building height over the 100 m sub-cells that carry buildings (m)
  f100  fraction of 100 m sub-cells carrying buildings
  vol   mean ANBH over all sub-cells = hnet * f100, a bulk height / volume index (m3 m-2)
  svf   sky-view factor of an idealised regular array (illustrative only; a function of f100)
"""
import numpy as np, rasterio, glob

d = np.load('layers.npz')
lat, lon = d['lat'], d['lon']
lat = lat if lat.ndim == 1 else lat[:, 0]
lon = lon if lon.ndim == 1 else lon[0, :]
ny, nx = len(lat), len(lon)
dy = lat[0] - lat[1]; dx = lon[1] - lon[0]
y_edge = np.concatenate([[lat[0] + dy / 2], lat - dy / 2])      # descending
x_edge = np.concatenate([[lon[0] - dx / 2], lon + dx / 2])      # ascending

hsum = np.zeros((ny, nx)); hcnt = np.zeros((ny, nx)); ncnt = np.zeros((ny, nx))

for f in sorted(glob.glob('ghsh/*.tif')):
    with rasterio.open(f) as r:
        nod = r.nodata
        for j0 in range(0, r.height, 512):
            h = min(512, r.height - j0)
            a = r.read(1, window=((j0, j0 + h), (0, r.width))).astype('f8')
            a[a == nod] = np.nan
            a[a < 0] = np.nan
            rows = np.arange(j0, j0 + h) + 0.5
            cols = np.arange(r.width) + 0.5
            xs, ys = rasterio.transform.xy(r.transform, np.zeros_like(cols), cols)
            _, ys = rasterio.transform.xy(r.transform, rows, np.zeros_like(rows))
            xi = np.searchsorted(x_edge, np.asarray(xs), 'right') - 1
            yi = np.searchsorted(-y_edge, -np.asarray(ys), 'right') - 1
            XI, YI = np.meshgrid(xi, yi)
            ok = (XI >= 0) & (XI < nx) & (YI >= 0) & (YI < ny) & np.isfinite(a)
            np.add.at(ncnt, (YI[ok], XI[ok]), 1)
            np.add.at(hsum, (YI[ok], XI[ok]), a[ok])
            b = ok & (a > 0)
            np.add.at(hcnt, (YI[b], XI[b]), 1)

with np.errstate(invalid='ignore', divide='ignore'):
    hnet = np.where(hcnt > 0, hsum / np.maximum(hcnt, 1), np.nan)
    f100 = np.where(ncnt > 0, hcnt / np.maximum(ncnt, 1), np.nan)
    vol = np.where(ncnt > 0, hsum / np.maximum(ncnt, 1), np.nan)
# idealised regular array of cubes on a square grid: H/W = sqrt(f)/(1-sqrt(f))
s = np.sqrt(np.clip(f100, 0, 0.95)); hw = s / np.maximum(1 - s, 1e-6)
svf = np.sqrt(hw ** 2 + 1) - hw

np.savez_compressed('morph.npz', hnet=hnet, f100=f100, vol=vol, svf=svf, ncnt=ncnt)
u = d['uae'].astype(bool)
m = u & (f100 > 0.02)
print('cells with >2%% built sub-cells: %d' % m.sum())
print('hnet  (m)  p25/50/75/95 %s' % np.round(np.nanpercentile(hnet[m], [25, 50, 75, 95]), 2))
print('vol   (m)  p25/50/75/95 %s' % np.round(np.nanpercentile(vol[m], [25, 50, 75, 95]), 2))
print('f100       p25/50/75/95 %s' % np.round(np.nanpercentile(f100[m], [25, 50, 75, 95]), 3))
print('svf        p25/50/75/95 %s' % np.round(np.nanpercentile(svf[m], [25, 50, 75, 95]), 3))
print('sub-cells per grid cell: median %.0f' % np.nanmedian(ncnt[u]))
