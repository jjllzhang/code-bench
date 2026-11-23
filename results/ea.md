# Explicit Expand–Accumulate (EA) Benchmark Results

Measurements of explicit sparse-matrix Expand–Accumulate encoders from the ERA codebase and the [CRYPTO '24 EACode artifact](https://artifacts.iacr.org/crypto/2024/a10/).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`target-cpu=native`); `32T`.
- **Field(s)**: Goldilocks, `secp256k1`, `Ristretto255`.
- **Construction**: Expands a `2^k`-element message via an explicit sparse bipartite matrix `E` of size `N × 2^k`, followed by sequential accumulation.
- **Rates**: `1/2` and `1/4`.

## Measurement Methodology

- **Sampling**: 1 warmup followed by 3 measured runs per configuration; reports both arithmetic mean and median encoding time.
- **Timing Scope**: `Encode` measures encoding time for `K = 2^k` input elements, excluding `Setup` and input generation. `Peak RSS` is process peak resident memory (GiB).
- **Missing Values**: `—` denotes unmeasured points that exceed a finite-field/implementation bound or the 420 GiB / 503 GiB memory limit.

## Results

### Explicit Sparse-Matrix EA — Goldilocks (64-bit) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 5.39 s | 137.95 ms | 138.02 ms | 8.869 |
| `1/2` | 22 | 22.89 s | 1.369 s | 1.369 s | 38.900 |
| `1/2` | 24 | 103.17 s | 7.717 s | 7.712 s | 169.104 |
| `1/2` | 26 | — | — | — | — |
| `1/2` | 28 | — | — | — | — |
| `1/2` | 30 | — | — | — | — |
| `1/4` | 20 | 5.66 s | 148.32 ms | 148.20 ms | 9.291 |
| `1/4` | 22 | 23.99 s | 1.447 s | 1.447 s | 40.658 |
| `1/4` | 24 | 107.86 s | 8.012 s | 8.008 s | 176.098 |
| `1/4` | 26 | — | — | — | — |
| `1/4` | 28 | — | — | — | — |
| `1/4` | 30 | — | — | — | — |

### Explicit Sparse-Matrix EA — secp256k1 Fr (256-bit) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 91.47 s | 1.495 s | 1.496 s | 17.803 |
| `1/2` | 22 | 400.09 s | 8.930 s | 8.930 s | 77.984 |
| `1/2` | 24 | 1778.43 s | 42.984 s | 43.008 s | 338.971 |
| `1/2` | 26 | — | — | — | — |
| `1/2` | 28 | — | — | — | — |
| `1/2` | 30 | — | — | — | — |
| `1/4` | 20 | 96.44 s | 1.581 s | 1.584 s | 18.715 |
| `1/4` | 22 | 417.63 s | 9.397 s | 9.410 s | 81.611 |
| `1/4` | 24 | 1838.10 s | 43.663 s | 43.684 s | 353.469 |
| `1/4` | 26 | — | — | — | — |
| `1/4` | 28 | — | — | — | — |
| `1/4` | 30 | — | — | — | — |

### CRYPTO'24 EACode EA — Ristretto255 Fr (253-bit) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 55.10 s | 1.383 s | 1.383 s | 17.809 |
| `1/2` | 22 | 237.97 s | 8.603 s | 8.616 s | 77.994 |
| `1/2` | 24 | 1046.68 s | 39.823 s | 39.823 s | 338.973 |
| `1/2` | 26 | — | — | — | — |
| `1/2` | 28 | — | — | — | — |
| `1/2` | 30 | — | — | — | — |
| `1/4` | 20 | 58.30 s | 1.458 s | 1.459 s | 18.709 |
| `1/4` | 22 | 251.79 s | 9.012 s | 9.005 s | 81.615 |
| `1/4` | 24 | 1108.53 s | 41.378 s | 41.377 s | 353.471 |
| `1/4` | 26 | — | — | — | — |
| `1/4` | 28 | — | — | — | — |
| `1/4` | 30 | — | — | — | — |

## Notes

- Explicitly storing the sparse matrix `E` requires memory growing super-linearly with `k` (~730 GiB+ lower bound at `k = 26` for Goldilocks, ~1,464 GiB+ for 256-bit curves), so `k >= 26` could not run within the host's 503 GiB RAM.
