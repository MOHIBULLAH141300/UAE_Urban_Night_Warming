import json,numpy as np,pandas as pd,geopandas as gpd,matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import Patch
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'axes.linewidth':0.6,'axes.titlesize':9,'axes.titleweight':'bold','savefig.dpi':300})
L=np.load('layers.npz'); lat=L['lat'];lon=L['lon']; ext=[lon[0],lon[-1],lat[-1],lat[0]]
g0=gpd.read_file('shp/gadm41_ARE_0.shp'); g1=gpd.read_file('shp/gadm41_ARE_1.shp')
mask=L['uae']&L['land']
S=pd.read_csv('station_v2.csv',dtype={'sid':str}); DW=pd.read_csv('dew_v2.csv')
DO=pd.read_csv('dose_v2.csv'); RG=json.load(open('reg_v2.json')); GR=json.load(open('groups_v2.json')); CL=json.load(open('classes_v2.json'))
TS=pd.read_csv('ts_v2.csv'); CC=pd.read_csv('cells_v2.csv'); AR=pd.read_csv('ar6_tmin.csv'); ARM=pd.read_csv('ar6_models.csv')
M=pd.read_csv('hadisd_meta.csv',dtype={'sid':str})
short={'Ras Al Khaimah':'RAK','Dubai':'DXB','Sharjah':'SHJ','Fujairah':'FJR','Al Bateen':'AZI','Abu Dhabi':'AUH','Al Ain':'AAN'}
mp=np.load('maps_v2.npz'); idx=mp['idx']
def to2d(v):
    a=np.full(mask.size,np.nan); a[idx]=v; return a.reshape(mask.shape)
def outline(ax,lw=0.5):
    g1.boundary.plot(ax=ax,color='0.35',lw=lw*0.6); g0.boundary.plot(ax=ax,color='k',lw=lw)
kx=0.00898*111.32*np.cos(np.deg2rad(24.5)); ky=0.00898*110.57

# ---------------- Figure 1
fig,ax=plt.subplots(1,2,figsize=(7.2,3.3),gridspec_kw={'width_ratios':[1.25,1]})
d=np.where(mask,(L['bf2020']-L['bf1995'])*100,np.nan)
a=ax[0]; a.set_facecolor('#dfe9f2')
a.imshow(np.where(mask,0.,np.nan),extent=ext,cmap='Greys',vmin=0,vmax=4)
a.imshow(np.where(mask&(L['bf1995']>=0.05),1,np.nan),extent=ext,cmap='Greys',vmin=0,vmax=1.6,alpha=0.9)
im=a.imshow(np.where(d>=1,d,np.nan),extent=ext,cmap='magma_r',vmin=0,vmax=25)
a.contour(lon,lat,np.where(mask,L['smod2020']==30,0),levels=[0.5],colors='#1a9850',linewidths=0.5)
outline(a)
for _,s in M.iterrows():
    if s.sid=='411945': continue
    nm=short.get(s['name'].replace(' Intl','').replace('Abu Dhabi Intl','Abu Dhabi'),None)
    key={'Dubai Intl':'DXB','Sharjah':'SHJ','Abu Dhabi Intl':'AUH','Al Bateen':'AZI','Al Ain':'AAN','Ras Al Khaimah':'RAK','Fujairah':'FJR'}[s['name']]
    a.plot(s.lon,s.lat,'^',ms=5,mfc='deepskyblue',mec='k',mew=0.5)
    off={'DXB':(-0.55,-0.2),'SHJ':(0.08,0.08),'AZI':(-0.45,0.12),'AUH':(0.08,-0.18),'FJR':(-0.45,-0.22),'RAK':(0.07,0.05),'AAN':(0.07,0.05)}[key]
    a.text(s.lon+off[0],s.lat+off[1],key,fontsize=7,weight='bold')
