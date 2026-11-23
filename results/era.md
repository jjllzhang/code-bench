# ERA (Encode–Repeat–Accumulate) Benchmark Results

Measurements of the ERA (`Encode–Repeat–Accumulate`) encoder over Goldilocks and `secp256k1` scalar fields.

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`target-cpu=native`); `32T`.
- **Field(s)**: Goldilocks, `secp256k1`.
- **Structure**: Inner Brakedown base code (`rho_B = 1 / 1.05`, `alpha = 0.04`, `c_n = 8`, `d_n = 64`), followed by `2×` or `4×` repetition and two rounds of permutation, diagonal scaling, and prefix accumulation.
- **Actual Code Rates**: Repetition `2` yields actual rate `20/42 ≈ 0.4762` (labeled `1/2`); repetition `4` yields actual rate `20/84 ≈ 0.2381` (labeled `1/4`).

## Measurement Methodology

- **Sampling**: 1 warmup followed by 3 serial runs per configuration; reports both arithmetic mean and median encoding time.
- **Timing & Memory Scope**: `Encode` measures pure encoding time for `K = 2^k` input elements, excluding setup/graph construction (`Setup`), input generation, and Merkle hashing. `Peak RSS` is process peak resident memory (GiB).
- **Missing Values**: `—` denotes unmeasured points that exceed a finite-field/implementation bound or the 420 GiB / 503 GiB memory limit.

## Results

### ERA (1.05x Brakedown + Repeat-Accumulate) — Goldilocks (64-bit) (32T)

| Config Rate | Actual Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|---:|
| `1/2` | 0.4762 | 20 | 563.99 ms | 14.76 ms | 14.39 ms | 0.328 |
| `1/2` | 0.4762 | 22 | 3.07 s | 78.03 ms | 78.00 ms | 1.307 |
| `1/2` | 0.4762 | 24 | 14.90 s | 348.46 ms | 348.40 ms | 5.225 |
| `1/2` | 0.4762 | 26 | 72.33 s | 1.418 s | 1.416 s | 20.898 |
| `1/2` | 0.4762 | 28 | 318.71 s | 8.144 s | 8.236 s | 83.588 |
| `1/2` | 0.4762 | 30 | 1530.49 s | 24.758 s | 24.576 s | 317.543 |
| `1/4` | 0.2381 | 20 | 681.90 ms | 20.92 ms | 20.93 ms | 0.441 |
| `1/4` | 0.2381 | 22 | 3.69 s | 134.70 ms | 134.83 ms | 1.768 |
| `1/4` | 0.2381 | 24 | 17.38 s | 521.73 ms | 525.53 ms | 7.061 |
| `1/4` | 0.2381 | 26 | 84.10 s | 2.257 s | 2.221 s | 28.248 |
| `1/4` | 0.2381 | 28 | 365.38 s | 10.806 s | 10.796 s | 112.986 |
| `1/4` | — | 30 | — | — | — | — |

### ERA (1.05x Brakedown + Repeat-Accumulate) — secp256k1 Fr (256-bit) (32T)

| Config Rate | Actual Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|---:|
| `1/2` | 0.4762 | 20 | 4.75 s | 75.49 ms | 72.93 ms | 0.850 |
| `1/2` | 0.4762 | 22 | 25.13 s | 418.11 ms | 415.95 ms | 3.658 |
| `1/2` | 0.4762 | 24 | 103.94 s | 1.426 s | 1.411 s | 13.578 |
| `1/2` | 0.4762 | 26 | 476.99 s | 6.541 s | 6.478 s | 54.307 |
| `1/2` | 0.4762 | 28 | 2074.46 s | 25.992 s | 25.825 s | 217.217 |
| `1/2` | — | 30 | — | — | — | — |
| `1/4` | 0.2381 | 20 | 5.76 s | 115.56 ms | 110.87 ms | 1.178 |
| `1/4` | 0.2381 | 22 | 29.18 s | 542.62 ms | 535.48 ms | 4.707 |
| `1/4` | 0.2381 | 24 | 120.69 s | 1.782 s | 1.774 s | 18.828 |
| `1/4` | 0.2381 | 26 | 549.34 s | 7.701 s | 7.695 s | 75.307 |
| `1/4` | 0.2381 | 28 | 2367.60 s | 30.520 s | 30.411 s | 301.219 |
| `1/4` | — | 30 | — | — | — | — |

## Notes

- At `k = 30`, Goldilocks rate `1/4` hit the 420 GiB per-process cap, and `secp256k1` was skipped prior to launch (`> 645 GiB` lower bound for stored graph and permutation tables).
