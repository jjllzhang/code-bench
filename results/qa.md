# Systematic Quasi-Abelian Codes (WHT / Binary Spectral)

Single-polynomial 1D encoding benchmarks for `qa` (Zoo #6; status summary: OK: 96).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`taskset -c 0-31`, `RAYON_NUM_THREADS=32`, `OMP_NUM_THREADS=32`); release build (`target-cpu=native`)
- **Repositories / Revisions**: `jjllzhang/HyperFold@405b2094c70747af6e4b1ae05aa0661bf6c7b9a9`, `jjllzhang/plonky3-binary-qa@19affa0a8de1b283e766556b757725c701397657`
- **Field(s)**: `bf128`, `bf32`, `bf32-bf128`, `bf32-bf64`, `bf64`, `bf64-bf128`, `goldilocks`, `m127`
- **Message Lengths**: `K = 2^k` (`k ∈ {20, 22, 24, 26, 28, 30}`)
- **1D Geometry**: Single codeword (`nrows = 1`, `width = 1`, `log_batch_size = 0`; no interleaving, no 2D matrix reshape)

## Measurement Methodology

- **Sampling**: 1 warmup + 3 serial measured runs; reports arithmetic mean and median.
- **Timing Scope**: Measures the native 1D encoder call (`input_elements` -> `codeword_elements`) only; excludes setup (`setup_ms`), input generation, caller-buffer reset (for in-place entry points), correctness checks, and Merkle hashing/opening. Before timing, the driver pre-touches or reuses caller-owned buffers; output and temporary scratch buffers allocated internally by the encoder during the timed interval can still trigger page faults, and those times are included in the recorded measurements (per-row minor/major fault counts are logged in `results/qa.csv` `notes`).
- **Memory**. `Peak RSS` is whole-process peak resident memory (`GiB`), including setup.

## Results

| Variant | Field | Nominal Rate | Actual Rate | k | T | Setup (ms) | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `binary-spectral` | `bf128` | `1/2` | 0.5000 | 20 | 32 | 10.01 | 8.272 | 8.304 | 0.053 | `OK` |
| `binary-spectral` | `bf128` | `1/2` | 0.5000 | 22 | 32 | 38.56 | 41.201 | 41.309 | 0.285 | `OK` |
| `binary-spectral` | `bf128` | `1/2` | 0.5000 | 24 | 32 | 150.01 | 176.686 | 176.287 | 1.232 | `OK` |
| `binary-spectral` | `bf128` | `1/2` | 0.5000 | 26 | 32 | 580.73 | 807.181 | 807.675 | 4.973 | `OK` |
| `binary-spectral` | `bf128` | `1/2` | 0.5000 | 28 | 32 | 2319.25 | 3530.756 | 3530.734 | 19.975 | `OK` |
| `binary-spectral` | `bf128` | `1/2` | 0.5000 | 30 | 32 | 9084.59 | 15412.375 | 15406.692 | 79.975 | `OK` |
| `binary-spectral` | `bf128` | `1/4` | 0.2500 | 20 | 32 | 29.64 | 17.534 | 17.209 | 0.119 | `OK` |
| `binary-spectral` | `bf128` | `1/4` | 0.2500 | 22 | 32 | 117.70 | 62.481 | 59.868 | 0.535 | `OK` |
| `binary-spectral` | `bf128` | `1/4` | 0.2500 | 24 | 32 | 441.42 | 348.339 | 346.437 | 2.221 | `OK` |
| `binary-spectral` | `bf128` | `1/4` | 0.2500 | 26 | 32 | 1760.34 | 1594.826 | 1596.003 | 8.969 | `OK` |
| `binary-spectral` | `bf128` | `1/4` | 0.2500 | 28 | 32 | 6903.94 | 7020.359 | 7022.656 | 35.979 | `OK` |
| `binary-spectral` | `bf128` | `1/4` | 0.2500 | 30 | 32 | 27112.99 | 26180.974 | 26151.554 | 143.971 | `OK` |
| `binary-spectral` | `bf32` | `1/2` | 0.5000 | 20 | 32 | 3.63 | 3.378 | 3.383 | 0.010 | `OK` |
| `binary-spectral` | `bf32` | `1/2` | 0.5000 | 22 | 32 | 14.52 | 10.239 | 10.153 | 0.053 | `OK` |
| `binary-spectral` | `bf32` | `1/2` | 0.5000 | 24 | 32 | 57.39 | 52.271 | 51.325 | 0.283 | `OK` |
| `binary-spectral` | `bf32` | `1/2` | 0.5000 | 26 | 32 | 229.79 | 214.622 | 219.598 | 1.230 | `OK` |
| `binary-spectral` | `bf32` | `1/2` | 0.5000 | 28 | 32 | 889.81 | 920.602 | 918.690 | 4.979 | `OK` |
| `binary-spectral` | `bf32` | `1/2` | 0.5000 | 30 | 32 | 3573.13 | 4036.944 | 4025.007 | 19.973 | `OK` |
| `binary-spectral` | `bf32` | `1/4` | 0.2500 | 20 | 32 | 10.99 | 7.305 | 7.306 | 0.018 | `OK` |
| `binary-spectral` | `bf32` | `1/4` | 0.2500 | 22 | 32 | 43.13 | 22.967 | 23.087 | 0.121 | `OK` |
| `binary-spectral` | `bf32` | `1/4` | 0.2500 | 24 | 32 | 172.20 | 85.440 | 85.012 | 0.541 | `OK` |
| `binary-spectral` | `bf32` | `1/4` | 0.2500 | 26 | 32 | 677.35 | 441.630 | 438.574 | 2.223 | `OK` |
| `binary-spectral` | `bf32` | `1/4` | 0.2500 | 28 | 32 | 2720.29 | 1960.591 | 1962.118 | 8.971 | `OK` |
| `binary-spectral` | `bf32` | `1/4` | 0.2500 | 30 | 32 | 10620.47 | 8414.776 | 8400.059 | 35.971 | `OK` |
| `binary-spectral` | `bf32-bf128` | `1/2` | 0.5000 | 20 | 32 | 11.19 | 7.192 | 6.767 | 0.023 | `OK` |
| `binary-spectral` | `bf32-bf128` | `1/2` | 0.5000 | 22 | 32 | 40.75 | 31.167 | 31.770 | 0.193 | `OK` |
| `binary-spectral` | `bf32-bf128` | `1/2` | 0.5000 | 24 | 32 | 155.49 | 122.673 | 120.488 | 0.850 | `OK` |
| `binary-spectral` | `bf32-bf128` | `1/2` | 0.5000 | 26 | 32 | 603.26 | 548.779 | 547.748 | 3.477 | `OK` |
| `binary-spectral` | `bf32-bf128` | `1/2` | 0.5000 | 28 | 32 | 2393.31 | 2478.662 | 2425.619 | 13.971 | `OK` |
| `binary-spectral` | `bf32-bf128` | `1/2` | 0.5000 | 30 | 32 | 9278.81 | 10456.858 | 10451.568 | 55.967 | `OK` |
| `binary-spectral` | `bf32-bf128` | `1/4` | 0.2500 | 20 | 32 | 32.17 | 18.131 | 17.821 | 0.078 | `OK` |
| `binary-spectral` | `bf32-bf128` | `1/4` | 0.2500 | 22 | 32 | 116.81 | 56.080 | 54.451 | 0.443 | `OK` |
| `binary-spectral` | `bf32-bf128` | `1/4` | 0.2500 | 24 | 32 | 454.06 | 295.334 | 295.105 | 1.855 | `OK` |
| `binary-spectral` | `bf32-bf128` | `1/4` | 0.2500 | 26 | 32 | 1790.71 | 1353.296 | 1353.195 | 7.477 | `OK` |
| `binary-spectral` | `bf32-bf128` | `1/4` | 0.2500 | 28 | 32 | 7054.22 | 5961.507 | 5961.057 | 29.973 | `OK` |
| `binary-spectral` | `bf32-bf128` | `1/4` | 0.2500 | 30 | 32 | 27578.93 | 23708.360 | 23693.480 | 119.969 | `OK` |
| `binary-spectral` | `bf32-bf64` | `1/2` | 0.5000 | 20 | 32 | 6.57 | 3.688 | 3.702 | 0.014 | `OK` |
| `binary-spectral` | `bf32-bf64` | `1/2` | 0.5000 | 22 | 32 | 21.87 | 14.098 | 14.156 | 0.104 | `OK` |
| `binary-spectral` | `bf32-bf64` | `1/2` | 0.5000 | 24 | 32 | 86.95 | 67.328 | 66.871 | 0.477 | `OK` |
| `binary-spectral` | `bf32-bf64` | `1/2` | 0.5000 | 26 | 32 | 347.26 | 295.596 | 294.104 | 1.975 | `OK` |
| `binary-spectral` | `bf32-bf64` | `1/2` | 0.5000 | 28 | 32 | 1378.94 | 1350.909 | 1348.472 | 7.969 | `OK` |
| `binary-spectral` | `bf32-bf64` | `1/2` | 0.5000 | 30 | 32 | 5277.03 | 5890.914 | 5867.309 | 31.969 | `OK` |
| `binary-spectral` | `bf32-bf64` | `1/4` | 0.2500 | 20 | 32 | 20.31 | 7.905 | 7.744 | 0.031 | `OK` |
| `binary-spectral` | `bf32-bf64` | `1/4` | 0.2500 | 22 | 32 | 65.62 | 30.599 | 31.891 | 0.219 | `OK` |
| `binary-spectral` | `bf32-bf64` | `1/4` | 0.2500 | 24 | 32 | 260.50 | 137.236 | 134.708 | 0.973 | `OK` |
| `binary-spectral` | `bf32-bf64` | `1/4` | 0.2500 | 26 | 32 | 1010.84 | 657.362 | 657.464 | 3.977 | `OK` |
| `binary-spectral` | `bf32-bf64` | `1/4` | 0.2500 | 28 | 32 | 4041.90 | 2979.390 | 2975.588 | 15.975 | `OK` |
| `binary-spectral` | `bf32-bf64` | `1/4` | 0.2500 | 30 | 32 | 15632.66 | 13207.516 | 13184.763 | 63.969 | `OK` |
| `binary-spectral` | `bf64` | `1/2` | 0.5000 | 20 | 32 | 6.03 | 4.607 | 4.584 | 0.018 | `OK` |
| `binary-spectral` | `bf64` | `1/2` | 0.5000 | 22 | 32 | 21.96 | 16.543 | 16.507 | 0.139 | `OK` |
| `binary-spectral` | `bf64` | `1/2` | 0.5000 | 24 | 32 | 87.54 | 86.079 | 84.503 | 0.602 | `OK` |
| `binary-spectral` | `bf64` | `1/2` | 0.5000 | 26 | 32 | 339.71 | 392.513 | 391.928 | 2.477 | `OK` |
| `binary-spectral` | `bf64` | `1/2` | 0.5000 | 28 | 32 | 1363.11 | 1769.486 | 1769.769 | 9.977 | `OK` |
| `binary-spectral` | `bf64` | `1/2` | 0.5000 | 30 | 32 | 5301.00 | 7714.876 | 7723.587 | 39.975 | `OK` |
| `binary-spectral` | `bf64` | `1/4` | 0.2500 | 20 | 32 | 16.51 | 9.435 | 9.266 | 0.035 | `OK` |
| `binary-spectral` | `bf64` | `1/4` | 0.2500 | 22 | 32 | 67.05 | 37.295 | 36.816 | 0.260 | `OK` |
| `binary-spectral` | `bf64` | `1/4` | 0.2500 | 24 | 32 | 259.78 | 161.218 | 160.476 | 1.104 | `OK` |
| `binary-spectral` | `bf64` | `1/4` | 0.2500 | 26 | 32 | 1017.72 | 795.119 | 794.592 | 4.473 | `OK` |
| `binary-spectral` | `bf64` | `1/4` | 0.2500 | 28 | 32 | 4055.49 | 3475.431 | 3476.174 | 17.979 | `OK` |
| `binary-spectral` | `bf64` | `1/4` | 0.2500 | 30 | 32 | 15854.01 | 15887.404 | 15282.516 | 71.973 | `OK` |
| `binary-spectral` | `bf64-bf128` | `1/2` | 0.5000 | 20 | 32 | 10.95 | 6.040 | 6.155 | 0.027 | `OK` |
| `binary-spectral` | `bf64-bf128` | `1/2` | 0.5000 | 22 | 32 | 38.85 | 30.801 | 31.200 | 0.225 | `OK` |
| `binary-spectral` | `bf64-bf128` | `1/2` | 0.5000 | 24 | 32 | 155.26 | 130.339 | 131.143 | 0.973 | `OK` |
| `binary-spectral` | `bf64-bf128` | `1/2` | 0.5000 | 26 | 32 | 595.10 | 597.121 | 599.815 | 3.975 | `OK` |
| `binary-spectral` | `bf64-bf128` | `1/2` | 0.5000 | 28 | 32 | 2367.28 | 2643.072 | 2643.071 | 15.973 | `OK` |
| `binary-spectral` | `bf64-bf128` | `1/2` | 0.5000 | 30 | 32 | 9293.18 | 11590.608 | 11586.063 | 63.977 | `OK` |
| `binary-spectral` | `bf64-bf128` | `1/4` | 0.2500 | 20 | 32 | 30.32 | 14.312 | 14.470 | 0.086 | `OK` |
| `binary-spectral` | `bf64-bf128` | `1/4` | 0.2500 | 22 | 32 | 113.86 | 60.412 | 60.020 | 0.475 | `OK` |
| `binary-spectral` | `bf64-bf128` | `1/4` | 0.2500 | 24 | 32 | 447.48 | 283.993 | 282.082 | 1.977 | `OK` |
| `binary-spectral` | `bf64-bf128` | `1/4` | 0.2500 | 26 | 32 | 1773.44 | 1313.537 | 1308.738 | 7.967 | `OK` |
| `binary-spectral` | `bf64-bf128` | `1/4` | 0.2500 | 28 | 32 | 6995.40 | 5908.374 | 5890.993 | 31.969 | `OK` |
| `binary-spectral` | `bf64-bf128` | `1/4` | 0.2500 | 30 | 32 | 27135.54 | 21629.646 | 21601.748 | 127.975 | `OK` |
| `packed-wht` | `m127` | `1/2` | 0.5000 | 20 | 32 | 42.97 | 10.333 | 10.150 | 0.080 | `OK` |
| `packed-wht` | `m127` | `1/2` | 0.5000 | 22 | 32 | 160.47 | 41.989 | 41.410 | 0.314 | `OK` |
| `packed-wht` | `m127` | `1/2` | 0.5000 | 24 | 32 | 638.20 | 268.650 | 268.744 | 1.252 | `OK` |
| `packed-wht` | `m127` | `1/2` | 0.5000 | 26 | 32 | 2455.33 | 1303.921 | 1303.378 | 5.002 | `OK` |
| `packed-wht` | `m127` | `1/2` | 0.5000 | 28 | 32 | 9615.72 | 5849.837 | 5851.313 | 20.000 | `OK` |
| `packed-wht` | `m127` | `1/2` | 0.5000 | 30 | 32 | 37902.59 | 26008.688 | 26017.781 | 80.002 | `OK` |
| `packed-wht` | `m127` | `1/4` | 0.2500 | 20 | 32 | 84.63 | 19.198 | 19.286 | 0.143 | `OK` |
| `packed-wht` | `m127` | `1/4` | 0.2500 | 22 | 32 | 329.66 | 79.216 | 78.957 | 0.564 | `OK` |
| `packed-wht` | `m127` | `1/4` | 0.2500 | 24 | 32 | 1297.72 | 543.667 | 520.726 | 2.252 | `OK` |
| `packed-wht` | `m127` | `1/4` | 0.2500 | 26 | 32 | 5195.17 | 2623.717 | 2603.610 | 9.002 | `OK` |
| `packed-wht` | `m127` | `1/4` | 0.2500 | 28 | 32 | 20358.14 | 11421.888 | 11422.962 | 36.002 | `OK` |
| `packed-wht` | `m127` | `1/4` | 0.2500 | 30 | 32 | 83278.42 | 56233.697 | 57858.407 | 144.002 | `OK` |
| `packed-wht` | `goldilocks` | `1/2` | 0.5000 | 20 | 32 | 21.20 | 5.203 | 5.138 | 0.041 | `OK` |
| `packed-wht` | `goldilocks` | `1/2` | 0.5000 | 22 | 32 | 81.73 | 20.804 | 20.657 | 0.158 | `OK` |
| `packed-wht` | `goldilocks` | `1/2` | 0.5000 | 24 | 32 | 307.00 | 118.749 | 117.257 | 0.627 | `OK` |
| `packed-wht` | `goldilocks` | `1/2` | 0.5000 | 26 | 32 | 1196.79 | 671.608 | 688.735 | 2.502 | `OK` |
| `packed-wht` | `goldilocks` | `1/2` | 0.5000 | 28 | 32 | 4816.92 | 3051.623 | 3051.839 | 10.002 | `OK` |
| `packed-wht` | `goldilocks` | `1/2` | 0.5000 | 30 | 32 | 18625.35 | 13029.117 | 12893.794 | 40.002 | `OK` |
| `packed-wht` | `goldilocks` | `1/4` | 0.2500 | 20 | 32 | 39.69 | 9.139 | 9.172 | 0.072 | `OK` |
| `packed-wht` | `goldilocks` | `1/4` | 0.2500 | 22 | 32 | 158.05 | 36.481 | 36.249 | 0.283 | `OK` |
| `packed-wht` | `goldilocks` | `1/4` | 0.2500 | 24 | 32 | 633.43 | 234.997 | 234.932 | 1.127 | `OK` |
| `packed-wht` | `goldilocks` | `1/4` | 0.2500 | 26 | 32 | 2523.92 | 1271.809 | 1295.136 | 4.502 | `OK` |
| `packed-wht` | `goldilocks` | `1/4` | 0.2500 | 28 | 32 | 10016.70 | 5704.423 | 5702.511 | 18.002 | `OK` |
| `packed-wht` | `goldilocks` | `1/4` | 0.2500 | 30 | 32 | 39223.46 | 25402.521 | 25229.725 | 72.002 | `OK` |

## Notes & Boundaries

- `binary-spectral` (`bf128`, config rate `1/2`, `OK`): One coefficient vector, log_batch_size=0. Hyphenated fields give input and codeword alphabets.
- `binary-spectral` (`bf128`, config rate `1/4`, `OK`): One coefficient vector, log_batch_size=0. Hyphenated fields give input and codeword alphabets.
- `binary-spectral` (`bf32`, config rate `1/2`, `OK`): One coefficient vector, log_batch_size=0. Hyphenated fields give input and codeword alphabets.
- `binary-spectral` (`bf32`, config rate `1/4`, `OK`): One coefficient vector, log_batch_size=0. Hyphenated fields give input and codeword alphabets.
- `binary-spectral` (`bf32-bf128`, config rate `1/2`, `OK`): One coefficient vector, log_batch_size=0. Hyphenated fields give input and codeword alphabets.
- `binary-spectral` (`bf32-bf128`, config rate `1/4`, `OK`): One coefficient vector, log_batch_size=0. Hyphenated fields give input and codeword alphabets.
- `binary-spectral` (`bf32-bf64`, config rate `1/2`, `OK`): One coefficient vector, log_batch_size=0. Hyphenated fields give input and codeword alphabets.
- `binary-spectral` (`bf32-bf64`, config rate `1/4`, `OK`): One coefficient vector, log_batch_size=0. Hyphenated fields give input and codeword alphabets.
- `binary-spectral` (`bf64`, config rate `1/2`, `OK`): One coefficient vector, log_batch_size=0. Hyphenated fields give input and codeword alphabets.
- `binary-spectral` (`bf64`, config rate `1/4`, `OK`): One coefficient vector, log_batch_size=0. Hyphenated fields give input and codeword alphabets.
- `binary-spectral` (`bf64-bf128`, config rate `1/2`, `OK`): One coefficient vector, log_batch_size=0. Hyphenated fields give input and codeword alphabets.
- `binary-spectral` (`bf64-bf128`, config rate `1/4`, `OK`): One coefficient vector, log_batch_size=0. Hyphenated fields give input and codeword alphabets.
- `packed-wht` (`goldilocks`, config rate `1/2`, `OK`): Benchmark-only parallel WHT, upstream packed butterflies. Fixed nonzero spectral units.
- `packed-wht` (`goldilocks`, config rate `1/4`, `OK`): Benchmark-only parallel WHT, upstream packed butterflies. Fixed nonzero spectral units.
- `packed-wht` (`m127`, config rate `1/2`, `OK`): Benchmark-only parallel WHT, upstream packed butterflies. Fixed nonzero spectral units.
- `packed-wht` (`m127`, config rate `1/4`, `OK`): Benchmark-only parallel WHT, upstream packed butterflies. Fixed nonzero spectral units.
