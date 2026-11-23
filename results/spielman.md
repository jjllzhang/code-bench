# SIMD-Spielman (Mersenne61 / Monty64)

Single-polynomial 1D encoding benchmarks for `spielman` (Zoo #12; status summary: EXCLUDED_INTERLEAVED: 12).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`taskset -c 0-31`, `RAYON_NUM_THREADS=32`, `OMP_NUM_THREADS=32`); release build (`target-cpu=native`)
- **Repositories / Revisions**: `simd-spielman@7b399dbfecc406c79349015f1e21accc4def1be7`
- **Field(s)**: `m61`, `monty64`
- **Message Lengths**: `K = 2^k` (`k ∈ {20, 22, 24, 26, 28, 30}`)
- **1D Geometry**: Single codeword (`nrows = 1`, `width = 1`, `log_batch_size = 0`; no interleaving, no 2D matrix reshape)

## Measurement Methodology

- **Sampling**: 1 warmup + 3 serial measured runs; reports arithmetic mean and median.
- **Timing Scope**: Measures the native 1D encoder call (`input_elements` -> `codeword_elements`) only; excludes setup (`setup_ms`), input generation, caller-buffer reset (for in-place entry points), correctness checks, and Merkle hashing/opening. Before timing, the driver pre-touches or reuses caller-owned buffers; output and temporary scratch buffers allocated internally by the encoder during the timed interval can still trigger page faults, and those times are included in the recorded measurements (per-row minor/major fault counts are logged in `results/spielman.csv` `notes`).
- **Memory**. `Peak RSS` is whole-process peak resident memory (`GiB`), including setup.

## Results

| Variant | Field | Nominal Rate | Actual Rate | k | T | Setup (ms) | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `simd-mt` | `m61` | `native` | — | 20 | 32 | — | — | — | — | `EXCLUDED_INTERLEAVED` |
| `simd-mt` | `m61` | `native` | — | 22 | 32 | — | — | — | — | `EXCLUDED_INTERLEAVED` |
| `simd-mt` | `m61` | `native` | — | 24 | 32 | — | — | — | — | `EXCLUDED_INTERLEAVED` |
| `simd-mt` | `m61` | `native` | — | 26 | 32 | — | — | — | — | `EXCLUDED_INTERLEAVED` |
| `simd-mt` | `m61` | `native` | — | 28 | 32 | — | — | — | — | `EXCLUDED_INTERLEAVED` |
| `simd-mt` | `m61` | `native` | — | 30 | 32 | — | — | — | — | `EXCLUDED_INTERLEAVED` |
| `simd-mt` | `monty64` | `native` | — | 20 | 32 | — | — | — | — | `EXCLUDED_INTERLEAVED` |
| `simd-mt` | `monty64` | `native` | — | 22 | 32 | — | — | — | — | `EXCLUDED_INTERLEAVED` |
| `simd-mt` | `monty64` | `native` | — | 24 | 32 | — | — | — | — | `EXCLUDED_INTERLEAVED` |
| `simd-mt` | `monty64` | `native` | — | 26 | 32 | — | — | — | — | `EXCLUDED_INTERLEAVED` |
| `simd-mt` | `monty64` | `native` | — | 28 | 32 | — | — | — | — | `EXCLUDED_INTERLEAVED` |
| `simd-mt` | `monty64` | `native` | — | 30 | 32 | — | — | — | — | `EXCLUDED_INTERLEAVED` |

## Notes & Boundaries

- `simd-mt` (`m61`, config rate `native`, `EXCLUDED_INTERLEAVED`): Official SIMD harness processes independent codewords in parallel columns.
- `simd-mt` (`monty64`, config rate `native`, `EXCLUDED_INTERLEAVED`): Official SIMD harness processes independent codewords in parallel columns.