a.set_xlim(51.5,56.45); a.set_ylim(22.6,26.1); a.set_xlabel('Longitude (°E)'); a.set_ylabel('Latitude (°N)')
cb=plt.colorbar(im,ax=a,shrink=0.75,pad=0.02); cb.set_label('Built-up fraction added\n1995–2020 (percentage points)')
a.set_title('a  Urban growth and stations',loc='left')
a=ax[1]
ep=[1975,1990,1995,2000,2005,2010,2015,2020,2025]
km2=[float(np.nansum(L[f'bf{e}'][mask])*kx*ky) for e in ep]
uc=[float((L[f'smod{e}'][mask]==30).sum()*kx*ky) if f'smod{e}' in L else np.nan for e in ep]
a.plot(ep,km2,'o-',color='#7a1f5c',ms=4,label='Built-up surface')
a.plot([e for e,v in zip(ep,uc) if np.isfinite(v)],[v for v in uc if np.isfinite(v)],'s--',color='#1a9850',ms=4,label='Land in UN urban centres')
a.axvspan(1995,2024,color='0.9',zorder=0); a.text(2010,max(km2)*0.3,'analysis period\n1995–2024',ha='center',fontsize=7.5,color='0.3')
a.set_ylabel('Area (km²)'); a.set_xlabel('GHSL epoch'); a.legend(frameon=False,fontsize=7,loc='upper left')
a.set_title('b  Built-up surface',loc='left'); a.spines[['top','right']].set_visible(False)
plt.tight_layout(); plt.savefig('figs/Figure1.png'); plt.close()
json.dump({'ep':ep,'km2':km2,'urban_centre':uc},open('builtup_v2.json','w'))

# ---------------- Figure 2 stations
order=['Dubai','Sharjah','Abu Dhabi','Al Ain','Ras Al Khaimah','Fujairah']
s=S.set_index('name').loc[order]
fig=plt.figure(figsize=(7.2,5.6)); gs=fig.add_gridspec(2,2)
a=fig.add_subplot(gs[0,:]); x=np.arange(len(order)); w=0.2
a.bar(x-1.5*w,s.tmin,w,yerr=[np.clip(s.tmin-s.tmin_lo,0,None),np.clip(s.tmin_hi-s.tmin,0,None)],color='#b2182b',capsize=2,error_kw=dict(lw=0.6),label='Station Tmin')
a.bar(x-0.5*w,s.tmax,w,color='#f4a582',label='Station Tmax')
a.bar(x+0.5*w,s.e5_tmin,w,color='#2166ac',label='ERA5-Land Tmin (nearest cell)')
a.bar(x+1.5*w,s.nex_med,w,yerr=[np.clip(s.nex_med-s.nex_p5,0,None),np.clip(s.nex_p95-s.nex_med,0,None)],color='#92c5de',capsize=2,error_kw=dict(lw=0.6),label='NEX-GDDP-CMIP6 Tmin (median, 5–95%)')
a.set_xticks(x); a.set_xticklabels([f"{short[n]}\nΔBF {100*s.loc[n,'dbf5']:.0f} pp" for n in order]); a.axhline(0,color='k',lw=0.5)
a.set_ylabel('Theil–Sen trend 1995–2024\n(°C decade⁻¹)'); a.legend(ncol=2,fontsize=7,frameon=False,loc='upper right'); a.spines[['top','right']].set_visible(False)
a.set_title('a  Station and reanalysis trends at the same locations',loc='left')
a=fig.add_subplot(gs[1,0])
r=S.dropna(subset=['excess']); r=r[r.name!='Al Bateen']
a.errorbar(r.dbf5*100,r.excess,yerr=[np.clip(r.excess-r.excess_lo,0,None),np.clip(r.excess_hi-r.excess,0,None)],fmt='o',color='#b2182b',ms=5,capsize=2,lw=0.6)
for _,q in r.iterrows(): a.annotate(short[q['name']],(q.dbf5*100,q.excess),xytext={'Ras Al Khaimah':(-20,-10),'Fujairah':(4,-12)}.get(q['name'],(4,3)),textcoords='offset points',fontsize=7)
a.axhline(0,color='k',lw=0.5); a.set_xlabel('Built-up fraction added within 5 km (pp)')
a.set_ylabel('Station − ERA5-Land Tmin trend\n(°C decade⁻¹)'); a.spines[['top','right']].set_visible(False)
a.set_title('b  Missing warming vs urban growth (ρ = 0.93)',loc='left')
a=fig.add_subplot(gs[1,1])
C=np.load('cci_annual30.npz')
A=pd.read_csv('hadisd_annual_anom.csv',dtype={'sid':str})
E=np.load('era5land_annual_tmin_tmax.npz')
dx=A[(A.sid=='411940')&(A.y>=1995)&(A.y<=2024)].set_index('y').tmin
D=(E['lat'][:,None]-25.255)**2+(E['lon'][None,:]-55.364)**2; D[~np.isfinite(E['tmin']).all(0)]=np.inf
i,j=np.unravel_index(D.argmin(),D.shape)
e=pd.Series(E['tmin'][:,i,j],index=E['years']).loc[1995:2024]
e=e-e.loc[1995:2020].mean(); st=dx-dx.loc[1995:2020].mean()
a.plot(e.index,e.values,color='#2166ac',lw=1.2,label='ERA5-Land cell')
a.plot(st.index,st.values,'o-',color='#b2182b',ms=2.5,lw=1.2,label='Dubai Intl station')
a.set_ylabel('Tmin anomaly (°C)'); a.legend(fontsize=7,frameon=False,loc='upper left'); a.spines[['top','right']].set_visible(False)
a.set_title('c  Dubai: station vs reanalysis',loc='left')
plt.tight_layout(); plt.savefig('figs/Figure2.png'); plt.close()

