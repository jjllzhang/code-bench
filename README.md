# code-bench

Benchmark archive for **1D single-polynomial linear code encoders** used in code-based polynomial commitment schemes (PCS), structured after [`pcs-bench`](https://github.com/jjllzhang/pcs-bench) with paired `<code_family>.md` + `<code_family>.csv` files under [`results/`](results/) and an interactive report at [`docs/index.html`](docs/index.html).

> **Snapshot Status** (`2026-11-23 06:33Z`): `704` OK · `0` PENDING · `8` DOMAIN_LIMIT · `29` OOM_SKIPPED · `9` OOM_LIMIT · `12` EXCLUDED_INTERLEAVED · `24` UNSUPPORTED_BACKEND (`786` total grid points).

[Methods and reproduction commands](benchmarks/README.md) · [Campaign summary](evidence/REPORT.md) · [Raw timings and command logs](evidence/)

## Repository Structure

```text
code-bench/
├── README.md            # Index of benchmarked code families & same-actual-rate snapshots
├── TEMPLATE.md          # Markdown template for adding new code encoders
├── docs/
│   └── index.html       # Interactive PCS-Zoo-style viewer + SVG scaling charts
├── results/             # Paired <code_family>.md and <code_family>.csv files
│   └── tracks/          # Track CSVs (prime_goldilocks_1d, binary_1d, native_fields_1d)
└── scripts/
    └── build_view.py    # Rebuilds README, per-family MD/CSV, and docs/index.html from CSVs
```

## Benchmarked Code Families

| Code Family | Zoo # | Variants | Field(s) | Config Rates | Tested `k` | Status (`OK/Total`) | Data |
|---|---|---|---|---|---|---|---|
| Reed–Solomon (Multiplicative NTT Coset LDE) | #1 | `p3-coset-lde` | `babybear`, `goldilocks` | `1/2`, `1/4` | 20, 22, 24, 26, 28, 30 | 19/24 | [md](results/rs.md) · [csv](results/rs.csv) |
| Binary Additive Reed–Solomon (LCH14 / PolyBasis / Bolt-RS) | #3 | `bolt-rs`, `lch`, `polybasis` | `bf128`, `bf32`, `bf64` | `1/2`, `1/4` | 20, 22, 24, 26, 28, 30 | 60/84 | [md](results/additive-rs.md) · [csv](results/additive-rs.csv) |
| BaseFold Random Foldable Codes (r = 2) | #5 | `rs64-rfc` | `goldilocks`, `m127` | `1/2`, `1/4` | 20, 22, 24, 26, 28, 30 | 22/24 | [md](results/basefold.md) · [csv](results/basefold.csv) |
| Binary HyperFold High-Arity Foldable Codes (r ∈ {2,4,8}) | #5+ | `r2-rs`, `r4-rs`, `r8-rs` | `bf128`, `bf16`, `bf32`, `bf64` | `1/2`, `1/4` | 20, 22, 24, 26, 28, 30 | 143/144 | [md](results/binary-hyperfold.md) · [csv](results/binary-hyperfold.csv) |
| HyperFold High-Arity Hyper-Invertible Foldable Codes (r ∈ {2,4,8}) | #5+ | `r2-qa`, `r2-rs`, `r4-qa`, `r4-rs`, `r8-qa`, `r8-rs` | `goldilocks`, `m127` | `1/2`, `1/4` | 20, 22, 24, 26, 28, 30 | 144/144 | [md](results/hyperfold.md) · [csv](results/hyperfold.csv) |
| Systematic Quasi-Abelian Codes (WHT / Binary Spectral) | #6 | `binary-spectral`, `packed-wht` | `bf128`, `bf32-bf128`, `bf32-bf64`, `bf32`, `bf64-bf128`, `bf64`, `goldilocks`, `m127` | `1/2`, `1/4` | 20, 22, 24, 26, 28, 30 | 96/96 | [md](results/qa.md) · [csv](results/qa.csv) |
| Juxtaposed Expand–Accumulate (1D Explicit EA) | #7 | `ea-explicit`, `eacode-official` | `goldilocks`, `ristretto255`, `secp256k1` | `1/2`, `1/4` | 20, 22, 24, 26, 28, 30 | 18/36 | [md](results/ea.md) · [csv](results/ea.csv) |
| Repeat–Accumulate–Accumulate (1D RAA) | #11, #7 | `blaze-packed-u64`, `bolt-raa`, `eacode-official`, `raa-unweighted` | `bf128`, `bf32`, `bf64`, `goldilocks`, `ristretto255`, `secp256k1` | `1/2`, `1/4` | 20, 22, 24, 26, 28, 30 | 72/72 | [md](results/raa.md) · [csv](results/raa.csv) |
| Bolt Sketched Codes (bolt-xor / bolt32) | #9 | `bolt-xor`, `bolt32` | `bf32` | `1/2`, `1/4` | 20, 22, 24, 26, 28, 30 | 24/24 | [md](results/bolt.md) · [csv](results/bolt.csv) |
| Lightning (LDPC Sketch + Brakedown Inner Code) | #13 | `ldpc-brakedown` | `bn254` | `half`, `native-high`, `native-low` | 20, 22, 24, 26, 28, 30 | 17/18 | [md](results/lightning.md) · [csv](results/lightning.csv) |
| Brakedown / Generalized Spielman Expander Codes | #12 | `bolt-binary`, `brakedown-recursive`, `plonkish-sdig3`, `sdig2`, `sdig3` | `bf32`, `ft127`, `goldilocks`, `m127`, `secp256k1` | `1/2`, `1/4`, `native-high`, `native-low`, `native` | 20, 22, 24, 26, 28, 30 | 58/72 | [md](results/brakedown.md) · [csv](results/brakedown.csv) |
| SIMD-Spielman (Mersenne61 / Monty64) | #12 | `simd-mt` | `m61`, `monty64` | `native` | 20, 22, 24, 26, 28, 30 | 0/12 | [md](results/spielman.md) · [csv](results/spielman.csv) |
| SPIN Binary Structured Linear Codes (IMT / Packet-RS8) | #19 | `imt`, `packet` | `block128` | `1/2` | 20, 22, 24, 26, 28, 30 | 10/12 | [md](results/spin.md) · [csv](results/spin.csv) |
| ERA (Encode–Repeat–Accumulate) | #20 | `brakedown-repeat-accumulate` | `goldilocks`, `secp256k1` | `1/2`, `1/4` | 20, 22, 24, 26, 28, 30 | 21/24 | [md](results/era.md) · [csv](results/era.csv) |

## Same-Field & Same-Actual-Rate Snapshot (Completed `OK` Rows)

Rows group by track, field, exact `K/N`, and `k`, then sort by mean encode time. The four-decimal rates are display values.

### `binary_1d` · `bf128` · actual `K/N = 1/4` (0.2500) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/polybasis` | #3 | `1/4` | 0.2500 | 7.536 | 7.405 | 0.078 |
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 9.318 | 9.315 | 0.064 |
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 17.534 | 17.209 | 0.119 |
| `raa/bolt-raa` | #11 | `1/4` | 0.2500 | 35.179 | 35.009 | 0.205 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 51.299 | 51.952 | 0.348 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 68.118 | 66.181 | 0.402 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 93.282 | 92.240 | 0.426 |

### `binary_1d` · `bf128` · actual `K/N = 1/4` (0.2500) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 36.266 | 36.244 | 0.299 |
| `additive-rs/polybasis` | #3 | `1/4` | 0.2500 | 51.521 | 51.206 | 0.314 |
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 62.481 | 59.868 | 0.535 |
| `raa/bolt-raa` | #11 | `1/4` | 0.2500 | 130.626 | 130.667 | 0.814 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 245.967 | 244.565 | 1.609 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 250.905 | 254.620 | 1.449 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 369.812 | 366.699 | 2.031 |

### `binary_1d` · `bf128` · actual `K/N = 1/4` (0.2500) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 147.517 | 147.544 | 1.246 |
| `additive-rs/polybasis` | #3 | `1/4` | 0.2500 | 168.257 | 168.139 | 1.252 |
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 348.339 | 346.437 | 2.221 |
| `raa/bolt-raa` | #11 | `1/4` | 0.2500 | 552.181 | 531.889 | 3.252 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 990.023 | 970.465 | 5.875 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 1197.371 | 1136.060 | 6.125 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 1665.029 | 1599.032 | 7.674 |

### `binary_1d` · `bf128` · actual `K/N = 1/4` (0.2500) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 612.931 | 590.190 | 4.986 |
| `additive-rs/polybasis` | #3 | `1/4` | 0.2500 | 685.705 | 687.349 | 5.002 |
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 1594.826 | 1596.003 | 8.969 |
| `raa/bolt-raa` | #11 | `1/4` | 0.2500 | 2242.782 | 2188.237 | 13.002 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 5093.240 | 4557.160 | 23.168 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 5675.636 | 5047.777 | 26.275 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 7620.194 | 7697.087 | 32.836 |

### `binary_1d` · `bf128` · actual `K/N = 1/4` (0.2500) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/polybasis` | #3 | `1/4` | 0.2500 | 2089.195 | 2090.391 | 19.994 |
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 3114.147 | 3129.605 | 19.977 |
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 7020.359 | 7022.656 | 35.979 |
| `raa/bolt-raa` | #11 | `1/4` | 0.2500 | 9477.657 | 9482.879 | 52.002 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 20724.142 | 20755.471 | 95.156 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 23413.637 | 22590.186 | 102.777 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 31684.358 | 31671.930 | 115.566 |

### `binary_1d` · `bf128` · actual `K/N = 1/4` (0.2500) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/polybasis` | #3 | `1/4` | 0.2500 | 7997.710 | 7992.449 | 79.998 |
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 13054.488 | 13330.975 | 79.979 |
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 26180.974 | 26151.554 | 143.971 |
| `raa/bolt-raa` | #11 | `1/4` | 0.2500 | 40066.773 | 42115.032 | 208.002 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 77260.421 | 66632.555 | 374.004 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 77522.831 | 76535.864 | 416.500 |

### `binary_1d` · `bf128` · actual `K/N = 1/2` (0.5000) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/polybasis` | #3 | `1/2` | 0.5000 | 4.483 | 4.470 | 0.049 |
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 5.298 | 5.386 | 0.021 |
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 8.272 | 8.304 | 0.053 |
| `raa/bolt-raa` | #11 | `1/2` | 0.5000 | 16.805 | 16.810 | 0.111 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 30.672 | 30.922 | 0.174 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 42.512 | 43.765 | 0.186 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 67.535 | 65.972 | 0.242 |

### `binary_1d` · `bf128` · actual `K/N = 1/2` (0.5000) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 23.690 | 23.296 | 0.156 |
| `additive-rs/polybasis` | #3 | `1/2` | 0.5000 | 27.208 | 28.308 | 0.188 |
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 41.201 | 41.309 | 0.285 |
| `raa/bolt-raa` | #11 | `1/2` | 0.5000 | 66.554 | 65.672 | 0.439 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 143.954 | 132.104 | 0.805 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 160.317 | 145.250 | 0.729 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 224.285 | 209.599 | 1.033 |

### `binary_1d` · `bf128` · actual `K/N = 1/2` (0.5000) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/polybasis` | #3 | `1/2` | 0.5000 | 81.539 | 79.701 | 0.752 |
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 89.084 | 89.048 | 0.744 |
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 176.686 | 176.287 | 1.232 |
| `raa/bolt-raa` | #11 | `1/2` | 0.5000 | 255.337 | 255.392 | 1.752 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 476.229 | 478.876 | 2.994 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 647.437 | 637.646 | 3.393 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 898.649 | 887.508 | 4.189 |

### `binary_1d` · `bf128` · actual `K/N = 1/2` (0.5000) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 358.549 | 358.758 | 2.996 |
| `additive-rs/polybasis` | #3 | `1/2` | 0.5000 | 371.011 | 370.898 | 3.002 |
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 807.181 | 807.675 | 4.973 |
| `raa/bolt-raa` | #11 | `1/2` | 0.5000 | 1047.442 | 1048.529 | 7.002 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 2265.097 | 2268.095 | 12.506 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 2779.495 | 2825.384 | 13.639 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 3604.585 | 3599.058 | 17.225 |

### `binary_1d` · `bf128` · actual `K/N = 1/2` (0.5000) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/polybasis` | #3 | `1/2` | 0.5000 | 1125.488 | 1115.038 | 12.002 |
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 1843.905 | 1838.489 | 11.977 |
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 3530.756 | 3530.734 | 19.975 |
| `raa/bolt-raa` | #11 | `1/2` | 0.5000 | 4324.470 | 4316.415 | 28.002 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 10683.549 | 10726.252 | 48.902 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 12044.337 | 11904.096 | 53.219 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 15894.805 | 15937.517 | 66.939 |

### `binary_1d` · `bf128` · actual `K/N = 1/2` (0.5000) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/polybasis` | #3 | `1/2` | 0.5000 | 4244.557 | 4233.646 | 47.998 |
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 8023.440 | 8031.899 | 47.979 |
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 15412.375 | 15406.692 | 79.975 |
| `raa/bolt-raa` | #11 | `1/2` | 0.5000 | 20586.482 | 20612.302 | 112.002 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 34882.388 | 34825.513 | 199.734 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 43610.472 | 39235.355 | 215.277 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 57187.358 | 57248.211 | 284.582 |

### `binary_1d` · `bf16` · actual `K/N = 1/4` (0.2500) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 23.094 | 22.794 | 0.021 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 27.049 | 26.382 | 0.027 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 44.491 | 43.520 | 0.037 |

### `binary_1d` · `bf16` · actual `K/N = 1/4` (0.2500) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 52.836 | 52.352 | 0.162 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 90.366 | 88.264 | 0.193 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 133.378 | 136.015 | 0.252 |

### `binary_1d` · `bf16` · actual `K/N = 1/4` (0.2500) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 201.508 | 193.425 | 0.707 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 306.859 | 303.418 | 0.803 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 481.952 | 477.019 | 1.012 |

### `binary_1d` · `bf16` · actual `K/N = 1/4` (0.2500) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 1009.904 | 987.056 | 2.900 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 1224.867 | 1223.763 | 2.902 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 1833.629 | 1837.229 | 4.080 |

### `binary_1d` · `bf16` · actual `K/N = 1/4` (0.2500) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 3804.835 | 3806.638 | 12.164 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 5442.703 | 5355.564 | 13.449 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 7540.591 | 7534.839 | 17.352 |

### `binary_1d` · `bf16` · actual `K/N = 1/4` (0.2500) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 15275.190 | 15293.210 | 48.342 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 21938.496 | 21921.528 | 52.373 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 32916.296 | 31518.363 | 69.342 |

### `binary_1d` · `bf16` · actual `K/N = 1/2` (0.5000) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 10.690 | 10.470 | 0.012 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 14.555 | 14.026 | 0.014 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 27.337 | 27.412 | 0.021 |

### `binary_1d` · `bf16` · actual `K/N = 1/2` (0.5000) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 34.729 | 33.170 | 0.062 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 40.411 | 40.964 | 0.084 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 74.476 | 75.287 | 0.105 |

### `binary_1d` · `bf16` · actual `K/N = 1/2` (0.5000) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 121.020 | 120.994 | 0.367 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 135.409 | 131.906 | 0.410 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 258.077 | 247.720 | 0.529 |

### `binary_1d` · `bf16` · actual `K/N = 1/2` (0.5000) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 422.813 | 417.736 | 1.561 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 587.147 | 555.718 | 1.729 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 950.883 | 959.447 | 2.156 |

### `binary_1d` · `bf16` · actual `K/N = 1/2` (0.5000) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 2088.847 | 2097.242 | 6.268 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 2597.022 | 2471.619 | 7.113 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 3787.602 | 3789.614 | 9.123 |

### `binary_1d` · `bf16` · actual `K/N = 1/2` (0.5000) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 8301.624 | 8307.503 | 24.861 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 10591.993 | 10524.816 | 28.684 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 15839.110 | 15850.100 | 33.188 |

### `binary_1d` · `bf32` · actual `K/N = 1/4` (0.2500) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 7.305 | 7.306 | 0.018 |
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 10.599 | 10.618 | 0.006 |
| `raa/bolt-raa` | #11 | `1/4` | 0.2500 | 26.563 | 26.751 | 0.100 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 31.516 | 28.616 | 0.055 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 34.380 | 34.338 | 0.070 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 52.461 | 50.973 | 0.102 |
| `additive-rs/bolt-rs` | #3 | `1/4` | 0.2500 | 81.573 | 81.582 | 0.041 |
| `brakedown/bolt-binary` | #12 | `1/4` | 0.2500 | 1397.999 | 1398.097 | 0.789 |

### `binary_1d` · `bf32` · actual `K/N = 1/4` (0.2500) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 22.967 | 23.087 | 0.121 |
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 28.307 | 27.673 | 0.051 |
| `raa/bolt-raa` | #11 | `1/4` | 0.2500 | 111.124 | 110.929 | 0.393 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 120.736 | 120.002 | 0.340 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 124.924 | 119.439 | 0.383 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 177.215 | 176.342 | 0.498 |
| `additive-rs/bolt-rs` | #3 | `1/4` | 0.2500 | 344.718 | 344.752 | 0.158 |
| `brakedown/bolt-binary` | #12 | `1/4` | 0.2500 | 6322.227 | 6370.706 | 3.148 |

### `binary_1d` · `bf32` · actual `K/N = 1/4` (0.2500) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 85.440 | 85.012 | 0.541 |
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 103.025 | 104.024 | 0.289 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 373.167 | 368.461 | 1.475 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 447.856 | 448.177 | 1.557 |
| `raa/bolt-raa` | #11 | `1/4` | 0.2500 | 455.238 | 455.496 | 1.564 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 724.414 | 700.913 | 2.105 |
| `additive-rs/bolt-rs` | #3 | `1/4` | 0.2500 | 1460.502 | 1462.607 | 0.627 |
| `brakedown/bolt-binary` | #12 | `1/4` | 0.2500 | 26545.893 | 26615.702 | 12.590 |

### `binary_1d` · `bf32` · actual `K/N = 1/4` (0.2500) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 428.128 | 406.051 | 1.242 |
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 441.630 | 438.574 | 2.223 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 1758.615 | 1777.613 | 6.064 |
| `raa/bolt-raa` | #11 | `1/4` | 0.2500 | 1896.638 | 1923.539 | 6.252 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 1974.932 | 1933.080 | 6.668 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 3033.422 | 2943.743 | 8.555 |
| `additive-rs/bolt-rs` | #3 | `1/4` | 0.2500 | 7054.133 | 7049.040 | 2.502 |
| `brakedown/bolt-binary` | #12 | `1/4` | 0.2500 | 109951.540 | 110218.636 | 50.357 |

### `binary_1d` · `bf32` · actual `K/N = 1/4` (0.2500) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 1731.166 | 1713.821 | 4.990 |
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 1960.591 | 1962.118 | 8.971 |
| `raa/bolt-raa` | #11 | `1/4` | 0.2500 | 7663.558 | 7638.992 | 25.002 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 7943.371 | 7923.565 | 23.541 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 9068.382 | 8435.598 | 26.410 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 12785.534 | 12750.779 | 33.279 |
| `additive-rs/bolt-rs` | #3 | `1/4` | 0.2500 | 31995.064 | 31991.939 | 10.002 |
| `brakedown/bolt-binary` | #12 | `1/4` | 0.2500 | 463395.539 | 458690.160 | 201.428 |

### `binary_1d` · `bf32` · actual `K/N = 1/4` (0.2500) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 7485.276 | 7602.427 | 19.975 |
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 8414.776 | 8400.059 | 35.971 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 28941.055 | 28907.767 | 93.738 |
| `raa/bolt-raa` | #11 | `1/4` | 0.2500 | 34157.845 | 33873.535 | 100.002 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 37548.489 | 36893.007 | 107.406 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 55494.181 | 55122.215 | 133.879 |
| `additive-rs/bolt-rs` | #3 | `1/4` | 0.2500 | 150013.433 | 150013.919 | 40.002 |

### `binary_1d` · `bf32` · actual `K/N = 1/2` (0.5000) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 3.378 | 3.383 | 0.010 |
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 6.872 | 6.930 | 0.006 |
| `raa/bolt-raa` | #11 | `1/2` | 0.5000 | 12.357 | 12.362 | 0.053 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 22.365 | 22.682 | 0.016 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 26.859 | 27.571 | 0.031 |
| `additive-rs/bolt-rs` | #3 | `1/2` | 0.5000 | 41.404 | 41.415 | 0.025 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 42.244 | 40.948 | 0.039 |
| `brakedown/bolt-binary` | #12 | `1/2` | 0.5000 | 507.178 | 506.602 | 0.543 |

### `binary_1d` · `bf32` · actual `K/N = 1/2` (0.5000) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 10.239 | 10.153 | 0.053 |
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 20.562 | 20.645 | 0.018 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 49.380 | 49.272 | 0.182 |
| `raa/bolt-raa` | #11 | `1/2` | 0.5000 | 56.548 | 56.337 | 0.205 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 80.597 | 81.585 | 0.180 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 132.108 | 129.537 | 0.252 |
| `additive-rs/bolt-rs` | #3 | `1/2` | 0.5000 | 174.759 | 174.763 | 0.096 |
| `brakedown/bolt-binary` | #12 | `1/2` | 0.5000 | 2263.051 | 2267.681 | 2.170 |

### `binary_1d` · `bf32` · actual `K/N = 1/2` (0.5000) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 52.271 | 51.325 | 0.283 |
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 56.579 | 57.135 | 0.154 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 177.423 | 177.108 | 0.756 |
| `raa/bolt-raa` | #11 | `1/2` | 0.5000 | 220.213 | 220.039 | 0.814 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 291.666 | 290.202 | 0.852 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 469.637 | 453.584 | 1.102 |
| `additive-rs/bolt-rs` | #3 | `1/2` | 0.5000 | 740.898 | 742.036 | 0.377 |
| `brakedown/bolt-binary` | #12 | `1/2` | 0.5000 | 9364.289 | 9311.654 | 8.676 |

### `binary_1d` · `bf32` · actual `K/N = 1/2` (0.5000) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 214.622 | 219.598 | 1.230 |
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 214.911 | 213.968 | 0.740 |
| `raa/bolt-raa` | #11 | `1/2` | 0.5000 | 903.144 | 900.922 | 3.252 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 970.342 | 961.474 | 3.148 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 1247.662 | 1229.673 | 3.480 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 1758.934 | 1761.594 | 4.588 |
| `additive-rs/bolt-rs` | #3 | `1/2` | 0.5000 | 3456.038 | 3450.693 | 1.502 |
| `brakedown/bolt-binary` | #12 | `1/2` | 0.5000 | 37946.374 | 38033.185 | 34.699 |

### `binary_1d` · `bf32` · actual `K/N = 1/2` (0.5000) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 920.602 | 918.690 | 4.979 |
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 930.558 | 926.804 | 2.990 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 3657.617 | 3613.746 | 12.641 |
| `raa/bolt-raa` | #11 | `1/2` | 0.5000 | 4323.220 | 4324.264 | 13.002 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 4918.868 | 4977.221 | 14.176 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 7309.237 | 7364.469 | 17.699 |
| `additive-rs/bolt-rs` | #3 | `1/2` | 0.5000 | 15774.159 | 15793.000 | 6.002 |
| `brakedown/bolt-binary` | #12 | `1/2` | 0.5000 | 154455.809 | 153913.563 | 138.795 |

### `binary_1d` · `bf32` · actual `K/N = 1/2` (0.5000) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 3876.730 | 3856.658 | 11.975 |
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 4036.944 | 4025.007 | 19.973 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 14433.167 | 14425.075 | 48.635 |
| `raa/bolt-raa` | #11 | `1/2` | 0.5000 | 15538.693 | 15508.369 | 52.002 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 19812.971 | 19731.707 | 56.354 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 30569.822 | 30566.420 | 67.121 |
| `additive-rs/bolt-rs` | #3 | `1/2` | 0.5000 | 72040.298 | 72038.301 | 24.002 |

### `binary_1d` · `bf32` · actual `K/N = 1048576/2072285` (0.5060) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/bolt-binary` | #12 | `native-low` | 0.5060 | 515.606 | 515.082 | 0.537 |

### `binary_1d` · `bf32` · actual `K/N = 134217728/265252427` (0.5060) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/bolt-binary` | #12 | `native-low` | 0.5060 | 152970.334 | 152618.571 | 136.969 |

### `binary_1d` · `bf32` · actual `K/N = 67108864/132626213` (0.5060) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/bolt-binary` | #12 | `native-low` | 0.5060 | 36735.619 | 36265.009 | 34.242 |

### `binary_1d` · `bf32` · actual `K/N = 16777216/33156553` (0.5060) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/bolt-binary` | #12 | `native-low` | 0.5060 | 9133.742 | 9141.437 | 8.562 |

### `binary_1d` · `bf32` · actual `K/N = 2097152/4144569` (0.5060) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/bolt-binary` | #12 | `native-low` | 0.5060 | 2195.020 | 2210.601 | 2.141 |

### `binary_1d` · `bf32` · actual `K/N = 2/3` (0.6667) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `bolt/bolt-xor` | #9 | `1/4` | 0.6667 | 85.791 | 85.838 | 0.156 |
| `bolt/bolt32` | #9 | `1/4` | 0.6667 | 86.429 | 86.496 | 0.197 |

### `binary_1d` · `bf32` · actual `K/N = 2/3` (0.6667) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `bolt/bolt-xor` | #9 | `1/4` | 0.6667 | 345.389 | 343.579 | 0.592 |
| `bolt/bolt32` | #9 | `1/4` | 0.6667 | 346.262 | 345.729 | 0.787 |

### `binary_1d` · `bf32` · actual `K/N = 2/3` (0.6667) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `bolt/bolt-xor` | #9 | `1/4` | 0.6667 | 1398.237 | 1392.450 | 2.361 |
| `bolt/bolt32` | #9 | `1/4` | 0.6667 | 1407.271 | 1398.032 | 3.143 |

### `binary_1d` · `bf32` · actual `K/N = 2/3` (0.6667) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `bolt/bolt-xor` | #9 | `1/4` | 0.6667 | 5577.472 | 5574.154 | 9.439 |
| `bolt/bolt32` | #9 | `1/4` | 0.6667 | 5712.088 | 5712.893 | 12.564 |

### `binary_1d` · `bf32` · actual `K/N = 2/3` (0.6667) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `bolt/bolt-xor` | #9 | `1/4` | 0.6667 | 22460.001 | 22341.327 | 37.752 |
| `bolt/bolt32` | #9 | `1/4` | 0.6667 | 22883.851 | 22831.240 | 50.252 |

### `binary_1d` · `bf32` · actual `K/N = 2/3` (0.6667) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `bolt/bolt-xor` | #9 | `1/4` | 0.6667 | 87469.614 | 87328.535 | 151.002 |
| `bolt/bolt32` | #9 | `1/4` | 0.6667 | 92324.786 | 92193.233 | 201.002 |

### `binary_1d` · `bf32` · actual `K/N = 1048576/1555751` (0.6740) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/bolt-binary` | #12 | `native-high` | 0.6740 | 290.791 | 291.020 | 0.516 |

### `binary_1d` · `bf32` · actual `K/N = 4194304/6223003` (0.6740) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/bolt-binary` | #12 | `native-high` | 0.6740 | 1184.306 | 1187.261 | 2.062 |

### `binary_1d` · `bf32` · actual `K/N = 4194304/6223003` (0.6740) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/bolt-binary` | #12 | `native-high` | 0.6740 | 4912.492 | 4926.631 | 8.242 |

### `binary_1d` · `bf32` · actual `K/N = 134217728/199136095` (0.6740) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/bolt-binary` | #12 | `native-high` | 0.6740 | 79073.194 | 79121.073 | 131.867 |

### `binary_1d` · `bf32` · actual `K/N = 67108864/99568047` (0.6740) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/bolt-binary` | #12 | `native-high` | 0.6740 | 19526.467 | 19524.203 | 32.967 |

### `binary_1d` · `bf32` · actual `K/N = 4/5` (0.8000) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `bolt/bolt32` | #9 | `1/2` | 0.8000 | 80.909 | 80.283 | 0.197 |
| `bolt/bolt-xor` | #9 | `1/2` | 0.8000 | 81.817 | 81.641 | 0.150 |

### `binary_1d` · `bf32` · actual `K/N = 4/5` (0.8000) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `bolt/bolt32` | #9 | `1/2` | 0.8000 | 320.895 | 320.876 | 0.785 |
| `bolt/bolt-xor` | #9 | `1/2` | 0.8000 | 325.655 | 324.767 | 0.576 |

### `binary_1d` · `bf32` · actual `K/N = 4/5` (0.8000) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `bolt/bolt-xor` | #9 | `1/2` | 0.8000 | 1310.895 | 1306.998 | 2.268 |
| `bolt/bolt32` | #9 | `1/2` | 0.8000 | 1387.811 | 1389.552 | 3.143 |

### `binary_1d` · `bf32` · actual `K/N = 4/5` (0.8000) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `bolt/bolt-xor` | #9 | `1/2` | 0.8000 | 5045.230 | 5030.381 | 9.064 |
| `bolt/bolt32` | #9 | `1/2` | 0.8000 | 5359.735 | 5355.899 | 12.564 |

### `binary_1d` · `bf32` · actual `K/N = 4/5` (0.8000) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `bolt/bolt-xor` | #9 | `1/2` | 0.8000 | 20558.636 | 20561.149 | 36.252 |
| `bolt/bolt32` | #9 | `1/2` | 0.8000 | 20879.130 | 20863.408 | 50.252 |

### `binary_1d` · `bf32` · actual `K/N = 4/5` (0.8000) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `bolt/bolt-xor` | #9 | `1/2` | 0.8000 | 80798.224 | 80809.058 | 145.002 |
| `bolt/bolt32` | #9 | `1/2` | 0.8000 | 82233.740 | 82040.880 | 201.002 |

### `binary_1d` · `bf32-bf128` · actual `K/N = 1/4` (0.2500) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 18.131 | 17.821 | 0.078 |

### `binary_1d` · `bf32-bf128` · actual `K/N = 1/4` (0.2500) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 56.080 | 54.451 | 0.443 |

### `binary_1d` · `bf32-bf128` · actual `K/N = 1/4` (0.2500) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 295.334 | 295.105 | 1.855 |

### `binary_1d` · `bf32-bf128` · actual `K/N = 1/4` (0.2500) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 1353.296 | 1353.195 | 7.477 |

### `binary_1d` · `bf32-bf128` · actual `K/N = 1/4` (0.2500) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 5961.507 | 5961.057 | 29.973 |

### `binary_1d` · `bf32-bf128` · actual `K/N = 1/4` (0.2500) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 23708.360 | 23693.480 | 119.969 |

### `binary_1d` · `bf32-bf128` · actual `K/N = 1/2` (0.5000) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 7.192 | 6.767 | 0.023 |

### `binary_1d` · `bf32-bf128` · actual `K/N = 1/2` (0.5000) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 31.167 | 31.770 | 0.193 |

### `binary_1d` · `bf32-bf128` · actual `K/N = 1/2` (0.5000) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 122.673 | 120.488 | 0.850 |

### `binary_1d` · `bf32-bf128` · actual `K/N = 1/2` (0.5000) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 548.779 | 547.748 | 3.477 |

### `binary_1d` · `bf32-bf128` · actual `K/N = 1/2` (0.5000) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 2478.662 | 2425.619 | 13.971 |

### `binary_1d` · `bf32-bf128` · actual `K/N = 1/2` (0.5000) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 10456.858 | 10451.568 | 55.967 |

### `binary_1d` · `bf32-bf64` · actual `K/N = 1/4` (0.2500) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 7.905 | 7.744 | 0.031 |

### `binary_1d` · `bf32-bf64` · actual `K/N = 1/4` (0.2500) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 30.599 | 31.891 | 0.219 |

### `binary_1d` · `bf32-bf64` · actual `K/N = 1/4` (0.2500) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 137.236 | 134.708 | 0.973 |

### `binary_1d` · `bf32-bf64` · actual `K/N = 1/4` (0.2500) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 657.362 | 657.464 | 3.977 |

### `binary_1d` · `bf32-bf64` · actual `K/N = 1/4` (0.2500) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 2979.390 | 2975.588 | 15.975 |

### `binary_1d` · `bf32-bf64` · actual `K/N = 1/4` (0.2500) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 13207.516 | 13184.763 | 63.969 |

### `binary_1d` · `bf32-bf64` · actual `K/N = 1/2` (0.5000) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 3.688 | 3.702 | 0.014 |

### `binary_1d` · `bf32-bf64` · actual `K/N = 1/2` (0.5000) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 14.098 | 14.156 | 0.104 |

### `binary_1d` · `bf32-bf64` · actual `K/N = 1/2` (0.5000) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 67.328 | 66.871 | 0.477 |

### `binary_1d` · `bf32-bf64` · actual `K/N = 1/2` (0.5000) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 295.596 | 294.104 | 1.975 |

### `binary_1d` · `bf32-bf64` · actual `K/N = 1/2` (0.5000) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 1350.909 | 1348.472 | 7.969 |

### `binary_1d` · `bf32-bf64` · actual `K/N = 1/2` (0.5000) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 5890.914 | 5867.309 | 31.969 |

### `binary_1d` · `bf64` · actual `K/N = 1/4` (0.2500) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 9.435 | 9.266 | 0.035 |
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 11.247 | 10.681 | 0.012 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 37.710 | 38.784 | 0.160 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 43.729 | 43.277 | 0.180 |
| `raa/blaze-packed-u64` | #11 | `1/4` | 0.2500 | 51.001 | 50.651 | 0.111 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 64.991 | 65.194 | 0.211 |

### `binary_1d` · `bf64` · actual `K/N = 1/4` (0.2500) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 32.917 | 31.718 | 0.145 |
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 37.295 | 36.816 | 0.260 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 132.539 | 133.144 | 0.730 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 133.490 | 133.511 | 0.709 |
| `raa/blaze-packed-u64` | #11 | `1/4` | 0.2500 | 190.867 | 181.475 | 0.537 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 206.241 | 208.029 | 0.918 |

### `binary_1d` · `bf64` · actual `K/N = 1/4` (0.2500) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 115.469 | 115.495 | 0.607 |
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 161.218 | 160.476 | 1.104 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 532.700 | 475.796 | 2.842 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 541.537 | 542.714 | 3.232 |
| `raa/blaze-packed-u64` | #11 | `1/4` | 0.2500 | 800.483 | 772.176 | 2.223 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 894.361 | 854.895 | 4.354 |

### `binary_1d` · `bf64` · actual `K/N = 1/4` (0.2500) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 489.328 | 466.414 | 2.484 |
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 795.119 | 794.592 | 4.473 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 2437.848 | 2214.778 | 11.662 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 2550.275 | 2380.776 | 13.008 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 3622.987 | 3615.909 | 16.402 |
| `raa/blaze-packed-u64` | #11 | `1/4` | 0.2500 | 3696.387 | 3600.439 | 8.977 |

### `binary_1d` · `bf64` · actual `K/N = 1/4` (0.2500) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 2286.234 | 2286.231 | 9.979 |
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 3475.431 | 3476.174 | 17.979 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 10164.204 | 10122.407 | 47.752 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 11499.688 | 10728.370 | 52.770 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 16985.891 | 15774.553 | 68.953 |
| `raa/blaze-packed-u64` | #11 | `1/4` | 0.2500 | 20745.094 | 20815.890 | 35.977 |

### `binary_1d` · `bf64` · actual `K/N = 1/4` (0.2500) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/4` | 0.2500 | 9347.412 | 9646.798 | 39.979 |
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 15887.404 | 15282.516 | 71.973 |
| `binary-hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 36273.473 | 35890.874 | 188.516 |
| `binary-hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 43568.947 | 43238.944 | 203.146 |
| `binary-hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 67859.635 | 67623.856 | 271.803 |
| `raa/blaze-packed-u64` | #11 | `1/4` | 0.2500 | 162869.537 | 167116.316 | 143.979 |

### `binary_1d` · `bf64` · actual `K/N = 1/2` (0.5000) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 4.607 | 4.584 | 0.018 |
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 7.205 | 7.217 | 0.010 |
| `raa/blaze-packed-u64` | #11 | `1/2` | 0.5000 | 24.577 | 24.596 | 0.049 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 26.841 | 27.249 | 0.055 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 30.996 | 30.247 | 0.076 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 45.473 | 46.133 | 0.107 |

### `binary_1d` · `bf64` · actual `K/N = 1/2` (0.5000) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 16.543 | 16.507 | 0.139 |
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 20.972 | 21.637 | 0.072 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 81.659 | 84.106 | 0.395 |
| `raa/blaze-packed-u64` | #11 | `1/2` | 0.5000 | 88.804 | 90.521 | 0.285 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 107.909 | 100.218 | 0.361 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 145.343 | 136.879 | 0.523 |

### `binary_1d` · `bf64` · actual `K/N = 1/2` (0.5000) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 63.304 | 63.025 | 0.363 |
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 86.079 | 84.503 | 0.602 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 249.509 | 224.825 | 1.461 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 319.222 | 316.556 | 1.709 |
| `raa/blaze-packed-u64` | #11 | `1/2` | 0.5000 | 406.414 | 384.633 | 1.221 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 523.733 | 519.612 | 1.914 |

### `binary_1d` · `bf64` · actual `K/N = 1/2` (0.5000) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 254.303 | 254.292 | 1.480 |
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 392.513 | 391.928 | 2.477 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 1239.436 | 1143.561 | 6.010 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 1318.016 | 1321.506 | 5.951 |
| `raa/blaze-packed-u64` | #11 | `1/2` | 0.5000 | 1858.924 | 1904.414 | 4.975 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 2131.934 | 2074.758 | 8.424 |

### `binary_1d` · `bf64` · actual `K/N = 1/2` (0.5000) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 1227.432 | 1226.536 | 5.975 |
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 1769.486 | 1769.769 | 9.977 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 5911.385 | 5438.234 | 26.822 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 6764.207 | 6765.901 | 24.725 |
| `raa/blaze-packed-u64` | #11 | `1/2` | 0.5000 | 7846.995 | 7624.032 | 19.979 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 8843.170 | 8466.205 | 35.359 |

### `binary_1d` · `bf64` · actual `K/N = 1/2` (0.5000) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `additive-rs/lch` | #3 | `1/2` | 0.5000 | 5253.158 | 5271.374 | 23.979 |
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 7714.876 | 7723.587 | 39.975 |
| `binary-hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 19596.156 | 19427.341 | 97.678 |
| `binary-hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 25065.653 | 24326.952 | 108.713 |
| `binary-hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 35976.550 | 35164.853 | 135.908 |
| `raa/blaze-packed-u64` | #11 | `1/2` | 0.5000 | 62814.142 | 63108.595 | 79.971 |

### `binary_1d` · `bf64-bf128` · actual `K/N = 1/4` (0.2500) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 14.312 | 14.470 | 0.086 |

### `binary_1d` · `bf64-bf128` · actual `K/N = 1/4` (0.2500) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 60.412 | 60.020 | 0.475 |

### `binary_1d` · `bf64-bf128` · actual `K/N = 1/4` (0.2500) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 283.993 | 282.082 | 1.977 |

### `binary_1d` · `bf64-bf128` · actual `K/N = 1/4` (0.2500) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 1313.537 | 1308.738 | 7.967 |

### `binary_1d` · `bf64-bf128` · actual `K/N = 1/4` (0.2500) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 5908.374 | 5890.993 | 31.969 |

### `binary_1d` · `bf64-bf128` · actual `K/N = 1/4` (0.2500) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/4` | 0.2500 | 21629.646 | 21601.748 | 127.975 |

### `binary_1d` · `bf64-bf128` · actual `K/N = 1/2` (0.5000) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 6.040 | 6.155 | 0.027 |

### `binary_1d` · `bf64-bf128` · actual `K/N = 1/2` (0.5000) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 30.801 | 31.200 | 0.225 |

### `binary_1d` · `bf64-bf128` · actual `K/N = 1/2` (0.5000) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 130.339 | 131.143 | 0.973 |

### `binary_1d` · `bf64-bf128` · actual `K/N = 1/2` (0.5000) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 597.121 | 599.815 | 3.975 |

### `binary_1d` · `bf64-bf128` · actual `K/N = 1/2` (0.5000) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 2643.072 | 2643.071 | 15.973 |

### `binary_1d` · `bf64-bf128` · actual `K/N = 1/2` (0.5000) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `qa/binary-spectral` | #6 | `1/2` | 0.5000 | 11590.608 | 11586.063 | 63.977 |

### `binary_1d` · `block128` · actual `K/N = 1/2` (0.5000) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `spin/packet` | #19 | `1/2` | 0.5000 | 8.029 | 7.998 | 0.102 |
| `spin/imt` | #19 | `1/2` | 0.5000 | 12.707 | 12.697 | 0.107 |

### `binary_1d` · `block128` · actual `K/N = 1/2` (0.5000) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `spin/packet` | #19 | `1/2` | 0.5000 | 35.657 | 35.645 | 0.385 |
| `spin/imt` | #19 | `1/2` | 0.5000 | 82.079 | 82.009 | 0.426 |

### `binary_1d` · `block128` · actual `K/N = 1/2` (0.5000) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `spin/packet` | #19 | `1/2` | 0.5000 | 146.979 | 147.001 | 1.539 |
| `spin/imt` | #19 | `1/2` | 0.5000 | 361.300 | 358.012 | 1.785 |

### `binary_1d` · `block128` · actual `K/N = 1/2` (0.5000) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `spin/packet` | #19 | `1/2` | 0.5000 | 618.195 | 618.282 | 6.154 |
| `spin/imt` | #19 | `1/2` | 0.5000 | 1558.486 | 1558.248 | 7.135 |

### `binary_1d` · `block128` · actual `K/N = 1/2` (0.5000) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `spin/imt` | #19 | `1/2` | 0.5000 | 7047.477 | 7043.644 | 28.533 |

### `binary_1d` · `block128` · actual `K/N = 1/2` (0.5000) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `spin/imt` | #19 | `1/2` | 0.5000 | 39889.260 | 39880.075 | 114.127 |

### `native_fields_1d` · `babybear` · actual `K/N = 1/4` (0.2500) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `rs/p3-coset-lde` | #1 | `1/4` | 0.2500 | 32.659 | 32.781 | 0.023 |

### `native_fields_1d` · `babybear` · actual `K/N = 1/4` (0.2500) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `rs/p3-coset-lde` | #1 | `1/4` | 0.2500 | 116.828 | 115.841 | 0.137 |

### `native_fields_1d` · `babybear` · actual `K/N = 1/4` (0.2500) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `rs/p3-coset-lde` | #1 | `1/4` | 0.2500 | 492.878 | 487.074 | 0.600 |

### `native_fields_1d` · `babybear` · actual `K/N = 1/2` (0.5000) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `rs/p3-coset-lde` | #1 | `1/2` | 0.5000 | 26.564 | 26.612 | 0.016 |

### `native_fields_1d` · `babybear` · actual `K/N = 1/2` (0.5000) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `rs/p3-coset-lde` | #1 | `1/2` | 0.5000 | 84.233 | 84.259 | 0.062 |

### `native_fields_1d` · `babybear` · actual `K/N = 1/2` (0.5000) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `rs/p3-coset-lde` | #1 | `1/2` | 0.5000 | 335.044 | 334.696 | 0.352 |

### `native_fields_1d` · `babybear` · actual `K/N = 1/2` (0.5000) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `rs/p3-coset-lde` | #1 | `1/2` | 0.5000 | 1371.380 | 1363.525 | 1.469 |

### `native_fields_1d` · `bn254` · actual `K/N = 1/2` (0.5000) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `lightning/ldpc-brakedown` | #13 | `half` | 0.5000 | 922.042 | 920.155 | 0.445 |

### `native_fields_1d` · `bn254` · actual `K/N = 1/2` (0.5000) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `lightning/ldpc-brakedown` | #13 | `half` | 0.5000 | 6404.216 | 6412.754 | 1.912 |

### `native_fields_1d` · `bn254` · actual `K/N = 1/2` (0.5000) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `lightning/ldpc-brakedown` | #13 | `half` | 0.5000 | 36003.128 | 35987.081 | 7.639 |

### `native_fields_1d` · `bn254` · actual `K/N = 1/2` (0.5000) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `lightning/ldpc-brakedown` | #13 | `half` | 0.5000 | 871511.532 | 881494.635 | 123.453 |

### `native_fields_1d` · `bn254` · actual `K/N = 67108864/134217727` (0.5000) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `lightning/ldpc-brakedown` | #13 | `half` | 0.5000 | 163944.070 | 164010.214 | 30.830 |

### `native_fields_1d` · `bn254` · actual `K/N = 1048576/1726355` (0.6074) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `lightning/ldpc-brakedown` | #13 | `native-low` | 0.6074 | 605.119 | 606.485 | 0.299 |

### `native_fields_1d` · `bn254` · actual `K/N = 4194304/6905415` (0.6074) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `lightning/ldpc-brakedown` | #13 | `native-low` | 0.6074 | 4946.751 | 4943.700 | 1.188 |

### `native_fields_1d` · `bn254` · actual `K/N = 4194304/6707989` (0.6253) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `lightning/ldpc-brakedown` | #13 | `native-low` | 0.6253 | 27469.379 | 27469.079 | 5.043 |

### `native_fields_1d` · `bn254` · actual `K/N = 67108864/106909967` (0.6277) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `lightning/ldpc-brakedown` | #13 | `native-low` | 0.6277 | 608270.737 | 608180.758 | 81.195 |

### `native_fields_1d` · `bn254` · actual `K/N = 33554432/53454983` (0.6277) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `lightning/ldpc-brakedown` | #13 | `native-low` | 0.6277 | 130206.762 | 130234.278 | 20.301 |

### `native_fields_1d` · `bn254` · actual `K/N = 1073741824/1709548723` (0.6281) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `lightning/ldpc-brakedown` | #13 | `native-low` | 0.6281 | 3574200.543 | 3567619.954 | 325.037 |

### `native_fields_1d` · `bn254` · actual `K/N = 2/3` (0.6667) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `lightning/ldpc-brakedown` | #13 | `native-high` | 0.6667 | 579.221 | 576.479 | 0.119 |

### `native_fields_1d` · `bn254` · actual `K/N = 4194304/5494797` (0.7633) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `lightning/ldpc-brakedown` | #13 | `native-high` | 0.7633 | 3305.111 | 3304.068 | 0.730 |

### `native_fields_1d` · `bn254` · actual `K/N = 8388608/10779005` (0.7782) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `lightning/ldpc-brakedown` | #13 | `native-high` | 0.7782 | 22448.416 | 22452.884 | 3.053 |

### `native_fields_1d` · `bn254` · actual `K/N = 67108864/86232037` (0.7782) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `lightning/ldpc-brakedown` | #13 | `native-high` | 0.7782 | 108872.133 | 109486.568 | 12.201 |

### `native_fields_1d` · `bn254` · actual `K/N = 268435456/343911047` (0.7805) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `lightning/ldpc-brakedown` | #13 | `native-high` | 0.7805 | 468512.294 | 468209.424 | 49.055 |

### `native_fields_1d` · `bn254` · actual `K/N = 1073741824/1375639049` (0.7805) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `lightning/ldpc-brakedown` | #13 | `native-high` | 0.7805 | 2795199.004 | 2790716.226 | 196.350 |

### `native_fields_1d` · `ft127` · actual `K/N = 1048576/1594885` (0.6575) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/sdig3` | #12 | `native` | 0.6575 | 404.029 | 384.515 | 0.436 |

### `native_fields_1d` · `ft127` · actual `K/N = 4194304/6379537` (0.6575) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/sdig3` | #12 | `native` | 0.6575 | 2296.574 | 2310.435 | 1.703 |

### `native_fields_1d` · `ft127` · actual `K/N = 8388608/12759073` (0.6575) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/sdig3` | #12 | `native` | 0.6575 | 14138.649 | 14314.609 | 6.809 |

### `native_fields_1d` · `ft127` · actual `K/N = 67108864/102072583` (0.6575) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/sdig3` | #12 | `native` | 0.6575 | 65778.836 | 65865.835 | 27.195 |

### `native_fields_1d` · `ft127` · actual `K/N = 268435456/408290329` (0.6575) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/sdig3` | #12 | `native` | 0.6575 | 287002.817 | 286902.526 | 108.748 |

### `native_fields_1d` · `ft127` · actual `K/N = 1048576/1541407` (0.6803) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/sdig2` | #12 | `native` | 0.6803 | 350.685 | 334.898 | 0.391 |

### `native_fields_1d` · `ft127` · actual `K/N = 4194304/6165627` (0.6803) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/sdig2` | #12 | `native` | 0.6803 | 2050.113 | 2052.661 | 1.549 |

### `native_fields_1d` · `ft127` · actual `K/N = 4194304/6165627` (0.6803) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/sdig2` | #12 | `native` | 0.6803 | 12747.215 | 13007.578 | 6.195 |

### `native_fields_1d` · `ft127` · actual `K/N = 67108864/98650031` (0.6803) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/sdig2` | #12 | `native` | 0.6803 | 59314.432 | 59376.209 | 24.795 |

### `native_fields_1d` · `ft127` · actual `K/N = 268435456/394600121` (0.6803) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/sdig2` | #12 | `native` | 0.6803 | 253892.669 | 254069.465 | 99.174 |

### `native_fields_1d` · `ft127` · actual `K/N = 536870912/789200241` (0.6803) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/sdig2` | #12 | `native` | 0.6803 | 1198505.524 | 1198875.907 | 396.701 |

### `native_fields_1d` · `m127` · actual `K/N = 1/4` (0.2500) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/4` | 0.2500 | 18.089 | 18.153 | 0.234 |
| `qa/packed-wht` | #6 | `1/4` | 0.2500 | 19.198 | 19.286 | 0.143 |
| `hyperfold/r4-qa` | #5+ | `1/4` | 0.2500 | 22.122 | 20.640 | 0.229 |
| `hyperfold/r2-qa` | #5+ | `1/4` | 0.2500 | 26.754 | 25.351 | 0.236 |
| `hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 31.003 | 29.982 | 0.232 |
| `hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 35.369 | 34.294 | 0.234 |
| `hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 56.602 | 56.500 | 0.244 |
| `basefold/rs64-rfc` | #5 | `1/4` | 0.2500 | 188.314 | 179.990 | 0.486 |

### `native_fields_1d` · `m127` · actual `K/N = 1/4` (0.2500) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/4` | 0.2500 | 62.158 | 62.103 | 1.029 |
| `qa/packed-wht` | #6 | `1/4` | 0.2500 | 79.216 | 78.957 | 0.564 |
| `hyperfold/r4-qa` | #5+ | `1/4` | 0.2500 | 87.548 | 87.473 | 1.035 |
| `hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 129.836 | 130.129 | 1.037 |
| `hyperfold/r2-qa` | #5+ | `1/4` | 0.2500 | 130.430 | 130.262 | 1.035 |
| `hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 146.461 | 146.400 | 1.027 |
| `hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 173.668 | 173.635 | 1.033 |
| `basefold/rs64-rfc` | #5 | `1/4` | 0.2500 | 815.162 | 793.772 | 2.035 |

### `native_fields_1d` · `m127` · actual `K/N = 1/4` (0.2500) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/4` | 0.2500 | 283.522 | 283.117 | 4.225 |
| `hyperfold/r4-qa` | #5+ | `1/4` | 0.2500 | 393.652 | 392.793 | 4.223 |
| `hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 449.643 | 449.942 | 4.221 |
| `qa/packed-wht` | #6 | `1/4` | 0.2500 | 543.667 | 520.726 | 2.252 |
| `hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 558.669 | 558.951 | 4.221 |
| `hyperfold/r2-qa` | #5+ | `1/4` | 0.2500 | 606.969 | 605.729 | 4.227 |
| `hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 770.549 | 771.206 | 4.227 |
| `basefold/rs64-rfc` | #5 | `1/4` | 0.2500 | 3571.384 | 3516.446 | 8.225 |

### `native_fields_1d` · `m127` · actual `K/N = 1/4` (0.2500) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/4` | 0.2500 | 1183.646 | 1183.075 | 16.975 |
| `hyperfold/r4-qa` | #5+ | `1/4` | 0.2500 | 1731.835 | 1729.091 | 16.980 |
| `hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 2391.941 | 2390.148 | 16.977 |
| `qa/packed-wht` | #6 | `1/4` | 0.2500 | 2623.717 | 2603.610 | 9.002 |
| `hyperfold/r2-qa` | #5+ | `1/4` | 0.2500 | 2867.646 | 2864.563 | 16.979 |
| `hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 3541.337 | 3540.957 | 16.975 |
| `hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 3903.033 | 3901.293 | 16.982 |
| `basefold/rs64-rfc` | #5 | `1/4` | 0.2500 | 15077.845 | 14844.303 | 32.977 |

### `native_fields_1d` · `m127` · actual `K/N = 1/4` (0.2500) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/4` | 0.2500 | 5199.570 | 5197.249 | 67.975 |
| `hyperfold/r4-qa` | #5+ | `1/4` | 0.2500 | 7576.941 | 7564.113 | 67.973 |
| `hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 10245.056 | 10253.298 | 67.979 |
| `hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 10524.854 | 10533.120 | 67.977 |
| `qa/packed-wht` | #6 | `1/4` | 0.2500 | 11421.888 | 11422.962 | 36.002 |
| `hyperfold/r2-qa` | #5+ | `1/4` | 0.2500 | 13227.721 | 13233.507 | 67.973 |
| `hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 15751.264 | 15736.686 | 67.975 |
| `basefold/rs64-rfc` | #5 | `1/4` | 0.2500 | 79169.185 | 79368.570 | 131.973 |

### `native_fields_1d` · `m127` · actual `K/N = 1/4` (0.2500) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/4` | 0.2500 | 19966.504 | 19968.984 | 271.975 |
| `hyperfold/r4-qa` | #5+ | `1/4` | 0.2500 | 28594.425 | 28597.865 | 271.975 |
| `hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 30536.564 | 30513.464 | 271.973 |
| `hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 39434.734 | 39525.381 | 271.973 |
| `hyperfold/r2-qa` | #5+ | `1/4` | 0.2500 | 48582.232 | 48636.890 | 271.975 |
| `qa/packed-wht` | #6 | `1/4` | 0.2500 | 56233.697 | 57858.407 | 144.002 |
| `hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 59251.030 | 59224.273 | 271.979 |

### `native_fields_1d` · `m127` · actual `K/N = 1/2` (0.5000) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/2` | 0.5000 | 10.187 | 10.441 | 0.123 |
| `qa/packed-wht` | #6 | `1/2` | 0.5000 | 10.333 | 10.150 | 0.080 |
| `hyperfold/r4-qa` | #5+ | `1/2` | 0.5000 | 13.624 | 13.447 | 0.109 |
| `hyperfold/r2-qa` | #5+ | `1/2` | 0.5000 | 15.811 | 15.501 | 0.111 |
| `hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 19.906 | 18.958 | 0.113 |
| `hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 20.850 | 20.506 | 0.102 |
| `hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 27.567 | 26.458 | 0.115 |
| `basefold/rs64-rfc` | #5 | `1/2` | 0.5000 | 138.114 | 139.048 | 0.230 |

### `native_fields_1d` · `m127` · actual `K/N = 1/2` (0.5000) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/2` | 0.5000 | 32.201 | 30.989 | 0.529 |
| `qa/packed-wht` | #6 | `1/2` | 0.5000 | 41.989 | 41.410 | 0.314 |
| `hyperfold/r4-qa` | #5+ | `1/2` | 0.5000 | 42.398 | 42.383 | 0.537 |
| `hyperfold/r2-qa` | #5+ | `1/2` | 0.5000 | 60.106 | 60.106 | 0.543 |
| `hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 65.076 | 64.995 | 0.533 |
| `hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 67.405 | 67.453 | 0.539 |
| `hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 85.836 | 85.548 | 0.535 |
| `basefold/rs64-rfc` | #5 | `1/2` | 0.5000 | 436.869 | 421.684 | 1.037 |

### `native_fields_1d` · `m127` · actual `K/N = 1/2` (0.5000) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/2` | 0.5000 | 140.765 | 140.756 | 2.229 |
| `hyperfold/r4-qa` | #5+ | `1/2` | 0.5000 | 192.876 | 192.874 | 2.215 |
| `hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 232.165 | 231.426 | 2.227 |
| `qa/packed-wht` | #6 | `1/2` | 0.5000 | 268.650 | 268.744 | 1.252 |
| `hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 278.394 | 278.966 | 2.221 |
| `hyperfold/r2-qa` | #5+ | `1/2` | 0.5000 | 295.825 | 295.729 | 2.227 |
| `hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 379.298 | 381.351 | 2.230 |
| `basefold/rs64-rfc` | #5 | `1/2` | 0.5000 | 1875.478 | 1876.162 | 4.219 |

### `native_fields_1d` · `m127` · actual `K/N = 1/2` (0.5000) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/2` | 0.5000 | 570.969 | 569.731 | 8.975 |
| `hyperfold/r4-qa` | #5+ | `1/2` | 0.5000 | 846.968 | 847.308 | 8.975 |
| `hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 1157.273 | 1156.401 | 8.975 |
| `qa/packed-wht` | #6 | `1/2` | 0.5000 | 1303.921 | 1303.378 | 5.002 |
| `hyperfold/r2-qa` | #5+ | `1/2` | 0.5000 | 1361.901 | 1360.525 | 8.973 |
| `hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 1669.379 | 1667.721 | 8.971 |
| `hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 1672.560 | 1672.192 | 8.973 |
| `basefold/rs64-rfc` | #5 | `1/2` | 0.5000 | 8336.013 | 8214.804 | 16.973 |

### `native_fields_1d` · `m127` · actual `K/N = 1/2` (0.5000) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/2` | 0.5000 | 2598.313 | 2599.293 | 35.975 |
| `hyperfold/r4-qa` | #5+ | `1/2` | 0.5000 | 3718.530 | 3721.076 | 35.969 |
| `hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 4758.126 | 4765.897 | 35.969 |
| `hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 4883.301 | 4884.777 | 35.977 |
| `qa/packed-wht` | #6 | `1/2` | 0.5000 | 5849.837 | 5851.313 | 20.000 |
| `hyperfold/r2-qa` | #5+ | `1/2` | 0.5000 | 6272.779 | 6262.373 | 35.971 |
| `hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 7431.584 | 7439.283 | 35.973 |
| `basefold/rs64-rfc` | #5 | `1/2` | 0.5000 | 42525.472 | 42268.924 | 67.975 |

### `native_fields_1d` · `m127` · actual `K/N = 1/2` (0.5000) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/2` | 0.5000 | 10759.149 | 10758.557 | 143.973 |
| `hyperfold/r4-qa` | #5+ | `1/2` | 0.5000 | 15312.198 | 15310.577 | 143.973 |
| `hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 16028.567 | 16013.298 | 143.969 |
| `hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 19916.341 | 19935.123 | 143.969 |
| `qa/packed-wht` | #6 | `1/2` | 0.5000 | 26008.688 | 26017.781 | 80.002 |
| `hyperfold/r2-qa` | #5+ | `1/2` | 0.5000 | 27803.052 | 27819.202 | 143.971 |
| `hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 32321.973 | 32371.404 | 143.973 |
| `basefold/rs64-rfc` | #5 | `1/2` | 0.5000 | 175858.640 | 175708.707 | 271.977 |

### `native_fields_1d` · `m127` · actual `K/N = 1048576/1594885` (0.6575) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/plonkish-sdig3` | #12 | `native` | 0.6575 | 239.612 | 238.174 | 0.424 |

### `native_fields_1d` · `m127` · actual `K/N = 4194304/6379537` (0.6575) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/plonkish-sdig3` | #12 | `native` | 0.6575 | 1326.290 | 1326.234 | 1.646 |

### `native_fields_1d` · `m127` · actual `K/N = 8388608/12759073` (0.6575) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/plonkish-sdig3` | #12 | `native` | 0.6575 | 8337.757 | 8335.080 | 6.561 |

### `native_fields_1d` · `m127` · actual `K/N = 67108864/102072583` (0.6575) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/plonkish-sdig3` | #12 | `native` | 0.6575 | 39933.420 | 39935.107 | 26.178 |

### `native_fields_1d` · `m127` · actual `K/N = 268435456/408290329` (0.6575) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/plonkish-sdig3` | #12 | `native` | 0.6575 | 169120.211 | 169124.493 | 104.666 |

### `native_fields_1d` · `ristretto255` · actual `K/N = 1/4` (0.2500) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/eacode-official` | #7 | `1/4` | 0.2500 | 143.636 | 143.572 | 0.346 |
| `ea/eacode-official` | #7 | `1/4` | 0.2500 | 1457.507 | 1458.924 | 18.709 |

### `native_fields_1d` · `ristretto255` · actual `K/N = 1/4` (0.2500) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/eacode-official` | #7 | `1/4` | 0.2500 | 604.750 | 599.748 | 1.377 |
| `ea/eacode-official` | #7 | `1/4` | 0.2500 | 9011.968 | 9004.628 | 81.615 |

### `native_fields_1d` · `ristretto255` · actual `K/N = 1/4` (0.2500) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/eacode-official` | #7 | `1/4` | 0.2500 | 2509.485 | 2509.500 | 5.502 |
| `ea/eacode-official` | #7 | `1/4` | 0.2500 | 41378.065 | 41376.893 | 353.471 |

### `native_fields_1d` · `ristretto255` · actual `K/N = 1/4` (0.2500) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/eacode-official` | #7 | `1/4` | 0.2500 | 12709.504 | 12672.566 | 22.002 |

### `native_fields_1d` · `ristretto255` · actual `K/N = 1/4` (0.2500) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/eacode-official` | #7 | `1/4` | 0.2500 | 70456.025 | 70410.268 | 88.000 |

### `native_fields_1d` · `ristretto255` · actual `K/N = 1/4` (0.2500) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/eacode-official` | #7 | `1/4` | 0.2500 | 460756.645 | 468436.052 | 352.002 |

### `native_fields_1d` · `ristretto255` · actual `K/N = 1/2` (0.5000) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/eacode-official` | #7 | `1/2` | 0.5000 | 70.041 | 70.087 | 0.188 |
| `ea/eacode-official` | #7 | `1/2` | 0.5000 | 1383.340 | 1383.104 | 17.809 |

### `native_fields_1d` · `ristretto255` · actual `K/N = 1/2` (0.5000) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/eacode-official` | #7 | `1/2` | 0.5000 | 298.171 | 295.557 | 0.752 |
| `ea/eacode-official` | #7 | `1/2` | 0.5000 | 8602.754 | 8616.211 | 77.994 |

### `native_fields_1d` · `ristretto255` · actual `K/N = 1/2` (0.5000) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/eacode-official` | #7 | `1/2` | 0.5000 | 1215.089 | 1212.161 | 3.002 |
| `ea/eacode-official` | #7 | `1/2` | 0.5000 | 39823.152 | 39823.175 | 338.973 |

### `native_fields_1d` · `ristretto255` · actual `K/N = 1/2` (0.5000) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/eacode-official` | #7 | `1/2` | 0.5000 | 5375.041 | 5357.986 | 12.000 |

### `native_fields_1d` · `ristretto255` · actual `K/N = 1/2` (0.5000) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/eacode-official` | #7 | `1/2` | 0.5000 | 32042.495 | 32049.317 | 48.002 |

### `native_fields_1d` · `ristretto255` · actual `K/N = 1/2` (0.5000) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/eacode-official` | #7 | `1/2` | 0.5000 | 206653.649 | 206240.176 | 192.002 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 16777216/70464307` (0.2381) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/4` | 0.2381 | 7700.663 | 7694.662 | 75.307 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 16777216/70464307` (0.2381) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/4` | 0.2381 | 30520.293 | 30411.289 | 301.219 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 1048576/4404019` (0.2381) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/4` | 0.2381 | 542.615 | 535.481 | 4.707 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 1048576/4404019` (0.2381) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/4` | 0.2381 | 1781.571 | 1774.171 | 18.828 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 65536/275251` (0.2381) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/4` | 0.2381 | 115.562 | 110.867 | 1.178 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 1/4` (0.2500) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/raa-unweighted` | #7 | `1/4` | 0.2500 | 62.980 | 63.067 | 0.346 |
| `brakedown/brakedown-recursive` | #12 | `1/4` | 0.2500 | 234.024 | 234.000 | 4.123 |
| `ea/ea-explicit` | #7 | `1/4` | 0.2500 | 1581.250 | 1583.514 | 18.715 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 1/4` (0.2500) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/raa-unweighted` | #7 | `1/4` | 0.2500 | 245.905 | 245.941 | 1.377 |
| `brakedown/brakedown-recursive` | #12 | `1/4` | 0.2500 | 1355.542 | 1353.394 | 16.484 |
| `ea/ea-explicit` | #7 | `1/4` | 0.2500 | 9396.916 | 9410.259 | 81.611 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 1/4` (0.2500) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/raa-unweighted` | #7 | `1/4` | 0.2500 | 983.490 | 983.182 | 5.502 |
| `brakedown/brakedown-recursive` | #12 | `1/4` | 0.2500 | 5998.684 | 5994.870 | 65.936 |
| `ea/ea-explicit` | #7 | `1/4` | 0.2500 | 43662.596 | 43683.954 | 353.469 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 1/4` (0.2500) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/raa-unweighted` | #7 | `1/4` | 0.2500 | 4011.192 | 4008.422 | 22.002 |
| `brakedown/brakedown-recursive` | #12 | `1/4` | 0.2500 | 27190.617 | 26826.660 | 263.727 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 1/4` (0.2500) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/raa-unweighted` | #7 | `1/4` | 0.2500 | 17057.134 | 17072.569 | 88.002 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 1/4` (0.2500) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/raa-unweighted` | #7 | `1/4` | 0.2500 | 62048.918 | 62060.942 | 352.002 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 33554432/70464307` (0.4762) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/2` | 0.4762 | 6540.959 | 6478.455 | 54.307 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 33554432/70464307` (0.4762) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/2` | 0.4762 | 25992.018 | 25824.959 | 217.217 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 2097152/4404019` (0.4762) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/2` | 0.4762 | 418.114 | 415.953 | 3.658 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 2097152/4404019` (0.4762) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/2` | 0.4762 | 1425.536 | 1411.474 | 13.578 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 131072/275251` (0.4762) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/2` | 0.4762 | 75.486 | 72.928 | 0.850 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 1/2` (0.5000) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/raa-unweighted` | #7 | `1/2` | 0.5000 | 31.462 | 31.514 | 0.189 |
| `brakedown/brakedown-recursive` | #12 | `1/2` | 0.5000 | 131.900 | 130.721 | 2.322 |
| `ea/ea-explicit` | #7 | `1/2` | 0.5000 | 1495.390 | 1496.377 | 17.803 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 1/2` (0.5000) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/raa-unweighted` | #7 | `1/2` | 0.5000 | 123.766 | 123.960 | 0.752 |
| `brakedown/brakedown-recursive` | #12 | `1/2` | 0.5000 | 815.016 | 815.750 | 9.283 |
| `ea/ea-explicit` | #7 | `1/2` | 0.5000 | 8929.561 | 8930.290 | 77.984 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 1/2` (0.5000) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/raa-unweighted` | #7 | `1/2` | 0.5000 | 497.229 | 495.163 | 3.002 |
| `brakedown/brakedown-recursive` | #12 | `1/2` | 0.5000 | 3934.330 | 3909.413 | 37.127 |
| `ea/ea-explicit` | #7 | `1/2` | 0.5000 | 42983.968 | 43007.513 | 338.971 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 1/2` (0.5000) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/raa-unweighted` | #7 | `1/2` | 0.5000 | 2005.762 | 2004.040 | 12.002 |
| `brakedown/brakedown-recursive` | #12 | `1/2` | 0.5000 | 16900.890 | 16830.857 | 148.500 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 1/2` (0.5000) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/raa-unweighted` | #7 | `1/2` | 0.5000 | 8576.530 | 8565.905 | 48.002 |

### `native_fields_1d` · `secp256k1` · actual `K/N = 1/2` (0.5000) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `raa/raa-unweighted` | #7 | `1/2` | 0.5000 | 32003.708 | 32017.679 | 192.002 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 16777216/70464307` (0.2381) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/4` | 0.2381 | 2257.479 | 2221.407 | 28.248 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 16777216/70464307` (0.2381) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/4` | 0.2381 | 10806.003 | 10795.792 | 112.986 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 1048576/4404019` (0.2381) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/4` | 0.2381 | 134.703 | 134.827 | 1.768 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 1048576/4404019` (0.2381) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/4` | 0.2381 | 521.734 | 525.532 | 7.061 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 65536/275251` (0.2381) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/4` | 0.2381 | 20.923 | 20.926 | 0.441 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 1/4` (0.2500) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/4` | 0.2500 | 5.614 | 5.607 | 0.113 |
| `hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 6.533 | 6.619 | 0.115 |
| `hyperfold/r4-qa` | #5+ | `1/4` | 0.2500 | 7.463 | 7.513 | 0.117 |
| `hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 8.362 | 8.349 | 0.117 |
| `qa/packed-wht` | #6 | `1/4` | 0.2500 | 9.139 | 9.172 | 0.072 |
| `hyperfold/r2-qa` | #5+ | `1/4` | 0.2500 | 13.204 | 13.072 | 0.113 |
| `hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 13.255 | 13.299 | 0.113 |
| `raa/raa-unweighted` | #7 | `1/4` | 0.2500 | 15.829 | 15.826 | 0.135 |
| `rs/p3-coset-lde` | #1 | `1/4` | 0.2500 | 22.740 | 22.419 | 0.051 |
| `brakedown/brakedown-recursive` | #12 | `1/4` | 0.2500 | 26.567 | 26.675 | 1.711 |
| `ea/ea-explicit` | #7 | `1/4` | 0.2500 | 148.322 | 148.198 | 9.291 |
| `basefold/rs64-rfc` | #5 | `1/4` | 0.2500 | 227.840 | 220.682 | 0.459 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 1/4` (0.2500) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/4` | 0.2500 | 25.114 | 25.032 | 0.508 |
| `hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 28.161 | 28.099 | 0.506 |
| `hyperfold/r4-qa` | #5+ | `1/4` | 0.2500 | 32.206 | 32.268 | 0.506 |
| `hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 34.445 | 34.436 | 0.504 |
| `qa/packed-wht` | #6 | `1/4` | 0.2500 | 36.481 | 36.249 | 0.283 |
| `hyperfold/r2-qa` | #5+ | `1/4` | 0.2500 | 59.282 | 59.440 | 0.506 |
| `hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 62.153 | 62.148 | 0.512 |
| `raa/raa-unweighted` | #7 | `1/4` | 0.2500 | 71.537 | 71.543 | 0.533 |
| `rs/p3-coset-lde` | #1 | `1/4` | 0.2500 | 92.533 | 91.341 | 0.293 |
| `brakedown/brakedown-recursive` | #12 | `1/4` | 0.2500 | 196.682 | 196.721 | 6.842 |
| `basefold/rs64-rfc` | #5 | `1/4` | 0.2500 | 996.560 | 985.890 | 1.910 |
| `ea/ea-explicit` | #7 | `1/4` | 0.2500 | 1447.288 | 1447.300 | 40.658 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 1/4` (0.2500) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/4` | 0.2500 | 118.452 | 118.466 | 2.102 |
| `hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 127.645 | 127.624 | 2.098 |
| `hyperfold/r4-qa` | #5+ | `1/4` | 0.2500 | 151.827 | 151.780 | 2.096 |
| `hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 160.963 | 160.924 | 2.098 |
| `qa/packed-wht` | #6 | `1/4` | 0.2500 | 234.997 | 234.932 | 1.127 |
| `hyperfold/r2-qa` | #5+ | `1/4` | 0.2500 | 283.480 | 281.493 | 2.100 |
| `rs/p3-coset-lde` | #1 | `1/4` | 0.2500 | 290.067 | 290.032 | 1.223 |
| `hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 291.780 | 291.076 | 2.098 |
| `raa/raa-unweighted` | #7 | `1/4` | 0.2500 | 306.463 | 306.438 | 2.127 |
| `brakedown/brakedown-recursive` | #12 | `1/4` | 0.2500 | 1155.391 | 1155.231 | 27.365 |
| `basefold/rs64-rfc` | #5 | `1/4` | 0.2500 | 4369.395 | 4372.868 | 7.725 |
| `ea/ea-explicit` | #7 | `1/4` | 0.2500 | 8011.912 | 8008.080 | 176.098 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 1/4` (0.2500) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/4` | 0.2500 | 484.707 | 484.953 | 8.477 |
| `hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 536.609 | 536.899 | 8.469 |
| `hyperfold/r4-qa` | #5+ | `1/4` | 0.2500 | 683.364 | 683.067 | 8.473 |
| `hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 721.531 | 722.127 | 8.479 |
| `rs/p3-coset-lde` | #1 | `1/4` | 0.2500 | 1178.320 | 1173.671 | 4.979 |
| `qa/packed-wht` | #6 | `1/4` | 0.2500 | 1271.809 | 1295.136 | 4.502 |
| `hyperfold/r2-qa` | #5+ | `1/4` | 0.2500 | 1294.776 | 1291.563 | 8.471 |
| `hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 1317.027 | 1314.901 | 8.473 |
| `raa/raa-unweighted` | #7 | `1/4` | 0.2500 | 1346.760 | 1350.963 | 8.502 |
| `brakedown/brakedown-recursive` | #12 | `1/4` | 0.2500 | 5345.110 | 5342.396 | 109.451 |
| `basefold/rs64-rfc` | #5 | `1/4` | 0.2500 | 21698.924 | 21283.420 | 30.975 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 1/4` (0.2500) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/4` | 0.2500 | 2245.150 | 2247.146 | 33.971 |
| `hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 2435.615 | 2432.977 | 33.977 |
| `hyperfold/r4-qa` | #5+ | `1/4` | 0.2500 | 3064.876 | 3066.075 | 33.975 |
| `hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 3209.928 | 3211.321 | 33.973 |
| `rs/p3-coset-lde` | #1 | `1/4` | 0.2500 | 5152.675 | 5152.885 | 19.971 |
| `qa/packed-wht` | #6 | `1/4` | 0.2500 | 5704.423 | 5702.511 | 18.002 |
| `raa/raa-unweighted` | #7 | `1/4` | 0.2500 | 5724.312 | 5609.407 | 34.002 |
| `hyperfold/r2-qa` | #5+ | `1/4` | 0.2500 | 5770.252 | 5775.588 | 33.977 |
| `hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 5887.565 | 5885.084 | 33.979 |
| `basefold/rs64-rfc` | #5 | `1/4` | 0.2500 | 109490.207 | 110202.642 | 123.965 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 1/4` (0.2500) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/4` | 0.2500 | 9413.034 | 9390.119 | 135.973 |
| `hyperfold/r8-rs` | #5+ | `1/4` | 0.2500 | 10041.591 | 9990.951 | 135.977 |
| `hyperfold/r4-qa` | #5+ | `1/4` | 0.2500 | 12727.459 | 12729.724 | 135.973 |
| `hyperfold/r4-rs` | #5+ | `1/4` | 0.2500 | 13321.629 | 13326.331 | 135.975 |
| `rs/p3-coset-lde` | #1 | `1/4` | 0.2500 | 21363.501 | 21420.770 | 79.969 |
| `hyperfold/r2-qa` | #5+ | `1/4` | 0.2500 | 24807.481 | 24843.225 | 135.975 |
| `qa/packed-wht` | #6 | `1/4` | 0.2500 | 25402.521 | 25229.725 | 72.002 |
| `hyperfold/r2-rs` | #5+ | `1/4` | 0.2500 | 25481.547 | 25457.078 | 135.977 |
| `raa/raa-unweighted` | #7 | `1/4` | 0.2500 | 26890.785 | 26893.612 | 136.002 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 536870912/1127428915` (0.4762) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/2` | 0.4762 | 24758.263 | 24576.244 | 317.543 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 33554432/70464307` (0.4762) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/2` | 0.4762 | 1417.528 | 1415.725 | 20.898 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 33554432/70464307` (0.4762) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/2` | 0.4762 | 8143.806 | 8235.936 | 83.588 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 2097152/4404019` (0.4762) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/2` | 0.4762 | 78.027 | 77.995 | 1.307 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 2097152/4404019` (0.4762) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/2` | 0.4762 | 348.457 | 348.398 | 5.225 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 131072/275251` (0.4762) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `era/brakedown-repeat-accumulate` | #20 | `1/2` | 0.4762 | 14.761 | 14.385 | 0.328 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 1/2` (0.5000) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/2` | 0.5000 | 2.869 | 2.851 | 0.035 |
| `hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 3.532 | 3.505 | 0.035 |
| `hyperfold/r4-qa` | #5+ | `1/2` | 0.5000 | 3.821 | 3.777 | 0.043 |
| `hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 4.002 | 4.044 | 0.041 |
| `qa/packed-wht` | #6 | `1/2` | 0.5000 | 5.203 | 5.138 | 0.041 |
| `hyperfold/r2-qa` | #5+ | `1/2` | 0.5000 | 7.150 | 7.030 | 0.041 |
| `hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 8.316 | 8.489 | 0.045 |
| `raa/raa-unweighted` | #7 | `1/2` | 0.5000 | 8.765 | 8.871 | 0.072 |
| `rs/p3-coset-lde` | #1 | `1/2` | 0.5000 | 16.767 | 16.910 | 0.029 |
| `brakedown/brakedown-recursive` | #12 | `1/2` | 0.5000 | 16.877 | 16.826 | 0.941 |
| `basefold/rs64-rfc` | #5 | `1/2` | 0.5000 | 117.924 | 115.750 | 0.211 |
| `ea/ea-explicit` | #7 | `1/2` | 0.5000 | 137.953 | 138.016 | 8.869 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 1/2` (0.5000) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/2` | 0.5000 | 12.669 | 12.520 | 0.256 |
| `hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 13.826 | 13.654 | 0.252 |
| `hyperfold/r4-qa` | #5+ | `1/2` | 0.5000 | 15.914 | 15.979 | 0.264 |
| `hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 17.821 | 17.443 | 0.256 |
| `qa/packed-wht` | #6 | `1/2` | 0.5000 | 20.804 | 20.657 | 0.158 |
| `hyperfold/r2-qa` | #5+ | `1/2` | 0.5000 | 24.996 | 24.582 | 0.258 |
| `hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 26.001 | 25.783 | 0.256 |
| `raa/raa-unweighted` | #7 | `1/2` | 0.5000 | 36.613 | 36.238 | 0.283 |
| `rs/p3-coset-lde` | #1 | `1/2` | 0.5000 | 80.127 | 81.055 | 0.172 |
| `brakedown/brakedown-recursive` | #12 | `1/2` | 0.5000 | 101.686 | 101.681 | 3.760 |
| `basefold/rs64-rfc` | #5 | `1/2` | 0.5000 | 492.489 | 471.895 | 0.979 |
| `ea/ea-explicit` | #7 | `1/2` | 0.5000 | 1369.412 | 1369.157 | 38.900 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 1/2` (0.5000) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/2` | 0.5000 | 53.431 | 53.353 | 1.096 |
| `hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 56.203 | 56.202 | 1.094 |
| `hyperfold/r4-qa` | #5+ | `1/2` | 0.5000 | 74.928 | 74.929 | 1.092 |
| `hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 78.844 | 78.906 | 1.090 |
| `qa/packed-wht` | #6 | `1/2` | 0.5000 | 118.749 | 117.257 | 0.627 |
| `hyperfold/r2-qa` | #5+ | `1/2` | 0.5000 | 133.662 | 132.976 | 1.094 |
| `hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 136.194 | 136.150 | 1.096 |
| `raa/raa-unweighted` | #7 | `1/2` | 0.5000 | 153.643 | 153.528 | 1.127 |
| `rs/p3-coset-lde` | #1 | `1/2` | 0.5000 | 258.672 | 258.672 | 0.729 |
| `brakedown/brakedown-recursive` | #12 | `1/2` | 0.5000 | 670.759 | 670.257 | 15.037 |
| `basefold/rs64-rfc` | #5 | `1/2` | 0.5000 | 2111.523 | 2112.577 | 3.971 |
| `ea/ea-explicit` | #7 | `1/2` | 0.5000 | 7717.441 | 7711.502 | 169.104 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 1/2` (0.5000) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/2` | 0.5000 | 243.321 | 243.466 | 4.473 |
| `hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 266.006 | 264.346 | 4.471 |
| `hyperfold/r4-qa` | #5+ | `1/2` | 0.5000 | 343.843 | 344.580 | 4.475 |
| `hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 356.443 | 355.599 | 4.471 |
| `hyperfold/r2-qa` | #5+ | `1/2` | 0.5000 | 620.710 | 620.736 | 4.471 |
| `raa/raa-unweighted` | #7 | `1/2` | 0.5000 | 631.397 | 629.610 | 4.502 |
| `hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 631.458 | 630.925 | 4.471 |
| `qa/packed-wht` | #6 | `1/2` | 0.5000 | 671.608 | 688.735 | 2.502 |
| `rs/p3-coset-lde` | #1 | `1/2` | 0.5000 | 966.558 | 961.177 | 2.975 |
| `brakedown/brakedown-recursive` | #12 | `1/2` | 0.5000 | 3240.275 | 3239.941 | 60.156 |
| `basefold/rs64-rfc` | #5 | `1/2` | 0.5000 | 9397.751 | 9299.605 | 15.975 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 1/2` (0.5000) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/2` | 0.5000 | 1124.028 | 1122.967 | 17.973 |
| `hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 1203.333 | 1204.516 | 17.977 |
| `hyperfold/r4-qa` | #5+ | `1/2` | 0.5000 | 1535.075 | 1536.416 | 17.975 |
| `hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 1588.789 | 1592.790 | 17.971 |
| `raa/raa-unweighted` | #7 | `1/2` | 0.5000 | 2663.569 | 2662.088 | 18.002 |
| `hyperfold/r2-qa` | #5+ | `1/2` | 0.5000 | 2786.389 | 2785.408 | 17.977 |
| `hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 2829.614 | 2829.270 | 17.975 |
| `qa/packed-wht` | #6 | `1/2` | 0.5000 | 3051.623 | 3051.839 | 10.002 |
| `rs/p3-coset-lde` | #1 | `1/2` | 0.5000 | 3830.910 | 3832.318 | 11.975 |
| `brakedown/brakedown-recursive` | #12 | `1/2` | 0.5000 | 17899.220 | 18028.532 | 240.594 |
| `basefold/rs64-rfc` | #5 | `1/2` | 0.5000 | 48213.057 | 47682.146 | 63.977 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 1/2` (0.5000) · `k = 30` (`2^30` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `hyperfold/r8-qa` | #5+ | `1/2` | 0.5000 | 4649.871 | 4653.357 | 71.969 |
| `hyperfold/r8-rs` | #5+ | `1/2` | 0.5000 | 4880.586 | 4878.238 | 71.973 |
| `hyperfold/r4-qa` | #5+ | `1/2` | 0.5000 | 6793.967 | 6782.386 | 71.975 |
| `hyperfold/r4-rs` | #5+ | `1/2` | 0.5000 | 7020.325 | 6999.645 | 71.979 |
| `raa/raa-unweighted` | #7 | `1/2` | 0.5000 | 12324.080 | 12304.139 | 72.002 |
| `hyperfold/r2-qa` | #5+ | `1/2` | 0.5000 | 12399.620 | 12411.569 | 71.975 |
| `hyperfold/r2-rs` | #5+ | `1/2` | 0.5000 | 12627.686 | 12630.601 | 71.973 |
| `qa/packed-wht` | #6 | `1/2` | 0.5000 | 13029.117 | 12893.794 | 40.002 |
| `rs/p3-coset-lde` | #1 | `1/2` | 0.5000 | 17053.001 | 16699.257 | 47.975 |
| `basefold/rs64-rfc` | #5 | `1/2` | 0.5000 | 194032.512 | 193742.933 | 255.982 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 1048576/1594885` (0.6575) · `k = 20` (`2^20` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/plonkish-sdig3` | #12 | `native` | 0.6575 | 228.850 | 228.535 | 0.422 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 4194304/6379537` (0.6575) · `k = 22` (`2^22` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/plonkish-sdig3` | #12 | `native` | 0.6575 | 1286.984 | 1281.671 | 1.646 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 8388608/12759073` (0.6575) · `k = 24` (`2^24` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/plonkish-sdig3` | #12 | `native` | 0.6575 | 8284.235 | 8272.676 | 6.561 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 67108864/102072583` (0.6575) · `k = 26` (`2^26` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/plonkish-sdig3` | #12 | `native` | 0.6575 | 39652.732 | 39668.392 | 26.178 |

### `prime_goldilocks_1d` · `goldilocks` · actual `K/N = 268435456/408290329` (0.6575) · `k = 28` (`2^28` elements)

| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) |
|---|---|---|---:|---:|---:|---:|
| `brakedown/plonkish-sdig3` | #12 | `native` | 0.6575 | 166283.759 | 166282.220 | 104.666 |

## Conventions

- **1D Single-Codeword Rule & Grid**: Inputs are single 1D vectors of `K = 2^k` elements (`k ∈ {20, 22, 24, 26, 28, 30}`, `nrows = 1`, `width = 1`, `log_batch_size = 0`). Interleaved codes and 2D matrix-reshaped tensor codes are excluded (`EXCLUDED_INTERLEAVED`).
- **Timing Scope**: Measures the native encoder call (`encode_mean_ms`, `encode_median_ms` across 3 serial runs after 1 warmup), excluding setup (`setup_ms`), input generation, caller-buffer reset (for in-place entry points), correctness checks, and Merkle hashing. Before timing, drivers pre-touch or reuse caller-owned buffers; however, output and temporary scratch buffers allocated internally by the encoder during the timed interval can still incur page faults (logged per row in `notes`), and those costs are included.
- **Hardware & Affinity**: AMD EPYC 9754 (503 GiB RAM), pinned to CPUs `0-31` (`RAYON_NUM_THREADS=32`, `OMP_NUM_THREADS=32`), serial one-process-per-config execution.
- **Rate & Boundary Transparency**: Rankings and snapshots group strictly by the exact reduced fraction `K/N` (`input_elements / codeword_elements`, with 4-decimal rounding used for display only), while preserving `nominal_rate` for configuration filtering; `DOMAIN_LIMIT`, `OOM_SKIPPED`, `OOM_LIMIT`, `HOST_MEMORY_LIMIT`, `EXCLUDED_INTERLEAVED`, `UNSUPPORTED_BACKEND`, and `PENDING` statuses are preserved explicitly.
- Use [`TEMPLATE.md`](TEMPLATE.md) when adding a new code family.
