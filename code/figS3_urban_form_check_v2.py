import os,json,numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
H=os.path.expanduser('~'); T=f'{H}/mnt/TEMPERATUTE PAPER A/TEMPERATURE PAPER ONLY/results/'; OUT=f'{H}/ghs/out'
M=json.load(open(T+'morph_v2.json')); R=json.load(open(T+'reg_v2.json')); C=pd.read_csv(T+'future_check_v3.csv')
HC=M['height_classes']; base=R['tn_base']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.6,'axes.linewidth':0,'axes.titlesize':9.4,
   'axes.titleweight':'bold','savefig.dpi':600,'text.color':'#222222','xtick.color':'#555555','ytick.color':'#555555'})
COL='#a01c30'; GREY='#8a8a8a'
fig,(a,b)=plt.subplots(1,2,figsize=(7.4,3.5),
    gridspec_kw={'width_ratios':[1,1.08],'wspace':0.30,'left':0.095,'right':0.985,'top':0.88,'bottom':0.155})
def style(ax):
    ax.set_axisbelow(True); ax.yaxis.grid(True,color='#e8e8e8',lw=0.7); ax.xaxis.grid(False)
    for s_ in ax.spines.values(): s_.set_visible(False)
    ax.tick_params(length=0,labelsize=8)
# a: slope by height class
a.axhspan(base['lo'],base['hi'],color=GREY,alpha=0.13,zorder=0)
a.axhline(base['dbf'],color=GREY,lw=1.1,ls=(0,(4,2)),zorder=1)
a.text(2.42,base['dbf']+0.012,'all urbanising pixels  %.2f'%base['dbf'],fontsize=7.4,color='#666666',ha='right',va='bottom')
x=np.arange(len(HC))
for i,h in enumerate(HC):
    a.plot([i,i],[h['lo'],h['hi']],color=COL,lw=1.6,solid_capstyle='round',zorder=3)
    a.plot(i,h['slope'],'o',ms=8,mfc=COL,mec='white',mew=1.2,zorder=4)
    a.text(i,h['hi']+0.022,'%.2f'%h['slope'],ha='center',fontsize=7.8,color=COL,fontweight='bold')
    a.text(i,-0.115,'n = %d'%h['n'],ha='center',fontsize=7.2,color='#888888')
a.axhline(0,color='#bbbbbb',lw=0.8,zorder=1)
a.set_xticks(x); a.set_xticklabels([h['cls'].replace('>=','≥ ').replace('<','< ').replace('5-10','5–10') for h in HC],fontsize=8.2)
a.set_xlim(-0.5,2.5); a.set_ylim(-0.16,0.68)
a.set_ylabel('Night LST trend per 10 pp added\nbuilt-up (°C decade⁻¹)')
a.set_xlabel('Mean building height, 2018')
a.set_title('a   Response weakens as buildings get taller',loc='left'); style(a)
# b: retrospective check
mx=max(C.pred_surface.max(),C.obs_total.max())*1.12
b.plot([0,mx],[0,mx],color='#999999',lw=1.0,zorder=1)
b.text(mx*0.955,mx*0.985,'1:1',fontsize=7.4,color='#888888',ha='right',va='top',rotation=38)
b.axhline(0,color='#cccccc',lw=0.8,zorder=1)
sz=30+C.dbf5_pp.values*22
b.scatter(C.pred_surface,C.obs_total,s=sz,c=COL,alpha=0.85,edgecolors='white',linewidths=1.0,zorder=3)
off={'Dubai':(8,-2),'Sharjah':(-8,6),'Abu Dhabi':(8,-4),'Al Ain':(8,2),'Fujairah':(9,-1),'Ras Al Khaimah':(9,-1)}
for _,r in C.iterrows():
    b.annotate(r['name'],(r.pred_surface,r.obs_total),xytext=off.get(r['name'],(7,3)),
               textcoords='offset points',fontsize=7.6,color='#333333',
               ha='right' if off.get(r['name'],(7,3))[0]<0 else 'left')
b.set_xlim(0,mx); b.set_ylim(min(-0.6,C.obs_total.min()*1.3),mx)
b.set_xlabel('Predicted from built-up growth (°C)')
b.set_ylabel('Observed excess warming 1995–2024 (°C)')
b.set_title('b   Observed rise exceeds the surface prediction',loc='left'); style(b)
fig.savefig(f'{OUT}/FigureS3.png',dpi=600,bbox_inches='tight')
fig.savefig(f'{OUT}/FigureS3.pdf',bbox_inches='tight')
print('ok')
