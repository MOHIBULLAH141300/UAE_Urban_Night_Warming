"""Projection rebased on observation-supported GHS epochs only.

GHS-BUILT-S R2023A is derived from Landsat and a 2018 Sentinel-2 composite, so epochs
after 2020 are not observation-supported. The baseline is therefore the 2020 epoch and
the growth rate is taken from 2010-2020. The earlier 2010-2025 version is retained as a
sensitivity test.
"""
import numpy as np, pandas as pd, json
from scipy.signal import fftconvolve

DEC = 2.9   # 1995 to 2024 endpoints span 29 years
d = np.load('layers.npz'); u = (d['uae'] & d['land'])
KX = 0.00898*111.32*np.cos(np.deg2rad(24.5)); KY = 0.00898*110.57; CELL = KX*KY
lat = d['lat']; lon = d['lon']
lat = lat if lat.ndim == 1 else lat[:, 0]
lon = lon if lon.ndim == 1 else lon[0, :]
sc = json.load(open('scale_v2.json'))
b, blo, bhi = sc['tn']['nbhd5km'][:3]
k, klo, khi = b*DEC, blo*DEC, bhi*DEC
ratio = sc['air_over_surface']

yy, xx = np.mgrid[-5:6, -5:6]
ker = ((yy**2 + xx**2) <= 25).astype(float); ker /= ker.sum()
cap = float(np.nanpercentile(d['bf2020'][u & (d['bf2020'] > 0.05)], 99))

def build(base, rate_per_yr, years, mult):
    b50 = np.clip(base + mult*rate_per_yr*years, 0, cap)
    return fftconvolve(np.nan_to_num(b50 - base), ker, mode='same'), b50

VARIANTS = {
    'primary (2010-2020 rate, 2020 base, to 2050)':
        dict(base=d['bf2020'], rate=(d['bf2020'] - d['bf2010'])/10.0, years=30, b0='bf2020'),
    'sensitivity (2005-2020 rate, 2020 base, to 2050)':
        dict(base=d['bf2020'], rate=(d['bf2020'] - d['bf2005'])/15.0, years=30, b0='bf2020'),
    'sensitivity (2010-2025 rate, 2025 base, to 2050)':
        dict(base=d['bf2025'], rate=(d['bf2025'] - d['bf2010'])/15.0, years=25, b0='bf2025'),
}

st = pd.read_csv('station_v2.csv'); full = st[st.n >= 29] if 'n' in st else st[st.n_x >= 29]
out = {'k_surface': [k, klo, khi], 'cap': cap, 'air_over_surface': ratio}
tables = {}
for nm, v in VARIANTS.items():
    res = {}
    for s_nm, mult in [('S-high', 1.0), ('S-low', 0.5)]:
        dl, b50 = build(v['base'], v['rate'], v['years'], mult)
        res[s_nm] = dl
        res[s_nm + '_km2'] = float(np.nansum(b50[u])*CELL)
    rows = []
    for _, s in full.iterrows():
        dy = (lat - s.lat)*111.0; dx = (lon - s.lon)*111.0*np.cos(np.radians(s.lat))
        msk = ((dy[:, None]**2 + dx[None, :]**2) <= 25.0) & u
        r = dict(name=s['name'])
        for s_nm in ('S-high', 'S-low'):
            dl = float(np.nanmean(res[s_nm][msk]))
            r[s_nm + '_dlp'] = dl*100
            r[s_nm + '_dT'] = dl*10*k
            r[s_nm + '_lo'] = dl*10*klo
            r[s_nm + '_hi'] = dl*10*khi
        rows.append(r)
    T = pd.DataFrame(rows).sort_values('S-high_dT', ascending=False)
    tables[nm] = T
    out[nm] = dict(km2_S_high=res['S-high_km2'], km2_S_low=res['S-low_km2'],
                   rows=T.to_dict('records'))
    print(f'\n=== {nm}')
    print(f"  built-up 2050: {res['S-high_km2']:.0f} km2 (S-high), {res['S-low_km2']:.0f} (S-low)")
    print(T[['name', 'S-high_dlp', 'S-high_dT', 'S-high_lo', 'S-high_hi', 'S-low_dT']].round(2).to_string(index=False))

out['km2_2010'] = float(np.nansum(d['bf2010'][u])*CELL)
out['km2_2020'] = float(np.nansum(d['bf2020'][u])*CELL)
ar6 = pd.read_csv('ar6_tmin.csv'); mid = ar6[ar6.period == 'mid'].set_index('ssp')['median']
out['ar6_mid'] = {kk: float(v) for kk, v in mid.items()}
top = tables['primary (2010-2020 rate, 2020 base, to 2050)'].iloc[0]
print('\nPrimary, top city = %s' % top['name'])
for kk, v in mid.items():
    print('  %-7s %.2f degC; adds %.2f (S-high) / %.2f (S-low) = %.0f%% / %.0f%%'
          % (kk, v, top['S-high_dT'], top['S-low_dT'],
             100*top['S-high_dT']/v, 100*top['S-low_dT']/v))
tables['primary (2010-2020 rate, 2020 base, to 2050)'].to_csv('future_v3.csv', index=False)
json.dump(out, open('future_v3.json', 'w'), indent=1, default=float)

# ---- retrospective check on the 2.9-decade basis -----------------------------------
chk = []
for _, s_ in full.iterrows():
    obs = float(s_.excess) * DEC
    pred = float(s_.dbf5) * 10 * k
    chk.append(dict(name=s_['name'], dbf5_pp=float(s_.dbf5) * 100, obs_total=obs,
                    pred_surface=pred, pred_air=pred * ratio,
                    ratio=obs / pred if pred > 0 else np.nan))
C2 = pd.DataFrame(chk).sort_values('obs_total', ascending=False)
C2.to_csv('future_check_v3.csv', index=False)
print('\nRetrospective check (2.9 decades):')
print(C2.round(2).to_string(index=False))
print('median observed/predicted, >1.5 pp growth: %.2f'
      % C2.ratio[C2.dbf5_pp > 1.5].median())
