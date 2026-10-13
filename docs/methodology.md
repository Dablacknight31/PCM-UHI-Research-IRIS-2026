# Implemented methodology

This describes the equations and parameters actually retained in [research_model.py](../src/research_model.py), not proposed extensions. Parameters are also recorded in [Category 1 configuration](../results/category1/category1_config.json) and [accepted atmospheric configuration](../configs/accepted_baseline.json). All signs are PCM minus matched latent-free control unless specified.

## Three spatial scales

| Scale | Representation | Interpretation |
|---|---|---|
| Material and roof | 1 m², 20 mm homogeneous slab; ten 2 mm cells | Surface temperature, cell enthalpy/phase and roof sensible flux |
| Treated hotspot | 44 shared-edge 150 m cells; 990,000 m² land | Roof footprint union ≈491,600.71 m²; assumed treated area ≈344,120.50 m² |
| Atmospheric domain | 93×88 cells of 150 m; 6 km outer buffer; 184.14 km² | Vertically averaged 40 m layer anomaly; hotspot, 2 km buffer and roof-weighted receptors |

GHSL built-weighted hotspot area (510,439.43 m²) is distinct from eligible roof footprint area. The large computational domain is not proof of citywide intervention or cooling.

## Sources, grid and climate processing

FAO GAUL 2015 level1 selects Delhi. Landsat 8/9 Collection 2 Level 2 scenes use [2025-04-01,2025-06-01) and [2025-10-01,2025-12-01), scene cloud cover below 30%, QA_PIXEL bits 0–5 rejected and QA_RADSAT=0. `mask_and_scale_landsat`, `retrieve_landsat_season` and `download_common_band` scale reflectance as DN×0.0000275−0.2 and temperature as DN×0.00341802+149−273.15 °C. NDVI=(B5−B4)/(B5+B4) and NDBI=(B6−B5)/(B6+B5), with validity checks. Overlap aggregation and seasonal medians yield aligned 150 m EPSG:32643 layers. GHSL 2020 built surface divided by native cell area gives a built fraction, aggregated to the common grid. NDVI/NDBI contextual correlations do not enter ranking.

One native ERA5-Land cell supplies regional temperature, 10 m wind and downward radiation. Instantaneous quantities are interpolated to canonical IST interval midpoints. Radiation increments are overlap-rebinned to hourly IST intervals and divided by duration; raw values and correction ledgers remain. Existing QC sets shortwave increments in [−5,0) J/m² to zero and fails on larger negatives. There are 8,760 intervals from local 2025-01-01 00:00 to 2026-01-01 00:00. This is not 150 m observed weather.

See [data availability](../DATA_AVAILABILITY.md) for licensing and the held GAUL-derived layers.

## Four-neighbour hotspot selection

`select_persistent_hotspot` defines jointly valid seasonal LST cells inside Delhi, computes each seasonal population mean and SD (`ddof=0`), and requires:

```text
LST_pre > mean_pre + SD_pre
LST_post > mean_post + SD_post
built_fraction >= Delhi valid-built 75th percentile
```

Saved thresholds are 43.306061913891284 °C, 31.89891006286183 °C and 0.36474066972732544. Connected-component traversal uses only `(r−1,c),(r+1,c),(r,c−1),(r,c+1)`: shared edges count; diagonals do not. Components with fewer than five cells are rejected. Rank descending built-weighted area, descending mean premonsoon excess, descending cell count, then ascending component ID. Among 126 candidate regions and 22 survivors, component 28 has 44 cells and 0.990 km². The selection establishes a persistent surface hotspot, not an optimum intervention site. [Hotspot summary](../manifests/preliminary/hotspot_summary.json) and [region audit](../results/preliminary/hotspot_region_audit.csv) preserve qualification/ranking evidence.

## Material screening

`load_section0_pcm` and `partition_pcm_tables` establish 77 entries and 32 model-ready rows. `derive_local_day_roof_screen_air` uses 61 complete April–May daily air maxima; their rounded mean is 37.8 °C. The rounded Delhi premonsoon 95th-percentile LST is 46.1 °C. `screen_workbook_roof` retains inclusive overlaps:

