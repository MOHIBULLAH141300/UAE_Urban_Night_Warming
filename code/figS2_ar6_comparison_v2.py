import os,numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
H=os.path.expanduser('~'); T=f'{H}/mnt/TEMPERATUTE PAPER A/TEMPERATURE PAPER ONLY/results/'; OUT=f'{H}/ghs/out'
M=pd.read_csv(T+'ar6_models.csv'); ST=pd.read_csv(T+'station_v2.csv')
SSP=[('ssp126','SSP1-2.6','#1d3354'),('ssp245','SSP2-4.5','#eba631'),
     ('ssp370','SSP3-7.0','#c5442e'),('ssp585','SSP5-8.5','#7d1d1d')]
PER=[('near','2021–2040'),('mid','2041–2060'),('long','2081–2100')]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.6,'axes.linewidth':0,
                     'axes.titlesize':9.4,'axes.titleweight':'bold','savefig.dpi':600,
                     'text.color':'#222222','xtick.color':'#555555','ytick.color':'#555555'})
fig=plt.figure(figsize=(7.4,4.3))
gs=fig.add_gridspec(1,2,width_ratios=[3.5,1.0],wspace=0.06,left=0.085,right=0.985,top=0.84,bottom=0.21)
a=fig.add_subplot(gs[0,0]); b=fig.add_subplot(gs[0,1],sharey=a)
def style(ax):
    ax.set_axisbelow(True); ax.yaxis.grid(True,color='#e8e8e8',lw=0.7); ax.xaxis.grid(False)
    for s_ in ax.spines.values(): s_.set_visible(False)
    ax.tick_params(length=0,labelsize=8)
rng=np.random.default_rng(20260713); pos=0; ticks=[]; labs=[]; cent=[]
for si,(ssp,lab,col) in enumerate(SSP):
    start=pos
    for pk,pl in PER:
        v=M[(M.ssp==ssp)&(M.period==pk)].dtmin.dropna().values
        q1,med,q3=np.percentile(v,[25,50,75]); lo,hi=np.percentile(v,[5,95])
        a.plot([pos,pos],[lo,hi],color=col,lw=1.0,alpha=0.55,zorder=2,solid_capstyle='round')
        a.add_patch(Rectangle((pos-0.22,q1),0.44,q3-q1,facecolor=col,alpha=0.20,edgecolor=col,lw=0.9,zorder=3))
        a.plot([pos-0.22,pos+0.22],[med,med],color=col,lw=2.0,zorder=5,solid_capstyle='butt')
        a.plot(pos+rng.uniform(-0.10,0.10,len(v)),v,'o',ms=2.4,mfc=col,mec='none',alpha=0.45,zorder=4)
        ticks.append(pos); labs.append(pl); pos+=1.15
    cent.append((start+pos-1)/2)
    if si<3: a.axvline(pos-0.5,color='#e0e0e0',lw=0.8,zorder=0)
    pos+=0.55
a.set_xticks(ticks); a.set_xticklabels(labs,fontsize=7.2,rotation=32,ha='right',rotation_mode='anchor')
for cx,(_,lab,col) in zip(cent,SSP):
    a.text(cx,-0.235,lab,transform=a.get_xaxis_transform(),ha='center',va='top',
           fontsize=8.6,fontweight='bold',color=col)
a.set_ylabel('Tmin change relative to 1995–2014 (°C)')
a.set_title('a   NEX-GDDP-CMIP6 projected UAE-area warming, IPCC AR6 periods',loc='left',pad=16)
a.set_xlim(-0.8,pos-0.9); style(a)
NAM=[('Dubai','DXB'),('Sharjah','SHJ'),('Abu Dhabi','AUH'),('Al Ain','AAN')]
DK='#a01c30'; LT='#f0b8a0'
for i,(nm,code) in enumerate(NAM):
    r=ST[ST.name==nm].iloc[0]
    tot=float(r.tmin)*2.9; e5=float(r.e5_tmin)*2.9; miss=tot-e5
    b.add_patch(Rectangle((i-0.30,0),0.60,e5,facecolor=LT,edgecolor='none',zorder=2))
    b.add_patch(Rectangle((i-0.30,e5),0.60,miss,facecolor=DK,edgecolor='none',zorder=2))
    b.text(i,tot+0.12,'%.1f'%tot,ha='center',fontsize=7.6,color=DK,fontweight='bold')
b.set_xticks(range(len(NAM))); b.set_xticklabels([c for _,c in NAM],fontsize=7.8)
b.text(1.5,-0.235,'Observed 1995–2024',transform=b.get_xaxis_transform(),ha='center',va='top',
       fontsize=8.6,fontweight='bold',color='#333333')
b.set_xlim(-0.7,len(NAM)-0.3); b.set_title('b   Observed station rise',loc='left',pad=16); style(b)
plt.setp(b.get_yticklabels(),visible=False)
b.legend(handles=[Patch(facecolor=DK,label='Not represented in ERA5-Land'),
                  Patch(facecolor=LT,label='Represented in ERA5-Land')],
         loc='upper center',bbox_to_anchor=(0.5,-0.245),frameon=False,fontsize=7.4,
         handlelength=1.3,labelspacing=0.3)
a.legend(handles=[plt.Line2D([0],[0],color='#555555',lw=2,label='median'),
                  Patch(facecolor='#cccccc',edgecolor='#888888',label='interquartile range'),
                  plt.Line2D([0],[0],color='#888888',lw=1,label='5–95% of models'),
                  plt.Line2D([0],[0],marker='o',color='none',mfc='#888888',ms=3,label='individual model')],
         loc='upper left',bbox_to_anchor=(0.0,1.19),ncol=4,frameon=False,fontsize=7.4,
         handlelength=1.3,columnspacing=1.4)
fig.savefig(f'{OUT}/FigureS2.png',dpi=600,bbox_inches='tight')
fig.savefig(f'{OUT}/FigureS2.pdf',bbox_inches='tight')
print('ok')
