#!/usr/bin/env python3
"""Measure the gate arms and write `docs/_generated/gate_metrics.md`.

One document holds every measured number the repository quotes about its gate:
per-arm wall time, per-test-selection counts, and the frozen pre-change
baseline. Nothing here is hand-edited proof: the arms are executed through
`./run.sh` (the same commands CI runs), the counts come from `git ls-files` and
`pytest --collect-only`, and `--check` fails when the recorded counts drift.

Usage:
    python scripts/docgen/gate_metrics.py --write            # measure + write
    python scripts/docgen/gate_metrics.py --check            # fail if stale
    python scripts/docgen/gate_metrics.py --write-baseline   # re-freeze the
                                                             # pre-change numbers

`--write-baseline` measures the current arms before editing them and records
the current source revision. With `--measurements PATH`, either write mode can
import a JSON object captured by a separately governed measurement run instead
of running the arms again.
"""

from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
METRICS = REPO_ROOT / "docs" / "_generated" / "gate_metrics.md"
BASELINE = REPO_ROOT / "docs" / "_generated" / "gate_baseline.json"

# The arms of ./run.sh that are measured here, in execution order. `gate` is
# their union and is not measured separately (it would just duplicate them).
ARMS = ("lint", "test-fast", "test-full", "docs", "gnn")

# Trees the lint arm does not cover, with the rule selection the arm uses. They
# are measured rather than described: see the rendered "Out of scope" table.
OUT_OF_SCOPE = ("0_CONTEXT", "1_PREPARE", "9_OTHER")
OUT_OF_SCOPE_IGNORE = (
    "--select",
    "E4,E7,E9,F,I",
    "--target-version",
    "py39",
    "--no-cache",
)

# Summary lines used in generated receipts.
DETAIL_PATTERNS = (
    r"Found \d+ errors?",
    r"All checks passed",
    r"\d+ passed",
    r"Aborted with \d+ warnings",
    r"COMPILE FAIL",
    r"\d+ (?:files )?would be reformatted",
    r"\d+ files already formatted",
    r'"extraction_schema_version"',
)


def pick_detail(lines: list[str], fallback: str) -> str:
    """Return the most informative line, preferring a recognised summary."""
    for pattern in DETAIL_PATTERNS:
        found = [line for line in lines if re.search(pattern, line)]
        if found:
            return found[0]
    return lines[-1] if lines else fallback


def run(command: list[str], cwd: Path = REPO_ROOT) -> tuple[float, int, str]:
    """Run one command, returning (wall seconds, exit code, a summary line)."""
    start = time.monotonic()
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    elapsed = time.monotonic() - start
    lines = [
        line.strip()
        for line in (result.stdout + result.stderr).splitlines()
        if line.strip()
    ]
    return elapsed, result.returncode, pick_detail(lines, f"exit {result.returncode}")


def tracked(pattern: list[str]) -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z", "--", *pattern],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return [p for p in out.split("\0") if p]


def collected(marker: str | None) -> int:
    command = [sys.executable, "-m", "pytest", "-q", "--collect-only"]
    if marker:
        command += ["-m", marker]
    result = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True)
    output = result.stdout + result.stderr
    # Pytest reports a filtered collection as "31/41 tests collected".
    match = re.search(r"(\d+)/\d+ tests? collected", output) or re.search(
        r"(\d+) tests? collected", output
    )
    if not match:
        raise SystemExit(f"could not count tests for marker {marker!r}")
    return int(match.group(1))


def counts() -> dict[str, int]:
    docs = [p for p in tracked(["docs"]) if p.endswith(".md")]
    return {
        "tests_fast": collected("not gnn"),
        "tests_gnn": collected("gnn"),
        "tests_full": collected(None),
        "tracked_python": len(tracked(["*.py"])),
        "tracked_markdown": len(tracked(["*.md"])),
        "docs_markdown": len(docs),
    }


def measure_out_of_scope() -> dict[str, str]:
    """Record what the lint gate would report on the excluded trees.

    The numbers behind "out of scope" live here instead of in prose, so the
    exclusion stays an observation rather than a claim.
    """
    measured: dict[str, str] = {}
    for tree in OUT_OF_SCOPE:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "ruff",
                "check",
                *OUT_OF_SCOPE_IGNORE,
                tree,
                "--output-format=concise",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        measured[tree] = pick_detail(lines, "no findings")
    return measured


def measure_arms() -> dict[str, dict[str, object]]:
    measured: dict[str, dict[str, object]] = {}
    for arm in ARMS:
        print(f"measuring ./run.sh {arm} ...", file=sys.stderr)
        elapsed, code, detail = run(["bash", "run.sh", arm])
        measured[arm] = {
            "seconds": round(elapsed, 2),
            "exit": code,
            "detail": detail,
        }
    return measured


