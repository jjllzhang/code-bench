# Reproduce the encoding campaign

An input is one vector of K = 2^k native symbols. A driver calls one encoder and checks one complete codeword of length N. Matrix APIs use one row or one column, depending on storage convention. The internal recursive and packet layouts of a single codeword are part of its encoder. Each invocation encodes one message.

## Inputs and clocks

- The grid uses k = 20, 22, 24, 26, 28, and 30. Most families use N = 2K and 4K. The reported rate is K/N. For Bolt, the nominal rate refers to its inner RS code. For ERA, the nominal rate identifies the repeat factor. Native-rate variants include their actual codeword length.
- The elapsed interval starts at the native encoder call and ends when the complete encoded data are available. Input generation, reset for in-place entry points, setup tables and graphs, correctness checks, and hashing are outside that interval. Allocation-returning APIs include their own allocations and scratch work.
- Each process takes one warmup and three formal samples. The driver reuses or prefaults caller-owned buffers and logs timed minor and major faults. Some allocation-returning encoders retained minor faults after warming. The recorded times include them.
- Fixed affinity binds every process to EPYC 9754 CPUs 0–31, 32 physical cores on NUMA node 0. Rayon and OpenMP pools allow 32 threads. The threads column reports 1 where the selected stock encode path is serial. Earlier runs shared the machine with builds on separate cores. Processes have a maximum 420 GiB virtual-address-space allowance, lowered when host memory is needed by other work. RSS is the whole-process peak, including setup.
- Plonky3's prime RS baseline starts from evaluations on a subgroup, as required by the coset LDE API. The RFC BaseFold and additive RS inputs are coefficients. Other drivers use the native source representation, including 16-byte Goldilocks in the original plonkish harness, subfield witnesses in mixed Binary QA, 128-bit records in SPIN, and uint64 input with BN254 parity in Lightning. Throughput counts actual input storage. These are encoder measurements at the stated code parameters. Minimum distances and PCS security are outside the comparison.

Native source setup may consume system randomness. Lightning seeds its message and control parameters, while graph edges and some BN254 weights are drawn from system random sources. Rerunning reproduces the geometry and timing protocol.

## Executable provenance

The first 270 formal cases ran with the core and Bolt binaries listed in [the executable manifest](host/binary-sha256.txt). The early runner recorded the executable path and command for each case. It gained per-case binary hashes after those cases.

The four k=20 plonkish BF64 packed RAA and M127 BaseFold cases used [the original plonkish binary](host/sdig3-old-binary.txt). The rebuild corrected parity reset in the plonkish Brakedown path. The earlier M127 Brakedown run was archived outside the grid. Formal Brakedown samples use [the corrected binary](host/sdig3-new-binary.txt).

## Build

The source checkouts and artifact snapshots are identified in [sources.json](sources.json). The materialize script accepts paths to those inputs, checks the revisions or source hashes, and applies the stored benchmark patches into the empty source directory. SPIN and Lightning use a C++20 compiler, CMake, and the listed mcl checkout. MCL_ROOT should point at that checkout with a Release build under build/lib/.

Use the public Plonky3 checkout at the `p3.commit` pin for `--p3`. The included patch reconstructs the measured Binary QA source on that pin and adds the RS setup timing hook. The measured QA revision is recorded separately in the manifest.

~~~sh
cd benchmarks
python3 scripts/materialize.py --help
scripts/compile-rust.sh core era bolt plonkish eacode lcpc
MCL_ROOT=/path/to/mcl scripts/compile-cpp.sh lightning spin
python3 run.py --dry-run
python3 run.py
python3 audit_raw.py --samples samples.csv
~~~

For existing data, unpack the raw archive into this directory and copy the three track CSVs from ../results/tracks/ into results/ before running the audit. To measure a subset, use the executable and k options listed by the runner help. Each complete attempt is retained and skipped on repeat invocations. Temp logs from interrupted attempts are preserved under raw/incomplete-attempts/.

## Statuses

OK contains three observed samples. DOMAIN_LIMIT, UNSUPPORTED_BACKEND, and EXCLUDED_INTERLEAVED give the source dispatch restrictions. OOM_SKIPPED is based on a preflight memory lower bound. OOM_LIMIT records an observed allocation failure under the experiment cap. HOST_MEMORY_LIMIT records an allocation failure under a lower shared-host cap. FAILED reports an execution error. These statuses carry no timing.

The estimate for a configured sparse graph counts elements at their actual storage widths. It is used to avoid a launch only when those required allocations alone exceed the experiment ceiling.