# ---------------- Figure 3 maps
zx=(53.9,56.45); zy=(23.95,25.85)
fig,ax=plt.subplots(1,3,figsize=(7.6,3.1),sharey=True)
for a,(k,tt) in zip(ax,[('tn','a  Night LST (satellite)'),('td','b  Day LST (satellite)'),('en','c  ERA5-Land Tmin')]):
    v=to2d(mp[k])
    im=a.imshow(v,extent=ext,cmap='RdBu_r',norm=TwoSlopeNorm(0,-1.5,2.0),interpolation='nearest')
    if k in ('tn','td'):
        q=to2d(mp[k+'_q']) if k+'_q' in mp else None
        if q is not None:
            sig=(q<0.05)
            yy,xx=np.where(sig[::7,::7]); a.plot(lon[::7][xx],lat[::7][yy],'.',color='0.25',ms=0.35,alpha=0.5)
    a.contour(lon,lat,np.where(mask,L['bf2020']-L['bf1995'],0),levels=[0.10],colors='k',linewidths=0.5)
    outline(a,0.4); a.set_xlim(*zx); a.set_ylim(*zy); a.set_title(tt,loc='left',fontsize=8.5); a.set_xlabel('Longitude (°E)')
    for _,q2 in M.iterrows():
        if q2.sid!='411945': a.plot(q2.lon,q2.lat,'^',ms=3.5,mfc='yellow',mec='k',mew=0.4)
ax[0].set_ylabel('Latitude (°N)')
cb=fig.colorbar(im,ax=ax,shrink=0.8,pad=0.015); cb.set_label('°C decade⁻¹ (1995–2024)')
plt.savefig('figs/Figure3.png',bbox_inches='tight'); plt.close()

# ---------------- Figure 4 dose response + cells
grp=['2-5','5-10','10-20','>=20']; labs=['2–5','5–10','10–20','≥20']
fig,ax=plt.subplots(1,2,figsize=(7.2,3.1),gridspec_kw={'width_ratios':[1.35,1]})
a=ax[0]; x=np.arange(4)
sty={'tn':('Night LST (satellite)','#b2182b','o',-0.15),'td':('Day LST (satellite)','#ef8a62','s',-0.05),'en':('ERA5-Land Tmin','#2166ac','D',0.05),'ex':('ERA5-Land Tmax','#67a9cf','v',0.15)}
for k,(nm,c,m_,off) in sty.items():
    r=DO[(DO['var']==k)&DO.group.isin(grp)].set_index('group').loc[grp]
    a.errorbar(x+off,r['diff'],yerr=[r['diff']-r.lo,r.hi-r['diff']],fmt=m_+'-',color=c,ms=4,capsize=2,lw=1,label=nm)
a.axhline(0,color='k',lw=0.5); a.set_xticks(x); a.set_xticklabels(labs); a.set_xlabel('Built-up fraction added 1995–2020 (pp)')
a.set_ylabel('Urban − coast-matched rural trend\n(°C decade⁻¹)'); a.legend(fontsize=7,frameon=False,loc='lower left'); a.spines[['top','right']].set_visible(False)
nn=DO[(DO['var']=='tn')&DO.group.isin(grp)].set_index('group').loc[grp].n.values
for i,n in enumerate(nn): a.text(i,a.get_ylim()[1]*0.95,f'n={n}',ha='center',fontsize=6.5,color='0.35')
a.set_title('a  Dose–response (UN rural reference)',loc='left')
a=ax[1]
a.scatter(CC.dbf*100,CC.tn,s=12,color='#b2182b',label='Satellite night LST',zorder=3)
a.scatter(CC.dbf*100,CC.en,s=12,marker='D',color='#2166ac',label='ERA5-Land Tmin',zorder=3)
for yv,c in [(CC.tn,'#b2182b'),(CC.en,'#2166ac')]:
    p=np.polyfit(CC.dbf*100,yv,1); xs=np.linspace(0,(CC.dbf*100).max(),10); a.plot(xs,np.polyval(p,xs),color=c,lw=1)