def measure_baseline() -> dict[str, object]:
    """Freeze the current arms before a change, without a second checkout."""
    return baseline_receipt(measure_arms())


def baseline_receipt(arms: dict[str, dict[str, object]]) -> dict[str, object]:
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO_ROOT,
        stdin=subprocess.DEVNULL,
        text=True,
    ).strip()
    return {
        "recorded": date.today().isoformat(),
        "host": host(),
        "source": revision,
        "arms": [
            {
                "arm": arm,
                "seconds": data["seconds"],
                "ok": data["exit"] == 0,
                "detail": data["detail"],
            }
            for arm, data in arms.items()
        ],
    }


def host() -> str:
    return (
        f"{platform.system()} {platform.machine()}, Python {platform.python_version()}"
    )


def render(receipt: dict[str, object]) -> str:
    counts_ = receipt["counts"]
    assert isinstance(counts_, dict)
    lines = [
        "# Gate metrics",
        "",
        "> Generated by `scripts/docgen/gate_metrics.py` — do not edit by hand.",
        "> Refresh with `python scripts/docgen/gate_metrics.py --write`; the",
        "> `docs` gate arm fails when the recorded counts go stale.",
        "",
        f"Measured {receipt['recorded']} on {receipt['host']}, one run per arm,",
        "with the arms executed through `./run.sh` exactly as CI executes them.",
        "Wall time is the arm's own wall clock, so it includes interpreter",
        "startup and the arm's subprocesses.",
        "",
        "## Current arms",
        "",
        "| Arm | Wall time | Exit | Last line |",
        "|---|---:|---:|---|",
    ]
    arms = receipt["arms"]
    assert isinstance(arms, dict)
    for arm in ARMS:
        data = arms[arm]
        assert isinstance(data, dict)
        detail = str(data["detail"]).replace("|", "\\|")
        lines.append(
            f"| `./run.sh {arm}` | {data['seconds']:.2f} s | {data['exit']} | {detail} |"
        )
    total = sum(float(arms[a]["seconds"]) for a in ("lint", "test-fast", "docs", "gnn"))  # type: ignore[index]
    lines += [
        "",
        f"`./run.sh gate` runs lint, test-fast, docs and gnn: {total:.2f} s of",
        "measured arm time. `test-full` is a superset used on its own (it adds the",
        "gnn-marked module to test-fast), so nothing is run twice by the gate.",
        "",
        "## Test selection",
        "",
        "| Selection | Tests |",
        "|---|---:|",
        f'| `pytest -m "not gnn"` (test-fast) | {counts_["tests_fast"]} |',
        f"| `pytest -m gnn` (gnn) | {counts_['tests_gnn']} |",
        f"| `pytest` (test-full) | {counts_['tests_full']} |",
        "",
        "## Repository inventory",
        "",
        "| Fact | Value |",
        "|---|---:|",
        f"| Tracked Python files | {counts_['tracked_python']} |",
        f"| Tracked Markdown files | {counts_['tracked_markdown']} |",
        f"| Markdown files under `docs/` | {counts_['docs_markdown']} |",
        "",
    ]
    lines += [
        "## Out of scope",
        "",
        "The lint arm covers the maintained Python surface (`active_infer_ants`,",
        "`tests`, `scripts`, `gnn_conformance.py`, and the phase directories",
        "`2_OPERATE`–`6_API`). These trees are outside it; the numbers below are",
        "what the same rule selection reports on them, measured with the metrics:",
        "",
        "| Tree | `ruff check` under the gate's rules |",
        "|---|---|",
    ]
    out_of_scope = receipt.get("out_of_scope")
    if isinstance(out_of_scope, dict):
        for tree, detail in out_of_scope.items():
            lines.append(f"| `{tree}/` | {str(detail).replace('|', chr(92) + '|')} |")
    lines.append("")
    baseline = receipt.get("baseline")
    if isinstance(baseline, dict):
        lines += [
            "## Pre-change baseline",
            "",
            f"Recorded {baseline['recorded']} on {baseline['host']}, one run",
            f"of each `./run.sh` arm at source `{baseline['source']}`.",
            "Setup and parser acquisition are excluded; both columns use an",
            "already-provisioned parser. Single samples are not a benchmark",
            "distribution; no hosted-CI speedup is inferred.",
            "",
            "| Arm before | Wall time | Green | Command → last line |",
            "|---|---:|---|---|",
        ]
        for arm in baseline["arms"]:
            detail = str(arm["detail"]).replace("|", "\\|")
            lines.append(
                f"| {arm['arm']} | {arm['seconds']:.2f} s | "
                f"{'yes' if arm['ok'] else 'no'} | {detail} |"
            )
        lines.append("")
    lines += [
        "<!-- gate-metrics-receipt",
        json.dumps(receipt, indent=2, sort_keys=True),
        "-->",
    ]
    return "\n".join(lines) + "\n"


