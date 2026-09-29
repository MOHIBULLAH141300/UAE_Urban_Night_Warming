# Temperature Paper A — urban night-time warming in the UAE

Target journal: Urban Climate (Elsevier), Research Article.

## What is here

    Temperature_Paper_A_Urban_Night_Warming.docx   main manuscript (7 figures, 5 tables)
    Temperature_Paper_A_Urban_Night_Warming.pdf    the same, for reading and circulation
    Supplementary_Information_TemperaturePaperA.docx  Figures S1-S3 and Tables S1-S7
    Supplementary_Information_TemperaturePaperA.pdf   the same, for reading and circulation
    Highlights_TemperaturePaperA.docx              five Elsevier-compliant highlights
    Response_to_DS_comments_TempPaperA.docx        point-by-point response to Daniel Scott's comments C0-C13
    figures/                                       Figure1.png .. Figure8.png at 300 dpi
    results/                                       every number in the manuscript, as produced by the scripts
    scripts/                                       the analysis pipeline, in the order it runs
    Urban_Climate_submission_READY/                clean journal package (main text, SI,
                                                   highlights, main figures and review PDFs)

## The paper in one line

Night-time warming in the UAE's fast-growing cities contains an urban component
that ERA5-Land and NEX-GDDP-CMIP6 do not represent, and which continued urban
growth will enlarge.

## Headline numbers

    Station Tmin trend 1995-2024      1.31 Dubai, 1.14 Abu Dhabi, 1.02 Sharjah degC/decade
                                      0.13-0.20 where little building occurred
    Missing warming vs ERA5-Land      0.87-1.16 degC/decade; vs built-up growth rho = 0.93 (p = 0.003)
                                      vs distance from coast rho = -0.21
    Night LST dose-response           +0.50 degC/decade per 10 pp built-up (95% CI 0.42-0.58)
    Day LST                           -0.19; ERA5-Land -0.01
    Rural background                  0.41 (rural LST) = 0.41 (ERA5-Land) = 0.41 (model median)
    Mediation                         31-60% via albedo darkening and night-light emission
    Building height                   +0.22 per 10 m at zero growth; interaction -0.36 per 10 pp per 10 m
    Projection to 2050                +0.5 to +1.7 degC night surface warming in the
                                      fastest-growing districts under the primary scenarios

## Conventions

    Trend period        1995-2024 (WMO 30 years), Theil-Sen + Mann-Kendall (Hamed-Rao)
    Normals             1991-2020 (WMO-No. 1203); satellite LST 1995-2020
    Indices             ETCCDI TN90p (5-day window), TR, TN30
    Projections         IPCC AR6 baseline 1995-2014; 2021-2040 / 2041-2060 / 2081-2100;
                        SSP1-2.6, SSP2-4.5, SSP3-7.0, SSP5-8.5
    Urban / rural       UN Degree of Urbanisation (GHS-SMOD); rural = class 11 only
    Multiple testing    Benjamini-Hochberg FDR at 5% on maps
    Uncertainty         moving-block bootstrap (stations), spatial block bootstrap over
                        0.25 deg blocks (pixels), cluster-robust SE (regressions)
    Random seed         20260713

## Running the pipeline

The scripts expect layers.npz and cci_annual30.npz in the working directory.

    layers6.py        adds Landsat NDVI/albedo, DMSP lights and SMOD epochs to the raster stack
    cci_annual30.py   CCI monthly LST -> annual and seasonal anomalies
    v2_grid.py        pixel trends (Theil-Sen, MK/Hamed-Rao, BH-FDR) -> maps_v2.npz, pixels_v2.pkl
    v2_dose.py        UN-rural reference, coast-matched dose-response -> dose_v2.csv, reg_v2.json
    v2_station.py     station trends, ETCCDI indices, Pettitt screen -> station_v2.csv
    v2_dew.py         dewpoint-adjusted station trends -> dew_v2.csv
    v2_groups.py      greening/browning/height groups, 0.25 deg cells -> groups_v2.json
    v2_extra.py       mediation, class surface change, AR6 scenarios -> ar6_tmin.csv
    v2_morph.py       building height and plan-area fraction from GHS-BUILT-H -> morph.npz
    v2_morphreg.py    height x built-up interaction models -> morph_v2.json
    v2_scale.py       station and pixel responses on a matched 5 km predictor -> scale_v2.json
    v2_sens.py        estimator and sub-period sensitivity -> sens_v2.json
    v2_event4.py      conversion event study with block-bootstrap slope inference -> event_v5.*
    v2_era.py         slope-only sensor-era heterogeneity test -> era_v2.json
    v2_future2.py     rebased urban growth scenarios to 2050 -> future_v3.json, future_v3.csv
    v2_uncert.py      projection uncertainty decomposition -> uncert_v2.json
    figs_v2.py        main and supplementary figures
    tp_text.py        the manuscript text
    tp_build.py       assembles the .docx
    resp.py           the response document

## Known limitations, stated in the paper

  - MODIS LST was evaluated and rejected: too few valid night-time composites over desert.
  - Landsat albedo is a narrow-to-broadband conversion, not a calibrated albedo product.
  - DMSP night lights saturate in city centres; the VIIRS mediator is a 2024 level, not a change.
  - Building height is a single 2018 snapshot, so morphology enters only cross-sectionally.
  - The 2050 projection is a scenario calculation, conservative, and its surface-to-air
    translation rests on six stations and is not statistically resolved.

## Still to do before submission

  - Author names, affiliations, corresponding-author email and CRediT contributions.
  - Confirm the funding statement.
  - Deposit the processed data and scripts, and add the DOI to Data availability.
  - Decide whether Table 1 (datasets) stays in Methods or moves to Supplementary.
