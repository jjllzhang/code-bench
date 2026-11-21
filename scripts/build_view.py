#!/usr/bin/env python3
"""Build pcs-bench style per-family Markdown+CSV files, README.md, and a
Code-based PCS Zoo style interactive HTML/SVG dashboard from canonical
code-encoding-bench track CSVs.

Stdlib-only; safe to re-run whenever ProverDev appends or finalizes CSV rows.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
from fractions import Fraction
import json
from pathlib import Path
import re

DEFAULT_OUT = Path(__file__).resolve().parent.parent
DEFAULT_SRC = DEFAULT_OUT / "results" / "tracks"

COLUMNS = [
    "table_id", "zoo_id", "code_family", "variant", "repo", "field", "field_bits",
    "k", "input_elements", "input_bytes", "nominal_rate", "actual_rate",
    "codeword_elements", "threads", "setup_ms", "encode_mean_ms", "encode_median_ms",
    "throughput_melem_s", "throughput_gib_s", "peak_rss_gib", "status", "notes",
]

TRACK_META = {
    "prime_goldilocks_1d": {
        "title": "Track A · Goldilocks (64-bit) 1D",
        "short": "Goldilocks 1D",
        "badge": "prime",
        "desc": "Same-field 1D single-polynomial comparison over 64-bit Goldilocks (RS, BaseFold, HyperFold r∈{2,4,8}, Systematic QA/WHT, EA, RAA, Brakedown, ERA).",
    },
    "binary_1d": {
        "title": "Track B · Binary Fields 1D",
        "short": "Binary 1D",
        "badge": "bin",
        "desc": "Characteristic-2 1D single-polynomial encoding across GF(2^16/32/64/128), mixed subfield-to-extension QA, and 128-bit binary records.",
    },
    "native_fields_1d": {
        "title": "Track C · Native Fields & Hardware Artifacts 1D",
        "short": "Native Fields 1D",
        "badge": "gen",
        "desc": "Paper-native finite fields (BabyBear, M127, Ft127, Ristretto255, secp256k1, BN254, M61/Monty64).",
    },
}

COMPLEXITY_ORDER = {
    "1": ("Quasi-linear: O(K log K) · RS & NTT", 0),
    "3": ("Quasi-linear: O(K log K) · Binary Additive RS", 1),
    "5": ("Quasi-linear: O(K log K) · Random Foldable", 2),
    "5+": ("Quasi-linear: O(K log K) · High-Arity HyperFold", 3),
    "6": ("Quasi-linear: O(K log K) · Systematic QA / Spectral", 4),
    "7": ("Quasi-linear / Linear: EA & RAA", 5),
    "9": ("Sketched + Inner RS (Bolt)", 6),
    "13": ("Sketched + Inner Brakedown (Lightning)", 7),
    "11": ("Linear: O(K) · Accumulate (RAA)", 8),
    "12": ("Linear: O(K) · Expander (Brakedown / Spielman)", 9),
    "19": ("Linear: O(K) · Binary Structured (SPIN)", 10),
    "20": ("Linear: O(K) · ERA", 11),
}

FAMILY_TITLES = {
    "rs": "Reed–Solomon (Multiplicative NTT Coset LDE)",
    "additive-rs": "Binary Additive Reed–Solomon (LCH14 / PolyBasis / Bolt-RS)",
    "basefold": "BaseFold Random Foldable Codes (r = 2)",
    "hyperfold": "HyperFold High-Arity Hyper-Invertible Foldable Codes (r ∈ {2,4,8})",
    "binary-hyperfold": "Binary HyperFold High-Arity Foldable Codes (r ∈ {2,4,8})",
    "qa": "Systematic Quasi-Abelian Codes (WHT / Binary Spectral)",
    "ea": "Juxtaposed Expand–Accumulate (1D Explicit EA)",
    "raa": "Repeat–Accumulate–Accumulate (1D RAA)",
    "bolt": "Bolt Sketched Codes (bolt-xor / bolt32)",
    "brakedown": "Brakedown / Generalized Spielman Expander Codes",
    "spielman": "SIMD-Spielman (Mersenne61 / Monty64)",
    "lightning": "Lightning (LDPC Sketch + Brakedown Inner Code)",
    "spin": "SPIN Binary Structured Linear Codes (IMT / Packet-RS8)",
    "era": "ERA (Encode–Repeat–Accumulate)",
}

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>code-bench · 1D Linear Code Encoding Benchmarks</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Newsreader:opsz,wght@6..72,600&display=swap">
<style>
:root{
  --bg:#f6f7f9; --surface:#ffffff; --band:#f0f2f6; --fg:#18202c; --muted:#5f6b7d; --line:#dfe4ec; --line-soft:#edf0f5;
  --accent:#255499; --accent-soft:#e8f0fc;
  --prime-bg:#e5eefb; --prime-fg:#1d4a8a; --prime-bd:#c6daf7;
  --bin-bg:#e2f4ee; --bin-fg:#126149; --bin-bd:#bce5d7;
  --gen-bg:#f3eefb; --gen-fg:#56348c; --gen-bd:#dfd2f5;
  --ok-bg:#e3f5ec; --ok-fg:#13633c;
  --mid-bg:#fef3dc; --mid-fg:#8a5308;
  --warn-bg:#fdebe8; --warn-fg:#9c2c1c;
  --dim-bg:#eef0f4; --dim-fg:#596475;
  --code-bg:#f2f4f8;
  --bar-bg:#dde7f6;
  --shadow:0 1px 2px rgba(15,23,42,.04), 0 4px 12px rgba(15,23,42,.03);
  --f-display:"Newsreader", Georgia, serif;
  --f-body:"IBM Plex Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --f-mono:"IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#0f131a; --surface:#161b24; --band:#1b222e; --fg:#e5eaf2; --muted:#95a2b6; --line:#273040; --line-soft:#1e2633;
  --accent:#82aef0; --accent-soft:#1c2a42;
  --prime-bg:#192842; --prime-fg:#9cc0f7; --prime-bd:#2a4068;
  --bin-bg:#143229; --bin-fg:#7adcb9; --bin-bd:#1f4d3f;
  --gen-bg:#281e3b; --gen-fg:#c7aef5; --gen-bd:#3f2f5c;
  --ok-bg:#143325; --ok-fg:#77dfb0;
  --mid-bg:#362812; --mid-fg:#f0c26e;
  --warn-bg:#3b1b18; --warn-fg:#f49b8f;
  --dim-bg:#212834; --dim-fg:#9aa6b8;
  --code-bg:#1e2532;
  --bar-bg:#22344f;
  --shadow:0 1px 2px rgba(0,0,0,.35);
  color-scheme:dark;
}}
:root[data-theme="dark"]{
  --bg:#0f131a; --surface:#161b24; --band:#1b222e; --fg:#e5eaf2; --muted:#95a2b6; --line:#273040; --line-soft:#1e2633;
  --accent:#82aef0; --accent-soft:#1c2a42;
  --prime-bg:#192842; --prime-fg:#9cc0f7; --prime-bd:#2a4068;
  --bin-bg:#143229; --bin-fg:#7adcb9; --bin-bd:#1f4d3f;
  --gen-bg:#281e3b; --gen-fg:#c7aef5; --gen-bd:#3f2f5c;
  --ok-bg:#143325; --ok-fg:#77dfb0;
  --mid-bg:#362812; --mid-fg:#f0c26e;
  --warn-bg:#3b1b18; --warn-fg:#f49b8f;
  --dim-bg:#212834; --dim-fg:#9aa6b8;
  --code-bg:#1e2532;
  --bar-bg:#22344f;
  --shadow:0 1px 2px rgba(0,0,0,.35);
  color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--f-body);font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}
.wrap{max-width:1300px;margin:0 auto;padding:32px max(18px,env(safe-area-inset-left,0px)) 64px;display:grid;gap:22px}
.wrap>*{min-width:0}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}

.hero{display:grid;gap:11px;border-bottom:1px solid var(--line);padding-bottom:18px}
.hero-top{display:flex;flex-wrap:wrap;align-items:flex-start;justify-content:space-between;gap:12px}
.kicker{font-family:var(--f-mono);font-size:.73rem;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:500}
h1{font-family:var(--f-display);font-weight:600;font-size:2.05rem;line-height:1.14;margin:4px 0 0;letter-spacing:-.01em}
.lead{margin:0;color:var(--muted);font-size:.89rem;max-width:96ch}
.hero-actions{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.snap-pill{font-family:var(--f-mono);font-size:.73rem;padding:5px 10px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--muted)}
.theme-btn{background:var(--surface);border:1px solid var(--line);color:var(--fg);font-family:var(--f-body);font-size:.78rem;padding:5px 12px;border-radius:999px;cursor:pointer}
.theme-btn:hover{border-color:var(--accent)}
.key{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:.78rem;color:var(--muted);align-items:center}
.key b{color:var(--fg);font-family:var(--f-mono);font-size:.75rem}

.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
@media (max-width:860px){.stats{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:480px){.stats{grid-template-columns:1fr}}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 15px;box-shadow:var(--shadow);display:grid;gap:3px}
.stat-label{font-size:.74rem;color:var(--muted);display:flex;align-items:center;justify-content:space-between}
.stat-num{font-family:var(--f-mono);font-size:1.32rem;font-weight:500;line-height:1.2}
.stat-sub{font-size:.73rem;color:var(--muted)}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.dot.prime{background:var(--prime-fg)} .dot.bin{background:var(--bin-fg)} .dot.gen{background:var(--gen-fg)} .dot.ok{background:var(--ok-fg)}

.toolbar{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:11px 14px;display:grid;gap:9px;position:sticky;top:10px;z-index:20;box-shadow:var(--shadow)}
.tool-row{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;justify-content:space-between}
.pills{display:flex;flex-wrap:wrap;gap:5px;align-items:center}
.pill-label{font-size:.72rem;color:var(--muted);margin-right:2px;font-weight:500}
.fbtn{border:1px solid var(--line);background:var(--bg);color:var(--fg);font-family:var(--f-body);font-size:.76rem;font-weight:500;padding:4px 10px;border-radius:999px;cursor:pointer;transition:all .12s}
.fbtn:hover{border-color:var(--accent)}
.fbtn.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.fbtn.active.f-prime{background:var(--prime-fg);border-color:var(--prime-fg)}
.fbtn.active.f-bin{background:var(--bin-fg);border-color:var(--bin-fg)}
.fbtn.active.f-gen{background:var(--gen-fg);border-color:var(--gen-fg)}
.search-box{display:flex;align-items:center;gap:8px;flex:1 1 220px;max-width:300px}
.search-box input{width:100%;padding:5px 10px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg);font-family:var(--f-body);font-size:.79rem;outline:none}
.search-box input:focus{border-color:var(--accent)}
.match-count{font-family:var(--f-mono);font-size:.73rem;color:var(--muted);white-space:nowrap}
.fair-note{font-size:.76rem;color:var(--muted);background:var(--band);border-radius:7px;padding:6px 10px;display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between}

.panel{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px 18px;box-shadow:var(--shadow);display:grid;gap:11px}
.panel-head{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px}
.panel-title{font-family:var(--f-display);font-weight:600;font-size:1.22rem;margin:0}
.chart-controls{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center}
.chart-wrap{position:relative;overflow-x:auto}
svg.chart{width:100%;min-width:660px;display:block;font-family:var(--f-mono)}
.legend{display:flex;flex-wrap:wrap;gap:5px 10px;font-size:.74rem}
.leg-item{display:inline-flex;align-items:center;gap:6px;padding:2px 8px;border:1px solid var(--line);border-radius:999px;cursor:pointer;background:var(--bg);color:var(--fg);user-select:none}
.leg-item.off{opacity:.38}
.leg-swatch{width:10px;height:3px;border-radius:2px;display:inline-block}
.tooltip{position:fixed;pointer-events:none;background:var(--surface);color:var(--fg);border:1px solid var(--line);border-radius:8px;padding:8px 10px;font-size:.75rem;box-shadow:0 8px 24px rgba(0,0,0,.18);z-index:50;display:none;max-width:340px;font-family:var(--f-mono);line-height:1.45}

.sec{display:grid;gap:9px}
.sec-head{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:8px}
.sec-title{display:flex;align-items:center;gap:10px}
.sec-title h2{font-family:var(--f-display);font-weight:600;font-size:1.28rem;margin:0}
.sec-badge{font-size:.71rem;font-weight:600;padding:2px 9px;border-radius:999px;border:1px solid transparent}
.sec-badge.prime{background:var(--prime-bg);color:var(--prime-fg);border-color:var(--prime-bd)}
.sec-badge.bin{background:var(--bin-bg);color:var(--bin-fg);border-color:var(--bin-bd)}
.sec-badge.gen{background:var(--gen-bg);color:var(--gen-fg);border-color:var(--gen-bd)}
.sec-desc{margin:0;font-size:.8rem;color:var(--muted)}

.tw{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--surface);box-shadow:var(--shadow)}
table{border-collapse:collapse;width:100%;min-width:980px}
thead th{background:var(--band);text-align:left;font-size:.68rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:600;padding:9px 11px;border-bottom:1px solid var(--line);white-space:nowrap}
thead th.num, tbody td.num{text-align:right;font-family:var(--f-mono);font-variant-numeric:tabular-nums}
tbody tr:hover{background:var(--line-soft)}
tbody td, tbody th{padding:8px 11px;border-top:1px solid var(--line-soft);vertical-align:top;text-align:left;font-weight:400}
tr.fam th{background:var(--band);font-size:.7rem;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);font-weight:600;padding:6px 11px}
.cname{font-weight:600;font-size:.87rem;color:var(--fg)}
.sub{display:block;font-size:.72rem;color:var(--muted);margin-top:2px}
.mono{font-family:var(--f-mono);font-size:.75rem}
.val-main{display:block;font-weight:500;font-size:.8rem}
.val-sub{display:block;font-size:.69rem;color:var(--muted)}
.tag{display:inline-block;font-size:.66rem;font-weight:600;padding:1px 6px;border-radius:4px;border:1px solid transparent;white-space:nowrap}
.tag.prime{background:var(--prime-bg);color:var(--prime-fg);border-color:var(--prime-bd)}
.tag.bin{background:var(--bin-bg);color:var(--bin-fg);border-color:var(--bin-bd)}
.tag.gen{background:var(--gen-bg);color:var(--gen-fg);border-color:var(--gen-bd)}
.tag.ok{background:var(--ok-bg);color:var(--ok-fg)}
.tag.mid{background:var(--mid-bg);color:var(--mid-fg)}
.tag.warn{background:var(--warn-bg);color:var(--warn-fg)}
.tag.dim{background:var(--dim-bg);color:var(--dim-fg)}
.tag.repo{background:var(--code-bg);color:var(--fg);border-color:var(--line);font-family:var(--f-mono);font-weight:400}
.tag.repo a{color:inherit}
.bar-cell{min-width:120px}
.bar-track{height:6px;background:var(--line-soft);border-radius:3px;overflow:hidden;margin-top:4px}
.bar-fill{height:100%;background:var(--accent);border-radius:3px}

footer{border-top:1px solid var(--line);padding-top:14px;font-size:.79rem;color:var(--muted);display:grid;gap:5px;max-width:108ch}
footer p{margin:0}
</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <div class="hero-top">
      <div>
        <div class="kicker">code-bench · Single-Polynomial 1D Linear Code Encoder Archive</div>
        <h1>1D Linear Code Encoding Benchmarks</h1>
      </div>
      <div class="hero-actions">
        <span class="snap-pill" id="snapshotPill">Snapshot</span>
        <button class="theme-btn" id="themeToggle" type="button">◐ Theme</button>
      </div>
    </div>
    <p class="lead">
      Single-polynomial 1D encoding throughput and latency for messages of length <code>K = 2^k</code> (<code>k ∈ {20, 22, 24, 26, 28, 30}</code>), excluding interleaved and 2D matrix-reshaped codes. Pinned 32 cores (AMD EPYC 9754, 503 GiB RAM), 1 warmup + 3 serial measured runs. Excludes setup (<code>setup_ms</code>), input generation, caller-buffer reset, correctness checks, and Merkle hashing. Drivers pre-touch or reuse caller-owned buffers before timing, while encoder-allocated output and scratch space inside the timed call may still incur page faults whose time is included (logged per row in Notes).
    </p>
    <div class="key">
      <span><b>K = 2^k</b> message elements (<code>k ∈ {20, 22, 24, 26, 28, 30}</code>)</span>
      <span><b>ρ</b> nominal vs. actual codeword ratio</span>
      <span><b>GiB/s</b> input_bytes / 2^30 / mean_s</span>
      <span><b>MElem/s</b> K / 10^6 / mean_s</span>
      <span><span class="tag ok">OK</span> length &amp; non-zero verified</span>
      <span><span class="tag mid">DOMAIN_LIMIT</span> field / impl bound</span>
      <span><span class="tag warn">OOM_SKIPPED</span> / <span class="tag warn">OOM_LIMIT</span> &gt;420 GiB or host cap</span>
      <span><span class="tag warn">EXCLUDED_INTERLEAVED</span> multi-codeword batch</span>
      <span><span class="tag mid">UNSUPPORTED_BACKEND</span> backend lacks 1D config</span>
      <span><span class="tag dim">PENDING</span> queued / not yet run</span>
    </div>
  </header>

  <section class="stats" id="statsStrip"></section>

  <div class="toolbar" role="region" aria-label="Filters">
    <div class="tool-row">
      <div class="pills" id="trackPills">
        <span class="pill-label">Track</span>
        <button class="fbtn active f-prime" data-track="prime_goldilocks_1d" type="button">Goldilocks 1D</button>
        <button class="fbtn f-bin" data-track="binary_1d" type="button">Binary 1D</button>
        <button class="fbtn f-gen" data-track="native_fields_1d" type="button">Native Fields 1D</button>
        <button class="fbtn" data-track="all" type="button">All Tracks</button>
      </div>
      <div class="pills" id="ratePills">
        <span class="pill-label">Config Rate</span>
        <button class="fbtn active" data-rate="all" type="button">All</button>
        <button class="fbtn" data-rate="1/2" type="button">1/2</button>
        <button class="fbtn" data-rate="1/4" type="button">1/4</button>
        <button class="fbtn" data-rate="native" type="button">Native</button>
      </div>
      <div class="pills" id="actualRatePills"></div>
      <div class="pills" id="statusPills">
        <span class="pill-label">Status</span>
        <button class="fbtn active" data-status="all" type="button">All</button>
        <button class="fbtn" data-status="ok" type="button">OK Only</button>
        <button class="fbtn" data-status="pending" type="button">Pending</button>
        <button class="fbtn" data-status="bounds" type="button">Limits / OOM</button>
        <button class="fbtn" data-status="excluded" type="button">Excluded / Unsupported</button>
      </div>
    </div>
    <div class="tool-row">
      <div class="pills" id="fieldPills"></div>
      <div class="pills" id="viewPills">
        <span class="pill-label">View</span>
        <button class="fbtn active" data-view="matrix" type="button">Scaling Matrix</button>
        <button class="fbtn" data-view="compare" type="button">Same-Field Rank @ k</button>
        <button class="fbtn" data-view="runs" type="button">Detailed Runs</button>
      </div>
      <div class="search-box">
        <input id="searchInput" type="search" placeholder="Filter code, field, variant, repo…">
        <span class="match-count" id="matchCount"></span>
      </div>
    </div>
    <div class="fair-note" id="fairNote"></div>
  </div>

  <section class="panel" aria-label="Comparison Chart">
    <div class="panel-head">
      <h2 class="panel-title" id="chartTitle">Comparison</h2>
      <div class="chart-controls">
        <div class="pills" id="kPills"></div>
        <div class="pills" id="chartModePills">
          <span class="pill-label">Chart</span>
          <button class="fbtn active" data-chartmode="auto" type="button">Auto</button>
          <button class="fbtn" data-chartmode="bar" type="button">Bar @ k</button>
          <button class="fbtn" data-chartmode="line" type="button">Scaling Curve</button>
        </div>
        <div class="pills" id="metricPills">
          <span class="pill-label">Metric</span>
          <button class="fbtn active" data-metric="throughput_gib_s" type="button">GiB/s</button>
          <button class="fbtn" data-metric="throughput_melem_s" type="button">MElem/s</button>
          <button class="fbtn" data-metric="encode_mean_ms" type="button">Time (ms)</button>
        </div>
      </div>
    </div>
    <div class="legend" id="chartLegend"></div>
    <div class="chart-wrap">
      <svg class="chart" id="chartSvg" viewBox="0 0 980 340" preserveAspectRatio="xMidYMid meet"></svg>
    </div>
  </section>

  <div id="tablesRoot"></div>

  <footer>
    <p>Generated directly from canonical <code>results/*.csv</code> outputs. Every row enforces 1D single-codeword encoding (<code>nrows = 1</code>, <code>width = 1</code>, <code>log_batch_size = 0</code>).</p>
    <p>Timing &amp; memory boundary: drivers pre-touch or reset caller-owned buffers before timing; allocation-returning encoders include their own output and temporary scratch allocations—plus any minor or major page faults incurred within the timed interval (logged per row in Notes)—in <code>encode_mean_ms</code> / <code>encode_median_ms</code>. <code>setup_ms</code> covers tables/graphs; <code>peak_rss_gib</code> is whole-process peak RSS.</p>
    <p>Notes on comparability: compare <code>MElem/s</code> and <code>GiB/s</code> directly only within the same <code>(field, reduced K/N)</code> slice (4-decimal values are for display only). ERA (<code>r∈{2,4}</code> includes 1.05× inner Brakedown) and Bolt (<code>bolt-xor</code>/<code>bolt32</code> include systematic input + inner RS) report both nominal and exact <code>K/N</code>. <code>bolt-rs</code> stock RS kernel runs with <code>threads=1</code> under the 32-core affinity. Hyphenated fields (e.g., <code>bf32-bf128</code>) indicate subfield inputs encoded into extension codewords.</p>
  </footer>
</div>
<div class="tooltip" id="tooltip"></div>

<script>
const DATA = __DATA_JSON__;
const TRACKS = __TRACKS_JSON__;
const GENERATED_AT = __GENERATED_JSON__;
const SIZES = [20, 22, 24, 26, 28, 30];
const PALETTE = [
  "#255499","#126149","#9c2c1c","#7a44a8","#b45309","#0e7490",
  "#be185d","#4338ca","#3f6212","#6d28d9","#0369a1","#b91c1c"
];

const state = {
  track: "prime_goldilocks_1d",
  field: "all",
  rate: "all",
  actualRate: "all",
  status: "all",
  view: "matrix",
  chartmode: "auto",
  metric: "throughput_gib_s",
  kFocus: 20,
  query: "",
  hiddenSeries: new Set(),
};

const rootEl = document.documentElement;
document.getElementById("themeToggle").addEventListener("click", () => {
  const dark = rootEl.getAttribute("data-theme") === "dark" ||
    (!rootEl.hasAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
  rootEl.setAttribute("data-theme", dark ? "light" : "dark");
});

function bindPills(id, key, onChange) {
  const box = document.getElementById(id);
  box.addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-" + key + "]");
    if (!btn) return;
    box.querySelectorAll(".fbtn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    state[key] = btn.dataset[key];
    onChange();
  });
}
bindPills("trackPills", "track", () => {
  state.field = "all";
  state.actualRate = "all";
  state.hiddenSeries.clear();
  syncDynamicPills();
  render();
});
bindPills("ratePills", "rate", () => { state.hiddenSeries.clear(); render(); });
bindPills("statusPills", "status", render);
bindPills("viewPills", "view", render);
bindPills("chartModePills", "chartmode", renderChart);
bindPills("metricPills", "metric", render);
document.getElementById("searchInput").addEventListener("input", (e) => {
  state.query = e.target.value.trim().toLowerCase();
  render();
});

function rateBucket(r) {
  if (r === "1/2" || r === "half") return "1/2";
  if (r === "1/4") return "1/4";
  return "native";
}

function gcdInt(a, b) {
  let x = Math.abs(a), y = Math.abs(b);
  while (y) { const t = x % y; x = y; y = t; }
  return x || 1;
}

function actualRateKey(r) {
  const kIn = Number(r.input_elements);
  const nOut = Number(r.codeword_elements);
  if (Number.isInteger(kIn) && Number.isInteger(nOut) && kIn > 0 && nOut > 0) {
    const g = gcdInt(kIn, nOut);
    return `${kIn / g}/${nOut / g}`;
  }
  return r.actual_rate ? String(r.actual_rate).trim() : "";
}

function actualRateNumeric(r) {
  const kIn = Number(r.input_elements);
  const nOut = Number(r.codeword_elements);
  if (Number.isInteger(kIn) && Number.isInteger(nOut) && kIn > 0 && nOut > 0) {
    return kIn / nOut;
  }
  const v = Number(r.actual_rate);
  return Number.isFinite(v) ? v : NaN;
}

function actualRateDisplay(r) {
  const key = actualRateKey(r);
  if (!key) return "";
  const v = actualRateNumeric(r);
  return Number.isFinite(v) ? `${key} (${v.toFixed(4)})` : key;
}

function statusMatch(st) {
  if (state.status === "all") return true;
  if (state.status === "ok") return st === "OK";
  if (state.status === "pending") return st === "PENDING";
  if (state.status === "bounds") return st === "DOMAIN_LIMIT" || st === "OOM_SKIPPED" || st === "OOM_LIMIT" || st === "HOST_MEMORY_LIMIT" || st === "FAILED";
  return st === "EXCLUDED_INTERLEAVED" || st === "UNSUPPORTED_BACKEND" || st === "EXCLUDED";
}

function syncDynamicPills() {
  const trackRows = state.track === "all" ? DATA : DATA.filter(r => r.table_id === state.track);
  const fields = Array.from(new Set(trackRows.map(r => r.field)));
  if (state.field !== "all" && !fields.includes(state.field)) state.field = "all";
  const fp = document.getElementById("fieldPills");
  fp.innerHTML = `<span class="pill-label">Field</span>` +
    [`<button class="fbtn ${state.field === "all" ? "active" : ""}" data-field="all" type="button">All Fields (${fields.length})</button>`]
    .concat(fields.map(f => `<button class="fbtn ${state.field === f ? "active" : ""}" data-field="${htmlEscape(f)}" type="button">${htmlEscape(f)}</button>`))
    .join("");
  fp.onclick = (e) => {
    const btn = e.target.closest("button[data-field]");
    if (!btn) return;
    state.field = btn.dataset.field;
    state.actualRate = "all";
    state.hiddenSeries.clear();
    syncDynamicPills();
    render();
  };

  const fieldRows = state.field === "all" ? trackRows : trackRows.filter(r => r.field === state.field);
  const rateMeta = new Map();
  for (const r of fieldRows) {
    const rk = actualRateKey(r);
    if (!rk || rateMeta.has(rk)) continue;
    rateMeta.set(rk, { key: rk, num: actualRateNumeric(r), label: actualRateDisplay(r) });
  }
  const actRates = Array.from(rateMeta.values()).sort((a, b) =>
    (Number.isFinite(a.num) && Number.isFinite(b.num) ? a.num - b.num : 0) || a.key.localeCompare(b.key)
  );
  if (state.actualRate !== "all" && !rateMeta.has(state.actualRate)) state.actualRate = "all";
  const arp = document.getElementById("actualRatePills");
  arp.innerHTML = `<span class="pill-label">Actual K/N</span>` +
    [`<button class="fbtn ${state.actualRate === "all" ? "active" : ""}" data-actualrate="all" type="button">All</button>`]
    .concat(actRates.map(a => `<button class="fbtn ${state.actualRate === a.key ? "active" : ""}" data-actualrate="${htmlEscape(a.key)}" type="button">${htmlEscape(a.label)}</button>`))
    .join("");
  arp.onclick = (e) => {
    const btn = e.target.closest("button[data-actualrate]");
    if (!btn) return;
    state.actualRate = btn.dataset.actualrate;
    state.hiddenSeries.clear();
    syncDynamicPills();
    render();
  };

  const okKs = Array.from(new Set(DATA.filter(r => r.status === "OK").map(r => Number(r.k)))).sort((a,b) => a-b);
  const availKs = okKs.length ? okKs : SIZES;
  if (!availKs.includes(state.kFocus)) state.kFocus = availKs[availKs.length - 1];
  const kp = document.getElementById("kPills");
  kp.innerHTML = `<span class="pill-label">Focus k</span>` +
    SIZES.map(k => `<button class="fbtn ${state.kFocus === k ? "active" : ""}" data-kfocus="${k}" type="button">k=${k}</button>`).join("");
  kp.onclick = (e) => {
    const btn = e.target.closest("button[data-kfocus]");
    if (!btn) return;
    state.kFocus = Number(btn.dataset.kfocus);
    syncDynamicPills();
    render();
  };
}

function filteredRows(ignoreStatus = false) {
  return DATA.filter(r => {
    if (state.track !== "all" && r.table_id !== state.track) return false;
    if (state.field !== "all" && r.field !== state.field) return false;
    if (state.rate !== "all" && rateBucket(r.nominal_rate) !== state.rate) return false;
    if (state.actualRate !== "all" && actualRateKey(r) !== state.actualRate) return false;
    if (!ignoreStatus && !statusMatch(r.status)) return false;
    if (state.query) {
      const hay = [r.zoo_id, r.code_family, r.variant, r.field, r.repo, r.status, r.nominal_rate, r.actual_rate, r.notes].join(" ").toLowerCase();
      if (!hay.includes(state.query)) return false;
    }
    return true;
  });
}

function fmtNum(v, digits = 3) {
  if (v === null || v === undefined || v === "") return "—";
  const n = Number(v);
  if (!Number.isFinite(n)) return "—";
  if (n >= 100) return n.toFixed(1);
  if (n >= 10) return n.toFixed(2);
  return n.toFixed(digits);
}

function statusChip(st, note = "") {
  const titleAttr = note ? ` title="${htmlEscape(note)}"` : "";
  if (st === "OK") return `<span class="tag ok"${titleAttr}>OK</span>`;
  if (st === "DOMAIN_LIMIT") return `<span class="tag mid"${titleAttr}>DOMAIN_LIMIT</span>`;
  if (st === "UNSUPPORTED_BACKEND") return `<span class="tag mid"${titleAttr}>UNSUPPORTED_BACKEND</span>`;
  if (st === "OOM_SKIPPED" || st === "OOM_LIMIT" || st === "HOST_MEMORY_LIMIT") return `<span class="tag warn"${titleAttr}>${htmlEscape(st)}</span>`;
  if (st === "EXCLUDED_INTERLEAVED") return `<span class="tag warn"${titleAttr}>EXCLUDED_INTERLEAVED</span>`;
  if (st === "EXCLUDED") return `<span class="tag warn"${titleAttr}>EXCLUDED</span>`;
  if (st === "FAILED") return `<span class="tag warn"${titleAttr}>FAILED</span>`;
  return `<span class="tag dim"${titleAttr}>${htmlEscape(st || "PENDING")}</span>`;
}

function repoChip(repo) {
  const s = String(repo || "");
  const m = s.match(/^([A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+)@([0-9a-f]{7,40})$/);
  if (m) {
    return `<span class="tag repo"><a href="https://github.com/${m[1]}/tree/${m[2]}" target="_blank" rel="noopener">${htmlEscape(m[1])}@${htmlEscape(m[2].slice(0,8))}</a></span>`;
  }
  return `<span class="tag repo">${htmlEscape(s)}</span>`;
}

function htmlEscape(s) {
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}

function renderStats() {
  const ok = DATA.filter(r => r.status === "OK");
  const pend = DATA.filter(r => r.status === "PENDING");
  const lim = DATA.filter(r => r.status === "DOMAIN_LIMIT" || r.status === "OOM_SKIPPED" || r.status === "OOM_LIMIT" || r.status === "HOST_MEMORY_LIMIT");
  const excl = DATA.filter(r => r.status === "EXCLUDED_INTERLEAVED" || r.status === "UNSUPPORTED_BACKEND" || r.status === "EXCLUDED");
  const primeOk = ok.filter(r => r.table_id === "prime_goldilocks_1d");
  const binOk = ok.filter(r => r.table_id === "binary_1d");
  const best = ok.reduce((a, b) => (+b.throughput_gib_s > +(a?.throughput_gib_s || -1) ? b : a), null);
  const seriesCount = new Set(DATA.map(r => `${r.table_id}|${r.code_family}|${r.variant}|${r.field}|${r.nominal_rate}`)).size;

  const exclPart = excl.length ? ` · ${excl.length} EXCL/UNSUP` : "";
  document.getElementById("snapshotPill").textContent =
    `${ok.length} OK · ${pend.length} PENDING · ${lim.length} LIMIT/OOM${exclPart} · ${GENERATED_AT}`;

  document.getElementById("statsStrip").innerHTML = `
    <div class="stat"><div class="stat-label"><span>Configured 1D Series</span><span class="dot gen"></span></div>
      <div class="stat-num">${seriesCount}</div><div class="stat-sub">${ok.length} OK / ${DATA.length} grid configs (${pend.length} pending${excl.length ? `, ${excl.length} excl/unsup` : ""})</div></div>
    <div class="stat"><div class="stat-label"><span>Goldilocks 1D</span><span class="dot prime"></span></div>
      <div class="stat-num">${primeOk.length}</div><div class="stat-sub">same-field 64-bit prime runs OK</div></div>
    <div class="stat"><div class="stat-label"><span>Binary 1D</span><span class="dot bin"></span></div>
      <div class="stat-num">${binOk.length}</div><div class="stat-sub">GF(2^16..128) &amp; 128b packed runs OK</div></div>
    <div class="stat"><div class="stat-label"><span>Peak Observed (Current)</span><span class="dot ok"></span></div>
      <div class="stat-num">${best ? fmtNum(best.throughput_gib_s, 2) + " GiB/s" : "Pending"}</div>
      <div class="stat-sub">${best ? `${best.code_family}/${best.variant} · ${best.field} · ρ_act=${fmtNum(best.actual_rate, 3)} · k=${best.k}` : "Awaiting OK measurements"}</div></div>
  `;

  const activeRows = filteredRows();
  const activeFields = new Set(activeRows.map(r => r.field));
  const activeActRates = new Set(activeRows.map(actualRateKey).filter(Boolean));
  const fair = document.getElementById("fairNote");
  const sameField = activeFields.size === 1;
  const sameActualRate = activeActRates.size === 1;
  if (sameField && sameActualRate) {
    const f = [...activeFields][0];
    const sample = activeRows.find(r => actualRateKey(r));
    const rt = sample ? actualRateDisplay(sample) : [...activeActRates][0];
    fair.innerHTML = `<span><strong>Fair comparison slice active:</strong> single field <code>${htmlEscape(f)}</code> at reduced rate <code>K/N = ${htmlEscape(rt)}</code>.</span><span>Both <code>GiB/s</code> and <code>MElem/s</code> are directly comparable.</span>`;
  } else {
    fair.innerHTML = `<span><strong>Multi-slice view (${activeFields.size} fields, ${activeActRates.size || 0} reduced K/N groups):</strong> rankings &amp; snapshots group strictly by reduced <b>K/N</b> (4 decimals for display only); filter a single <b>Field</b> and <b>Actual K/N</b> above for strict 1:1 comparison.</span><span>${activeRows.length} / ${DATA.length} configs shown</span>`;
  }
}

function seriesRateLabel(s) {
  if (!s.actualKeys || s.actualKeys.size === 0) return `cfg ${s.nominal_rate}`;
  if (s.actualKeys.size === 1) {
    const rk = [...s.actualKeys][0];
    const disp = [...s.actualDisplays][0];
    const nom = s.nominal_rate === "half" ? "1/2" : s.nominal_rate;
    if (rk === nom) return disp;
    return `${disp} [cfg ${s.nominal_rate}]`;
  }
  const nums = Object.values(s.byK).map(actualRateNumeric).filter(Number.isFinite);
  const lo = Math.min(...nums).toFixed(4), hi = Math.max(...nums).toFixed(4);
  return `${lo === hi ? lo : lo + "–" + hi} (by k) [cfg ${s.nominal_rate}]`;
}

function groupSeries(rows) {
  const map = new Map();
  for (const r of rows) {
    const key = `${r.table_id}|${r.zoo_id}|${r.code_family}|${r.variant}|${r.field}|${r.nominal_rate}`;
    if (!map.has(key)) {
      map.set(key, {
        key,
        table_id: r.table_id,
        zoo_id: r.zoo_id,
        code_family: r.code_family,
        variant: r.variant,
        field: r.field,
        field_bits: r.field_bits,
        nominal_rate: r.nominal_rate,
        actualKeys: new Set(),
        actualDisplays: new Set(),
        repo: r.repo,
        threads: r.threads,
        group: r.group_label,
        sortOrder: r.group_order,
        byK: {},
      });
    }
    const g = map.get(key);
    g.byK[Number(r.k)] = r;
    const rk = actualRateKey(r);
    if (rk) {
      g.actualKeys.add(rk);
      g.actualDisplays.add(actualRateDisplay(r));
    }
  }
  return Array.from(map.values()).sort((a, b) =>
    a.sortOrder - b.sortOrder || a.code_family.localeCompare(b.code_family) ||
    a.variant.localeCompare(b.variant) || a.field.localeCompare(b.field) || a.nominal_rate.localeCompare(b.nominal_rate)
  );
}

function renderChart() {
  const rows = filteredRows(true).filter(r => r.status === "OK" && r[state.metric] !== "" && Number(r[state.metric]) > 0);
  const series = groupSeries(rows);
  const svg = document.getElementById("chartSvg");
  const leg = document.getElementById("chartLegend");
  const tip = document.getElementById("tooltip");
  const metricLabel = state.metric === "throughput_gib_s" ? "Throughput (GiB/s)" :
                      state.metric === "throughput_melem_s" ? "Throughput (MElem/s)" : "Pure Encode Time (ms)";

  const distinctKs = Array.from(new Set(rows.map(r => Number(r.k)))).sort((a,b) => a-b);
  const mode = state.chartmode === "auto" ? (distinctKs.length <= 1 ? "bar" : "line") : state.chartmode;
  const kBar = distinctKs.includes(state.kFocus) ? state.kFocus : (distinctKs[distinctKs.length - 1] || state.kFocus);

  document.getElementById("chartTitle").textContent = mode === "bar"
    ? `${TRACKS[state.track]?.short || "All Tracks"} · ${metricLabel} at k=${kBar}`
    : `${TRACKS[state.track]?.short || "All Tracks"} · ${metricLabel} Scaling (k ∈ {20, 22, 24, 26, 28, 30})`;

  if (!series.length) {
    leg.innerHTML = `<span class="val-sub">No completed OK rows for current filter.</span>`;
    svg.setAttribute("viewBox", "0 0 980 200");
    svg.innerHTML = `<text x="490" y="105" text-anchor="middle" fill="var(--muted)" font-size="13">Awaiting OK benchmark measurements for this filter</text>`;
    return;
  }

  leg.innerHTML = series.map((s, idx) => {
    const color = PALETTE[idx % PALETTE.length];
    const off = state.hiddenSeries.has(s.key) ? "off" : "";
    const label = `${s.code_family}/${s.variant} · ${s.field} · ρ=${seriesRateLabel(s)}`;
    return `<button class="leg-item ${off}" data-key="${htmlEscape(s.key)}" type="button"><span class="leg-swatch" style="background:${color}"></span>${htmlEscape(label)}</button>`;
  }).join("");

  leg.onclick = (e) => {
    const btn = e.target.closest(".leg-item");
    if (!btn) return;
    const k = btn.dataset.key;
    if (state.hiddenSeries.has(k)) state.hiddenSeries.delete(k); else state.hiddenSeries.add(k);
    renderChart();
  };

  const active = series.map((s, idx) => ({ ...s, color: PALETTE[idx % PALETTE.length] })).filter(s => !state.hiddenSeries.has(s.key));

  if (mode === "bar") {
    const bars = active.map(s => ({ s, r: s.byK[kBar] })).filter(x => x.r && Number(x.r[state.metric]) > 0);
    const higherBetter = state.metric !== "encode_mean_ms";
    bars.sort((a, b) => higherBetter
      ? Number(b.r[state.metric]) - Number(a.r[state.metric])
      : Number(a.r[state.metric]) - Number(b.r[state.metric]));
    if (!bars.length) {
      svg.setAttribute("viewBox", "0 0 980 200");
      svg.innerHTML = `<text x="490" y="105" text-anchor="middle" fill="var(--muted)" font-size="13">No OK measurements at k=${kBar} for current filter</text>`;
      return;
    }
    const rowH = 26, top = 16, bot = 28, left = 370, right = 110, W = 980;
    const H = top + bot + bars.length * rowH;
    const pw = W - left - right;
    const maxV = Math.max(...bars.map(b => Number(b.r[state.metric])));
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    svg.style.height = Math.max(180, H) + "px";

    let out = "";
    for (const frac of [0, 0.25, 0.5, 0.75, 1]) {
      const x = left + frac * pw;
      const v = frac * maxV;
      out += `<line x1="${x}" y1="${top}" x2="${x}" y2="${H - bot}" stroke="var(--line-soft)" />`;
      out += `<text x="${x}" y="${H - 8}" text-anchor="middle" fill="var(--muted)" font-size="10">${fmtNum(v, 2)}</text>`;
    }
    bars.forEach((b, i) => {
      const y = top + i * rowH;
      const val = Number(b.r[state.metric]);
      const bw = Math.max(2, (val / Math.max(1e-9, maxV)) * pw);
      const label = `${b.s.code_family}/${b.s.variant} · ${b.s.field} · ρ=${seriesRateLabel(b.s)}`;
      const shortLabel = label.length > 55 ? label.slice(0, 54) + "…" : label;
      const unit = state.metric === "throughput_gib_s" ? "GiB/s" : state.metric === "throughput_melem_s" ? "MElem/s" : "ms";
      out += `<text x="${left - 10}" y="${y + 16}" text-anchor="end" fill="var(--fg)" font-size="10.8">${htmlEscape(shortLabel)}</text>`;
      out += `<rect x="${left}" y="${y + 5}" width="${bw}" height="15" rx="3" fill="${b.s.color}" class="pt" data-tip="${htmlEscape(JSON.stringify({
        name: `${b.s.code_family}/${b.s.variant}`,
        field: b.s.field,
        rate: `cfg ${b.s.nominal_rate} · actual ${actualRateDisplay(b.r)}`,
        k: kBar,
        gib: fmtNum(b.r.throughput_gib_s, 3),
        melem: fmtNum(b.r.throughput_melem_s, 2),
        mean: fmtNum(b.r.encode_mean_ms, 3),
        med: fmtNum(b.r.encode_median_ms, 3),
        setup: fmtNum(b.r.setup_ms, 2),
        rss: fmtNum(b.r.peak_rss_gib, 3),
      }))}" />`;
      out += `<text x="${left + bw + 8}" y="${y + 16}" fill="var(--muted)" font-size="10.5">${fmtNum(val, 2)} ${unit}</text>`;
    });
    svg.innerHTML = out;
  } else {
    svg.setAttribute("viewBox", "0 0 980 340");
    svg.style.height = "340px";
    const vals = active.flatMap(s => Object.values(s.byK).map(r => Number(r[state.metric])).filter(v => v > 0));
    if (!vals.length) {
      svg.innerHTML = `<text x="490" y="165" text-anchor="middle" fill="var(--muted)" font-size="13">All curves hidden in legend</text>`;
      return;
    }
    const isLog = state.metric === "encode_mean_ms" || (Math.max(...vals) / Math.min(...vals) > 15);
    const minRaw = Math.min(...vals), maxRaw = Math.max(...vals);
    const yMin = isLog ? Math.pow(10, Math.floor(Math.log10(minRaw))) : 0;
    const yMax = isLog ? Math.pow(10, Math.ceil(Math.log10(maxRaw))) : maxRaw * 1.12;
    const pad = { l: 64, r: 24, t: 18, b: 36 }, W = 980, H = 340;
    const pw = W - pad.l - pad.r, ph = H - pad.t - pad.b;
    const xPos = k => pad.l + ((k - 20) / 10) * pw;
    const yPos = v => isLog
      ? pad.t + ph - ((Math.log10(v) - Math.log10(yMin)) / Math.max(1e-9, Math.log10(yMax) - Math.log10(yMin))) * ph
      : pad.t + ph - ((v - yMin) / Math.max(1e-9, yMax - yMin)) * ph;

    let out = "";
    const ticks = isLog
      ? Array.from({ length: Math.round(Math.log10(yMax) - Math.log10(yMin)) + 1 }, (_, i) => Math.pow(10, Math.log10(yMin) + i))
      : [0, 0.25, 0.5, 0.75, 1].map(f => yMin + f * (yMax - yMin));
    for (const tv of ticks) {
      const y = yPos(tv);
      out += `<line x1="${pad.l}" y1="${y}" x2="${W - pad.r}" y2="${y}" stroke="var(--line-soft)" />`;
      out += `<text x="${pad.l - 8}" y="${y + 4}" text-anchor="end" fill="var(--muted)" font-size="10.5">${isLog ? tv.toPrecision(1) : fmtNum(tv, 2)}</text>`;
    }
    for (const k of SIZES) {
      const x = xPos(k);
      out += `<line x1="${x}" y1="${pad.t}" x2="${x}" y2="${H - pad.b}" stroke="var(--line-soft)" />`;
      out += `<text x="${x}" y="${H - 12}" text-anchor="middle" fill="var(--muted)" font-size="11">k=${k}</text>`;
    }
    out += `<line x1="${pad.l}" y1="${pad.t}" x2="${pad.l}" y2="${H - pad.b}" stroke="var(--line)" />`;
    out += `<line x1="${pad.l}" y1="${H - pad.b}" x2="${W - pad.r}" y2="${H - pad.b}" stroke="var(--line)" />`;

    for (const s of active) {
      const pts = SIZES.filter(k => s.byK[k] && Number(s.byK[k][state.metric]) > 0)
        .map(k => ({ k, r: s.byK[k], x: xPos(k), y: yPos(Number(s.byK[k][state.metric])) }));
      if (pts.length > 1) {
        out += `<polyline fill="none" stroke="${s.color}" stroke-width="2.1" points="${pts.map(p => `${p.x},${p.y}`).join(" ")}" />`;
      }
      for (const p of pts) {
        out += `<circle cx="${p.x}" cy="${p.y}" r="4.3" fill="${s.color}" stroke="var(--surface)" stroke-width="1.4" class="pt"
          data-tip="${htmlEscape(JSON.stringify({
            name: `${s.code_family}/${s.variant}`,
            field: s.field,
            rate: `cfg ${s.nominal_rate} · actual ${actualRateDisplay(p.r)}`,
            k: p.k,
            gib: fmtNum(p.r.throughput_gib_s, 3),
            melem: fmtNum(p.r.throughput_melem_s, 2),
            mean: fmtNum(p.r.encode_mean_ms, 3),
            med: fmtNum(p.r.encode_median_ms, 3),
            setup: fmtNum(p.r.setup_ms, 2),
            rss: fmtNum(p.r.peak_rss_gib, 3),
          }))}" />`;
      }
    }
    svg.innerHTML = out;
  }

  svg.querySelectorAll(".pt").forEach(el => {
    el.addEventListener("mouseenter", (e) => {
      const d = JSON.parse(el.dataset.tip);
      tip.innerHTML = `<strong>${htmlEscape(d.name)}</strong> (${htmlEscape(d.field)}, k=${d.k})<br>` +
        `rate: ${htmlEscape(d.rate)}<br>throughput: ${d.gib} GiB/s · ${d.melem} MElem/s<br>` +
        `mean: ${d.mean} ms · median: ${d.med} ms<br>setup: ${d.setup} ms · peak RSS: ${d.rss} GiB`;
      tip.style.display = "block";
      tip.style.left = Math.min(window.innerWidth - 350, e.clientX + 12) + "px";
      tip.style.top = (e.clientY + 12) + "px";
    });
    el.addEventListener("mouseleave", () => { tip.style.display = "none"; });
  });
}

function renderTables() {
  const rows = filteredRows();
  document.getElementById("matchCount").textContent = `${rows.length} / ${DATA.length}`;
  const tracks = state.track === "all" ? Object.keys(TRACKS) : [state.track];
  const htmlParts = [];

  for (const tid of tracks) {
    const trows = rows.filter(r => r.table_id === tid);
    if (!trows.length) continue;
    const meta = TRACKS[tid] || { title: tid, badge: "gen", desc: "" };
    const okCount = trows.filter(r => r.status === "OK").length;
    const head = `<div class="sec-head"><div class="sec-title"><h2>${htmlEscape(meta.title)}</h2>` +
      `<span class="sec-badge ${meta.badge}">${okCount} OK / ${trows.length} shown</span></div><p class="sec-desc">${htmlEscape(meta.desc)}</p></div>`;

    if (state.view === "matrix") {
      const series = groupSeries(trows);
      let lastGroup = null;
      const bodyRows = [];
      for (const s of series) {
        if (s.group !== lastGroup) {
          bodyRows.push(`<tr class="fam"><th colspan="10">${htmlEscape(s.group)}</th></tr>`);
          lastGroup = s.group;
        }
        const cells = SIZES.map(k => {
          const r = s.byK[k];
          if (!r) return `<td class="num"><span class="val-sub">—</span></td>`;
          if (r.status === "OK") {
            const tipTitle = `actual ${actualRateDisplay(r)}` + (r.notes ? ` · ${r.notes}` : "");
            return `<td class="num" title="${htmlEscape(tipTitle)}"><span class="val-main">${fmtNum(r.throughput_gib_s, 2)} GiB/s</span>` +
              `<span class="val-sub">${fmtNum(r.encode_mean_ms, 2)} ms · ${fmtNum(r.throughput_melem_s, 1)}M/s</span></td>`;
          }
          return `<td class="num">${statusChip(r.status, r.notes)}</td>`;
        }).join("");
        const actRate = s.actualKeys.size === 1
          ? `<span class="val-sub">actual ${htmlEscape([...s.actualDisplays][0])}</span>`
          : (s.actualKeys.size > 1 ? `<span class="val-sub">actual varies by k</span>` : "");
        const threadTag = s.threads && s.threads !== "32" ? `<span class="tag mid">${htmlEscape(s.threads)}T</span>` : "";
        bodyRows.push(`<tr>
          <td><span class="tag dim">#${htmlEscape(s.zoo_id)}</span></td>
          <td><span class="cname">${htmlEscape(s.code_family)} / ${htmlEscape(s.variant)}</span> ${threadTag}
              <span class="sub">${repoChip(s.repo)}</span></td>
          <td><span class="mono">${htmlEscape(s.field)}</span><span class="val-sub">${htmlEscape(s.field_bits)}b</span></td>
          <td><span class="mono">${htmlEscape(s.nominal_rate)}</span>${actRate}</td>
          ${cells}
        </tr>`);
      }
      htmlParts.push(`<section class="sec">${head}<div class="tw"><table><thead><tr>
        <th>Zoo</th><th>Code / Variant &amp; Repo</th><th>Field</th><th>Rate</th>
        ${SIZES.map(k => `<th class="num">k=${k}</th>`).join("")}
      </tr></thead><tbody>${bodyRows.join("")}</tbody></table></div></section>`);
    } else if (state.view === "compare") {
      const kRows = trows.filter(r => Number(r.k) === state.kFocus);
      const okK = kRows.filter(r => r.status === "OK");
      const nonOkK = kRows.filter(r => r.status !== "OK");
      const slices = new Map();
      for (const r of okK) {
        const rk = actualRateKey(r);
        const sliceKey = `${r.field}\0${rk}`;
        if (!slices.has(sliceKey)) {
          slices.set(sliceKey, {
            field: r.field,
            rateKey: rk,
            rateNum: actualRateNumeric(r),
            rateDisp: actualRateDisplay(r),
            rows: [],
          });
        }
        slices.get(sliceKey).rows.push(r);
      }
      const hb = state.metric !== "encode_mean_ms";
      const rowHtml = (r, maxVal) => {
        const ok = r.status === "OK";
        const val = ok ? Number(r[state.metric]) : 0;
        const pct = ok && maxVal > 0 ? Math.min(100, (val / maxVal) * 100) : 0;
        const rk = actualRateKey(r);
        return `<tr>
          <td><span class="tag dim">#${htmlEscape(r.zoo_id)}</span></td>
          <td><span class="cname">${htmlEscape(r.code_family)} / ${htmlEscape(r.variant)}</span><span class="sub">${repoChip(r.repo)}</span></td>
          <td class="mono">${htmlEscape(r.field)}</td>
          <td class="mono">${rk ? `${fmtNum(r.actual_rate, 4)}<span class="val-sub">K/N=${htmlEscape(rk)} · cfg ${htmlEscape(r.nominal_rate)}</span>` : `—<span class="val-sub">cfg ${htmlEscape(r.nominal_rate)}</span>`}</td>
          <td class="num">${r.threads || "32"}</td>
          <td class="num">${fmtNum(r.setup_ms, 2)}</td>
          <td class="num">${fmtNum(r.encode_mean_ms, 3)}</td>
          <td class="num">${fmtNum(r.encode_median_ms, 3)}</td>
          <td class="num">${fmtNum(r.throughput_melem_s, 2)}</td>
          <td class="num bar-cell">${ok ? `<strong>${fmtNum(r.throughput_gib_s, 3)}</strong><div class="bar-track"><div class="bar-fill" style="width:${pct.toFixed(1)}%"></div></div>` : "—"}</td>
          <td>${statusChip(r.status, r.notes)}<span class="sub">${htmlEscape((r.notes || "").slice(0, 80))}</span></td>
        </tr>`;
      };
      const blocks = [];
      const sortedSlices = Array.from(slices.values()).sort((a, b) =>
        a.field.localeCompare(b.field) ||
        (Number.isFinite(a.rateNum) && Number.isFinite(b.rateNum) ? a.rateNum - b.rateNum : 0) ||
        a.rateKey.localeCompare(b.rateKey)
      );
      for (const sl of sortedSlices) {
        const maxVal = Math.max(1e-9, ...sl.rows.map(r => Number(r[state.metric]) || 0));
        const sorted = [...sl.rows].sort((a, b) => hb
          ? Number(b[state.metric]) - Number(a[state.metric])
          : Number(a[state.metric]) - Number(b[state.metric]));
        blocks.push(`<tr class="fam"><th colspan="11">${htmlEscape(sl.field)} · actual K/N = ${htmlEscape(sl.rateDisp)} (k=${state.kFocus})</th></tr>`);
        blocks.push(...sorted.map(r => rowHtml(r, maxVal)));
      }
      if (nonOkK.length) {
        const sortedNon = [...nonOkK].sort((a, b) => a.status.localeCompare(b.status) || a.field.localeCompare(b.field) || a.code_family.localeCompare(b.code_family));
        blocks.push(`<tr class="fam"><th colspan="11">Pending / Limits / Excluded at k=${state.kFocus} (${nonOkK.length})</th></tr>`);
        blocks.push(...sortedNon.map(r => rowHtml(r, 1)));
      }
      const bodyRows = blocks.join("");
      htmlParts.push(`<section class="sec">${head}<div class="tw"><table><thead><tr>
        <th>Zoo</th><th>Code / Variant</th><th>Field</th><th>Actual Rate (Cfg)</th><th class="num">T</th>
        <th class="num">Setup (ms)</th><th class="num">Mean (ms)</th><th class="num">Median (ms)</th>
        <th class="num">MElem/s</th><th class="num">GiB/s</th><th>Status &amp; Notes</th>
      </tr></thead><tbody>${bodyRows}</tbody></table></div></section>`);
    } else {
      const bodyRows = trows.map(r => `<tr>
        <td><span class="tag dim">#${htmlEscape(r.zoo_id)}</span></td>
        <td><span class="cname">${htmlEscape(r.code_family)} / ${htmlEscape(r.variant)}</span><span class="sub">${repoChip(r.repo)}</span></td>
        <td class="mono">${htmlEscape(r.field)}</td>
        <td class="mono">${htmlEscape(r.nominal_rate)}${actualRateKey(r) ? `<span class="val-sub">actual ${actualRateDisplay(r)}</span>` : ""}</td>
        <td class="num">${r.k}</td>
        <td class="num">${r.threads || "32"}</td>
        <td class="num">${fmtNum(r.setup_ms, 2)}</td>
        <td class="num">${fmtNum(r.encode_mean_ms, 3)}</td>
        <td class="num">${fmtNum(r.encode_median_ms, 3)}</td>
        <td class="num">${fmtNum(r.throughput_melem_s, 2)}</td>
        <td class="num">${fmtNum(r.throughput_gib_s, 3)}</td>
        <td class="num">${fmtNum(r.peak_rss_gib, 3)}</td>
        <td>${statusChip(r.status, r.notes)}<span class="sub">${htmlEscape(r.notes || "")}</span></td>
      </tr>`).join("");
      htmlParts.push(`<section class="sec">${head}<div class="tw"><table><thead><tr>
        <th>Zoo</th><th>Code / Variant</th><th>Field</th><th>Rate</th><th class="num">k</th><th class="num">T</th>
        <th class="num">Setup (ms)</th><th class="num">Mean (ms)</th><th class="num">Median (ms)</th>
        <th class="num">MElem/s</th><th class="num">GiB/s</th><th class="num">RSS (GiB)</th><th>Status &amp; Notes</th>
      </tr></thead><tbody>${bodyRows}</tbody></table></div></section>`);
    }
  }
  document.getElementById("tablesRoot").innerHTML = htmlParts.join("") || `<p class="val-sub">No matching rows.</p>`;
}

function render() {
  renderStats();
  renderChart();
  renderTables();
}

syncDynamicPills();
render();
</script>
</body>
</html>
"""


