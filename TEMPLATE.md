# <Code Family> Benchmark Results

Measurements of [<Implementation Name>](<repo-url>) over message lengths `K = 2^k` (`k ∈ {20, 22, 24, 26, 28, 30}`).

## Setup & Parameters

- **Hardware & Runtime**: e.g., AMD EPYC 9754, 503 GiB RAM, 32 physical cores (`target-cpu=native`); `32T` (or `1T` if single-threaded).
- **Field(s)**: e.g., Goldilocks (64-bit), `GF(2^32)`, `GF(2^128)`.
- **Code Parameters**: Rates (report both configured and actual `K / N` if they differ), base code, folding arity, or graph parameters.

## Measurement Methodology

- **Sampling**: 1 warmup followed by 3 measured runs; reports arithmetic mean and median encoding time.
- **Timing Scope**: `Encode` measures encoding time for `K = 2^k` input elements, excluding `Setup` and input generation. `Peak RSS` is process peak resident memory (GiB).
- **Missing Values**: `—` denotes an unmeasured configuration (e.g., finite-field domain bound or memory limit).

## Results

### <Variant> — <Field> (<Threads>)

| Rate | k | Setup | Mean Encode | Median Encode | Peak RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| `1/2` | 20 | | | | |

## Notes

- ...
