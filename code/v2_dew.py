import netCDF4 as nc,glob,numpy as np,pandas as pd
names={'411840':'Ras Al Khaimah','411940':'Dubai','411960':'Sharjah','411980':'Fujairah','412160':'Al Bateen','412170':'Abu Dhabi','412180':'Al Ain'}
B0,B1,Y0,Y1=1991,2020,1995,2024
def sen_xy(x,y):
    ok=np.isfinite(y); x=np.asarray(x,float)[ok]; y=np.asarray(y,float)[ok]
    i,j=np.triu_indices(len(x),1); d=x[j]-x[i]
    return float(np.median((y[j]-y[i])[d!=0]/d[d!=0]))*10
rows=[]
for f in sorted(glob.glob('hadisd/*.nc')):
    sid=f.split('_')[-1][:6]
    if sid not in names: continue
    d=nc.Dataset(f); t=d['time'][:].astype('f8')
    T=np.ma.filled(d['temperatures'][:].astype('f8'),np.nan); Td=np.ma.filled(d['dewpoints'][:].astype('f8'),np.nan)
    T[T<-50]=np.nan; Td[Td<-80]=np.nan
    ts=pd.Timestamp('1931-01-01')+pd.to_timedelta(t,'h')+pd.Timedelta(hours=4)
    x=pd.DataFrame({'ts':ts,'T':T,'Td':Td}); x=x[(x.ts.dt.year>=B0)&(x.ts.dt.year<=Y1)]
    x['date']=x.ts.dt.floor('D'); x['h']=x.ts.dt.hour
    g=x.dropna(subset=['T']).groupby('date')
    day=pd.DataFrame({'n':g.T.size(),'tmin':g.T.min(),'night':g.h.apply(lambda h:((h>=0)&(h<=7)).any()),'aft':g.h.apply(lambda h:((h>=11)&(h<=16)).any())})
    day=day[(day.n>=6)&day.night&day.aft]
    nt=x[(x.h>=0)&(x.h<=6)].dropna(subset=['Td'])
    dew=nt.groupby(nt.ts.dt.floor('D')).Td.mean(); day['dew']=dew.reindex(day.index)
    mo=day.groupby([day.index.year,day.index.month]).agg(tmin=('tmin','mean'),dew=('dew','mean'),n=('tmin','size'))
    mo=mo[mo.n>=20].rename_axis(['y','m']).reset_index()
    for v in ['tmin','dew']:
        base=mo[(mo.y>=B0)&(mo.y<=B1)].groupby('m')[v].mean()
        mo[v+'_a']=mo[v]-mo.m.map(base)
    a=mo.groupby('y').agg(tmin=('tmin_a','mean'),dew=('dew_a','mean'),nm=('m','size'))
    a=a[(a.nm>=10)&(a.index>=Y0)&(a.index<=Y1)].dropna()
    xx=a.index.values.astype(float)
    b=np.polyfit(a.dew-a.dew.mean(),a.tmin-a.tmin.mean(),1)[0]
    rows.append(dict(name=names[sid],dew_trend=sen_xy(xx,a.dew.values),tmin=sen_xy(xx,a.tmin.values),
                     tmin_dewadj=sen_xy(xx,(a.tmin-b*(a.dew-a.dew.mean())).values),beta=b,n=len(a)))
R=pd.DataFrame(rows); print(R.round(3).to_string()); R.to_csv('dew_v2.csv',index=False)
