import os,sys,numpy as np
from scipy.stats import norm
sys.path.insert(0,os.path.expanduser('~/ghs')); from shp import read_shp
H=os.path.expanduser('~'); U=f'{H}/mnt/TEMPERATUTE PAPER A/urban_analysis/'
SHP=f'{H}/mnt/ADAM DATA PART 1/xin hong/UAE/'
GB=f'{H}/mnt/ADAM DATA part2/newly donwloaded1/GHS_POP_Urban/UAE_clipped/GHS_BUILT_S/'
OUT=f'{H}/ghs/out'; os.makedirs(OUT,exist_ok=True)
Y0,Y1=1995,2024; yrs=np.arange(Y0,Y1+1)

def annual(tag):
    d=np.load(U+f'cci_{tag}_monthly_raw.npz'); a=d['lst']; ym=d['ym']
    lat=d['lat'].astype('f8'); lon=d['lon'].astype('f8')
    X=np.where(a==-32768,np.nan,a*0.01).astype('f4')
    mon=ym[:,1]; yr=ym[:,0]; ref=(yr>=1995)&(yr<=2020)
    clim=np.stack([np.nanmean(X[ref&(mon==k)],0) for k in range(1,13)])
    cnt=np.stack([np.isfinite(X[ref&(mon==k)]).sum(0) for k in range(1,13)])
    clim[cnt<8]=np.nan
    an=X-clim[mon-1]
    A=np.full((len(yrs),)+X.shape[1:],np.nan,'f4')
    for i,y in enumerate(yrs):
        s=yr==y; c=np.isfinite(an[s]).sum(0)
        A[i]=np.where(c>=6,np.nanmean(an[s],0),np.nan)
    return A,lat,lon
NI,lat,lon=annual('NIGHT'); DA,_,_=annual('DAY')
np.seterr(all='ignore')

def sen_mk(A,years,minn=20):
    t,n=A.shape; i,j=np.triu_indices(t,1); dy=(years[j]-years[i])[:,None]
    num=A[j]-A[i]; slope=np.nanmedian(num/dy,0)*10
    S=np.nansum(np.sign(num),0); cnt=np.isfinite(A).sum(0)
    var=cnt*(cnt-1)*(2*cnt+5)/18.0
    Ad=A-np.nanmean(A,0); corr=np.ones(n)
    for lag in (1,2,3):
        x1=Ad[:-lag]; x2=Ad[lag:]; ok=np.isfinite(x1)&np.isfinite(x2)
        num_=np.nansum(np.where(ok,x1*x2,0),0); den=np.nansum(np.where(np.isfinite(Ad),Ad**2,0),0)
        r=np.where(den>0,num_/den,0); sig=np.abs(r)>1.96/np.sqrt(np.maximum(cnt,3))
        corr+=np.where(sig,2*(cnt-lag)*(cnt-lag-1)*(cnt-lag-2)/np.maximum(cnt*(cnt-1)*(cnt-2),1)*r,0)
    var=var*np.maximum(corr,0.2)
    z=np.where(S>0,S-1,np.where(S<0,S+1,0))/np.sqrt(np.maximum(var,1e-9))
    p=2*(1-norm.cdf(np.abs(z))); slope[cnt<minn]=np.nan; p[cnt<minn]=np.nan
    return slope,p
def bh(p):
    q=np.full_like(p,np.nan); ok=np.isfinite(p); pv=p[ok]
    o=np.argsort(pv); qv=pv*len(pv)/ (np.argsort(o)+1)
    qs=np.minimum.accumulate((pv*len(pv)/(np.arange(1,len(pv)+1)))[o][::-1])[::-1]
    out=np.empty_like(pv); out[o]=qs; q[ok]=np.minimum(out,1); return q
