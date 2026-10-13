# Third-party data attribution

Official terms reviewed on 13 October 2026. These apply to the identified data, not to the entire code repository. No project-wide license has been chosen.

## ERA5-Land / Copernicus / ECMWF

2025 raw forcing was extracted from the Earth Engine ERA5-Land hourly collection; processed weather rebins time intervals and applies the documented shortwave QC. Weather and climate-driven research outputs contain modified Copernicus Climate Change Service information (2025). Neither the European Commission nor ECMWF is responsible for subsequent use of that information.

Dataset: Muñoz-Sabater, J. (2019), *ERA5-Land hourly data from 1950 to present*, Copernicus Climate Change Service Climate Data Store, [doi:10.24381/cds.e2161bac](https://doi.org/10.24381/cds.e2161bac). Reference: Muñoz-Sabater et al. (2021), *ERA5-Land: a state-of-the-art global reanalysis dataset for land applications*, [doi:10.5194/essd-13-4349-2021](https://doi.org/10.5194/essd-13-4349-2021).

The [Earth Engine catalogue](https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_HOURLY) links to the [Copernicus licence](https://apps.ecmwf.int/datasets/licences/copernicus/), permitting distribution/adaptation with attribution and responsibility notice. The [current CDS entry](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=overview) displays a CC-BY licence. Both provider attribution requirements and applicable original acquisition terms should accompany reuse.

## Google Research Open Buildings v3

Source: Google Research, *Open Buildings v3* (May 2023 inference). Local modifications: confidence≥0.75 filter, projection, hotspot clipping, footprint union and roof-fraction rasterisation with assumed η=0.7. Google Research does not endorse these calculations or certify rooftop suitability.

The saved acquisition record identifies [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This is confirmed in the [Earth Engine v3 catalogue](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_Research_open-buildings_v3_polygons). The [provider FAQ](https://sites.research.google/gr/open-buildings/) offers CC BY 4.0 and ODbL alternatives. These repository assets retain their recorded CC BY 4.0 provenance; this does not select a license for the author's code. Reference: Sirko et al. (2021), *Continental-scale building detection from high resolution satellite imagery*, [arXiv:2107.12283](https://arxiv.org/abs/2107.12283).

## Landsat 8/9

Source: U.S. Geological Survey, Earth Resources Observation and Science Center (2020), *Landsat 8–9 OLI/TIRS Level-2, Collection 2*, [doi:10.5066/P9OGBGM6](https://doi.org/10.5066/P9OGBGM6). Modifications include quality masking, radiometric scaling, seasonal medians, index calculation and 150 m aggregation. [USGS redistribution policy](https://www.usgs.gov/faqs/are-there-any-restrictions-use-or-redistribution-landsat-data) permits redistribution and requests source credit. Direct provider permission does not clear GAUL boundary material embedded in a derivative; those copies/maps are held.

## GHSL

Source: European Commission Joint Research Centre; © European Union. Dataset: Pesaresi and Politis (2023), *GHS-BUILT-S R2023A*, [doi:10.2905/9F06F36F-4B11-47EC-ABB0-4F8B7B1D72EA](https://doi.org/10.2905/9F06F36F-4B11-47EC-ABB0-4F8B7B1D72EA). Method reference: Pesaresi et al. (2024), *Advances on the Global Human Settlement Layer by joint assessment of Earth Observation and population survey data*, [doi:10.1080/17538947.2024.2390454](https://doi.org/10.1080/17538947.2024.2390454).

Changes: 2020 epoch built surface converted to fraction and aggregated to the study grid. [Official GHSL conditions](https://human-settlement.emergency.copernicus.eu/GHSLhowToCite.php) specify CC BY 4.0, credit, change indication and no endorsement, with dataset and methodology references. The public candidate holds the boundary-conditioned raster/map copies because GAUL is also involved; source licensing for GHSL itself is established.

## Held sources

FAO GAUL 2015 has non-commercial, sublicensing, attribution and redistribution conditions in the [official catalogue-hosted licence](https://developers.google.com/earth-engine/datasets/catalog/DataLicenseGAUL2015.pdf). Unrestricted public redistribution of the specific boundary/derivative copies has not been established. The candidate omits them. Citation alone does not resolve that issue.

The intact PCM/source-evidence workbooks compile multiple scholarly/manufacturer sources whose complete redistribution permissions have not been verified. Original provider URLs remain in saved run metadata and [material conflicts](docs/material_input_conflicts.md); no third-party full-text article or datasheet facsimile is included. Author-generated numerical outputs and factual executed-parameter records remain separate from the held compilations. See [data availability](DATA_AVAILABILITY.md).
