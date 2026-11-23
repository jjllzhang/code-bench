# code-bench

Benchmark archive for linear code encoders used in code-based polynomial commitment schemes (PCS), structured as paired `<code_family>.md` + `<code_family>.csv` files under [`results/`](results/).

## Repository Structure

```text
code-bench/
├── README.md        # Overview tables and index of benchmarked code families
├── TEMPLATE.md      # Markdown template for adding new code families
├── docs/
│   └── index.html   # Interactive comparison charts and tables
└── results/         # Paired <code_family>.md and <code_family>.csv files
```

## Encoding Efficiency Overview

Tables below report **median** encoding time for `K = 2^k` input elements across 3 measured runs on a 32-core AMD EPYC 9754 (`target-cpu=native`), excluding setup. `—` denotes a domain or memory limit; `1T` marks single-threaded implementations (all others use 32 threads).

### Goldilocks (64-bit) — Rate 1/2

| Code / Variant | `k=20` | `k=22` | `k=24` | `k=26` | `k=28` | `k=30` |
|---|---:|---:|---:|---:|---:|---:|
| [HyperFold](results/hyperfold.md) (`r=8`, QA) | 2.85 ms | 12.5 ms | 53.4 ms | 243.5 ms | 1.12 s | 4.65 s |
| [HyperFold](results/hyperfold.md) (`r=8`, RS) | 3.50 ms | 13.7 ms | 56.2 ms | 264.3 ms | 1.20 s | 4.88 s |
| [HyperFold](results/hyperfold.md) (`r=4`, QA) | 3.78 ms | 16.0 ms | 74.9 ms | 344.6 ms | 1.54 s | 6.78 s |
| [HyperFold](results/hyperfold.md) (`r=4`, RS) | 4.04 ms | 17.4 ms | 78.9 ms | 355.6 ms | 1.59 s | 7.00 s |
| [RAA](results/raa.md) (unweighted) | 8.87 ms | 36.2 ms | 153.5 ms | 629.6 ms | 2.66 s | 12.30 s |
| [HyperFold](results/hyperfold.md) (`r=2`, QA) | 7.03 ms | 24.6 ms | 133.0 ms | 620.7 ms | 2.79 s | 12.41 s |
| [HyperFold](results/hyperfold.md) (`r=2`, RS) | 8.49 ms | 25.8 ms | 136.2 ms | 630.9 ms | 2.83 s | 12.63 s |
| [Systematic QA](results/qa.md) (packed WHT) | 5.14 ms | 20.7 ms | 117.3 ms | 688.7 ms | 3.05 s | 12.89 s |
| [Reed–Solomon](results/rs.md) (Plonky3 coset LDE) | 16.9 ms | 81.1 ms | 258.7 ms | 961.2 ms | 3.83 s | 16.70 s |
| [ERA](results/era.md) (`ρ ≈ 0.476`) | 14.4 ms | 78.0 ms | 348.4 ms | 1.42 s | 8.24 s | 24.58 s |
| [BaseFold](results/basefold.md) (`r=2` RFC, 16B) | 115.7 ms | 471.9 ms | 2.11 s | 9.30 s | 47.68 s | 193.74 s |
| [Brakedown](results/brakedown.md) (recursive) | 16.8 ms | 101.7 ms | 670.3 ms | 3.24 s | 18.03 s | — |
| [Brakedown](results/brakedown.md) (`plonkish`, `ρ=0.657`, `1T`, 16B) | 228.5 ms | 1.28 s | 8.27 s | 39.67 s | 166.28 s | — |
| [EA](results/ea.md) (explicit sparse) | 138.0 ms | 1.37 s | 7.71 s | — | — | — |

> Notes: `plonkish` (`BaseFold` and `plonkish-sdig3`) uses 16 B/element vs. 8 B/element in the other Goldilocks encoders. `ERA` uses a `1.05×` inner Brakedown code (`ρ ≈ 0.476`). Missing entries (`—`) at larger `k` reflect host/process memory limits (420–503 GiB).

