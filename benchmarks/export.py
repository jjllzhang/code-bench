#!/usr/bin/env python3
"""Make the reviewed report and raw evidence archive from a completed campaign."""
import argparse
import csv
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
import tarfile

from audit_raw import audit, TRACKS
from cases import grid

ROOT = Path(__file__).resolve().parent


def all_rows():
    for name in TRACKS:
        with (ROOT/"results"/f"{name}.csv").open(newline="") as f:
            yield from csv.DictReader(f)


def summarize(rows, audit_counts, out):
    timed = [r for r in rows if r["status"]=="OK"]
    ratios = Counter(r["actual_rate"] for r in timed)
    table_counts = defaultdict(Counter)
    for row in rows:
        table_counts[row["table_id"]][row["status"]] += 1
    lines = [
        "# Single-polynomial encoding results", "",
        f"{len(timed)} completed points contribute {len(timed)*3} timed samples.",
        f"The full grid contains {len(rows)} points.", "",
        "| Track | Measured | Domain limit | Unsupported | Interleaved | Memory bound/failure | Other |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for track, outcome in table_counts.items():
        memory = sum(outcome[s] for s in ("OOM_LIMIT","HOST_MEMORY_LIMIT","OOM_SKIPPED"))
        other = sum(outcome.values()) - memory - sum(outcome[s] for s in ("OK","DOMAIN_LIMIT","UNSUPPORTED_BACKEND","EXCLUDED_INTERLEAVED"))
        lines.append(f"| {track} | {outcome['OK']} | {outcome['DOMAIN_LIMIT']} | {outcome['UNSUPPORTED_BACKEND']} | "
                     f"{outcome['EXCLUDED_INTERLEAVED']} | {memory} | {other} |")
    lines += ["", "## Matched examples at rate 1/2", "",
              "Times are the median of three samples. The rows link to full data grouped by code family.", "",
              "| Field | log₂ K | Variant | Encode (ms) | Setup (ms) | Peak RSS (GiB) |",
              "|---|---:|---|---:|---:|---:|"]
    picks = [
        ("goldilocks", "rs", "p3-coset-lde"),
        ("goldilocks", "qa", "packed-wht"),
        ("goldilocks", "hyperfold", "r4-qa"),
        ("goldilocks", "brakedown", "brakedown-recursive"),
        ("bf32", "additive-rs", "lch"),
        ("bf32", "qa", "binary-spectral"),
        ("bf64", "binary-hyperfold", "r4-rs"),
        ("bf128", "additive-rs", "polybasis"),
    ]
    by_kind = defaultdict(dict)
    for row in timed:
        if row["actual_rate"] == "0.500000000000":
            by_kind[(row["field"],row["code_family"],row["variant"])][int(row["k"])] = row
    for field, family, variant in picks:
        for k in (20,24,28,30):
            r=by_kind[field,family,variant].get(k)
            if r is not None:
                lines.append(f"| {field} | {k} | {family} / {variant} | {float(r['encode_median_ms']):.3f} | "
                             f"{float(r['setup_ms']):.3f} | {float(r['peak_rss_gib']):.3f} |")
    lines += ["", "## Reading the measurements", "",
              "- The timing columns measure the one-vector encoder call. Setup, input preparation, and commitment hashing have separate boundaries.",
              "- Sizes measure native symbols. The time and input-byte throughput are useful together when storage widths differ.",
              "- Actual code rates are computed from observed lengths. ERA adds redundancy in its Brakedown base code. Bolt adds inner RS parity to the systematic input.",
              "- Binary HyperFold uses its released additive-RS base code. The independent Binary QA implementation has its own rows.",
              "- The reference SIMD-Spielman targets encode columns of independent messages and are excluded.",
              "- Setup plus encoding RSS is reported for each process. Encoders with owned scratch may still incur minor faults in timed samples.",
              "", "[Methods and source revisions](benchmarks/README.md)", ""]
    (out/"REPORT.md").write_text("\n".join(lines))
    (out/"result-counts.json").write_text(json.dumps({"status_counts": dict(audit_counts),
          "by_track": {k:dict(v) for k,v in table_counts.items()},
          "successful_actual_rate_counts":dict(ratios)},indent=2)+"\n")


def export(out):
    counts, samples = audit(False)
    out.mkdir(parents=True, exist_ok=True)
    with (out/"raw-samples.csv").open("w",newline="") as f:
        w = csv.writer(f)
        w.writerow(("case_id","iteration","encode_ms","codeword_elements","minor_faults","major_faults"))
        w.writerows(samples)
    files = [p for c in grid() for p in sorted((ROOT/"raw"/c["id"]).glob("*"))
             if p.is_file() and (p.parent/"exit.json").is_file()]
    paths = []
    archive = out/"raw-evidence.tar.gz"
    with archive.open("wb") as raw, gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as gz, tarfile.open(fileobj=gz,mode="w|") as tf:
        for p in files:
            name = str(p.relative_to(ROOT))
            info=tf.gettarinfo(str(p),arcname=name)
            info.uid = info.gid = info.mtime = 0
            info.uname = info.gname = ""
            with p.open("rb") as stream:
                tf.addfile(info,stream)
            paths.append((name,hashlib.sha256(p.read_bytes()).hexdigest()))
    with tarfile.open(archive, "r:gz") as tf:
        verified = [(member.name, hashlib.sha256(tf.extractfile(member).read()).hexdigest()) for member in tf]
    if verified != paths:
        raise ValueError("Raw archive checksum mismatch")
    (out/"raw-manifest.sha256").write_text("".join(f"{digest}  {name}\n" for name,digest in paths))
    (out/"raw-evidence.sha256").write_text(f"{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n")
    summarize(list(all_rows()), counts, out)


if __name__=="__main__":
    par=argparse.ArgumentParser()
    par.add_argument("output_dir",type=Path)
    export(par.parse_args().output_dir)