ne=GR['cell_nex']
a.axhspan(0,0,color='none')
a.plot([],[],'^',color='#92c5de',label='NEX-GDDP slope: %.2f (5–95%%: %.2f, %.2f)'%(ne[0],ne[1],ne[2]))
a.set_xlabel('Built-up fraction added in 0.25° cell (pp)'); a.set_ylabel('Trend 1995–2024 (°C decade⁻¹)')
a.legend(fontsize=6.3,frameon=False,loc='upper left'); a.spines[['top','right']].set_visible(False)
a.set_title('b  Model grid scale (0.25°, n = %d)'%len(CC),loc='left',fontsize=8)
plt.tight_layout(); plt.savefig('figs/Figure4.png'); plt.close()

# ---------------- Figure 5 time series
fig,ax=plt.subplots(figsize=(7.0,3.0))
for a0,b0 in [(1994.5,2002.5),(2012.5,2017.5)]: ax.axvspan(a0,b0,color='0.93',zorder=0)
ax.axvspan(2017.5,2018.5,color='0.8',zorder=0,hatch='///',alpha=0.4)
ax.plot(TS.year,TS.night_diff,'o-',color='#b2182b',ms=3,label='Night LST: urbanising − rural')
ax.plot(TS.year,TS.day_diff,'s-',color='#ef8a62',ms=3,label='Day LST: urbanising − rural')
for col,c in [('night_diff','#b2182b'),('day_diff','#ef8a62')]:
    v=TS[['year',col]].dropna(); p=np.polyfit(v.year,v[col],1); ax.plot(v.year,np.polyval(p,v.year),'--',color=c,lw=0.8)
ax.axhline(0,color='k',lw=0.5); ax.set_ylabel('Anomaly difference (°C)'); ax.set_xlabel('Year')
bk=json.load(open('builtup_v2.json'))
ax2=ax.twinx(); ax2.plot(bk['ep'][2:],bk['km2'][2:],'k:',lw=1.2,marker='x',ms=4,label='UAE built-up surface'); ax2.set_ylabel('Built-up surface (km²)')
h1,l1=ax.get_legend_handles_labels(); h2,l2=ax2.get_legend_handles_labels(); ax.legend(h1+h2,l1+l2,fontsize=7,frameon=False,loc='upper left')
ax.set_xlim(1994.5,2024.5); plt.tight_layout(); plt.savefig('figs/FigureS1.png'); plt.close()

# ---------------- Figure 6 AR6 projections vs realised
fig,ax=plt.subplots(figsize=(7.2,3.4))
sc=['ssp126','ssp245','ssp370','ssp585']; per=['near','mid','long']
lab={'ssp126':'SSP1-2.6','ssp245':'SSP2-4.5','ssp370':'SSP3-7.0','ssp585':'SSP5-8.5'}
plab={'near':'2021–40','mid':'2041–60','long':'2081–2100'}
col={'near':'#deebf7','mid':'#9ecae1','long':'#3182bd'}
pos=0; ticks=[];tlabs=[]
for s_ in sc:
    for p_ in per:
        v=ARM[(ARM.ssp==s_)&(ARM.period==p_)].dtmin.values
        if len(v)==0: continue
        bp=ax.boxplot(v,positions=[pos],widths=0.6,patch_artist=True,whis=(5,95),showfliers=False,
                      boxprops=dict(facecolor=col[p_],lw=0.6),medianprops=dict(color='k'))
        ax.scatter(np.full(len(v),pos)+np.random.default_rng(1).uniform(-0.15,0.15,len(v)),v,s=4,color='k',alpha=0.4,zorder=3)
        ticks.append(pos); tlabs.append(plab[p_]); pos+=1
    ax.text(pos-2,-0.28,lab[s_],ha='center',fontsize=8,weight='bold',transform=ax.get_xaxis_transform())
    pos+=0.6
