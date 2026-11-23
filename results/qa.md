# Systematic Quasi-Abelian Codes Benchmark Results

Measurements of systematic Quasi-Abelian codes using [plonky3-binary-qa](https://github.com/jjllzhang/plonky3-binary-qa) (commit `19affa0a`) for characteristic-2 spectral transforms and [HyperFold](https://github.com/jjllzhang/HyperFold) (commit `405b2094`) parallel packed Walsh–Hadamard transforms over Goldilocks and M127.

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`target-cpu=native`); `32T`.
- **Field(s)**: `GF(2^32/64/128)` (+ mixed), Goldilocks, M127.
- **Binary Spectral (`binary-spectral`)**: Supports both same-field (`GF(2^m) -> GF(2^m)`) and subfield-to-extension (`GF(2^32) -> GF(2^64/128)`, `GF(2^64) -> GF(2^128)`) encoding.
- **Prime WHT (`packed-wht`)**: Systematic code `(m, H D_1 H m, ...)` with parallel packed butterflies and fixed nonzero diagonal spectral units.
- **Rates**: `1/2` and `1/4`.

## Measurement Methodology

- **Sampling**: 1 warmup followed by 3 serial runs per configuration; reports both arithmetic mean and median encoding time.
- **Timing & Memory Scope**: `Encode` measures single-polynomial 1D encoding (`K = 2^k` input elements) excluding setup/graph construction (`Setup`), input generation, and Merkle hashing. `Peak RSS` is process peak resident memory (GiB).
- **Missing Values**: `—` denotes unmeasured points that exceed a finite-field/implementation bound or the 420 GiB / 503 GiB memory limit.

## Results

### Binary Spectral QA — GF(2^32) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 3.63 ms | 3.378 ms | 3.383 ms | 0.010 |
| `1/2` | 22 | 14.52 ms | 10.24 ms | 10.15 ms | 0.053 |
| `1/2` | 24 | 57.39 ms | 52.27 ms | 51.32 ms | 0.283 |
| `1/2` | 26 | 229.79 ms | 214.62 ms | 219.60 ms | 1.230 |
| `1/2` | 28 | 889.81 ms | 920.60 ms | 918.69 ms | 4.979 |
| `1/2` | 30 | 3.57 s | 4.037 s | 4.025 s | 19.973 |
| `1/4` | 20 | 10.99 ms | 7.305 ms | 7.306 ms | 0.018 |
| `1/4` | 22 | 43.13 ms | 22.97 ms | 23.09 ms | 0.121 |
| `1/4` | 24 | 172.20 ms | 85.44 ms | 85.01 ms | 0.541 |
| `1/4` | 26 | 677.35 ms | 441.63 ms | 438.57 ms | 2.223 |
| `1/4` | 28 | 2.72 s | 1.961 s | 1.962 s | 8.971 |
| `1/4` | 30 | 10.62 s | 8.415 s | 8.400 s | 35.971 |

### Binary Spectral QA — GF(2^64) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 6.03 ms | 4.607 ms | 4.584 ms | 0.018 |
| `1/2` | 22 | 21.96 ms | 16.54 ms | 16.51 ms | 0.139 |
| `1/2` | 24 | 87.54 ms | 86.08 ms | 84.50 ms | 0.602 |
| `1/2` | 26 | 339.71 ms | 392.51 ms | 391.93 ms | 2.477 |
| `1/2` | 28 | 1.36 s | 1.769 s | 1.770 s | 9.977 |
| `1/2` | 30 | 5.30 s | 7.715 s | 7.724 s | 39.975 |
| `1/4` | 20 | 16.51 ms | 9.435 ms | 9.266 ms | 0.035 |
| `1/4` | 22 | 67.05 ms | 37.30 ms | 36.82 ms | 0.260 |
| `1/4` | 24 | 259.78 ms | 161.22 ms | 160.48 ms | 1.104 |
| `1/4` | 26 | 1.02 s | 795.12 ms | 794.59 ms | 4.473 |
| `1/4` | 28 | 4.06 s | 3.475 s | 3.476 s | 17.979 |
| `1/4` | 30 | 15.85 s | 15.887 s | 15.283 s | 71.973 |

