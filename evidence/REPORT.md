# Single-polynomial encoding results

704 completed points contribute 2112 timed samples.
The full grid contains 786 points.

| Track | Measured | Domain limit | Unsupported | Interleaved | Preflight memory bound | Runtime memory failure | Other |
|---|---:|---:|---:|---:|---:|---:|---:|
| prime_goldilocks_1d | 150 | 0 | 0 | 0 | 8 | 4 | 0 |
| binary_1d | 365 | 2 | 24 | 0 | 3 | 2 | 0 |
| native_fields_1d | 189 | 6 | 0 | 12 | 18 | 3 | 0 |

| log₂ K | Measured | Grid points |
|---|---:|---:|
| 20 | 125 | 131 |
| 22 | 125 | 131 |
| 24 | 125 | 131 |
| 26 | 118 | 131 |
| 28 | 113 | 131 |
| 30 | 98 | 131 |

## Matched examples at rate 1/2

Times are the median of three samples. The full data are [grouped by code family](../results/).

| Field | log₂ K | Variant | Encode (ms) | Setup (ms) | Peak RSS (GiB) |
|---|---:|---|---:|---:|---:|
| goldilocks | 20 | [rs](../results/rs.md) / p3-coset-lde | 16.910 | 10.814 | 0.029 |
| goldilocks | 24 | [rs](../results/rs.md) / p3-coset-lde | 258.672 | 125.103 | 0.729 |
| goldilocks | 28 | [rs](../results/rs.md) / p3-coset-lde | 3832.318 | 1832.083 | 11.975 |
| goldilocks | 30 | [rs](../results/rs.md) / p3-coset-lde | 16699.257 | 7629.364 | 47.975 |
| goldilocks | 20 | [qa](../results/qa.md) / packed-wht | 5.138 | 21.202 | 0.041 |
| goldilocks | 24 | [qa](../results/qa.md) / packed-wht | 117.257 | 306.999 | 0.627 |
| goldilocks | 28 | [qa](../results/qa.md) / packed-wht | 3051.839 | 4816.915 | 10.002 |
| goldilocks | 30 | [qa](../results/qa.md) / packed-wht | 12893.794 | 18625.350 | 40.002 |
| goldilocks | 20 | [hyperfold](../results/hyperfold.md) / r4-qa | 3.777 | 23.513 | 0.043 |
| goldilocks | 24 | [hyperfold](../results/hyperfold.md) / r4-qa | 74.929 | 266.232 | 1.092 |
| goldilocks | 28 | [hyperfold](../results/hyperfold.md) / r4-qa | 1536.416 | 3484.588 | 17.975 |
| goldilocks | 30 | [hyperfold](../results/hyperfold.md) / r4-qa | 6782.386 | 13482.185 | 71.975 |
| goldilocks | 20 | [hyperfold](../results/hyperfold.md) / r8-qa | 2.851 | 20.723 | 0.035 |
| goldilocks | 24 | [hyperfold](../results/hyperfold.md) / r8-qa | 53.353 | 266.498 | 1.096 |
| goldilocks | 28 | [hyperfold](../results/hyperfold.md) / r8-qa | 1122.967 | 3463.478 | 17.973 |
| goldilocks | 30 | [hyperfold](../results/hyperfold.md) / r8-qa | 4653.357 | 13547.635 | 71.969 |
| goldilocks | 20 | [brakedown](../results/brakedown.md) / brakedown-recursive | 16.826 | 3471.749 | 0.941 |
| goldilocks | 24 | [brakedown](../results/brakedown.md) / brakedown-recursive | 670.257 | 77996.001 | 15.037 |
| goldilocks | 28 | [brakedown](../results/brakedown.md) / brakedown-recursive | 18028.532 | 1590855.183 | 240.594 |
| bf32 | 20 | [additive-rs](../results/additive-rs.md) / lch | 6.930 | 0.000 | 0.006 |
| bf32 | 24 | [additive-rs](../results/additive-rs.md) / lch | 57.135 | 0.000 | 0.154 |
| bf32 | 28 | [additive-rs](../results/additive-rs.md) / lch | 926.804 | 0.000 | 2.990 |
| bf32 | 30 | [additive-rs](../results/additive-rs.md) / lch | 3856.658 | 0.000 | 11.975 |
| bf32 | 20 | [qa](../results/qa.md) / binary-spectral | 3.383 | 3.628 | 0.010 |
| bf32 | 24 | [qa](../results/qa.md) / binary-spectral | 51.325 | 57.385 | 0.283 |
| bf32 | 28 | [qa](../results/qa.md) / binary-spectral | 918.690 | 889.813 | 4.979 |
| bf32 | 30 | [qa](../results/qa.md) / binary-spectral | 4025.007 | 3573.125 | 19.973 |
| bf32 | 20 | [raa](../results/raa.md) / bolt-raa | 12.362 | 49.562 | 0.053 |
| bf32 | 24 | [raa](../results/raa.md) / bolt-raa | 220.039 | 1594.326 | 0.814 |
| bf32 | 28 | [raa](../results/raa.md) / bolt-raa | 4324.264 | 30112.222 | 13.002 |
| bf32 | 30 | [raa](../results/raa.md) / bolt-raa | 15508.369 | 157590.057 | 52.002 |
| bf64 | 20 | [binary-hyperfold](../results/binary-hyperfold.md) / r4-rs | 30.247 | 25.876 | 0.076 |
| bf64 | 24 | [binary-hyperfold](../results/binary-hyperfold.md) / r4-rs | 316.556 | 347.083 | 1.709 |
| bf64 | 28 | [binary-hyperfold](../results/binary-hyperfold.md) / r4-rs | 5438.234 | 4874.615 | 26.822 |
| bf64 | 30 | [binary-hyperfold](../results/binary-hyperfold.md) / r4-rs | 24326.952 | 18769.521 | 108.713 |
| bf128 | 20 | [additive-rs](../results/additive-rs.md) / polybasis | 4.470 | 0.000 | 0.049 |
| bf128 | 24 | [additive-rs](../results/additive-rs.md) / polybasis | 79.701 | 0.000 | 0.752 |
| bf128 | 28 | [additive-rs](../results/additive-rs.md) / polybasis | 1115.038 | 0.000 | 12.002 |
| bf128 | 30 | [additive-rs](../results/additive-rs.md) / polybasis | 4233.646 | 0.000 | 47.998 |

## Reading the measurements

- The timing columns measure the one-vector encoder call. Setup, input preparation, and commitment hashing have separate boundaries.
- Sizes measure native symbols. Some encoders use different storage widths for the same field.
- Actual code rates are computed from observed lengths. ERA adds redundancy in its Brakedown base code. Bolt adds inner RS parity to the systematic input.
- Binary HyperFold uses its released additive-RS base code. The independent Binary QA implementation has its own rows.
- The reference SIMD-Spielman targets encode columns of independent messages and are excluded.
- Setup plus encoding RSS is reported for each process. Encoders with owned scratch may still incur minor faults in timed samples.
- Runtime memory failures are allocations rejected under the 420 GiB process address-space limit. Preflight memory bounds identify cases skipped before launch.

[Methods and source revisions](../benchmarks/README.md)
