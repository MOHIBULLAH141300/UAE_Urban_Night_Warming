"""Additional urban night-time warming implied by continued built-up growth to 2050.

The observed response is a trend (degC/decade, 1995-2024) regressed on the built-up
increment over the same period, so b * 3.0 decades = k, the accumulated extra warming per
10 percentage points of built-up gain. k is pace-independent under the assumption that the
response scales with the increment rather than its rate; that assumption is stated in the
text and is the main caveat on this calculation.

The central estimate uses the SURFACE (night LST) coefficient, which is estimated from
75,528 pixels and is tightly bounded. The station air-temperature response on the same
5 km predictor is about twice as large but rests on six stations, so it is reported as an
upper bound rather than used for the projection: the numbers below are conservative.

Built-up scenarios extrapolate the GHS-BUILT-S 2010-2025 rate to 2050 (S-high) and half
that rate (S-low), capped at the 99th percentile of observed plan-area fraction.
"""
import numpy as np, pandas as pd, json
from scipy.signal import fftconvolve

DEC = (2024 - 1995 + 1) / 10.0
d = np.load('layers.npz'); u = (d['uae'] & d['land'])
KX = 0.00898*111.32*np.cos(np.deg2rad(24.5)); KY = 0.00898*110.57; CELL = KX*KY
lat = d['lat']; lon = d['lon']
lat = lat if lat.ndim == 1 else lat[:, 0]
lon = lon if lon.ndim == 1 else lon[0, :]
sc = json.load(open('scale_v2.json'))
b, blo, bhi = sc['tn']['nbhd5km'][:3]
k, klo, khi = b * DEC, blo * DEC, bhi * DEC
air_ratio = sc['air_over_surface']
out = dict(period_decades=DEC, b_surface=[b, blo, bhi], k_surface=[k, klo, khi],
           air_over_surface=air_ratio, station_slope_p=sc['station']['p'])
print('surface k = %.2f degC per 10 pp built-up (95%% CI %.2f-%.2f)' % (k, klo, khi))
print('station air response is %.1fx the surface response (n=6, p=%.2f): treated as an upper bound\n'
      % (air_ratio, sc['station']['p']))

b10, b25 = d['bf2010'], d['bf2025']
rate = (b25 - b10) / 15.0
cap = float(np.nanpercentile(d['bf2025'][u & (d['bf2025'] > 0.05)], 99))
out['cap'] = cap
yy, xx = np.mgrid[-5:6, -5:6]
ker = ((yy ** 2 + xx ** 2) <= 25).astype(float); ker /= ker.sum()
scen = {}
for nm, mult in [('S-high', 1.0), ('S-low', 0.5)]:
    b50 = np.clip(b25 + mult * rate * 25.0, 0, cap)
    scen[nm] = fftconvolve(np.nan_to_num(b50 - b25), ker, mode='same')
    out[nm + '_km2_2050'] = float(np.nansum(b50[u]) * CELL)
out['km2_1995'] = float(np.nansum(d['bf1995'][u]) * CELL)
out['km2_2020'] = float(np.nansum(d['bf2020'][u]) * CELL)
out['km2_2025'] = float(np.nansum(b25[u]) * CELL)
print('built-up area: %.0f km2 (1995) -> %.0f (2025) -> %.0f (S-high 2050) / %.0f (S-low 2050)'
      % (out['km2_1995'], out['km2_2025'], out['S-high_km2_2050'], out['S-low_km2_2050']))

st = pd.read_csv('station_v2.csv'); full = st[st.n_x >= 29]
rows = []
for _, s in full.iterrows():
    dy = (lat - s.lat) * 111.0
    dx = (lon - s.lon) * 111.0 * np.cos(np.radians(s.lat))
    msk = ((dy[:, None] ** 2 + dx[None, :] ** 2) <= 25.0) & u
    r = dict(name=s['name'], lp2025=float(np.nanmean(b25[msk])), dbf_obs=float(s.dbf5),
             excess=float(s.excess))
    for nm in scen:
        dl = float(np.nanmean(scen[nm][msk]))
        r[nm + '_dlp'] = dl
        r[nm + '_dT'] = dl * 10 * k
        r[nm + '_lo'] = dl * 10 * klo
        r[nm + '_hi'] = dl * 10 * khi
        r[nm + '_air'] = dl * 10 * k * air_ratio
    rows.append(r)
F = pd.DataFrame(rows).sort_values('S-high_dT', ascending=False)
F.to_csv('future_v2.csv', index=False)
print()
print(F[['name', 'lp2025', 'S-high_dlp', 'S-high_dT', 'S-high_lo', 'S-high_hi',
         'S-low_dT', 'S-high_air']].round(2).to_string(index=False))

ar6 = pd.read_csv('ar6_tmin.csv'); mid = ar6[ar6.period == 'mid'].set_index('ssp')['median']
out['ar6_mid'] = {kk: float(v) for kk, v in mid.items()}
top = F.iloc[0]
out['top_city'] = top['name']
out['frac_of_ssp245'] = float(top['S-high_dT'] / mid['ssp245'])
print('\nAR6 mid-century (2041-2060 vs 1995-2014) Tmin change, 28-model median:')
for kk, v in mid.items():
    print('  %-7s %.2f degC; %s adds %.2f (S-high) / %.2f (S-low) = +%.0f%% / +%.0f%%'
          % (kk, v, top['name'], top['S-high_dT'], top['S-low_dT'],
             100 * top['S-high_dT'] / v, 100 * top['S-low_dT'] / v))
json.dump(out, open('future_v2.json', 'w'), indent=1)

# ---- retrospective check: does k reproduce the observed 1995-2024 station excess? ----
chk = []
for _, s in full.iterrows():
    obs = float(s.excess) * DEC
    pred_s = float(s.dbf5) * 10 * k
    chk.append(dict(name=s['name'], dbf5_pp=float(s.dbf5) * 100, obs_total=obs,
                    pred_surface=pred_s, pred_air=pred_s * air_ratio,
                    ratio=obs / pred_s if pred_s > 0 else np.nan))
C = pd.DataFrame(chk).sort_values('obs_total', ascending=False)
C.to_csv('future_check_v2.csv', index=False)
print('\nRetrospective check (total excess warming 1995-2024, degC):')
print(C.round(2).to_string(index=False))
o = json.load(open('future_v2.json'))
o['retro_median_ratio'] = float(np.nanmedian(C.ratio[C.dbf5_pp > 1]))
json.dump(o, open('future_v2.json', 'w'), indent=1)
print('median observed/predicted at stations with >1 pp growth: %.1f' % o['retro_median_ratio'])
