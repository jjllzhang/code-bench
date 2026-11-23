# Repeat–Accumulate–Accumulate (RAA) Benchmark Results

Measurements of 1D Repeat–Accumulate–Accumulate encoders across prime and binary fields: `raa-unweighted` (ERA reference implementation), [bolt-rs](https://github.com/bcc-research/bolt-rs) (`3832e47b`), [plonkish_basefold](https://github.com/hadasz/plonkish_basefold) (`c29f0865`) 64-bit packed binary RAA, and the [CRYPTO '24 EACode artifact](https://artifacts.iacr.org/crypto/2024/a10/).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`target-cpu=native`); `32T / 1T`.
- **Field(s)**: Goldilocks, `secp256k1`, `Ristretto255`, `GF(2^32/64/128)`.
- **`raa-unweighted`**: Repeat-permute-accumulate pipeline over Goldilocks (`8B`) and `secp256k1` Fr (`32B`).
- **`bolt-raa`**: Binary RAA over `GF(2^32)` and `GF(2^128)`.
- **`blaze-packed-u64`**: 64-bit word-packed binary RAA (`bf64` packed records, XOR accumulation rather than field multiplication).
- **`eacode-official`**: Official CRYPTO '24 `EACode` RAA kernel over `Ristretto255` (`1T` serial).

## Measurement Methodology

- **Sampling**: 1 warmup followed by 3 serial runs per configuration; reports both arithmetic mean and median encoding time.
- **Timing & Memory Scope**: `Encode` measures single-polynomial 1D encoding (`K = 2^k` input elements) excluding setup/graph construction (`Setup`), input generation, and Merkle hashing. `Peak RSS` is process peak resident memory (GiB).
- **Missing Values**: `—` denotes unmeasured points that exceed a finite-field/implementation bound or the 420 GiB / 503 GiB memory limit.

## Results

### Unweighted RAA — Goldilocks (64-bit) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 61.05 ms | 8.765 ms | 8.871 ms | 0.072 |
| `1/2` | 22 | 354.02 ms | 36.61 ms | 36.24 ms | 0.283 |
| `1/2` | 24 | 1.62 s | 153.64 ms | 153.53 ms | 1.127 |
| `1/2` | 26 | 6.89 s | 631.40 ms | 629.61 ms | 4.502 |
| `1/2` | 28 | 30.10 s | 2.664 s | 2.662 s | 18.002 |
| `1/2` | 30 | 150.82 s | 12.324 s | 12.304 s | 72.002 |
| `1/4` | 20 | 152.94 ms | 15.83 ms | 15.83 ms | 0.135 |
| `1/4` | 22 | 782.43 ms | 71.54 ms | 71.54 ms | 0.533 |
| `1/4` | 24 | 3.37 s | 306.46 ms | 306.44 ms | 2.127 |
| `1/4` | 26 | 14.13 s | 1.347 s | 1.351 s | 8.502 |
| `1/4` | 28 | 65.95 s | 5.724 s | 5.609 s | 34.002 |
| `1/4` | 30 | 363.50 s | 26.891 s | 26.894 s | 136.002 |

### Unweighted RAA — secp256k1 Fr (256-bit) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 109.05 ms | 31.46 ms | 31.51 ms | 0.189 |
| `1/2` | 22 | 573.41 ms | 123.77 ms | 123.96 ms | 0.752 |
| `1/2` | 24 | 2.43 s | 497.23 ms | 495.16 ms | 3.002 |
| `1/2` | 26 | 9.95 s | 2.006 s | 2.004 s | 12.002 |
| `1/2` | 28 | 41.28 s | 8.577 s | 8.566 s | 48.002 |
| `1/2` | 30 | 202.71 s | 32.004 s | 32.018 s | 192.002 |
| `1/4` | 20 | 253.73 ms | 62.98 ms | 63.07 ms | 0.346 |
| `1/4` | 22 | 1.19 s | 245.91 ms | 245.94 ms | 1.377 |
| `1/4` | 24 | 4.94 s | 983.49 ms | 983.18 ms | 5.502 |
| `1/4` | 26 | 20.03 s | 4.011 s | 4.008 s | 22.002 |
| `1/4` | 28 | 89.15 s | 17.057 s | 17.073 s | 88.002 |
| `1/4` | 30 | 480.28 s | 62.049 s | 62.061 s | 352.002 |

### Bolt Binary RAA — GF(2^32) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 49.56 ms | 12.36 ms | 12.36 ms | 0.053 |
| `1/2` | 22 | 329.21 ms | 56.55 ms | 56.34 ms | 0.205 |
| `1/2` | 24 | 1.59 s | 220.21 ms | 220.04 ms | 0.814 |
| `1/2` | 26 | 6.99 s | 903.14 ms | 900.92 ms | 3.252 |
| `1/2` | 28 | 30.11 s | 4.323 s | 4.324 s | 13.002 |
| `1/2` | 30 | 157.59 s | 15.539 s | 15.508 s | 52.002 |
| `1/4` | 20 | 137.63 ms | 26.56 ms | 26.75 ms | 0.100 |
| `1/4` | 22 | 738.30 ms | 111.12 ms | 110.93 ms | 0.393 |
| `1/4` | 24 | 3.39 s | 455.24 ms | 455.50 ms | 1.564 |
| `1/4` | 26 | 14.42 s | 1.897 s | 1.924 s | 6.252 |
| `1/4` | 28 | 67.00 s | 7.664 s | 7.639 s | 25.002 |
| `1/4` | 30 | 261.91 s | 34.158 s | 33.874 s | 100.002 |

### Bolt Binary RAA — GF(2^128) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 62.54 ms | 16.80 ms | 16.81 ms | 0.111 |
| `1/2` | 22 | 381.25 ms | 66.55 ms | 65.67 ms | 0.439 |
| `1/2` | 24 | 1.79 s | 255.34 ms | 255.39 ms | 1.752 |
| `1/2` | 26 | 7.84 s | 1.047 s | 1.049 s | 7.002 |
| `1/2` | 28 | 33.11 s | 4.324 s | 4.316 s | 28.002 |
| `1/2` | 30 | 169.05 s | 20.586 s | 20.612 s | 112.002 |
| `1/4` | 20 | 156.57 ms | 35.18 ms | 35.01 ms | 0.205 |
| `1/4` | 22 | 841.88 ms | 130.63 ms | 130.67 ms | 0.814 |
| `1/4` | 24 | 3.78 s | 552.18 ms | 531.89 ms | 3.252 |
| `1/4` | 26 | 15.96 s | 2.243 s | 2.188 s | 13.002 |
| `1/4` | 28 | 74.13 s | 9.478 s | 9.483 s | 52.002 |
| `1/4` | 30 | 290.57 s | 40.067 s | 42.115 s | 208.002 |

### Blaze 64-bit Packed RAA — GF(2^64) (32T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 84.99 ms | 24.58 ms | 24.60 ms | 0.049 |
| `1/2` | 22 | 479.98 ms | 88.80 ms | 90.52 ms | 0.285 |
| `1/2` | 24 | 2.32 s | 406.41 ms | 384.63 ms | 1.221 |
| `1/2` | 26 | 10.61 s | 1.859 s | 1.904 s | 4.975 |
| `1/2` | 28 | 44.98 s | 7.847 s | 7.624 s | 19.979 |
| `1/2` | 30 | 237.40 s | 62.814 s | 63.109 s | 79.971 |
| `1/4` | 20 | 199.96 ms | 51.00 ms | 50.65 ms | 0.111 |
| `1/4` | 22 | 1.06 s | 190.87 ms | 181.48 ms | 0.537 |
| `1/4` | 24 | 5.04 s | 800.48 ms | 772.18 ms | 2.223 |
| `1/4` | 26 | 21.97 s | 3.696 s | 3.600 s | 8.977 |
| `1/4` | 28 | 102.23 s | 20.745 s | 20.816 s | 35.977 |
| `1/4` | 30 | 536.32 s | 162.87 s | 167.12 s | 143.979 |

### CRYPTO'24 EACode RAA — Ristretto255 Fr (253-bit) (1T)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | 61.26 ms | 70.04 ms | 70.09 ms | 0.188 |
| `1/2` | 22 | 332.61 ms | 298.17 ms | 295.56 ms | 0.752 |
| `1/2` | 24 | 1.50 s | 1.215 s | 1.212 s | 3.002 |
| `1/2` | 26 | 6.35 s | 5.375 s | 5.358 s | 12.000 |
| `1/2` | 28 | 27.09 s | 32.042 s | 32.049 s | 48.002 |
| `1/2` | 30 | 132.52 s | 206.65 s | 206.24 s | 192.002 |
| `1/4` | 20 | 144.81 ms | 143.64 ms | 143.57 ms | 0.346 |
| `1/4` | 22 | 716.31 ms | 604.75 ms | 599.75 ms | 1.377 |
| `1/4` | 24 | 3.10 s | 2.509 s | 2.509 s | 5.502 |
| `1/4` | 26 | 13.03 s | 12.710 s | 12.673 s | 22.002 |
| `1/4` | 28 | 58.51 s | 70.456 s | 70.410 s | 88.000 |
| `1/4` | 30 | 291.44 s | 460.76 s | 468.44 s | 352.002 |

## Notes

- `eacode-official` RAA executes on `1` thread; all other RAA variants use `32` threads.
- All 72 configurations completed from `k = 20` to `k = 30`.
