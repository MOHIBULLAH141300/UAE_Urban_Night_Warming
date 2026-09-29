"""Station analysis on WMO/ETCCDI conventions:
   trend period 1995-2024 (30 yr), anomalies and percentile bases 1991-2020,
   Theil-Sen + Mann-Kendall (Hamed-Rao), 3-year moving-block bootstrap CIs,
   ETCCDI TN90p (5-day window), TR (Tmin>=20 C) and local TN30."""
import netCDF4 as nc,glob,numpy as np,pandas as pd,pymannkendall as mk,json
rng=np.random.default_rng(20260713)
names={'411840':'Ras Al Khaimah','411940':'Dubai','411945':'Al Maktoum','411960':'Sharjah','411980':'Fujairah','412160':'Al Bateen','412170':'Abu Dhabi','412180':'Al Ain'}
Y0,Y1,B0,B1=1995,2024,1991,2020

def daily_station():
    out={}
    for f in sorted(glob.glob('hadisd/*.nc')):
        sid=f.split('_')[-1][:6]
        d=nc.Dataset(f); t=d['time'][:].astype('f8')
        T=np.ma.filled(d['temperatures'][:].astype('f8'),np.nan); Td=np.ma.filled(d['dewpoints'][:].astype('f8'),np.nan)
        T[T<-50]=np.nan; Td[Td<-80]=np.nan
        ts=pd.Timestamp('1931-01-01')+pd.to_timedelta(t,'h')+pd.Timedelta(hours=4)
        x=pd.DataFrame({'ts':ts,'T':T,'Td':Td}); x=x[(x.ts.dt.year>=B0)&(x.ts.dt.year<=Y1)]
        x['date']=x.ts.dt.floor('D'); x['h']=x.ts.dt.hour
        g=x.dropna(subset=['T']).groupby('date')
        day=pd.DataFrame({'n':g.T.size(),'tmin':g.T.min(),'tmax':g.T.max(),
                          'night':g.h.apply(lambda h:((h>=0)&(h<=7)).any()),'aft':g.h.apply(lambda h:((h>=11)&(h<=16)).any())})
        day=day[(day.n>=6)&day.night&day.aft][['tmin','tmax']]
        nt=x[(x.h>=0)&(x.h<=6)].dropna(subset=['Td'])
        dew=nt.groupby(nt.ts.dt.floor('D')).Td.mean()
        day['dew']=dew.reindex(day.index)
        out[sid]=day
    return out

def annual_anom(day,col):
    m=day[col].groupby([day.index.year,day.index.month]).agg(['mean','size'])
    m=m[m['size']>=20]['mean'].rename_axis(['y','m']).reset_index()
    base=m[(m.y>=B0)&(m.y<=B1)].groupby('m')['mean'].mean()
    m['a']=m['mean']-m.m.map(base)
    a=m.groupby('y').agg(v=('a','mean'),nm=('m','size'))
    return a[a.nm>=10].v

def sen(y,x):
    """Theil-Sen slope per decade using the actual year spacing.

    pymannkendall's sens_slope assumes evenly spaced observations, which inflates the
    slope for a record with an interior gap (Al Bateen, 2001-2009), so the pairwise
    slope is computed on (year, value) pairs directly."""
    y=np.asarray(y,dtype=float); x=np.asarray(x,dtype=float); ok=np.isfinite(y)&np.isfinite(x)
    if ok.sum()<8: return np.nan,np.nan
    yy=y[ok]; xx=x[ok]
    i,j=np.triu_indices(len(xx),1); d=xx[j]-xx[i]
    slope=float(np.median((yy[j]-yy[i])[d!=0]/d[d!=0]))*10
    try: p=mk.hamed_rao_modification_test(yy).p
    except Exception: p=mk.original_test(yy).p
    return slope,p

def sen_xy(x,y):
    i,j=np.triu_indices(len(x),1)
    d=x[j]-x[i]
    return float(np.median((y[j]-y[i])[d!=0]/d[d!=0]))*10

def block_ci(x,y,B=2000,bl=3):
    x=np.asarray(x,dtype=float); y=np.asarray(y,dtype=float)
    ok=np.isfinite(y); x=x[ok]; y=y[ok]; n=len(x)
    if n<8: return (np.nan,np.nan)
    nb=int(np.ceil(n/bl)); out=[]
    for _ in range(B):
        st=rng.integers(0,n-bl+1,nb); idx=np.concatenate([np.arange(s,s+bl) for s in st])[:n]
        idx=idx[idx<n]
        xs=x[idx]; ys=y[idx]
        if len(ys)<8 or np.ptp(xs)==0: continue
        out.append(sen_xy(xs,ys))
    if not out: return (np.nan,np.nan)
    return float(np.percentile(out,2.5)),float(np.percentile(out,97.5))

