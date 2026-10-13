# Model assumptions and parameter evidence

These assumptions describe the executed inputs and retained code. They are not measured deployment parameters. See [methodology](methodology.md) for equations and [material conflicts](material_input_conflicts.md) for source discrepancies.

| Component | Implemented assumption | Consequence |
|---|---|---|
| Climate | One 2025 ERA5-Land native cell; canonical IST intervals | Regional forcing without observed 150 m weather or multi-year robustness |
| Geospatial | Two seasonal LST composites; 150 m common UTM grid | Selection reflects sampled surface heat, not continuously measured air heat |
| Connectivity | Four shared-edge neighbours; minimum five cells | Diagonal-only contact remains disconnected |
| Screening | Inclusive overlap with 37.8–46.1 °C heuristic | Not an optimum or validated performance score |
| PCM phase | Reversible equilibrium enthalpy; assigned property sets | No hysteresis/supercooling, ageing, moisture or experimentally verified formulation |
| Roof | 1 m², 20 mm exposed homogeneous slab, ten cells, insulated base | No multilayer roof, room coupling, packaging resistance or water transport |
| Surface | α=0.6, ε=0.9, h=5.7+3.8V10, initial 26 °C | Same prescribed optics and initial state for matched comparisons |
| Control | Same material/geometry with latent heat zero | Not conventional concrete or validated cool roof |
| Footprints | Open Buildings May 2023 inference; confidence≥0.75; unioned | Geometry proxy, not 2025 measured usable rooftops |
| Deployment | 70% usable fraction, coverage=100% of that fraction | Treated ≈34.76% of hotspot land, not 100% land coverage |
| Atmosphere | 40 m effective layer, ρ=1.2, cp=1005, Kh=20, τ=1800, rU=0.6 | Vertically averaged response under prescribed transport; no CFD |
| Domain | 93×88×150 m grid; 6 km outer buffer; open boundaries | Hotspot and surroundings, not citywide demonstration |
| Coupling | ΔH roof forcing to air only | Atmospheric anomaly does not update roof/PCM phase |
| Initial air | Zero anomaly, no spinup | Relative response starts from identical control state |
| Reporting | Trapezoidal substep area/time means and independent extrema | Mean profiles, hottest-subset means and instantaneous maxima are distinct |
| Feasibility | Active material mass only | Total assembly mass/structural, fire and durability suitability remain unknown |

The retained convergence tests assess numerical behaviour under these assumptions. They do not estimate total uncertainty or establish that the assumed effective mixing layer describes Delhi's real pedestrian-level atmosphere. Surface cooling is not equal to air cooling because the latter depends on flux, treated area, air-column heat capacity and transport/exchange.
