import json, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 7.5, 'axes.linewidth': 0.6,
                     'axes.titlesize': 8, 'axes.titleweight': 'bold', 'savefig.dpi': 300})
U = json.load(open('uncert_v2.json'))
fig, ax = plt.subplots(1, 3, figsize=(17.4 / 2.54, 6.4 / 2.54))

# (a) relative uncertainty of each term
a = ax[0]
terms = [('Dose-\nresponse', U['cv_k']), ('Growth\nscenario', U['sd_ln_growth']),
         ('Surface\nto air', U['cv_r'])]
x = np.arange(3)
a.bar(x, [100 * v for _, v in terms], 0.6, color=['#92c5de', '#ef8a62', '#b2182b'],
      edgecolor='k', lw=0.4)
a.set_xticks(x); a.set_xticklabels([t for t, _ in terms])
a.set_ylabel('Relative uncertainty, 1 s.d. (%)')
a.set_title('a  Size of each term', loc='left')
a.spines[['top', 'right']].set_visible(False)

# (b) share of total variance
a = ax[1]
sh = U['shares']
order = ['Surface-to-air conversion', 'Urban growth scenario', 'Dose-response coefficient']
vals = [100 * sh[k] for k in order]
cols = ['#b2182b', '#ef8a62', '#92c5de']
left = 0
for v, c, k in zip(vals, cols, order):
    a.barh(0, v, 0.5, left=left, color=c, edgecolor='k', lw=0.4)
    if v > 6:
        a.text(left + v / 2, 0, f'{v:.0f}%', ha='center', va='center', fontsize=8,
               color='w' if c == '#b2182b' else 'k', weight='bold')
    left += v
a.set_xlim(0, 100); a.set_ylim(-0.6, 0.9); a.set_yticks([])
a.set_xlabel('Percent')
a.set_title('b  Share of total variance', loc='left')
for c, k in zip(cols, order):
    a.bar(np.nan, np.nan, color=c, edgecolor='k', lw=0.4, label=k)
a.legend(frameon=False, fontsize=6.3, loc='upper center', ncol=1, bbox_to_anchor=(0.5, 1.02))
a.spines[['top', 'right', 'left']].set_visible(False)

# (c) the resulting interval, against the background projection
a = ax[2]
sj = U['sharjah']; ar = U['ar6_mid_spread']
a.errorbar([0], [sj['air_central']], yerr=[[sj['air_central'] - sj['air_lo']],
           [sj['air_hi'] - sj['air_central']]], fmt='o', color='#b2182b', ms=6,
           capsize=3, lw=1.0, label='Urban increment, air (Sharjah, S-high)')
a.plot([0.55], [sj['surface_S_high']], 's', color='#ef8a62', ms=6,
       label='Urban increment, surface')
a.plot([0.55, 0.55], [0.97, 1.38], '-', color='#ef8a62', lw=1.0)
for i, (k, lab) in enumerate([('ssp245', 'SSP2-4.5'), ('ssp585', 'SSP5-8.5')]):
    lo, md, hi = ar[k]
    a.errorbar([1.3 + 0.55 * i], [md], yerr=[[md - lo], [hi - md]], fmt='D',
               color='#2166ac', ms=5, capsize=3, lw=1.0)
    a.text(1.3 + 0.55 * i, hi + 0.18, lab, ha='center', fontsize=6.5, color='#2166ac')
a.set_xlim(-0.35, 2.3); a.set_xticks([])
a.set_ylabel('Warming by mid-century (°C)')
a.set_title('c  Against the background', loc='left')
a.legend(frameon=False, fontsize=6.3, loc='upper left')
a.text(1.6, 0.25, 'AR6 background\n(model 5–95%)', ha='center', fontsize=6.3, color='#2166ac')
a.set_ylim(0, 7.0)
a.spines[['top', 'right']].set_visible(False)
plt.tight_layout(w_pad=2.6); plt.savefig('figs/Figure9.png'); plt.close()
print('Figure9 written')
