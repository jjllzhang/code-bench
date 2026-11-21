#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export RUSTFLAGS='-C target-cpu=native'
for code in "${@}"; do
  export CARGO_TARGET_DIR="$PWD/build/$code"
  case "$code" in
    plonkish)
      RUSTC_BOOTSTRAP=1 cargo build --offline --locked --release -j 10 --manifest-path source/plonkish/plonkish/Cargo.toml --example encoding_1d -p plonkish_backend
      cp "build/$code/release/examples/encoding_1d" "bin/$code";;
    eacode)
      cargo build --offline --locked --release -j 10 --manifest-path source/eacode/Cargo.toml --features ecc_pc --bin encode
      cp "build/$code/release/encode" "bin/$code";;
    lcpc)
      RUSTC_BOOTSTRAP=1 cargo build --locked --release -j 10 --manifest-path "$code/Cargo.toml"
      cp "build/$code/release/encoding-$code" "bin/$code";;
    *)
      cargo build --offline --locked --release -j 10 --manifest-path "$code/Cargo.toml"
      cp "build/$code/release/encoding-$code" "bin/$code";;
  esac
done
