#!/usr/bin/env python3
"""Recompute the table from per-case geometry and unrounded timings."""
import argparse
from collections import Counter
import csv
import json
import math
from pathlib import Path
from statistics import median
from cases import grid

ROOT = Path(__file__).resolve().parent
KEYS = ("table_id", "code_family", "variant", "field", "k", "nominal_rate")
TRACKS = ("prime_goldilocks_1d", "binary_1d", "native_fields_1d")


def key(row):
    return tuple(str(row[k]) for k in KEYS)


def expected_out(case):
    n = 1 << case["k"]
    c = case["rate"]
    if not isinstance(c,int):
        return None
    family = case["code_family"]
    if family == "bolt":
        return n + (n//8)*c
    if family == "era":
        return int(n*1.05)*c
    return n*c


def close(observed, expected, name):
    if abs(float(observed) - expected) > 1e-8:
        raise ValueError(f"{name}: {observed} != {expected}")


def audit(allow_pending):
    rows = {}
    for track in TRACKS:
        with (ROOT / "results" / f"{track}.csv").open(newline="") as f:
            for row in csv.DictReader(f):
                ident = key(row)
                assert ident not in rows, ident
                rows[ident] = row
    assert len(rows) == len(grid()), (len(rows), len(grid()))
    samples = []
    checked = Counter()
    for case in grid():
        requested = case["rate"]
        row = rows[key(dict(case, nominal_rate=f"1/{requested}" if isinstance(requested,int) else requested))]
        status = row["status"]
        checked[status] += 1
        arc = ROOT / "raw" / case["id"]
        if status != "OK":
            assert not row["encode_mean_ms"] and not row["encode_median_ms"]
            if status == "PENDING" and not allow_pending:
                raise ValueError(f"Pending case: {case['id']}")
            continue
        assert json.loads((arc / "exit.json").read_text())["returncode"] == 0
        actual = (arc / "stdout.log").read_text().splitlines()
        geo, = [line.split()[1:] for line in actual if line.startswith("GEOMETRY ")]
        n, m, b = map(int,geo)
        assert n == 1<<case["k"] and int(row["input_elements"]) == n
        assert m >= n and int(row["codeword_elements"]) == m
        assert b == int(row["input_bytes"]) and b % n == 0
        guess = expected_out(case)
        assert guess in (None,m), (case["id"], guess, m)
        close(row["actual_rate"], n/m, "actual_rate")
        close(row["setup_ms"], float(next(r[6:] for r in actual if r.startswith("SETUP "))), "setup")
        reps = [line.split()[1:] for line in actual if line.startswith("ITER ")]
        assert [int(r[0]) for r in reps] == [0,1,2,3]
        assert all(int(r[2]) == m and math.isfinite(float(r[1])) and float(r[1]) > 0 for r in reps)
        times = [float(r[1]) for r in reps[1:]]
        mean = math.fsum(times)/3
        close(row["encode_mean_ms"], mean, "mean")
        close(row["encode_median_ms"], median(times), "median")
        close(row["throughput_melem_s"], n/mean/1000, "element throughput")
        close(row["throughput_gib_s"], b/2**30/mean*1000, "bytes throughput")
        for index, ms, encoded, minor, major in reps:
            samples.append((case["id"], index, ms, encoded, minor, major))
    return checked, samples


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--allow-pending", action="store_true")
    parser.add_argument("--samples", type=Path)
    args=parser.parse_args()
    checked, samples=audit(args.allow_pending)
    print(json.dumps(dict(status_counts=checked, raw_samples=len(samples), formal_samples=len(samples)*3//4), indent=2))
    if args.samples:
        with args.samples.open("w", newline="") as f:
            writer=csv.writer(f)
            writer.writerow(("case_id","iteration","encode_ms","codeword_elements","minor_faults","major_faults"))
            writer.writerows(samples)


if __name__=="__main__":
    main()