def previous_arms() -> dict[str, dict[str, object]]:
    """Return the arms recorded in the current page, or a "not yet" placeholder.

    The placeholder is what gets published while the arms are being measured;
    it must render (and must not claim a time the harness has not observed).
    """
    unmeasured = {
        arm: {"seconds": 0.0, "exit": -1, "detail": "not measured in this run"}
        for arm in ARMS
    }
    if not METRICS.exists():
        return unmeasured
    match = re.search(
        r"<!-- gate-metrics-receipt\n(.*?)\n-->",
        METRICS.read_text(encoding="utf-8"),
        re.DOTALL,
    )
    if not match:
        return unmeasured
    try:
        recorded = json.loads(match.group(1)).get("arms", {})
    except json.JSONDecodeError:
        return unmeasured
    return {arm: recorded.get(arm, unmeasured[arm]) for arm in ARMS}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="measure and rewrite")
    mode.add_argument("--check", action="store_true", help="fail if stale")
    mode.add_argument(
        "--write-baseline", action="store_true", help="re-freeze the baseline JSON"
    )
    parser.add_argument("--measurements", type=Path, help="import captured arm results")
    args = parser.parse_args(argv)
    # Importing captured measurements avoids repeating tests simply to publish
    # their timings after an offline, source-bound execution has finished.
    if args.measurements:
        measured = json.loads(args.measurements.read_text(encoding="utf-8"))
        if set(measured) != set(ARMS):
            parser.error("measurements must contain exactly the gate arms")
        for data in measured.values():
            if "output" in data:
                data["detail"] = pick_detail(
                    data.pop("output").splitlines(), "no output"
                )
    else:
        measured = None

    if args.write_baseline:
        BASELINE.write_text(
            json.dumps(
                baseline_receipt(measured)
                if measured is not None
                else measure_baseline(),
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"wrote {BASELINE.relative_to(REPO_ROOT)}")
        return 0

    if args.check:
        if not METRICS.exists():
            print(f"{METRICS.relative_to(REPO_ROOT)} is missing", file=sys.stderr)
            return 1
        match = re.search(
            r"<!-- gate-metrics-receipt\n(.*?)\n-->",
            METRICS.read_text(encoding="utf-8"),
            re.DOTALL,
        )
        if not match:
            print(f"{METRICS.relative_to(REPO_ROOT)} has no receipt", file=sys.stderr)
            return 1
        receipt = json.loads(match.group(1))
        stale = {
            key: (receipt["counts"].get(key), value)
            for key, value in counts().items()
            if receipt["counts"].get(key) != value
        }
        if stale:
            for key, (recorded, current) in stale.items():
                print(
                    f"stale count {key}: doc {recorded}, now {current}", file=sys.stderr
                )
            print(
                "run `python scripts/docgen/gate_metrics.py --write`",
                file=sys.stderr,
            )
            return 1
        print(f"{METRICS.relative_to(REPO_ROOT)} is current")
        return 0

    receipt: dict[str, object] = {
        "recorded": date.today().isoformat(),
        "host": host(),
        "counts": counts(),
        "out_of_scope": measure_out_of_scope(),
        "arms": previous_arms(),
    }
    if BASELINE.exists():
        receipt["baseline"] = json.loads(BASELINE.read_text(encoding="utf-8"))
        if receipt["baseline"].get("recorded") != date.today().isoformat():
            print(
                f"note: baseline is frozen from {receipt['baseline']['recorded']}; "
                "re-run --write-baseline to re-measure it",
                file=sys.stderr,
            )
    # Publish the fresh counts before measuring: the docs arm runs inside this
    # measurement, and it must not see a stale page just because the arm's own
    # wall time has not been recorded yet.
    METRICS.write_text(render(receipt), encoding="utf-8")
    receipt["arms"] = measured if measured is not None else measure_arms()
    METRICS.write_text(render(receipt), encoding="utf-8")
    print(f"wrote {METRICS.relative_to(REPO_ROOT)}")
    return int(any(data["exit"] != 0 for data in receipt["arms"].values()))


if __name__ == "__main__":
    raise SystemExit(main())
