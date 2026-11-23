# Brakedown / Generalized Spielman Expander Codes

Single-polynomial 1D encoding benchmarks for `brakedown` (Zoo #12; status summary: OK: 58, OOM_LIMIT: 5, OOM_SKIPPED: 9).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`taskset -c 0-31`, `RAYON_NUM_THREADS=32`, `OMP_NUM_THREADS=32`); release build (`target-cpu=native`)
- **Repositories / Revisions**: `ERA local source snapshot`, `bolt-rs@3832e47b24e7b3e10525c9c5bcfc1cfe66d525f2 with local 1D driver`, `lcpc@f0e2116001af5a1bbf39481535f837d6a25772e8`, `plonkish_basefold@c29f08653121637b456e4705d901d078cd6fc668`
- **Field(s)**: `bf32`, `ft127`, `goldilocks`, `m127`, `secp256k1`
- **Message Lengths**: `K = 2^k` (`k ∈ {20, 22, 24, 26, 28, 30}`)
- **1D Geometry**: Single codeword (`nrows = 1`, `width = 1`, `log_batch_size = 0`; no interleaving, no 2D matrix reshape)

## Measurement Methodology

- **Sampling**: 1 warmup + 3 serial measured runs; reports arithmetic mean and median.
- **Timing Scope**: Measures the native 1D encoder call (`input_elements` -> `codeword_elements`) only; excludes setup (`setup_ms`), input generation, caller-buffer reset (for in-place entry points), correctness checks, and Merkle hashing/opening. Before timing, the driver pre-touches or reuses caller-owned buffers; output and temporary scratch buffers allocated internally by the encoder during the timed interval can still trigger page faults, and those times are included in the recorded measurements (per-row minor/major fault counts are logged in `results/brakedown.csv` `notes`).
- **Memory**. `Peak RSS` is whole-process peak resident memory (`GiB`), including setup.

## Results

| Variant | Field | Nominal Rate | Actual Rate | k | T | Setup (ms) | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `bolt-binary` | `bf32` | `1/2` | 0.5000 | 20 | 32 | 1601.82 | 507.178 | 506.602 | 0.543 | `OK` |
| `bolt-binary` | `bf32` | `1/2` | 0.5000 | 22 | 32 | 6983.63 | 2263.051 | 2267.681 | 2.170 | `OK` |
| `bolt-binary` | `bf32` | `1/2` | 0.5000 | 24 | 32 | 29332.18 | 9364.289 | 9311.654 | 8.676 | `OK` |
| `bolt-binary` | `bf32` | `1/2` | 0.5000 | 26 | 32 | 121732.37 | 37946.374 | 38033.185 | 34.699 | `OK` |
| `bolt-binary` | `bf32` | `1/2` | 0.5000 | 28 | 32 | 549960.34 | 154455.809 | 153913.563 | 138.795 | `OK` |
| `bolt-binary` | `bf32` | `1/2` | — | 30 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `bolt-binary` | `bf32` | `1/4` | 0.2500 | 20 | 32 | 2066.64 | 1397.999 | 1398.097 | 0.789 | `OK` |
| `bolt-binary` | `bf32` | `1/4` | 0.2500 | 22 | 32 | 8913.55 | 6322.227 | 6370.706 | 3.148 | `OK` |
| `bolt-binary` | `bf32` | `1/4` | 0.2500 | 24 | 32 | 37549.63 | 26545.893 | 26615.702 | 12.590 | `OK` |
| `bolt-binary` | `bf32` | `1/4` | 0.2500 | 26 | 32 | 157475.93 | 109951.540 | 110218.636 | 50.357 | `OK` |
| `bolt-binary` | `bf32` | `1/4` | 0.2500 | 28 | 32 | 753452.48 | 463395.539 | 458690.160 | 201.428 | `OK` |
| `bolt-binary` | `bf32` | `1/4` | — | 30 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `bolt-binary` | `bf32` | `native-high` | 0.6740 | 20 | 32 | 1548.08 | 290.791 | 291.020 | 0.516 | `OK` |
| `bolt-binary` | `bf32` | `native-high` | 0.6740 | 22 | 32 | 6803.35 | 1184.306 | 1187.261 | 2.062 | `OK` |
| `bolt-binary` | `bf32` | `native-high` | 0.6740 | 24 | 32 | 28807.89 | 4912.492 | 4926.631 | 8.242 | `OK` |
| `bolt-binary` | `bf32` | `native-high` | 0.6740 | 26 | 32 | 119144.05 | 19526.467 | 19524.203 | 32.967 | `OK` |
| `bolt-binary` | `bf32` | `native-high` | 0.6740 | 28 | 32 | 532468.73 | 79073.194 | 79121.073 | 131.867 | `OK` |
| `bolt-binary` | `bf32` | `native-high` | — | 30 | 32 | — | — | — | 419.996 | `OOM_LIMIT` |
| `bolt-binary` | `bf32` | `native-low` | 0.5060 | 20 | 32 | 1580.84 | 515.606 | 515.082 | 0.537 | `OK` |
| `bolt-binary` | `bf32` | `native-low` | 0.5060 | 22 | 32 | 6955.34 | 2195.020 | 2210.601 | 2.141 | `OK` |
| `bolt-binary` | `bf32` | `native-low` | 0.5060 | 24 | 32 | 29162.68 | 9133.742 | 9141.437 | 8.562 | `OK` |
| `bolt-binary` | `bf32` | `native-low` | 0.5060 | 26 | 32 | 122019.54 | 36735.619 | 36265.009 | 34.242 | `OK` |
| `bolt-binary` | `bf32` | `native-low` | 0.5060 | 28 | 32 | 549077.75 | 152970.334 | 152618.571 | 136.969 | `OK` |
| `bolt-binary` | `bf32` | `native-low` | — | 30 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `brakedown-recursive` | `secp256k1` | `1/2` | 0.5000 | 20 | 32 | 19472.84 | 131.900 | 130.721 | 2.322 | `OK` |
| `brakedown-recursive` | `secp256k1` | `1/2` | 0.5000 | 22 | 32 | 92207.73 | 815.016 | 815.750 | 9.283 | `OK` |
| `brakedown-recursive` | `secp256k1` | `1/2` | 0.5000 | 24 | 32 | 418906.40 | 3934.330 | 3909.413 | 37.127 | `OK` |
| `brakedown-recursive` | `secp256k1` | `1/2` | 0.5000 | 26 | 32 | 1806608.05 | 16900.890 | 16830.857 | 148.500 | `OK` |
| `brakedown-recursive` | `secp256k1` | `1/2` | — | 28 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `brakedown-recursive` | `secp256k1` | `1/2` | — | 30 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `brakedown-recursive` | `secp256k1` | `1/4` | 0.2500 | 20 | 32 | 34673.56 | 234.024 | 234.000 | 4.123 | `OK` |
| `brakedown-recursive` | `secp256k1` | `1/4` | 0.2500 | 22 | 32 | 157354.64 | 1355.542 | 1353.394 | 16.484 | `OK` |
| `brakedown-recursive` | `secp256k1` | `1/4` | 0.2500 | 24 | 32 | 694120.30 | 5998.684 | 5994.870 | 65.936 | `OK` |
| `brakedown-recursive` | `secp256k1` | `1/4` | 0.2500 | 26 | 32 | 3210079.19 | 27190.617 | 26826.660 | 263.727 | `OK` |
| `brakedown-recursive` | `secp256k1` | `1/4` | — | 28 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `brakedown-recursive` | `secp256k1` | `1/4` | — | 30 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `plonkish-sdig3` | `m127` | `native` | 0.6575 | 20 | 1 | 1024.80 | 239.612 | 238.174 | 0.424 | `OK` |
| `plonkish-sdig3` | `m127` | `native` | 0.6575 | 22 | 1 | 3969.14 | 1326.290 | 1326.234 | 1.646 | `OK` |
| `plonkish-sdig3` | `m127` | `native` | 0.6575 | 24 | 1 | 15757.10 | 8337.757 | 8335.080 | 6.561 | `OK` |
| `plonkish-sdig3` | `m127` | `native` | 0.6575 | 26 | 1 | 62849.57 | 39933.420 | 39935.107 | 26.178 | `OK` |
| `plonkish-sdig3` | `m127` | `native` | 0.6575 | 28 | 1 | 250563.50 | 169120.211 | 169124.493 | 104.666 | `OK` |
| `plonkish-sdig3` | `m127` | `native` | — | 30 | 1 | — | — | — | 316.000 | `OOM_LIMIT` |
| `sdig2` | `ft127` | `native` | 0.6803 | 20 | 1 | 1151.89 | 350.685 | 334.898 | 0.391 | `OK` |
| `sdig2` | `ft127` | `native` | 0.6803 | 22 | 1 | 4437.68 | 2050.113 | 2052.661 | 1.549 | `OK` |
| `sdig2` | `ft127` | `native` | 0.6803 | 24 | 1 | 17891.84 | 12747.215 | 13007.578 | 6.195 | `OK` |
| `sdig2` | `ft127` | `native` | 0.6803 | 26 | 1 | 71220.10 | 59314.432 | 59376.209 | 24.795 | `OK` |
| `sdig2` | `ft127` | `native` | 0.6803 | 28 | 1 | 287046.59 | 253892.669 | 254069.465 | 99.174 | `OK` |
| `sdig2` | `ft127` | `native` | 0.6803 | 30 | 1 | 1160122.86 | 1198505.524 | 1198875.907 | 396.701 | `OK` |
| `sdig3` | `ft127` | `native` | 0.6575 | 20 | 1 | 1225.87 | 404.029 | 384.515 | 0.436 | `OK` |
| `sdig3` | `ft127` | `native` | 0.6575 | 22 | 1 | 4666.79 | 2296.574 | 2310.435 | 1.703 | `OK` |
| `sdig3` | `ft127` | `native` | 0.6575 | 24 | 1 | 18642.71 | 14138.649 | 14314.609 | 6.809 | `OK` |
| `sdig3` | `ft127` | `native` | 0.6575 | 26 | 1 | 74616.55 | 65778.836 | 65865.835 | 27.195 | `OK` |
| `sdig3` | `ft127` | `native` | 0.6575 | 28 | 1 | 303508.45 | 287002.817 | 286902.526 | 108.748 | `OK` |
| `sdig3` | `ft127` | `native` | — | 30 | 1 | — | — | — | 406.660 | `OOM_LIMIT` |
| `brakedown-recursive` | `goldilocks` | `1/2` | 0.5000 | 20 | 32 | 3471.75 | 16.877 | 16.826 | 0.941 | `OK` |
| `brakedown-recursive` | `goldilocks` | `1/2` | 0.5000 | 22 | 32 | 16662.40 | 101.686 | 101.681 | 3.760 | `OK` |
| `brakedown-recursive` | `goldilocks` | `1/2` | 0.5000 | 24 | 32 | 77996.00 | 670.759 | 670.257 | 15.037 | `OK` |
| `brakedown-recursive` | `goldilocks` | `1/2` | 0.5000 | 26 | 32 | 350111.49 | 3240.275 | 3239.941 | 60.156 | `OK` |
| `brakedown-recursive` | `goldilocks` | `1/2` | 0.5000 | 28 | 32 | 1590855.18 | 17899.220 | 18028.532 | 240.594 | `OK` |
| `brakedown-recursive` | `goldilocks` | `1/2` | — | 30 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `brakedown-recursive` | `goldilocks` | `1/4` | 0.2500 | 20 | 32 | 7201.04 | 26.567 | 26.675 | 1.711 | `OK` |
| `brakedown-recursive` | `goldilocks` | `1/4` | 0.2500 | 22 | 32 | 32885.92 | 196.682 | 196.721 | 6.842 | `OK` |
| `brakedown-recursive` | `goldilocks` | `1/4` | 0.2500 | 24 | 32 | 151641.02 | 1155.391 | 1155.231 | 27.365 | `OK` |
| `brakedown-recursive` | `goldilocks` | `1/4` | 0.2500 | 26 | 32 | 687380.88 | 5345.110 | 5342.396 | 109.451 | `OK` |
| `brakedown-recursive` | `goldilocks` | `1/4` | — | 28 | 32 | — | — | — | 299.799 | `OOM_LIMIT` |
| `brakedown-recursive` | `goldilocks` | `1/4` | — | 30 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `plonkish-sdig3` | `goldilocks` | `native` | 0.6575 | 20 | 1 | 959.05 | 228.850 | 228.535 | 0.422 | `OK` |
| `plonkish-sdig3` | `goldilocks` | `native` | 0.6575 | 22 | 1 | 3707.17 | 1286.984 | 1281.671 | 1.646 | `OK` |
| `plonkish-sdig3` | `goldilocks` | `native` | 0.6575 | 24 | 1 | 14867.11 | 8284.235 | 8272.676 | 6.561 | `OK` |
| `plonkish-sdig3` | `goldilocks` | `native` | 0.6575 | 26 | 1 | 58901.90 | 39652.732 | 39668.392 | 26.178 | `OK` |
| `plonkish-sdig3` | `goldilocks` | `native` | 0.6575 | 28 | 1 | 234784.34 | 166283.759 | 166282.220 | 104.666 | `OK` |
| `plonkish-sdig3` | `goldilocks` | `native` | — | 30 | 1 | — | — | — | 316.002 | `OOM_LIMIT` |

## Notes & Boundaries

- `bolt-binary` (`bf32`, config rate `1/2`, `OK`): Native-rate labels are target ratios with fixed alpha and graph degrees. alpha=0.238 c_n=13 d_n=14 base_limit=64
- `bolt-binary` (`bf32`, config rate `1/2`, `OOM_SKIPPED`): Native-rate labels are target ratios with fixed alpha and graph degrees. Retained weighted graph and input/output lower bound 424.9 GiB.
- `bolt-binary` (`bf32`, config rate `1/4`, `OK`): Native-rate labels are target ratios with fixed alpha and graph degrees. alpha=0.238 c_n=13 d_n=14 base_limit=64
- `bolt-binary` (`bf32`, config rate `1/4`, `OOM_SKIPPED`): Native-rate labels are target ratios with fixed alpha and graph degrees. Retained weighted graph and input/output lower bound 572.8 GiB.
- `bolt-binary` (`bf32`, config rate `native-high`, `OK`): Native-rate labels are target ratios with fixed alpha and graph degrees. alpha=0.238 c_n=13 d_n=14 base_limit=64
- `bolt-binary` (`bf32`, config rate `native-high`, `OOM_LIMIT`): Native-rate labels are target ratios with fixed alpha and graph degrees. exit=134; see raw/binary_1d-brakedown-bolt-binary-bf32-30-native-high.
- `bolt-binary` (`bf32`, config rate `native-low`, `OK`): Native-rate labels are target ratios with fixed alpha and graph degrees. alpha=0.238 c_n=13 d_n=14 base_limit=64
- `bolt-binary` (`bf32`, config rate `native-low`, `OOM_SKIPPED`): Native-rate labels are target ratios with fixed alpha and graph degrees. Retained weighted graph and input/output lower bound 423.1 GiB.
- `brakedown-recursive` (`goldilocks`, config rate `1/2`, `OK`): alpha=0.3 c_n=14 d_n=28
- `brakedown-recursive` (`goldilocks`, config rate `1/2`, `OOM_SKIPPED`): Retained Brakedown graph and message lower bound 712.0 GiB.
- `brakedown-recursive` (`goldilocks`, config rate `1/4`, `OK`): alpha=0.3 c_n=14 d_n=28
- `brakedown-recursive` (`goldilocks`, config rate `1/4`, `OOM_LIMIT`): exit=134; see raw/prime_goldilocks_1d-brakedown-brakedown-recursive-goldilocks-28-4.
- `brakedown-recursive` (`goldilocks`, config rate `1/4`, `OOM_SKIPPED`): Retained Brakedown graph and message lower bound 1096.0 GiB.
- `brakedown-recursive` (`secp256k1`, config rate `1/2`, `OK`): alpha=0.3 c_n=14 d_n=28
- `brakedown-recursive` (`secp256k1`, config rate `1/2`, `OOM_SKIPPED`): Retained Brakedown graph and message lower bound 1792.0 GiB.
- `brakedown-recursive` (`secp256k1`, config rate `1/2`, `OOM_SKIPPED`): Retained Brakedown graph and message lower bound 448.0 GiB.
- `brakedown-recursive` (`secp256k1`, config rate `1/4`, `OK`): alpha=0.3 c_n=14 d_n=28
- `brakedown-recursive` (`secp256k1`, config rate `1/4`, `OOM_SKIPPED`): Retained Brakedown graph and message lower bound 2752.0 GiB.
- `brakedown-recursive` (`secp256k1`, config rate `1/4`, `OOM_SKIPPED`): Retained Brakedown graph and message lower bound 688.0 GiB.
- `plonkish-sdig3` (`goldilocks`, config rate `native`, `OK`): Native BrakedownSpec3, original serial 1D encode. Field element occupies 16 bytes. profile=BrakedownSpec3 base_limit=128
- `plonkish-sdig3` (`goldilocks`, config rate `native`, `OOM_LIMIT`): Native BrakedownSpec3, original serial 1D encode. Field element occupies 16 bytes. exit=134; see raw/prime_goldilocks_1d-brakedown-plonkish-sdig3-goldilocks-30-native.
- `plonkish-sdig3` (`m127`, config rate `native`, `OK`): Native BrakedownSpec3, original serial 1D encode. Field element occupies 16 bytes. profile=BrakedownSpec3 base_limit=128
- `plonkish-sdig3` (`m127`, config rate `native`, `OOM_LIMIT`): Native BrakedownSpec3, original serial 1D encode. Field element occupies 16 bytes. exit=134; see raw/native_fields_1d-brakedown-plonkish-sdig3-m127-30-native.
- `sdig2` (`ft127`, config rate `native`, `OK`): Stock sparse multiply is serial for one codeword.
- `sdig3` (`ft127`, config rate `native`, `OK`): Stock sparse multiply is serial for one codeword.
- `sdig3` (`ft127`, config rate `native`, `OOM_LIMIT`): Stock sparse multiply is serial for one codeword. exit=134; see raw/native_fields_1d-brakedown-sdig3-ft127-30-native.