### Goldilocks (64-bit) — Rate 1/4

| Code / Variant | `k=20` | `k=22` | `k=24` | `k=26` | `k=28` | `k=30` |
|---|---:|---:|---:|---:|---:|---:|
| [HyperFold](results/hyperfold.md) (`r=8`, QA) | 5.61 ms | 25.0 ms | 118.5 ms | 485.0 ms | 2.25 s | 9.39 s |
| [HyperFold](results/hyperfold.md) (`r=8`, RS) | 6.62 ms | 28.1 ms | 127.6 ms | 536.9 ms | 2.43 s | 9.99 s |
| [HyperFold](results/hyperfold.md) (`r=4`, QA) | 7.51 ms | 32.3 ms | 151.8 ms | 683.1 ms | 3.07 s | 12.73 s |
| [HyperFold](results/hyperfold.md) (`r=4`, RS) | 8.35 ms | 34.4 ms | 160.9 ms | 722.1 ms | 3.21 s | 13.33 s |
| [Reed–Solomon](results/rs.md) (Plonky3 coset LDE) | 22.4 ms | 91.3 ms | 290.0 ms | 1.17 s | 5.15 s | 21.42 s |
| [HyperFold](results/hyperfold.md) (`r=2`, QA) | 13.1 ms | 59.4 ms | 281.5 ms | 1.29 s | 5.78 s | 24.84 s |
| [Systematic QA](results/qa.md) (packed WHT) | 9.17 ms | 36.2 ms | 234.9 ms | 1.30 s | 5.70 s | 25.23 s |
| [HyperFold](results/hyperfold.md) (`r=2`, RS) | 13.3 ms | 62.1 ms | 291.1 ms | 1.31 s | 5.89 s | 25.46 s |
| [RAA](results/raa.md) (unweighted) | 15.8 ms | 71.5 ms | 306.4 ms | 1.35 s | 5.61 s | 26.89 s |
| [ERA](results/era.md) (`ρ ≈ 0.238`) | 20.9 ms | 134.8 ms | 525.5 ms | 2.22 s | 10.80 s | — |
| [BaseFold](results/basefold.md) (`r=2` RFC, 16B) | 220.7 ms | 985.9 ms | 4.37 s | 21.28 s | 110.20 s | — |
| [Brakedown](results/brakedown.md) (recursive) | 26.7 ms | 196.7 ms | 1.16 s | 5.34 s | — | — |
| [EA](results/ea.md) (explicit sparse) | 148.2 ms | 1.45 s | 8.01 s | — | — | — |

### Binary `GF(2^32)` — Rate 1/2

| Code / Variant | `k=20` | `k=22` | `k=24` | `k=26` | `k=28` | `k=30` |
|---|---:|---:|---:|---:|---:|---:|
| [Additive RS](results/additive-rs.md) (Plonky3 LCH) | 6.93 ms | 20.6 ms | 57.1 ms | 214.0 ms | 926.8 ms | 3.86 s |
| [Systematic QA](results/qa.md) (binary spectral) | 3.38 ms | 10.2 ms | 51.3 ms | 219.6 ms | 918.7 ms | 4.03 s |
| [Binary HyperFold](results/binary-hyperfold.md) (`r=8`, RS) | 22.7 ms | 49.3 ms | 177.1 ms | 961.5 ms | 3.61 s | 14.43 s |
| [RAA](results/raa.md) (`bolt-raa`) | 12.4 ms | 56.3 ms | 220.0 ms | 900.9 ms | 4.32 s | 15.51 s |
| [Binary HyperFold](results/binary-hyperfold.md) (`r=4`, RS) | 27.6 ms | 81.6 ms | 290.2 ms | 1.23 s | 4.98 s | 19.73 s |
| [Binary HyperFold](results/binary-hyperfold.md) (`r=2`, RS) | 40.9 ms | 129.5 ms | 453.6 ms | 1.76 s | 7.36 s | 30.57 s |
| [Additive RS](results/additive-rs.md) (`bolt-rs`, `1T`) | 41.4 ms | 174.8 ms | 742.0 ms | 3.45 s | 15.79 s | 72.04 s |
| [Bolt](results/bolt.md) (`bolt-xor`, `ρ=0.800`) | 81.6 ms | 324.8 ms | 1.31 s | 5.03 s | 20.56 s | 80.81 s |
| [Bolt](results/bolt.md) (`bolt32`, `ρ=0.800`) | 80.3 ms | 320.9 ms | 1.39 s | 5.36 s | 20.86 s | 82.04 s |
| [Brakedown](results/brakedown.md) (`bolt-binary`) | 506.6 ms | 2.27 s | 9.31 s | 38.03 s | 153.91 s | — |

