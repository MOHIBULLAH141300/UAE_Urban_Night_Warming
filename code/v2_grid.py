import numpy as np, pandas as pd, statsmodels.api as sm, json
from scipy.ndimage import uniform_filter
from scipy.stats import norm
rng=np.random.default_rng(20260713)
L=np.load('layers.npz'); C=np.load('cci_annual30.npz'); E=np.load('era5land_annual_tmin_tmax.npz')
lat=L['lat'];lon=L['lon']; LAT,LON=np.meshgrid(lat,lon,indexing='ij')
mask=L['uae']&L['land']
Y0,Y1=1995,2024
yrs=C['years']; sel=(yrs>=Y0)&(yrs<=Y1); Yv=yrs[sel].astype(float)

def sen_mk(A,years,minn=20):
    """Theil-Sen slope per decade and Mann-Kendall p with Hamed-Rao correction.
    A: (t, npix) with NaNs."""
    t,n=A.shape
    i,j=np.triu_indices(t,1)
    dy=(years[j]-years[i])[:,None]
    num=A[j]-A[i]
    sl=num/dy
    slope=np.nanmedian(sl,0)*10
    S=np.nansum(np.sign(num),0)
    cnt=np.isfinite(A).sum(0)
    var=cnt*(cnt-1)*(2*cnt+5)/18.0
    # Hamed-Rao correction using lag-1..3 autocorrelation of the detrended series
    Ad=A-np.nanmean(A,0)
    corr=np.ones(n)
    for lag in (1,2,3):
        x1=Ad[:-lag]; x2=Ad[lag:]
        ok=np.isfinite(x1)&np.isfinite(x2)
        num_=np.nansum(np.where(ok,x1*x2,0),0); den=np.nansum(np.where(np.isfinite(Ad),Ad**2,0),0)
        r=np.where(den>0,num_/den,0)
        sig=np.abs(r)>1.96/np.sqrt(np.maximum(cnt,3))
        k=np.arange(1,1+1)
        corr+=np.where(sig,2*(cnt-lag)*(cnt-lag-1)*(cnt-lag-2)/np.maximum(cnt*(cnt-1)*(cnt-2),1)*r,0)
    var=var*np.maximum(corr,0.2)
    z=np.where(S>0,(S-1),np.where(S<0,(S+1),0))/np.sqrt(np.maximum(var,1e-9))
    p=2*(1-norm.cdf(np.abs(z)))
    slope[cnt<minn]=np.nan; p[cnt<minn]=np.nan
    return slope,p

def bh(p):
    q=np.full_like(p,np.nan); ok=np.isfinite(p); pv=p[ok]
    o=np.argsort(pv); r=np.empty_like(o); r[o]=np.arange(1,len(pv)+1)
    qv=pv*len(pv)/r
    qs=np.minimum.accumulate(qv[o][::-1])[::-1]; out=np.empty_like(qv); out[o]=qs
    q[ok]=np.minimum(out,1); return q

idx=np.where(mask.ravel())[0]
res={}
maps={}
for nm,key in [('tn','night_anom'),('td','day_anom'),('tn_s','night_summer'),('tn_w','night_winter'),('td_s','day_summer'),('td_w','day_winter')]:
    A=C[key][sel].reshape(sel.sum(),-1)[:,idx].astype('f8')
    s,p=sen_mk(A,Yv)
    maps[nm]=s; maps[nm+'_p']=p
    if nm in ('tn','td'): maps[nm+'_q']=bh(p)
# ERA5-Land Sen slopes on the same grid/period
ey=E['years']; es=(ey>=Y0)&(ey<=Y1)
el=E['lat'];eo=E['lon']
iy=np.clip(np.round((lat-el[0])/(el[1]-el[0])).astype(int),0,len(el)-1); ix=np.clip(np.round((lon-eo[0])/(eo[1]-eo[0])).astype(int),0,len(eo)-1)
for v,nm in [('tmin','en'),('tmax','ex')]:
    A=E[v][es][:,iy][:,:,ix].reshape(es.sum(),-1)[:,idx].astype('f8')
    s,p=sen_mk(A,ey[es].astype(float))
    maps[nm]=s; maps[nm+'_p']=p
np.savez_compressed('maps_v2.npz',idx=idx,**maps)

# ---- pixel table
bf95=L['bf1995']; bf20=L['bf2020']; dbf=bf20-bf95
nb=uniform_filter(np.nan_to_num(bf20),size=11)
df=pd.DataFrame({k:v for k,v in maps.items() if not k.endswith(('_p','_q'))})
df['tn_q']=maps['tn_q']; df['td_q']=maps['td_q']
flat=lambda a: a.ravel()[idx]
df['b0']=flat(bf95); df['b1']=flat(bf20); df['dbf']=flat(dbf); df['nb']=flat(nb)
df['dist']=flat(L['dist']); df['lat']=flat(LAT); df['lon']=flat(LON); df['emi']=flat(L['emi'])
df['smod95']=flat(L['smod1995']); df['smod20']=flat(L['smod2020'])
# mediators / confounders on the full period
def epoch_diff(A,years,a0,a1,b0,b1):
    return np.nanmean(A[(years>=b0)&(years<=b1)],0)-np.nanmean(A[(years>=a0)&(years<=a1)],0)
df['dndvi']=flat(epoch_diff(L['lsndvi'],L['lsndvi_years'],1995,1999,2020,2024))
df['ndvi0']=flat(np.nanmean(L['lsndvi'][L['lsndvi_years']<=1999],0))
df['dalb']=flat(epoch_diff(L['lsalb'],L['lsalb_years'],1995,1999,2020,2024))
df['alb0']=flat(np.nanmean(L['lsalb'][L['lsalb_years']<=1999],0))
df['dntl']=flat(np.nanmean(L['dmsp'][L['dmsp_years']>=2010],0)-np.nanmean(L['dmsp'][L['dmsp_years']<=1998],0))
df['ntl24']=flat(L['ntl'][-1])
df['dbin']=pd.cut(df.dist,[-1,5,10,20,40,80,1e4],labels=False)
df['blk']=(np.floor(df.lat/0.25)*100+np.floor(df.lon/0.25)).astype(int)
df=df.dropna(subset=['tn','td','en','ex']).reset_index(drop=True)
df.to_pickle('pixels_v2.pkl')
print('pixels',len(df),'blocks',df.blk.nunique())
print('median trends', df[['tn','td','en','ex']].median().round(3).to_dict())
print('FDR-significant night', float((df.tn_q<0.05).mean().round(3)), 'day', float((df.td_q<0.05).mean().round(3)))