def load_rows(csv_paths: list[Path]) -> list[dict[str, str]]:
    rows = []
    for path in csv_paths:
        with path.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                group_label, group_order = COMPLEXITY_ORDER.get(r["zoo_id"], ("Other Linear Codes", 99))
                r["group_label"] = group_label
                r["group_order"] = group_order
                r["notes"] = (r.get("notes") or "").strip()
                rows.append(r)
    return rows


def fmt_num(val: str, decimals: int = 3) -> str:
    if not val:
        return "—"
    try:
        return f"{float(val):.{decimals}f}"
    except ValueError:
        return val


def actual_rate_fraction(r: dict[str, str]) -> str:
    in_raw = (r.get("input_elements") or "").strip()
    out_raw = (r.get("codeword_elements") or "").strip()
    if in_raw and out_raw:
        try:
            k_in = int(in_raw)
            n_out = int(out_raw)
            if k_in > 0 and n_out > 0:
                frac = Fraction(k_in, n_out)
                return f"{frac.numerator}/{frac.denominator}"
        except ValueError:
            pass
    return (r.get("actual_rate") or "").strip()


def actual_rate_numeric(r: dict[str, str]) -> float:
    in_raw = (r.get("input_elements") or "").strip()
    out_raw = (r.get("codeword_elements") or "").strip()
    if in_raw and out_raw:
        try:
            k_in = int(in_raw)
            n_out = int(out_raw)
            if k_in > 0 and n_out > 0:
                return k_in / n_out
        except ValueError:
            pass
    raw = (r.get("actual_rate") or "").strip()
    try:
        return float(raw)
    except ValueError:
        return float("nan")