> Notes: `Bolt` includes systematic input plus inner RS parity, yielding actual code rate `0.800` (with inner `1/2`) or `0.667` (with inner `1/4`). `bolt-rs` additive RS runs on `1` thread.

### Binary `GF(2^32)` — Rate 1/4

| Code / Variant | `k=20` | `k=22` | `k=24` | `k=26` | `k=28` | `k=30` |
|---|---:|---:|---:|---:|---:|---:|
| [Additive RS](results/additive-rs.md) (Plonky3 LCH) | 10.6 ms | 27.7 ms | 104.0 ms | 406.1 ms | 1.71 s | 7.60 s |
| [Systematic QA](results/qa.md) (binary spectral) | 7.31 ms | 23.1 ms | 85.0 ms | 438.6 ms | 1.96 s | 8.40 s |
| [Binary HyperFold](results/binary-hyperfold.md) (`r=8`, RS) | 28.6 ms | 120.0 ms | 368.5 ms | 1.78 s | 7.92 s | 28.91 s |
| [RAA](results/raa.md) (`bolt-raa`) | 26.8 ms | 110.9 ms | 455.5 ms | 1.92 s | 7.64 s | 33.87 s |
| [Binary HyperFold](results/binary-hyperfold.md) (`r=4`, RS) | 34.3 ms | 119.4 ms | 448.2 ms | 1.93 s | 8.44 s | 36.89 s |
| [Binary HyperFold](results/binary-hyperfold.md) (`r=2`, RS) | 51.0 ms | 176.3 ms | 700.9 ms | 2.94 s | 12.75 s | 55.12 s |
| [Bolt](results/bolt.md) (`bolt-xor`, `ρ=0.667`) | 85.8 ms | 343.6 ms | 1.39 s | 5.57 s | 22.34 s | 87.33 s |
| [Bolt](results/bolt.md) (`bolt32`, `ρ=0.667`) | 86.5 ms | 345.7 ms | 1.40 s | 5.71 s | 22.83 s | 92.19 s |
| [Additive RS](results/additive-rs.md) (`bolt-rs`, `1T`) | 81.6 ms | 344.8 ms | 1.46 s | 7.05 s | 31.99 s | 150.01 s |
| [Brakedown](results/brakedown.md) (`bolt-binary`) | 1.40 s | 6.37 s | 26.62 s | 110.22 s | 458.69 s | — |

### Binary `GF(2^128)` — Rate 1/2