pos+=0.6; bars=[]
yrs=2.9
for n in ['Dubai','Sharjah','Abu Dhabi','Al Ain']:
    q=S.set_index('name').loc[n]
    ax.bar(pos,q.tmin*yrs,0.6,color='#f4a582',edgecolor='k',lw=0.4)
    ax.bar(pos,q.excess*yrs,0.6,color='#b2182b',edgecolor='k',lw=0.4)
    ticks.append(pos); tlabs.append(short[n]); pos+=0.8
ax.text(pos-2.0,-0.28,'observed 1995–2024',ha='center',fontsize=8,weight='bold',transform=ax.get_xaxis_transform())
ax.set_xticks(ticks); ax.set_xticklabels(tlabs,fontsize=7,rotation=45,ha='right')
ax.set_ylabel('Tmin change (°C)'); ax.axhline(0,color='k',lw=0.5); ax.spines[['top','right']].set_visible(False)
ax.legend(handles=[Patch(facecolor='#9ecae1',label='NEX-GDDP-CMIP6 UAE-area, vs 1995–2014 (IPCC AR6 periods)'),
                   Patch(color='#f4a582',label='Observed station Tmin rise 1995–2024'),
                   Patch(color='#b2182b',label='Part not present in ERA5-Land')],fontsize=6.8,frameon=False,loc='upper left')
plt.tight_layout(); plt.savefig('figs/FigureS2.png'); plt.close()

# ---------------- Figure 7 mechanisms
fig,ax=plt.subplots(3,2,figsize=(7.4,8.6))
a=ax[0,0]
groups=[('green_nobuild','Greening,\nno building'),('brown_nobuild','Browning,\nno building'),('urb_nogreen','Urbanising,\nno greening'),('urb_green','Urbanising,\nwith greening'),('h_low','Height\n< 5 m'),('h_mid','Height\n5\u201310 m'),('h_high','Height\n> 10 m')]
x=np.arange(len(groups))
for var,c,off,lb in [('tn','#b2182b',-0.19,'Night LST'),('td','#ef8a62',0.19,'Day LST')]:
    v=np.array([GR[f'{g}_{var}'][:3] for g,_ in groups])
    a.bar(x+off,v[:,0],0.38,yerr=[v[:,0]-v[:,1],v[:,2]-v[:,0]],color=c,capsize=2,error_kw=dict(lw=0.6),label=lb)
a.axhline(0,color='k',lw=0.5); a.set_xticks(x); a.set_xticklabels([g[1] for g in groups],fontsize=6.3,rotation=35,ha='right')
a.set_ylabel('Minus coast-matched rural trend\n(°C decade⁻¹)'); a.legend(frameon=False,fontsize=7,loc='lower left'); a.spines[['top','right']].set_visible(False)
a.set_title('a  Buildings, greening and height',loc='left')
a=ax[0,1]
lab2=['Annual','Summer\n(Jun–Sep)','Winter\n(Dec–Mar)']; x=np.arange(3)
n=[[RG['tn_base']['dbf'],RG['tn_base']['lo'],RG['tn_base']['hi']],[RG['tn_s_base']['dbf'],RG['tn_s_base']['lo'],RG['tn_s_base']['hi']],[RG['tn_w_base']['dbf'],RG['tn_w_base']['lo'],RG['tn_w_base']['hi']]]
d2=[[RG['td_base']['dbf'],RG['td_base']['lo'],RG['td_base']['hi']],[RG['td_s_base']['dbf'],RG['td_s_base']['lo'],RG['td_s_base']['hi']],[RG['td_w_base']['dbf'],RG['td_w_base']['lo'],RG['td_w_base']['hi']]]
for v,c,off,l in [(np.array(n),'#b2182b',-0.19,'Night LST'),(np.array(d2),'#ef8a62',0.19,'Day LST')]:
    a.bar(x+off,v[:,0],0.38,yerr=[v[:,0]-v[:,1],v[:,2]-v[:,0]],color=c,capsize=2,error_kw=dict(lw=0.6),label=l)
