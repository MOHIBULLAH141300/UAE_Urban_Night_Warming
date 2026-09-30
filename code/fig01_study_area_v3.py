import os, json, sys, numpy as np, rasterio
from rasterio.warp import reproject, Resampling
from rasterio.transform import from_origin
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patheffects
from matplotlib.patches import Patch, Rectangle
sys.path.insert(0, os.path.expanduser('~/ghs'))
from shp import read_shp

H=os.path.expanduser('~')
GB=f'{H}/mnt/ADAM DATA part2/newly donwloaded1/GHS_POP_Urban/UAE_clipped/GHS_BUILT_S/'
SMOD=f'{H}/ghs/GHS_SMOD_E2020_GLOBE_R2023A_54009_1000_V1_0.tif'
SHP=f'{H}/mnt/ADAM DATA PART 1/xin hong/UAE/'
OUT=f'{H}/ghs/out'; os.makedirs(OUT, exist_ok=True)
BJ=f'{H}/mnt/TEMPERATUTE PAPER A/TEMPERATURE PAPER ONLY/results/builtup_v2.json'

def builtup(year):
    with rasterio.open(GB+f'GHS_BUILT_S_E{year}_GLOBE_R2023A_4326_30ss_V1_0.tif') as s:
        a=s.read(1).astype('float64'); prof=s.profile; T=s.transform
    a[a<0]=np.nan
    return a, T, prof
b95,T,prof=builtup(1995); b20,_,_=builtup(2020)
Hh,Ww=b95.shape
lon=T.c+(np.arange(Ww)+0.5)*T.a
lat=T.f+(np.arange(Hh)+0.5)*T.e
dx=abs(T.a)*111320.0*np.cos(np.deg2rad(lat)); dy=abs(T.e)*110574.0
area=(dx*dy)[:,None]
bf95=np.clip(b95/area,0,1); bf20=np.clip(b20/area,0,1)
d=(bf20-bf95)*100.0
ext=[lon[0]-abs(T.a)/2, lon[-1]+abs(T.a)/2, lat[-1]+T.e/2, lat[0]-T.e/2]

# SMOD 2020 urban centres on the same grid
uc=np.zeros((Hh,Ww),'float32')
with rasterio.open(SMOD) as s:
    reproject(rasterio.band(s,1), uc, dst_transform=T, dst_crs='EPSG:4326', resampling=Resampling.nearest)
uc=(uc>=30).astype(float)

# restrict to UAE land using the GADM national outline
from matplotlib.path import Path as MplPath
from shp import read_shp as _rs
_g0=[r for sh in _rs(SHP+'gadm41_ARE_0.shp') for r in sh]
LO,LA=np.meshgrid(lon,lat); pts=np.column_stack([LO.ravel(),LA.ravel()])
inside=np.zeros(pts.shape[0],bool)
for r in _g0:
    if len(r)>3: inside |= MplPath(np.asarray(r)).contains_points(pts)
uae=inside.reshape(LO.shape)
bf95=np.where(uae,bf95,np.nan); bf20=np.where(uae,bf20,np.nan)
d=np.where(uae,d,np.nan); uc=np.where(uae,uc,0.0)

# coarse land mask for the Gulf locator
res=0.05; x0,x1,y0,y1=42.0,64.0,10.0,34.0
nw=int((x1-x0)/res); nh=int((y1-y0)/res)
loc=np.zeros((nh,nw),'float32'); Tl=from_origin(x0,y1,res,res)
with rasterio.open(SMOD) as s:
    reproject(rasterio.band(s,1), loc, dst_transform=Tl, dst_crs='EPSG:4326', resampling=Resampling.nearest)
land=(loc>=11).astype(float)