### Binary Spectral QA — GF(2^128) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 10.01 ms | 8.272 ms | 8.304 ms | 0.053 |
| `1/2` | 22 | 38.56 ms | 41.20 ms | 41.31 ms | 0.285 |
| `1/2` | 24 | 150.01 ms | 176.69 ms | 176.29 ms | 1.232 |
| `1/2` | 26 | 580.73 ms | 807.18 ms | 807.67 ms | 4.973 |
| `1/2` | 28 | 2.32 s | 3.531 s | 3.531 s | 19.975 |
| `1/2` | 30 | 9.08 s | 15.412 s | 15.407 s | 79.975 |
| `1/4` | 20 | 29.64 ms | 17.53 ms | 17.21 ms | 0.119 |
| `1/4` | 22 | 117.70 ms | 62.48 ms | 59.87 ms | 0.535 |
| `1/4` | 24 | 441.42 ms | 348.34 ms | 346.44 ms | 2.221 |
| `1/4` | 26 | 1.76 s | 1.595 s | 1.596 s | 8.969 |
| `1/4` | 28 | 6.90 s | 7.020 s | 7.023 s | 35.979 |
| `1/4` | 30 | 27.11 s | 26.181 s | 26.152 s | 143.971 |

### Binary Spectral QA — GF(2^32) -> GF(2^64) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 6.57 ms | 3.688 ms | 3.702 ms | 0.014 |
| `1/2` | 22 | 21.87 ms | 14.10 ms | 14.16 ms | 0.104 |
| `1/2` | 24 | 86.95 ms | 67.33 ms | 66.87 ms | 0.477 |
| `1/2` | 26 | 347.26 ms | 295.60 ms | 294.10 ms | 1.975 |
| `1/2` | 28 | 1.38 s | 1.351 s | 1.348 s | 7.969 |
| `1/2` | 30 | 5.28 s | 5.891 s | 5.867 s | 31.969 |
| `1/4` | 20 | 20.31 ms | 7.905 ms | 7.744 ms | 0.031 |
| `1/4` | 22 | 65.62 ms | 30.60 ms | 31.89 ms | 0.219 |
| `1/4` | 24 | 260.50 ms | 137.24 ms | 134.71 ms | 0.973 |
| `1/4` | 26 | 1.01 s | 657.36 ms | 657.46 ms | 3.977 |
| `1/4` | 28 | 4.04 s | 2.979 s | 2.976 s | 15.975 |
| `1/4` | 30 | 15.63 s | 13.208 s | 13.185 s | 63.969 |

### Binary Spectral QA — GF(2^32) -> GF(2^128) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 11.19 ms | 7.192 ms | 6.767 ms | 0.023 |
| `1/2` | 22 | 40.75 ms | 31.17 ms | 31.77 ms | 0.193 |
| `1/2` | 24 | 155.49 ms | 122.67 ms | 120.49 ms | 0.850 |
| `1/2` | 26 | 603.26 ms | 548.78 ms | 547.75 ms | 3.477 |
| `1/2` | 28 | 2.39 s | 2.479 s | 2.426 s | 13.971 |
| `1/2` | 30 | 9.28 s | 10.457 s | 10.452 s | 55.967 |
| `1/4` | 20 | 32.17 ms | 18.13 ms | 17.82 ms | 0.078 |
| `1/4` | 22 | 116.81 ms | 56.08 ms | 54.45 ms | 0.443 |
| `1/4` | 24 | 454.06 ms | 295.33 ms | 295.10 ms | 1.855 |
| `1/4` | 26 | 1.79 s | 1.353 s | 1.353 s | 7.477 |
| `1/4` | 28 | 7.05 s | 5.962 s | 5.961 s | 29.973 |
| `1/4` | 30 | 27.58 s | 23.708 s | 23.693 s | 119.969 |

