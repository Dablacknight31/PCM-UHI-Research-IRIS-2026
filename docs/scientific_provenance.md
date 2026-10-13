# Scientific provenance and checksum policy

Dataset origins, collection identifiers and epochs, units, equations, model parameters, input-content seals, numerical acceptance status and saved run identities describe the scientific computations. Current input and output locations are repository-relative. Dependencies without included files are explicitly identified as retained privately or unavailable; no substitute location or result is invented.

Metadata fields describing original computer locations, account configuration and source-file organization are unnecessary to interpret the science and are omitted. The public metadata is a projection of the source records, not an exact serialization of every original identity preimage. Recorded experiment IDs, pair IDs, input identities, forcing/layout/grid hashes and result-content seals are preserved as scientific identifiers. They must not be recalculated from projected metadata and presented as the original run identities.

`manifests/repository_file_manifest.csv` seals every current public file except the manifest itself and its detached `repository_file_manifest.sha256` seal. The detached seal covers the manifest. These checksums describe the current distributed bytes. Recorded scientific-content fingerprints describe their documented original computational scope and are distinct from public-file checksums.

[Dependency provenance](../manifests/dependency_provenance.json) links retained private checkpoint hashes to experiment IDs and hour intervals where saved derived tables need that source relationship. It lists scientific dependencies, without their computer paths. File entries in run manifests refer only to available public scientific files. Missing spatial cubes, exact substep times, original generators and exploratory exports remain missing.

Public source-identity metadata uses generic computational labels and actual environment configuration. Its access changes do not alter scientific equations, physical parameters or saved numerical values. Fresh computations create new identities and must not overwrite or relabel saved baselines.
