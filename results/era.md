# ERA (Encode–Repeat–Accumulate)

Single-polynomial 1D encoding benchmarks for `era` (Zoo #20; status summary: OK: 21, OOM_LIMIT: 1, OOM_SKIPPED: 2).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`taskset -c 0-31`, `RAYON_NUM_THREADS=32`, `OMP_NUM_THREADS=32`); release build (`target-cpu=native`)
- **Repositories / Revisions**: `ERA local source snapshot`
- **Field(s)**: `goldilocks`, `secp256k1`
- **Message Lengths**: `K = 2^k` (`k ∈ {20, 22, 24, 26, 28, 30}`)
- **1D Geometry**: Single codeword (`nrows = 1`, `width = 1`, `log_batch_size = 0`; no interleaving, no 2D matrix reshape)

## Measurement Methodology

- **Sampling**: 1 warmup + 3 serial measured runs; reports arithmetic mean and median.
- **Timing Scope**: Measures the native 1D encoder call (`input_elements` -> `codeword_elements`) only; excludes setup (`setup_ms`), input generation, caller-buffer reset (for in-place entry points), correctness checks, and Merkle hashing/opening. Before timing, the driver pre-touches or reuses caller-owned buffers; output and temporary scratch buffers allocated internally by the encoder during the timed interval can still trigger page faults, and those times are included in the recorded measurements (per-row minor/major fault counts are logged in `results/era.csv` `notes`).
- **Memory**. `Peak RSS` is whole-process peak resident memory (`GiB`), including setup.

## Results

| Variant | Field | Nominal Rate | Actual Rate | k | T | Setup (ms) | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `brakedown-repeat-accumulate` | `secp256k1` | `1/2` | 0.4762 | 20 | 32 | 4751.08 | 75.486 | 72.928 | 0.850 | `OK` |
| `brakedown-repeat-accumulate` | `secp256k1` | `1/2` | 0.4762 | 22 | 32 | 25128.04 | 418.114 | 415.953 | 3.658 | `OK` |
| `brakedown-repeat-accumulate` | `secp256k1` | `1/2` | 0.4762 | 24 | 32 | 103944.47 | 1425.536 | 1411.474 | 13.578 | `OK` |
| `brakedown-repeat-accumulate` | `secp256k1` | `1/2` | 0.4762 | 26 | 32 | 476990.96 | 6540.959 | 6478.455 | 54.307 | `OK` |
| `brakedown-repeat-accumulate` | `secp256k1` | `1/2` | 0.4762 | 28 | 32 | 2074464.61 | 25992.018 | 25824.959 | 217.217 | `OK` |
| `brakedown-repeat-accumulate` | `secp256k1` | `1/2` | — | 30 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `brakedown-repeat-accumulate` | `secp256k1` | `1/4` | 0.2381 | 20 | 32 | 5755.74 | 115.562 | 110.867 | 1.178 | `OK` |
| `brakedown-repeat-accumulate` | `secp256k1` | `1/4` | 0.2381 | 22 | 32 | 29177.66 | 542.615 | 535.481 | 4.707 | `OK` |
| `brakedown-repeat-accumulate` | `secp256k1` | `1/4` | 0.2381 | 24 | 32 | 120693.00 | 1781.571 | 1774.171 | 18.828 | `OK` |
| `brakedown-repeat-accumulate` | `secp256k1` | `1/4` | 0.2381 | 26 | 32 | 549341.80 | 7700.663 | 7694.662 | 75.307 | `OK` |
| `brakedown-repeat-accumulate` | `secp256k1` | `1/4` | 0.2381 | 28 | 32 | 2367602.81 | 30520.293 | 30411.289 | 301.219 | `OK` |
| `brakedown-repeat-accumulate` | `secp256k1` | `1/4` | — | 30 | 32 | — | — | — | — | `OOM_SKIPPED` |
| `brakedown-repeat-accumulate` | `goldilocks` | `1/2` | 0.4762 | 20 | 32 | 563.99 | 14.761 | 14.385 | 0.328 | `OK` |
| `brakedown-repeat-accumulate` | `goldilocks` | `1/2` | 0.4762 | 22 | 32 | 3071.86 | 78.027 | 77.995 | 1.307 | `OK` |
| `brakedown-repeat-accumulate` | `goldilocks` | `1/2` | 0.4762 | 24 | 32 | 14898.62 | 348.457 | 348.398 | 5.225 | `OK` |
| `brakedown-repeat-accumulate` | `goldilocks` | `1/2` | 0.4762 | 26 | 32 | 72330.42 | 1417.528 | 1415.725 | 20.898 | `OK` |
| `brakedown-repeat-accumulate` | `goldilocks` | `1/2` | 0.4762 | 28 | 32 | 318713.87 | 8143.806 | 8235.936 | 83.588 | `OK` |
| `brakedown-repeat-accumulate` | `goldilocks` | `1/2` | 0.4762 | 30 | 32 | 1530485.43 | 24758.263 | 24576.244 | 317.543 | `OK` |
| `brakedown-repeat-accumulate` | `goldilocks` | `1/4` | 0.2381 | 20 | 32 | 681.90 | 20.923 | 20.926 | 0.441 | `OK` |
| `brakedown-repeat-accumulate` | `goldilocks` | `1/4` | 0.2381 | 22 | 32 | 3689.94 | 134.703 | 134.827 | 1.768 | `OK` |
| `brakedown-repeat-accumulate` | `goldilocks` | `1/4` | 0.2381 | 24 | 32 | 17381.00 | 521.734 | 525.532 | 7.061 | `OK` |
| `brakedown-repeat-accumulate` | `goldilocks` | `1/4` | 0.2381 | 26 | 32 | 84100.96 | 2257.479 | 2221.407 | 28.248 | `OK` |
| `brakedown-repeat-accumulate` | `goldilocks` | `1/4` | 0.2381 | 28 | 32 | 365375.45 | 10806.003 | 10795.792 | 112.986 | `OK` |
| `brakedown-repeat-accumulate` | `goldilocks` | `1/4` | — | 30 | 32 | — | — | — | 418.340 | `OOM_LIMIT` |

## Notes & Boundaries

- `brakedown-repeat-accumulate` (`goldilocks`, config rate `1/2`, `OK`): Nominal repetition 2/4. Actual rate includes 1.05x inner Brakedown. alpha=0.04 inner_inverse_rate=1.05 c_n=8 d_n=64 repetition=2
- `brakedown-repeat-accumulate` (`goldilocks`, config rate `1/4`, `OK`): Nominal repetition 2/4. Actual rate includes 1.05x inner Brakedown. alpha=0.04 inner_inverse_rate=1.05 c_n=8 d_n=64 repetition=4
- `brakedown-repeat-accumulate` (`goldilocks`, config rate `1/4`, `OOM_LIMIT`): Nominal repetition 2/4. Actual rate includes 1.05x inner Brakedown. exit=134; see raw/prime_goldilocks_1d-era-brakedown-repeat-accumulate-goldilocks-30-4.
- `brakedown-repeat-accumulate` (`secp256k1`, config rate `1/2`, `OK`): Nominal repetition 2/4. Actual rate includes 1.05x inner Brakedown. alpha=0.04 inner_inverse_rate=1.05 c_n=8 d_n=64 repetition=2
- `brakedown-repeat-accumulate` (`secp256k1`, config rate `1/2`, `OOM_SKIPPED`): Nominal repetition 2/4. Actual rate includes 1.05x inner Brakedown. Retained ERA graph, permutations and weights lower bound 645.3 GiB.
- `brakedown-repeat-accumulate` (`secp256k1`, config rate `1/4`, `OK`): Nominal repetition 2/4. Actual rate includes 1.05x inner Brakedown. alpha=0.04 inner_inverse_rate=1.05 c_n=8 d_n=64 repetition=4
- `brakedown-repeat-accumulate` (`secp256k1`, config rate `1/4`, `OOM_SKIPPED`): Nominal repetition 2/4. Actual rate includes 1.05x inner Brakedown. Retained ERA graph, permutations and weights lower bound 813.3 GiB.
