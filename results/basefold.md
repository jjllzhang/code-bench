# BaseFold Random Foldable Codes Benchmark Results

Measurements of [plonkish_basefold](https://github.com/hadasz/plonkish_basefold) (commit `c29f0865`) random foldable codes (`r = 2`) initialized from a Reed–Solomon base code of message length `64`.

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`target-cpu=native`); `32T`.
- **Field(s)**: Goldilocks (`16B`), M127.
- **Base Code & Folding**: Message length `64` RS base code followed by `k - 6` binary folding rounds (`r = 2`) with random diagonal multipliers.
- **Element Storage**: Both `M127` and `Goldilocks` use `plonkish_basefold`'s native 16-byte representation.

## Measurement Methodology

- **Sampling**: 1 warmup followed by 3 serial runs per configuration; reports both arithmetic mean and median encoding time.
- **Timing & Memory Scope**: `Encode` measures pure encoding time for `K = 2^k` input elements, excluding setup/graph construction (`Setup`), input generation, and Merkle hashing. `Peak RSS` is process peak resident memory (GiB).
- **Missing Values**: `—` denotes unmeasured points that exceed a finite-field/implementation bound or the 420 GiB / 503 GiB memory limit.

## Results

### RS-64 Random Foldable Code (r = 2) — Goldilocks (64-bit) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 381.20 ms | 117.92 ms | 115.75 ms | 0.211 |
| `1/2` | 22 | 1.51 s | 492.49 ms | 471.89 ms | 0.979 |
| `1/2` | 24 | 6.87 s | 2.112 s | 2.113 s | 3.971 |
| `1/2` | 26 | 27.50 s | 9.398 s | 9.300 s | 15.975 |
| `1/2` | 28 | 110.29 s | 48.213 s | 47.682 s | 63.977 |
| `1/2` | 30 | 461.98 s | 194.03 s | 193.74 s | 255.982 |
| `1/4` | 20 | 751.65 ms | 227.84 ms | 220.68 ms | 0.459 |
| `1/4` | 22 | 3.25 s | 996.56 ms | 985.89 ms | 1.910 |
| `1/4` | 24 | 13.96 s | 4.369 s | 4.373 s | 7.725 |
| `1/4` | 26 | 58.31 s | 21.699 s | 21.283 s | 30.975 |
| `1/4` | 28 | 219.04 s | 109.49 s | 110.20 s | 123.965 |
| `1/4` | 30 | — | — | — | — |

### RS-64 Random Foldable Code (r = 2) — M127 (2^127 - 1) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 395.12 ms | 138.11 ms | 139.05 ms | 0.230 |
| `1/2` | 22 | 1.61 s | 436.87 ms | 421.68 ms | 1.037 |
| `1/2` | 24 | 7.14 s | 1.875 s | 1.876 s | 4.219 |
| `1/2` | 26 | 26.81 s | 8.336 s | 8.215 s | 16.973 |
| `1/2` | 28 | 109.45 s | 42.525 s | 42.269 s | 67.975 |
| `1/2` | 30 | 478.66 s | 175.86 s | 175.71 s | 271.977 |
| `1/4` | 20 | 784.24 ms | 188.31 ms | 179.99 ms | 0.486 |
| `1/4` | 22 | 3.39 s | 815.16 ms | 793.77 ms | 2.035 |
| `1/4` | 24 | 14.10 s | 3.571 s | 3.516 s | 8.225 |
| `1/4` | 26 | 57.77 s | 15.078 s | 14.844 s | 32.977 |
| `1/4` | 28 | 231.38 s | 79.169 s | 79.369 s | 131.973 |
| `1/4` | 30 | — | — | — | — |

## Notes

- `Goldilocks` elements occupy 16 bytes in `plonkish_basefold` (compared with 8 bytes in Plonky3 and HyperFold).
- At rate `1/4` and `k = 30`, Goldilocks hit the 420 GiB per-process memory cap, while M127 hit the upstream AES-CTR32 table block limit (`2^32` blocks).