def etccdi_tn90p(day, base0=B0, base1=B1):
    """ETCCDI TN90p: % of days with Tmin above the calendar-day 90th percentile
    from a 5-day window in the base period."""
    s=day.tmin.dropna()
    doy=s.index.dayofyear.values
    base=s[(s.index.year>=base0)&(s.index.year<=base1)]
    bdoy=base.index.dayofyear.values
    thr=np.full(367,np.nan)
    for d in range(1,367):
        w=np.abs(((bdoy-d+182)%365)-182)<=2
        if w.sum()>=30: thr[d]=np.percentile(base.values[w],90)
    ex=s.values>thr[doy]
    df=pd.DataFrame({'y':s.index.year,'ex':ex})
    g=df.groupby('y').agg(p=('ex','mean'),n=('ex','size'))
    return (g[g.n>=300].p*100)

def counts(day,thr):
    s=day.tmin.dropna(); df=pd.DataFrame({'y':s.index.year,'c':s.values>=thr})
    g=df.groupby('y').agg(c=('c','sum'),n=('c','size'))
    return (g[g.n>=300].c*365/g[g.n>=300].n)

def pettitt(x):
    n=len(x); r=np.argsort(np.argsort(x))+1
    U=np.array([2*np.sum(r[:k])-k*(n+1) for k in range(1,n)])
    K=np.max(np.abs(U)); k=int(np.argmax(np.abs(U)))+1
    p=2*np.exp(-6*K**2/(n**3+n**2))
    return k,float(min(p,1))

day=daily_station()
E=pd.read_csv('e5l_station_daily.csv',dtype={'sid':str})
E2=pd.read_csv('e5l_station_daily_1991_1996.csv',dtype={'sid':str})
E3=pd.read_csv('e5l_station_daily_azi.csv',dtype={'sid':str})
E=pd.concat([E2,E3,E]).drop_duplicates(['sid','day'])
E['date']=pd.to_datetime(E.day,unit='D')
NXa=np.load('nex_station_daily_all.npz'); NXb=np.load('nex_station_daily_azi.npz'); NX9=np.load('nex_station_daily_1991_1995.npz')
NX={k:NXa[k] for k in NXa.files}
for k in NXb.files: NX.setdefault(k,NXb[k])
models=sorted({k.split('|')[0] for k in NX})
M=pd.read_csv('hadisd_meta.csv',dtype={'sid':str}).set_index('sid')
L=np.load('layers.npz'); lat=L['lat'];lon=L['lon']; LAT,LON=np.meshgrid(lat,lon,indexing='ij')

rows=[]
for sid,d in day.items():
    if sid not in names or sid=='411945': continue
    a=annual_anom(d,'tmin'); ax=annual_anom(d,'tmax')
    a=a[(a.index>=Y0)&(a.index<=Y1)]; ax=ax.reindex(a.index)
    if len(a)<0.7*(Y1-Y0+1): 
        print('skip',names[sid],len(a)); continue
    x=a.index.values.astype(float)
    tn,pn=sen(a.values,x); tx,_=sen(ax.values,x)
    ci_n=block_ci(x,a.values); 
    dd=(a-ax).dropna(); ci_d=block_ci(dd.index.values.astype(float),dd.values)
    # ERA5-Land reference, same anomaly base
    e=E[E.sid==sid].set_index('date')
    em=e.tmin.groupby([e.index.year,e.index.month]).mean().rename_axis(['y','m']).reset_index()
    bs=em[(em.y>=B0)&(em.y<=B1)].groupby('m').tmin.mean()
    em['a']=em.tmin-em.m.map(bs); ea=em.groupby('y').a.mean()
    ea=ea.reindex(a.index)
    e_tn,_=sen(ea.values,x)
    ex_series=(a-ea).dropna(); ex_tn=sen(ex_series.values,ex_series.index.values.astype(float))[0]
    ci_e=block_ci(ex_series.index.values.astype(float),ex_series.values)
    # Pettitt on the DETRENDED excess series: a step test applied to a trending
    # series would remove the trend by construction
    xs=ex_series.index.values.astype(float); ys=ex_series.values
    b=sen_xy(xs,ys)/10.0
    resid=ys-b*(xs-xs.mean())
    kk,pp=pettitt(resid)
    adj=ex_series.copy()
    step=resid[kk:].mean()-resid[:kk].mean()
    adj.iloc[kk:]-=step
    ex_adj=sen(adj.values,adj.index.values.astype(float))[0]
    # indices
    tn90=etccdi_tn90p(d); tn90=tn90[(tn90.index>=Y0)&(tn90.index<=Y1)]
    tr=counts(d,20); tr=tr[(tr.index>=Y0)&(tr.index<=Y1)]
    tn30=counts(d,30); tn30=tn30[(tn30.index>=Y0)&(tn30.index<=Y1)]
    # ERA5-Land TN90p with its own base
    ed=e.tmin.rename('tmin').to_frame(); ed.index.name=None
    e_tn90=etccdi_tn90p(ed); e_tn90=e_tn90[(e_tn90.index>=Y0)&(e_tn90.index<=Y1)]
    # NEX TN90p per model
    nex_tn90=[]
    for m_ in (models if f'{models[0]}|{sid}' in NX else []):
        v=np.concatenate([NX9[f'{m_}|{sid}'],NX[f'{m_}|{sid}']]); yr=np.concatenate([NX9[f'{m_}|year'],NX[f'{m_}|year']])
        dates=[]
        for y in range(1991,2025):
            k=(yr==y).sum(); dates+=list(pd.date_range(f'{y}-01-01',periods=k,freq='D'))
        s=pd.DataFrame({'tmin':v},index=pd.DatetimeIndex(dates))
        t90=etccdi_tn90p(s); t90=t90[(t90.index>=Y0)&(t90.index<=Y1)]
        nex_tn90.append(sen(t90.values,t90.index.values.astype(float))[0])
    if not nex_tn90: nex_tn90=[np.nan]
    st=M.loc[sid]
    dist=np.sqrt(((LAT-st.lat)*110.57)**2+((LON-st.lon)*111.32*np.cos(np.deg2rad(st.lat)))**2)
    r5=dist<=5
    rows.append(dict(sid=sid,name=names[sid],lat=st.lat,lon=st.lon,n=len(a),
        coast_km=float(L['dist'][np.unravel_index(np.argmin(dist),dist.shape)]),
        dbf5=float(np.nanmean(L['bf2020'][r5]-L['bf1995'][r5])),
        tmin=tn,tmin_p=pn,tmin_lo=ci_n[0],tmin_hi=ci_n[1],tmax=tx,diff=tn-tx,diff_lo=ci_d[0],diff_hi=ci_d[1],
        e5_tmin=e_tn,excess=ex_tn,excess_lo=ci_e[0],excess_hi=ci_e[1],
        pettitt_year=int(ex_series.index[kk]),pettitt_p=pp,excess_break_adj=ex_adj,
        tn90p=sen(tn90.values,tn90.index.values.astype(float))[0],tn90p_p=sen(tn90.values,tn90.index.values.astype(float))[1],
        e5_tn90p=sen(e_tn90.values,e_tn90.index.values.astype(float))[0],
        nex_tn90p_med=float(np.median(nex_tn90)),nex_tn90p_p5=float(np.percentile(nex_tn90,5)),nex_tn90p_p95=float(np.percentile(nex_tn90,95)),
        nex_tn90p_max=float(np.max(nex_tn90)),
        tr=sen(tr.values,tr.index.values.astype(float))[0],tn30=sen(tn30.values,tn30.index.values.astype(float))[0],
        tn30_9599=float(tn30.loc[1995:1999].mean()),tn30_2024=float(tn30.loc[2020:2024].mean()),
        dew_trend=sen(d.dew.groupby(d.index.year).mean().reindex(a.index).values,x)[0]))
