#!/usr/bin/env python3
"""Check that every relative link in the documentation resolves.

The repository has no third-party link checker; this is its documentation
check. Only tracked Markdown is scanned, so an untracked scratch file cannot
make the gate pass or fail, and only relative links are checked (external URLs
are not fetched — the gate must run offline).

Scope: `docs/`, the root-level Markdown, and the folder guides the gate
maintains (`tests/`, `active_infer_ants/`, `gnn/`, `.github/`).

Exit codes: 0 every relative link resolves, 1 at least one does not.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

REPO_ROOT = Path(__file__).resolve().parents[1]

SCOPES = ("docs/", ".github/", "tests/", "active_infer_ants/", "gnn/")

# Inline Markdown links/images, excluding images (`!`) — a broken image is also
# worth catching, so images are included; only reference-style links, which have
# no inline target, are skipped.
LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)>\s]+)>?(?:\s+\"[^\"]*\")?\s*\)")

SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "data:", "#")


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return [p for p in out.split("\0") if p]


def in_scope(path: str) -> bool:
    return path.endswith(".md") and ("/" not in path or path.startswith(SCOPES))


def check(files: list[str]) -> list[tuple[str, str, str]]:
    broken: list[tuple[str, str, str]] = []
    for rel in files:
        source = REPO_ROOT / rel
        text = source.read_text(encoding="utf-8", errors="replace")
        for match in LINK_RE.finditer(text):
            raw = match.group(1)
            if raw.startswith(SKIP_PREFIXES):
                continue
            target = unquote(raw.split("#", 1)[0].split("?", 1)[0])
            if not target:
                continue
            if target.startswith("/"):
                broken.append((rel, raw, "absolute path, not repository-relative"))
                continue
            resolved = (source.parent / target).resolve()
            try:
                resolved.relative_to(REPO_ROOT)
            except ValueError:
                broken.append((rel, raw, "escapes the repository"))
                continue
            if not resolved.exists():
                broken.append((rel, raw, "target does not exist"))
    return broken


def main(argv: list[str] | None = None) -> int:
    del argv
    files = [f for f in tracked_files() if in_scope(f) and (REPO_ROOT / f).exists()]
    broken = check(files)
    for source, target, reason in broken:
        print(f"{source}: {target}: {reason}", file=sys.stderr)
    print(f"checked {len(files)} Markdown files, {len(broken)} broken relative links")
    return 1 if broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
