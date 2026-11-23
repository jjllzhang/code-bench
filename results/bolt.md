# Bolt Sketched Codes Benchmark Results

Measurements of [bolt-rs](https://github.com/bcc-research/bolt-rs) (commit `3832e47b`) sketched linear codes (`bolt-xor` and `bolt32`) over `GF(2^32)`.

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`target-cpu=native`); `32T`.
- **Field(s)**: `GF(2^32)`.
- **Construction**: Systematic `K`-element message concatenated with an LDPC-like expander sketch (`left_degree = 8`, `right_degree = 64`) encoded by an inner RS code of inverse rate `2` or `4`.
- **Actual Code Rates**: Inner RS rate `1/2` gives overall codeword length `5K / 4` (`actual_rate = 0.8000`); inner RS rate `1/4` gives `3K / 2` (`actual_rate = 0.6667`).

## Measurement Methodology

- **Sampling**: 1 warmup followed by 3 measured runs per configuration; reports both arithmetic mean and median encoding time.
- **Timing Scope**: `Encode` measures encoding time for `K = 2^k` input elements, excluding `Setup` and input generation. `Peak RSS` is process peak resident memory (GiB).
- **Missing Values**: `—` denotes unmeasured points that exceed a finite-field/implementation bound or the 420 GiB / 503 GiB memory limit.

## Results

### Bolt-XOR (Inner RS 1/2 & 1/4) — GF(2^32) (32T)

| Config Rate | Actual Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|---:|
| `1/2` | 0.8000 | 20 | 205.81 ms | 81.82 ms | 81.64 ms | 0.150 |
| `1/2` | 0.8000 | 22 | 1.01 s | 325.66 ms | 324.77 ms | 0.576 |
| `1/2` | 0.8000 | 24 | 4.87 s | 1.311 s | 1.307 s | 2.268 |
| `1/2` | 0.8000 | 26 | 20.87 s | 5.045 s | 5.030 s | 9.064 |
| `1/2` | 0.8000 | 28 | 86.22 s | 20.559 s | 20.561 s | 36.252 |
| `1/2` | 0.8000 | 30 | 383.16 s | 80.798 s | 80.809 s | 145.002 |
| `1/4` | 0.6667 | 20 | 208.79 ms | 85.79 ms | 85.84 ms | 0.156 |
| `1/4` | 0.6667 | 22 | 1.01 s | 345.39 ms | 343.58 ms | 0.592 |
| `1/4` | 0.6667 | 24 | 4.87 s | 1.398 s | 1.392 s | 2.361 |
| `1/4` | 0.6667 | 26 | 21.00 s | 5.577 s | 5.574 s | 9.439 |
| `1/4` | 0.6667 | 28 | 86.78 s | 22.460 s | 22.341 s | 37.752 |
| `1/4` | 0.6667 | 30 | 381.73 s | 87.470 s | 87.329 s | 151.002 |

### Bolt32 (Inner RS 1/2 & 1/4) — GF(2^32) (32T)

| Config Rate | Actual Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|---:|
| `1/2` | 0.8000 | 20 | 473.09 ms | 80.91 ms | 80.28 ms | 0.197 |
| `1/2` | 0.8000 | 22 | 2.03 s | 320.89 ms | 320.88 ms | 0.785 |
| `1/2` | 0.8000 | 24 | 8.43 s | 1.388 s | 1.390 s | 3.143 |
| `1/2` | 0.8000 | 26 | 34.98 s | 5.360 s | 5.356 s | 12.564 |
| `1/2` | 0.8000 | 28 | 157.76 s | 20.879 s | 20.863 s | 50.252 |
| `1/2` | 0.8000 | 30 | 606.87 s | 82.234 s | 82.041 s | 201.002 |
| `1/4` | 0.6667 | 20 | 471.66 ms | 86.43 ms | 86.50 ms | 0.197 |
| `1/4` | 0.6667 | 22 | 2.04 s | 346.26 ms | 345.73 ms | 0.787 |
| `1/4` | 0.6667 | 24 | 8.48 s | 1.407 s | 1.398 s | 3.143 |
| `1/4` | 0.6667 | 26 | 35.18 s | 5.712 s | 5.713 s | 12.564 |
| `1/4` | 0.6667 | 28 | 158.22 s | 22.884 s | 22.831 s | 50.252 |
| `1/4` | 0.6667 | 30 | 615.49 s | 92.325 s | 92.193 s | 201.002 |

## Notes

- Because Bolt outputs systematic input plus inner RS parity, its actual code rate (`0.800` / `0.667`) is higher than the inner RS rate (`1/2` / `1/4`).
