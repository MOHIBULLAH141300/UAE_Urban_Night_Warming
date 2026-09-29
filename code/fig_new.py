import json, numpy as np, pandas as pd, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7.5,'axes.linewidth':0.6,
                     'axes.titlesize':8,'axes.titleweight':'bold','savefig.dpi':300})

# ---------------- Figure 5: event study ----------------
E = json.load(open('event_v5.json')); tau = np.array(E['night']['tau'])
fig, ax = plt.subplots(1, 3, figsize=(17.4/2.54, 6.2/2.54))
for a, key, col, lab in ((ax[0], 'night', '#b2182b', 'Night LST'),
                         (ax[1], 'day', '#ef8a62', 'Day LST')):
    m = np.array(E[key]['mean']); lo = np.array(E[key]['lo']); hi = np.array(E[key]['hi'])
    a.axvspan(tau[0]-0.5, -0.5, color='0.93', zorder=0)
    a.fill_between(tau, lo, hi, color=col, alpha=0.25, lw=0)
    a.plot(tau, m, '-o', color=col, ms=2.6, lw=1.1)
    a.axhline(0, color='k', lw=0.5); a.axvline(0, color='k', lw=0.8, ls='--')
    a.set_xlabel('Years from conversion'); a.set_ylabel(f'{lab} minus matched control (°C)')
    a.set_title(('a  Night: step after conversion' if key == 'night'
                 else 'b  Day: no step'), loc='left')
    a.text(-8.5, a.get_ylim()[1]*0.88, 'before', fontsize=6.5, color='0.4')
    a.set_xlim(-10.5, 12.5); a.spines[['top','right']].set_visible(False)
    a.text(0.03, 0.03,
           f"pre-slope p = {E[key]['pre_p']:.2f}\npost-slope p = {E[key]['post_p']:.3f}",
           transform=a.transAxes, fontsize=6.4, va='bottom')

a = ax[2]
SW = E['sweep']
thr = [r['thr_pp'] for r in SW]; pre_p = [r['pre_p'] for r in SW]
lev = [r['level'] for r in SW]
a.plot(thr, pre_p, '-o', color='#2166ac', ms=4, label='pre-slope p')
a.axhline(0.05, color='0.5', ls=':', lw=0.9)
a.text(4.6, 0.062, 'p = 0.05', fontsize=6.3, color='0.4', ha='right')
a.set_xlabel('Built-up threshold used to date conversion (pp)')
a.set_ylabel('Pre-slope p value', color='#2166ac')
a.tick_params(axis='y', colors='#2166ac')
a2 = a.twinx()
a2.plot(thr, lev, '-s', color='#b2182b', ms=4)
a2.set_ylabel('Night step at 3–10 yr (°C)', color='#b2182b')
a2.tick_params(axis='y', colors='#b2182b'); a2.set_ylim(0, 1.0)
a.set_title('c  Dating sensitivity', loc='left')
a.set_xticks(thr); a.spines[['top']].set_visible(False); a2.spines[['top']].set_visible(False)
plt.tight_layout(w_pad=2.2); plt.savefig('figs/Figure5.png'); plt.close()
print('Figure5 (event study) written')

# ---------------- Figure 7: projection and its uncertainty ----------------
F = pd.read_csv('future_v3.csv'); U = json.load(open('uncert_v2.json'))
FU = json.load(open('future_v3.json'))
short = {'Ras Al Khaimah':'RAK','Dubai':'DXB','Sharjah':'SHJ','Fujairah':'FJR',
         'Abu Dhabi':'AUH','Al Ain':'AAN'}
fig, ax = plt.subplots(1, 2, figsize=(17.4/2.54, 6.6/2.54),
                       gridspec_kw={'width_ratios': [1.5, 1]})
a = ax[0]; F = F.sort_values('S-high_dT'); y = np.arange(len(F))
a.barh(y+0.19, F['S-high_dT'], 0.36, color='#b2182b', edgecolor='k', lw=0.4,
       label='S-high (2010–2020 rate continued)')
a.errorbar(F['S-high_dT'], y+0.19,
           xerr=[F['S-high_dT']-F['S-high_lo'], F['S-high_hi']-F['S-high_dT']],
           fmt='none', ecolor='k', lw=0.7, capsize=2)
a.barh(y-0.19, F['S-low_dT'], 0.36, color='#ef8a62', edgecolor='k', lw=0.4,
       label='S-low (half that rate)')
for lab, c, ls in (('ssp126','#2166ac',':'), ('ssp245','#053061','--')):
    a.axvline(FU['ar6_mid'][lab], color=c, ls=ls, lw=1.0)
    a.text(FU['ar6_mid'][lab], len(F)-0.3,
           lab.upper().replace('SSP1','SSP1-').replace('SSP2','SSP2-').replace('26','2.6').replace('45','4.5'),
           rotation=90, fontsize=6.3, color=c, va='top', ha='right')
a.set_yticks(y); a.set_yticklabels([short[n] for n in F.name])
a.set_xlabel('Additional night-time surface warming, 2020–2050 (°C)')
a.set_title('a  Implied by continued growth', loc='left')
a.legend(frameon=False, fontsize=6.4, loc='lower right')
a.spines[['top','right']].set_visible(False)

a = ax[1]; sh = U['shares']
order = ['Surface-to-air conversion','Urban growth scenario','Dose-response coefficient']
cols = ['#b2182b','#ef8a62','#92c5de']; left = 0
for k, c in zip(order, cols):
    v = 100*sh[k]
    a.barh(0, v, 0.45, left=left, color=c, edgecolor='k', lw=0.4, label=k)
    if v > 6:
        a.text(left+v/2, 0, f'{v:.0f}%', ha='center', va='center', fontsize=8,
               color='w' if c == '#b2182b' else 'k', weight='bold')
    left += v
a.set_xlim(0, 100); a.set_ylim(-0.75, 0.85); a.set_yticks([])
a.set_xlabel('Share of projection variance (%)')
a.set_title('b  Where the uncertainty sits', loc='left')
a.legend(frameon=False, fontsize=6.3, loc='upper center', bbox_to_anchor=(0.5, 1.03))
a.spines[['top','right','left']].set_visible(False)
plt.tight_layout(w_pad=2.0); plt.savefig('figs/Figure7.png'); plt.close()
print('Figure7 (projection) written')
