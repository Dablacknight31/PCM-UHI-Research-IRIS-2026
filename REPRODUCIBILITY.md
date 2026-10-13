# Reproducibility and saved-result inspection

## Supported verification

The public package provides scientific code, permitted inputs, saved numerical outputs and original figures. File integrity and the saved relationships below are verifiable. A full independent rerun of the annual simulation pipeline is **not established**, and exact regeneration of all manuscript figures is **not established**.

Use Python 3.12 and NumPy from the repository root:

```bash
python src/validation/verify_publication.py --saved
```

The verifier checks required files, source checksum, Python syntax, relative documentation links, file-manifest membership, privacy patterns, and file sizes. The saved-data checks cover 77 screening entries, 32 model-ready entries, three selected materials, paired 8,760-hour chronology, latent-only controls, sensible-forcing signs, 8,761×10 roof states, 93×88 atmospheric fields, 438 weather-defined extreme hours, saved convergence flags, selected geometry, and independent hourly/cell cooling maxima. It does not import the main model, acquire remote data, run a solver, or generate figures.

To save a receipt outside the tracked scientific files:

```bash
python src/validation/verify_publication.py --saved --output runtime/publication_check.json
```

## Scientific environment

The recorded scientific environment is Python 3.12.14 on arm64. [requirements.txt](requirements.txt) records scientific dependencies and [requirements.lock.txt](requirements.lock.txt) records installed versions. Installing every pinned dependency on a new platform has not been verified. Saved inspection in another NumPy environment is not a simulation-equivalence certificate.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Fresh execution and inputs

Read [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md), [input locations](configs/input_locations.json), [methodology](docs/methodology.md), and [workflow](docs/research_workflow.md). The exact compiled PCM workbook and GAUL-conditioned inputs are not distributed. Do not substitute a different workbook or boundary and label the result as the saved baseline.

`PCM_UHI_EE_PROJECT` must identify your own authorized Earth Engine project; no project identifier or credentials are bundled. `PCM_UHI_OUTPUT_ROOT` selects a new output directory. The main model uses repository-relative input defaults. Its optional private input-validation routines require actual dependencies configured through `PCM_UHI_PRIVATE_ROOF_SOURCE`, `PCM_UHI_PRIVATE_PRELIM_SOURCE`, and `PCM_UHI_PRIVATE_COMPLETION_RECEIPT`; those dependencies are not included in this package. When an authorized private package uses other field labels, `PCM_UHI_PRIVATE_METADATA_FIELDS` supplies a JSON mapping for the scientific roles `source_content`, `pair_source`, `upstream_identity`, `source_identity` and `experiment_source`. Public metadata uses the documented current schema; no private field labels are bundled.

The intended fresh-run order, after restoring exact authorized inputs, is:

```python
import sys
sys.path.insert(0, "src")
import research_model as model
model.run_preliminary()
model.run_rooftop()
model.run_atmospheric_baselines()
```

This is a deliberate expensive workflow, not a tested complete annual reproduction recipe. Newly executed runs have their own source and input identities. Public metadata is a scientific projection of the original records; original run identities remain identifiers of saved computations and are not recomputed from the projected metadata. [The provenance policy](docs/scientific_provenance.md) separates original scientific seals from current public file checksums.

## Available and unavailable evidence

All three annual roof/control result sets and accepted atmospheric hourly/compact spatial outputs are included. Exact peak substep timestamps and a full hourly atmospheric spatial cube are absent. The wider uncertainty/feedback ensemble and deployment assessment are incomplete. Seven figure generators are unavailable, and the exploratory heat-diversion/indoor numerical exports are absent. See [PAPER_FIGURE_INDEX.md](PAPER_FIGURE_INDEX.md).

The saved plot adapter may write selected source-backed plots to a new output directory. It does not recreate every included figure, and no figure regeneration is needed for inspection.
