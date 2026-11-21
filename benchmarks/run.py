#!/usr/bin/env python3
"""Serial one-process-per-case execution and aggregation."""
import argparse
import csv
import fcntl
import hashlib
import os
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shlex
import statistics
import subprocess
import time

from cases import grid

ROOT = Path(__file__).resolve().parent
COLUMNS = """table_id,zoo_id,code_family,variant,repo,field,field_bits,k,input_elements,input_bytes,nominal_rate,actual_rate,codeword_elements,threads,setup_ms,encode_mean_ms,encode_median_ms,throughput_melem_s,throughput_gib_s,peak_rss_gib,status,notes""".split(",")
APEAK = 420 << 30


def available():
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) * 1024
    raise RuntimeError("MemAvailable missing")


def meminfo():
    return {"available_bytes": available(), "loadavg": Path("/proc/loadavg").read_text().strip()}


def now():
    return datetime.now(timezone.utc).isoformat()


def run_one(case):
    out = ROOT / "raw" / case["id"]
    if (out / "exit.json").is_file():
        raise RuntimeError(f"Attempt already recorded: {out}")
    out.mkdir(parents=True, exist_ok=False)
    memory = available()
    cap = min(APEAK, memory - (32 << 30))
    if cap <= 0:
        raise RuntimeError(f"Host MemAvailable too low to run safely: {memory}")
    binary = ROOT / "bin" / case["executable"]
    case = dict(case, binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(), as_limit_bytes=cap)
    cmd = [
        "taskset","-c","0-31","env","LC_ALL=C","RAYON_NUM_THREADS=32","OMP_NUM_THREADS=32",
        "MALLOC_MMAP_MAX_=0","MALLOC_TRIM_THRESHOLD_=-1","MALLOC_ARENA_MAX=1",
        "/usr/bin/time","-v","-o",str(out / "resources.txt"),
        "prlimit",f"--as={cap}","--",
        str(binary), *case["command"],
    ]
    (out / "command.txt").write_text(shlex.join(cmd) + "\n")
    (out / "case.json").write_text(json.dumps(case, indent=2)+"\n")
    before = {"start":now(), **meminfo()}
    t0 = time.monotonic()
    with (out / "stdout.log").open("w") as stdout, (out / "stderr.log").open("w") as stderr:
        rc = subprocess.run(cmd, stdout=stdout, stderr=stderr, cwd=ROOT).returncode
    info = {"returncode":rc,"wall_seconds":time.monotonic()-t0,"finish":now(),
            "before":before,"after":meminfo()}
    temp = out / "exit.json.tmp"
    temp.write_text(json.dumps(info, indent=2)+"\n")
    os.replace(temp, out / "exit.json")
    print(case["id"],rc,f"{info['wall_seconds']:.2f}s",flush=True)


def aggregate():
    rows = {}
    for case in grid():
        row = {col:case.get(col, "") for col in COLUMNS}
        k = case["k"]
        row.update(input_elements=1<<k, nominal_rate=f"1/{case['rate']}" if isinstance(case["rate"],int) else case["rate"])
        out = ROOT / "raw" / case["id"]
        if (out / "exit.json").is_file():
            info = json.loads((out / "exit.json").read_text())
            lines = (out / "stdout.log").read_text().splitlines()
            results = [line.split()[1:] for line in lines if line.startswith("ITER ")]
            geo = [line.split()[1:] for line in lines if line.startswith("GEOMETRY ")]
            setups = [line.split()[1] for line in lines if line.startswith("SETUP ")]
            raw_res = (out / "resources.txt").read_text()
            rss = re.search(r"Maximum resident set size \(kbytes\):\s+([0-9]+)",raw_res)
            if rss:
                row["peak_rss_gib"] = f"{int(rss[1])/1048576:.9f}"
            if info["returncode"]==0 and len(results)==4 and len(geo)==len(setups)==1:
                n_in, n_out, input_bytes = map(int, geo[0])
                assert n_in == row["input_elements"]
                assert [int(r[0]) for r in results] == list(range(4))
                assert all(int(r[2])==n_out for r in results)
                measured = [float(r[1]) for r in results[1:]]
                mean = statistics.mean(measured)
                worst_faults = max(int(r[3]) for r in results[1:])
                major_faults = sum(int(r[4]) for r in results[1:])
                params = " ".join(line[6:] for line in lines if line.startswith("PARAM "))
                row.update(input_bytes=input_bytes,actual_rate=f"{n_in/n_out:.12f}",
                           codeword_elements=n_out,setup_ms=setups[0],
                           encode_mean_ms=f"{mean:.9f}",encode_median_ms=f"{statistics.median(measured):.9f}",
                           throughput_melem_s=f"{n_in/1000/mean:.9f}",
                           throughput_gib_s=f"{input_bytes/2**30*1000/mean:.9f}",status="OK")
                row["notes"] += f" peak minor faults/sample={worst_faults}; timed major faults={major_faults}. {params}"
            else:
                stderr = (out / "stderr.log").read_text()
                if "domain limit from spin::valid_message_size" in stderr:
                    row["status"] = "DOMAIN_LIMIT"
                elif any(key in stderr for key in ("allocation of ", "std::bad_alloc", "out of memory", "Cannot allocate memory")):
                    measured_cap = json.loads((out / "case.json").read_text()).get("as_limit_bytes", APEAK)
                    row["status"] = "OOM_LIMIT" if measured_cap==APEAK else "HOST_MEMORY_LIMIT"
                else:
                    row["status"] = "FAILED"
                row["notes"] += f" exit={info['returncode']}; see raw/{case['id']}."
        elif not row["status"]:
            row["status"] = "PENDING"
        rows.setdefault(row["table_id"], []).append(row)
    for table, items in rows.items():
        target = ROOT/"results"/f"{table}.csv"
        temp = target.with_name(f".{target.name}.{os.getpid()}")
        with temp.open("w",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(items)
        os.replace(temp, target)



def run_grid(opts):
    finished = 0
    for case in grid():
        if case["status"] or case["executable"] in opts.skip_executable or (opts.executable and case["executable"] not in opts.executable):
            continue
        if opts.k and case["k"] not in opts.k:
            continue
        if opts.id_prefix and not case["id"].startswith(opts.id_prefix):
            continue
        if (ROOT/"raw"/case["id"]/"exit.json").is_file():
            continue
        if opts.dry_run:
            print(case["id"])
            continue
        if not (ROOT/"bin"/case["executable"]).is_file():
            raise RuntimeError(f"Missing binary {case['executable']}")
        out = ROOT / "raw" / case["id"]
        if out.exists():
            archive = ROOT / "raw" / "incomplete-attempts" / now().replace(':', '-')
            archive.mkdir(parents=True, exist_ok=True)
            out.rename(archive / out.name)
        run_one(case)
        finished += 1
        if (ROOT/"raw"/".yield-after-case").is_file():
            print("Requested checkpoint reached. All files for the last case are closed.", flush=True)
            break
        if finished % 16 == 0:
            aggregate()
    if not opts.dry_run:
        aggregate()

def main():
    args = argparse.ArgumentParser()
    args.add_argument("--executable",action="append")
    args.add_argument("--k",type=int,action="append")
    args.add_argument("--id-prefix")
    args.add_argument("--aggregate-only",action="store_true")
    args.add_argument("--skip-executable",action="append",default=[])
    args.add_argument("--dry-run",action="store_true")
    opts=args.parse_args()
    if opts.aggregate_only:
        aggregate()
    elif opts.dry_run:
        run_grid(opts)
    else:
        with (ROOT / "raw" / ".campaign-lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            run_grid(opts)


if __name__=="__main__":
    main()
