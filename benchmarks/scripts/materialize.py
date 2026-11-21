#!/usr/bin/env python3
"""Restore benchmark source directories from pinned upstream checkouts."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parents[1]


def copy_snapshot(src, dst, names):
    for name in names:
        p = src / name
        q = dst / name
        if p.is_dir():
            shutil.copytree(p, q)
        else:
            shutil.copy2(p, q)


def git_snapshot(repo, revision, dst, prefix):
    subprocess.run(["git", "-C", str(repo), "cat-file", "-e", f"{revision}^{{commit}}"], check=True)
    with tempfile.TemporaryFile() as archive:
        subprocess.run(["git", "-C", str(repo), "archive", revision, *prefix], stdout=archive, check=True)
        archive.seek(0)
        subprocess.run(["tar", "-xf", "-", "-C", str(dst)], stdin=archive, check=True)


def main():
    sources = json.loads((HERE / "sources.json").read_text())
    parser = argparse.ArgumentParser(description=__doc__)
    for name in sources["repos"]:
        parser.add_argument("--" + name, type=Path, required=True)
    args = vars(parser.parse_args())
    target = HERE / "source"
    target.mkdir(exist_ok=True)
    for name, spec in sources["repos"].items():
        src = args[name.replace("-", "_")]
        dst = target / name
        dst.mkdir()
        if "commit" in spec:
            git_snapshot(src, spec["commit"], dst, spec.get("paths", []))
        else:
            copy_snapshot(src, dst, spec["copy"])
            for check in spec["files"]:
                digest = hashlib.sha256((dst / check["path"]).read_bytes()).hexdigest()
                if digest != check["sha256"]:
                    raise ValueError(f"Source SHA-256 changed for {name}/{check['path']}")
        patch = HERE / "patches" / f"{name}.patch"
        if patch.exists():
            subprocess.run(["patch", "--batch", "-p1", "-d", str(dst), "-i", str(patch)], check=True)
    for restore in sources["source_locks"]:
        shutil.copyfile(HERE/"locks"/restore["filename"], target/restore["destination"])
    for folder in ("bin", "raw", "results", "build"):
        (HERE/folder).mkdir(exist_ok=True)


if __name__ == "__main__":
    main()
