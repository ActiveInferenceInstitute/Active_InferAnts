"""Load actual phase definitions without optional-provider/import side effects.

Definition-only loading is for local contract tests, not provider qualification.
In particular it never imports FieldSHIFT config, requests credentials, downloads
NLTK data, or substitutes a production provider implementation.
"""

import ast
import importlib.util
import json
import logging
import os
import sys
from collections import Counter
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FIELD = Path("1_PREPARE/Methods/Research/FieldSHIFT-2")


def load_phase(monkeypatch, phase, name):
    path = ROOT / phase / f"{name}.py"
    module_name = f"_ants_contract_{phase}_{name}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, module_name, module)
    spec.loader.exec_module(module)
    return module


def load_definitions(relative, **values):
    path = ROOT / relative
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    nodes = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    ]
    namespace = {
        "__name__": "_ants_definition_contract",
        "__file__": str(path),
        "os": os,
        "json": json,
        "logging": logging,
        "logger": logging.getLogger("ants_contract"),
        "np": np,
        "Counter": Counter,
        "product": product,
        "DEFAULT_CONFIG": {
            "llm_params": {},
            "analysis_params": {"linguistic_features": []},
        },
    }
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in {
                    "TARGET_LANGUAGES",
                    "TARGET_AUDIENCES",
                }:
                    namespace[target.id] = ast.literal_eval(node.value)
    namespace.update(values)
    future = ast.ImportFrom(
        module="__future__", names=[ast.alias(name="annotations")], level=0
    )
    module = ast.fix_missing_locations(
        ast.Module(body=[future, *nodes], type_ignores=[])
    )
    exec(compile(module, str(path), "exec"), namespace)
    namespace.update(values)
    return namespace


class ForbiddenWork:
    def __init__(self):
        self.calls = []

    def __call__(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        raise AssertionError("Existing output must skip provider/input work")

    def __getattr__(self, name):
        self.calls.append(name)
        raise AssertionError("Existing output must skip data/render work")


def seed_output(root, relative, content=b"historical\x00\xff\r\n"):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path
