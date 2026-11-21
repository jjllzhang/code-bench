#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mcl_root="${MCL_ROOT:?set MCL_ROOT to the mcl checkout}"
for code in "$@"; do
  case "$code" in
    spin)
      cmake -S source/spin/spin -B build/spin -DCMAKE_BUILD_TYPE=Release -DSPIN_BUILD_TESTS=OFF -DSPIN_TUNE=generic
      cmake --build build/spin --parallel 10
      g++ -std=c++20 -O3 -march=native -Isource/spin/spin/include cpp/spin.cpp build/spin/libspin.a -pthread -o bin/spin;;
    lightning)
      g++ -std=c++20 -O3 -march=native -I"$mcl_root/include" cpp/lightning.cpp source/lightning/brakedown.cpp           -L"$mcl_root/build/lib" -Wl,-rpath,"$mcl_root/build/lib" -lmcl -lgmp -lcrypto -o bin/lightning;;
    *) exit 2;;
  esac
done
