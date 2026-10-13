# A Roof-to-Neighbourhood Modelled Assessment of Phase-Change Materials to Mitigate Urban Heat Island Effects: A Case Study of Delhi

**Kanav Rakheja · Delhi, India · Research prepared for IRIS National Fair 2026**

## Overview

Urban surfaces store and release heat, changing the timing and intensity of urban warming. Rooftop phase change materials (PCMs) absorb latent heat while melting and release it during solidification. This computational study asks how that thermal storage changes roof temperatures and, through sensible heat exchange, the surrounding atmospheric response. Delhi provides a case study with strong premonsoon heat, dense development and seasonal variation. Linking roof fluxes to a neighbourhood model matters because cooler roof surfaces do not automatically yield equal air-temperature reductions.

The study uses **Delhi's 2025 meteorological conditions** and one selected **44-cell, 0.990 km² hotspot**. A vertically averaged 2D advection–diffusion model represents a surrounding 184.14 km² computational domain. It is a simplified anomaly model, not full CFD. No citywide cooling, empirical validation, or conventional/cool-roof comparison is demonstrated.

## Research objectives

1. Characterise seasonal surface-temperature and land-cover patterns and select a persistent, built-up hotspot with shared-edge connectivity.
2. Screen model-ready PCM property sets and quantify annual melting, saturation, regeneration and rooftop heat exchange.
3. Couple PCM-minus-control sensible heat flux to an atmospheric model under explicit rooftop-coverage assumptions.
4. Compare diurnal, extreme-heat, spatial and annual responses, including compensating warming and deployment evidence gaps.

## Methodology

1. **Climate and geospatial characterisation:** Landsat 8/9 seasonal LST, NDVI and NDBI; GHSL built fraction; ERA5-Land weather; FAO GAUL study boundary.
2. **Hotspot selection:** elevated LST in both seasons and high built fraction; four-neighbour connected components; minimum five cells; deterministic region ranking. Diagonal contact alone does not connect cells.
3. **PCM screening:** 77 compiled entries, 32 model-ready, three inclusive overlaps with the heuristic 37.8–46.1 °C air/LST interval: PCM-011 lauric acid, PCM-067 OM42, PCM-069 PEG1000.
4. **Category 1 rooftop model:** 20 mm exposed slab, ten enthalpy finite-volume cells, environmental top balance, insulated base, continuous annual simulation and an otherwise matched L=0 control for each material.
5. **Category 3 atmospheric model:** signed interval-average sensible flux differences, Open Buildings roof-area proxy, 70% usable-area assumption, prescribed 40 m air layer, advection, horizontal diffusion and vertical relaxation.
6. **Interpretation:** distinct surface/air scales, signed means, positive gross cooling/warming and cell extrema. Category 4 reports active mass and incomplete feasibility. Heat-removal and indoor illustrations remain exploratory with missing exact generators/exports.

Read the implemented equations in [methodology](docs/methodology.md), [workflow](docs/research_workflow.md), [assumptions](docs/model_assumptions.md) and [limitations](docs/limitations.md).

## Repository structure

```text
README.md                         study and navigation
REPRODUCIBILITY.md                evidence levels and commands
DATA_AVAILABILITY.md              datasets, access and rights
PAPER_FIGURE_INDEX.md              latest PDF numbering and provenance
src/research_model.py              cleaned main model, retained numerics
src/postprocessing/               protected saved-result calculations
src/visualization/                 original plot adapter for saved baselines
src/validation/                    package and saved-result verification
configs/                          input locations and accepted baseline
 data/inputs/materials/            factual screening records; workbook excluded
 data/inputs/weather/              raw and processed 2025 forcing
 data/inputs/geospatial/           selected hotspot mask
 data/inputs/roof_coverage/         footprints and eligible roof fractions
results/preliminary/              screening, hotspot and contextual tables
results/category1/pcm_001..003/    three PCM/control annual pairs and states
results/category3/accepted_baselines/<experiment-id>/
                                  hourly statistics and compact spatial fields
results/category4/                partial mass/feasibility reporting
results/postprocessing/           saved derived comparison tables
results/validation/               evidence receipts, never new simulations
figures/                          original PNGs in manuscript-related folders
manifests/                        identities, provenance, checksums, exclusions
docs/                             methods, limitations and consistency review
```

`pcm_001=PCM-011`, `pcm_002=PCM-067`, `pcm_003=PCM-069`. See [release scope](docs/public_release_scope.md) for included scientific evidence and unavailable dependencies.

## Key findings from saved outputs

