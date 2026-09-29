# -*- coding: utf-8 -*-
TITLE = "Quantifying the urban increment in night-time warming and its absence from the climate products used for heat planning: United Arab Emirates, 1995–2024"
SHORT_TITLE = "The urban increment in night-time warming"

ABSTRACT = (
"Urbanisation contributes to observed warming, but what heat planning needs — how much of the night warming at a place is urban, and whether the products used to plan for it hold that part — has not been measured. "
"We measure it for the United Arab Emirates over 1995–2024 following WMO and ETCCDI conventions, combining seven stations, a 1 km satellite land-surface temperature record, satellite urban and surface data, ERA5-Land and 28 NEX-GDDP-CMIP6 models. "
"Minimum temperature rose by 1.31, 1.14 and 1.02 °C decade⁻¹ at the three fastest-urbanising stations against 0.13–0.20 elsewhere, scaling with built-up growth (ρ = 0.93) but not with coastal distance. "
"Across 75,528 pixels, each 10 percentage points of added built-up surface raised the night-time surface trend by 0.50 (95% CI 0.42–0.58) °C decade⁻¹ relative to rural land; daytime trends fell by 0.19. "
"An event study on 432 converted pixels found the night-time difference from matched never-built land an order of magnitude larger after conversion than before (0.66 °C after a decade), with no daytime step. "
"Including albedo darkening and night lights reduced the adjusted built-up coefficient by 31–60%, and each added percentage point raised the trend less where buildings are tall. "
"Rural land and ERA5-Land warmed at 0.41 °C decade⁻¹, closely matching the model-ensemble median, whereas the local urban increment was not represented. "
"Continued growth at the observed 2010–2020 rate would add 0.5–1.7 °C more by 2050 in the fastest-growing districts."
)
KEYWORDS = "urban heat island; nocturnal warming; urban expansion; land-surface temperature; ERA5-Land; hot desert cities"

INTRO = [
"The south-eastern Arabian Peninsula is warming about twice as fast as the global mean, and its temperature extremes intensify disproportionately at each additional level of global warming (Zittis et al., 2022; Vinodhkumar et al., 2024). "
"Along the southern Gulf coast, humid heat peaks in the evening and at night, when maritime moisture moves inland (Raymond et al., 2024). "
"Night-time temperature therefore carries particular weight in this region. Warm nights limit physiological recovery and are associated with excess heat-related mortality (He et al., 2022). "
"They also drive the cooling demand of cities in which air-conditioning is close to universal.",

"The UAE combines this regional warming with some of the fastest urban expansion on Earth. "
"Built-up surface in the country doubled between 1995 and 2020, from 298 to 618 km², and the land classified as urban centres under the UN Degree of Urbanisation almost tripled, from 499 to 1,457 km² (Results). "
"Urban surfaces store heat during the day and release it at night, reduce long-wave cooling and add waste heat, so urban heat islands are typically strongest at night (Oke, 1982; Manoli et al., 2019). "
"Hot desert cities differ from temperate cities in one important respect. Irrigated vegetation, shading and the high thermal inertia of built materials can make them cooler than the surrounding bare sand during the day, "
"producing a daytime urban cool island alongside a night-time heat island (Lazzarini et al., 2015). "
"Satellite studies of Dubai show that its surface heat island strengthened markedly during 2003–2019 and that newly developed districts warmed fastest (Elhacham and Alpert, 2021).",

"This combination creates a problem for adaptation planning. National and municipal heat assessments rely on reanalyses such as ERA5-Land and on statistically downscaled projections such as NEX-GDDP-CMIP6 (Muñoz-Sabater et al., 2021; Thrasher et al., 2022). "
"Neither explicitly represents the observed time-varying urban expansion at the scale examined here, for reasons that are structural rather than simply a matter of resolution or tuning. "
"ERA5-Land is an offline simulation of the CHTESSEL land-surface scheme (IFS cycle CY45R1) driven by ERA5 atmospheric fields; the scheme tiles each grid box into vegetation, bare soil, snow and water and carries no urban tile (Muñoz-Sabater et al., 2021). "
"The land run performs no data assimilation of its own, although the ERA5 forcing that drives it is produced by a system that does assimilate observations, so a weak indirect urban influence through the forcing cannot be excluded. "
"NEX-GDDP-CMIP6 applies a daily bias-correction and spatial-disaggregation method whose reference is the Global Meteorological Forcing Dataset for 1960–2014 (Sheffield et al., 2006; Thrasher et al., 2022). "
"Bias adjustment of that kind rescales the distribution of the driving model but transfers the model's own trend, and most CMIP6 land components either carry no urban parameterisation or hold urban extent fixed (Zhao et al., 2021). "
"A warming trend arising from local land-cover change is therefore not explicitly represented by either product, whatever their nominal spatial resolution. "
"If a large share of observed night-time warming in UAE cities is urban, those datasets may omit or attenuate the component needed for local heat planning.",

"The observation-minus-reanalysis approach, which attributes the difference between station and reanalysis trends to land-use change, was developed to diagnose exactly this kind of gap (Kalnay and Cai, 2003). "
"It has known weaknesses: reanalyses reproduce multidecadal variability weakly, so observation-minus-reanalysis trends can depend on the period chosen (Wang et al., 2013), and the difference also absorbs station inhomogeneity and any local effect the reanalysis misses for other reasons. "
"The design used here addresses all three. The period is fixed in advance by the WMO 30-year convention rather than selected; a rural control shows what the method returns where no urbanisation occurred; and an independent satellite record, which involves no reanalysis at all, provides the same test over 75,528 pixels. "
"The approach has not previously been applied to Gulf cities.",

"Recent work has established that urbanisation contributes measurably to warming at scales beyond the city. Chakraborty and Qian (2024) show from satellite land-surface temperature that urban areas contributed on the order of 1–2% of observed land warming over 2003–2019, with much larger regional contributions where urbanisation is rapid, and argue that Earth system models should represent urban land explicitly. Zhao et al. (2021) reach a compatible conclusion from the modelling side, and Liu et al. (2025) show that the warm-season sensitivity to urbanisation varies with background climate, being two to three times larger in the wetter mid-latitudes, where the evaporative contrast between city and countryside is large, than in East and South Asia. "
"That mechanism is weak in a hyper-arid setting, where the rural surface is bare sand with almost no evaporative capacity, which is one reason the UAE signal reported below is nocturnal rather than a warm-season daytime effect. "
"What neither line of work does is measure the increment where it matters for planning: in screen-level air temperature, at the scale of a city, over a period long enough to meet climate-trend conventions, and against the specific products that heat assessments actually use. "
"Regional evaluations of those products over the Arabian Peninsula have compared reanalyses with station observations without separating urban from rural sites (Ullah et al., 2024), and the Gulf surface-heat-island studies cited above do not test the products at all. "
"The quantity that planning needs — how much of the observed night-time warming at a given place is urban, and whether the product used to plan for that place contains it — has not been measured.",

"This study measures that one quantity, which we call the urban increment, in a setting chosen because it can be measured there cleanly: UAE built-up surface doubled inside a single 30-year record, the surrounding desert provides an unambiguous rural reference, and vegetation is too sparse to confound the signal. "
"The question is therefore single: how large is the urban increment in night-time warming in the UAE's cities, and do the climate products used for heat planning contain it? "
"Everything that follows serves that question — the dose–response that sizes the increment, the mechanism and form analyses that establish what drives it and how it varies, the comparison with ERA5-Land and NEX-GDDP-CMIP6 that tests whether the products hold it, and the projection that gives its future magnitude. "
"We answer it with three independent lines of evidence that share a common spatial reference and a common set of climatological conventions, drawn from the datasets listed in Table 1. "
"First, station Tmin and Tmax trends are compared with ERA5-Land and NEX-GDDP-CMIP6 at the same locations and related to nearby built-up growth and to distance from the coast. "
"Second, satellite land-surface temperature trends are related to built-up change pixel by pixel, with distance from the coast controlled explicitly and rural reference land defined by the UN Degree of Urbanisation. "
"Third, we test whether the signal survives aggregation to the 0.25° grid of the downscaled projections and compare its magnitude with the IPCC AR6 scenario projections. "
"We then test the main alternative explanations — greening and irrigation, coastal humidity, and building form — quantify how much of the effect measured surface changes explain, "
"and express the result in the ETCCDI warm-night indices used in climate monitoring.",
]

