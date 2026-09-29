import numpy as np,pandas as pd,statsmodels.api as sm,json
L=np.load('layers.npz'); lat=L['lat'];lon=L['lon']
df=pd.read_pickle('pixels_v2.pkl')
iy=np.round((lat[0]-df.lat.values)/(lat[0]-lat[1])).astype(int); ix=np.round((df.lon.values-lon[0])/(lon[1]-lon[0])).astype(int)
flat=lambda a: a[iy,ix]
def ep(A,years,a0,a1,b0,b1): return np.nanmean(A[(years>=b0)&(years<=b1)],0)-np.nanmean(A[(years>=a0)&(years<=a1)],0)
df=df.copy()
df['m_dndvi']=flat(ep(L['ndvi'],L['ndvi_years'],2000,2004,2020,2024))
df['m_dalb']=flat(ep(L['alb'],L['alb_years'],2001,2005,2020,2024))
df['viirs']=flat(np.log1p(np.clip(L['ntl'][-1],0,None)))
out=json.load(open('reg_v2.json'))
def reg(d,var,extra=()):
    X=pd.get_dummies(d[['dbin','emi']].astype(str),drop_first=True).astype(float)
    X['dbf']=d.dbf*10; X['b0']=d.b0*10; X['lat']=d.lat; X['lon']=d.lon
    for e in extra: X[e]=d[e]
    X=sm.add_constant(X); return sm.OLS(d[var],X).fit(cov_type='cluster',cov_kwds={'groups':d.blk})
d=df.dropna(subset=['m_dndvi','m_dalb','viirs'])
for var in ['tn','td']:
    for nm,extra in [('base',()),('modis_ndvi',('m_dndvi',)),('modis_alb',('m_dalb',)),('viirs',('viirs',)),('modis_all',('m_dndvi','m_dalb','viirs'))]:
        f=reg(d,var,extra); ci=f.conf_int()
        out[f'{var}_{nm}_modis']=dict(dbf=float(f.params['dbf']),lo=float(ci.loc['dbf',0]),hi=float(ci.loc['dbf',1]),
                                      **{e:[float(f.params[e]),float(ci.loc[e,0]),float(ci.loc[e,1])] for e in extra})
        print(var,nm,round(f.params['dbf'],3),{e:round(f.params[e],3) for e in extra})
# surface change by dBF class (for the figure)
rural=df.rural
cl={}
for g,sel in [('rural',rural)]+[(l,df.grp==l) for l in ['2-5','5-10','10-20','>=20']]:
    cl[g]=dict(n=int(sel.sum()),dalb_ls=float(df.dalb[sel].mean()),dndvi_ls=float(df.dndvi[sel].mean()),
               dalb_modis=float(df.m_dalb[sel].mean()),dndvi_modis=float(df.m_dndvi[sel].mean()),
               dmsp=float(df.dntl[sel].mean()),viirs=float(np.expm1(df.viirs[sel]).median()))
json.dump(cl,open('classes_v2.json','w'),indent=1); print(pd.DataFrame(cl).T.round(3).to_string())
json.dump(out,open('reg_v2.json','w'),indent=1)
# ---- AR6 scenario table
fut=json.load(open('nex_ar6.json'))
base={}
import glob,os
for f in sorted(glob.glob('nex/*.npz')):
    m=os.path.basename(f)[:-4]; d=np.load(f); la=d['lat'];lo=d['lon']
    bx=(la[:,None]>=22.6)&(la[:,None]<=26.1)&(lo[None,:]>=51.5)&(lo[None,:]<=56.4)
    y=d['years']; s=(y>=1995)&(y<=2014)
    base[m]=float(np.mean([np.nanmean(np.where(bx,a,np.nan)) for a in d['tasmin'][s]]))
rows=[]
for k,v in fut.items():
    m,sc,pn=k.split('|')
    if v is None or v.get('tasmin') is None or m not in base: continue
    rows.append(dict(model=m,ssp=sc,period=pn,dtmin=v['tasmin']-base[m]))
A=pd.DataFrame(rows)
A=A[(A.dtmin>-5)&(A.dtmin<12)]
S=A.groupby(['ssp','period']).dtmin.agg(['count','median',lambda x: np.percentile(x,5),lambda x: np.percentile(x,95)])
S.columns=['n','median','p5','p95']
order={'near':0,'mid':1,'long':2}
S=S.reset_index(); S['o']=S.period.map(order); S=S.sort_values(['ssp','o']).drop(columns='o')
print(S.round(2).to_string())
S.to_csv('ar6_tmin.csv',index=False); A.to_csv('ar6_models.csv',index=False)
