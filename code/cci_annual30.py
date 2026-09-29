import numpy as np
L=np.load('layers.npz')
out={}
for tag in ['NIGHT','DAY']:
    d=np.load(f'cci_{tag}_monthly_raw.npz'); a=d['lst']; ym=d['ym']; clat=d['lat'].astype('f8'); clon=d['lon'].astype('f8')
    iy=np.clip(np.round((L['lat']-clat[0])/np.diff(clat).mean()).astype(int),0,len(clat)-1)
    ix=np.clip(np.round((L['lon']-clon[0])/np.diff(clon).mean()).astype(int),0,len(clon)-1)
    a=a[:,iy][:,:,ix]
    X=np.where(a==-32768,np.nan,a*0.01).astype('f4')
    mon=ym[:,1]; yr=ym[:,0]
    # climatological reference: 1995-2020 (longest overlap with the 1991-2020 WMO normal)
    ref=(yr>=1995)&(yr<=2020)
    clim=np.stack([np.nanmean(X[ref&(mon==k)],0) for k in range(1,13)])
    cnt=np.stack([np.isfinite(X[ref&(mon==k)]).sum(0) for k in range(1,13)])
    clim[cnt<8]=np.nan
    an=X-clim[mon-1]
    yrs=np.arange(1995,2025)
    A=np.full((len(yrs),)+X.shape[1:],np.nan,'f4'); N=np.zeros((len(yrs),)+X.shape[1:],'i1')
    for i,y in enumerate(yrs):
        s=yr==y; c=np.isfinite(an[s]).sum(0)
        A[i]=np.where(c>=6,np.nanmean(an[s],0),np.nan); N[i]=c
    out[tag.lower()+'_anom']=A; out[tag.lower()+'_n']=N; out[tag.lower()+'_clim']=np.nanmean(clim,0)
    sy=yr+(mon==12)
    for sname,months in [('summer',[6,7,8,9]),('winter',[12,1,2,3])]:
        S=np.full((len(yrs),)+X.shape[1:],np.nan,'f4')
        for i,y in enumerate(yrs):
            s=(sy==y)&np.isin(mon,months); c=np.isfinite(an[s]).sum(0)
            S[i]=np.where(c>=2,np.nanmean(an[s],0),np.nan)
        out[f'{tag.lower()}_{sname}']=S
out['years']=np.arange(1995,2025)
np.savez_compressed('cci_annual30.npz',**out)
m=L['uae']&L['land']
print({k:v.shape for k,v in out.items()})
print('years with data (UAE mean):')
for i,y in enumerate(out['years']):
    print(y, round(float(np.nanmean(out['night_anom'][i][m])),2), int(np.isfinite(out['night_anom'][i][m]).sum()))