METHODS = [
("2.1 Study area, period and conventions",
["The UAE extends over 22.6–26.1°N and 51.5–56.4°E. The interior is sand desert. Relief is confined to the Hajar Mountains in the north-east, and most of the population lives along the Gulf coast between Abu Dhabi and Ras Al Khaimah and in the inland oasis city of Al Ain (Fig. 1).",
"Periods and reference conventions follow established climatological practice rather than data-driven choices. "
"Trends are estimated over 1995–2024, a full 30-year period, the minimum length recommended for climate-trend assessment. "
"Anomalies and percentile thresholds use the 1991–2020 climatological standard normal (WMO, 2017); the satellite LST record begins in July 1995, so its reference period is 1995–2020, the longest overlap available. "
"Extreme-temperature indices follow the ETCCDI definitions (Zhang et al., 2011). "
"Projection baselines and time slices follow the IPCC Sixth Assessment Report: changes are expressed relative to 1995–2014 for the near term (2021–2040), mid term (2041–2060) and long term (2081–2100) under SSP1-2.6, SSP2-4.5, SSP3-7.0 and SSP5-8.5 (IPCC, 2021). "
"Urban and rural land are classified with the UN Degree of Urbanisation, the definition endorsed by the UN Statistical Commission, as implemented in the GHS Settlement Model grid (Dijkstra et al., 2021; Pesaresi et al., 2024). "
"Results for the 2001–2024 sub-period and for alternative estimators and coastal thresholds are reported as sensitivity analyses (Table 4); the 1991–2020 normal period cannot be used for the satellite record, which begins in July 1995. "
"Every comparison between an observation and a product is made at matched locations, periods and reference baselines. "
"Table 1 lists the datasets, the period over which each is used and the role it plays in the analysis."]),
("2.2 Station records",
["Sub-daily 2-m air temperature and dewpoint were taken from HadISD version 3.4.3.2025f, a quality-controlled subset of the Integrated Surface Database (Dunn et al., 2012; Smith et al., 2011). "
"The eight UAE stations in HadISD are Dubai International, Sharjah International, Abu Dhabi International, Al Bateen, Al Ain International, Ras Al Khaimah International, Fujairah International and Al Maktoum International. "
"Observations were converted to local time (UTC+4). A day was retained when it contained at least six observations, including at least one between 00:00 and 07:00 and one between 11:00 and 16:00. "
"Daily Tmin and Tmax were averaged by month (at least 20 valid days), converted to anomalies from the 1991–2020 monthly normals, and averaged to annual values from years with at least 10 valid months. "
"A station entered the analysis when at least 90% of the 30 years were valid: six stations qualify, with 29 or 30 valid years each. Al Bateen, whose 2001–2009 gap leaves 21 valid years (70%), is reported separately (Supplementary Table S7). "
"Al Maktoum International (from 2011) is too short. "
"Independent Integrated Surface Database processing used earlier for Dubai gave a 1991–2020 Tmin trend of 1.47 °C decade⁻¹, consistent with the value obtained here."]),
("2.3 Satellite land-surface temperature",
["Pixel-level evidence comes from the Copernicus Climate Change Service monthly land-surface temperature product derived from the European Space Agency Climate Change Initiative infrared climate data record (C3S, 2023). "
"The record merges successive sensors into a harmonised series at 0.01° resolution, with separate day-time (about 10:30 local time) and night-time (about 22:30) overpasses, and covers July 1995 to June 2025. "
"Monthly values were converted to anomalies from each pixel's 1995–2020 calendar-month normal and averaged into annual anomalies when at least six months were valid. "
"Gaps associated with instrument changes leave 29 usable years of the 30-year period; 2018 is missing entirely. "
"Data were sampled to a common 0.009° (about 1 km) analysis grid. "
"Sensor changes can alter absolute trends but largely cancel in the urban-minus-rural differences on which the inference rests, because urban and rural pixels are observed by the same sensor on the same overpass; differences are also reported separately for each sensor era (Results). "
"MODIS 8-day LST (MOD11A2/MYD11A2 v061) was evaluated as a second record and rejected: after quality screening fewer than 15% of monthly composites were valid over desert pixels, which is insufficient for the rural reference. "
"A harmonised climate data record is in any case the appropriate source for trend work."]),
("2.4 Urban growth, land cover and surface properties",
["Built-up surface came from GHS-BUILT-S R2023A at 30 arc-seconds for the epochs 1975–2020 (Pesaresi et al., 2024). "
"Built-up area per cell was divided by cell area to give a built-up fraction, and the primary exposure variable is the change between 1995 and 2020, ΔBF, in percentage points (pp); note that this is the built-up window, which is shorter than the 1995–2024 temperature-trend period because the settlement grid ends at 2020. "
"Settlement classes came from GHS-SMOD for the same epochs, and mean building height from GHS-BUILT-H 2018. "
"Distance from the coast was computed for every land pixel from a land–sea mask derived from satellite LST validity; the UAE boundary and emirate identifiers are from GADM 4.1.",
"Vegetation, albedo and night-time light were measured over the full analysis period. "
"Annual NDVI and Liang (2001) shortwave broadband albedo were computed from Landsat 5, 7, 8 and 9 Collection 2 surface reflectance for 1995–2024, cloud-masked and averaged onto the 1 km grid. "
"MODIS MOD13A2 NDVI (2000–2024) and MCD43A3 white-sky albedo (2001–2024) provide instrument-calibrated versions for the later part of the record, and are used for the mechanism analysis, with the Landsat series as the full-period check. "
"Night-time light came from DMSP-OLS stable lights (1996–2013) and VIIRS monthly composites (2014–2024). "
"Changes in NDVI and albedo are differences between the first and last five years of each record (1995–1999 against 2020–2024 for Landsat). "
"For night-time light, the DMSP series enters as an epoch difference (1996–1998 against 2010–2013, the years with stable intercalibrated coverage) and the VIIRS series as the 2024 level, because DMSP and VIIRS are not radiometrically continuous and a difference across the two instruments would not be meaningful; the VIIRS mediator is therefore a level, not a change."]),
("2.5 Regional products used for planning",
["ERA5-Land hourly 2-m temperature at 0.1° (Muñoz-Sabater et al., 2021) was aggregated to daily Tmin and Tmax over the same local-time day as the stations, then to monthly and annual anomalies from the 1991–2020 normal. "
"Downscaled projections came from NEX-GDDP-CMIP6 at 0.25° (Thrasher et al., 2022); the 28 models with complete daily tasmin and tasmax were used, splicing historical simulations (to 2014) with SSP2-4.5 for the observational period (Supplementary Table S6). "
"Products were sampled at the nearest land cell for station comparisons and averaged over the UAE land area for area-scale comparisons. "
"Scenario changes were computed for the three IPCC AR6 periods relative to 1995–2014 under four SSPs; model–scenario combinations with corrupt archived files were excluded, leaving 23–28 models per combination. "
"UAE-area Tmin/Tmax ratios from native CMIP6 (21 models), NEX-GDDP-CMIP6 (14 models) and ERA5-Land for 1991–2020 were retained from the earlier scale-matched comparison as evidence of the regional background these products represent."]),
("2.6 Trend estimation and testing",
["Trends are Theil–Sen slopes (Sen, 1968), tested with the Mann–Kendall test using the Hamed–Rao variance correction for serial dependence (Hamed and Rao, 1998). "
"Ordinary least squares is reported as a sensitivity. "
"Station confidence intervals come from a moving-block bootstrap with three-year blocks and 2,000 replicates (Künsch, 1989), resampling years in pairs so that the year–value correspondence and the Tmin–Tmax covariance are preserved. "
"For the pixel maps, p values are controlled for multiple testing with the Benjamini–Hochberg false-discovery rate at 5% (Benjamini and Hochberg, 1995).",
"The missing warming at each station is the station trend minus the trend at the nearest ERA5-Land cell, computed on the difference series, following the observation-minus-reanalysis logic of Kalnay and Cai (2003). "
"Because station histories are unavailable, homogeneity was assessed with the Pettitt test (Pettitt, 1979) applied to the detrended station-minus-ERA5-Land difference series; applying a step test to a trending series would remove the trend by construction. "
"The trend was then recomputed after removing the detected level shift.",
"For the satellite analysis, pixel trends were grouped by ΔBF class and compared with rural pixels in the same coastal-distance band (0–5, 5–10, 10–20, 20–40, 40–80 and >80 km). "
"Rural pixels are those classified as very low density rural grid cells (SMOD class 11, the most restrictive of the three rural classes in the Degree of Urbanisation) in both 1995 and 2020, with a built-up fraction below 1% in the pixel and its 10 km neighbourhood. "
"Rural means were weighted by the coastal-distance distribution of the urban class, so the urban–rural difference is not confounded by coastal moderation. "
"Uncertainty comes from a spatial block bootstrap over 0.25° blocks (135 blocks, 2,000 replicates). "
"Pixel trends were also regressed on ΔBF with the 1995 built-up fraction, coastal-distance band, emirate, latitude and longitude as covariates and standard errors clustered by block; "
"NDVI change was added as a potential confounder, and albedo change and night-time light as mechanisms that mediate the effect of building. "
"The identical analysis was applied to ERA5-Land Tmin and Tmax sampled at every pixel, which tests whether the product contains an urban signal. "
"The random seed was 20260713 throughout."]),
("2.7 Heat indices and humidity",
["Warm nights are expressed with the ETCCDI index TN90p, the percentage of nights with Tmin above the calendar-day 90th percentile computed from a five-day window in the 1991–2020 base period (Zhang et al., 2011). "
"Each dataset uses its own base period percentiles, so mean biases between stations and gridded products cannot affect the comparison. "
"Tropical nights (TR, Tmin ≥ 20 °C) and a regionally relevant count of nights with Tmin ≥ 30 °C are also reported. "
"Coastal humidity was tested with HadISD dewpoint: night-time (00:00–06:00) monthly mean dewpoint anomalies were averaged to annual values, the station Tmin anomaly was regressed on the dewpoint anomaly, and the Tmin trend was recomputed after removing the dewpoint-related component."]),
("2.8 Urban morphology",
["Built-up fraction measures how much of a cell is covered by building, not how much building it contains. "
"Two further morphometric parameters were therefore derived (Grimmond and Oke, 1999). "
"The average net building height product of GHS-BUILT-H R2023A, at 100 m for 2018, was aggregated to the analysis grid as the mean height over the sub-cells that carry buildings (H, in metres, median 4.7 m in cells at least 5% built up, 95th percentile 12.1 m, maximum 45.6 m), "
"and the plan-area fraction λp was taken from GHS-BUILT-S for 2020 (median 0.12, 95th percentile 0.34). "
"A bulk height index was also tested: the mean of the height product over all sub-cells of the analysis cell, whether built or not, which is the building volume per unit ground area implied by the height data alone. ""Because most 100 m sub-cells in a built-up kilometre carry some building (median fraction 0.83), this index is close to a rescaling of H (median 3.6 m against 4.7 m) and adds little independent information; this is reported rather than glossed. "
"Sky-view factor was not derived: building footprint geometry is not available at this resolution, and any sky-view factor estimated from λp alone under an idealised array assumption would be a deterministic re-expression of λp rather than independent information. "
"Height is a single 2018 snapshot, so morphology enters the analysis as a cross-sectional modifier of the built-up response — through an interaction between ΔBF and H — and not as a change variable.",

"Urban form was also classified with the Local Climate Zone scheme (Stewart and Oke, 2012), using the global LCZ map of Demuzere et al. (2022) at 100 m. "
"The 100 m classes were aggregated to the analysis grid by counting sub-cells: each cell was assigned the built LCZ class (1–10) occupying most of its built sub-cells, and was analysed when built classes covered at least 20% of the cell and at least 40 cells fell in the class. "
"Like building height, the LCZ map is a single epoch and is used as a cross-sectional stratification, not as a change variable."]),
("2.9 Event study of built-up conversion",
["To test whether the association between building and night-time warming behaves like a response to conversion rather than a pre-existing difference between the pixels that were built on and those that were not, pixels were aligned on the time at which they were converted. "
"A pixel is treated if it gained at least 5 percentage points of built-up surface between 1995 and 2020 from a 1995 base below 2%. "
"Controls are never-built pixels: rural in the Degree of Urbanisation in both epochs, below 1% built-up in the pixel and its 10 km neighbourhood, and with no detectable growth; 61,437 pixels qualify, distributed across 23 strata. "
"Matching is to the stratum mean rather than pixel to pixel: each treated pixel is differenced against the mean of the control pool sharing its coastal-distance band and emirate. "
"Event time is the year minus the GHS epoch at which conversion is dated, and each pixel is normalised to its own mean over the five years before that date. "
"Confidence intervals come from a block bootstrap over 0.25° blocks with 2,000 replicates, and the analysis is restricted to the 2005, 2010 and 2015 cohorts, which have both a pre-window and a post-window inside the satellite record.",
"Dating conversion is the one discretionary choice, and it is treated as such. "
"GHS epochs are five years apart, and the built-up surface a sensor detects appears only after clearing, grading and infrastructure have already altered the surface, so dating conversion at a large built-up increment places part of the real conversion inside the pre-window. "
"The primary threshold was fixed a priori at 1 percentage point, the smallest increment resolved above zero; thresholds of 2, 3 and 5 percentage points are reported as sensitivity tests (Fig. 5c). Raising the threshold both delays the event date and slightly changes which pixels have a usable pre-window, so the sample is not identical across the sweep (n = 432, 458, 441 and 331); the sweep is a sensitivity test, not a controlled re-dating of one fixed set. "
"The pre- and post-conversion trends were estimated as linear slopes inside each spatial-block bootstrap replicate, preserving the covariance among event years."]),
("2.10 Projecting the urban increment",
["The dose–response relates the 1995–2024 temperature trend to the built-up increment observed between 1995 and 2020. Multiplying the regression coefficient by the 2.9 decades separating the 1995 and 2024 temperature endpoints converts it into k, the warming accumulated per 10 pp of added built-up surface. "
"Expressed this way the coefficient no longer refers to a particular period length and can be applied to a future increment, under the assumption — stated here as the principal caveat on the calculation — that the response scales with the size of the built-up increment rather than with the rate at which it occurs. "
"To keep the station and pixel estimates comparable, the pixel regression was refitted on the built-up increment averaged over a 5 km radius, the same predictor used for the stations; smoothing the predictor raises the coefficient, so the two are otherwise not comparable. "
"The projection uses the surface (night LST) coefficient, which rests on 75,528 pixels, rather than the station air-temperature coefficient, which rests on six stations, is about twice as large and is not statistically resolved (p = 0.07); the resulting estimates are therefore conservative if that ratio is real, and the uncertainty in it is carried through the Discussion. "
"Two built-up scenarios extrapolate each cell's growth to 2050 and are capped at the 99th percentile of observed plan-area fraction. "
"The baseline is the 2020 epoch and the rate is taken from 2010–2020, because GHS-BUILT-S R2023A is derived from Landsat and a 2018 Sentinel-2 composite, so epochs after 2020 are not observation-supported; S-high continues that rate for the thirty years to 2050 and S-low applies half of it. "
"Two further variants — a 2005–2020 rate and the 2010–2025 rate from the projected 2025 layer — are reported as sensitivity tests (Table 5). "
"The transfer coefficient was checked retrospectively by predicting the observed 1995–2024 station excess from each station's observed built-up increment."]),
]

