import numpy as np,pandas as pd,json,glob,os
import statsmodels.api as sm
rng=np.random.default_rng(20260713)
L=np.load('layers.npz'); C=np.load('cci_annual30.npz'); lat=L['lat'];lon=L['lon']
df=pd.read_pickle('pixels_v2.pkl')
iy=np.round((lat[0]-df.lat.values)/(lat[0]-lat[1])).astype(int); ix=np.round((df.lon.values-lon[0])/(lon[1]-lon[0])).astype(int)
df['bh']=np.load('morph.npz')['hnet'][iy,ix]   # mean building height over built sub-cells
rural=df.rural.values
blks=np.sort(df.blk.unique()); bi=np.searchsorted(blks,df.blk.values); nbk=len(blks)
W=rng.multinomial(nbk,np.ones(nbk)/nbk,size=2000).astype(float)
def SN(sel,var):
    S=np.zeros((nbk,6));N=np.zeros((nbk,6)); np.add.at(S,(bi[sel],df.dbin.values[sel]),df[var].values[sel]); np.add.at(N,(bi[sel],df.dbin.values[sel]),1); return S,N
def dfrom(Su,Nu,Sr,Nr):
    ok=(Nu>0)&(Nr>0); w=np.where(ok,Nu,0.); w=w/w.sum(-1,keepdims=True)
    um=np.where(ok,Su/np.where(Nu>0,Nu,1),0); rm=np.where(ok,Sr/np.where(Nr>0,Nr,1),0); return (um*w).sum(-1)-(rm*w).sum(-1)
def mdiff(sel,var):
    sel=np.asarray(sel); Su,Nu=SN(sel,var); Sr,Nr=SN(rural,var)
    e=dfrom(Su.sum(0),Nu.sum(0),Sr.sum(0),Nr.sum(0)); b=dfrom(W@Su,W@Nu,W@Sr,W@Nr)
    return [float(e),float(np.nanpercentile(b,2.5)),float(np.nanpercentile(b,97.5)),int(sel.sum())]
out={}
urb=(df.dbf>=0.10).values
groups={'green_nobuild':((df.dbf<0.01)&(df.dndvi>=0.05)&(df.b1<0.02)).values,
        'brown_nobuild':((df.dbf<0.01)&(df.dndvi<=-0.02)&(df.b1<0.02)).values,
        'urb_nogreen':(urb&(df.dndvi<0.02).values),'urb_green':(urb&(df.dndvi>=0.02).values)}
u=df[(df.dbf>=0.05)&np.isfinite(df.bh)]
hc=pd.cut(u.bh,[0,5,10,1e4],labels=['low','mid','high'])   # same cuts as Section 3.9
for c in ['low','mid','high']:
    groups['h_'+c]=df.index.isin(u.index[hc==c]).astype(bool)
    out[f'h_{c}_dbf']=float(u.dbf[hc==c].mean())
for nm,sel in groups.items():
    for var in ['tn','td']: out[f'{nm}_{var}']=mdiff(sel,var)
    out[nm+'_dndvi']=float(df.dndvi[sel].mean()); out[nm+'_n']=int(sel.sum())
    print(nm,out[f'{nm}_tn'][:3],out[f'{nm}_td'][:3])
# ---- urban minus rural annual series (SMOD rural reference, coast matched)
dist=L['dist']; dbin=np.digitize(dist,[5,10,20,40,80])
mask=L['uae']&L['land']
U=mask&((L['bf2020']-L['bf1995'])>=0.10)
R=np.zeros_like(mask)
R[iy[rural],ix[rural]]=True
w=np.bincount(dbin[U],minlength=6)/U.sum()
ts={}
for var in ['night','day']:
    A=C[var+'_anom']; rows=[]
    for i,y in enumerate(C['years']):
        a=A[i]; num=0;den=0;nu=0;nr=0
        for k in range(6):
            if w[k]==0: continue
            uu=np.nanmean(a[U&(dbin==k)]); rr=np.nanmean(a[R&(dbin==k)])
            if np.isfinite(uu) and np.isfinite(rr): nu+=w[k]*uu; nr+=w[k]*rr; den+=w[k]
        rows.append((y,nu/den,nr/den) if den>0 else (y,np.nan,np.nan))
    t=pd.DataFrame(rows,columns=['year',var+'_urban',var+'_rural']); t[var+'_diff']=t[var+'_urban']-t[var+'_rural']
    ts[var]=t.set_index('year')
