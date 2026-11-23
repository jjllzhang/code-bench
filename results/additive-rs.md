# Binary Additive Reed–Solomon (LCH14 / PolyBasis / Bolt-RS)

Single-polynomial 1D encoding benchmarks for `additive-rs` (Zoo #3; status summary: OK: 60, UNSUPPORTED_BACKEND: 24).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`taskset -c 0-31`, `RAYON_NUM_THREADS=32`, `OMP_NUM_THREADS=32`); release build (`target-cpu=native`)
- **Repositories / Revisions**: `Plonky3/Plonky3@0d803737b681774186cd283b1fd2d8e493655c82`, `bolt-rs@3832e47b24e7b3e10525c9c5bcfc1cfe66d525f2 with local 1D driver`
- **Field(s)**: `bf128`, `bf32`, `bf64`
- **Message Lengths**: `K = 2^k` (`k ∈ {20, 22, 24, 26, 28, 30}`)
- **1D Geometry**: Single codeword (`nrows = 1`, `width = 1`, `log_batch_size = 0`; no interleaving, no 2D matrix reshape)

## Measurement Methodology

- **Sampling**: 1 warmup + 3 serial measured runs; reports arithmetic mean and median.
- **Timing Scope**: Measures the native 1D encoder call (`input_elements` -> `codeword_elements`) only; excludes setup (`setup_ms`), input generation, caller-buffer reset (for in-place entry points), correctness checks, and Merkle hashing/opening. Before timing, the driver pre-touches or reuses caller-owned buffers; output and temporary scratch buffers allocated internally by the encoder during the timed interval can still trigger page faults, and those times are included in the recorded measurements (per-row minor/major fault counts are logged in `results/additive-rs.csv` `notes`).
- **Memory**. `Peak RSS` is whole-process peak resident memory (`GiB`), including setup.

## Results

| Variant | Field | Nominal Rate | Actual Rate | k | T | Setup (ms) | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `bolt-rs` | `bf32` | `1/2` | 0.5000 | 20 | 1 | 18.22 | 41.404 | 41.415 | 0.025 | `OK` |
| `bolt-rs` | `bf32` | `1/2` | 0.5000 | 22 | 1 | 74.55 | 174.759 | 174.763 | 0.096 | `OK` |
| `bolt-rs` | `bf32` | `1/2` | 0.5000 | 24 | 1 | 291.85 | 740.898 | 742.036 | 0.377 | `OK` |
| `bolt-rs` | `bf32` | `1/2` | 0.5000 | 26 | 1 | 1208.23 | 3456.038 | 3450.693 | 1.502 | `OK` |
| `bolt-rs` | `bf32` | `1/2` | 0.5000 | 28 | 1 | 5182.71 | 15774.159 | 15793.000 | 6.002 | `OK` |
| `bolt-rs` | `bf32` | `1/2` | 0.5000 | 30 | 1 | 20876.32 | 72040.298 | 72038.301 | 24.002 | `OK` |
| `bolt-rs` | `bf32` | `1/4` | 0.2500 | 20 | 1 | 32.25 | 81.573 | 81.582 | 0.041 | `OK` |
| `bolt-rs` | `bf32` | `1/4` | 0.2500 | 22 | 1 | 129.33 | 344.718 | 344.752 | 0.158 | `OK` |
| `bolt-rs` | `bf32` | `1/4` | 0.2500 | 24 | 1 | 520.68 | 1460.502 | 1462.607 | 0.627 | `OK` |
| `bolt-rs` | `bf32` | `1/4` | 0.2500 | 26 | 1 | 2194.04 | 7054.133 | 7049.040 | 2.502 | `OK` |
| `bolt-rs` | `bf32` | `1/4` | 0.2500 | 28 | 1 | 9105.25 | 31995.064 | 31991.939 | 10.002 | `OK` |
| `bolt-rs` | `bf32` | `1/4` | 0.2500 | 30 | 1 | 36249.35 | 150013.433 | 150013.919 | 40.002 | `OK` |
| `lch` | `bf128` | `1/2` | 0.5000 | 20 | 32 | 0.00 | 5.298 | 5.386 | 0.021 | `OK` |
| `lch` | `bf128` | `1/2` | 0.5000 | 22 | 32 | 0.00 | 23.690 | 23.296 | 0.156 | `OK` |
| `lch` | `bf128` | `1/2` | 0.5000 | 24 | 32 | 0.00 | 89.084 | 89.048 | 0.744 | `OK` |
| `lch` | `bf128` | `1/2` | 0.5000 | 26 | 32 | 0.00 | 358.549 | 358.758 | 2.996 | `OK` |
| `lch` | `bf128` | `1/2` | 0.5000 | 28 | 32 | 0.00 | 1843.905 | 1838.489 | 11.977 | `OK` |
| `lch` | `bf128` | `1/2` | 0.5000 | 30 | 32 | 0.00 | 8023.440 | 8031.899 | 47.979 | `OK` |
| `lch` | `bf128` | `1/4` | 0.2500 | 20 | 32 | 0.00 | 9.318 | 9.315 | 0.064 | `OK` |
| `lch` | `bf128` | `1/4` | 0.2500 | 22 | 32 | 0.00 | 36.266 | 36.244 | 0.299 | `OK` |
| `lch` | `bf128` | `1/4` | 0.2500 | 24 | 32 | 0.00 | 147.517 | 147.544 | 1.246 | `OK` |
| `lch` | `bf128` | `1/4` | 0.2500 | 26 | 32 | 0.00 | 612.931 | 590.190 | 4.986 | `OK` |
| `lch` | `bf128` | `1/4` | 0.2500 | 28 | 32 | 0.00 | 3114.147 | 3129.605 | 19.977 | `OK` |
| `lch` | `bf128` | `1/4` | 0.2500 | 30 | 32 | 0.00 | 13054.488 | 13330.975 | 79.979 | `OK` |
| `lch` | `bf32` | `1/2` | 0.5000 | 20 | 32 | 0.00 | 6.872 | 6.930 | 0.006 | `OK` |
| `lch` | `bf32` | `1/2` | 0.5000 | 22 | 32 | 0.00 | 20.562 | 20.645 | 0.018 | `OK` |
| `lch` | `bf32` | `1/2` | 0.5000 | 24 | 32 | 0.00 | 56.579 | 57.135 | 0.154 | `OK` |
| `lch` | `bf32` | `1/2` | 0.5000 | 26 | 32 | 0.00 | 214.911 | 213.968 | 0.740 | `OK` |
| `lch` | `bf32` | `1/2` | 0.5000 | 28 | 32 | 0.00 | 930.558 | 926.804 | 2.990 | `OK` |
| `lch` | `bf32` | `1/2` | 0.5000 | 30 | 32 | 0.00 | 3876.730 | 3856.658 | 11.975 | `OK` |
| `lch` | `bf32` | `1/4` | 0.2500 | 20 | 32 | 0.00 | 10.599 | 10.618 | 0.006 | `OK` |
| `lch` | `bf32` | `1/4` | 0.2500 | 22 | 32 | 0.00 | 28.307 | 27.673 | 0.051 | `OK` |
| `lch` | `bf32` | `1/4` | 0.2500 | 24 | 32 | 0.00 | 103.025 | 104.024 | 0.289 | `OK` |
| `lch` | `bf32` | `1/4` | 0.2500 | 26 | 32 | 0.00 | 428.128 | 406.051 | 1.242 | `OK` |
| `lch` | `bf32` | `1/4` | 0.2500 | 28 | 32 | 0.00 | 1731.166 | 1713.821 | 4.990 | `OK` |
| `lch` | `bf32` | `1/4` | 0.2500 | 30 | 32 | 0.00 | 7485.276 | 7602.427 | 19.975 | `OK` |
| `lch` | `bf64` | `1/2` | 0.5000 | 20 | 32 | 0.00 | 7.205 | 7.217 | 0.010 | `OK` |
| `lch` | `bf64` | `1/2` | 0.5000 | 22 | 32 | 0.00 | 20.972 | 21.637 | 0.072 | `OK` |
| `lch` | `bf64` | `1/2` | 0.5000 | 24 | 32 | 0.00 | 63.304 | 63.025 | 0.363 | `OK` |
| `lch` | `bf64` | `1/2` | 0.5000 | 26 | 32 | 0.00 | 254.303 | 254.292 | 1.480 | `OK` |
| `lch` | `bf64` | `1/2` | 0.5000 | 28 | 32 | 0.00 | 1227.432 | 1226.536 | 5.975 | `OK` |
| `lch` | `bf64` | `1/2` | 0.5000 | 30 | 32 | 0.00 | 5253.158 | 5271.374 | 23.979 | `OK` |
| `lch` | `bf64` | `1/4` | 0.2500 | 20 | 32 | 0.00 | 11.247 | 10.681 | 0.012 | `OK` |
| `lch` | `bf64` | `1/4` | 0.2500 | 22 | 32 | 0.00 | 32.917 | 31.718 | 0.145 | `OK` |
| `lch` | `bf64` | `1/4` | 0.2500 | 24 | 32 | 0.00 | 115.469 | 115.495 | 0.607 | `OK` |
| `lch` | `bf64` | `1/4` | 0.2500 | 26 | 32 | 0.00 | 489.328 | 466.414 | 2.484 | `OK` |
| `lch` | `bf64` | `1/4` | 0.2500 | 28 | 32 | 0.00 | 2286.234 | 2286.231 | 9.979 | `OK` |
| `lch` | `bf64` | `1/4` | 0.2500 | 30 | 32 | 0.00 | 9347.412 | 9646.798 | 39.979 | `OK` |
| `polybasis` | `bf128` | `1/2` | 0.5000 | 20 | 32 | 0.00 | 4.483 | 4.470 | 0.049 | `OK` |
| `polybasis` | `bf128` | `1/2` | 0.5000 | 22 | 32 | 0.00 | 27.208 | 28.308 | 0.188 | `OK` |
| `polybasis` | `bf128` | `1/2` | 0.5000 | 24 | 32 | 0.00 | 81.539 | 79.701 | 0.752 | `OK` |
| `polybasis` | `bf128` | `1/2` | 0.5000 | 26 | 32 | 0.00 | 371.011 | 370.898 | 3.002 | `OK` |
| `polybasis` | `bf128` | `1/2` | 0.5000 | 28 | 32 | 0.00 | 1125.488 | 1115.038 | 12.002 | `OK` |
| `polybasis` | `bf128` | `1/2` | 0.5000 | 30 | 32 | 0.00 | 4244.557 | 4233.646 | 47.998 | `OK` |
| `polybasis` | `bf128` | `1/4` | 0.2500 | 20 | 32 | 0.00 | 7.536 | 7.405 | 0.078 | `OK` |
| `polybasis` | `bf128` | `1/4` | 0.2500 | 22 | 32 | 0.00 | 51.521 | 51.206 | 0.314 | `OK` |
| `polybasis` | `bf128` | `1/4` | 0.2500 | 24 | 32 | 0.00 | 168.257 | 168.139 | 1.252 | `OK` |
| `polybasis` | `bf128` | `1/4` | 0.2500 | 26 | 32 | 0.00 | 685.705 | 687.349 | 5.002 | `OK` |
| `polybasis` | `bf128` | `1/4` | 0.2500 | 28 | 32 | 0.00 | 2089.195 | 2090.391 | 19.994 | `OK` |
| `polybasis` | `bf128` | `1/4` | 0.2500 | 30 | 32 | 0.00 | 7997.710 | 7992.449 | 79.998 | `OK` |
| `polybasis` | `bf32` | `1/2` | — | 20 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf32` | `1/2` | — | 22 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf32` | `1/2` | — | 24 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf32` | `1/2` | — | 26 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf32` | `1/2` | — | 28 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf32` | `1/2` | — | 30 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf32` | `1/4` | — | 20 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf32` | `1/4` | — | 22 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf32` | `1/4` | — | 24 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf32` | `1/4` | — | 26 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf32` | `1/4` | — | 28 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf32` | `1/4` | — | 30 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf64` | `1/2` | — | 20 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf64` | `1/2` | — | 22 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf64` | `1/2` | — | 24 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf64` | `1/2` | — | 26 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf64` | `1/2` | — | 28 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf64` | `1/2` | — | 30 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf64` | `1/4` | — | 20 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf64` | `1/4` | — | 22 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf64` | `1/4` | — | 24 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf64` | `1/4` | — | 26 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf64` | `1/4` | — | 28 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |
| `polybasis` | `bf64` | `1/4` | — | 30 | 32 | — | — | — | — | `UNSUPPORTED_BACKEND` |

## Notes & Boundaries

- `bolt-rs` (`bf32`, config rate `1/2`, `OK`): Stock per-codeword RS kernel is serial under the 32-core affinity.
- `bolt-rs` (`bf32`, config rate `1/4`, `OK`): Stock per-codeword RS kernel is serial under the 32-core affinity.
- `polybasis` (`bf32`, config rate `1/2`, `UNSUPPORTED_BACKEND`): Stock PolyBasisNtt implements BinaryField128 only.
- `polybasis` (`bf32`, config rate `1/4`, `UNSUPPORTED_BACKEND`): Stock PolyBasisNtt implements BinaryField128 only.
- `polybasis` (`bf64`, config rate `1/2`, `UNSUPPORTED_BACKEND`): Stock PolyBasisNtt implements BinaryField128 only.
- `polybasis` (`bf64`, config rate `1/4`, `UNSUPPORTED_BACKEND`): Stock PolyBasisNtt implements BinaryField128 only.
