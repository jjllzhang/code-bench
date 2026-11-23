# Reed–Solomon (Multiplicative NTT Coset LDE)

Single-polynomial 1D encoding benchmarks for `rs` (Zoo #1; status summary: DOMAIN_LIMIT: 5, OK: 19).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`taskset -c 0-31`, `RAYON_NUM_THREADS=32`, `OMP_NUM_THREADS=32`); release build (`target-cpu=native`)
- **Repositories / Revisions**: `Plonky3/Plonky3@0d803737b681774186cd283b1fd2d8e493655c82`
- **Field(s)**: `babybear`, `goldilocks`
- **Message Lengths**: `K = 2^k` (`k ∈ {20, 22, 24, 26, 28, 30}`)
- **1D Geometry**: Single codeword (`nrows = 1`, `width = 1`, `log_batch_size = 0`; no interleaving, no 2D matrix reshape)

## Measurement Methodology

- **Sampling**: 1 warmup + 3 serial measured runs; reports arithmetic mean and median.
- **Timing Scope**: Measures the native 1D encoder call (`input_elements` -> `codeword_elements`) only; excludes setup (`setup_ms`), input generation, caller-buffer reset (for in-place entry points), correctness checks, and Merkle hashing/opening. Before timing, the driver pre-touches or reuses caller-owned buffers; output and temporary scratch buffers allocated internally by the encoder during the timed interval can still trigger page faults, and those times are included in the recorded measurements (per-row minor/major fault counts are logged in `results/rs.csv` `notes`).
- **Memory**. `Peak RSS` is whole-process peak resident memory (`GiB`), including setup.

## Results

| Variant | Field | Nominal Rate | Actual Rate | k | T | Setup (ms) | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `p3-coset-lde` | `babybear` | `1/2` | 0.5000 | 20 | 32 | 7.66 | 26.564 | 26.612 | 0.016 | `OK` |
| `p3-coset-lde` | `babybear` | `1/2` | 0.5000 | 22 | 32 | 19.44 | 84.233 | 84.259 | 0.062 | `OK` |
| `p3-coset-lde` | `babybear` | `1/2` | 0.5000 | 24 | 32 | 70.67 | 335.044 | 334.696 | 0.352 | `OK` |
| `p3-coset-lde` | `babybear` | `1/2` | 0.5000 | 26 | 32 | 263.72 | 1371.380 | 1363.525 | 1.469 | `OK` |
| `p3-coset-lde` | `babybear` | `1/2` | — | 28 | 32 | — | — | — | — | `DOMAIN_LIMIT` |
| `p3-coset-lde` | `babybear` | `1/2` | — | 30 | 32 | — | — | — | — | `DOMAIN_LIMIT` |
| `p3-coset-lde` | `babybear` | `1/4` | 0.2500 | 20 | 32 | 7.61 | 32.659 | 32.781 | 0.023 | `OK` |
| `p3-coset-lde` | `babybear` | `1/4` | 0.2500 | 22 | 32 | 20.81 | 116.828 | 115.841 | 0.137 | `OK` |
| `p3-coset-lde` | `babybear` | `1/4` | 0.2500 | 24 | 32 | 79.47 | 492.878 | 487.074 | 0.600 | `OK` |
| `p3-coset-lde` | `babybear` | `1/4` | — | 26 | 32 | — | — | — | — | `DOMAIN_LIMIT` |
| `p3-coset-lde` | `babybear` | `1/4` | — | 28 | 32 | — | — | — | — | `DOMAIN_LIMIT` |
| `p3-coset-lde` | `babybear` | `1/4` | — | 30 | 32 | — | — | — | — | `DOMAIN_LIMIT` |
| `p3-coset-lde` | `goldilocks` | `1/2` | 0.5000 | 20 | 32 | 10.81 | 16.767 | 16.910 | 0.029 | `OK` |
| `p3-coset-lde` | `goldilocks` | `1/2` | 0.5000 | 22 | 32 | 33.97 | 80.127 | 81.055 | 0.172 | `OK` |
| `p3-coset-lde` | `goldilocks` | `1/2` | 0.5000 | 24 | 32 | 125.10 | 258.672 | 258.672 | 0.729 | `OK` |
| `p3-coset-lde` | `goldilocks` | `1/2` | 0.5000 | 26 | 32 | 482.50 | 966.558 | 961.177 | 2.975 | `OK` |
| `p3-coset-lde` | `goldilocks` | `1/2` | 0.5000 | 28 | 32 | 1832.08 | 3830.910 | 3832.318 | 11.975 | `OK` |
| `p3-coset-lde` | `goldilocks` | `1/2` | 0.5000 | 30 | 32 | 7629.36 | 17053.001 | 16699.257 | 47.975 | `OK` |
| `p3-coset-lde` | `goldilocks` | `1/4` | 0.2500 | 20 | 32 | 12.79 | 22.740 | 22.419 | 0.051 | `OK` |
| `p3-coset-lde` | `goldilocks` | `1/4` | 0.2500 | 22 | 32 | 42.50 | 92.533 | 91.341 | 0.293 | `OK` |
| `p3-coset-lde` | `goldilocks` | `1/4` | 0.2500 | 24 | 32 | 149.73 | 290.067 | 290.032 | 1.223 | `OK` |
| `p3-coset-lde` | `goldilocks` | `1/4` | 0.2500 | 26 | 32 | 590.16 | 1178.320 | 1173.671 | 4.979 | `OK` |
| `p3-coset-lde` | `goldilocks` | `1/4` | 0.2500 | 28 | 32 | 2296.46 | 5152.675 | 5152.885 | 19.971 | `OK` |
| `p3-coset-lde` | `goldilocks` | `1/4` | 0.2500 | 30 | 32 | 9420.31 | 21363.501 | 21420.770 | 79.969 | `OK` |

## Notes & Boundaries

- `p3-coset-lde` (`babybear`, config rate `1/2`, `DOMAIN_LIMIT`): Single-column coset LDE from input evaluations. Owned output buffer reused. Need k+log2(c) <= 27.
- `p3-coset-lde` (`babybear`, config rate `1/2`, `OK`): Single-column coset LDE from input evaluations. Owned output buffer reused.
- `p3-coset-lde` (`babybear`, config rate `1/4`, `DOMAIN_LIMIT`): Single-column coset LDE from input evaluations. Owned output buffer reused. Need k+log2(c) <= 27.
- `p3-coset-lde` (`babybear`, config rate `1/4`, `OK`): Single-column coset LDE from input evaluations. Owned output buffer reused.
- `p3-coset-lde` (`goldilocks`, config rate `1/2`, `OK`): Single-column coset LDE from input evaluations. Owned output buffer reused.
- `p3-coset-lde` (`goldilocks`, config rate `1/4`, `OK`): Single-column coset LDE from input evaluations. Owned output buffer reused.
