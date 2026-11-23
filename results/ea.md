# Juxtaposed Expand–Accumulate (1D Explicit EA)

Single-polynomial 1D encoding benchmarks for `ea` (Zoo #7; status summary: OK: 18, OOM_SKIPPED: 18).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`taskset -c 0-31`, `RAYON_NUM_THREADS=32`, `OMP_NUM_THREADS=32`); release build (`target-cpu=native`)
- **Repositories / Revisions**: `EACode CRYPTO’24 artifact`, `ERA local source snapshot`
- **Field(s)**: `goldilocks`, `ristretto255`, `secp256k1`
- **Message Lengths**: `K = 2^k` (`k ∈ {20, 22, 24, 26, 28, 30}`)
- **1D Geometry**: Single codeword (`nrows = 1`, `width = 1`, `log_batch_size = 0`; no interleaving, no 2D matrix reshape)

## Measurement Methodology

- **Sampling**: 1 warmup + 3 serial measured runs; reports arithmetic mean and median.
- **Timing Scope**: Measures the native 1D encoder call (`input_elements` -> `codeword_elements`) only; excludes setup (`setup_ms`), input generation, caller-buffer reset (for in-place entry points), correctness checks, and Merkle hashing/opening. Before timing, the driver pre-touches or reuses caller-owned buffers; output and temporary scratch buffers allocated internally by the encoder during the timed interval can still trigger page faults, and those times are included in the recorded measurements (per-row minor/major fault counts are logged in `results/ea.csv` `notes`).
- **Memory**. `Peak RSS` is whole-process peak resident memory (`GiB`), including setup.

## Results

| Variant | Field | Nominal Rate | Actual Rate | k | T | Setup (ms) | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `ea-explicit` | `secp256k1` | `1/2` | 0.5000 | 20 | 32 | 91465.74 | 1495.390 | 1496.377 | 17.803 | `OK` |
| `ea-explicit` | `secp256k1` | `1/2` | 0.5000 | 22 | 32 | 400089.05 | 8929.561 | 8930.290 | 77.984 | `OK` |
| `ea-explicit` | `secp256k1` | `1/2` | 0.5000 | 24 | 32 | 1778429.36 | 42983.968 | 43007.513 | 338.971 | `OK` |
| `ea-explicit` | `secp256k1` | `1/2` | — | 26 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `ea-explicit` | `secp256k1` | `1/2` | — | 28 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `ea-explicit` | `secp256k1` | `1/2` | — | 30 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `ea-explicit` | `secp256k1` | `1/4` | 0.2500 | 20 | 32 | 96443.25 | 1581.250 | 1583.514 | 18.715 | `OK` |
| `ea-explicit` | `secp256k1` | `1/4` | 0.2500 | 22 | 32 | 417626.77 | 9396.916 | 9410.259 | 81.611 | `OK` |
| `ea-explicit` | `secp256k1` | `1/4` | 0.2500 | 24 | 32 | 1838103.54 | 43662.596 | 43683.954 | 353.469 | `OK` |
| `ea-explicit` | `secp256k1` | `1/4` | — | 26 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `ea-explicit` | `secp256k1` | `1/4` | — | 28 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `ea-explicit` | `secp256k1` | `1/4` | — | 30 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `eacode-official` | `ristretto255` | `1/2` | 0.5000 | 20 | 32 | 55101.22 | 1383.340 | 1383.104 | 17.809 | `OK` |
| `eacode-official` | `ristretto255` | `1/2` | 0.5000 | 22 | 32 | 237966.96 | 8602.754 | 8616.211 | 77.994 | `OK` |
| `eacode-official` | `ristretto255` | `1/2` | 0.5000 | 24 | 32 | 1046678.47 | 39823.152 | 39823.175 | 338.973 | `OK` |
| `eacode-official` | `ristretto255` | `1/2` | — | 26 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `eacode-official` | `ristretto255` | `1/2` | — | 28 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `eacode-official` | `ristretto255` | `1/2` | — | 30 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `eacode-official` | `ristretto255` | `1/4` | 0.2500 | 20 | 32 | 58302.38 | 1457.507 | 1458.924 | 18.709 | `OK` |
| `eacode-official` | `ristretto255` | `1/4` | 0.2500 | 22 | 32 | 251792.93 | 9011.968 | 9004.628 | 81.615 | `OK` |
| `eacode-official` | `ristretto255` | `1/4` | 0.2500 | 24 | 32 | 1108526.45 | 41378.065 | 41376.893 | 353.471 | `OK` |
| `eacode-official` | `ristretto255` | `1/4` | — | 26 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `eacode-official` | `ristretto255` | `1/4` | — | 28 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `eacode-official` | `ristretto255` | `1/4` | — | 30 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `ea-explicit` | `goldilocks` | `1/2` | 0.5000 | 20 | 32 | 5385.34 | 137.953 | 138.016 | 8.869 | `OK` |
| `ea-explicit` | `goldilocks` | `1/2` | 0.5000 | 22 | 32 | 22886.32 | 1369.412 | 1369.157 | 38.900 | `OK` |
| `ea-explicit` | `goldilocks` | `1/2` | 0.5000 | 24 | 32 | 103173.41 | 7717.441 | 7711.502 | 169.104 | `OK` |
| `ea-explicit` | `goldilocks` | `1/2` | — | 26 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `ea-explicit` | `goldilocks` | `1/2` | — | 28 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `ea-explicit` | `goldilocks` | `1/2` | — | 30 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `ea-explicit` | `goldilocks` | `1/4` | 0.2500 | 20 | 32 | 5656.10 | 148.322 | 148.198 | 9.291 | `OK` |
| `ea-explicit` | `goldilocks` | `1/4` | 0.2500 | 22 | 32 | 23988.08 | 1447.288 | 1447.300 | 40.658 | `OK` |
| `ea-explicit` | `goldilocks` | `1/4` | 0.2500 | 24 | 32 | 107859.58 | 8011.912 | 8008.080 | 176.098 | `OK` |
| `ea-explicit` | `goldilocks` | `1/4` | — | 26 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `ea-explicit` | `goldilocks` | `1/4` | — | 28 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `ea-explicit` | `goldilocks` | `1/4` | — | 30 | 32 | — | — | — | — | `OOM_SKIPPED` |

## Notes & Boundaries

- `ea-explicit` (`goldilocks`, config rate `1/2`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 13416.0 GiB.
- `ea-explicit` (`goldilocks`, config rate `1/2`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 3138.0 GiB.
- `ea-explicit` (`goldilocks`, config rate `1/2`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 730.5 GiB.
- `ea-explicit` (`goldilocks`, config rate `1/4`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 13864.0 GiB.
- `ea-explicit` (`goldilocks`, config rate `1/4`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 3250.0 GiB.
- `ea-explicit` (`goldilocks`, config rate `1/4`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 758.5 GiB.
- `ea-explicit` (`secp256k1`, config rate `1/2`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 1464.0 GiB.
- `ea-explicit` (`secp256k1`, config rate `1/2`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 26880.0 GiB.
- `ea-explicit` (`secp256k1`, config rate `1/2`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 6288.0 GiB.
- `ea-explicit` (`secp256k1`, config rate `1/4`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 1522.0 GiB.
- `ea-explicit` (`secp256k1`, config rate `1/4`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 27808.0 GiB.
- `ea-explicit` (`secp256k1`, config rate `1/4`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 6520.0 GiB.
- `eacode-official` (`ristretto255`, config rate `1/2`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 1464.0 GiB.
- `eacode-official` (`ristretto255`, config rate `1/2`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 26880.0 GiB.
- `eacode-official` (`ristretto255`, config rate `1/2`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 6288.0 GiB.
- `eacode-official` (`ristretto255`, config rate `1/4`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 1522.0 GiB.
- `eacode-official` (`ristretto255`, config rate `1/4`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 27808.0 GiB.
- `eacode-official` (`ristretto255`, config rate `1/4`, `OOM_SKIPPED`): Explicit matrix plus message/output lower bound 6520.0 GiB.