RESULTS = [
("3.1 Urban growth around the stations",
["UAE built-up surface increased from 298 km² in 1995 to 618 km² in 2020, and land classified as urban centres grew from 499 to 1,457 km² (Fig. 1b). "
"Growth was concentrated along the Dubai–Sharjah and Abu Dhabi coasts and around Al Ain (Fig. 1a). "
"Within 5 km of the stations, built-up fraction rose by 7 pp at Sharjah, 4 pp at Dubai, 3 pp at Abu Dhabi and 2 pp at Al Ain, against 1 pp at Ras Al Khaimah and Fujairah (Table 2). "
"Coastal distance and urban growth are not collinear across the network: Fujairah, the station closest to the sea (4.5 km), had almost no urban growth, whereas Sharjah (13.4 km) had the most. "
"This contrast allows the two influences to be separated.",

"The growth was not uniform between emirates or with distance inland. "
"Abu Dhabi added 151 km² of built-up surface between 1995 and 2020, 47% of the national increase, and Dubai 84 km² (26%), followed by Sharjah (36 km², 11%), Ras Al Khaimah (24 km²), Ajman (11 km²) and Umm Al Quwain and Fujairah (7 km² each). "
"Two-thirds of the national increase (67%) lies within 20 km of the coast, where the population is concentrated, but 18% lies more than 50 km inland, around Al Ain and the interior settlements. "
"The urban signal therefore has both a coastal and an inland expression, which is what allows coastal moderation to be separated from urbanisation in the analysis that follows.",

"Three kinds of development contributed. "
"Coastal reclamation extended the shoreline itself: cumulative reclamation along the UAE coast reached about 119 km² by the early 2020s, of which Dubai accounts for more than two-thirds and Abu Dhabi for a further 35 km² (Dahy et al., 2024). "
"These are new land surfaces, sand replaced by built fabric, and they appear in the built-up record as growth in the 0–5 km coastal band. "
"Densification of existing urban land accounts for the pixels already built up in 1995 whose built-up fraction rose further, concentrated in the Dubai–Sharjah conurbation. "
"Peripheral expansion onto desert accounts for the largest share by area: the two smallest growth classes, gaining 2–10 percentage points, contain 2,800 of the 3,623 pixels in the four growth classes of Table 3. "
"The analysis treats all three as built-up increments and does not distinguish them; the height results in Section 3.10 bear on the difference between the second and the third."]),
("3.2 Night-time warming at the city stations exceeds the regional products",
["Tmin increased faster than Tmax at every station, but the size of the asymmetry differed sharply between stations (Fig. 2a; Table 2). "
"During 1995–2024, Tmin rose by 1.31 °C decade⁻¹ at Dubai (95% CI 1.04–1.60), 1.14 at Abu Dhabi (0.83–1.35) and 1.02 at Sharjah (0.72–1.29), with paired Tmin–Tmax differences of 0.80, 1.06 and 0.98 °C decade⁻¹. "
"Inland Al Ain warmed at an intermediate rate (0.63; 0.42–0.82). "
"At Ras Al Khaimah (0.20) and Fujairah (0.13) the trends were small and not statistically resolved.",
"The regional products did not reproduce the trends at the urbanising stations. "
"ERA5-Land Tmin trends at the nearest cells were 0.20–0.42 °C decade⁻¹ at every station and NEX-GDDP-CMIP6 medians 0.33–0.36 °C decade⁻¹. "
"Tmin at Dubai, Abu Dhabi and Sharjah exceeded all 28 models at the same location, whereas Ras Al Khaimah and Fujairah fell at the 21st and 11th percentiles of the ensemble. "
"The missing warming (station minus ERA5-Land) was 1.16 °C decade⁻¹ (0.75–1.54) at Dubai, 0.87 (0.71–1.01) at Abu Dhabi and 0.87 (0.54–1.25) at Sharjah, against 0.23 at Al Ain and −0.12 and 0.01 at Ras Al Khaimah and Fujairah. "
"Across the seven stations, the missing Tmin warming increased with built-up growth within 5 km (Spearman ρ = 0.93, p = 0.003; Fig. 2b) and was unrelated to distance from the coast (ρ = −0.21, p = 0.64). "
"At Dubai, annual Tmin anomalies separate from ERA5-Land after about 2008 and have remained above it since (Fig. 2c).",
"The missing warming is not the product of a discontinuity in the station records. "
"The Pettitt test on the detrended station-minus-ERA5-Land series identified a shift reaching significance only at Dubai (2019, p = 0.04); the next smallest p value was at Ras Al Khaimah (2001, p = 0.05, marginally above the 5% level); after removing the detected shift the missing warming at Dubai was larger, not smaller (1.35 °C decade⁻¹), and the values at Sharjah (0.81), Abu Dhabi (0.82) and Al Ain (0.26) were essentially unchanged (Table 2)."]),
("3.3 A night-specific urban signal in satellite land-surface temperature",
["Satellite LST shows the same contrast continuously across the country (Fig. 3). "
"During 1995–2024, night-time LST warmed fastest in a band that follows the areas developed since 1995: the Dubai–Sharjah coastal strip and its inland extensions, the Abu Dhabi mainland suburbs and parts of Al Ain. "
"Daytime LST in the same areas warmed less than the surrounding desert or cooled, whereas ERA5-Land Tmin trends were spatially smooth and showed no urban structure. "
"After false-discovery-rate control, 79% of land pixels had a significant night-time warming trend, and none had a significant daytime trend.",
"Compared with rural pixels at the same distance from the coast, the night-time LST trend increased steadily with built-up growth (Fig. 4a; Table 3). "
"The excess was 0.31 °C decade⁻¹ (0.24–0.38) for pixels gaining 2–5 pp, 0.54 (0.41–0.65) for 5–10 pp, 0.85 (0.65–1.00) for 10–20 pp and 0.92 (0.71–1.13) for at least 20 pp. "
"Daytime differences had the opposite sign, from −0.17 to −0.54 °C decade⁻¹. "
"ERA5-Land showed no corresponding response: its Tmin differences ranged from −0.05 to −0.07 °C decade⁻¹ and its Tmax differences were within 0.02 of zero. "
"Classified by the Degree of Urbanisation, land in urban centres warmed 0.67 °C decade⁻¹ (0.50–0.81) faster than rural land at night and land in urban clusters 0.47 (0.34–0.60). "
"In the regression with coastal band, emirate, initial built-up fraction and location as covariates, each additional 10 pp of built-up surface increased the night-time LST trend by 0.50 °C decade⁻¹ (0.42–0.58) and reduced the daytime trend by 0.19 (0.08–0.30); "
"the ERA5-Land Tmin coefficient was −0.012 (−0.023 to 0.000). "
"Areas already built up in 1995 that changed little afterwards also warmed faster at night than rural land (0.37 °C decade⁻¹; 0.25–0.50), consistent with densification and growing waste heat within established districts.",
"The rural background is consistent across data sets. "
"Rural night-time LST warmed by 0.41 °C decade⁻¹ and ERA5-Land Tmin by 0.41 at the same pixels, matching the ERA5-Land UAE-area Tmin trend of 0.41 and the NEX-GDDP-CMIP6 ensemble median of 0.41 (5–95%: 0.18–0.63). "
"Their central trend estimates therefore align closely with rural warming over this period, although the model spread remains substantial; what they do not reproduce is the additional relationship between local urban growth and warming."]),
("3.4 Night-time warming follows conversion",
["Aligning pixels on the time they were built on separates a response to conversion from a pre-existing difference between converted and unconverted land (Fig. 5). "
"Slopes and levels are estimated inside each spatial-block bootstrap replicate, so their intervals carry the dependence between event years rather than treating them as independent. "
"Across the treated pixels with a usable pre-window — 432 at night and 433 by day, in 51 blocks — the night-time difference from the control stratum means changes little before conversion and rises after it: the pre-conversion slope is 0.022 °C yr⁻¹ (95% CI -0.001 to 0.042, p = 0.065), the post-conversion slope is 0.096 °C yr⁻¹ (0.061 to 0.129, p = 0.0005), and the mean level three to ten years after conversion is 0.66 °C (0.44 to 0.88, p = 0.0005). "
"The pre-conversion slope is not significant at the 5% level, but neither is it comfortably zero, and we do not claim a flat pre-trend: what the design shows is that the divergence is an order of magnitude larger after conversion than before it. "
"Day-time land-surface temperature shows no resolved change on either side — pre-slope −0.032 °C yr⁻¹ (p = 0.25), post-slope 0.049 (p = 0.19), level 0.13 °C (−0.19 to 0.38, p = 0.41) — the same diurnal asymmetry seen in the dose–response. "
"An earlier estimate that treated event years as independent returned a nominally significant day-time post-slope; it does not survive the bootstrap, and the corrected inference is reported here.",

"The date assigned to conversion matters, and the way it matters is informative (Fig. 5c). "
"The dating threshold is set a priori at 1 percentage point, the smallest increment the product resolves above zero and therefore the earliest epoch at which the surface has demonstrably begun to change; clearing, grading and infrastructure precede the built surface a sensor detects. "
"Sweeping the threshold from 1 to 5 pp shows why the choice matters for the timing test and not for the effect: the pre-conversion slope rises from 0.022 (p = 0.069) to 0.073 °C yr⁻¹ (p = 0.001) as the dating is pushed later, which is what would happen if part of the real conversion were being placed inside the pre-window, while the post-conversion slope stays between 0.061 and 0.096 °C yr⁻¹ and the three-to-ten-year level between 0.66 and 0.84 °C. The treated sample is not identical across the sweep (n = 432 to 458), so it is a sensitivity test rather than a re-dating of one fixed set. "
"The size of the divergence therefore does not depend on the dating; only the timing test does. "
"This design does not establish causation in the sense a controlled experiment would, but it removes the most plausible alternative: that the pixels which were built on were already warming faster."]),
("3.5 When the signal emerged, and how robust it is",
["The night-time LST difference between urbanising pixels (ΔBF ≥ 10 pp) and coast-matched rural pixels rose from about −1.4 °C in the mid-1990s to about +1.0 °C in the early 2020s, a Theil–Sen trend of 0.89 °C decade⁻¹ (Hamed–Rao p < 10⁻¹²), closely following national built-up growth (Fig. S1). "
"The daytime difference declined by 0.54 °C decade⁻¹ (p < 10⁻⁶). "
"The night-time difference increased within every sensor era of the satellite record, but not at the same rate: 1.59 ± 0.60 °C decade⁻¹ in 1995–2002, 1.46 ± 0.16 in 2003–2011 and 0.29 ± 0.20 in 2013–2024, against 0.84 ± 0.07 over the record as a whole. "
"These era figures and the whole-record value are least-squares slopes, fitted so that the eras can be compared within one model, and differ slightly from the Theil–Sen estimate quoted above for the same series. "
"Comparing a model with era-specific levels and a common slope against one with era-specific slopes tests the slopes alone: the slopes differ significantly (F = 6.65, p = 0.005, 2 d.f.), so the difference between eras is more than sampling noise and is reported as such. "
"Two readings are available and the evidence favours the first. "
"Day-time slopes show no such heterogeneity (F = 0.52, p = 0.60), whereas an instrument discontinuity would be expected to affect both overpasses; and the slowing is what the form results predict, since the earliest period converted desert at the urban margin, where the response per unit area is largest, while later growth was increasingly densification of land already partly built. "
"The alternative, a residual sensor effect that the urban-minus-rural differencing does not fully remove at night, cannot be excluded with these data. "
"Either way the full-period estimate is an average over a response that was stronger early in the record. "
"The event study is anchored on conversion dates rather than calendar time and compares treated and control pixels observed by the same sensor in the same year, which reduces its sensitivity to common sensor discontinuities; it does not remove them entirely, because the conversion cohorts still occupy different calendar periods.",
"The result was insensitive to the analysis choices tested (Table 4). "
"Excluding pixels within 5 km of the coast, which removes reclaimed land and shoreline mixing, raised the night-time coefficient to 0.57 °C decade⁻¹ per 10 pp; restricting the analysis to pixels within 50 km of the coast gave 0.47. "
"The result does not depend on the estimator: ordinary least squares instead of Theil–Sen gives 0.47 °C decade⁻¹ per 10 pp (0.39–0.56) against 0.50 for the primary estimate. "
"Restricting the analysis to 2001–2024, with the 2000–2020 built-up increment, gives a larger response, 0.65 (0.53–0.78) (Table 4). "
"The signal is therefore not weakening as the record lengthens; if anything the more recent, more rapidly built period shows a stronger response, which is consistent with the growth of the urban–rural difference in Fig. S1 and matters for the projection below. "
"Every estimate excluded zero, and the corresponding ERA5-Land coefficients remained close to zero throughout."]),
("3.6 What carries the signal: surface darkening, waste heat and season",
["Greening does not produce the night signal; buildings do (Fig. 6a). "
"Land that greened without being built on (ΔNDVI ≥ 0.05, ΔBF < 1 pp) warmed 0.16 °C decade⁻¹ (0.10–0.21) faster than rural desert at night and cooled by day (−0.14; −0.29 to −0.01). "
"Land that lost vegetation without being built on warmed by 0.12 (0.02–0.20). "
"Urbanising land (ΔBF ≥ 10 pp) warmed 0.76 °C decade⁻¹ (0.58–0.93) faster than rural at night where NDVI did not increase and 0.99 (0.79–1.13) where it did, with daytime trends 0.28 and 0.80 °C decade⁻¹ lower. "
"Irrigated landscaping therefore cools days and adds to night-time warming only in combination with buildings. "
"Adding NDVI change and its initial level to the regression left the built-up coefficient essentially unchanged at 0.49 °C decade⁻¹ per 10 pp (0.41–0.58).",
"Two measured surface changes substantially attenuate the adjusted built-up coefficient (Fig. 6e, f). "
"Compared with rural land, urbanising pixels (ΔBF ≥ 10 pp) darkened (albedo change −0.061 against +0.003) and now emit far more light at night (median about 80 against 0.5 nW cm⁻² sr⁻¹), while their NDVI rose only slightly (+0.018 against +0.002). "
"Both changes scale with the amount of building: mean albedo fell by 0.021 in pixels gaining 2–5 pp and by 0.062 in those gaining at least 20 pp. "
"Adding albedo change to the regression reduced the built-up coefficient from 0.50 to 0.28 °C decade⁻¹ per 10 pp, adding night lights reduced it to 0.37, and adding all three variables reduced it to 0.20. "
"The full-period Landsat and DMSP versions of the same variables, which are noisier, give a smaller but consistent reduction (0.50 to 0.35). "
"Adding NDVI change on its own left the coefficient unchanged (0.498 to 0.498), so the reduction is carried by albedo and light, not by vegetation. "
"Including surface darkening and night-time light attenuates the adjusted built-up coefficient by 60% with the instrument-calibrated MODIS and VIIRS records and by 31% with the noisier full-period Landsat and DMSP series, consistent with a surface-energy explanation. "
"Because built-up fraction, albedo and light emission all change together as a city is built, these shares bound the contribution of the measured surface changes rather than partitioning it.",
"Taller development did not amplify the night signal; the height model below quantifies this. "
"Night-time excess trends were 0.57 °C decade⁻¹ in urbanising pixels with mean building height below 5 m, 0.79 at 5–10 m and 0.76 above 10 m, whose mean added built-up fractions were 8, 13 and 16 pp, so the effect per unit of building was, if anything, weaker where buildings are taller. "
"The urban night signal was strongest in summer: 0.57 °C decade⁻¹ per 10 pp (0.48–0.67) in June–September against 0.45 (0.34–0.55) in December–March (Fig. 6b), consistent with a contribution from waste heat released by air-conditioning.",
"Humidity does not explain the station results (Fig. 6d). "
"Night-time dewpoint trends were small at the urbanising stations (−0.07 to +0.22 °C decade⁻¹) and unrelated to urban growth. "
"Removing the dewpoint-related component left the trends far above the products: 1.31 to 1.30 °C decade⁻¹ at Dubai, 1.02 to 0.98 at Sharjah and, with the largest adjustment, 1.14 to 0.99 at Abu Dhabi — a 13% reduction that still leaves Abu Dhabi more than twice the ERA5-Land trend."]),
("3.7 Warm nights",
["The urban signal translates directly into the standard warm-night indices (Fig. 6c; Table S1). "
"TN90p, the percentage of nights above the 1991–2020 calendar-day 90th percentile, increased by 10.5, 8.8 and 7.5 percentage points per decade at Dubai, Abu Dhabi and Sharjah, against 3.3–3.6 in ERA5-Land at the same locations and an ensemble median of 5.6–6.1 in NEX-GDDP-CMIP6. "
"At Al Ain the station trend (5.0) was close to ERA5-Land (4.0), and at Ras Al Khaimah and Fujairah it was below it. "
"Tropical nights (Tmin ≥ 20 °C) increased by 22.2, 18.5 and 17.8 nights decade⁻¹ at the three city stations and by 2.7–4.3 at the two stations with little urban growth. "
"Nights with Tmin of at least 30 °C at Dubai rose from an average of 55 per year in 1995–1999 to 126 in 2020–2024."]),
("3.8 The signal is resolvable at the grid scale of the projections",
["The mismatch is not simply a matter of resolution. "
"Averaged into the 104 NEX-GDDP-CMIP6 0.25° cells that cover UAE land, cells with more built-up growth still show faster night-time warming, by 0.76 °C decade⁻¹ per 10 pp of cell-mean ΔBF (p < 10⁻⁹; Fig. 4b). "
"At the same cells, ERA5-Land Tmin trends decline slightly with ΔBF (−0.20 °C decade⁻¹ per 10 pp), as does the NEX-GDDP-CMIP6 ensemble (median −0.14; 5–95% of models −0.27 to 0.03), because the most urbanised cells lie on the coast where the regional background warming is slightly weaker. "
"A 0.25° product could therefore carry a substantial part of the urban night signal if it contained the relevant processes. The downscaled projections do not.",
"Away from the cities the products agree with the observations and with one another. "
"Over rural land as defined by the UN Degree of Urbanisation, night-time LST warmed by 0.41 °C decade⁻¹ over 1995–2024; ERA5-Land Tmin over the same land gives 0.41, and the NEX-GDDP-CMIP6 ensemble median is also 0.41 (5–95% of models 0.18–0.63). "
"The central estimates therefore align closely with the regional background, although individual-model trends vary; the products do not reproduce the increment over it in the cities."]),
("3.9 Magnitude relative to the IPCC AR6 projections",
["The urban component is large compared with the change that planning scenarios anticipate (Fig. S2; Table S2). "
"Relative to 1995–2014, NEX-GDDP-CMIP6 projects UAE-area Tmin warming of 0.98–1.18 °C in the near term (2021–2040) across the four scenarios, 1.48–2.45 °C in the mid term (2041–2060) and 1.42–5.52 °C in the long term (2081–2100). "
"Over the 2.9 decades separating the 1995 and 2024 trend endpoints, the observed Tmin trend at Dubai corresponds to a rise of 3.8 °C, of which 3.4 °C is absent from ERA5-Land; the corresponding missing rises are 2.5 °C at both Abu Dhabi and Sharjah and 0.7 °C at Al Ain. "
"In the UAE's largest cities, the night-time warming that has already occurred but is missing from the regional products therefore exceeds the median regional night-time warming projected for mid-century under the highest scenario, "
"and at Dubai reaches about three-quarters of the long-term SSP3-7.0 projection. "
"Where urban growth was small, as at Ras Al Khaimah and Fujairah, observed and product trends agree within their uncertainties."]),
("3.10 How urban form modifies the response",
["Building height modulates the built-up response rather than amplifying it: it reduces the marginal night-time warming associated with each further increment of built-up surface, confirming the pattern noted above with an explicit model (Table S4; Fig. S3a). "
"Among urbanising pixels, the night-time dose–response was 0.44 °C decade⁻¹ per 10 pp (95% CI 0.34–0.55) where mean building height was below 5 m, 0.34 (0.25–0.43) at 5–10 m and 0.14 (−0.01 to 0.29) above 10 m, the last not distinguishable from zero. "
"In the regression the interaction between added built-up fraction and height is correspondingly negative, at −0.36 °C decade⁻¹ per 10 pp per 10 m (95% CI −0.48 to −0.25).",
"The positive height term in the same model (0.22 °C decade⁻¹ per 10 m, 95% CI 0.13–0.30) should not be read as taller districts warming faster in general: in a model with an interaction it is the height effect at zero built-up growth, that is, among fabric already in place in 1995. "
"Combined with the interaction, the net height effect passes through zero at about 6 pp of added built-up surface and is −0.03 °C decade⁻¹ per 10 m at the mean increment of the urbanising pixels (6.8 pp). "
"Height therefore separates two different things: established tall fabric that continued to warm, and new construction whose effect per unit of added area is smaller where it goes upward.",
"The negative interaction is not simply saturation of cells that were already built up. Adding an explicit interaction between the 1995 built-up fraction and its increment left it at −0.28 (−0.39 to −0.18), and restricting the sample to pixels less than 10% built up in 1995 left it at −0.32 (−0.44 to −0.19). "
"The likeliest reading is that in high-rise districts much of the fabric added between 1995 and 2020 was vertical, so a change in built-up area understates the change in urban fabric. "
"The available height data cannot test that directly: the bulk height index is close to a rescaling of mean height (the Methods) and did not resolve the difference (0.11 °C decade⁻¹ per 10 m, 95% CI −0.07 to 0.28), and with a single 2018 snapshot no measure of height can distinguish fabric present in 1995 from fabric added since. "
"The vertical-growth explanation is therefore consistent with the data but not established by it.",
"Day-time LST showed no height effect (main effect p = 0.81, interaction p = 0.30). "
"The ERA5-Land interaction was statistically significant (0.03 °C decade⁻¹ per 10 pp per 10 m, 95% CI 0.00–0.05, p = 0.04) but an order of magnitude smaller than the night-time LST term and of opposite sign, which is what a null effect looks like in a sample of 75,528 pixels rather than an urban process in the reanalysis. "
"If the vertical-growth reading is right, built-up area is a conservative exposure measure in exactly the districts that are densifying fastest, and estimates of urban warming based on it will understate the effect there; testing this needs time-resolved building heights, which do not yet exist for the period."]),
("3.11 The response by Local Climate Zone",
["Classifying the same pixels by Local Climate Zone gives the result in the vocabulary used for urban-form comparison, and shows where that vocabulary runs out in a Gulf city (Table S3). "
"Built LCZ classes cover 2,736 km² of the UAE, dominated by large low-rise (1,647 km², 60% of built LCZ area), open low-rise (555 km², 20%) and sparsely built (328 km², 12%), with bare soil and sand covering 92% of the country. "
"Five built classes had enough 1 km cells to analyse. Night-time excess over coast-matched rural land was 0.53 °C decade⁻¹ (95% CI 0.23–0.72) in heavy industry, 0.47 (0.28–0.62) in large low-rise, 0.46 (0.31–0.58) in open low-rise, 0.25 (0.19–0.32) in sparsely built and 0.03 (−0.12 to 0.24) in compact low-rise, the last indistinguishable from zero. "
"Day-time trends were negative in every class, from −0.19 in sparsely built to −0.69 in open low-rise, and the ERA5-Land response was between −0.05 and −0.07 in all of them.",

"Two features of this table matter more than the ranking. "
"First, the classes differ in how much they grew, so the excess per unit of added built-up surface is the comparable quantity, and by that measure sparsely built land responds most strongly, at 0.15 °C decade⁻¹ per percentage point against 0.062–0.075 in heavy industry, large low-rise and open low-rise. "
"Compact low-rise is not included in that comparison: its excess is not distinguishable from zero, so the ratio is unstable and is not quoted. "
"The pattern matches the height interaction of Section 3.10, reached independently: conversion at the desert margin produces the largest response per unit of area converted, and already-dense fabric the smallest. "
"Second, the high-rise classes cannot be analysed at all. Compact high-rise, compact mid-rise, open mid-rise, open high-rise and lightweight low-rise together occupy 13 km² and yield at most two 1 km cells each. "
"The UAE's high-rise development is real and thermally distinctive but too spatially concentrated to resolve on a kilometre grid, so the LCZ framework at this resolution describes the low-rise majority of the country well and the towers not at all. "
"That is a property of the grid rather than of the classification, and it is the reason the continuous height variable of Section 3.10, which does not require a class to occupy a whole cell, carries the form analysis in this paper."]),
("3.12 How large the increment becomes by 2050",
["Expressed as accumulated warming, the measured response is 2.37 °C of additional night-time surface warming per 10 pp of added built-up surface (95% CI 1.95–2.78), using the 5 km predictor that matches the station analysis. "
"This figure is not a restatement of the 0.50 °C decade⁻¹ per 10 pp reported earlier and the two should not be compared directly: they are different estimands. "
"The earlier coefficient is a difference in warming rate estimated at the pixel scale; the coefficient used here is the warming accumulated over the whole analysis period, and it is estimated on the built-up increment averaged over a 5 km radius. "
"Each of those two changes raises the number — multiplying by the 2.9 decades of the period, and smoothing the predictor, which spreads a given amount of building over a larger area and so attaches more warming to each percentage point. "
"On the pixel-scale predictor the same accumulated coefficient is 1.45 °C per 10 pp (95% CI 1.21–1.69). "
"The 5 km version is used for the projection because it matches the scale at which the station evidence and the built-up scenarios are defined. "
"Applying it retrospectively to the observed 1995–2020 increments tests the magnitude, not the ordering: the prediction is a monotone function of built-up growth, so its rank agreement with the observed excess warming is the same correlation already reported for the stations above and carries no additional information. "
"On magnitude, the prediction is too small at the four stations that gained more than 1.5 pp of built-up surface, by factors of 1.5 (Sharjah), 1.6 (Al Ain), 3.2 (Dubai) and 4.0 (Abu Dhabi), and it predicts small increments at the two stations that gained less, where little or nothing was observed (0.18 and 0.28 °C predicted at Ras Al Khaimah and Fujairah against −0.35 and 0.02 °C observed). "
"Part of that shortfall is the conversion from surface to air temperature, for which the station response on the matched predictor is about twice the surface response; because that ratio rests on six stations and is not statistically resolved (see Limitations), the projection below is best read as a plausible lower bound rather than a bounded estimate. "
"The spread of the individual ratios, from 1.5 to 4.0 at the growing stations, is the honest measure of how well the transfer performs (Fig. S3b).",
"UAE built-up surface reached 618 km² at the last observation-supported epoch, 2020. Continuing each cell's 2010–2020 growth rate for thirty years gives 1,068 km² by 2050 (S-high), and half that rate 847 km² (S-low). "
"The implied additional night-time surface warming between 2020 and 2050 is 1.66 °C (95% CI 1.37–1.95) around Sharjah under S-high and 0.86 °C under S-low, 1.18 and 0.59 °C around Abu Dhabi, 1.05 and 0.51 °C around Dubai, 0.77 and 0.38 °C around Al Ain, 0.35 and 0.17 °C at Fujairah and 0.29 and 0.14 °C at Ras Al Khaimah (Table 5; Fig. 7a). "
"Two alternative growth baselines bracket these figures: a 2005–2020 rate gives 1.76 and 0.93 °C around Sharjah, and the 2010–2025 rate based on the projected 2025 layer gives 1.14 and 0.58 °C, the lowest of the three because that layer implies a slowdown after 2020 that the observations do not yet support. "
"For comparison, the ensemble-median UAE-area Tmin change for 2041–2060 relative to 1995–2014 is 1.48 °C under SSP1-2.6 (26 models), 1.80 under SSP2-4.5 (28), 1.96 under SSP3-7.0 (23) and 2.45 under SSP5-8.5 (27) (Table S2). "
"These two quantities are not the same variable: the increment is a surface temperature and the projection a 2 m air temperature, and the comparison is made because the urban increment has no counterpart in the projections at all, not because the two are interchangeable. "
"With that qualification, the increment around Sharjah is equivalent to 35–112% of the projected mid-century change, depending on scenario and emissions pathway — in the SSP2-4.5 case, 92% under S-high and 48% under S-low. "
"Under both growth scenarios it exceeds the mid-century difference between SSP1-2.6 and SSP3-7.0, which is 0.48 °C. "
"At the more slowly growing stations the increment is smaller: around Dubai it is 58% (S-high) and 28% (S-low) of the SSP2-4.5 mid-century change.",

"Three quantities multiply to give the projected increment in air temperature — the built-up increment, the accumulated surface response and the surface-to-air conversion — so their relative uncertainties can be decomposed (Fig. 7b; Table S5). "
"Expressed as one standard deviation of the logarithm, the dose–response coefficient contributes 9%, the built-up growth scenario 20% (treating S-low and S-high as the bounds of a uniform range) and the surface-to-air conversion 41%. "
"In variance terms the conversion accounts for 78% of the total, the growth scenario for 19% and the dose–response coefficient for 4%. "
"The dominant uncertainty in this calculation is therefore neither the climate scenario nor the measured urban response, both of which are comparatively well constrained, but the step from surface to air temperature, which rests on six stations. "
"Propagating all three gives an additional night-time air warming around Sharjah of 3.4 °C by 2050 under S-high, with a 95% interval of 1.4–8.5 °C. "
"That interval is wide enough that the air-temperature figure should be read as an order of magnitude rather than an estimate, which is why the surface increment, at 1.66 (1.37–1.95) °C, is quoted as the headline result. "
"For scale, the model spread on the background projection is of comparable relative size: the 5–95% range across models for SSP2-4.5 at mid-century spans 1.36–2.62 °C, 70% of the median. "
"The practical implication is specific: a denser urban and rural air-temperature network, not a better climate model or a better urban dataset, is what would narrow this projection."]),
]