NON_OK_VISIBLE = {
    "DOMAIN_LIMIT", "OOM_SKIPPED", "OOM_LIMIT", "HOST_MEMORY_LIMIT",
    "FAILED", "EXCLUDED", "EXCLUDED_INTERLEAVED", "UNSUPPORTED_BACKEND",
}


def render_family_markdown(family: str, rows: list[dict[str, str]]) -> str:
    title = FAMILY_TITLES.get(family, family)
    repos = sorted({r["repo"] for r in rows if r.get("repo")})
    fields = sorted({r["field"] for r in rows if r.get("field")})
    zoo_ids = sorted({f"#{r['zoo_id']}" for r in rows if r.get("zoo_id")})
    ks = sorted({int(r["k"]) for r in rows})
    k_grid = ", ".join(map(str, ks))
    st_counts = Counter(r["status"] for r in rows)
    status_str = ", ".join(f"{k}: {v}" for k, v in sorted(st_counts.items()))

    lines = [
        f"# {title}",
        "",
        f"Single-polynomial 1D encoding benchmarks for `{family}` (Zoo {', '.join(zoo_ids)}; status summary: {status_str}).",
        "",
        "## Setup & Parameters",
        "",
        "- **Hardware & Runtime**: AMD EPYC 9754, 503 GiB RAM, 32 physical cores pinned to CPUs 0–31 (`taskset -c 0-31`, `RAYON_NUM_THREADS=32`, `OMP_NUM_THREADS=32`); release build (`target-cpu=native`)",
        f"- **Repositories / Revisions**: {', '.join(f'`{x}`' for x in repos)}",
        f"- **Field(s)**: {', '.join(f'`{x}`' for x in fields)}",
        f"- **Message Lengths**: `K = 2^k` (`k ∈ {{{k_grid}}}`)",
        "- **1D Geometry**: Single codeword (`nrows = 1`, `width = 1`, `log_batch_size = 0`; no interleaving, no 2D matrix reshape)",
        "",
        "## Measurement Methodology",
        "",
        "- **Sampling**: 1 warmup + 3 serial measured runs; reports arithmetic mean and median.",
        f"- **Timing Scope**: Measures the native 1D encoder call (`input_elements` -> `codeword_elements`) only; excludes setup (`setup_ms`), input generation, caller-buffer reset (for in-place entry points), correctness checks, and Merkle hashing/opening. Before timing, the driver pre-touches or reuses caller-owned buffers; output and temporary scratch buffers allocated internally by the encoder during the timed interval can still trigger page faults, and those times are included in the recorded measurements (per-row minor/major fault counts are logged in `results/{family}.csv` `notes`).",
        "- **Throughput & Memory**: `MElem/s = input_elements / 1e6 / (encode_mean_ms / 1000)`, `GiB/s = input_bytes / 2^30 / (encode_mean_ms / 1000)`. `Peak RSS` is whole-process peak resident memory (`GiB`), including setup.",
        "",
        "## Results",
        "",
        "| Variant | Field | Nominal Rate | Actual Rate | k | T | Setup (ms) | Mean (ms) | Median (ms) | MElem/s | GiB/s | Peak RSS (GiB) | Status |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for r in sorted(rows, key=lambda x: (x["table_id"], x["variant"], x["field"], x["nominal_rate"], int(x["k"]))):
        lines.append(
            f"| `{r['variant']}` | `{r['field']}` | `{r['nominal_rate']}` | {fmt_num(r['actual_rate'], 4)} | "
            f"{r['k']} | {r['threads']} | {fmt_num(r['setup_ms'], 2)} | {fmt_num(r['encode_mean_ms'], 3)} | "
            f"{fmt_num(r['encode_median_ms'], 3)} | {fmt_num(r['throughput_melem_s'], 2)} | "
            f"{fmt_num(r['throughput_gib_s'], 3)} | {fmt_num(r['peak_rss_gib'], 3)} | `{r['status']}` |"
        )

    special = sorted({(r["variant"], r["field"], r["nominal_rate"], r["status"], r["notes"])
                      for r in rows if r["status"] in NON_OK_VISIBLE or (r["notes"] and not r["notes"].startswith("peak minor"))})
    if special:
        lines.extend(["", "## Notes & Boundaries", ""])
        seen_notes = set()
        for var, fld, rt, st, note in special:
            clean = re.sub(r"\s*peak minor faults/sample=\d+; timed major faults=\d+\.\s*", " ", note).strip()
            key = (var, fld, rt, st, clean)
            if clean and key not in seen_notes:
                seen_notes.add(key)
                lines.append(f"- `{var}` (`{fld}`, config rate `{rt}`, `{st}`): {clean}")
    lines.append("")
    return "\n".join(lines)


def render_readme(rows: list[dict[str, str]], out_dir: Path, generated_at: str) -> str:
    st_counts = Counter(r["status"] for r in rows)
    by_family: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in rows:
        by_family[r["code_family"]].append(r)

    status_order = ["OK", "PENDING", "DOMAIN_LIMIT", "OOM_SKIPPED", "OOM_LIMIT", "HOST_MEMORY_LIMIT", "EXCLUDED_INTERLEAVED", "UNSUPPORTED_BACKEND", "EXCLUDED", "FAILED"]
    status_parts = [f"`{st_counts[s]}` {s}" for s in status_order if st_counts.get(s, 0) > 0 or s in {"OK", "PENDING", "DOMAIN_LIMIT", "OOM_SKIPPED"}]
    for s in sorted(st_counts):
        if s not in status_order:
            status_parts.append(f"`{st_counts[s]}` {s}")

    lines = [
        "# code-bench",
        "",
        "Benchmark archive for **1D single-polynomial linear code encoders** used in code-based polynomial commitment schemes (PCS), structured after [`pcs-bench`](https://github.com/jjllzhang/pcs-bench) with paired `<code_family>.md` + `<code_family>.csv` files under [`results/`](results/) and an interactive report at [`docs/index.html`](docs/index.html).",
        "",
        f"> **Snapshot Status** (`{generated_at}`): {' · '.join(status_parts)} (`{len(rows)}` total grid points).",
        "",
        "## Repository Structure",
        "",
        "```text",
        "code-bench/",
        "├── README.md            # Index of benchmarked code families & same-actual-rate snapshots",
        "├── TEMPLATE.md          # Markdown template for adding new code encoders",
        "├── docs/",
        "│   └── index.html       # Interactive PCS-Zoo-style viewer + SVG scaling charts",
        "├── results/             # Paired <code_family>.md and <code_family>.csv files",
        "│   └── tracks/          # Track CSVs (prime_goldilocks_1d, binary_1d, native_fields_1d)",
        "└── scripts/",
        "    └── build_view.py    # Rebuilds README, per-family MD/CSV, and docs/index.html from CSVs",
        "```",
        "",
        "## Benchmarked Code Families",
        "",
        "| Code Family | Zoo # | Variants | Field(s) | Config Rates | Tested `k` | Status (`OK/Total`) | Data |",
        "|---|---|---|---|---|---|---|---|",
    ]
    def fam_sort(item):
        fam, frows = item
        z = frows[0]["zoo_id"]
        return (COMPLEXITY_ORDER.get(z, ("", 99))[1], fam)

    for fam, frows in sorted(by_family.items(), key=fam_sort):
        zoo = ", ".join(sorted({f"#{r['zoo_id']}" for r in frows}))
        variants = ", ".join(sorted({f"`{r['variant']}`" for r in frows}))
        fields = ", ".join(sorted({f"`{r['field']}`" for r in frows}))
        rates = ", ".join(sorted({f"`{r['nominal_rate']}`" for r in frows}))
        ks = sorted({int(r["k"]) for r in frows})
        krange = ", ".join(map(str, ks))
        ok_n = sum(1 for r in frows if r["status"] == "OK")
        lines.append(
            f"| {FAMILY_TITLES.get(fam, fam)} | {zoo} | {variants} | {fields} | {rates} | {krange} | {ok_n}/{len(frows)} | [md](results/{fam}.md) · [csv](results/{fam}.csv) |"
        )

    # Same-field, same-actual-rate quick comparison snapshot for completed OK rows
    ok_rows = [r for r in rows if r["status"] == "OK"]
    if ok_rows:
        lines.extend([
            "",
            "## Same-Field & Same-Actual-Rate Snapshot (Completed `OK` Rows)",
            "",
            "Grouped strictly by `(table_id, field, reduced K/N, k)` using the exact reduced fraction `K/N = input_elements / codeword_elements` (4-decimal values in the table are for display only; `nominal_rate` is retained as configuration metadata).",
            "",
        ])
        by_slice: dict[tuple[str, str, str, int], list[dict[str, str]]] = defaultdict(list)
        for r in ok_rows:
            by_slice[(r["table_id"], r["field"], actual_rate_fraction(r), int(r["k"]))].append(r)

        def slice_sort(item: tuple[tuple[str, str, str, int], list[dict[str, str]]]):
            (tab, fld, rate_key, k), srows = item
            return (tab, fld, actual_rate_numeric(srows[0]), rate_key, k)

        for (tab, fld, rate_key, k), srows in sorted(by_slice.items(), key=slice_sort):
            rate_dec = fmt_num(srows[0]["actual_rate"], 4)
            lines.extend([
                f"### `{tab}` · `{fld}` · actual `K/N = {rate_key}` ({rate_dec}) · `k = {k}` (`2^{k}` elements)",
                "",
                "| Code / Variant | Zoo # | Config Rate | Actual Rate | Mean (ms) | Median (ms) | MElem/s | GiB/s | Peak RSS (GiB) |",
                "|---|---|---|---:|---:|---:|---:|---:|---:|",
            ])
            for r in sorted(srows, key=lambda x: -float(x["throughput_gib_s"])):
                lines.append(
                    f"| `{r['code_family']}/{r['variant']}` | #{r['zoo_id']} | `{r['nominal_rate']}` | {fmt_num(r['actual_rate'], 4)} | "
                    f"{fmt_num(r['encode_mean_ms'], 3)} | {fmt_num(r['encode_median_ms'], 3)} | "
                    f"{fmt_num(r['throughput_melem_s'], 2)} | **{fmt_num(r['throughput_gib_s'], 3)}** | {fmt_num(r['peak_rss_gib'], 3)} |"
                )
            lines.append("")

    lines.extend([
        "## Conventions",
        "",
        "- **1D Single-Codeword Rule & Grid**: Inputs are single 1D vectors of `K = 2^k` elements (`k ∈ {20, 22, 24, 26, 28, 30}`, `nrows = 1`, `width = 1`, `log_batch_size = 0`). Interleaved codes and 2D matrix-reshaped tensor codes are excluded (`EXCLUDED_INTERLEAVED`).",
        "- **Timing Scope**: Measures the native encoder call (`encode_mean_ms`, `encode_median_ms` across 3 serial runs after 1 warmup), excluding setup (`setup_ms`), input generation, caller-buffer reset (for in-place entry points), correctness checks, and Merkle hashing. Before timing, drivers pre-touch or reuse caller-owned buffers; however, output and temporary scratch buffers allocated internally by the encoder during the timed interval can still incur page faults (logged per row in `notes`), and those costs are included.",
        "- **Hardware & Affinity**: AMD EPYC 9754 (503 GiB RAM), pinned to CPUs `0-31` (`RAYON_NUM_THREADS=32`, `OMP_NUM_THREADS=32`), serial one-process-per-config execution.",
        "- **Rate & Boundary Transparency**: Rankings and snapshots group strictly by the exact reduced fraction `K/N` (`input_elements / codeword_elements`, with 4-decimal rounding used for display only), while preserving `nominal_rate` for configuration filtering; `DOMAIN_LIMIT`, `OOM_SKIPPED`, `OOM_LIMIT`, `HOST_MEMORY_LIMIT`, `EXCLUDED_INTERLEAVED`, `UNSUPPORTED_BACKEND`, and `PENDING` statuses are preserved explicitly.",
        "- Use [`TEMPLATE.md`](TEMPLATE.md) when adding a new code family.",
        "",
    ])
    return "\n".join(lines)


def _safe_json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def build(csv_dir: Path, out_dir: Path) -> None:
    track_names = ["prime_goldilocks_1d.csv", "binary_1d.csv", "native_fields_1d.csv"]
    csv_files = [csv_dir / n for n in track_names if (csv_dir / n).is_file()]
    if not csv_files and (csv_dir / "tracks").is_dir():
        csv_files = [csv_dir / "tracks" / n for n in track_names if (csv_dir / "tracks" / n).is_file()]
    if not csv_files:
        csv_files = sorted(csv_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {csv_dir}")

    # Load both parsed rows and raw track CSV payloads before touching out_dir
    # so in-place rebuilds (--csv-dir <out>/results/tracks --out-dir <out>) are safe.
    rows = load_rows(csv_files)
    src_payloads = [(src.name, src.read_text(encoding="utf-8")) for src in csv_files]
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ")

    by_family: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in rows:
        by_family[r["code_family"]].append(r)

    family_outputs: list[tuple[str, list[dict[str, str]], str]] = []
    for fam, frows in sorted(by_family.items()):
        sorted_frows = sorted(
            frows, key=lambda x: (x["table_id"], x["variant"], x["field"], x["nominal_rate"], int(x["k"]))
        )
        family_outputs.append((fam, sorted_frows, render_family_markdown(fam, sorted_frows)))

    readme_text = render_readme(rows, out_dir, generated_at)
    html_payload = (
        HTML_TEMPLATE
        .replace("__DATA_JSON__", _safe_json(rows))
        .replace("__TRACKS_JSON__", _safe_json(TRACK_META))
        .replace("__GENERATED_JSON__", _safe_json(generated_at))
    )

    results_dir = out_dir / "results"
    tracks_dir = results_dir / "tracks"
    docs_dir = out_dir / "docs"
    results_dir.mkdir(parents=True, exist_ok=True)
    tracks_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    # Remove stale per-family Markdown/CSV and track CSVs before emitting refreshed files
    for stale in results_dir.glob("*.csv"):
        stale.unlink()
    for stale in results_dir.glob("*.md"):
        stale.unlink()
    for stale in tracks_dir.glob("*.csv"):
        stale.unlink()

    # Write track CSVs into results/tracks/ from buffered payloads
    for name, content in src_payloads:
        (tracks_dir / name).write_text(content, encoding="utf-8")

    # Emit paired per-family CSV + MD matching pcs-bench
    for fam, sorted_frows, md_text in family_outputs:
        with (results_dir / f"{fam}.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(sorted_frows)
        (results_dir / f"{fam}.md").write_text(md_text, encoding="utf-8")

    (out_dir / "README.md").write_text(readme_text, encoding="utf-8")
    (docs_dir / "index.html").write_text(html_payload, encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Build code-bench Markdown/CSV/HTML presentation from track CSVs.")
    ap.add_argument("--csv-dir", type=Path, default=DEFAULT_SRC, help="Source directory containing track CSVs")
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT, help="Destination code-bench view directory")
    args = ap.parse_args()
    build(args.csv_dir, args.out_dir)


if __name__ == "__main__":
    main()
