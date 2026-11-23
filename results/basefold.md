# BaseFold Random Foldable Codes (r = 2)

Single-polynomial 1D encoding benchmarks for `basefold` (Zoo #5; status summary: DOMAIN_LIMIT: 1, OK: 22, OOM_LIMIT: 1).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`taskset -c 0-31`, `RAYON_NUM_THREADS=32`, `OMP_NUM_THREADS=32`); release build (`target-cpu=native`)
- **Repositories / Revisions**: `plonkish_basefold@c29f08653121637b456e4705d901d078cd6fc668`
- **Field(s)**: `goldilocks`, `m127`
- **Message Lengths**: `K = 2^k` (`k ∈ {20, 22, 24, 26, 28, 30}`)
- **1D Geometry**: Single codeword (`nrows = 1`, `width = 1`, `log_batch_size = 0`; no interleaving, no 2D matrix reshape)

## Measurement Methodology

- **Sampling**: 1 warmup + 3 serial measured runs; reports arithmetic mean and median.
- **Timing Scope**: Measures the native 1D encoder call (`input_elements` -> `codeword_elements`) only; excludes setup (`setup_ms`), input generation, caller-buffer reset (for in-place entry points), correctness checks, and Merkle hashing/opening. Before timing, the driver pre-touches or reuses caller-owned buffers; output and temporary scratch buffers allocated internally by the encoder during the timed interval can still trigger page faults, and those times are included in the recorded measurements (per-row minor/major fault counts are logged in `results/basefold.csv` `notes`).
- **Memory**. `Peak RSS` is whole-process peak resident memory (`GiB`), including setup.

## Results

| Variant | Field | Nominal Rate | Actual Rate | k | T | Setup (ms) | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `rs64-rfc` | `m127` | `1/2` | 0.5000 | 20 | 32 | 395.12 | 138.114 | 139.048 | 0.230 | `OK` |
| `rs64-rfc` | `m127` | `1/2` | 0.5000 | 22 | 32 | 1607.58 | 436.869 | 421.684 | 1.037 | `OK` |
| `rs64-rfc` | `m127` | `1/2` | 0.5000 | 24 | 32 | 7137.49 | 1875.478 | 1876.162 | 4.219 | `OK` |
| `rs64-rfc` | `m127` | `1/2` | 0.5000 | 26 | 32 | 26806.57 | 8336.013 | 8214.804 | 16.973 | `OK` |
| `rs64-rfc` | `m127` | `1/2` | 0.5000 | 28 | 32 | 109451.88 | 42525.472 | 42268.924 | 67.975 | `OK` |
| `rs64-rfc` | `m127` | `1/2` | 0.5000 | 30 | 32 | 478663.11 | 175858.640 | 175708.707 | 271.977 | `OK` |
| `rs64-rfc` | `m127` | `1/4` | 0.2500 | 20 | 32 | 784.24 | 188.314 | 179.990 | 0.486 | `OK` |
| `rs64-rfc` | `m127` | `1/4` | 0.2500 | 22 | 32 | 3389.72 | 815.162 | 793.772 | 2.035 | `OK` |
| `rs64-rfc` | `m127` | `1/4` | 0.2500 | 24 | 32 | 14098.22 | 3571.384 | 3516.446 | 8.225 | `OK` |
| `rs64-rfc` | `m127` | `1/4` | 0.2500 | 26 | 32 | 57771.10 | 15077.845 | 14844.303 | 32.977 | `OK` |
| `rs64-rfc` | `m127` | `1/4` | 0.2500 | 28 | 32 | 231381.89 | 79169.185 | 79368.570 | 131.973 | `OK` |
| `rs64-rfc` | `m127` | `1/4` | — | 30 | 32 | — | — | — | — | `DOMAIN_LIMIT` |
| `rs64-rfc` | `goldilocks` | `1/2` | 0.5000 | 20 | 32 | 381.20 | 117.924 | 115.750 | 0.211 | `OK` |
| `rs64-rfc` | `goldilocks` | `1/2` | 0.5000 | 22 | 32 | 1510.24 | 492.489 | 471.895 | 0.979 | `OK` |
| `rs64-rfc` | `goldilocks` | `1/2` | 0.5000 | 24 | 32 | 6870.52 | 2111.523 | 2112.577 | 3.971 | `OK` |
| `rs64-rfc` | `goldilocks` | `1/2` | 0.5000 | 26 | 32 | 27504.71 | 9397.751 | 9299.605 | 15.975 | `OK` |
| `rs64-rfc` | `goldilocks` | `1/2` | 0.5000 | 28 | 32 | 110290.03 | 48213.057 | 47682.146 | 63.977 | `OK` |
| `rs64-rfc` | `goldilocks` | `1/2` | 0.5000 | 30 | 32 | 461978.02 | 194032.512 | 193742.933 | 255.982 | `OK` |
| `rs64-rfc` | `goldilocks` | `1/4` | 0.2500 | 20 | 32 | 751.65 | 227.840 | 220.682 | 0.459 | `OK` |
| `rs64-rfc` | `goldilocks` | `1/4` | 0.2500 | 22 | 32 | 3245.97 | 996.560 | 985.890 | 1.910 | `OK` |
| `rs64-rfc` | `goldilocks` | `1/4` | 0.2500 | 24 | 32 | 13957.95 | 4369.395 | 4372.868 | 7.725 | `OK` |
| `rs64-rfc` | `goldilocks` | `1/4` | 0.2500 | 26 | 32 | 58312.41 | 21698.924 | 21283.420 | 30.975 | `OK` |
| `rs64-rfc` | `goldilocks` | `1/4` | 0.2500 | 28 | 32 | 219036.88 | 109490.207 | 110202.642 | 123.965 | `OK` |
| `rs64-rfc` | `goldilocks` | `1/4` | — | 30 | 32 | — | — | — | 399.969 | `OOM_LIMIT` |

## Notes & Boundaries

- `rs64-rfc` (`goldilocks`, config rate `1/2`, `OK`): Original field representations (Goldilocks occupies 16 B) and RS base encoder. Input coefficients.
- `rs64-rfc` (`goldilocks`, config rate `1/4`, `OK`): Original field representations (Goldilocks occupies 16 B) and RS base encoder. Input coefficients.
- `rs64-rfc` (`goldilocks`, config rate `1/4`, `OOM_LIMIT`): Original field representations (Goldilocks occupies 16 B) and RS base encoder. Input coefficients. exit=134; see raw/prime_goldilocks_1d-basefold-rs64-rfc-goldilocks-30-4.
- `rs64-rfc` (`m127`, config rate `1/2`, `OK`): Original field representations (Goldilocks occupies 16 B) and RS base encoder. Input coefficients.
- `rs64-rfc` (`m127`, config rate `1/4`, `DOMAIN_LIMIT`): Original field representations (Goldilocks occupies 16 B) and RS base encoder. Input coefficients. Original AES-CTR32 table stream cannot emit 2^32 blocks.
- `rs64-rfc` (`m127`, config rate `1/4`, `OK`): Original field representations (Goldilocks occupies 16 B) and RS base encoder. Input coefficients.
