import os,json,numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
H=os.path.expanduser('~'); T=f'{H}/mnt/TEMPERATUTE PAPER A/TEMPERATURE PAPER ONLY/results/'; OUT=f'{H}/ghs/out'
S=pd.read_csv(T+'ts_v2.csv'); B=json.load(open(T+'builtup_v2.json'))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.6,'axes.linewidth':0,
                     'axes.titlesize':9.4,'axes.titleweight':'bold','savefig.dpi':600,
                     'axes.labelcolor':'#333333','text.color':'#222222',
                     'xtick.color':'#666666','ytick.color':'#666666'})
NIGHT='#a01c30'; DAY='#e8833a'; BUILT='#6d2f66'; GRID='#e6e6e6'
fig,ax=plt.subplots(3,1,figsize=(7.2,5.9),sharex=True,
    gridspec_kw={'height_ratios':[1,1,0.62],'hspace':0.30,'left':0.095,'right':0.975,'top':0.955,'bottom':0.085})
def style(a):
    a.set_axisbelow(True); a.yaxis.grid(True,color=GRID,lw=0.7); a.xaxis.grid(False)
    for s_ in a.spines.values(): s_.set_visible(False)
    a.tick_params(length=0,labelsize=8)
def panel(a,y,col,title,note_y):
    x=S.year.values.astype(float); ok=np.isfinite(y)
    a.axvspan(2017.5,2018.5,color='#f2f2f2',zorder=0)
    a.fill_between(x[ok],0,y[ok],color=col,alpha=0.13,lw=0,zorder=1)
    a.axhline(0,color='#9a9a9a',lw=0.8,zorder=2)
    k,b0=np.polyfit(x[ok],y[ok],1)
    xs=np.linspace(x.min(),x.max(),100); fit=k*xs+b0
    n=ok.sum(); res=y[ok]-(k*x[ok]+b0); se=np.sqrt(res@res/(n-2))
    sx=np.sqrt(1/n+(xs-x[ok].mean())**2/((x[ok]-x[ok].mean())**2).sum())*se*2
    a.fill_between(xs,fit-sx,fit+sx,color=col,alpha=0.16,lw=0,zorder=3)
    a.plot(xs,fit,color=col,lw=1.3,ls=(0,(4,2)),zorder=4)
    a.plot(x[ok],y[ok],'-',color=col,lw=1.5,alpha=0.85,zorder=5)
    a.plot(x[ok],y[ok],'o',ms=3.6,mfc='white',mec=col,mew=1.1,zorder=6)
    sgn='+' if k>=0 else '−'
    a.text(0.995,note_y,'%s%.3f °C yr⁻¹'%(sgn,abs(k)),transform=a.transAxes,
           ha='right',va='center',fontsize=8,color=col,fontweight='bold')
    a.set_title(title,loc='left',color='#222222'); a.set_ylabel('Difference (°C)')
    style(a)
panel(ax[0],S.night_diff.values,NIGHT,'a   Night-time LST  ·  urbanising − rural',0.08)
panel(ax[1],S.day_diff.values,DAY,'b   Day-time LST  ·  urbanising − rural',0.92)
c=ax[2]
c.axvspan(2017.5,2018.5,color='#f2f2f2',zorder=0)
c.fill_between(B['ep'],B['km2'],color=BUILT,alpha=0.16,lw=0,zorder=1)
c.plot(B['ep'],B['km2'],'-',color=BUILT,lw=1.6,zorder=2)
c.plot(B['ep'],B['km2'],'o',ms=3.6,mfc='white',mec=BUILT,mew=1.1,zorder=3)
for yr,lb in ((1995,'298'),(2020,'626')):
    v=B['km2'][B['ep'].index(yr)]
    c.annotate(f'{lb} km²',(yr,v),xytext=(4,7),textcoords='offset points',fontsize=7.6,color=BUILT,fontweight='bold')
c.set_title('c   UAE built-up surface  ·  GHS-BUILT-S',loc='left',color='#222222')
c.set_ylabel('Built-up (km²)'); c.set_xlabel('Year')
c.set_xlim(1994.5,2024.5); c.set_ylim(0,760); style(c)
ax[0].text(2018,ax[0].get_ylim()[0]*0.92,'no data',fontsize=7,color='#8a8a8a',ha='center',va='bottom',rotation=90)
fig.savefig(f'{OUT}/FigureS1.png',dpi=600,bbox_inches='tight')
fig.savefig(f'{OUT}/FigureS1.pdf',bbox_inches='tight')
print('ok')
