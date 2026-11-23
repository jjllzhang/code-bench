# Binary HyperFold High-Arity Foldable Codes (r ∈ {2,4,8})

Single-polynomial 1D encoding benchmarks for `binary-hyperfold` (Zoo #5+; status summary: OK: 143, OOM_LIMIT: 1).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`taskset -c 0-31`, `RAYON_NUM_THREADS=32`, `OMP_NUM_THREADS=32`); release build (`target-cpu=native`)
- **Repositories / Revisions**: `jjllzhang/binary-hyperfold@80f16b8e32da3d2b2478b8e075f5095c8ae8c8cb`
- **Field(s)**: `bf128`, `bf16`, `bf32`, `bf64`
- **Message Lengths**: `K = 2^k` (`k ∈ {20, 22, 24, 26, 28, 30}`)
- **1D Geometry**: Single codeword (`nrows = 1`, `width = 1`, `log_batch_size = 0`; no interleaving, no 2D matrix reshape)

## Measurement Methodology

- **Sampling**: 1 warmup + 3 serial measured runs; reports arithmetic mean and median.
- **Timing Scope**: Measures the native 1D encoder call (`input_elements` -> `codeword_elements`) only; excludes setup (`setup_ms`), input generation, caller-buffer reset (for in-place entry points), correctness checks, and Merkle hashing/opening. Before timing, the driver pre-touches or reuses caller-owned buffers; output and temporary scratch buffers allocated internally by the encoder during the timed interval can still trigger page faults, and those times are included in the recorded measurements (per-row minor/major fault counts are logged in `results/binary-hyperfold.csv` `notes`).
- **Memory**. `Peak RSS` is whole-process peak resident memory (`GiB`), including setup.

## Results

| Variant | Field | Nominal Rate | Actual Rate | k | T | Setup (ms) | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `r2-rs` | `bf128` | `1/2` | 0.5000 | 20 | 32 | 84.49 | 67.535 | 65.972 | 0.242 | `OK` |
| `r2-rs` | `bf128` | `1/2` | 0.5000 | 22 | 32 | 301.61 | 224.285 | 209.599 | 1.033 | `OK` |
| `r2-rs` | `bf128` | `1/2` | 0.5000 | 24 | 32 | 1048.86 | 898.649 | 887.508 | 4.189 | `OK` |
| `r2-rs` | `bf128` | `1/2` | 0.5000 | 26 | 32 | 4044.57 | 3604.585 | 3599.058 | 17.225 | `OK` |
| `r2-rs` | `bf128` | `1/2` | 0.5000 | 28 | 32 | 15676.35 | 15894.805 | 15937.517 | 66.939 | `OK` |
| `r2-rs` | `bf128` | `1/2` | 0.5000 | 30 | 32 | 62238.29 | 57187.358 | 57248.211 | 284.582 | `OK` |
| `r2-rs` | `bf128` | `1/4` | 0.2500 | 20 | 32 | 177.58 | 93.282 | 92.240 | 0.426 | `OK` |
| `r2-rs` | `bf128` | `1/4` | 0.2500 | 22 | 32 | 549.20 | 369.812 | 366.699 | 2.031 | `OK` |
| `r2-rs` | `bf128` | `1/4` | 0.2500 | 24 | 32 | 2064.28 | 1665.029 | 1599.032 | 7.674 | `OK` |
| `r2-rs` | `bf128` | `1/4` | 0.2500 | 26 | 32 | 7931.15 | 7620.194 | 7697.087 | 32.836 | `OK` |
| `r2-rs` | `bf128` | `1/4` | 0.2500 | 28 | 32 | 31209.12 | 31684.358 | 31671.930 | 115.566 | `OK` |
| `r2-rs` | `bf128` | `1/4` | — | 30 | 32 | — | — | — | 417.838 | `OOM_LIMIT` |
| `r2-rs` | `bf16` | `1/2` | 0.5000 | 20 | 32 | 17.32 | 27.337 | 27.412 | 0.021 | `OK` |
| `r2-rs` | `bf16` | `1/2` | 0.5000 | 22 | 32 | 57.76 | 74.476 | 75.287 | 0.105 | `OK` |
| `r2-rs` | `bf16` | `1/2` | 0.5000 | 24 | 32 | 223.80 | 258.077 | 247.720 | 0.529 | `OK` |
| `r2-rs` | `bf16` | `1/2` | 0.5000 | 26 | 32 | 816.64 | 950.883 | 959.447 | 2.156 | `OK` |
| `r2-rs` | `bf16` | `1/2` | 0.5000 | 28 | 32 | 3046.03 | 3787.602 | 3789.614 | 9.123 | `OK` |
| `r2-rs` | `bf16` | `1/2` | 0.5000 | 30 | 32 | 11840.63 | 15839.110 | 15850.100 | 33.188 | `OK` |
| `r2-rs` | `bf16` | `1/4` | 0.2500 | 20 | 32 | 31.06 | 44.491 | 43.520 | 0.037 | `OK` |
| `r2-rs` | `bf16` | `1/4` | 0.2500 | 22 | 32 | 114.24 | 133.378 | 136.015 | 0.252 | `OK` |
| `r2-rs` | `bf16` | `1/4` | 0.2500 | 24 | 32 | 437.09 | 481.952 | 477.019 | 1.012 | `OK` |
| `r2-rs` | `bf16` | `1/4` | 0.2500 | 26 | 32 | 1565.80 | 1833.629 | 1837.229 | 4.080 | `OK` |
| `r2-rs` | `bf16` | `1/4` | 0.2500 | 28 | 32 | 5993.87 | 7540.591 | 7534.839 | 17.352 | `OK` |
| `r2-rs` | `bf16` | `1/4` | 0.2500 | 30 | 32 | 23461.41 | 32916.296 | 31518.363 | 69.342 | `OK` |
| `r2-rs` | `bf32` | `1/2` | 0.5000 | 20 | 32 | 32.50 | 42.244 | 40.948 | 0.039 | `OK` |
| `r2-rs` | `bf32` | `1/2` | 0.5000 | 22 | 32 | 108.72 | 132.108 | 129.537 | 0.252 | `OK` |
| `r2-rs` | `bf32` | `1/2` | 0.5000 | 24 | 32 | 376.11 | 469.637 | 453.584 | 1.102 | `OK` |
| `r2-rs` | `bf32` | `1/2` | 0.5000 | 26 | 32 | 1374.98 | 1758.934 | 1761.594 | 4.588 | `OK` |
| `r2-rs` | `bf32` | `1/2` | 0.5000 | 28 | 32 | 5182.71 | 7309.237 | 7364.469 | 17.699 | `OK` |
| `r2-rs` | `bf32` | `1/2` | 0.5000 | 30 | 32 | 20251.11 | 30569.822 | 30566.420 | 67.121 | `OK` |
| `r2-rs` | `bf32` | `1/4` | 0.2500 | 20 | 32 | 57.21 | 52.461 | 50.973 | 0.102 | `OK` |
| `r2-rs` | `bf32` | `1/4` | 0.2500 | 22 | 32 | 199.82 | 177.215 | 176.342 | 0.498 | `OK` |
| `r2-rs` | `bf32` | `1/4` | 0.2500 | 24 | 32 | 692.86 | 724.414 | 700.913 | 2.105 | `OK` |
| `r2-rs` | `bf32` | `1/4` | 0.2500 | 26 | 32 | 2646.43 | 3033.422 | 2943.743 | 8.555 | `OK` |
| `r2-rs` | `bf32` | `1/4` | 0.2500 | 28 | 32 | 10277.60 | 12785.534 | 12750.779 | 33.279 | `OK` |
| `r2-rs` | `bf32` | `1/4` | 0.2500 | 30 | 32 | 41348.98 | 55494.181 | 55122.215 | 133.879 | `OK` |
| `r2-rs` | `bf64` | `1/2` | 0.5000 | 20 | 32 | 38.14 | 45.473 | 46.133 | 0.107 | `OK` |
| `r2-rs` | `bf64` | `1/2` | 0.5000 | 22 | 32 | 143.88 | 145.343 | 136.879 | 0.523 | `OK` |
| `r2-rs` | `bf64` | `1/2` | 0.5000 | 24 | 32 | 515.47 | 523.733 | 519.612 | 1.914 | `OK` |
| `r2-rs` | `bf64` | `1/2` | 0.5000 | 26 | 32 | 1860.75 | 2131.934 | 2074.758 | 8.424 | `OK` |
| `r2-rs` | `bf64` | `1/2` | 0.5000 | 28 | 32 | 7088.36 | 8843.170 | 8466.205 | 35.359 | `OK` |
| `r2-rs` | `bf64` | `1/2` | 0.5000 | 30 | 32 | 27623.02 | 35976.550 | 35164.853 | 135.908 | `OK` |
| `r2-rs` | `bf64` | `1/4` | 0.2500 | 20 | 32 | 74.72 | 64.991 | 65.194 | 0.211 | `OK` |
| `r2-rs` | `bf64` | `1/4` | 0.2500 | 22 | 32 | 269.47 | 206.241 | 208.029 | 0.918 | `OK` |
| `r2-rs` | `bf64` | `1/4` | 0.2500 | 24 | 32 | 960.53 | 894.361 | 854.895 | 4.354 | `OK` |
| `r2-rs` | `bf64` | `1/4` | 0.2500 | 26 | 32 | 3623.03 | 3622.987 | 3615.909 | 16.402 | `OK` |
| `r2-rs` | `bf64` | `1/4` | 0.2500 | 28 | 32 | 14040.99 | 16985.891 | 15774.553 | 68.953 | `OK` |
| `r2-rs` | `bf64` | `1/4` | 0.2500 | 30 | 32 | 55097.83 | 67859.635 | 67623.856 | 271.803 | `OK` |
| `r4-rs` | `bf128` | `1/2` | 0.5000 | 20 | 32 | 52.39 | 42.512 | 43.765 | 0.186 | `OK` |
| `r4-rs` | `bf128` | `1/2` | 0.5000 | 22 | 32 | 194.01 | 143.954 | 132.104 | 0.805 | `OK` |
| `r4-rs` | `bf128` | `1/2` | 0.5000 | 24 | 32 | 658.00 | 647.437 | 637.646 | 3.393 | `OK` |
| `r4-rs` | `bf128` | `1/2` | 0.5000 | 26 | 32 | 2507.06 | 2779.495 | 2825.384 | 13.639 | `OK` |
| `r4-rs` | `bf128` | `1/2` | 0.5000 | 28 | 32 | 9807.47 | 12044.337 | 11904.096 | 53.219 | `OK` |
| `r4-rs` | `bf128` | `1/2` | 0.5000 | 30 | 32 | 38398.28 | 43610.472 | 39235.355 | 215.277 | `OK` |
| `r4-rs` | `bf128` | `1/4` | 0.2500 | 20 | 32 | 112.37 | 68.118 | 66.181 | 0.402 | `OK` |
| `r4-rs` | `bf128` | `1/4` | 0.2500 | 22 | 32 | 354.95 | 245.967 | 244.565 | 1.609 | `OK` |
| `r4-rs` | `bf128` | `1/4` | 0.2500 | 24 | 32 | 1290.53 | 1197.371 | 1136.060 | 6.125 | `OK` |
| `r4-rs` | `bf128` | `1/4` | 0.2500 | 26 | 32 | 4976.90 | 5675.636 | 5047.777 | 26.275 | `OK` |
| `r4-rs` | `bf128` | `1/4` | 0.2500 | 28 | 32 | 19516.46 | 23413.637 | 22590.186 | 102.777 | `OK` |
| `r4-rs` | `bf128` | `1/4` | 0.2500 | 30 | 32 | 77718.22 | 77522.831 | 76535.864 | 416.500 | `OK` |
| `r4-rs` | `bf16` | `1/2` | 0.5000 | 20 | 32 | 12.09 | 14.555 | 14.026 | 0.014 | `OK` |
| `r4-rs` | `bf16` | `1/2` | 0.5000 | 22 | 32 | 38.18 | 40.411 | 40.964 | 0.084 | `OK` |
| `r4-rs` | `bf16` | `1/2` | 0.5000 | 24 | 32 | 154.03 | 135.409 | 131.906 | 0.410 | `OK` |
| `r4-rs` | `bf16` | `1/2` | 0.5000 | 26 | 32 | 573.09 | 587.147 | 555.718 | 1.729 | `OK` |
| `r4-rs` | `bf16` | `1/2` | 0.5000 | 28 | 32 | 2141.25 | 2597.022 | 2471.619 | 7.113 | `OK` |
| `r4-rs` | `bf16` | `1/2` | 0.5000 | 30 | 32 | 8338.53 | 10591.993 | 10524.816 | 28.684 | `OK` |
| `r4-rs` | `bf16` | `1/4` | 0.2500 | 20 | 32 | 21.28 | 27.049 | 26.382 | 0.027 | `OK` |
| `r4-rs` | `bf16` | `1/4` | 0.2500 | 22 | 32 | 77.69 | 90.366 | 88.264 | 0.193 | `OK` |
| `r4-rs` | `bf16` | `1/4` | 0.2500 | 24 | 32 | 307.15 | 306.859 | 303.418 | 0.803 | `OK` |
| `r4-rs` | `bf16` | `1/4` | 0.2500 | 26 | 32 | 1091.16 | 1224.867 | 1223.763 | 2.902 | `OK` |
| `r4-rs` | `bf16` | `1/4` | 0.2500 | 28 | 32 | 4253.07 | 5442.703 | 5355.564 | 13.449 | `OK` |
| `r4-rs` | `bf16` | `1/4` | 0.2500 | 30 | 32 | 16573.24 | 21938.496 | 21921.528 | 52.373 | `OK` |
| `r4-rs` | `bf32` | `1/2` | 0.5000 | 20 | 32 | 19.46 | 26.859 | 27.571 | 0.031 | `OK` |
| `r4-rs` | `bf32` | `1/2` | 0.5000 | 22 | 32 | 73.08 | 80.597 | 81.585 | 0.180 | `OK` |
| `r4-rs` | `bf32` | `1/2` | 0.5000 | 24 | 32 | 260.54 | 291.666 | 290.202 | 0.852 | `OK` |
| `r4-rs` | `bf32` | `1/2` | 0.5000 | 26 | 32 | 913.06 | 1247.662 | 1229.673 | 3.480 | `OK` |
| `r4-rs` | `bf32` | `1/2` | 0.5000 | 28 | 32 | 3546.69 | 4918.868 | 4977.221 | 14.176 | `OK` |
| `r4-rs` | `bf32` | `1/2` | 0.5000 | 30 | 32 | 13784.99 | 19812.971 | 19731.707 | 56.354 | `OK` |
| `r4-rs` | `bf32` | `1/4` | 0.2500 | 20 | 32 | 36.22 | 34.380 | 34.338 | 0.070 | `OK` |
| `r4-rs` | `bf32` | `1/4` | 0.2500 | 22 | 32 | 134.49 | 124.924 | 119.439 | 0.383 | `OK` |
| `r4-rs` | `bf32` | `1/4` | 0.2500 | 24 | 32 | 482.15 | 447.856 | 448.177 | 1.557 | `OK` |
| `r4-rs` | `bf32` | `1/4` | 0.2500 | 26 | 32 | 1808.58 | 1974.932 | 1933.080 | 6.668 | `OK` |
| `r4-rs` | `bf32` | `1/4` | 0.2500 | 28 | 32 | 6977.57 | 9068.382 | 8435.598 | 26.410 | `OK` |
| `r4-rs` | `bf32` | `1/4` | 0.2500 | 30 | 32 | 27484.74 | 37548.489 | 36893.007 | 107.406 | `OK` |
| `r4-rs` | `bf64` | `1/2` | 0.5000 | 20 | 32 | 25.88 | 30.996 | 30.247 | 0.076 | `OK` |
| `r4-rs` | `bf64` | `1/2` | 0.5000 | 22 | 32 | 96.36 | 81.659 | 84.106 | 0.395 | `OK` |
| `r4-rs` | `bf64` | `1/2` | 0.5000 | 24 | 32 | 347.08 | 319.222 | 316.556 | 1.709 | `OK` |
| `r4-rs` | `bf64` | `1/2` | 0.5000 | 26 | 32 | 1277.47 | 1318.016 | 1321.506 | 5.951 | `OK` |
| `r4-rs` | `bf64` | `1/2` | 0.5000 | 28 | 32 | 4874.62 | 5911.385 | 5438.234 | 26.822 | `OK` |
| `r4-rs` | `bf64` | `1/2` | 0.5000 | 30 | 32 | 18769.52 | 25065.653 | 24326.952 | 108.713 | `OK` |
| `r4-rs` | `bf64` | `1/4` | 0.2500 | 20 | 32 | 49.36 | 43.729 | 43.277 | 0.180 | `OK` |
| `r4-rs` | `bf64` | `1/4` | 0.2500 | 22 | 32 | 186.05 | 133.490 | 133.511 | 0.709 | `OK` |
| `r4-rs` | `bf64` | `1/4` | 0.2500 | 24 | 32 | 658.50 | 541.537 | 542.714 | 3.232 | `OK` |
| `r4-rs` | `bf64` | `1/4` | 0.2500 | 26 | 32 | 2485.27 | 2550.275 | 2380.776 | 13.008 | `OK` |
| `r4-rs` | `bf64` | `1/4` | 0.2500 | 28 | 32 | 9671.51 | 11499.688 | 10728.370 | 52.770 | `OK` |
| `r4-rs` | `bf64` | `1/4` | 0.2500 | 30 | 32 | 39172.55 | 43568.947 | 43238.944 | 203.146 | `OK` |
| `r8-rs` | `bf128` | `1/2` | 0.5000 | 20 | 32 | 40.98 | 30.672 | 30.922 | 0.174 | `OK` |
| `r8-rs` | `bf128` | `1/2` | 0.5000 | 22 | 32 | 153.53 | 160.317 | 145.250 | 0.729 | `OK` |
| `r8-rs` | `bf128` | `1/2` | 0.5000 | 24 | 32 | 532.33 | 476.229 | 478.876 | 2.994 | `OK` |
| `r8-rs` | `bf128` | `1/2` | 0.5000 | 26 | 32 | 2032.78 | 2265.097 | 2268.095 | 12.506 | `OK` |
| `r8-rs` | `bf128` | `1/2` | 0.5000 | 28 | 32 | 7863.80 | 10683.549 | 10726.252 | 48.902 | `OK` |
| `r8-rs` | `bf128` | `1/2` | 0.5000 | 30 | 32 | 30893.49 | 34882.388 | 34825.513 | 199.734 | `OK` |
| `r8-rs` | `bf128` | `1/4` | 0.2500 | 20 | 32 | 88.59 | 51.299 | 51.952 | 0.348 | `OK` |
| `r8-rs` | `bf128` | `1/4` | 0.2500 | 22 | 32 | 290.94 | 250.905 | 254.620 | 1.449 | `OK` |
| `r8-rs` | `bf128` | `1/4` | 0.2500 | 24 | 32 | 1042.07 | 990.023 | 970.465 | 5.875 | `OK` |
| `r8-rs` | `bf128` | `1/4` | 0.2500 | 26 | 32 | 4007.29 | 5093.240 | 4557.160 | 23.168 | `OK` |
| `r8-rs` | `bf128` | `1/4` | 0.2500 | 28 | 32 | 15649.34 | 20724.142 | 20755.471 | 95.156 | `OK` |
| `r8-rs` | `bf128` | `1/4` | 0.2500 | 30 | 32 | 62515.39 | 77260.421 | 66632.555 | 374.004 | `OK` |
| `r8-rs` | `bf16` | `1/2` | 0.5000 | 20 | 32 | 11.32 | 10.690 | 10.470 | 0.012 | `OK` |
| `r8-rs` | `bf16` | `1/2` | 0.5000 | 22 | 32 | 33.56 | 34.729 | 33.170 | 0.062 | `OK` |
| `r8-rs` | `bf16` | `1/2` | 0.5000 | 24 | 32 | 128.03 | 121.020 | 120.994 | 0.367 | `OK` |
| `r8-rs` | `bf16` | `1/2` | 0.5000 | 26 | 32 | 494.13 | 422.813 | 417.736 | 1.561 | `OK` |
| `r8-rs` | `bf16` | `1/2` | 0.5000 | 28 | 32 | 1829.20 | 2088.847 | 2097.242 | 6.268 | `OK` |
| `r8-rs` | `bf16` | `1/2` | 0.5000 | 30 | 32 | 7242.63 | 8301.624 | 8307.503 | 24.861 | `OK` |
| `r8-rs` | `bf16` | `1/4` | 0.2500 | 20 | 32 | 20.60 | 23.094 | 22.794 | 0.021 | `OK` |
| `r8-rs` | `bf16` | `1/4` | 0.2500 | 22 | 32 | 63.64 | 52.836 | 52.352 | 0.162 | `OK` |
| `r8-rs` | `bf16` | `1/4` | 0.2500 | 24 | 32 | 257.85 | 201.508 | 193.425 | 0.707 | `OK` |
| `r8-rs` | `bf16` | `1/4` | 0.2500 | 26 | 32 | 951.10 | 1009.904 | 987.056 | 2.900 | `OK` |
| `r8-rs` | `bf16` | `1/4` | 0.2500 | 28 | 32 | 3639.57 | 3804.835 | 3806.638 | 12.164 | `OK` |
| `r8-rs` | `bf16` | `1/4` | 0.2500 | 30 | 32 | 14287.42 | 15275.190 | 15293.210 | 48.342 | `OK` |
| `r8-rs` | `bf32` | `1/2` | 0.5000 | 20 | 32 | 17.87 | 22.365 | 22.682 | 0.016 | `OK` |
| `r8-rs` | `bf32` | `1/2` | 0.5000 | 22 | 32 | 62.20 | 49.380 | 49.272 | 0.182 | `OK` |
| `r8-rs` | `bf32` | `1/2` | 0.5000 | 24 | 32 | 227.38 | 177.423 | 177.108 | 0.756 | `OK` |
| `r8-rs` | `bf32` | `1/2` | 0.5000 | 26 | 32 | 795.69 | 970.342 | 961.474 | 3.148 | `OK` |
| `r8-rs` | `bf32` | `1/2` | 0.5000 | 28 | 32 | 3109.79 | 3657.617 | 3613.746 | 12.641 | `OK` |
| `r8-rs` | `bf32` | `1/2` | 0.5000 | 30 | 32 | 11973.20 | 14433.167 | 14425.075 | 48.635 | `OK` |
| `r8-rs` | `bf32` | `1/4` | 0.2500 | 20 | 32 | 30.50 | 31.516 | 28.616 | 0.055 | `OK` |
| `r8-rs` | `bf32` | `1/4` | 0.2500 | 22 | 32 | 116.38 | 120.736 | 120.002 | 0.340 | `OK` |
| `r8-rs` | `bf32` | `1/4` | 0.2500 | 24 | 32 | 416.75 | 373.167 | 368.461 | 1.475 | `OK` |
| `r8-rs` | `bf32` | `1/4` | 0.2500 | 26 | 32 | 1561.16 | 1758.615 | 1777.613 | 6.064 | `OK` |
| `r8-rs` | `bf32` | `1/4` | 0.2500 | 28 | 32 | 6054.21 | 7943.371 | 7923.565 | 23.541 | `OK` |
| `r8-rs` | `bf32` | `1/4` | 0.2500 | 30 | 32 | 23723.82 | 28941.055 | 28907.767 | 93.738 | `OK` |
| `r8-rs` | `bf64` | `1/2` | 0.5000 | 20 | 32 | 22.44 | 26.841 | 27.249 | 0.055 | `OK` |
| `r8-rs` | `bf64` | `1/2` | 0.5000 | 22 | 32 | 85.35 | 107.909 | 100.218 | 0.361 | `OK` |
| `r8-rs` | `bf64` | `1/2` | 0.5000 | 24 | 32 | 299.09 | 249.509 | 224.825 | 1.461 | `OK` |
| `r8-rs` | `bf64` | `1/2` | 0.5000 | 26 | 32 | 1103.48 | 1239.436 | 1143.561 | 6.010 | `OK` |
| `r8-rs` | `bf64` | `1/2` | 0.5000 | 28 | 32 | 4215.22 | 6764.207 | 6765.901 | 24.725 | `OK` |
| `r8-rs` | `bf64` | `1/2` | 0.5000 | 30 | 32 | 16555.12 | 19596.156 | 19427.341 | 97.678 | `OK` |
| `r8-rs` | `bf64` | `1/4` | 0.2500 | 20 | 32 | 41.01 | 37.710 | 38.784 | 0.160 | `OK` |
| `r8-rs` | `bf64` | `1/4` | 0.2500 | 22 | 32 | 154.70 | 132.539 | 133.144 | 0.730 | `OK` |
| `r8-rs` | `bf64` | `1/4` | 0.2500 | 24 | 32 | 565.98 | 532.700 | 475.796 | 2.842 | `OK` |
| `r8-rs` | `bf64` | `1/4` | 0.2500 | 26 | 32 | 2130.75 | 2437.848 | 2214.778 | 11.662 | `OK` |
| `r8-rs` | `bf64` | `1/4` | 0.2500 | 28 | 32 | 8373.36 | 10164.204 | 10122.407 | 47.752 | `OK` |
| `r8-rs` | `bf64` | `1/4` | 0.2500 | 30 | 32 | 32912.42 | 36273.473 | 35890.874 | 188.516 | `OK` |

## Notes & Boundaries

- `r2-rs` (`bf128`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r2-rs` (`bf128`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r2-rs` (`bf128`, config rate `1/4`, `OOM_LIMIT`): Default admissible mu0 rule. Encoder geometry only. exit=134; see raw/binary_1d-binary-hyperfold-r2-rs-bf128-30-4.
- `r2-rs` (`bf16`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r2-rs` (`bf16`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r2-rs` (`bf32`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r2-rs` (`bf32`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r2-rs` (`bf64`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r2-rs` (`bf64`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r4-rs` (`bf128`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r4-rs` (`bf128`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r4-rs` (`bf16`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r4-rs` (`bf16`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r4-rs` (`bf32`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r4-rs` (`bf32`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r4-rs` (`bf64`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r4-rs` (`bf64`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r8-rs` (`bf128`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r8-rs` (`bf128`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=7
- `r8-rs` (`bf128`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=9
- `r8-rs` (`bf128`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=7
- `r8-rs` (`bf128`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r8-rs` (`bf128`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=9
- `r8-rs` (`bf16`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=7
- `r8-rs` (`bf16`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r8-rs` (`bf16`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=9
- `r8-rs` (`bf16`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=9
- `r8-rs` (`bf16`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r8-rs` (`bf16`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=7
- `r8-rs` (`bf32`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=7
- `r8-rs` (`bf32`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=9
- `r8-rs` (`bf32`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r8-rs` (`bf32`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r8-rs` (`bf32`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=7
- `r8-rs` (`bf32`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=9
- `r8-rs` (`bf64`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=7
- `r8-rs` (`bf64`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=9
- `r8-rs` (`bf64`, config rate `1/2`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
- `r8-rs` (`bf64`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=9
- `r8-rs` (`bf64`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=7
- `r8-rs` (`bf64`, config rate `1/4`, `OK`): Default admissible mu0 rule. Encoder geometry only. mu0=8