### Binary Spectral QA — GF(2^64) -> GF(2^128) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 10.95 ms | 6.040 ms | 6.155 ms | 0.027 |
| `1/2` | 22 | 38.85 ms | 30.80 ms | 31.20 ms | 0.225 |
| `1/2` | 24 | 155.26 ms | 130.34 ms | 131.14 ms | 0.973 |
| `1/2` | 26 | 595.10 ms | 597.12 ms | 599.81 ms | 3.975 |
| `1/2` | 28 | 2.37 s | 2.643 s | 2.643 s | 15.973 |
| `1/2` | 30 | 9.29 s | 11.591 s | 11.586 s | 63.977 |
| `1/4` | 20 | 30.32 ms | 14.31 ms | 14.47 ms | 0.086 |
| `1/4` | 22 | 113.86 ms | 60.41 ms | 60.02 ms | 0.475 |
| `1/4` | 24 | 447.48 ms | 283.99 ms | 282.08 ms | 1.977 |
| `1/4` | 26 | 1.77 s | 1.314 s | 1.309 s | 7.967 |
| `1/4` | 28 | 7.00 s | 5.908 s | 5.891 s | 31.969 |
| `1/4` | 30 | 27.14 s | 21.630 s | 21.602 s | 127.975 |

### Prime Packed WHT QA — Goldilocks (64-bit) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 21.20 ms | 5.203 ms | 5.138 ms | 0.041 |
| `1/2` | 22 | 81.73 ms | 20.80 ms | 20.66 ms | 0.158 |
| `1/2` | 24 | 307.00 ms | 118.75 ms | 117.26 ms | 0.627 |
| `1/2` | 26 | 1.20 s | 671.61 ms | 688.74 ms | 2.502 |
| `1/2` | 28 | 4.82 s | 3.052 s | 3.052 s | 10.002 |
| `1/2` | 30 | 18.63 s | 13.029 s | 12.894 s | 40.002 |
| `1/4` | 20 | 39.69 ms | 9.139 ms | 9.172 ms | 0.072 |
| `1/4` | 22 | 158.05 ms | 36.48 ms | 36.25 ms | 0.283 |
| `1/4` | 24 | 633.43 ms | 235.00 ms | 234.93 ms | 1.127 |
| `1/4` | 26 | 2.52 s | 1.272 s | 1.295 s | 4.502 |
| `1/4` | 28 | 10.02 s | 5.704 s | 5.703 s | 18.002 |
| `1/4` | 30 | 39.22 s | 25.403 s | 25.230 s | 72.002 |

### Prime Packed WHT QA — M127 (2^127 - 1) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 42.97 ms | 10.33 ms | 10.15 ms | 0.080 |
| `1/2` | 22 | 160.47 ms | 41.99 ms | 41.41 ms | 0.314 |
| `1/2` | 24 | 638.20 ms | 268.65 ms | 268.74 ms | 1.252 |
| `1/2` | 26 | 2.46 s | 1.304 s | 1.303 s | 5.002 |
| `1/2` | 28 | 9.62 s | 5.850 s | 5.851 s | 20.000 |
| `1/2` | 30 | 37.90 s | 26.009 s | 26.018 s | 80.002 |
| `1/4` | 20 | 84.63 ms | 19.20 ms | 19.29 ms | 0.143 |
| `1/4` | 22 | 329.66 ms | 79.22 ms | 78.96 ms | 0.564 |
| `1/4` | 24 | 1.30 s | 543.67 ms | 520.73 ms | 2.252 |
| `1/4` | 26 | 5.20 s | 2.624 s | 2.604 s | 9.002 |
| `1/4` | 28 | 20.36 s | 11.422 s | 11.423 s | 36.002 |
| `1/4` | 30 | 83.28 s | 56.234 s | 57.858 s | 144.002 |

## Notes

- In mixed subfield-to-extension rows (e.g., `GF(2^32) -> GF(2^128)`), `2^k` input elements in the smaller subfield are encoded into `2^k / rate` extension-field codeword elements.
- All 96 configurations completed from `k = 20` to `k = 30`.