Temperature differences are **PCM minus its matched L=0 control**; negative values mean cooling. The controls preserve other material/geometry parameters and remove latent heat only. They are not validated concrete or commercial cool roofs.

| Metric (°C unless specified) | Lauric acid | OM42 | PEG1000 |
|---|---:|---:|---:|
| Peak roof cooling in annual mean diurnal profile | 2.273 | 3.007 | 3.921 |
| Peak roof warming in that profile | 1.750 | 2.389 | 2.747 |
| Peak hotspot air cooling in annual mean diurnal profile | 0.06175 | 0.08022 | 0.10238 |
| Mean hotspot cooling over 438 hottest-weather hours | 0.09101 | 0.09507 | 0.11926 |
| Maximum hourly hotspot cooling | 0.456324687826 | 0.500685497998 | 0.502713612937 |
| Maximum instantaneous grid-cell cooling | 0.697010701462 | 0.796938813589 | 0.819003907026 |
| Signed annual mean hotspot air anomaly | −0.00021441 | +0.00010540 | +0.00181595 |
| Signed annual mean roof-to-air flux difference (W/m²) | +0.45969 | +0.54086 | +0.58775 |

The diurnal values are extrema of profiles averaged across the year, not annual mean temperature reductions. The hottest-weather subset mean is not a maximum. Hourly hotspot maxima are area/time averages; instantaneous maxima track individual cells at solver substeps. Exact within-hour peak times are absent. All three annual sensible-flux differences are positive, and cooling is accompanied by warming. Near-zero signed air means do not imply that gross cooling and warming are absent or that total urban energy has been removed.

Sources: [Category 1 annual summary](results/category1/annual_summary.csv), the paired hourly tables, and [accepted atmospheric baselines](results/category3/accepted_baselines). [Verified findings](results/validation/verified_findings.json) records the derivation and rounding.

## Figures

**Start with the [paper figure index](PAPER_FIGURE_INDEX.md).** The index follows Figures 1–7, including Figure 4(a/b), and links the 34 included original PNGs. Four GAUL-dependent city maps are excluded. Seven figures lack exact generators; two exploratory figures also lack numerical exports. Full regeneration of every figure is not established.

## Reproducibility

[REPRODUCIBILITY.md](REPRODUCIBILITY.md) describes the verified saved-data checks and the limits of fresh execution. **The full annual pipeline has not been independently rerun from the public code.**

From the repository root, use Python 3.12 with NumPy:

```bash
python src/validation/verify_publication.py --saved
```

This command checks available files and saved numerical relationships without running a solver. [requirements.txt](requirements.txt) records scientific dependency versions; [requirements.lock.txt](requirements.lock.txt) records the arm64 environment and is not a universal installation guarantee. Fresh execution needs permission-cleared inputs and your own `PCM_UHI_EE_PROJECT` configuration.

## Data availability and reuse

[DATA_AVAILABILITY.md](DATA_AVAILABILITY.md) gives precise inclusion status, official acquisition links and redistribution review. Publicly included weather and roof data carry [third-party attribution](THIRD_PARTY_NOTICES.md). The intact compiled PCM workbook, source-evidence workbook, GAUL boundary and affected geospatial copies/maps are held outside the public candidate. Access restrictions and missing dependencies are documented explicitly.

No project-wide open-source license has been selected. Public visibility is not a general permission to reuse or redistribute the project's code/figures. Third-party licenses remain applicable to their own data; they do not license the author's entire repository.

## Limitations

One weather year, three shortlisted property sets with source conflicts, an idealised insulated slab, prescribed transport/mixing, no building-scale CFD or field validation, no completed uncertainty/deployment ensemble, and missing exploratory provenance limit the conclusions. Roof surface temperature is not pedestrian air temperature or indoor comfort. See [limitations](docs/limitations.md) and [material-input conflicts](docs/material_input_conflicts.md).

## Citation

Suggested bibliographic form using verified information:

> Rakheja, K. (2026). *A Roof-to-Neighbourhood Modelled Assessment of Phase-Change Materials to Mitigate Urban Heat Island Effects: A Case Study of Delhi*. Computational research repository prepared for IRIS National Fair 2026.

After publication, append the actual repository URL and commit/tag used. No DOI, journal, accepted publication or peer-review status is claimed. Cite the original data providers separately using [third-party notices](THIRD_PARTY_NOTICES.md). Do not use a placeholder URL as if it were published.

## Research status

Research prepared for IRIS 2026. Saved annual numerical results and preservation checks are available; independent experimental validation is absent. A final manuscript is not included. The repository provides scientific methods and saved evidence with the qualifications described in [limitations](docs/limitations.md).
