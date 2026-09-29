import json, numpy as np, pandas as pd, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 7.5, 'axes.linewidth': 0.6,
                     'axes.titlesize': 8, 'axes.titleweight': 'bold', 'savefig.dpi': 300})
MO = json.load(open('morph_v2.json')); FU = json.load(open('future_v3.json'))
F = pd.read_csv('future_v3.csv'); CK = pd.read_csv('future_check_v3.csv')
RG = json.load(open('reg_v2.json'))
short = {'Ras Al Khaimah': 'RAK', 'Dubai': 'DXB', 'Sharjah': 'SHJ', 'Fujairah': 'FJR',
         'Abu Dhabi': 'AUH', 'Al Ain': 'AAN'}
fig, ax = plt.subplots(1, 2, figsize=(13.0 / 2.54, 7.0 / 2.54))

# (a) dose-response by building-height class
a = ax[0]; hc = MO['height_classes']
x = np.arange(len(hc))
v = [h['slope'] for h in hc]
lo = [h['slope'] - h['lo'] for h in hc]; hi = [h['hi'] - h['slope'] for h in hc]
a.bar(x, v, 0.6, color=['#fdd0a2', '#fd8d3c', '#d94801'], edgecolor='k', lw=0.4)
a.errorbar(x, v, yerr=[lo, hi], fmt='none', ecolor='k', lw=0.8, capsize=2.5)
a.axhline(RG['tn_base']['dbf'], color='#2166ac', ls='--', lw=0.9)
a.text(2.42, RG['tn_base']['dbf'] + 0.02, 'all pixels', fontsize=7, color='#2166ac', ha='right')
a.set_xticks(x); a.set_xticklabels([h['cls'].replace('>=', '\u2265').replace('-', '\u2013') for h in hc])
for i, h in enumerate(hc): a.text(i, 0.015, f"n={h['n']}", ha='center', fontsize=6.5, color='0.25')
a.set_xlabel('Mean building height (2018)')
a.set_ylabel('Night LST trend per 10 pp\nbuilt-up added (°C decade⁻¹)')
a.set_title('a  Height and the response', loc='left')
a.axhline(0, color='k', lw=0.5); a.spines[['top', 'right']].set_visible(False)

# (c) retrospective check
a = ax[1]
a.plot([0, 3.8], [0, 3.8], 'k--', lw=0.8)
a.scatter(CK.pred_surface, CK.obs_total, s=34, c='#b2182b', edgecolor='k', lw=0.4, zorder=3)
for _, r in CK.iterrows():
    a.annotate(short[r['name']], (r.pred_surface, r.obs_total), textcoords='offset points',
               xytext=(5, -2), fontsize=6.5)
a.axhline(0, color='0.6', lw=0.5)
a.set_xlabel('Predicted from built-up growth (°C)')
a.set_ylabel('Observed excess warming\n1995–2024 (°C)')
a.set_title('b  Retrospective check', loc='left')
a.set_xlim(0, 2.3); a.set_ylim(-0.8, 4.1)
a.spines[['top', 'right']].set_visible(False)
plt.tight_layout(w_pad=2.2); plt.savefig('figs/FigureS3.png'); plt.close()
print('Figure8 written')