| Code / Variant | `k=20` | `k=22` | `k=24` | `k=26` | `k=28` | `k=30` |
|---|---:|---:|---:|---:|---:|---:|
| [Additive RS](results/additive-rs.md) (Plonky3 PolyBasis) | 4.47 ms | 28.3 ms | 79.7 ms | 370.9 ms | 1.12 s | 4.23 s |
| [Additive RS](results/additive-rs.md) (Plonky3 LCH) | 5.39 ms | 23.3 ms | 89.0 ms | 358.8 ms | 1.84 s | 8.03 s |
| [Systematic QA](results/qa.md) (binary spectral) | 8.30 ms | 41.3 ms | 176.3 ms | 807.7 ms | 3.53 s | 15.41 s |
| [RAA](results/raa.md) (`bolt-raa`) | 16.8 ms | 65.7 ms | 255.4 ms | 1.05 s | 4.32 s | 20.61 s |
| [Binary HyperFold](results/binary-hyperfold.md) (`r=8`, RS) | 30.9 ms | 145.2 ms | 478.9 ms | 2.27 s | 10.73 s | 34.83 s |
| [Binary HyperFold](results/binary-hyperfold.md) (`r=4`, RS) | 43.8 ms | 132.1 ms | 637.6 ms | 2.83 s | 11.90 s | 39.24 s |
| [Binary HyperFold](results/binary-hyperfold.md) (`r=2`, RS) | 66.0 ms | 209.6 ms | 887.5 ms | 3.60 s | 15.94 s | 57.25 s |

> Notes: `SPIN` (`128-bit` binary blocks, `1T`) and `QA` mixed subfield-to-extension encoders (`GF(2^32) -> GF(2^128)`, `GF(2^64) -> GF(2^128)`) are reported in [spin.md](results/spin.md) and [qa.md](results/qa.md).

### Binary `GF(2^128)` — Rate 1/4

| Code / Variant | `k=20` | `k=22` | `k=24` | `k=26` | `k=28` | `k=30` |
|---|---:|---:|---:|---:|---:|---:|
| [Additive RS](results/additive-rs.md) (Plonky3 PolyBasis) | 7.41 ms | 51.2 ms | 168.1 ms | 687.3 ms | 2.09 s | 7.99 s |
| [Additive RS](results/additive-rs.md) (Plonky3 LCH) | 9.31 ms | 36.2 ms | 147.5 ms | 590.2 ms | 3.13 s | 13.33 s |
| [Systematic QA](results/qa.md) (binary spectral) | 17.2 ms | 59.9 ms | 346.4 ms | 1.60 s | 7.02 s | 26.15 s |
| [RAA](results/raa.md) (`bolt-raa`) | 35.0 ms | 130.7 ms | 531.9 ms | 2.19 s | 9.48 s | 42.12 s |
| [Binary HyperFold](results/binary-hyperfold.md) (`r=8`, RS) | 52.0 ms | 254.6 ms | 970.5 ms | 4.56 s | 20.76 s | 66.63 s |
| [Binary HyperFold](results/binary-hyperfold.md) (`r=4`, RS) | 66.2 ms | 244.6 ms | 1.14 s | 5.05 s | 22.59 s | 76.54 s |
| [Binary HyperFold](results/binary-hyperfold.md) (`r=2`, RS) | 92.2 ms | 366.7 ms | 1.60 s | 7.70 s | 31.67 s | — |

### `M127` (127-bit Prime) — Rate 1/2

| Code / Variant | `k=20` | `k=22` | `k=24` | `k=26` | `k=28` | `k=30` |
|---|---:|---:|---:|---:|---:|---:|
| [HyperFold](results/hyperfold.md) (`r=8`, QA) | 10.4 ms | 31.0 ms | 140.8 ms | 569.7 ms | 2.60 s | 10.76 s |
| [HyperFold](results/hyperfold.md) (`r=4`, QA) | 13.4 ms | 42.4 ms | 192.9 ms | 847.3 ms | 3.72 s | 15.31 s |
| [HyperFold](results/hyperfold.md) (`r=8`, RS) | 26.5 ms | 65.0 ms | 231.4 ms | 1.67 s | 4.77 s | 16.01 s |
| [HyperFold](results/hyperfold.md) (`r=4`, RS) | 19.0 ms | 67.5 ms | 279.0 ms | 1.16 s | 4.88 s | 19.94 s |
| [Systematic QA](results/qa.md) (packed WHT) | 10.1 ms | 41.4 ms | 268.7 ms | 1.30 s | 5.85 s | 26.02 s |
| [HyperFold](results/hyperfold.md) (`r=2`, QA) | 15.5 ms | 60.1 ms | 295.7 ms | 1.36 s | 6.26 s | 27.82 s |
| [HyperFold](results/hyperfold.md) (`r=2`, RS) | 20.5 ms | 85.5 ms | 381.4 ms | 1.67 s | 7.44 s | 32.37 s |
| [BaseFold](results/basefold.md) (`r=2` RFC) | 139.0 ms | 421.7 ms | 1.88 s | 8.21 s | 42.27 s | 175.71 s |
| [Brakedown](results/brakedown.md) (`plonkish`, `ρ=0.657`, `1T`) | 238.2 ms | 1.33 s | 8.34 s | 39.94 s | 169.12 s | — |

