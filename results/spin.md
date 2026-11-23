# SPIN Binary Structured Linear Codes (IMT / Packet-RS8)

Single-polynomial 1D encoding benchmarks for `spin` (Zoo #19; status summary: DOMAIN_LIMIT: 2, OK: 10).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`taskset -c 0-31`, `RAYON_NUM_THREADS=32`, `OMP_NUM_THREADS=32`); release build (`target-cpu=native`)
- **Repositories / Revisions**: `spin_codes@584a7fb654e824bf296aeb92ef7c6edd92e63fc2`
- **Field(s)**: `block128`
- **Message Lengths**: `K = 2^k` (`k ∈ {20, 22, 24, 26, 28, 30}`)
- **1D Geometry**: Single codeword (`nrows = 1`, `width = 1`, `log_batch_size = 0`; no interleaving, no 2D matrix reshape)

## Measurement Methodology

- **Sampling**: 1 warmup + 3 serial measured runs; reports arithmetic mean and median.
- **Timing Scope**: Measures the native 1D encoder call (`input_elements` -> `codeword_elements`) only; excludes setup (`setup_ms`), input generation, caller-buffer reset (for in-place entry points), correctness checks, and Merkle hashing/opening. Before timing, the driver pre-touches or reuses caller-owned buffers; output and temporary scratch buffers allocated internally by the encoder during the timed interval can still trigger page faults, and those times are included in the recorded measurements (per-row minor/major fault counts are logged in `results/spin.csv` `notes`).
- **Memory**. `Peak RSS` is whole-process peak resident memory (`GiB`), including setup.

## Results

| Variant | Field | Nominal Rate | Actual Rate | k | T | Setup (ms) | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `imt` | `block128` | `1/2` | 0.5000 | 20 | 1 | 63.99 | 12.707 | 12.697 | 0.107 | `OK` |
| `imt` | `block128` | `1/2` | 0.5000 | 22 | 1 | 269.66 | 82.079 | 82.009 | 0.426 | `OK` |
| `imt` | `block128` | `1/2` | 0.5000 | 24 | 1 | 1201.79 | 361.300 | 358.012 | 1.785 | `OK` |
| `imt` | `block128` | `1/2` | 0.5000 | 26 | 1 | 5027.17 | 1558.486 | 1558.248 | 7.135 | `OK` |
| `imt` | `block128` | `1/2` | 0.5000 | 28 | 1 | 22069.33 | 7047.477 | 7043.644 | 28.533 | `OK` |
| `imt` | `block128` | `1/2` | 0.5000 | 30 | 1 | 150433.75 | 39889.260 | 39880.075 | 114.127 | `OK` |
| `packet` | `block128` | `1/2` | 0.5000 | 20 | 1 | 36.71 | 8.029 | 7.998 | 0.102 | `OK` |
| `packet` | `block128` | `1/2` | 0.5000 | 22 | 1 | 156.05 | 35.657 | 35.645 | 0.385 | `OK` |
| `packet` | `block128` | `1/2` | 0.5000 | 24 | 1 | 642.69 | 146.979 | 147.001 | 1.539 | `OK` |
| `packet` | `block128` | `1/2` | 0.5000 | 26 | 1 | 2595.44 | 618.195 | 618.282 | 6.154 | `OK` |
| `packet` | `block128` | `1/2` | — | 28 | 1 | — | — | — | — | `DOMAIN_LIMIT` |
| `packet` | `block128` | `1/2` | — | 30 | 1 | — | — | — | — | `DOMAIN_LIMIT` |

## Notes & Boundaries

- `imt` (`block128`, config rate `1/2`, `OK`): 128-bit binary records. Stock forward single-codeword transform is serial.
- `packet` (`block128`, config rate `1/2`, `DOMAIN_LIMIT`): 128-bit binary records. Stock forward single-codeword transform is serial. 32-bit byte route bounds.
- `packet` (`block128`, config rate `1/2`, `OK`): 128-bit binary records. Stock forward single-codeword transform is serial.
