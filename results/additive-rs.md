# Binary Additive Reed–Solomon Benchmark Results

Measurements of additive-NTT Reed–Solomon encoders over binary tower fields: [Plonky3](https://github.com/Plonky3/Plonky3) (`p3-binary-dft`, commit `0d803737`) LCH14 and polynomial-basis encoders (`32T`), alongside [bolt-rs](https://github.com/bcc-research/bolt-rs) (commit `3832e47b`) (`1T`).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`target-cpu=native`); `32T / 1T`.
- **Field(s)**: `GF(2^32)`, `GF(2^64)`, `GF(2^128)`.
- **`lch`**: Plonky3 Lin–Chung–Han additive NTT (`GF(2^32)`, `GF(2^64)`, `GF(2^128)`).
- **`polybasis`**: Plonky3 `PolyBasisNtt` (supports `GF(2^128)` only).
- **`bolt-rs`**: `bolt-rs` `ReedSolomonEncoding` encoder (`1T`).

## Measurement Methodology

- **Sampling**: 1 warmup followed by 3 measured runs per configuration; reports both arithmetic mean and median encoding time.
- **Timing Scope**: `Encode` measures encoding time for `K = 2^k` input elements, excluding `Setup` and input generation. `Peak RSS` is process peak resident memory (GiB).
- **Missing Values**: `—` denotes unmeasured points that exceed a finite-field/implementation bound or the 420 GiB / 503 GiB memory limit.

## Results

### Plonky3 PolyBasis NTT — GF(2^128) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | <0.01 ms | 4.483 ms | 4.470 ms | 0.049 |
| `1/2` | 22 | <0.01 ms | 27.21 ms | 28.31 ms | 0.188 |
| `1/2` | 24 | <0.01 ms | 81.54 ms | 79.70 ms | 0.752 |
| `1/2` | 26 | <0.01 ms | 371.01 ms | 370.90 ms | 3.002 |
| `1/2` | 28 | <0.01 ms | 1.125 s | 1.115 s | 12.002 |
| `1/2` | 30 | <0.01 ms | 4.245 s | 4.234 s | 47.998 |
| `1/4` | 20 | <0.01 ms | 7.536 ms | 7.405 ms | 0.078 |
| `1/4` | 22 | <0.01 ms | 51.52 ms | 51.21 ms | 0.314 |
| `1/4` | 24 | <0.01 ms | 168.26 ms | 168.14 ms | 1.252 |
| `1/4` | 26 | <0.01 ms | 685.71 ms | 687.35 ms | 5.002 |
| `1/4` | 28 | <0.01 ms | 2.089 s | 2.090 s | 19.994 |
| `1/4` | 30 | <0.01 ms | 7.998 s | 7.992 s | 79.998 |

### Plonky3 LCH14 Additive NTT — GF(2^32) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | <0.01 ms | 6.872 ms | 6.930 ms | 0.006 |
| `1/2` | 22 | <0.01 ms | 20.56 ms | 20.65 ms | 0.018 |
| `1/2` | 24 | <0.01 ms | 56.58 ms | 57.13 ms | 0.154 |
| `1/2` | 26 | <0.01 ms | 214.91 ms | 213.97 ms | 0.740 |
| `1/2` | 28 | <0.01 ms | 930.56 ms | 926.80 ms | 2.990 |
| `1/2` | 30 | <0.01 ms | 3.877 s | 3.857 s | 11.975 |
| `1/4` | 20 | <0.01 ms | 10.60 ms | 10.62 ms | 0.006 |
| `1/4` | 22 | <0.01 ms | 28.31 ms | 27.67 ms | 0.051 |
| `1/4` | 24 | <0.01 ms | 103.03 ms | 104.02 ms | 0.289 |
| `1/4` | 26 | <0.01 ms | 428.13 ms | 406.05 ms | 1.242 |
| `1/4` | 28 | <0.01 ms | 1.731 s | 1.714 s | 4.990 |
| `1/4` | 30 | <0.01 ms | 7.485 s | 7.602 s | 19.975 |

### Plonky3 LCH14 Additive NTT — GF(2^64) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | <0.01 ms | 7.205 ms | 7.217 ms | 0.010 |
| `1/2` | 22 | <0.01 ms | 20.97 ms | 21.64 ms | 0.072 |
| `1/2` | 24 | <0.01 ms | 63.30 ms | 63.03 ms | 0.363 |
| `1/2` | 26 | <0.01 ms | 254.30 ms | 254.29 ms | 1.480 |
| `1/2` | 28 | <0.01 ms | 1.227 s | 1.227 s | 5.975 |
| `1/2` | 30 | <0.01 ms | 5.253 s | 5.271 s | 23.979 |
| `1/4` | 20 | <0.01 ms | 11.25 ms | 10.68 ms | 0.012 |
| `1/4` | 22 | <0.01 ms | 32.92 ms | 31.72 ms | 0.145 |
| `1/4` | 24 | <0.01 ms | 115.47 ms | 115.50 ms | 0.607 |
| `1/4` | 26 | <0.01 ms | 489.33 ms | 466.41 ms | 2.484 |
| `1/4` | 28 | <0.01 ms | 2.286 s | 2.286 s | 9.979 |
| `1/4` | 30 | <0.01 ms | 9.347 s | 9.647 s | 39.979 |

### Plonky3 LCH14 Additive NTT — GF(2^128) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | <0.01 ms | 5.298 ms | 5.386 ms | 0.021 |
| `1/2` | 22 | <0.01 ms | 23.69 ms | 23.30 ms | 0.156 |
| `1/2` | 24 | <0.01 ms | 89.08 ms | 89.05 ms | 0.744 |
| `1/2` | 26 | <0.01 ms | 358.55 ms | 358.76 ms | 2.996 |
| `1/2` | 28 | <0.01 ms | 1.844 s | 1.838 s | 11.977 |
| `1/2` | 30 | <0.01 ms | 8.023 s | 8.032 s | 47.979 |
| `1/4` | 20 | <0.01 ms | 9.318 ms | 9.315 ms | 0.064 |
| `1/4` | 22 | <0.01 ms | 36.27 ms | 36.24 ms | 0.299 |
| `1/4` | 24 | <0.01 ms | 147.52 ms | 147.54 ms | 1.246 |
| `1/4` | 26 | <0.01 ms | 612.93 ms | 590.19 ms | 4.986 |
| `1/4` | 28 | <0.01 ms | 3.114 s | 3.130 s | 19.977 |
| `1/4` | 30 | <0.01 ms | 13.054 s | 13.331 s | 79.979 |

### bolt-rs Additive RS — GF(2^32) (1T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 18.22 ms | 41.40 ms | 41.41 ms | 0.025 |
| `1/2` | 22 | 74.55 ms | 174.76 ms | 174.76 ms | 0.096 |
| `1/2` | 24 | 291.85 ms | 740.90 ms | 742.04 ms | 0.377 |
| `1/2` | 26 | 1.21 s | 3.456 s | 3.451 s | 1.502 |
| `1/2` | 28 | 5.18 s | 15.774 s | 15.793 s | 6.002 |
| `1/2` | 30 | 20.88 s | 72.040 s | 72.038 s | 24.002 |
| `1/4` | 20 | 32.25 ms | 81.57 ms | 81.58 ms | 0.041 |
| `1/4` | 22 | 129.33 ms | 344.72 ms | 344.75 ms | 0.158 |
| `1/4` | 24 | 520.68 ms | 1.461 s | 1.463 s | 0.627 |
| `1/4` | 26 | 2.19 s | 7.054 s | 7.049 s | 2.502 |
| `1/4` | 28 | 9.11 s | 31.995 s | 31.992 s | 10.002 |
| `1/4` | 30 | 36.25 s | 150.01 s | 150.01 s | 40.002 |

## Notes

- `bolt-rs` RS executes on `1` thread under 32-core affinity, whereas Plonky3 `lch` and `polybasis` parallelize across `32` threads.
- Plonky3 `PolyBasisNtt` only implements `GF(2^128)` in upstream commit `0d803737`.
