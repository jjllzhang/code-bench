# Bolt Sketched Codes (bolt-xor / bolt32)

Single-polynomial 1D encoding benchmarks for `bolt` (Zoo #9; status summary: OK: 24).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`taskset -c 0-31`, `RAYON_NUM_THREADS=32`, `OMP_NUM_THREADS=32`); release build (`target-cpu=native`)
- **Repositories / Revisions**: `bolt-rs@3832e47b24e7b3e10525c9c5bcfc1cfe66d525f2 with local 1D driver`
- **Field(s)**: `bf32`
- **Message Lengths**: `K = 2^k` (`k ∈ {20, 22, 24, 26, 28, 30}`)
- **1D Geometry**: Single codeword (`nrows = 1`, `width = 1`, `log_batch_size = 0`; no interleaving, no 2D matrix reshape)

## Measurement Methodology

- **Sampling**: 1 warmup + 3 serial measured runs; reports arithmetic mean and median.
- **Timing Scope**: Measures the native 1D encoder call (`input_elements` -> `codeword_elements`) only; excludes setup (`setup_ms`), input generation, caller-buffer reset (for in-place entry points), correctness checks, and Merkle hashing/opening. Before timing, the driver pre-touches or reuses caller-owned buffers; output and temporary scratch buffers allocated internally by the encoder during the timed interval can still trigger page faults, and those times are included in the recorded measurements (per-row minor/major fault counts are logged in `results/bolt.csv` `notes`).
- **Memory**. `Peak RSS` is whole-process peak resident memory (`GiB`), including setup.

## Results

| Variant | Field | Nominal Rate | Actual Rate | k | T | Setup (ms) | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `bolt-xor` | `bf32` | `1/2` | 0.8000 | 20 | 32 | 205.81 | 81.817 | 81.641 | 0.150 | `OK` |
| `bolt-xor` | `bf32` | `1/2` | 0.8000 | 22 | 32 | 1009.23 | 325.655 | 324.767 | 0.576 | `OK` |
| `bolt-xor` | `bf32` | `1/2` | 0.8000 | 24 | 32 | 4871.50 | 1310.895 | 1306.998 | 2.268 | `OK` |
| `bolt-xor` | `bf32` | `1/2` | 0.8000 | 26 | 32 | 20871.28 | 5045.230 | 5030.381 | 9.064 | `OK` |
| `bolt-xor` | `bf32` | `1/2` | 0.8000 | 28 | 32 | 86223.27 | 20558.636 | 20561.149 | 36.252 | `OK` |
| `bolt-xor` | `bf32` | `1/2` | 0.8000 | 30 | 32 | 383159.51 | 80798.224 | 80809.058 | 145.002 | `OK` |
| `bolt-xor` | `bf32` | `1/4` | 0.6667 | 20 | 32 | 208.79 | 85.791 | 85.838 | 0.156 | `OK` |
| `bolt-xor` | `bf32` | `1/4` | 0.6667 | 22 | 32 | 1009.84 | 345.389 | 343.579 | 0.592 | `OK` |
| `bolt-xor` | `bf32` | `1/4` | 0.6667 | 24 | 32 | 4874.58 | 1398.237 | 1392.450 | 2.361 | `OK` |
| `bolt-xor` | `bf32` | `1/4` | 0.6667 | 26 | 32 | 21003.23 | 5577.472 | 5574.154 | 9.439 | `OK` |
| `bolt-xor` | `bf32` | `1/4` | 0.6667 | 28 | 32 | 86778.83 | 22460.001 | 22341.327 | 37.752 | `OK` |
| `bolt-xor` | `bf32` | `1/4` | 0.6667 | 30 | 32 | 381734.75 | 87469.614 | 87328.535 | 151.002 | `OK` |
| `bolt32` | `bf32` | `1/2` | 0.8000 | 20 | 32 | 473.09 | 80.909 | 80.283 | 0.197 | `OK` |
| `bolt32` | `bf32` | `1/2` | 0.8000 | 22 | 32 | 2032.35 | 320.895 | 320.876 | 0.785 | `OK` |
| `bolt32` | `bf32` | `1/2` | 0.8000 | 24 | 32 | 8428.94 | 1387.811 | 1389.552 | 3.143 | `OK` |
| `bolt32` | `bf32` | `1/2` | 0.8000 | 26 | 32 | 34978.23 | 5359.735 | 5355.899 | 12.564 | `OK` |
| `bolt32` | `bf32` | `1/2` | 0.8000 | 28 | 32 | 157759.35 | 20879.130 | 20863.408 | 50.252 | `OK` |
| `bolt32` | `bf32` | `1/2` | 0.8000 | 30 | 32 | 606866.76 | 82233.740 | 82040.880 | 201.002 | `OK` |
| `bolt32` | `bf32` | `1/4` | 0.6667 | 20 | 32 | 471.66 | 86.429 | 86.496 | 0.197 | `OK` |
| `bolt32` | `bf32` | `1/4` | 0.6667 | 22 | 32 | 2038.56 | 346.262 | 345.729 | 0.787 | `OK` |
| `bolt32` | `bf32` | `1/4` | 0.6667 | 24 | 32 | 8482.17 | 1407.271 | 1398.032 | 3.143 | `OK` |
| `bolt32` | `bf32` | `1/4` | 0.6667 | 26 | 32 | 35182.67 | 5712.088 | 5712.893 | 12.564 | `OK` |
| `bolt32` | `bf32` | `1/4` | 0.6667 | 28 | 32 | 158222.51 | 22883.851 | 22831.240 | 50.252 | `OK` |
| `bolt32` | `bf32` | `1/4` | 0.6667 | 30 | 32 | 615489.70 | 92324.786 | 92193.233 | 201.002 | `OK` |

## Notes & Boundaries

- `bolt-xor` (`bf32`, config rate `1/2`, `OK`): Requested rate applies to inner RS. Actual rate includes systematic input. expander_left_degree=8 expander_right_degree=64 inner_inverse_rate=2
- `bolt-xor` (`bf32`, config rate `1/4`, `OK`): Requested rate applies to inner RS. Actual rate includes systematic input. expander_left_degree=8 expander_right_degree=64 inner_inverse_rate=4
- `bolt32` (`bf32`, config rate `1/2`, `OK`): Requested rate applies to inner RS. Actual rate includes systematic input. expander_left_degree=8 expander_right_degree=64 inner_inverse_rate=2
- `bolt32` (`bf32`, config rate `1/4`, `OK`): Requested rate applies to inner RS. Actual rate includes systematic input. expander_left_degree=8 expander_right_degree=64 inner_inverse_rate=4
