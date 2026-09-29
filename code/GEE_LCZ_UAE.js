// ---------------------------------------------------------------------------
// Local Climate Zones for the UAE  (Demuzere et al. 2022, ESSD 14, 3835-3873)
// One small categorical export. Paste into the GEE Code Editor and press Run,
// then start the task in the Tasks tab. It should finish in a couple of minutes.
// ---------------------------------------------------------------------------

var uae = ee.FeatureCollection('projects/ee-mohibullah141300/assets/gadm41_ARE_0');
var region = uae.geometry().bounds();

// Global LCZ map, 100 m. Band LCZ_Filter is the Gaussian-filtered (recommended)
// classification; LCZ is the raw one. Both are exported so either can be used.
var lcz = ee.ImageCollection('RUB/RUBCLIM/LCZ/global_lcz_map/latest')
            .mosaic()
            .select(['LCZ', 'LCZ_Filter'])
            .clip(uae);

Map.centerObject(uae, 7);
Map.addLayer(lcz.select('LCZ_Filter'), {min: 1, max: 17,
  palette: ['8c0000','d10000','ff0000','bf4d00','ff6600','ff9955','faee05','bcbcbc',
            'ffccaa','555555','006a00','00aa00','648525','b9db79','000000','fbf7ae','6a6aff']},
  'LCZ (filtered)');

Export.image.toDrive({
  image: lcz.toByte(),
  description: 'UAE_LCZ_Demuzere2022_100m',
  folder: 'GEE_UAE_urban',
  fileNamePrefix: 'UAE_LCZ_Demuzere2022_100m',
  region: region,
  scale: 100,
  crs: 'EPSG:4326',
  maxPixels: 1e10,
  fileFormat: 'GeoTIFF'
});

// LCZ class key (Stewart & Oke 2012):
//  1 compact high-rise      7 lightweight low-rise   11 dense trees
//  2 compact mid-rise       8 large low-rise         12 scattered trees
//  3 compact low-rise       9 sparsely built         13 bush, scrub
//  4 open high-rise        10 heavy industry         14 low plants
//  5 open mid-rise                                   15 bare rock or paved
//  6 open low-rise                                   16 bare soil or sand
//                                                    17 water
