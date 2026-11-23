# SPIN Binary Structured Linear Codes Benchmark Results

Measurements of [spin_codes](https://github.com/ladnir/spin_codes) (commit `584a7fb6`) structured binary codes (`IMT` and `Packet-RS8`) over 128-bit binary records (`block128`).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`target-cpu=native`); `1T`.
- **Field(s)**: 128-bit binary blocks.
- **Input Unit**: `2^k` 128-bit binary blocks (`block128`), fixed rate `1/2`.
- **Execution**: Upstream forward single-codeword transform is serial (`1T`).

## Measurement Methodology

- **Sampling**: 1 warmup followed by 3 serial runs per configuration; reports both arithmetic mean and median encoding time.
- **Timing & Memory Scope**: `Encode` measures single-polynomial 1D encoding (`K = 2^k` input elements) excluding setup/graph construction (`Setup`), input generation, and Merkle hashing. `Peak RSS` is process peak resident memory (GiB).
- **Missing Values**: `—` denotes unmeasured points that exceed a finite-field/implementation bound or the 420 GiB / 503 GiB memory limit.

## Results

### SPIN IMT (T128S19) — 128-bit binary blocks (1T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 63.99 ms | 12.71 ms | 12.70 ms | 0.107 |
| `1/2` | 22 | 269.66 ms | 82.08 ms | 82.01 ms | 0.426 |
| `1/2` | 24 | 1.20 s | 361.30 ms | 358.01 ms | 1.785 |
| `1/2` | 26 | 5.03 s | 1.558 s | 1.558 s | 7.135 |
| `1/2` | 28 | 22.07 s | 7.047 s | 7.044 s | 28.533 |
| `1/2` | 30 | 150.43 s | 39.889 s | 39.880 s | 114.127 |

### SPIN Packet-RS8 (PacketRs8T64) — 128-bit binary blocks (1T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 36.71 ms | 8.029 ms | 7.998 ms | 0.102 |
| `1/2` | 22 | 156.05 ms | 35.66 ms | 35.64 ms | 0.385 |
| `1/2` | 24 | 642.69 ms | 146.98 ms | 147.00 ms | 1.539 |
| `1/2` | 26 | 2.60 s | 618.20 ms | 618.28 ms | 6.154 |
| `1/2` | 28 | — | — | — | — |
| `1/2` | 30 | — | — | — | — |

## Notes

- `packet` (`PacketRs8T64`) uses 32-bit internal byte routing offsets and is bounded to `k <= 26`; `imt` (`T128S19`) scales to `k = 30`.