def trend(A,mask,years):
    idx=np.where(mask.ravel())[0]; F=A.reshape(len(years),-1)[:,idx].astype('f8')
    sl=np.full(idx.size,np.nan); pv=np.full(idx.size,np.nan)
    for k in range(0,idx.size,20000):
        s,p=sen_mk(F[:,k:k+20000],years.astype(float)); sl[k:k+20000]=s; pv[k:k+20000]=p
    S=np.full(mask.size,np.nan); P=np.full(mask.size,np.nan); Q=np.full(mask.size,np.nan)
    S[idx]=sl; P[idx]=pv; Q[idx]=bh(pv)
    return S.reshape(mask.shape),Q.reshape(mask.shape)

# UAE mask
from matplotlib.path import Path as MplPath
g0=[r for sh in read_shp(SHP+'gadm41_ARE_0.shp') for r in sh]
g1=[r for sh in read_shp(SHP+'gadm41_ARE_1.shp') for r in sh]
LO,LA=np.meshgrid(lon,lat); pts=np.column_stack([LO.ravel(),LA.ravel()])
ins=np.zeros(pts.shape[0],bool)
for r in g0:
    if len(r)>3: ins |= MplPath(np.asarray(r)).contains_points(pts)
uae=ins.reshape(LO.shape)
mask=uae&np.isfinite(NI).sum(0).astype(bool)&(np.isfinite(NI).sum(0)>=20)
TN,QN=trend(NI,mask,yrs); TD,QD=trend(DA,mask,yrs)
E=np.load(U+'era5land_annual_tmin_tmax.npz'); ey=E['years'] if 'years' in E.files else np.arange(1978,1978+E['tmin'].shape[0])
es=(ey>=Y0)&(ey<=Y1); el=E['lat'].astype('f8'); eo=E['lon'].astype('f8')
iy=np.clip(np.round((lat-el[0])/(el[1]-el[0])).astype(int),0,len(el)-1)
ix=np.clip(np.round((lon-eo[0])/(eo[1]-eo[0])).astype(int),0,len(eo)-1)
EN=E['tmin'][es][:,iy][:,:,ix]
TE,_=trend(EN,mask,ey[es])
# GHSL built-up change on this grid
import rasterio
from rasterio.warp import reproject,Resampling
from rasterio.transform import from_origin
def bf(y):
    with rasterio.open(GB+f'GHS_BUILT_S_E{y}_GLOBE_R2023A_4326_30ss_V1_0.tif') as s:
        a=s.read(1).astype('f8'); T=s.transform; hh,ww=a.shape
    la=T.f+(np.arange(hh)+0.5)*T.e
    ar=(abs(T.a)*111320*np.cos(np.deg2rad(la))*abs(T.e)*110574)[:,None]
    return np.clip(a/ar,0,1),T
b95,T95=bf(1995); b20,_=bf(2020)
dbf=np.zeros_like(TN)
Tg=from_origin(lon[0]-abs(lon[1]-lon[0])/2, lat[0]+abs(lat[1]-lat[0])/2, abs(lon[1]-lon[0]), abs(lat[1]-lat[0]))
reproject((b20-b95).astype('f4'),dbf,src_transform=T95,src_crs='EPSG:4326',dst_transform=Tg,dst_crs='EPSG:4326',resampling=Resampling.bilinear)
np.savez_compressed(f'{OUT}/fig3_fields.npz',lat=lat,lon=lon,mask=mask,tn=TN,qn=QN,td=TD,qd=QD,en=TE,dbf=dbf)
m=mask&np.isfinite(TN)
print('pixels',int(m.sum()))
print('median night %.3f day %.3f era5 %.3f'%(np.nanmedian(TN[m]),np.nanmedian(TD[m]),np.nanmedian(TE[m])))
r=m&(dbf<0.005)&(b95.shape and True)
print('low-growth (dbf<0.5pp) median night %.3f era5 %.3f n=%d'%(np.nanmedian(TN[r]),np.nanmedian(TE[r]),int(r.sum())))
print('FDR sig night %.3f day %.3f'%(np.nanmean(QN[m]<0.05),np.nanmean(QD[m]<0.05)))
