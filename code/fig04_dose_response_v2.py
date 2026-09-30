import os,json,numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
H=os.path.expanduser('~'); T=f'{H}/mnt/TEMPERATUTE PAPER A/TEMPERATURE PAPER ONLY/results/'
OUT=f'{H}/ghs/out'
D=pd.read_csv(T+'dose_v2.csv'); C=pd.read_csv(T+'cells_v2.csv'); R=json.load(open(T+'reg_v2.json'))
GR=['2-5','5-10','10-20','>=20']; LBL=['2–5 pp','5–10 pp','10–20 pp','≥ 20 pp']
VAR=[('tn','Night LST (satellite)','#b2182b','o'),('td','Day LST (satellite)','#ef8a62','s'),
     ('en','ERA5-Land Tmin','#2166ac','D'),('ex','ERA5-Land Tmax','#92c5de','^')]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'axes.linewidth':0.6,
                     'axes.titlesize':9,'axes.titleweight':'bold','savefig.dpi':600})
fig=plt.figure(figsize=(7.48,5.6))
gs=fig.add_gridspec(2,2,width_ratios=[1.12,1.0],height_ratios=[1.0,0.80],wspace=0.40,hspace=1.05,left=0.115,right=0.985,top=0.93,bottom=0.115)
a=fig.add_subplot(gs[:,0])
a.axvline(0,color='0.25',lw=0.8,zorder=1)
off=[0.255,0.085,-0.085,-0.255]
for i,g in enumerate(GR):
    if i%2==0: a.axhspan(i-0.5,i+0.5,color='0.955',zorder=0)
    for j,(v,lab,col,mk) in enumerate(VAR):
        r=D[(D.group==g)&(D['var']==v)].iloc[0]
        y=i+off[j]
        a.plot([r.lo,r.hi],[y,y],color=col,lw=1.5,solid_capstyle='round',zorder=3)
        a.plot(r['diff'],y,mk,ms=5.2,mfc=col,mec='k',mew=0.5,zorder=4)
    n=int(D[(D.group==g)&(D['var']=='tn')].iloc[0].n)
    a.text(1.30,i-0.40,f'n = {n:,}',fontsize=7,color='0.35',ha='right',va='center')
a.set_yticks(range(len(GR))); a.set_yticklabels(LBL)
a.set_ylim(len(GR)-0.5,-0.5); a.set_xlim(-0.95,1.35)
a.set_xlabel('Urban − coast-matched rural trend (°C decade⁻¹)')
a.set_ylabel('Built-up fraction added, 1995–2020')
a.set_title('a   Exposure–response by urban growth class',loc='left')
a.spines[['top','right']].set_visible(False); a.tick_params(labelsize=8)
a.legend(handles=[Line2D([0],[0],marker=m,color=c,mfc=c,mec='k',mew=0.5,ms=5.2,lw=1.5,label=l)
                  for _,l,c,m in VAR],loc='upper left',bbox_to_anchor=(-0.02,-0.115),ncol=2,
         frameon=False,fontsize=7.2,labelspacing=0.35,columnspacing=1.2,handlelength=1.5)
b=fig.add_subplot(gs[0,1])
x=C.dbf.values*100 if C.dbf.max()<1.5 else C.dbf.values
HB=[]
for v,col,lab,mk in [('tn','#b2182b','Night LST (satellite)','o'),('en','#2166ac','ERA5-Land Tmin','D')]:
    y=C[v].values; ok=np.isfinite(x)&np.isfinite(y)
    b.plot(x[ok],y[ok],mk,ms=3.4,mfc=col,mec='none',alpha=0.55,zorder=2)
    sl,i0=np.polyfit(x[ok],y[ok],1)
    xs=np.linspace(0,x[ok].max(),50); b.plot(xs,sl*xs+i0,color=col,lw=1.4,zorder=3)
    HB.append(Line2D([0],[0],marker=mk,color=col,mfc=col,mec='none',ms=4.5,lw=1.4,
              label='%s: %s%.2f \u00b0C decade\u207b\u00b9 pp\u207b\u00b9'%(lab,'+' if sl>=0 else '\u2212',abs(sl))))
HB.append(Line2D([0],[0],color='#5b9bd5',lw=1.4,ls='--',
          label='NEX-GDDP-CMIP6: \u22120.14 (5\u201395%: \u22120.27, 0.03)'))
b.set_xlabel('Built-up fraction added in 0.25° cell (pp)')
b.set_ylabel('Trend 1995–2024 (°C decade⁻¹)')
b.set_title(f'b   Model grid scale (0.25°, n = {len(C)})',loc='left')
b.spines[['top','right']].set_visible(False); b.tick_params(labelsize=8)
b.legend(handles=HB,loc='upper left',bbox_to_anchor=(-0.02,-0.24),ncol=1,frameon=False,fontsize=7.0,labelspacing=0.30,handlelength=1.5)

# panel c: rural background convergence vs the urban increment
import json as _j
RB=_j.load(open(T+'rural_background_v2.json'))
u=D[(D.group=='10-20')]
u_tn=float(u[u['var']=='tn'].iloc[0].urban); u_en=float(u[u['var']=='en'].iloc[0].urban)
c=fig.add_subplot(gs[1,1])
rows=[('Satellite night LST',RB['rural_night_lst_trend'],None,'#b2182b'),
      ('ERA5-Land Tmin',RB['rural_era5land_tmin_trend'],None,'#2166ac'),
      ('NEX-GDDP-CMIP6 median',RB['nex_ensemble_median_uae_tmin_trend'],RB['nex_5_95'],'#5b9bd5'),
      ('Satellite night LST',u_tn,None,'#b2182b'),
      ('ERA5-Land Tmin',u_en,None,'#2166ac')]
ypos=[4.35,3.65,2.95,1.55,0.85]
for (lab,v,rng,col),y in zip(rows,ypos):
    if rng: c.plot(rng,[y,y],color=col,lw=1.4,alpha=0.55,solid_capstyle='round',zorder=2)
    c.plot([0,v],[y,y],color=col,lw=1.0,alpha=0.35,zorder=1)
    c.plot(v,y,'o',ms=6,mfc=col,mec='k',mew=0.5,zorder=3)
    c.text(v+0.04,y+0.22,'%.2f'%v,fontsize=7,color=col,va='center')
c.axvline(RB['rural_night_lst_trend'],color='0.55',lw=0.7,ls=':',zorder=0)
c.set_yticks(ypos); c.set_yticklabels([r[0] for r in rows],fontsize=7.2)
c.set_ylim(0.3,5.15); c.set_xlim(0,1.45)
c.text(1.42,4.95,'Rural background (UN rural)',fontsize=7.4,style='italic',color='0.3',ha='right')
c.text(1.42,2.15,'Urbanising land (\u2265 10 pp added)',fontsize=7.4,style='italic',color='0.3',ha='right')
c.set_xlabel('Trend 1995\u20132024 (\u00b0C decade\u207b\u00b9)')
c.set_title('c   Background vs urban increment',loc='left',fontsize=8.6)
c.spines[['top','right']].set_visible(False); c.tick_params(labelsize=7.5)
fig.savefig(f'{OUT}/Figure4.png',dpi=600,bbox_inches='tight')
fig.savefig(f'{OUT}/Figure4.pdf',bbox_inches='tight')
print('ok', round(float(x.max()),2))