```text
Tm_high >= 37.8 °C AND Tm_low <= 46.1 °C
```

PCM-011, PCM-067 and PCM-069 pass. Endpoint contact counts. This mixed air/surface interval is a heuristic, not a measured roof operating interval, validated performance ranking or exhaustive material optimisation. [Screen table](../results/postprocessing/baseline_graphs/candidate_screen_audit.csv) and [derivation](../manifests/preliminary/pcm_screen_derivation.json) are saved. Source-sheet conflicts are detailed in [material inputs](material_input_conflicts.md).

## Category 1 surface balance and enthalpy

`c1_surface_energy_balance` implements inward-positive top flux:

```text
q_top = α G + h_c (T_air − T_s) + ε [LW_down − σ (T_s+273.15)^4]
h_c = 5.7 + 3.8 V10
α=0.6; ε=0.9; σ=5.670374419e−8 W m−2 K−4
```

`c1_surface` jointly solves this environment balance and top half-cell conduction `q_top=(2 k_0/Δz)(T_s−T_0)`. The bottom is adiabatic. Initial temperature is uniform 26 °C; reference temperature is 0 °C. Area is 1 m², thickness 0.02 m, and Δz=0.002 m.

`c1_h_from_temperature` uses **specific enthalpy** h in J/kg. Let Tl, Tu be the assigned melting bounds, w=Tu−Tl, z=T−Tl and hl=cp_s(Tl−Tref). For w>0:

```text
T <= Tl:       h = cp_s (T−Tref)
Tl < T < Tu:   h = hl + cp_s z + (cp_l−cp_s) z²/(2w) + L z/w
T >= Tu:       h = hl + (cp_s+cp_l)w/2 + L + cp_l(T−Tu)
```

In the transition, f=z/w; below/above it f=0/1. `c1_state_from_h_scalar` inverts this relation and returns dT/dh. Volumetric enthalpy is ρh. For zero width, temperature remains at the transition point over the latent plateau and f follows enthalpy; the zero-latent/zero-width branch and coexistence handling remain in the solver. Freezing hysteresis and supercooling are not imposed from the source sheet. Conductivity is `k=ks(1−f)+kl f`; interior face conductance is `2ki kj/[(ki+kj)Δz]`.

`c1_residual` implements backward-Euler cell balance:

```text
ρ Δz (h_i,new−h_i,old)/Δt = q_in,i − q_out,i
```

For an interior face, downward heat flux is harmonic conductance times `(T_i−T_i+1)`. The top cell receives q_top; the last cell has no lower-face flux. `c1_implicit_step` uses a tridiagonal Newton solve, line search and retained phase-jump corrector; `c1_zero_latent_coexistence_step` preserves the repaired control branch. Nominal timestep is 60 s with retry minimum 0.9375 s, maximum 40 nonlinear iterations, residual tolerance `1e−7 + 1e−9×scale` W/m². Energy tolerances and validation gates are preserved in configuration; no tolerance was weakened during packaging.

Each material's control changes L alone to zero. Category 1 outputs include paired 8,760-row hourly temperatures/fluxes, liquid fractions, daily/monthly/annual/reset/saturation summaries, and six 8,761×10 depth-state arrays. The preceding endpoint is retained for continuity. Latent charging and release are accounting metrics, not permanent annual heat removal.

## Roof-to-atmosphere forcing and deployment

Category 1 convection is positive air→slab. `c1_delta_h` converts interval-average convection to roof→air forcing:

```text
H_PCM = −q_convection,PCM
H_L0  = −q_convection,L0
ΔH    = H_PCM−H_L0
```

Do not replace these saved flux averages with separately averaged h_c and ΔT. `c3_validate_handoff` checks chronology, complete real annual status, candidates and input/code identities. Google Open Buildings v3 footprints with confidence≥0.75 are projected, clipped to the hotspot and unioned to remove overlap. `c3_layout`/`c3_domain` allocate the full assumed usable share η=0.7 in the accepted baseline (`coverage=1`). F(x,y) is treated roof area divided by grid-cell plan area; η is usability, not a thermal efficiency. Static 2023 inferred footprints represent a 2025 proxy, without a roof eligibility survey.