g0=[r for sh in read_shp(SHP+'gadm41_ARE_0.shp') for r in sh]
g1=[r for sh in read_shp(SHP+'gadm41_ARE_1.shp') for r in sh]
ST=[('DXB','Dubai International',25.255,55.364,(-0.44,-0.17)),
    ('SHJ','Sharjah International',25.329,55.517,(0.09,0.10)),
    ('AUH','Abu Dhabi International',24.433,54.651,(0.10,-0.20)),
    ('AZI','Al Bateen',24.428,54.458,(-0.52,0.12)),
    ('AAN','Al Ain International',24.262,55.609,(0.07,0.05)),
    ('RAK','Ras Al Khaimah International',25.613,55.939,(-0.52,0.05)),
    ('FJR','Fujairah International',25.112,56.324,(-0.10,-0.22))]
BU=json.load(open(BJ))

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'axes.linewidth':0.6,
                     'axes.titlesize':9.5,'axes.titleweight':'bold','savefig.dpi':600})
SEA='#dfe9f2'; OLD='#b9b9b9'; UCC='#1a9850'
fig=plt.figure(figsize=(7.48,7.3))
gs=fig.add_gridspec(2,2,height_ratios=[2.55,1.0],width_ratios=[1.12,1.0],
                    hspace=0.30,wspace=0.24,left=0.072,right=0.985,top=0.955,bottom=0.075)
a=fig.add_subplot(gs[0,:]); a.set_facecolor(SEA)
a.imshow(np.where(np.isfinite(bf95),1.0,np.nan),extent=ext,cmap='Greys',vmin=0,vmax=6,interpolation='nearest')
a.imshow(np.where(bf95>=0.05,1.0,np.nan),extent=ext,cmap=matplotlib.colors.ListedColormap([OLD]),interpolation='nearest')
im=a.imshow(np.where(d>=1,d,np.nan),extent=ext,cmap='magma_r',vmin=0,vmax=25,interpolation='nearest')
a.contour(lon,lat,uc,levels=[0.5],colors=UCC,linewidths=0.7)
for r in g1: a.plot(*zip(*r),color='0.45',lw=0.4,zorder=3)
for r in g0: a.plot(*zip(*r),color='k',lw=0.45,zorder=4)
for code,_,la,lo,off in ST:
    a.plot(lo,la,'^',ms=6,mfc='deepskyblue',mec='k',mew=0.6,zorder=6)
    a.text(lo+off[0],la+off[1],code,fontsize=7.5,weight='bold',zorder=7,
           path_effects=[matplotlib.patheffects.withStroke(linewidth=2,foreground='white')])
a.set_xlim(51.4,56.55); a.set_ylim(22.5,26.2)
a.set_xlabel('Longitude (°E)'); a.set_ylabel('Latitude (°N)')
a.set_title('a   Urban growth 1995–2020 and the station network',loc='left')
# scale bar
km=100.0; dlon=km/(111.32*np.cos(np.deg2rad(23.2)))
a.plot([52.15,52.15+dlon],[22.80,22.80],color='k',lw=2,solid_capstyle='butt',zorder=8)
a.text(52.15+dlon/2,22.88,'100 km',ha='center',fontsize=7,zorder=8)
# locator inset (Gulf region, Natural Earth 1:50m)
import json as _json
CT=_json.load(open(os.path.expanduser('~/ghs/gulf_countries.json')))
ins=a.inset_axes([0.008,0.555,0.305,0.435])
ins.set_facecolor('#cfe0ef')
for iso,v in CT.items():
    for r in v['rings']:
        xs=[c[0] for c in r]; ys=[c[1] for c in r]
        ins.fill(xs,ys,color='#ece7de',lw=0,zorder=1)
        ins.plot(xs,ys,color='0.55',lw=0.35,zorder=2)
for r in [rr for rr in CT['ARE']['rings']]:
    xs=[c[0] for c in r]; ys=[c[1] for c in r]
    ins.fill(xs,ys,color='#f3c0b8',lw=0,zorder=3); ins.plot(xs,ys,color='#b3251b',lw=0.8,zorder=4)
