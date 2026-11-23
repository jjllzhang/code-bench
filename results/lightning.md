# Lightning (LDPC Sketch + Brakedown Inner Code)

Single-polynomial 1D encoding benchmarks for `lightning` (Zoo #13; status summary: OK: 17, OOM_LIMIT: 1).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`taskset -c 0-31`, `RAYON_NUM_THREADS=32`, `OMP_NUM_THREADS=32`); release build (`target-cpu=native`)
- **Repositories / Revisions**: `Lightning@08dbd81b0785c78704b9dafc0315d793760a97fe`
- **Field(s)**: `bn254`
- **Message Lengths**: `K = 2^k` (`k ∈ {20, 22, 24, 26, 28, 30}`)
- **1D Geometry**: Single codeword (`nrows = 1`, `width = 1`, `log_batch_size = 0`; no interleaving, no 2D matrix reshape)

## Measurement Methodology

- **Sampling**: 1 warmup + 3 serial measured runs; reports arithmetic mean and median.
- **Timing Scope**: Measures the native 1D encoder call (`input_elements` -> `codeword_elements`) only; excludes setup (`setup_ms`), input generation, caller-buffer reset (for in-place entry points), correctness checks, and Merkle hashing/opening. Before timing, the driver pre-touches or reuses caller-owned buffers; output and temporary scratch buffers allocated internally by the encoder during the timed interval can still trigger page faults, and those times are included in the recorded measurements (per-row minor/major fault counts are logged in `results/lightning.csv` `notes`).
- **Memory**. `Peak RSS` is whole-process peak resident memory (`GiB`), including setup.

## Results

| Variant | Field | Nominal Rate | Actual Rate | k | T | Setup (ms) | Mean Encode (ms) | Median Encode (ms) | Peak RSS (GiB) | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `ldpc-brakedown` | `bn254` | `half` | 0.5000 | 20 | 1 | 1582.43 | 922.042 | 920.155 | 0.445 | `OK` |
| `ldpc-brakedown` | `bn254` | `half` | 0.5000 | 22 | 1 | 7363.76 | 6404.216 | 6412.754 | 1.912 | `OK` |
| `ldpc-brakedown` | `bn254` | `half` | 0.5000 | 24 | 1 | 32196.03 | 36003.128 | 35987.081 | 7.639 | `OK` |
| `ldpc-brakedown` | `bn254` | `half` | 0.5000 | 26 | 1 | 137786.79 | 163944.070 | 164010.214 | 30.830 | `OK` |
| `ldpc-brakedown` | `bn254` | `half` | 0.5000 | 28 | 1 | 562233.26 | 871511.532 | 881494.635 | 123.453 | `OK` |
| `ldpc-brakedown` | `bn254` | `half` | — | 30 | 1 | — | — | — | 416.729 | `OOM_LIMIT` |
| `ldpc-brakedown` | `bn254` | `native-high` | 0.6667 | 20 | 1 | 95.08 | 579.221 | 576.479 | 0.119 | `OK` |
| `ldpc-brakedown` | `bn254` | `native-high` | 0.7633 | 22 | 1 | 2130.10 | 3305.111 | 3304.068 | 0.730 | `OK` |
| `ldpc-brakedown` | `bn254` | `native-high` | 0.7782 | 24 | 1 | 10406.29 | 22448.416 | 22452.884 | 3.053 | `OK` |
| `ldpc-brakedown` | `bn254` | `native-high` | 0.7782 | 26 | 1 | 50136.76 | 108872.133 | 109486.568 | 12.201 | `OK` |
| `ldpc-brakedown` | `bn254` | `native-high` | 0.7805 | 28 | 1 | 215473.33 | 468512.294 | 468209.424 | 49.055 | `OK` |
| `ldpc-brakedown` | `bn254` | `native-high` | 0.7805 | 30 | 1 | 921642.58 | 2795199.004 | 2790716.226 | 196.350 | `OK` |
| `ldpc-brakedown` | `bn254` | `native-low` | 0.6074 | 20 | 1 | 974.85 | 605.119 | 606.485 | 0.299 | `OK` |
| `ldpc-brakedown` | `bn254` | `native-low` | 0.6074 | 22 | 1 | 4050.45 | 4946.751 | 4943.700 | 1.188 | `OK` |
| `ldpc-brakedown` | `bn254` | `native-low` | 0.6253 | 24 | 1 | 20025.88 | 27469.379 | 27469.079 | 5.043 | `OK` |
| `ldpc-brakedown` | `bn254` | `native-low` | 0.6277 | 26 | 1 | 87973.17 | 130206.762 | 130234.278 | 20.301 | `OK` |
| `ldpc-brakedown` | `bn254` | `native-low` | 0.6277 | 28 | 1 | 361783.94 | 608270.737 | 608180.758 | 81.195 | `OK` |
| `ldpc-brakedown` | `bn254` | `native-low` | 0.6281 | 30 | 1 | 1525720.34 | 3574200.543 | 3567619.954 | 325.037 | `OK` |

## Notes & Boundaries

- `ldpc-brakedown` (`bn254`, config rate `half`, `OK`): Original uint64 input and BN254 operations. Sparse aggregation and inner encoder are serial. input_storage=u64 output_parity_storage=32 actual_sketch_fraction=0.699826 degree=9
- `ldpc-brakedown` (`bn254`, config rate `half`, `OK`): Original uint64 input and BN254 operations. Sparse aggregation and inner encoder are serial. input_storage=u64 output_parity_storage=32 actual_sketch_fraction=0.703264 degree=9
- `ldpc-brakedown` (`bn254`, config rate `half`, `OK`): Original uint64 input and BN254 operations. Sparse aggregation and inner encoder are serial. input_storage=u64 output_parity_storage=32 actual_sketch_fraction=0.703265 degree=9
- `ldpc-brakedown` (`bn254`, config rate `half`, `OK`): Original uint64 input and BN254 operations. Sparse aggregation and inner encoder are serial. input_storage=u64 output_parity_storage=32 actual_sketch_fraction=0.704051 degree=9
- `ldpc-brakedown` (`bn254`, config rate `half`, `OK`): Original uint64 input and BN254 operations. Sparse aggregation and inner encoder are serial. input_storage=u64 output_parity_storage=32 actual_sketch_fraction=0.704197 degree=9
- `ldpc-brakedown` (`bn254`, config rate `half`, `OOM_LIMIT`): Original uint64 input and BN254 operations. Sparse aggregation and inner encoder are serial. exit=134; see raw/native_fields_1d-lightning-ldpc-brakedown-bn254-30-half.
- `ldpc-brakedown` (`bn254`, config rate `native-high`, `OK`): Original uint64 input and BN254 operations. Sparse aggregation and inner encoder are serial. input_storage=u64 output_parity_storage=32 actual_sketch_fraction=0.198 degree=10
- `ldpc-brakedown` (`bn254`, config rate `native-high`, `OK`): Original uint64 input and BN254 operations. Sparse aggregation and inner encoder are serial. input_storage=u64 output_parity_storage=32 actual_sketch_fraction=0.198001 degree=10
- `ldpc-brakedown` (`bn254`, config rate `native-low`, `OK`): Original uint64 input and BN254 operations. Sparse aggregation and inner encoder are serial. input_storage=u64 output_parity_storage=32 actual_sketch_fraction=0.417 degree=9
- `ldpc-brakedown` (`bn254`, config rate `native-low`, `OK`): Original uint64 input and BN254 operations. Sparse aggregation and inner encoder are serial. input_storage=u64 output_parity_storage=32 actual_sketch_fraction=0.417001 degree=9
