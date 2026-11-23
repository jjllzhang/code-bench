# Brakedown / Generalized Spielman Expander Codes Benchmark Results

Measurements of recursive sparse-expander Brakedown codes across four implementations: parallel recursive Brakedown (ERA codebase), [bolt-rs](https://github.com/bcc-research/bolt-rs) (`3832e47b`), [lcpc](https://github.com/conroi/lcpc) (`f0e21160`), and [plonkish_basefold](https://github.com/hadasz/plonkish_basefold) (`c29f0865`).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`target-cpu=native`); `32T / 1T`.
- **Field(s)**: Goldilocks, M127, `Ft127`, `secp256k1`, `GF(2^32)`.
- **`brakedown-recursive`** (`32T`): `alpha = 0.3`, `c_n = 14`, `d_n = 28`, rates `1/2` and `1/4`.
- **`bolt-binary`** (`32T`, `GF(2^32)`): `alpha = 0.238`, `c_n = 13`, `d_n = 14`, `base_limit = 64`; tested at rates `1/2`, `1/4`, and native ratios (`~0.674`, `~0.506`).
- **`plonkish-sdig3`** (`1T`): Native `BrakedownSpec3` (`rate ≈ 0.6574`, `base_limit = 128`, 16-byte elements for both Goldilocks and M127).
- **`sdig2` / `sdig3`** (`1T`, `Ft127`): Native `lcpc` generalized Spielman profiles (`rate ≈ 0.6803` and `0.6575`).

## Measurement Methodology

- **Sampling**: 1 warmup followed by 3 measured runs per configuration; reports both arithmetic mean and median encoding time.
- **Timing Scope**: `Encode` measures encoding time for `K = 2^k` input elements, excluding `Setup` and input generation. `Peak RSS` is process peak resident memory (GiB).
- **Missing Values**: `—` denotes unmeasured points that exceed a finite-field/implementation bound or the 420 GiB / 503 GiB memory limit.

## Results

### Recursive Brakedown — Goldilocks (64-bit) (32T)

| Config Rate | Actual Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|---:|
| `1/2` | 0.5000 | 20 | 3.47 s | 16.88 ms | 16.83 ms | 0.941 |
| `1/2` | 0.5000 | 22 | 16.66 s | 101.69 ms | 101.68 ms | 3.760 |
| `1/2` | 0.5000 | 24 | 78.00 s | 670.76 ms | 670.26 ms | 15.037 |
| `1/2` | 0.5000 | 26 | 350.11 s | 3.240 s | 3.240 s | 60.156 |
| `1/2` | 0.5000 | 28 | 1590.86 s | 17.899 s | 18.029 s | 240.594 |
| `1/2` | — | 30 | — | — | — | — |
| `1/4` | 0.2500 | 20 | 7.20 s | 26.57 ms | 26.68 ms | 1.711 |
| `1/4` | 0.2500 | 22 | 32.89 s | 196.68 ms | 196.72 ms | 6.842 |
| `1/4` | 0.2500 | 24 | 151.64 s | 1.155 s | 1.155 s | 27.365 |
| `1/4` | 0.2500 | 26 | 687.38 s | 5.345 s | 5.342 s | 109.451 |
| `1/4` | — | 28 | — | — | — | — |
| `1/4` | — | 30 | — | — | — | — |

### Recursive Brakedown — secp256k1 Fr (256-bit) (32T)

| Config Rate | Actual Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|---:|
| `1/2` | 0.5000 | 20 | 19.47 s | 131.90 ms | 130.72 ms | 2.322 |
| `1/2` | 0.5000 | 22 | 92.21 s | 815.02 ms | 815.75 ms | 9.283 |
| `1/2` | 0.5000 | 24 | 418.91 s | 3.934 s | 3.909 s | 37.127 |
| `1/2` | 0.5000 | 26 | 1806.61 s | 16.901 s | 16.831 s | 148.500 |
| `1/2` | — | 28 | — | — | — | — |
| `1/2` | — | 30 | — | — | — | — |
| `1/4` | 0.2500 | 20 | 34.67 s | 234.02 ms | 234.00 ms | 4.123 |
| `1/4` | 0.2500 | 22 | 157.35 s | 1.356 s | 1.353 s | 16.484 |
| `1/4` | 0.2500 | 24 | 694.12 s | 5.999 s | 5.995 s | 65.936 |
| `1/4` | 0.2500 | 26 | 3210.08 s | 27.191 s | 26.827 s | 263.727 |
| `1/4` | — | 28 | — | — | — | — |
| `1/4` | — | 30 | — | — | — | — |

### Bolt Binary Brakedown — GF(2^32) (32T)

| Config Rate | Actual Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|---:|
| `1/2` | 0.5000 | 20 | 1.60 s | 507.18 ms | 506.60 ms | 0.543 |
| `1/2` | 0.5000 | 22 | 6.98 s | 2.263 s | 2.268 s | 2.170 |
| `1/2` | 0.5000 | 24 | 29.33 s | 9.364 s | 9.312 s | 8.676 |
| `1/2` | 0.5000 | 26 | 121.73 s | 37.946 s | 38.033 s | 34.699 |
| `1/2` | 0.5000 | 28 | 549.96 s | 154.46 s | 153.91 s | 138.795 |
| `1/2` | — | 30 | — | — | — | — |
| `1/4` | 0.2500 | 20 | 2.07 s | 1.398 s | 1.398 s | 0.789 |
| `1/4` | 0.2500 | 22 | 8.91 s | 6.322 s | 6.371 s | 3.148 |
| `1/4` | 0.2500 | 24 | 37.55 s | 26.546 s | 26.616 s | 12.590 |
| `1/4` | 0.2500 | 26 | 157.48 s | 109.95 s | 110.22 s | 50.357 |
| `1/4` | 0.2500 | 28 | 753.45 s | 463.40 s | 458.69 s | 201.428 |
| `1/4` | — | 30 | — | — | — | — |
| `native-high` | 0.6740 | 20 | 1.55 s | 290.79 ms | 291.02 ms | 0.516 |
| `native-high` | 0.6740 | 22 | 6.80 s | 1.184 s | 1.187 s | 2.062 |
| `native-high` | 0.6740 | 24 | 28.81 s | 4.912 s | 4.927 s | 8.242 |
| `native-high` | 0.6740 | 26 | 119.14 s | 19.526 s | 19.524 s | 32.967 |
| `native-high` | 0.6740 | 28 | 532.47 s | 79.073 s | 79.121 s | 131.867 |
| `native-high` | — | 30 | — | — | — | — |
| `native-low` | 0.5060 | 20 | 1.58 s | 515.61 ms | 515.08 ms | 0.537 |
| `native-low` | 0.5060 | 22 | 6.96 s | 2.195 s | 2.211 s | 2.141 |
| `native-low` | 0.5060 | 24 | 29.16 s | 9.134 s | 9.141 s | 8.562 |
| `native-low` | 0.5060 | 26 | 122.02 s | 36.736 s | 36.265 s | 34.242 |
| `native-low` | 0.5060 | 28 | 549.08 s | 152.97 s | 152.62 s | 136.969 |
| `native-low` | — | 30 | — | — | — | — |

### Plonkish BrakedownSpec3 (16B elem) — Goldilocks (64-bit) (1T)

| Config Rate | Actual Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|---:|
| `native` | 0.6575 | 20 | 959.05 ms | 228.85 ms | 228.54 ms | 0.422 |
| `native` | 0.6575 | 22 | 3.71 s | 1.287 s | 1.282 s | 1.646 |
| `native` | 0.6575 | 24 | 14.87 s | 8.284 s | 8.273 s | 6.561 |
| `native` | 0.6575 | 26 | 58.90 s | 39.653 s | 39.668 s | 26.178 |
| `native` | 0.6575 | 28 | 234.78 s | 166.28 s | 166.28 s | 104.666 |
| `native` | — | 30 | — | — | — | — |

### Plonkish BrakedownSpec3 (16B elem) — M127 (2^127 - 1) (1T)

| Config Rate | Actual Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|---:|
| `native` | 0.6575 | 20 | 1.02 s | 239.61 ms | 238.17 ms | 0.424 |
| `native` | 0.6575 | 22 | 3.97 s | 1.326 s | 1.326 s | 1.646 |
| `native` | 0.6575 | 24 | 15.76 s | 8.338 s | 8.335 s | 6.561 |
| `native` | 0.6575 | 26 | 62.85 s | 39.933 s | 39.935 s | 26.178 |
| `native` | 0.6575 | 28 | 250.56 s | 169.12 s | 169.12 s | 104.666 |
| `native` | — | 30 | — | — | — | — |

### lcpc SdigCode2 — Ft127 (127-bit) (1T)

| Config Rate | Actual Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|---:|
| `native` | 0.6803 | 20 | 1.15 s | 350.68 ms | 334.90 ms | 0.391 |
| `native` | 0.6803 | 22 | 4.44 s | 2.050 s | 2.053 s | 1.549 |
| `native` | 0.6803 | 24 | 17.89 s | 12.747 s | 13.008 s | 6.195 |
| `native` | 0.6803 | 26 | 71.22 s | 59.314 s | 59.376 s | 24.795 |
| `native` | 0.6803 | 28 | 287.05 s | 253.89 s | 254.07 s | 99.174 |
| `native` | 0.6803 | 30 | 1160.12 s | 1198.51 s | 1198.88 s | 396.701 |

### lcpc SdigCode3 — Ft127 (127-bit) (1T)

| Config Rate | Actual Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|---:|
| `native` | 0.6575 | 20 | 1.23 s | 404.03 ms | 384.51 ms | 0.436 |
| `native` | 0.6575 | 22 | 4.67 s | 2.297 s | 2.310 s | 1.703 |
| `native` | 0.6575 | 24 | 18.64 s | 14.139 s | 14.315 s | 6.809 |
| `native` | 0.6575 | 26 | 74.62 s | 65.779 s | 65.866 s | 27.195 |
| `native` | 0.6575 | 28 | 303.51 s | 287.00 s | 286.90 s | 108.748 |
| `native` | — | 30 | — | — | — | — |

## Notes

- `plonkish-sdig3`, `sdig2`, and `sdig3` are single-threaded (`1T`); `brakedown-recursive` and `bolt-binary` use `32` threads.
- Expander graph storage causes `k = 30` (and `k = 28` for `secp256k1` / Goldilocks `1/4`) to exceed the 420–503 GiB memory budget, except `lcpc` `sdig2` over `Ft127` (`396.7 GiB` RSS).
