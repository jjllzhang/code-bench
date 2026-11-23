# Lightning (LDPC Sketch + Brakedown Inner Code) Benchmark Results

Measurements of [Lightning](https://github.com/quwenjie/Lightning) (commit `08dbd81b`) 1D LDPC-sketch + Brakedown inner code over `BN254` scalar field (`mcl`).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`target-cpu=native`); `1T`.
- **Field(s)**: `u64 -> BN254 Fr`.
- **Representation**: `64-bit` integer message inputs (`u64`) with `254-bit` `BN254` parity symbols (`32 B`), executed single-threaded (`1T`).
- **Rates**: `native-high` (degree `10`, sketch fraction `~0.198`, actual rate `0.667–0.781`), `native-low` (degree `9`, sketch fraction `~0.417`, actual rate `0.607–0.628`), and `half` (tuned to actual rate `0.500`, sketch fraction `~0.70`).

## Measurement Methodology

- **Sampling**: 1 warmup followed by 3 serial runs per configuration; reports both arithmetic mean and median encoding time.
- **Timing & Memory Scope**: `Encode` measures single-polynomial 1D encoding (`K = 2^k` input elements) excluding setup/graph construction (`Setup`), input generation, and Merkle hashing. `Peak RSS` is process peak resident memory (GiB).
- **Missing Values**: `—` denotes unmeasured points that exceed a finite-field/implementation bound or the 420 GiB / 503 GiB memory limit.

## Results

### Lightning LDPC + Brakedown — BN254 Fr (254-bit) (1T)

| Config Rate | Actual Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|---:|
| `half` | 0.5000 | 20 | 1.58 s | 922.04 ms | 920.16 ms | 0.445 |
| `half` | 0.5000 | 22 | 7.36 s | 6.404 s | 6.413 s | 1.912 |
| `half` | 0.5000 | 24 | 32.20 s | 36.003 s | 35.987 s | 7.639 |
| `half` | 0.5000 | 26 | 137.79 s | 163.94 s | 164.01 s | 30.830 |
| `half` | 0.5000 | 28 | 562.23 s | 871.51 s | 881.49 s | 123.453 |
| `half` | — | 30 | — | — | — | — |
| `native-high` | 0.6667 | 20 | 95.08 ms | 579.22 ms | 576.48 ms | 0.119 |
| `native-high` | 0.7633 | 22 | 2.13 s | 3.305 s | 3.304 s | 0.730 |
| `native-high` | 0.7782 | 24 | 10.41 s | 22.448 s | 22.453 s | 3.053 |
| `native-high` | 0.7782 | 26 | 50.14 s | 108.87 s | 109.49 s | 12.201 |
| `native-high` | 0.7805 | 28 | 215.47 s | 468.51 s | 468.21 s | 49.055 |
| `native-high` | 0.7805 | 30 | 921.64 s | 2795.20 s | 2790.72 s | 196.350 |
| `native-low` | 0.6074 | 20 | 974.85 ms | 605.12 ms | 606.49 ms | 0.299 |
| `native-low` | 0.6074 | 22 | 4.05 s | 4.947 s | 4.944 s | 1.188 |
| `native-low` | 0.6253 | 24 | 20.03 s | 27.469 s | 27.469 s | 5.043 |
| `native-low` | 0.6277 | 26 | 87.97 s | 130.21 s | 130.23 s | 20.301 |
| `native-low` | 0.6277 | 28 | 361.78 s | 608.27 s | 608.18 s | 81.195 |
| `native-low` | 0.6281 | 30 | 1525.72 s | 3574.20 s | 3567.62 s | 325.037 |

## Notes

- The upstream C++ 1D path is single-threaded (`1T`).
- At `k = 30`, rate `1/2` (`half`) exceeded the 420 GiB per-process cap.
