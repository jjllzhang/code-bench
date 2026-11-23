# Repeat–Accumulate–Accumulate (1D RAA)

Single-polynomial 1D encoding benchmarks for `raa` (Zoo #11, #7; status summary: OK: 72).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`taskset -c 0-31`, `RAYON_NUM_THREADS=32`, `OMP_NUM_THREADS=32`); release build (`target-cpu=native`)
- **Repositories / Revisions**: `EACode CRYPTO’24 artifact`, `ERA local source snapshot`, `bolt-rs@3832e47b24e7b3e10525c9c5bcfc1cfe66d525f2 with local 1D driver`, `plonkish_basefold@c29f08653121637b456e4705d901d078cd6fc668`
- **Field(s)**: `bf128`, `bf32`, `bf64`, `goldilocks`, `ristretto255`, `secp256k1`
- **Message Lengths**: `K = 2^k` (`k ∈ {20, 22, 24, 26, 28, 30}`)
- **1D Geometry**: Single codeword (`nrows = 1`, `width = 1`, `log_batch_size = 0`; no interleaving, no 2D matrix reshape)

## Measurement Methodology

- **Sampling**: 1 warmup + 3 serial measured runs; reports arithmetic mean and median.
- **Timing Scope**: Measures the native 1D encoder call (`input_elements` -> `codeword_elements`) only; excludes setup (`setup_ms`), input generation, caller-buffer reset (for in-place entry points), correctness checks, and Merkle hashing/opening. Before timing, the driver pre-touches or reuses caller-owned buffers; output and temporary scratch buffers allocated internally by the encoder during the timed interval can still trigger page faults, and those times are included in the recorded measurements (per-row minor/major fault counts are logged in `results/raa.csv` `notes`).
- **Memory**. `Peak RSS` is whole-process peak resident memory (`GiB`), including setup.

## Results

| Variant | Field | Nominal Rate | Actual Rate | k | T | Setup (ms) | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `blaze-packed-u64` | `bf64` | `1/2` | 0.5000 | 20 | 32 | 84.99 | 24.577 | 24.596 | 0.049 | `OK` |
| `blaze-packed-u64` | `bf64` | `1/2` | 0.5000 | 22 | 32 | 479.98 | 88.804 | 90.521 | 0.285 | `OK` |
| `blaze-packed-u64` | `bf64` | `1/2` | 0.5000 | 24 | 32 | 2318.21 | 406.414 | 384.633 | 1.221 | `OK` |
| `blaze-packed-u64` | `bf64` | `1/2` | 0.5000 | 26 | 32 | 10611.05 | 1858.924 | 1904.414 | 4.975 | `OK` |
| `blaze-packed-u64` | `bf64` | `1/2` | 0.5000 | 28 | 32 | 44976.88 | 7846.995 | 7624.032 | 19.979 | `OK` |
| `blaze-packed-u64` | `bf64` | `1/2` | 0.5000 | 30 | 32 | 237399.29 | 62814.142 | 63108.595 | 79.971 | `OK` |
| `blaze-packed-u64` | `bf64` | `1/4` | 0.2500 | 20 | 32 | 199.96 | 51.001 | 50.651 | 0.111 | `OK` |
| `blaze-packed-u64` | `bf64` | `1/4` | 0.2500 | 22 | 32 | 1056.56 | 190.867 | 181.475 | 0.537 | `OK` |
| `blaze-packed-u64` | `bf64` | `1/4` | 0.2500 | 24 | 32 | 5035.66 | 800.483 | 772.176 | 2.223 | `OK` |
| `blaze-packed-u64` | `bf64` | `1/4` | 0.2500 | 26 | 32 | 21969.49 | 3696.387 | 3600.439 | 8.977 | `OK` |
| `blaze-packed-u64` | `bf64` | `1/4` | 0.2500 | 28 | 32 | 102227.41 | 20745.094 | 20815.890 | 35.977 | `OK` |
| `blaze-packed-u64` | `bf64` | `1/4` | 0.2500 | 30 | 32 | 536321.64 | 162869.537 | 167116.316 | 143.979 | `OK` |
| `bolt-raa` | `bf128` | `1/2` | 0.5000 | 20 | 32 | 62.54 | 16.805 | 16.810 | 0.111 | `OK` |
| `bolt-raa` | `bf128` | `1/2` | 0.5000 | 22 | 32 | 381.25 | 66.554 | 65.672 | 0.439 | `OK` |
| `bolt-raa` | `bf128` | `1/2` | 0.5000 | 24 | 32 | 1788.04 | 255.337 | 255.392 | 1.752 | `OK` |
| `bolt-raa` | `bf128` | `1/2` | 0.5000 | 26 | 32 | 7835.79 | 1047.442 | 1048.529 | 7.002 | `OK` |
| `bolt-raa` | `bf128` | `1/2` | 0.5000 | 28 | 32 | 33110.44 | 4324.470 | 4316.415 | 28.002 | `OK` |
| `bolt-raa` | `bf128` | `1/2` | 0.5000 | 30 | 32 | 169051.08 | 20586.482 | 20612.302 | 112.002 | `OK` |
| `bolt-raa` | `bf128` | `1/4` | 0.2500 | 20 | 32 | 156.57 | 35.179 | 35.009 | 0.205 | `OK` |
| `bolt-raa` | `bf128` | `1/4` | 0.2500 | 22 | 32 | 841.88 | 130.626 | 130.667 | 0.814 | `OK` |
| `bolt-raa` | `bf128` | `1/4` | 0.2500 | 24 | 32 | 3775.45 | 552.181 | 531.889 | 3.252 | `OK` |
| `bolt-raa` | `bf128` | `1/4` | 0.2500 | 26 | 32 | 15956.46 | 2242.782 | 2188.237 | 13.002 | `OK` |
| `bolt-raa` | `bf128` | `1/4` | 0.2500 | 28 | 32 | 74134.08 | 9477.657 | 9482.879 | 52.002 | `OK` |
| `bolt-raa` | `bf128` | `1/4` | 0.2500 | 30 | 32 | 290569.26 | 40066.773 | 42115.032 | 208.002 | `OK` |
| `bolt-raa` | `bf32` | `1/2` | 0.5000 | 20 | 32 | 49.56 | 12.357 | 12.362 | 0.053 | `OK` |
| `bolt-raa` | `bf32` | `1/2` | 0.5000 | 22 | 32 | 329.21 | 56.548 | 56.337 | 0.205 | `OK` |
| `bolt-raa` | `bf32` | `1/2` | 0.5000 | 24 | 32 | 1594.33 | 220.213 | 220.039 | 0.814 | `OK` |
| `bolt-raa` | `bf32` | `1/2` | 0.5000 | 26 | 32 | 6990.14 | 903.144 | 900.922 | 3.252 | `OK` |
| `bolt-raa` | `bf32` | `1/2` | 0.5000 | 28 | 32 | 30112.22 | 4323.220 | 4324.264 | 13.002 | `OK` |
| `bolt-raa` | `bf32` | `1/2` | 0.5000 | 30 | 32 | 157590.06 | 15538.693 | 15508.369 | 52.002 | `OK` |
| `bolt-raa` | `bf32` | `1/4` | 0.2500 | 20 | 32 | 137.63 | 26.563 | 26.751 | 0.100 | `OK` |
| `bolt-raa` | `bf32` | `1/4` | 0.2500 | 22 | 32 | 738.30 | 111.124 | 110.929 | 0.393 | `OK` |
| `bolt-raa` | `bf32` | `1/4` | 0.2500 | 24 | 32 | 3387.42 | 455.238 | 455.496 | 1.564 | `OK` |
| `bolt-raa` | `bf32` | `1/4` | 0.2500 | 26 | 32 | 14417.02 | 1896.638 | 1923.539 | 6.252 | `OK` |
| `bolt-raa` | `bf32` | `1/4` | 0.2500 | 28 | 32 | 67000.46 | 7663.558 | 7638.992 | 25.002 | `OK` |
| `bolt-raa` | `bf32` | `1/4` | 0.2500 | 30 | 32 | 261908.25 | 34157.845 | 33873.535 | 100.002 | `OK` |
| `eacode-official` | `ristretto255` | `1/2` | 0.5000 | 20 | 1 | 61.26 | 70.041 | 70.087 | 0.188 | `OK` |
| `eacode-official` | `ristretto255` | `1/2` | 0.5000 | 22 | 1 | 332.61 | 298.171 | 295.557 | 0.752 | `OK` |
| `eacode-official` | `ristretto255` | `1/2` | 0.5000 | 24 | 1 | 1498.98 | 1215.089 | 1212.161 | 3.002 | `OK` |
| `eacode-official` | `ristretto255` | `1/2` | 0.5000 | 26 | 1 | 6348.75 | 5375.041 | 5357.986 | 12.000 | `OK` |
| `eacode-official` | `ristretto255` | `1/2` | 0.5000 | 28 | 1 | 27085.98 | 32042.495 | 32049.317 | 48.002 | `OK` |
| `eacode-official` | `ristretto255` | `1/2` | 0.5000 | 30 | 1 | 132518.20 | 206653.649 | 206240.176 | 192.002 | `OK` |
| `eacode-official` | `ristretto255` | `1/4` | 0.2500 | 20 | 1 | 144.81 | 143.636 | 143.572 | 0.346 | `OK` |
| `eacode-official` | `ristretto255` | `1/4` | 0.2500 | 22 | 1 | 716.31 | 604.750 | 599.748 | 1.377 | `OK` |
| `eacode-official` | `ristretto255` | `1/4` | 0.2500 | 24 | 1 | 3101.08 | 2509.485 | 2509.500 | 5.502 | `OK` |
| `eacode-official` | `ristretto255` | `1/4` | 0.2500 | 26 | 1 | 13028.96 | 12709.504 | 12672.566 | 22.002 | `OK` |
| `eacode-official` | `ristretto255` | `1/4` | 0.2500 | 28 | 1 | 58506.45 | 70456.025 | 70410.268 | 88.000 | `OK` |
| `eacode-official` | `ristretto255` | `1/4` | 0.2500 | 30 | 1 | 291438.86 | 460756.645 | 468436.052 | 352.002 | `OK` |
| `raa-unweighted` | `secp256k1` | `1/2` | 0.5000 | 20 | 32 | 109.05 | 31.462 | 31.514 | 0.189 | `OK` |
| `raa-unweighted` | `secp256k1` | `1/2` | 0.5000 | 22 | 32 | 573.41 | 123.766 | 123.960 | 0.752 | `OK` |
| `raa-unweighted` | `secp256k1` | `1/2` | 0.5000 | 24 | 32 | 2430.81 | 497.229 | 495.163 | 3.002 | `OK` |
| `raa-unweighted` | `secp256k1` | `1/2` | 0.5000 | 26 | 32 | 9950.22 | 2005.762 | 2004.040 | 12.002 | `OK` |
| `raa-unweighted` | `secp256k1` | `1/2` | 0.5000 | 28 | 32 | 41280.96 | 8576.530 | 8565.905 | 48.002 | `OK` |
| `raa-unweighted` | `secp256k1` | `1/2` | 0.5000 | 30 | 32 | 202713.18 | 32003.708 | 32017.679 | 192.002 | `OK` |
| `raa-unweighted` | `secp256k1` | `1/4` | 0.2500 | 20 | 32 | 253.73 | 62.980 | 63.067 | 0.346 | `OK` |
| `raa-unweighted` | `secp256k1` | `1/4` | 0.2500 | 22 | 32 | 1185.14 | 245.905 | 245.941 | 1.377 | `OK` |
| `raa-unweighted` | `secp256k1` | `1/4` | 0.2500 | 24 | 32 | 4938.16 | 983.490 | 983.182 | 5.502 | `OK` |
| `raa-unweighted` | `secp256k1` | `1/4` | 0.2500 | 26 | 32 | 20029.63 | 4011.192 | 4008.422 | 22.002 | `OK` |
| `raa-unweighted` | `secp256k1` | `1/4` | 0.2500 | 28 | 32 | 89147.61 | 17057.134 | 17072.569 | 88.002 | `OK` |
| `raa-unweighted` | `secp256k1` | `1/4` | 0.2500 | 30 | 32 | 480279.56 | 62048.918 | 62060.942 | 352.002 | `OK` |
| `raa-unweighted` | `goldilocks` | `1/2` | 0.5000 | 20 | 32 | 61.05 | 8.765 | 8.871 | 0.072 | `OK` |
| `raa-unweighted` | `goldilocks` | `1/2` | 0.5000 | 22 | 32 | 354.02 | 36.613 | 36.238 | 0.283 | `OK` |
| `raa-unweighted` | `goldilocks` | `1/2` | 0.5000 | 24 | 32 | 1616.46 | 153.643 | 153.528 | 1.127 | `OK` |
| `raa-unweighted` | `goldilocks` | `1/2` | 0.5000 | 26 | 32 | 6888.79 | 631.397 | 629.610 | 4.502 | `OK` |
| `raa-unweighted` | `goldilocks` | `1/2` | 0.5000 | 28 | 32 | 30102.48 | 2663.569 | 2662.088 | 18.002 | `OK` |
| `raa-unweighted` | `goldilocks` | `1/2` | 0.5000 | 30 | 32 | 150815.63 | 12324.080 | 12304.139 | 72.002 | `OK` |
| `raa-unweighted` | `goldilocks` | `1/4` | 0.2500 | 20 | 32 | 152.94 | 15.829 | 15.826 | 0.135 | `OK` |
| `raa-unweighted` | `goldilocks` | `1/4` | 0.2500 | 22 | 32 | 782.43 | 71.537 | 71.543 | 0.533 | `OK` |
| `raa-unweighted` | `goldilocks` | `1/4` | 0.2500 | 24 | 32 | 3371.52 | 306.463 | 306.438 | 2.127 | `OK` |
| `raa-unweighted` | `goldilocks` | `1/4` | 0.2500 | 26 | 32 | 14127.44 | 1346.760 | 1350.963 | 8.502 | `OK` |
| `raa-unweighted` | `goldilocks` | `1/4` | 0.2500 | 28 | 32 | 65947.61 | 5724.312 | 5609.407 | 34.002 | `OK` |
| `raa-unweighted` | `goldilocks` | `1/4` | 0.2500 | 30 | 32 | 363496.88 | 26890.785 | 26893.612 | 136.002 | `OK` |

## Notes & Boundaries

- `blaze-packed-u64` (`bf64`, config rate `1/2`, `OK`): 64-bit packed binary record, not a field multiply representation.
- `blaze-packed-u64` (`bf64`, config rate `1/4`, `OK`): 64-bit packed binary record, not a field multiply representation.