LBL=[('IRAN',54.0,29.6,6.2,'k'),('SAUDI ARABIA',46.3,22.6,6.2,'k'),('OMAN',57.6,20.6,6.2,'k'),
     ('QATAR',50.0,25.9,5.6,'k'),('YEMEN',46.2,15.0,6.2,'k'),('U.A.E.',55.6,23.2,5.6,'#b3251b')]
for t,x,y,fs,c in LBL:
    ins.text(x,y,t,fontsize=fs,weight='bold',color=c,ha='center',va='center',zorder=6)
ins.text(50.9,28.4,'Persian / Arabian Gulf',fontsize=5.4,style='italic',color='#2e6da4',ha='center',va='center',rotation=-30,zorder=6)
ins.text(59.6,24.4,'Gulf of\nOman',fontsize=5.4,style='italic',color='#2e6da4',ha='center',va='center',zorder=6)
ins.add_patch(Rectangle((51.4,22.5),5.15,3.7,fill=False,ec='k',lw=0.9,zorder=7))
ins.set_xlim(43.5,61.5); ins.set_ylim(12.5,31.5); ins.set_xticks([]); ins.set_yticks([])
for s_ in ins.spines.values(): s_.set_linewidth(0.7)
# north arrow on the main map
a.annotate('', xy=(53.62,25.92), xytext=(53.62,25.45),
           arrowprops=dict(arrowstyle='-|>',color='k',lw=1.1))
a.text(53.62,25.98,'N',fontsize=8,weight='bold',ha='center',va='bottom')
# panel b
b=fig.add_subplot(gs[1,0])
ep=BU['ep']; km2=BU['km2']; ucv=BU['urban_centre']
b.plot(ep,km2,'o-',color='#7a1f5c',ms=3.5,lw=1.2,label='Built-up surface')
ok=[(e,v) for e,v in zip(ep,ucv) if v==v and v is not None]
b.plot([e for e,_ in ok],[v for _,v in ok],'s--',color=UCC,ms=3.5,lw=1.2,label='Land in UN urban centres')
b.axvspan(1995,2024,color='0.9',zorder=0)
b.text(2009,max(km2)*0.28,'analysis period\n1995–2024',ha='center',fontsize=7,color='0.35')
b.set_ylabel('Area (km²)'); b.set_xlabel('GHSL epoch')
b.set_title('b   Built-up surface by epoch',loc='left')
b.spines[['top','right']].set_visible(False); b.tick_params(labelsize=7.5)
b.legend(frameon=False,fontsize=7,loc='upper left')
# legend panel
lg=fig.add_subplot(gs[1,1]); lg.axis('off')
cax=lg.inset_axes([0.03,0.90,0.94,0.07])
cb=fig.colorbar(im,cax=cax,orientation='horizontal')
cb.ax.tick_params(labelsize=7,pad=1.5)
cb.set_label('Built-up fraction added 1995\u20132020 (pp)',fontsize=7.2,labelpad=2)
h=[Patch(facecolor=OLD,edgecolor='none',label='Already \u22655% built up in 1995'),
   Line2D([0],[0],color=UCC,lw=1.2,label='UN urban centre, 2020 (GHS-SMOD)'),
   Line2D([0],[0],marker='^',color='none',mfc='deepskyblue',mec='k',ms=7,label='HadISD station'),
   Line2D([0],[0],color='k',lw=0.9,label='National boundary'),
   Line2D([0],[0],color='0.45',lw=0.5,label='Emirate boundary'),
   Patch(facecolor=SEA,edgecolor='0.6',label='Sea')]
lg.legend(handles=h,loc='upper left',bbox_to_anchor=(0.0,0.68),frameon=False,fontsize=7.0,
          handlelength=1.5,labelspacing=0.40,borderpad=0)
fig.savefig(f'{OUT}/Figure1.png',dpi=600,bbox_inches='tight')
fig.savefig(f'{OUT}/Figure1.pdf',bbox_inches='tight')
print('UAE built-up km2 1995/2020:', round(float(np.nansum(bf95*area))/1e6,1), round(float(np.nansum(bf20*area))/1e6,1))
