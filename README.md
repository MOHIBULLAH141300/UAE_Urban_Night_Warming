# Urbanisation-driven nocturnal warming amplification: Evidence from the United Arab Emirates

Analysis pipeline, derived results and figures for the manuscript:

**Urbanisation-driven nocturnal warming amplification: Evidence from the United Arab Emirates**

Mohib Ullah, Adam Fenech, Dan Scott, Xander Wang, Ross Gordon
Submitted to *Urban Climate* (2026).
Corresponding author: Adam Fenech — adam.fenech@cud.ac.ae
DOI: *to be assigned on publication.*

---

## What the study does

Station records, satellite land-surface temperature, built-up surface and morphology, ERA5-Land and
NEX-GDDP-CMIP6 are combined over 1995–2024 to measure the nocturnal urban warming increment in the
UAE and to test whether the climate products used for heat assessment contain it. Attribution rests on
a coast-matched exposure–response between built-up growth and warming and on a matched conversion
event study, in which newly developed pixels are compared with similar pixels that remained
undeveloped, including a pre-conversion trend test.

## Headline results

| Quantity | Value |
|---|---|
| Station Tmin trend 1995–2024 | 1.31 Dubai, 1.14 Abu Dhabi, 1.02 Sharjah °C decade⁻¹; 0.13–0.20 where little building occurred |
| Night LST dose–response | +0.50 °C decade⁻¹ per 10 pp added built-up (95% CI 0.42–0.58) |
| Day LST | −0.19 °C decade⁻¹; ERA5-Land −0.01 |
| Conversion event study | +0.66 °C at night in years 3–10 after conversion; no day-time response |
| Rural background | 0.41 (rural LST) = 0.41 (ERA5-Land) = 0.41 (CMIP6 ensemble median) °C decade⁻¹ |
| Mediation | 31–60% via albedo darkening and night-light emission |
| Projection to 2050 | +0.5 to +1.7 °C additional night-time surface warming in the fastest-growing districts |

## Repository contents

### `code/` — the pipeline, in the order it runs
`layers6.py` (raster stack: Landsat NDVI/albedo, DMSP lights, SMOD epochs) → `cci_annual30.py`
(CCI monthly LST to annual and seasonal anomalies) → `v2_grid.py` (pixel Theil–Sen trends,
Mann–Kendall with Hamed–Rao, Benjamini–Hochberg FDR) → `v2_dose.py` (UN-rural reference, coast-matched
dose–response) → `v2_station.py` (station trends, ETCCDI indices, Pettitt screen) → `v2_event4.py`
(matched conversion event study with spatial-block bootstrap) → `v2_era.py` (sensor-era slope test) →
`v2_morph.py`, `v2_morphreg.py`, `v2_lcz.py` (urban form, building height, Local Climate Zones) →
`v2_uncert.py` (uncertainty decomposition) → `v2_future2.py` (projection to 2050) →
`figs_v2.py`, `fig_new.py`, `fig8.py` (figures) and `tp_text.py`, `tp_build.py` (manuscript assembly).
`GEE_LCZ_UAE.js` exports the Local Climate Zone layer from Google Earth Engine.

### `results/` — every number quoted in the manuscript
JSON and CSV outputs of each stage, including `event_v5.json` (event study), `era_v2.json` (sensor-era
test), `dose_v2.csv`, `lcz_v2.csv`, `morph_v2.json`, `uncert_v2.json`, `future_v3.json` and
`rural_background_v2.json`.

### `figures/` — Figures 1–7 and Supplementary Figures S1–S3 at 300 dpi

## Data availability

All primary datasets are public: HadISD (Met Office Hadley Centre); the C3S satellite land-surface
temperature record (Copernicus Climate Data Store); GHS-BUILT-S, GHS-BUILT-H and GHS-SMOD R2023A
(European Commission Joint Research Centre); MODIS MOD13A2 and MCD43A3 and Landsat Collection 2
(NASA/USGS); DMSP-OLS and VIIRS night-time lights (NOAA); ERA5-Land (Copernicus Climate Data Store);
NEX-GDDP-CMIP6 (NASA Center for Climate Simulation); and GADM 4.1. The gridded source archives are too
large to deposit; the intermediate stacks `layers.npz` and `cci_annual30.npz` are rebuilt by the first
two scripts and are available from the corresponding author on request.

## Reproducibility

Trends use the Theil–Sen slope with Mann–Kendall testing (Hamed–Rao correction) and Benjamini–Hochberg
false-discovery control; uncertainty uses a moving-block bootstrap for stations, a spatial block
bootstrap over 0.25° blocks for pixels, and cluster-robust standard errors for the regressions. All
resampling, bootstrap and permutation procedures use the fixed random seed **20260713**.

Conventions: trend period 1995–2024 (WMO 30 years); normals 1991–2020 (WMO-No. 1203), satellite LST
1995–2020; ETCCDI TN90p, TR and TN30; IPCC AR6 baseline 1995–2014 with SSP1-2.6, SSP2-4.5, SSP3-7.0
and SSP5-8.5; urban/rural from the UN Degree of Urbanisation (GHS-SMOD), rural = class 11 only.

## Funding

Supported by the Dubai Future Foundation through its Research, Development and Innovation (RDI) Grant
Program, awarded to Canadian University Dubai under Project Reference No. 2025/DRDI0746 (Principal
Investigator: A. Fenech).

## License

CC BY 4.0 (see `LICENSE`).

## Citation

```
Ullah, M., Fenech, A., Scott, D., Wang, X., Gordon, R. (2026). Urbanisation-driven nocturnal warming
amplification: evidence from the United Arab Emirates. Urban Climate (submitted).
```
