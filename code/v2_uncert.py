"""Where the uncertainty in the 2050 urban increment comes from.

The projected additional night-time AIR warming for a district is

    dT = dLambda x k x r

where dLambda is the built-up increment to 2050, k the accumulated surface response
per unit built-up (degC per 10 pp) and r the surface-to-air conversion. The three terms
multiply, so a log-variance decomposition gives each one's share of the total spread.

Scenario uncertainty in dLambda is not a sampling distribution; the S-high and S-low
scenarios are treated as the bounds of a uniform range, which is the conventional
way to put a scenario term on the same footing as the statistical ones and is stated
as such in the text.
"""
import numpy as np, pandas as pd, json

sc = json.load(open('scale_v2.json')); fu = json.load(open('future_v3.json'))
F = pd.read_csv('future_v3.csv'); ar6 = pd.read_csv('ar6_tmin.csv')
DEC = 2.9   # 1995 to 2024 endpoints span 29 years

# --- 1. transfer coefficient k -------------------------------------------------------
k, klo, khi = fu['k_surface']
se_k = (khi - klo) / 3.92
cv_k = se_k / k

# --- 2. surface-to-air conversion r --------------------------------------------------
slope, se_slope = sc['station']['slope'], sc['station']['se']
b_surf = sc['tn']['nbhd5km'][0]
r = slope / b_surf
cv_r = se_slope / slope            # the surface term's own error is already in cv_k

# --- 3. built-up growth scenario -----------------------------------------------------
# S-low is half S-high, so ln(dLambda) spans ln 2 across the scenario range
sd_ln_growth = np.log(2.0) / np.sqrt(12)

v_k, v_r, v_g = cv_k ** 2, cv_r ** 2, sd_ln_growth ** 2
tot = v_k + v_r + v_g
share = {'Surface-to-air conversion': v_r / tot,
         'Urban growth scenario': v_g / tot,
         'Dose-response coefficient': v_k / tot}
out = {'cv_k': cv_k, 'cv_r': cv_r, 'sd_ln_growth': sd_ln_growth,
       'shares': share, 'k': [k, klo, khi], 'r': r, 'se_slope': se_slope}
print('relative uncertainty (1 sd):')
print('  dose-response coefficient  %.1f%%' % (100 * cv_k))
print('  surface-to-air conversion  %.1f%%' % (100 * cv_r))
print('  urban growth scenario      %.1f%% (ln-uniform over the S-low to S-high range)'
      % (100 * sd_ln_growth))
print('\nshare of total variance:')
for nm, v in sorted(share.items(), key=lambda x: -x[1]):
    print('  %-28s %.0f%%' % (nm, 100 * v))

# --- 4. total uncertainty on the headline number -------------------------------------
sh = F.set_index('name').loc['Sharjah']
central_surface = sh['S-high_dT']
sd_ln_tot = np.sqrt(tot)
lo = central_surface * r * np.exp(-1.96 * sd_ln_tot)
hi = central_surface * r * np.exp(+1.96 * sd_ln_tot)
out['sharjah'] = {'surface_S_high': float(central_surface),
                  'air_central': float(central_surface * r),
                  'air_lo': float(lo), 'air_hi': float(hi),
                  'sd_ln_total': float(sd_ln_tot)}
print('\nSharjah 2050, S-high:')
print('  surface increment                 %.2f degC' % central_surface)
print('  air increment, central            %.2f degC' % (central_surface * r))
print('  air increment, 95%% interval       %.2f to %.2f degC' % (lo, hi))

# --- 5. for context: the climate-model spread on the background ----------------------
mid = ar6[ar6.period == 'mid'].set_index('ssp')
out['ar6_mid_spread'] = {k_: [float(mid.loc[k_, 'p5']), float(mid.loc[k_, 'median']),
                              float(mid.loc[k_, 'p95'])] for k_ in mid.index}
print('\nAR6 mid-century background, 5-95%% across models:')
for k_ in mid.index:
    print('  %-8s %.2f (%.2f to %.2f)' % (k_, mid.loc[k_, 'median'], mid.loc[k_, 'p5'], mid.loc[k_, 'p95']))
rel = (mid.loc['ssp245', 'p95'] - mid.loc['ssp245', 'p5']) / mid.loc['ssp245', 'median']
out['ar6_ssp245_relative_spread'] = float(rel)
print('  SSP2-4.5 relative spread %.0f%% of the median' % (100 * rel))
json.dump(out, open('uncert_v2.json', 'w'), indent=1)
