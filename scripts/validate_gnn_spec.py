#!/usr/bin/env python3
"""Strict local gate: validate the Gaussian agent GNN spec against the pinned GNN.

Parses ``gnn/gaussian_agent.gnn.md`` with the Generalized Notation Notation
revision pinned in ``gnn/upstream.json`` (read from the pinned commit, never the
checkout's working tree) and checks the extracted matrices against the
framework agent in ``active_infer_ants``.

Exit codes: 0 pass, 1 conformance failure, 2 the pinned GNN checkout or its
interpreter is unavailable (set GNN_ROOT / GNN_PYTHON).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from gnn_conformance import (  # noqa: E402  (import after the sys.path insert)
    SPEC_PATH,
    ConformanceError,
    GnnUnavailable,
    check_conformance,
    extract_spec,
    receipt,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, default=SPEC_PATH)
    parser.add_argument("--gnn-root", type=Path, default=None)
    parser.add_argument("--interpreter", type=Path, default=None)
    args = parser.parse_args(argv)

    try:
        model = extract_spec(
            args.spec, gnn_root=args.gnn_root, interpreter=args.interpreter
        )
        checks = check_conformance(model)
    except GnnUnavailable as exc:
        print(f"GNN unavailable: {exc}", file=sys.stderr)
        return 2
    except ConformanceError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(receipt(model, checks, spec=args.spec), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