## Category 3 atmospheric equation and solver

θ=T_air,PCM−T_air,L0 is a vertically averaged layer anomaly:

```text
∂θ/∂t = −u ∂θ/∂x −v ∂θ/∂y + Kh ∇²θ −θ/τ + S
S(x,y,t) = F(x,y) ΔH(t)/(ρair cpair H)
ρair=1.2 kg/m³; cpair=1005 J/(kg K); H=40 m
ρair cpair H=48,240 J/(m² K)
Kh=20 m²/s; τ=1800 s; wind scale rU=0.6
```

Projected ERA5 wind is scaled and spatially uniform per hour. Forcing is piecewise constant per canonical hour. Initial θ is zero without spinup. Accepted open boundaries have zero incoming advective anomaly, outgoing upwind anomaly and no lateral diffusive flux. An alternative zero-anomaly diffusive boundary exists for numerical comparison; the saved accepted baseline uses open boundaries.

`c3_transport` uses conservative MUSCL/minmod finite volumes for advection plus horizontal diffusion. `c3_step` applies SSPRK2 transport between exact Strang source/relaxation half steps. Each half step is `θ←a θ+b S`, where `a=exp(−Δt/(2τ))`, `b=τ[1−exp(−Δt/(2τ))]`; SSPRK2 is `θ1=θ0+Δt L(θ0)`, `θ2=0.5θ0+0.5[θ1+Δt L(θ1)]`. The limiting no-exchange branch is retained. `c3_stable_dt` uses:

```text
rate = 2(|u|+|v|)/Δx + 4Kh/Δx²       [open boundary]
Δt = min(120 s, 0.45/rate)
```

The alternative diffusive boundary uses 6Kh/Δx². Steps are divided to fit hour/solar-daylight segments exactly. Accepted geometry is Δx=150 m, 93×88 cells, bounds [684600,3167850,697800,3181800] m. Chunk size is 168 h, with a final 24 h chunk. Numerical acceptance/refinement tables are included; numerical consistency is distinct from empirical validation. This model has no resolved buildings, vertical airflow or fully coupled roof feedback.

## Anomalies, aggregation and maxima

`c3_chunk` integrates area-weighted signed θ and separate positive parts by trapezoidal substep endpoints:

```text
hourly receptor mean = Σcells,steps [0.5(θold+θnew) w Δt]/(Σw ×3600)
gross cooling = Σ max(−θ,0) w Δt       [endpoint trapezoids]
gross warming = Σ max( θ,0) w Δt       [endpoint trapezoids]
```

Receptors are hotspot, hotspot-plus-2-km buffer and treated-roof weights. Gross integrals are K m² s, not energy; cancellation must not erase the separate components. Effect-area indicators use strict θ<−0.001/θ>+0.001 K; sign-based hourly counts and cell maxima have different definitions. Solar segments define day/night. The weather-only mask `Tair >= annual 95th percentile` selects 438 hottest intervals independently of outcomes.

`c3_hourly_table` and `c3_summarize` aggregate the saved intervals. **Maximum hourly hotspot cooling** is `max(0,−min(hotspot_mean_K))`. **Instantaneous cell cooling** is tracked at accepted substep endpoints and independently agrees with `max(0,−min(peak_cool_K))`. `peak_cool_K`/`peak_warm_K` are entire synchronous event fields at global extrema, not per-cell envelopes. Exact event substep times and an hourly spatial cube were not saved. [saved_metrics.py](../src/postprocessing/saved_metrics.py) retains both protected calculations.

## Exploratory and deployment reporting

Category 4 active mass is ρd (20.14, 17.00, 24.20 kg/m² for the executed inputs); encapsulation and assembly masses are missing and `CATEGORY4_READY=false`. The PDF describes indicative heat diversion and one-way indoor transfer, but exact generators/scenario exports are absent. They are not additional validated models in this documentation and have not been reconstructed.