a.axhline(0,color='k',lw=0.5); a.set_xticks(x); a.set_xticklabels(lab2); a.set_ylabel('Trend change per 10 pp added\nbuilt-up (°C decade⁻¹)')
a.legend(frameon=False,fontsize=7); a.spines[['top','right']].set_visible(False); a.set_title('b  Season',loc='left')
a=ax[1,0]
order2=['Dubai','Sharjah','Abu Dhabi','Al Ain','Ras Al Khaimah','Fujairah']; r=S.set_index('name').loc[order2]
x=np.arange(len(order2))
a.bar(x-0.25,r.tn90p,0.25,color='#b2182b',label='Station')
a.bar(x,r.e5_tn90p,0.25,color='#2166ac',label='ERA5-Land')
a.bar(x+0.25,r.nex_tn90p_med,0.25,yerr=[np.clip(r.nex_tn90p_med-r.nex_tn90p_p5,0,None),np.clip(r.nex_tn90p_p95-r.nex_tn90p_med,0,None)],color='#92c5de',capsize=2,error_kw=dict(lw=0.6),label='NEX-GDDP (median, 5–95%)')
a.axhline(0,color='k',lw=0.5); a.set_xticks(x); a.set_xticklabels([short[o] for o in order2]); a.set_ylabel('TN90p trend (% of nights decade⁻¹)')
a.legend(frameon=False,fontsize=6.2,loc='upper center',ncol=1,bbox_to_anchor=(0.62,1.0)); a.spines[['top','right']].set_visible(False); a.set_title('c  ETCCDI warm nights (TN90p)',loc='left')
a=ax[1,1]
w=DW.set_index('name').loc[order2]
a.bar(x-0.18,w.tmin,0.36,color='#b2182b',label='Station Tmin trend')
a.bar(x+0.18,w.tmin_dewadj,0.36,color='#fddbc7',edgecolor='#b2182b',lw=0.6,label='After removing dewpoint-related variation')
for i,o in enumerate(order2): a.text(i,max(w.tmin.iloc[i],w.tmin_dewadj.iloc[i])+0.04,f"Td {w.dew_trend.iloc[i]:+.2f}",ha='center',fontsize=6.3,color='0.3')
a.axhline(0,color='k',lw=0.5); a.set_xticks(x); a.set_xticklabels([short[o] for o in order2]); a.set_ylabel('°C decade⁻¹ (1995–2024)')
a.legend(frameon=False,fontsize=6.5,loc='upper right'); a.spines[['top','right']].set_visible(False); a.set_title('d  Humidity check',loc='left'); a.set_ylim(top=1.7)
a=ax[2,0]
keys=[('base','No mediator'),('modis_ndvi_modis','+ NDVI change'),('modis_alb_modis','+ albedo change'),('viirs_modis','+ night lights'),('modis_all_modis','+ all three')]
v=np.array([[RG['tn_'+k]['dbf'],RG['tn_'+k]['lo'],RG['tn_'+k]['hi']] for k,_ in keys])
x2=np.arange(len(keys))
a.bar(x2,v[:,0],0.55,yerr=[v[:,0]-v[:,1],v[:,2]-v[:,0]],color='#b2182b',capsize=2,error_kw=dict(lw=0.6))
a.set_xticks(x2); a.set_xticklabels([k[1] for k in keys],rotation=30,ha='right',fontsize=7)
a.set_ylabel('Night LST trend per 10 pp\nadded built-up (°C decade⁻¹)'); a.spines[['top','right']].set_visible(False)
a.set_title('e  How much the mechanisms explain',loc='left')
a=ax[2,1]
gg=['2-5','5-10','10-20','>=20']; lab3=['2–5','5–10','10–20','≥20']; x3=np.arange(4)
dal=[-CL[g]['dalb_modis'] for g in gg]; dnd=[CL[g]['dndvi_modis'] for g in gg]; ntl=[CL[g]['viirs'] for g in gg]
a.bar(x3-0.19,dal,0.38,color='#4d4d4d',label='Albedo decrease')
a.bar(x3+0.19,dnd,0.38,color='#1a9850',label='NDVI increase')
a.axhline(CL['rural']['dndvi_modis'],color='#1a9850',ls=':',lw=0.8); a.axhline(-CL['rural']['dalb_modis'],color='#4d4d4d',ls=':',lw=0.8)
a.set_xticks(x3); a.set_xticklabels(lab3); a.set_xlabel('Built-up fraction added 1995–2020 (pp)')
a.set_ylabel('Change, 2000s to 2020s'); a.legend(frameon=False,fontsize=7,loc='upper left'); a.spines[['top','right']].set_visible(False)
a2=a.twinx(); a2.plot(x3,ntl,'o-',color='#f0a202',ms=4,lw=1.2); a2.set_ylabel('Night lights 2024 (nW cm⁻² sr⁻¹)',color='#b07700'); a2.tick_params(axis='y',colors='#b07700')
a.set_title('f  Surface change with urban growth',loc='left')
plt.tight_layout(); plt.savefig('figs/Figure6.png'); plt.close()
print('figures ok')