DISCUSSION = [
("4.1 Why urban growth warms nights and cools days in a hot desert",
["The evidence indicates that the rapid night-time warming at the UAE's main city stations is an urban signal. "
"Four independent lines of evidence point the same way, and the main alternative explanations do not account for it. "
"The strongest of the four is the event study: pixels that were built on diverge from matched never-built land after conversion, at night only, an order of magnitude more than they do before it. "
"That ordering in time does not by itself establish causation, but it removes the explanation that would otherwise be hardest to rule out, namely that land selected for development was already warming faster than land that was not. "
"The station trend missing from ERA5-Land scales with nearby urban growth but not with distance from the coast. "
"Satellite night-time LST shows a steady increase in trend with built-up growth at fixed coastal distance, and the same gradient appears when rural land is defined by the UN Degree of Urbanisation rather than by our own thresholds. "
"Both the satellite and station differences grew over time as the built-up area expanded. "
"A coastal explanation would require the missing warming to be largest at Fujairah, the station closest to the sea, where it is zero. "
"A station-siting explanation cannot account for the same built-up gradient in an independent satellite record over 75,528 pixels, nor for the fact that removing the only significant discontinuity in the Dubai difference series increases the estimate. "
"Land that greened without being built on warmed about five times less at night than urbanising land, and station humidity trends were small and unrelated to urban growth. "
"A satellite retrieval artefact, such as a fixed emissivity applied to land that changed from sand to buildings, would bias day and night trends in the same direction, whereas the observed responses have opposite signs.",
"The mechanisms can be partly quantified. Adding the satellite-measured surface changes to the regression reduces the built-up coefficient by about 60% with the MODIS and VIIRS records and by 31% with the full-period Landsat and DMSP series, the reduction being carried by albedo darkening and rising night-time light emission rather than by vegetation, "
"which points to increased absorbed solar energy stored in urban fabric and to waste heat. "
"This is a statistical decomposition, not a closed energy budget. Built-up fraction, albedo and light emission change together as a city is built, so the individual shares cannot be separated cleanly, and the design measures no surface energy fluxes; "
"the 60% should be read as the part of the built-up effect that these two observable surface changes can stand in for, not as a causal attribution to them. "
"Night-time light is in addition only an indirect proxy for anthropogenic heat: in a Gulf city the dominant waste-heat source is air-conditioning, whose load peaks in the afternoon and is not what the lights measure. "
"The opposite daytime and night-time responses fit the known energy balance of desert cities. "
"Replacing dry sand with concrete, asphalt and buildings increases heat storage and reduces the sky view that controls night-time long-wave cooling, and air-conditioning then releases stored and waste heat at night (Oke, 1982). "
"During the day, irrigation, shading by tall buildings and higher thermal inertia keep urban surfaces cooler than the very hot surrounding desert, producing the daytime urban cool island reported for Abu Dhabi (Lazzarini et al., 2015). "
"Three results constrain these processes: the daytime cool island persisted where urbanising land did not green, so it is not only an irrigation effect; the night signal was about 30% stronger in summer than in winter, when cooling demand is highest; and urban albedo fell by 0.06 while rural albedo did not change. "
"Our estimates extend the Dubai surface heat-island results of Elhacham and Alpert (2021) in three ways: to the whole country, to a 30-year record, and to station air temperature and standard warm-night indices.",

"The height result deserves a physical reading rather than a statistical one, because it runs against the usual expectation. "
"Taller buildings reduce the sky view that controls long-wave cooling, so the textbook prediction is that added building should warm nights more, not less, where buildings are tall. "
"We find the opposite for the marginal effect, and four explanations are consistent with the data. "
"First, and in our view most likely, built-up area is the wrong measure of what is added in a high-rise district: growth there is largely vertical, so a given increment of plan area accompanies far more new fabric than the same increment on the periphery, and the response per unit of area is correspondingly diluted. "
"Second, the surface being replaced differs. Peripheral growth converts bare desert, which has the largest thermal contrast with urban fabric; densification replaces land that is already partly built, so the marginal change in surface properties is smaller. "
"Third, shading and the greater thermal inertia of tall districts suppress daytime surface heating, leaving less stored heat to release at night — the mechanism that produces the daytime cool island may also damp the night-time increment. "
"Fourth, saturation: dense districts were already partly converted in 1995. We tested this one directly and it accounts for only part of the effect, since the interaction survives both an explicit control for the 1995 built-up fraction and restriction to pixels that were less than 10% built up.",

"The first three cannot be separated with the data used here, and each implies a different test. "
"Time-resolved building heights, from repeated height products or from interferometric or stereo imagery, would settle the first by allowing built volume rather than built area to be used as the exposure variable. "
"The second is addressable with a land-cover-transition analysis that distinguishes desert-to-urban from urban-to-denser-urban conversion at the pixel scale. "
"The third predicts a specific signature — a stronger daytime cool island in tall districts — which our daytime results neither confirm nor rule out, since the daytime height terms are not statistically resolved; sub-daily land-surface temperature with a consistent overpass would test it. "
"What the result does establish is narrower but useful for planning: where cities grow upward, the built-up area that planners and global datasets record understates the change in urban fabric, so exposure measures based on area will understate the warming those districts have experienced."]),
("4.2 Using the result: correcting the products and choosing urban form",
["Earlier comparisons of UAE stations with regional products could not determine whether the large station trends indicated product error, station problems or a genuine local signal. "
"The present analysis resolves that ambiguity. "
"The central estimates from ERA5-Land and the downscaled ensemble closely match the regional and rural background: rural LST, ERA5-Land and the NEX-GDDP-CMIP6 ensemble median each give about 0.41 °C decade⁻¹ of warming over 1995–2024, although individual model trends vary, and the area-scale diurnal ratios agree across products. "
"What these products lack is the urban increment, and the reason is structural. "
"ERA5-Land runs the CHTESSEL scheme offline over tiles for vegetation, bare soil, snow and water, with no urban tile, and performs no assimilation itself, so the product has no mechanism by which an urbanisation trend in the land surface could arise (Muñoz-Sabater et al., 2021). "
"Its ERA5 forcing is assimilated, so a small indirect urban influence is possible in principle; the near-zero response of ERA5-Land to built-up growth measured here (−0.01 °C decade⁻¹ per 10 pp) indicates that in practice it is negligible. "
"NEX-GDDP-CMIP6 bias-corrects each model against the Global Meteorological Forcing Dataset for 1960–2014 and then disaggregates spatially; that procedure rescales the distribution but transfers the driving model's trend, and the CMIP6 land components either omit urban land or hold its extent fixed (Sheffield et al., 2006; Zhao et al., 2021; Thrasher et al., 2022). "
"The agreement of three independent quantities supports this reading: rural night-time LST, ERA5-Land Tmin and the NEX-GDDP-CMIP6 ensemble median all give about 0.41 °C decade⁻¹. "
"The convergence of the central estimates on the rural value, together with the absence of a positive relationship with built-up growth, indicates that the products capture the regional background while omitting or strongly attenuating the additional local urban process. "
"Consistently, the increment is not a sub-grid detail that coarse grids inevitably lose: it remains clear at 0.25° (Fig. 4b).",

"The result also addresses the standing objection to observation-minus-reanalysis estimates, that reanalyses represent multidecadal variability weakly and that the difference is therefore sensitive to the period analysed (Wang et al., 2013). "
"Three features of the present design limit that risk. The period was fixed by the WMO 30-year convention rather than chosen; ERA5-Land performs no assimilation of its own, so it cannot absorb the urban signal from the stations directly; "
"and the stations with little urban growth return a difference indistinguishable from zero (−0.12 and 0.01 °C decade⁻¹), which is the control the method requires and which a general variability deficit would not produce. "
"Above all, the same dose–response appears in a satellite record that involves no reanalysis at all.",
"For planning, this has a direct consequence. "
"Heat-health warning thresholds, cooling-energy demand, outdoor-work regulation and building design standards derived from ERA5-Land or NEX-GDDP-CMIP6 will underestimate current night-time temperatures and warm-night frequencies in the fastest-growing districts, "
"where TN90p has risen two to three times faster than the reanalysis indicates. "
"Projections of future change will also omit the component that planning decisions themselves control. "
"One practical approach is to evaluate an observationally constrained urban increment alongside regional projections while keeping the surface-to-air conversion uncertainty explicit. "
"The projection above gives one: 2.37 °C of accumulated night-time surface warming per 10 pp of added built-up surface, which under a continuation of observed 2010–2020 growth adds 0.5–1.7 °C to mid-century night-time warming in the fastest-growing districts. "
"Around Sharjah, the fastest-growing, that is half to almost all of the projected SSP2-4.5 regional change again; around Dubai between a quarter and three-fifths of it. "
"The increment is a surface quantity set against an air-temperature projection, and the station evidence suggests the air response is about twice as large, so these figures are probably conservative — but that ratio is not statistically resolved and the comparison should be read as an order of magnitude, not a correction factor. "
"Urban-resolving regional models remain the process-based alternative.",

"The measurements also identify which levers matter, and how much. "
"Surface darkening is the largest single one: urban albedo fell by 0.06 over the period while rural albedo did not change, and adding albedo to the mediation model reduces the adjusted built-up coefficient by 44%, compared with 26% for night-time light emission. "
"Raising the albedo of roofs and pavements therefore acts on the dominant measured pathway, and it acts where the warming is, since the darkening scales with the amount of building (0.021 in pixels gaining 2–5 pp against 0.062 in those gaining at least 20 pp). "
"Vegetation works differently and should not be expected to do the same job: land that greened without being built on warmed 0.16 °C decade⁻¹ faster than rural desert at night, so irrigated landscaping does not by itself remove the night-time signal — but it cooled days by 0.14, and the daytime cool island in urbanising land is strongest where greening occurred. "
"Greening is thus a daytime instrument and albedo a night-time one, which matters in a region where the health burden is nocturnal. "
"Urban form is the third lever, and the height result gives it a specific meaning: because vertical growth adds fabric that built-up area does not record, density targets expressed in plan area will understate the thermal consequence of building upward.",

"For the standards that translate climate data into decisions, the consequences are quantifiable. "
"Heat-health warning thresholds set from reanalysis will be exceeded more often than the reanalysis implies, because TN90p at the city stations has risen two to three times faster than in ERA5-Land. "
"Nights above 30 °C at Dubai rose from 55 per year in 1995–1999 to 126 in 2020–2024, a change in exposure that no product used for planning contains. "
"Cooling-demand projections are affected in the same direction and most in the season that matters: the urban response is about 30% larger in summer than in winter. "
"And because the increment scales with built-up growth rather than with emissions, it is the component of future night-time heat that local decisions control — which is the practical reason for measuring it separately from the regional signal."]),
("4.3 The UAE among hot desert cities",
["The UAE result is not a local peculiarity. The diurnal asymmetry reported here — rapid night-time warming with little or negative daytime change — is the signature reported across hot desert cities, although the present study is the first to test whether the planning products contain it. "
"At Doha, Tmin rose about 1 °C decade⁻¹ over 1983–2012 against about 0.5 °C decade⁻¹ for Tmax, during a fivefold increase in population, which the authors attributed in part to urbanisation (Cheng et al., 2017). "
"At Phoenix, mid-summer Tmin at the urban station rose about 1 °C decade⁻¹ over 1948–2000 while Tmax showed no significant change (Baker et al., 2002). "
"Across six Saudi Arabian cities over 1994–2024, urban areas were warmer than their rural surroundings at night but cooler by day, the daytime reversal being attributed to urban greening and landscaping (Munir et al., 2025). "
"Canopy-layer measurements in Kuwait likewise find a nocturnal heat island with a weak or reversed daytime signal (AlKhaled et al., 2024), and the Abu Dhabi and Dubai surface studies report the same asymmetry (Lazzarini et al., 2015; Elhacham and Alpert, 2021).",
"The UAE station values sit within this range rather than above it: Dubai, Abu Dhabi and Sharjah at 1.0–1.3 °C decade⁻¹ are comparable to Doha and Phoenix, and the daytime cool island matches the Saudi and Abu Dhabi findings. "
"What distinguishes the UAE is the pace of the land-cover change that drives it — built-up surface doubled in 25 years — which makes the urban increment unusually easy to separate from the regional trend and provides the dose–response gradient the analysis rests on. "
"The UAE is therefore best read as a model system rather than a special case: the same physical setting occurs widely, but rarely with a land-cover change large enough to separate the urban increment from the regional trend within a single 30-year record. "
"Four conditions produce the effect measured here, and none is specific to the UAE. "
"Arid surroundings give a large thermal contrast between bare sand and urban fabric, which is what makes the night-time signal and the daytime cool island both large. "
"Near-universal mechanical cooling adds waste heat at night. "
"High-thermal-mass construction with little vegetated cover stores daytime radiation and releases it after sunset. "
"And rapid, spatially concentrated construction supplies the dose–response gradient that identification depends on.",

"Those conditions are met across the Gulf Cooperation Council states, where the published records for Doha, Kuwait City and the Saudi cities already show the night-warming and daytime-cooling pattern reported here (Cheng et al., 2017; AlKhaled et al., 2024; Munir et al., 2025); in the expanding cities of North Africa and the wider Middle East; and, with the same surface physics, in the desert cities of the southwestern United States, where the Phoenix record shows the same diurnal asymmetry over a much longer period (Baker et al., 2002). "
"We have not measured built-up growth in those cities and make no claim about its rate; the point is that the physical setting and the products are the same. "
"The products at issue are global. ERA5-Land carries no urban tile, and the statistical downscaling behind NEX-GDDP-CMIP6 introduces no time-varying urban land cover, so wherever cities have grown quickly the same component will be absent from both, not only over the UAE; the UAE is simply a place where its size can be measured. "
"The quantitative coefficients reported here should not be transferred to other cities without local calibration — the response depends on the surrounding surface, the building stock and the cooling load, all of which vary — but the design can be: stations, a satellite dose–response against a Degree of Urbanisation rural reference, and the same comparison against the products, using data that exist globally. "
"Applying it across the Gulf and the wider arid subtropics is the obvious extension of this work, and would establish whether the increment measured here is typical of rapidly urbanising hot desert cities or unusually large."]),
("4.4 Limitations",
["Three limitations bear on how the results should be read. "
"First, land-surface temperature is not air temperature: the satellite analysis establishes the spatial structure and dose–response of the urban signal, and the station analysis supplies the air-temperature magnitude, but the two are distinct quantities and the conversion between them is the largest single uncertainty in the projection (Fig. 7b). "
"Second, the station network is small, consists of airports and has no documented histories, so the Pettitt test is a homogeneity screen rather than full homogenisation; the station evidence is therefore strongest in combination with the satellite evidence, which does not depend on station siting. "
"Third, building height is a single 2018 snapshot, so urban form enters only as a cross-sectional modifier and the vertical-growth interpretation of the height interaction remains untested. The Local Climate Zone analysis is limited in the same way and additionally cannot resolve the high-rise classes at 1 km, so both form results describe low-rise and mid-density fabric.",
"Data limitations that constrain the mechanism analysis are documented in Methods and summarised here: the satellite record joins several sensors and loses 2018 to an instrument gap, mitigated but not removed by urban-minus-rural differencing and by reporting each sensor era separately; MODIS could not provide an independent check because its quality-screened night-time record is too sparse over desert; Landsat albedo is a narrow-to-broadband conversion; DMSP night lights saturate in city centres, and the VIIRS mediator is a 2024 level rather than a change. "
"Night-time light is an indirect proxy for waste heat, whose dominant source in a Gulf city is air-conditioning. "
"ERA5-Land is a model product used here to represent the regional background, not as ground truth, and NEX-GDDP-CMIP6 is represented by one realisation per model.",
"The projection to 2050 is a scenario calculation rather than a prediction. It assumes that accumulated warming scales with the size of the built-up increment rather than its rate, that the dose–response continues to hold as cities densify, and that growth follows the extrapolated GHS trajectory; the uncertainty decomposition quantifies the consequences of the first assumption and shows the surface-to-air conversion to dominate. "
"These limitations point to three priorities, in order of value: a denser urban and rural air-temperature network with documented histories, which would resolve the dominant uncertainty; time-resolved building heights, which would convert the form result from cross-sectional to causal; and urban-resolving simulations for the Gulf, which would allow the increment to be projected rather than extrapolated."]),
]

