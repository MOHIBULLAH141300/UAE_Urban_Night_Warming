import os,sys,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle
sys.path.insert(0,os.path.expanduser('~/ghs')); from shp import read_shp
H=os.path.expanduser('~'); OUT=f'{H}/ghs/out'
SHP=f'{H}/mnt/ADAM DATA PART 1/xin hong/UAE/'
GB=f'{H}/mnt/ADAM DATA part2/newly donwloaded1/GHS_POP_Urban/UAE_clipped/GHS_BUILT_S/'
D=np.load(f'{OUT}/fig3_fields.npz')
lat=D['lat']; lon=D['lon']; mask=D['mask']; TN=D['tn']; QN=D['qn']; TD=D['td']; QD=D['qd']; TE=D['en']
# built-up change on this grid by nearest-neighbour index mapping
import rasterio
def bf(y):
    with rasterio.open(GB+f'GHS_BUILT_S_E{y}_GLOBE_R2023A_4326_30ss_V1_0.tif') as s:
        a=s.read(1).astype('f8'); T=s.transform
    hh,ww=a.shape
    la=T.f+(np.arange(hh)+0.5)*T.e; lo=T.c+(np.arange(ww)+0.5)*T.a
    ar=(abs(T.a)*111320*np.cos(np.deg2rad(la))*abs(T.e)*110574)[:,None]
    return np.clip(a/ar,0,1),la,lo
b95,la,lo=bf(1995); b20,_,_=bf(2020)
iy=np.clip(np.round((lat-la[0])/(la[1]-la[0])).astype(int),0,len(la)-1)
ix=np.clip(np.round((lon-lo[0])/(lo[1]-lo[0])).astype(int),0,len(lo)-1)
dbf=((b20-b95)[:,ix])[iy,:]*100.0
from scipy.ndimage import uniform_filter
dbf=uniform_filter(np.nan_to_num(dbf),size=5)
g0=[r for sh in read_shp(SHP+'gadm41_ARE_0.shp') for r in sh]
g1=[r for sh in read_shp(SHP+'gadm41_ARE_1.shp') for r in sh]
ST=[('DXB',25.255,55.364),('SHJ',25.329,55.517),('AUH',24.433,54.651),('AZI',24.428,54.458),
    ('AAN',24.262,55.609),('RAK',25.613,55.939),('FJR',25.112,56.324)]
ext=[lon[0],lon[-1],lat[-1],lat[0]]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.linewidth':0.6,
                     'axes.titlesize':8.8,'axes.titleweight':'bold','savefig.dpi':600})
SEA='#dfe9f2'; norm=TwoSlopeNorm(vmin=-1.5,vcenter=0,vmax=2.0); CM='RdBu_r'
ZX=(53.85,56.50); ZY=(23.90,25.95)
def base(ax,zoom=True):
    ax.set_facecolor(SEA)
    for r in g1: ax.plot(*zip(*r),color='0.45',lw=0.35,zorder=3)
    for r in g0: ax.plot(*zip(*r),color='k',lw=0.6,zorder=4)
    if zoom: ax.set_xlim(*ZX); ax.set_ylim(*ZY)
    else: ax.set_xlim(51.4,56.55); ax.set_ylim(22.5,26.2)
def draw(ax,T,Q,title,stip=True):
    im=ax.imshow(np.where(mask,T,np.nan),extent=ext,cmap=CM,norm=norm,interpolation='nearest',zorder=1)
    if stip and Q is not None:
        yy,xx=np.where(mask&np.isfinite(Q)&(Q<0.05))
        s=slice(None,None,55)
        ax.plot(lon[xx][s],lat[yy][s],'.',ms=0.45,color='0.15',alpha=0.55,zorder=2)
    ax.contour(lon,lat,np.where(mask,dbf,0),levels=[10],colors='k',linewidths=0.55,zorder=5)
    base(ax)
    for c,la_,lo_ in ST:
        ax.plot(lo_,la_,'^',ms=4.5,mfc='yellow',mec='k',mew=0.5,zorder=6)
    ax.set_title(title,loc='left')
    return im
fig=plt.figure(figsize=(7.48,5.0))
gs=fig.add_gridspec(2,3,height_ratios=[1.30,1.0],hspace=0.16,wspace=0.16,
                    left=0.062,right=0.988,top=0.95,bottom=0.075)
ax1=fig.add_subplot(gs[0,0]); ax2=fig.add_subplot(gs[0,1],sharey=ax1); ax3=fig.add_subplot(gs[0,2],sharey=ax1)
im=draw(ax1,TN,QN,'a   Night-time LST')
draw(ax2,TD,QD,'b   Day-time LST')
draw(ax3,TE,None,'c   ERA5-Land Tmin',stip=False)
ax1.set_ylabel('Latitude (°N)')
for ax in (ax2,ax3): plt.setp(ax.get_yticklabels(),visible=False)
for ax in (ax1,ax2,ax3): ax.set_xlabel('Longitude (°E)'); ax.tick_params(labelsize=7)
ax4=fig.add_subplot(gs[1,0])
draw(ax4,TN,None,'d   Night-time LST, whole UAE',stip=False); base(ax4,zoom=False)
ax4.add_patch(Rectangle((ZX[0],ZY[0]),ZX[1]-ZX[0],ZY[1]-ZY[0],fill=False,ec='k',lw=1.0,ls='-',zorder=8))
ax4.set_xlabel('Longitude (°E)'); ax4.set_ylabel('Latitude (°N)'); ax4.tick_params(labelsize=7)
lg=fig.add_subplot(gs[1,1:]); lg.axis('off')
cax=lg.inset_axes([0.06,0.80,0.88,0.075])
cb=fig.colorbar(im,cax=cax,orientation='horizontal',extend='both')
cb.set_label('Theil–Sen trend 1995–2024 (°C decade⁻¹)',fontsize=7.6,labelpad=2); cb.ax.tick_params(labelsize=7)
h=[Line2D([0],[0],marker='.',color='none',mfc='0.15',mec='none',ms=6,label='Trend significant at q < 0.05 (Benjamini–Hochberg)'),
   Line2D([0],[0],color='k',lw=0.55,label='Built-up fraction increased ≥ 10 pp, 1995–2020'),
   Line2D([0],[0],marker='^',color='none',mfc='yellow',mec='k',ms=6,label='HadISD station'),
   Line2D([0],[0],color='k',lw=0.6,label='National boundary'),
   Line2D([0],[0],color='0.45',lw=0.4,label='Emirate boundary'),
   Patch(facecolor=SEA,edgecolor='0.6',label='Sea or outside the UAE'),
   Line2D([0],[0],color='k',lw=1.0,label='Extent of panels a–c (shown in d)')]
lg.legend(handles=h,loc='upper left',bbox_to_anchor=(0.03,0.60),frameon=False,fontsize=7.2,
          handlelength=1.6,labelspacing=0.45,borderpad=0)
fig.savefig(f'{OUT}/Figure3.png',dpi=600,bbox_inches='tight')
fig.savefig(f'{OUT}/Figure3.pdf',bbox_inches='tight')
print('ok')
