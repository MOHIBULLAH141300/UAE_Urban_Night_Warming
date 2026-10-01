import argparse
from pathlib import Path

import numpy as np
import rasterio
from rasterio.warp import reproject,Resampling
from rasterio.transform import from_origin

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(
    description="Augment a source-derived UAE raster stack with Landsat, DMSP and GHS-SMOD layers."
)
parser.add_argument(
    "--base-layers", type=Path, required=True,
    help="Path to the source-derived base NPZ containing lat, lon, uae and land arrays."
)
parser.add_argument(
    "--gee-dir", type=Path, required=True,
    help="Directory containing the three annual Landsat/DMSP GeoTIFF stacks."
)
parser.add_argument(
    "--smod-dir", type=Path, required=True,
    help="Directory containing GHS_SMOD_E1995, E2000 and E2020 GeoTIFFs."
)
parser.add_argument(
    "--output", type=Path, default=ROOT / "results" / "layers.npz",
    help="Output NPZ path (default: repository results/layers.npz)."
)
args = parser.parse_args()

if not args.base_layers.is_file():
    parser.error(f"Base raster stack not found: {args.base_layers}")

L=dict(np.load(args.base_layers)); lat=L['lat'];lon=L['lon']
dx=np.diff(lon).mean(); dy=-np.diff(lat).mean(); tr=from_origin(lon[0]-dx/2,lat[0]+dy/2,dx,dy); sh=(len(lat),len(lon))
def load_stack(f,clip=None):
    out=[];names=[]
    with rasterio.open(f) as r:
        for b in range(1,r.count+1):
            a=r.read(b).astype('f8'); a[~np.isfinite(a)]=np.nan; a[a<=-999]=np.nan
            if clip is not None: a[(a<clip[0])|(a>clip[1])]=np.nan
            o=np.full(sh,np.nan)
            reproject(a,o,src_transform=r.transform,src_crs=r.crs,dst_transform=tr,dst_crs='EPSG:4326',resampling=Resampling.nearest,src_nodata=np.nan,dst_nodata=np.nan)
            out.append(o); names.append(r.descriptions[b-1])
    return np.array(out,'f4'),np.array([int(n[1:5]) for n in names])
L['lsndvi'],L['lsndvi_years']=load_stack(args.gee_dir/'UAE_Landsat_NDVI_annual_1995_2024.tif',clip=(-0.2,1.0))
L['lsalb'],L['lsalb_years']=load_stack(args.gee_dir/'UAE_Landsat_albedo_annual_1995_2024.tif',clip=(0.02,0.8))
L['dmsp'],L['dmsp_years']=load_stack(args.gee_dir/'UAE_DMSP_nightlights_annual_1996_2013.tif',clip=(0,63))
# UN Degree of Urbanisation (GHS-SMOD): 30 urban centre, 23/22/21 urban cluster/suburban, 13/12/11 rural
for ep in [1995,2000,2020]:
    matches=sorted(args.smod_dir.glob(f'GHS_SMOD_E{ep}_*.tif'))
    if len(matches) != 1:
        parser.error(f"Expected one GHS-SMOD file for {ep} in {args.smod_dir}; found {len(matches)}")
    f=matches[0]
    with rasterio.open(f) as r:
        a=r.read(1).astype('f8'); a[a<0]=np.nan
        src_transform=r.transform; src_crs=r.crs
    o=np.full(sh,np.nan)
    reproject(a,o,src_transform=src_transform,src_crs=src_crs,dst_transform=tr,dst_crs='EPSG:4326',resampling=Resampling.nearest,src_nodata=np.nan,dst_nodata=np.nan)
    L[f'smod{ep}']=o
args.output.parent.mkdir(parents=True, exist_ok=True)
np.savez_compressed(args.output,**L)
print('wrote', args.output)
m=L['uae']&L['land']
for k in ['lsndvi','lsalb','dmsp']:
    A=L[k]; print(k,A.shape,L[k+'_years'][[0,-1]],'valid %.2f'%np.isfinite(A[0][m]).mean(),np.round(np.nanpercentile(A[0][m],[5,50,95]),3))
for ep in [1995,2020]:
    u,c=np.unique(L[f'smod{ep}'][m][np.isfinite(L[f'smod{ep}'][m])],return_counts=True); print('SMOD',ep,dict(zip(u.astype(int).tolist(),c.tolist())))