CONCLUSIONS = [
"The urban increment in night-time warming is large, measurable, follows conversion in time, and is absent from the products used to plan for heat. "
"Over the standard 30-year period 1995–2024, Tmin at Dubai, Abu Dhabi and Sharjah rose by 1.0–1.3 °C decade⁻¹, about three times the regional background, while stations with little nearby urban growth warmed at or below that background. "
"Across the country, night-time LST trends rose steadily with added built-up surface, by about 0.5 °C decade⁻¹ per 10 percentage points, whereas daytime trends fell. "
"The signal is independent of distance from the coast, is not explained by greening or humidity, is strongest in summer, persists across satellite-sensor eras, and remains resolvable at 0.25°. "
"Adding satellite-measured albedo darkening and night-time light emission to the model reduces the adjusted built-up coefficient by 31–60%, depending on which surface record is used. "
"The response also varies with urban form: each added percentage point of built-up surface raises the night-time trend less where buildings are tall, which suggests that area-based exposure measures understate urban change where cities grow upward.",
"ERA5-Land and the NEX-GDDP-CMIP6 ensemble median closely match the regional background, although individual-model trends vary, while neither product reproduces the observed relationship between local urban growth and night-time warming. "
"In the largest cities, the night-time warming since 1995 that is missing from the reanalysis already exceeds the UAE-area warming projected for mid-century under SSP5-8.5, and warm nights have increased two to three times faster than the reanalysis indicates. "
"If built-up growth continues at the rate observed over 2010–2020, the same response adds 0.5–1.7 °C of night-time surface warming by 2050 in the fastest-growing districts; around Sharjah that is between a third of the projected mid-century air-temperature change and slightly more than all of it, depending on the emissions pathway, and under either growth rate it exceeds the mid-century difference between the lowest and a high emissions scenario. "
"Heat planning in rapidly urbanising hot desert regions should therefore evaluate an observationally constrained urban increment alongside regional products, and should treat urban form as a lever that controls part of future night-time heat.",
]

