# <Code Family> 1D Encoding Benchmark Results

Measurements of [<Implementation Name>](<repo-url>) (revision `<commit-or-tag>`) for single-polynomial 1D encoding over message lengths `K = 2^k` (`k ∈ {20, 22, 24, 26, 28, 30}`).

## Setup & Parameters

- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`taskset -c 0-31`, `RAYON_NUM_THREADS=32`, `OMP_NUM_THREADS=32`); optimized release build (`target-cpu=native`)
- **Code & Zoo Mapping**: Zoo `#<id>` — single-polynomial 1D linear encoding (`nrows = 1`, `width = 1`, `log_batch_size = 0`; no interleaving and no 2D matrix reshape)
- **Field(s)**: `<field>` (`<field_bits>`-bit base/input alphabet; note extension codeword field if hyphenated)
- **Code Rate(s)**: Nominal `<1/2, 1/4, native>` (report `actual_rate = input_elements / codeword_elements`)
- **Threads**: `32` (or `1` if upstream single-codeword kernel is serial)

## Measurement Methodology

- **Sampling**: 1 warmup run followed by 3 serial measured runs per configuration; reports **arithmetic mean** and **median**.
- **Timing Scope**: Measures the native 1D encoder call (`input_elements` -> `codeword_elements`) only; excludes setup/precomputation (`setup_ms`), input generation, caller-buffer reset (for in-place entry points), correctness checks, and Merkle hashing/opening. Before timing, the driver pre-touches or reuses caller-owned buffers; output and temporary scratch buffers allocated internally by the encoder during the timed interval can still trigger page faults, and those times are included in the recorded measurements (per-row minor/major fault counts are logged in `notes`).
- **Throughput & Memory**: `MElem/s = input_elements / 1e6 / (encode_mean_ms / 1000)`, `GiB/s = input_bytes / 2^30 / (encode_mean_ms / 1000)`. `Peak RSS` is process-wide peak resident memory (`GiB`), including setup.
- **Rate & Status Transparency**: Same-rate comparisons and rankings group strictly by the exact reduced fraction `K/N = input_elements / codeword_elements` (4-decimal values in tables are for display only, while retaining `nominal_rate` as configuration metadata, e.g., Bolt inner rate vs. full codeword `4/5`, or ERA repetition count vs. `1.05x` inner Brakedown rate). `OK` rows passed expected-length and non-zero checks; `DOMAIN_LIMIT`, `OOM_SKIPPED`, `OOM_LIMIT`, `HOST_MEMORY_LIMIT`, `EXCLUDED_INTERLEAVED`, `UNSUPPORTED_BACKEND`, and `PENDING` remain explicitly visible with rationale in Notes.

## Results

| Variant | Field | Nominal Rate | Actual Rate | k | Threads | Setup (ms) | Mean (ms) | Median (ms) | MElem/s | GiB/s | Peak RSS (GiB) | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| | | | | | | | | | | | | |

## Notes & Boundaries

- ...