R=pd.DataFrame(rows); pd.set_option('display.width',260)
R.to_csv('station_v2.csv',index=False)
print(R[['name','n','coast_km','dbf5','tmin','tmin_lo','tmin_hi','tmax','diff','e5_tmin','excess','excess_lo','excess_hi','pettitt_year','pettitt_p','excess_break_adj']].round(2).to_string())
print(R[['name','tn90p','e5_tn90p','nex_tn90p_med','nex_tn90p_p95','nex_tn90p_max','tr','tn30','tn30_9599','tn30_2024','dew_trend']].round(2).to_string())
from scipy.stats import spearmanr
Rc=R.dropna(subset=['excess'])
print('n',len(Rc),'excess vs dbf5',spearmanr(Rc.excess,Rc.dbf5),'vs coast',spearmanr(Rc.excess,Rc.coast_km))
print('tn90p vs dbf5',spearmanr(Rc.tn90p,Rc.dbf5))


# ---- merge the per-station NEX-GDDP-CMIP6 ensemble and the model rank -----------------
NX = pd.read_csv('nex_station_v2.csv')
R = pd.read_csv('station_v2.csv').merge(NX, on='name', how='left', suffixes=('_x', '_y'))

# per-model station Tmin trends over the analysis period, for the ensemble rank
Z = np.load('nex_station_daily_all.npz', allow_pickle=True)
models = sorted({k.split('|')[0] for k in Z.files})
sid_of = dict(zip(R.name, R.sid.astype(str)))
rank = {}
for nm, sid in sid_of.items():
    tr = []
    for m in models:
        key = f'{m}|{sid}'
        if key not in Z.files:
            continue
        yr = Z[f'{m}|year']; tn = Z[key]
        d = pd.DataFrame({'y': yr, 't': tn})
        d = d[(d.y >= 1995) & (d.y <= 2024)].groupby('y')['t'].mean()
        if len(d) < 25:
            continue
        tr.append(sen(d.values, d.index.values.astype(float))[0])
    rank[nm] = np.array(tr, dtype=float)
R['rank_pct'] = [100 * float((rank[n] < t).mean()) if len(rank.get(n, [])) else np.nan
                 for n, t in zip(R.name, R.tmin)]
R.to_csv('station_v2.csv', index=False)
print(R[['name', 'tmin', 'nex_med', 'rank_pct']].round(2).to_string(index=False))