DATA_AVAIL = ("All primary datasets are publicly available: HadISD (Met Office Hadley Centre), the C3S satellite land-surface temperature record (Copernicus Climate Data Store), "
"GHS-BUILT-S, GHS-BUILT-H and GHS-SMOD R2023A (European Commission Joint Research Centre), MODIS MOD13A2 and MCD43A3 and Landsat Collection 2 (NASA/USGS), "
"DMSP-OLS and VIIRS night-time lights (NOAA), ERA5-Land (Copernicus Climate Data Store), NEX-GDDP-CMIP6 (NASA Center for Climate Simulation) and GADM 4.1. "
"Processed annual station series, pixel trend fields, urban–rural tables and analysis scripts will be deposited in a public repository with a persistent identifier on acceptance.")

REFERENCES = [
"AlKhaled, S., Coseo, P., Brazel, A., Cheng, C., Sailor, D. (2024) Diurnal and seasonal dynamics of the canopy-layer urban heat island of Kuwait. International Journal of Climatology 44. doi:10.1002/joc.8560.",
"Baker, L.A., Brazel, A.J., Selover, N., et al. (2002) Urbanization and warming of Phoenix (Arizona, USA): impacts, feedbacks and mitigation. Urban Ecosystems 6. doi:10.1023/A:1026101528700.",
"Benjamini, Y., Hochberg, Y. (1995) Controlling the false discovery rate: a practical and powerful approach to multiple testing. Journal of the Royal Statistical Society B 57, 289–300.",
"Chakraborty, T.C., Qian, Y. (2024) Urbanization exacerbates continental- to regional-scale warming. One Earth 7, 1387–1401. doi:10.1016/j.oneear.2024.05.005.",
"Copernicus Climate Change Service (C3S) (2023) Land surface temperature monthly gridded data from 1995 to present derived from satellite observations. Copernicus Climate Change Service Climate Data Store.",
"Cheng, W.L., Saleem, A., Sadr, R. (2017) Recent warming trend in the coastal region of Qatar. Theoretical and Applied Climatology 128. doi:10.1007/s00704-015-1693-6.",
"Dahy, B., Al-Memari, M., Al-Gergawi, A., Burt, J.A. (2024) Remote sensing of 50 years of coastal urbanization and environmental change in the Arabian Gulf: a systematic review. Frontiers in Remote Sensing 5. doi:10.3389/frsen.2024.1422910.",
"Didan, K. (2021) MODIS/Terra Vegetation Indices 16-Day L3 Global 1 km SIN Grid V061. NASA EOSDIS Land Processes DAAC.",
"Dijkstra, L., Florczyk, A.J., Freire, S., et al. (2021) Applying the Degree of Urbanisation to the globe: a new harmonised definition reveals a different picture of global urbanisation. Journal of Urban Economics 125, 103312.",
"Dunn, R.J.H., Willett, K.M., Thorne, P.W., et al. (2012) HadISD: a quality-controlled global synoptic report database for selected variables at long-term stations from 1973–2011. Climate of the Past 8, 1649–1679.",
"Demuzere, M., Kittner, J., Martilli, A., et al. (2022) A global map of local climate zones to support earth system modelling and urban-scale environmental science. Earth System Science Data 14, 3835–3873.",
"Elhacham, E., Alpert, P. (2021) Temperature patterns along an arid coastline experiencing extreme and rapid urbanization, case study: Dubai. Science of the Total Environment 784, 147168.",
"Elvidge, C.D., Baugh, K., Zhizhin, M., Hsu, F.C., Ghosh, T. (2017) VIIRS night-time lights. International Journal of Remote Sensing 38, 5860–5879.",
"Grimmond, C.S.B., Oke, T.R. (1999) Aerodynamic properties of urban areas derived from analysis of surface form. Journal of Applied Meteorology 38, 1262–1292.",
"Hamed, K.H., Rao, A.R. (1998) A modified Mann–Kendall trend test for autocorrelated data. Journal of Hydrology 204, 182–196.",
"He, C., Kim, H., Hashizume, M., et al. (2022) The effects of night-time warming on mortality burden under future climate change scenarios: a modelling study. The Lancet Planetary Health 6, e648–e657.",
"IPCC (2021) Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change. Cambridge University Press, Cambridge and New York.",
"Kalnay, E., Cai, M. (2003) Impact of urbanization and land-use change on climate. Nature 423, 528–531.",
"Künsch, H.R. (1989) The jackknife and the bootstrap for general stationary observations. Annals of Statistics 17, 1217–1241.",
"Lazzarini, M., Molini, A., Marpu, P.R., Ouarda, T.B.M.J., Ghedira, H. (2015) Urban climate modifications in hot desert cities: the role of land cover, local climate, and seasonality. Geophysical Research Letters 42, 9980–9989.",
"Liang, S. (2001) Narrowband to broadband conversions of land surface albedo: I. Algorithms. Remote Sensing of Environment 76, 213–238.",
"Liu, S., Wang, Y., Gong, P., et al. (2025) Regional warming from urbanization is disproportionate to urban expansion rate. One Earth 8, 101234. doi:10.1016/j.oneear.2025.101234.",
"Manoli, G., Fatichi, S., Schläpfer, M., et al. (2019) Magnitude of urban heat islands largely explained by climate and population. Nature 573, 55–60.",
"Muñoz-Sabater, J., Dutra, E., Agustí-Panareda, A., et al. (2021) ERA5-Land: a state-of-the-art global reanalysis dataset for land applications. Earth System Science Data 13, 4349–4383.",
"Munir, S., Habeebullah, T.M.A., Zamreeq, A.O., et al. (2025) Cooling of maximum temperatures in six Saudi Arabian cities (1994–2024) — reversal of urban heat islands. Urban Science 9, 445. doi:10.3390/urbansci9110445.",
"Oke, T.R. (1982) The energetic basis of the urban heat island. Quarterly Journal of the Royal Meteorological Society 108, 1–24.",
"Pesaresi, M., Schiavina, M., Politis, P., et al. (2024) Advances on the Global Human Settlement Layer by joint assessment of Earth Observation and population survey data. International Journal of Digital Earth 17, 2390454.",
"Pettitt, A.N. (1979) A non-parametric approach to the change-point problem. Journal of the Royal Statistical Society C 28, 126–135.",
"Raymond, C., Matthews, T., Tuholske, C. (2024) Evening humid-heat maxima near the southern Persian/Arabian Gulf. Communications Earth & Environment 5, 591.",
"Sen, P.K. (1968) Estimates of the regression coefficient based on Kendall's tau. Journal of the American Statistical Association 63, 1379–1389.",
"Sheffield, J., Goteti, G., Wood, E.F. (2006) Development of a 50-year high-resolution global dataset of meteorological forcings for land surface modeling. Journal of Climate 19, 3088–3111.",
"Stewart, I.D., Oke, T.R. (2012) Local climate zones for urban temperature studies. Bulletin of the American Meteorological Society 93, 1879–1900.",
"Smith, A., Lott, N., Vose, R. (2011) The Integrated Surface Database: recent developments and partnerships. Bulletin of the American Meteorological Society 92, 704–708.",
"Thrasher, B., Wang, W., Michaelis, A., Melton, F., Lee, T., Nemani, R. (2022) NASA Global Daily Downscaled Projections, CMIP6. Scientific Data 9, 262.",
"Ullah, W., Alabduoli, K., Ullah, S., et al. (2024) Comparison of 2-m surface temperature data between reanalysis and observations over the Arabian Peninsula. Atmospheric Research 311, 107725. doi:10.1016/j.atmosres.2024.107725.",
"Vinodhkumar, B., Ullah, S., Lakshmi Kumar, T.V., Al-Ghamdi, S.G. (2024) Amplification of temperature extremes in Arabian Peninsula under warmer worlds. Scientific Reports 14, 16656.",
"Wang, J., Yan, Z., Jones, P.D., Xia, J. (2013) On \"observation minus reanalysis\" method: a view from multidecadal variability. Journal of Geophysical Research: Atmospheres 118. doi:10.1002/jgrd.50574.",
"WMO (2017) WMO Guidelines on the Calculation of Climate Normals. WMO-No. 1203. World Meteorological Organization, Geneva.",
"Zhang, X., Alexander, L., Hegerl, G.C., et al. (2011) Indices for monitoring changes in extremes based on daily temperature and precipitation data. WIREs Climate Change 2, 851–870.",
"Zhao, L., Oleson, K., Bou-Zeid, E., et al. (2021) Global multi-model projections of local urban climates. Nature Climate Change 11, 152–157.",
"Zittis, G., Almazroui, M., Alpert, P., et al. (2022) Climate change and weather extremes in the Eastern Mediterranean and Middle East. Reviews of Geophysics 60, e2021RG000762.",
]