### `M127` (127-bit Prime) — Rate 1/4

| Code / Variant | `k=20` | `k=22` | `k=24` | `k=26` | `k=28` | `k=30` |
|---|---:|---:|---:|---:|---:|---:|
| [HyperFold](results/hyperfold.md) (`r=8`, QA) | 18.2 ms | 62.1 ms | 283.1 ms | 1.18 s | 5.20 s | 19.97 s |
| [HyperFold](results/hyperfold.md) (`r=4`, QA) | 20.6 ms | 87.5 ms | 392.8 ms | 1.73 s | 7.56 s | 28.60 s |
| [HyperFold](results/hyperfold.md) (`r=8`, RS) | 56.5 ms | 146.4 ms | 449.9 ms | 3.90 s | 10.53 s | 30.51 s |
| [HyperFold](results/hyperfold.md) (`r=4`, RS) | 30.0 ms | 130.1 ms | 559.0 ms | 2.39 s | 10.25 s | 39.53 s |
| [HyperFold](results/hyperfold.md) (`r=2`, QA) | 25.4 ms | 130.3 ms | 605.7 ms | 2.86 s | 13.23 s | 48.64 s |
| [Systematic QA](results/qa.md) (packed WHT) | 19.3 ms | 79.0 ms | 520.7 ms | 2.60 s | 11.42 s | 57.86 s |
| [HyperFold](results/hyperfold.md) (`r=2`, RS) | 34.3 ms | 173.6 ms | 771.2 ms | 3.54 s | 15.74 s | 59.22 s |
| [BaseFold](results/basefold.md) (`r=2` RFC) | 180.0 ms | 793.8 ms | 3.52 s | 14.84 s | 79.37 s | — |

## Benchmarked Code Families

Full tables including `Setup` time, arithmetic mean and median `Encode` time, `Peak RSS`, and additional native fields (`M127`, `BabyBear`, `Ft127`, `secp256k1`, `Ristretto255`, `BN254`, `GF(2^16)`, `GF(2^64)`, `block128`):