T=pd.concat(ts.values(),axis=1).reset_index()
T.to_csv('ts_v2.csv',index=False)
import pymannkendall as mk
def sen_xy(x,y):
    ok=np.isfinite(y); x=np.asarray(x,float)[ok]; y=np.asarray(y,float)[ok]
    i,j=np.triu_indices(len(x),1); d=x[j]-x[i]
    return float(np.median((y[j]-y[i])[d!=0]/d[d!=0]))*10, float(mk.hamed_rao_modification_test(y).p)
for var in ['night','day']:
    v=T[['year',var+'_diff']].dropna()
    s,p=sen_xy(v.year.values,v[var+'_diff'].values); out[f'ts_{var}']=[s,p]
    print('ts',var,round(s,3),'p=%.2g'%p)
    for a,b in [(1995,2002),(2003,2011),(2013,2024)]:
        vv=v[(v.year>=a)&(v.year<=b)]; out[f'ts_{var}_{a}_{b}']=sen_xy(vv.year.values,vv[var+'_diff'].values)[0]
# ---- 0.25 degree model-grid cells
LAT,LON=np.meshgrid(lat,lon,indexing='ij')
tn=np.full(LAT.shape,np.nan); td=np.full(LAT.shape,np.nan); en=np.full(LAT.shape,np.nan); dbf=np.full(LAT.shape,np.nan)
tn[iy,ix]=df.tn; td[iy,ix]=df.td; en[iy,ix]=df.en; dbf[iy,ix]=df.dbf
nex=np.load('nex/ACCESS-CM2.npz'); cl=nex['lat']; co=nex['lon']
cells=[]
for la in cl:
    for lo in co:
        box=(abs(LAT-la)<=0.125)&(abs(LON-lo)<=0.125)&mask
        if box.sum()<300: continue
        cells.append(dict(lat=float(la),lon=float(lo),dbf=float(np.nanmean(dbf[box])),tn=float(np.nanmean(tn[box])),
                          td=float(np.nanmean(td[box])),en=float(np.nanmean(en[box]))))
CC=pd.DataFrame(cells)
X=sm.add_constant(CC[['dbf']]*10)
f=sm.OLS(CC.tn,X).fit(); g=sm.OLS(CC.en,X).fit()
out['cell_obs']=[float(f.params['dbf']),float(f.pvalues['dbf']),len(CC)]; out['cell_e5']=[float(g.params['dbf']),float(g.pvalues['dbf'])]
CC.to_csv('cells_v2.csv',index=False)
print('cells',len(CC),'obs slope per 10pp %.2f (p=%.1e)'%(f.params['dbf'],f.pvalues['dbf']),'era5l %.2f'%g.params['dbf'])
# NEX per-model slopes at cells
sl=[]
for fn in sorted(glob.glob('nex/*.npz')):
    d=np.load(fn); y=d['years']; s=(y>=1995)&(y<=2024)
    A=d['tasmin'][s]; x=y[s].astype(float); x=x-x.mean()
    tr=(A*x[:,None,None]).sum(0)/(x**2).sum()*10
    v=[]
    for _,r in CC.iterrows():
        i=np.argmin(abs(d['lat']-r.lat)); j=np.argmin(abs(d['lon']-r.lon)); v.append(tr[i,j])
    v=np.array(v); ok=np.isfinite(v)
    if ok.sum()<len(CC)*0.8: continue
    ff=sm.OLS(v[ok],sm.add_constant(CC.dbf.values[ok]*10)).fit(); sl.append(float(ff.params[1]))
out['cell_nex']=[float(np.median(sl)),float(np.percentile(sl,5)),float(np.percentile(sl,95)),len(sl)]
print('nex cell slope median %.2f (5-95%%: %.2f, %.2f) n=%d'%tuple(out['cell_nex']))
json.dump(out,open('groups_v2.json','w'),indent=1)