FIG_CAPTIONS = {
    '1': 'Figure 1. Urban growth and station network. (a) Increase in built-up fraction between 1995 and 2020 from GHS-BUILT-S (percentage points, shown where at least 1 pp); grey shading marks areas already at least 5% built up in 1995 and green outlines mark UN urban centres in 2020. Triangles show the HadISD stations: DXB, Dubai International; SHJ, Sharjah; AUH, Abu Dhabi International; AZI, Al Bateen; AAN, Al Ain; RAK, Ras Al Khaimah; FJR, Fujairah. (b) UAE built-up surface by GHSL epoch, and land in UN urban centres, for which the settlement grid is available for 1995, 2000 and 2020 only; shading marks the 1995–2024 analysis period.',
    '2': 'Figure 2. Station night-time warming and the regional products. (a) Theil–Sen trends for 1995–2024 in station Tmin (with 95% moving-block-bootstrap intervals) and Tmax, ERA5-Land Tmin at the nearest cell, and NEX-GDDP-CMIP6 Tmin (median and 5–95% range of 28 models) at the same locations; labels give the built-up fraction added within 5 km between 1995 and 2020 (ΔBF). (b) Station-minus-ERA5-Land Tmin trend (missing warming) against ΔBF within 5 km, with 95% intervals. (c) Annual Tmin anomalies at Dubai International and the nearest ERA5-Land cell, relative to 1995–2020.',
    '3': 'Figure 3. Theil–Sen trends for 1995–2024 over the northern UAE. (a) Night-time and (b) daytime satellite land-surface temperature (LST), with stippling where the Benjamini–Hochberg false-discovery rate is below 5%. (c) ERA5-Land Tmin on the same grid. Black contours enclose areas where built-up fraction increased by at least 10 percentage points between 1995 and 2020; triangles mark stations.',
    '4': 'Figure 4. Dose–response of warming trends to urban growth. (a) Difference between trends in urbanising pixels and coast-matched rural pixels by class of added built-up fraction, for night-time and daytime LST and for ERA5-Land Tmin and Tmax sampled at the same pixels; rural land is defined by the UN Degree of Urbanisation. Error bars are 95% spatial block-bootstrap intervals; n is the number of urban pixels. (b) Night-time LST and ERA5-Land Tmin trends in the 104 NEX-GDDP-CMIP6 0.25° cells over UAE land against the cell-mean added built-up fraction, with least-squares fits; the legend gives the corresponding NEX-GDDP-CMIP6 ensemble slope.',
    '6': 'Figure 6. Mechanisms, alternative explanations and warm nights. (a) Night-time and daytime LST trend minus the coast-matched rural trend for land that changed without building (greening, ΔNDVI ≥ 0.05; browning, ΔNDVI ≤ −0.02), for urbanising land (added built-up fraction ≥ 10 pp) without and with greening, and for urbanising pixels (≥ 5 pp) by mean building height (< 5 m, 5–10 m, > 10 m). (b) Regression coefficient per 10 pp of added built-up fraction for annual, summer and winter LST trends. (c) Trends in the ETCCDI warm-night index TN90p (base period 1991–2020) at stations, the nearest ERA5-Land cell and NEX-GDDP-CMIP6 (median and 5–95% of 28 models). (d) Station Tmin trends before and after removing the component related to night-time dewpoint; labels give the dewpoint trend (°C decade⁻¹). (e) The built-up coefficient for night-time LST when satellite-measured mechanisms are added to the regression. (f) Decrease in albedo and change in NDVI between the early 2000s and the early 2020s, and night-time light emission in 2024, by class of added built-up fraction; dotted lines mark the rural values. Error bars, where shown, are 95% intervals; panels d and f show point estimates only.',
    'S1': 'Figure S1. Evolution of the urban LST signal. Annual differences between urbanising pixels (added built-up fraction of at least 10 percentage points) and coast-matched rural pixels for night-time and daytime LST, with linear fits, and total UAE built-up surface (right axis). Grey bands mark the transitions between the successive sensor eras of the satellite record (1995–2002, 2003–2011 and 2013–2024); the hatched bar marks the 2018 gap.',
    'S2': 'Figure S2. Missing urban night-time warming compared with the IPCC AR6 projections. Box plots show NEX-GDDP-CMIP6 UAE-area Tmin change relative to 1995–2014 for the AR6 near-term, mid-term and long-term periods under four scenarios (box: interquartile range; whiskers: 5–95%; dots: individual models). Bars show the observed station Tmin rise over 1995–2024 (trend × 2.9 decades); the dark portion is the part absent from ERA5-Land at the same location.',
    'S3': "Figure S3. Urban form and the retrospective check on the transfer coefficient. (a) Night-time LST dose–response (change in trend per 10 percentage points of added built-up fraction) for urbanising pixels grouped by mean building height in 2018; error bars are 95% cluster-robust confidence intervals and the dashed line is the all-pixel estimate. (b) Observed station excess warming over 1995–2024 against the value predicted from each station's built-up increment using the same coefficient; the line is 1:1. The horizontal axis is a surface-temperature prediction and the vertical axis an air-temperature observation, so departure from the line includes the conversion between the two as well as any error in the coefficient.",
    '5': 'Figure 5. Night-time land-surface temperature before and after built-up conversion. Each treated pixel is differenced against the mean of never-built control pixels in the same coastal-distance band and emirate, and normalised to its own mean over the five years before conversion; shading is the 95% block-bootstrap interval over 0.25° blocks. (a) Night-time and (b) day-time difference from matched controls against years from conversion, for the treated pixels of the 2005, 2010 and 2015 cohorts (432 at night, 433 by day); the dashed line marks the conversion date and grey shading the pre-conversion window. (c) Sensitivity to the built-up threshold used to date conversion: the bootstrap p value of the pre-conversion slope (left axis) and the mean night-time level three to ten years after conversion (right axis). The estimated effect is stable across datings; only the timing test depends on the choice. Slopes, levels and their p values are estimated inside each bootstrap replicate.',
    '7': 'Figure 7. The urban increment to 2050 and where its uncertainty lies. (a) Additional night-time surface warming between 2020 and 2050 within 5 km of each station, under continuation of the observed 2010–2020 built-up growth rate (S-high) and half that rate (S-low); error bars are 95% confidence intervals from the dose–response. Vertical lines give the NEX-GDDP-CMIP6 UAE-area Tmin change for 2041–2060 relative to 1995–2014 under two scenarios; those are 2 m air temperatures and the bars are surface temperatures, so the comparison shows relative magnitude rather than a common variable. (b) Share of the projection variance contributed by the surface-to-air conversion, the built-up growth scenario and the dose–response coefficient. Station codes as in Fig. 1.',
}
TABLE_CAPTIONS = {
    '1': 'Table 1. Datasets, periods and roles. All gridded products were resampled to a common 0.009° (about 1 km) grid.',
    '2': 'Table 2. Station trends for 1995–2024 (°C decade⁻¹, Theil–Sen) and comparison with regional products at the same locations. Intervals are 95% moving-block bootstrap intervals. ΔBF5km is the built-up fraction added within 5 km between 1995 and 2020; NEX rank is the percentage of the 28 NEX-GDDP-CMIP6 models with a smaller Tmin trend; the last two columns give the most likely change point in the detrended station-minus-ERA5-Land series with its Pettitt p value, and the missing warming recomputed after removing a shift at that year; only Dubai reaches significance.',
    '3': 'Table 3. Urbanising minus coast-matched rural trends for 1995–2024 (°C decade⁻¹). Rural land follows the UN Degree of Urbanisation. Intervals are 95% spatial block-bootstrap intervals over 0.25° blocks.',
    '4': 'Table 4. Regression estimates of the change in trend per 10 percentage points of added built-up fraction (°C decade⁻¹) and sensitivity analyses. Intervals are 95% confidence intervals with standard errors clustered by 0.25° block, except in the last row, where the NEX-GDDP-CMIP6 entry gives the 5–95% range across models.',
    '5': "Table 5. Additional night-time surface warming between 2020 and 2050 implied by continued built-up growth within 5 km of each station. The primary scenarios continue each cell's observed 2010–2020 growth rate (S-high) and half that rate (S-low) for thirty years, capped at the 99th percentile of observed plan-area fraction. Intervals are 95% confidence intervals from the dose–response coefficient alone; the full uncertainty, which is dominated by the surface-to-air conversion, is given in Fig. 7b and Table S5. The two alternative growth baselines are reported for comparison.",
    'S1': 'Table S1. Warm-night indices, 1995–2024. TN90p follows the ETCCDI definition with a 1991–2020 base period and is given in percentage points of nights per decade; TR (Tmin ≥ 20 °C) and TN30 (Tmin ≥ 30 °C) are in nights per decade. Each dataset uses its own base-period percentiles.',
    'S2': 'Table S2. NEX-GDDP-CMIP6 UAE-area Tmin change (°C) relative to 1995–2014 for the IPCC AR6 periods, and the observed 1995–2024 station Tmin rise for comparison.',
    'S3': 'Table S3. Night-time and day-time warming by Local Climate Zone. Classes follow Stewart and Oke (2012) as mapped by Demuzere et al. (2022); each 1 km cell takes the built LCZ class occupying most of its built 100 m sub-cells, and a class is reported when built classes cover at least 20% of the cell and at least 40 cells fall in the class. Trends are differences from coast-matched rural land with 95% spatial block-bootstrap intervals. ΔBF is the mean built-up fraction added 1995–2020 and H the mean building height in 2018. The five classes omitted (compact high-rise, compact mid-rise, open mid-rise, open high-rise and lightweight low-rise) occupy 13 km² in total and yield at most two cells each.',
    'S4': 'Table S4. Urban form. Regression estimates of the night-time LST response to added built-up fraction with mean building height (H) entered as a main effect and as an interaction, with day-time LST and ERA5-Land Tmin for comparison; coefficients are °C decade⁻¹ per 10 pp of added built-up fraction, per 10 m of H, and per 10 pp per 10 m for the interaction, with 95% cluster-robust intervals.',
    'S5': 'Table S5. Decomposition of the uncertainty in the projected urban increment. The projected additional night-time air warming is the product of the built-up increment, the accumulated surface response and the surface-to-air conversion, so the relative uncertainties combine multiplicatively; the growth-scenario term treats S-low and S-high as the bounds of a uniform range.',
}