| Code Family | Variants / Implementations | Field(s) | Rate(s) | Range (`k`) | Threads | Data |
|---|---|---|---|---|---|---|
| HyperFold | `r2`/`r4`/`r8` × (`QA`, `RS`) | Goldilocks, M127 | `1/2`, `1/4` | 20–30 | 32T | [md](results/hyperfold.md) · [csv](results/hyperfold.csv) |
| Binary HyperFold | `r2`/`r4`/`r8` (`RS` base) | `GF(2^16/32/64/128)` | `1/2`, `1/4` | 20–30 | 32T | [md](results/binary-hyperfold.md) · [csv](results/binary-hyperfold.csv) |
| Systematic QA | Binary Spectral, Packed WHT | `GF(2^32/64/128)` (+ mixed), Goldilocks, M127 | `1/2`, `1/4` | 20–30 | 32T | [md](results/qa.md) · [csv](results/qa.csv) |
| Reed–Solomon | Plonky3 coset LDE | Goldilocks, BabyBear | `1/2`, `1/4` | 20–30 (BB: 24/26) | 32T | [md](results/rs.md) · [csv](results/rs.csv) |
| Additive RS | Plonky3 `LCH`, `PolyBasis`; Bolt RS (`1T`) | `GF(2^32)`, `GF(2^64)`, `GF(2^128)` | `1/2`, `1/4` | 20–30 | 32T / 1T | [md](results/additive-rs.md) · [csv](results/additive-rs.csv) |
| BaseFold (RFC) | `r = 2` RS-base RFC | Goldilocks (`16B`), M127 | `1/2`, `1/4` | 20–30 | 32T | [md](results/basefold.md) · [csv](results/basefold.csv) |
| RAA | ERA `unweighted`, `bolt-raa`, `blaze-u64`, `EACode` (`1T`) | Goldilocks, `secp256k1`, `Ristretto255`, `GF(2^32/64/128)` | `1/2`, `1/4` | 20–30 | 32T / 1T | [md](results/raa.md) · [csv](results/raa.csv) |
| EA (Explicit) | `ea-explicit`, `EACode` | Goldilocks, `secp256k1`, `Ristretto255` | `1/2`, `1/4` | 20–24 | 32T | [md](results/ea.md) · [csv](results/ea.csv) |
| ERA | Brakedown + Repeat–Accumulate | Goldilocks, `secp256k1` | `0.476`, `0.238` (native) | 20–30 (secp: 28) | 32T | [md](results/era.md) · [csv](results/era.csv) |
| Brakedown | ERA `recursive`, `bolt-binary`, `lcpc` (`1T`), `plonkish` (`1T`) | Goldilocks, M127, `Ft127`, `secp256k1`, `GF(2^32)` | `1/2`, `1/4`, native (`0.506`–`0.680`) | 20–28 (sdig2: 30) | 32T / 1T | [md](results/brakedown.md) · [csv](results/brakedown.csv) |
| Bolt | `bolt-xor`, `bolt32` | `GF(2^32)` | `0.800`, `0.667` (native) | 20–30 | 32T | [md](results/bolt.md) · [csv](results/bolt.csv) |
| Lightning | `ldpc-brakedown` (`1T`) | `u64 -> BN254 Fr` | `1/2`, native (`0.61–0.78`) | 20–30 | 1T | [md](results/lightning.md) · [csv](results/lightning.csv) |
| SPIN | `imt`, `packet` (`1T`) | 128-bit binary blocks | `1/2` | 20–30 (`packet`: 26) | 1T | [md](results/spin.md) · [csv](results/spin.csv) |

## Conventions

- Each code family lives in `results/<code_family>.md` (setup, parameters, summary tables, notes) and `results/<code_family>.csv` (timings and memory).
- **Input & Rates**: Each entry encodes `K = 2^k` input elements into `N = K / ρ` codeword elements. `ERA` and `Bolt` include inner-code redundancy (`ρ ≈ 0.476 / 0.238` and `ρ = 0.800 / 0.667`, respectively).
- **Timing & Memory**: `Setup` (parameter/graph generation) and `Encode` (encoding `K` elements, excluding input generation) are measured across 1 warmup + 3 runs on an AMD EPYC 9754 (503 GiB RAM, 32 pinned cores, `target-cpu=native`). `Peak RSS` reports process peak resident memory in GiB.
- **Element Width & Parallelism**: `plonkish_basefold` stores Goldilocks elements in 16 bytes (vs. 8 bytes in Plonky3 and HyperFold); `Lightning` takes `u64` inputs with `BN254` parity symbols; `SPIN` operates on 128-bit blocks; `bolt-rs` RS, `lcpc`, `plonkish-sdig3`, `Lightning`, `SPIN`, and `EACode` RAA execute single-threaded (`1T`).
- Use [`TEMPLATE.md`](TEMPLATE.md) when adding new code families. Runner scripts and raw logs from the initial sweep remain in commit [`9038389`](https://github.com/jjllzhang/code-bench/tree/9038389e4e7c10fe90ee59affcb2647142114cfa).
