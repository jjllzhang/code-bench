# Reed–Solomon (Multiplicative NTT Coset LDE) Benchmark Results

Measurements of [Plonky3](https://github.com/Plonky3/Plonky3) (`p3-dft` `Radix2DitParallel`, commit `0d803737`) multiplicative NTT coset low-degree extension from subgroup evaluations.

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`target-cpu=native`); `32T`.
- **Field(s)**: Goldilocks, BabyBear.
- **Input Representation**: Evaluations on a multiplicative subgroup of size `2^k`.
- **Rates**: `1/2` and `1/4`.

## Measurement Methodology

- **Sampling**: 1 warmup followed by 3 serial runs per configuration; reports both arithmetic mean and median encoding time.
- **Timing & Memory Scope**: `Encode` measures pure encoding time for `K = 2^k` input elements, excluding setup/graph construction (`Setup`), input generation, and Merkle hashing. `Peak RSS` is process peak resident memory (GiB).
- **Missing Values**: `—` denotes unmeasured points that exceed a finite-field/implementation bound or the 420 GiB / 503 GiB memory limit.

## Results

### Plonky3 Radix-2 DIT Coset LDE — Goldilocks (64-bit) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 10.81 ms | 16.77 ms | 16.91 ms | 0.029 |
| `1/2` | 22 | 33.97 ms | 80.13 ms | 81.06 ms | 0.172 |
| `1/2` | 24 | 125.10 ms | 258.67 ms | 258.67 ms | 0.729 |
| `1/2` | 26 | 482.50 ms | 966.56 ms | 961.18 ms | 2.975 |
| `1/2` | 28 | 1.83 s | 3.831 s | 3.832 s | 11.975 |
| `1/2` | 30 | 7.63 s | 17.053 s | 16.699 s | 47.975 |
| `1/4` | 20 | 12.79 ms | 22.74 ms | 22.42 ms | 0.051 |
| `1/4` | 22 | 42.50 ms | 92.53 ms | 91.34 ms | 0.293 |
| `1/4` | 24 | 149.73 ms | 290.07 ms | 290.03 ms | 1.223 |
| `1/4` | 26 | 590.16 ms | 1.178 s | 1.174 s | 4.979 |
| `1/4` | 28 | 2.30 s | 5.153 s | 5.153 s | 19.971 |
| `1/4` | 30 | 9.42 s | 21.364 s | 21.421 s | 79.969 |

### Plonky3 Radix-2 DIT Coset LDE — BabyBear (31-bit) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 7.66 ms | 26.56 ms | 26.61 ms | 0.016 |
| `1/2` | 22 | 19.44 ms | 84.23 ms | 84.26 ms | 0.062 |
| `1/2` | 24 | 70.67 ms | 335.04 ms | 334.70 ms | 0.352 |
| `1/2` | 26 | 263.72 ms | 1.371 s | 1.364 s | 1.469 |
| `1/2` | 28 | — | — | — | — |
| `1/2` | 30 | — | — | — | — |
| `1/4` | 20 | 7.61 ms | 32.66 ms | 32.78 ms | 0.023 |
| `1/4` | 22 | 20.81 ms | 116.83 ms | 115.84 ms | 0.137 |
| `1/4` | 24 | 79.47 ms | 492.88 ms | 487.07 ms | 0.600 |
| `1/4` | 26 | — | — | — | — |
| `1/4` | 28 | — | — | — | — |
| `1/4` | 30 | — | — | — | — |

## Notes

- BabyBear (`31-bit`) has a 2-adic subgroup order limit of `2^27`, capping codeword length `N = 2^k / rate <= 2^27` (`k <= 26` at rate `1/2`, `k <= 24` at rate `1/4`).
