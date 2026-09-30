import os,json,numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
H=os.path.expanduser('~'); T=f'{H}/mnt/TEMPERATUTE PAPER A/TEMPERATURE PAPER ONLY/results/'; OUT=f'{H}/ghs/out'
E=json.load(open(T+'event_v5.json')); C=pd.read_csv(T+'event_v5.csv')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.6,'axes.linewidth':0,'axes.titlesize':9.4,
 'axes.titleweight':'bold','savefig.dpi':600,'text.color':'#222222','xtick.color':'#555555','ytick.color':'#555555'})
NIGHT='#a01c30'; DAY='#e8833a'; GREY='#8a8a8a'
fig=plt.figure(figsize=(7.5,3.9))
gs=fig.add_gridspec(1,3,width_ratios=[1,1,0.92],wspace=0.30,left=0.075,right=0.985,top=0.86,bottom=0.30)
def style(ax):
    ax.set_axisbelow(True); ax.yaxis.grid(True,color='#e9e9e9',lw=0.7); ax.xaxis.grid(False)
    for s_ in ax.spines.values(): s_.set_visible(False)
    ax.tick_params(length=0,labelsize=8)
def ev(ax,key,col,title,verdict):
    d=E[key]; tau=np.array(d['tau']); m=np.array(d['mean']); lo=np.array(d['lo']); hi=np.array(d['hi'])
    ax.axvspan(tau.min()-0.6,0,color='#f4f4f4',zorder=0)
    ax.axhline(0,color='#bbbbbb',lw=0.8,zorder=1)
    ax.fill_between(tau,lo,hi,color=col,alpha=0.17,lw=0,zorder=2)
    ax.plot(tau,m,'-',color=col,lw=1.7,zorder=4)
    ax.plot(tau,m,'o',ms=3.2,mfc='white',mec=col,mew=1.1,zorder=5)
    ax.axvline(0,color='#333333',lw=1.1,ls=(0,(3,2)),zorder=3)
    ax.text(0,ax.get_ylim()[1],' conversion',fontsize=7.4,color='#333333',va='top',ha='left')
    ax.text(0.03,0.955,'before',transform=ax.transAxes,fontsize=7.4,color='#9a9a9a',va='top',ha='left')
    pre=np.polyfit(tau[tau<0],m[tau<0],1); post=np.polyfit(tau[tau>0],m[tau>0],1)
    xp=np.array([tau.min(),0.0]); ax.plot(xp,np.polyval(pre,xp),color=GREY,lw=1.2,ls=(0,(4,2)),zorder=6)
    xq=np.array([0.0,tau.max()]); ax.plot(xq,np.polyval(post,xq),color=col,lw=1.4,ls=(0,(4,2)),zorder=6)
    ax.set_xlabel('Years from conversion'); ax.set_title(title,loc='left'); style(ax)
    return d
a=fig.add_subplot(gs[0,0]); b=fig.add_subplot(gs[0,1],sharey=a)
dn=ev(a,'night',NIGHT,'a   Night-time LST',None)
dd=ev(b,'day',DAY,'b   Day-time LST',None)
a.set_ylabel('LST minus matched control (°C)')
plt.setp(b.get_yticklabels(),visible=False)
def box(ax,d,col,head,lines):
    txt=head+'\n'+'\n'.join(lines)
    ax.text(0.03,-0.30,txt,transform=ax.transAxes,fontsize=7.4,va='top',ha='left',color='#333333',linespacing=1.5)
box(a,dn,NIGHT,'Night, n = %d pixels'%dn['n'],
    ['before: %+.3f °C yr⁻¹  (p = %.2f, flat)'%(dn['pre_slope'],dn['pre_p']),
     'after:  %+.3f °C yr⁻¹  (p = %.4f)'%(dn['post_slope'],dn['post_p']),
     'step at 3–10 yr: %+.2f °C (%.2f–%.2f)'%(dn['level'],dn['level_lo'],dn['level_hi'])])
box(b,dd,DAY,'Day, n = %d pixels'%dd['n'],
    ['before: −%.3f °C yr⁻¹  (p = %.2f)'%(abs(dd['pre_slope']),dd['pre_p']),
     'after:  %+.3f °C yr⁻¹  (p = %.2f, not resolved)'%(dd['post_slope'],dd['post_p']),
     'step at 3–10 yr: %+.2f °C (p = %.2f)'%(dd['level'],dd['level_p'])])
# c: dating sensitivity
c=fig.add_subplot(gs[0,2]); S=E['sweep']
x=[s['thr_pp'] for s in S]; lev=[s['level'] for s in S]; ok=[s['pre_p']>=0.05 for s in S]
c.axhline(0,color='#bbbbbb',lw=0.8)
c.plot(x,lev,'-',color=NIGHT,lw=1.4,zorder=2)
for xi,li,o,s in zip(x,lev,ok,S):
    c.plot(xi,li,'o',ms=9,mfc=NIGHT if o else 'white',mec=NIGHT,mew=1.6,zorder=3)
    c.text(xi,li+0.045,'%.2f'%li,ha='center',fontsize=7.6,color=NIGHT,fontweight='bold')
c.set_ylim(0,1.02); c.set_xticks(x); c.set_xticklabels(['%g'%v for v in x],fontsize=8)
c.text(0.5,0.04,'treated pixels: '+', '.join(str(s2['n']) for s2 in S),transform=c.transAxes,ha='center',fontsize=7.2,color='#888888')
c.set_xlabel('Built-up threshold used to date conversion (pp)')
c.set_ylabel('Night step at 3–10 yr (°C)')
c.set_title('c   Dating sensitivity',loc='left'); style(c)
c.legend(handles=[Line2D([0],[0],marker='o',color='none',mfc=NIGHT,mec=NIGHT,mew=1.6,ms=7,label='parallel trends hold (pre-slope p ≥ 0.05)'),
                  Line2D([0],[0],marker='o',color='none',mfc='white',mec=NIGHT,mew=1.6,ms=7,label='pre-trend present — assumption violated')],
         loc='upper left',bbox_to_anchor=(-0.02,-0.20),frameon=False,fontsize=7.2,labelspacing=0.35,handlelength=1.2)
c.text(1.0,0.995,'1 pp: chosen a priori',fontsize=7.2,color='#666666',ha='left',va='top')
fig.savefig(f'{OUT}/Figure5.png',dpi=600,bbox_inches='tight'); fig.savefig(f'{OUT}/Figure5.pdf',bbox_inches='tight')
print('ok')
