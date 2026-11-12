"""Conformance checks for the Active InferAnts Gaussian agent GNN specification.

The model is specified in ``gnn/gaussian_agent.gnn.md`` and validated with the
Generalized Notation Notation (GNN) revision pinned in ``gnn/upstream.json``.
The pinned revision is read from the pinned commit (via ``git archive``), never
from the GNN checkout's working tree, so in-progress edits in that repository
cannot contaminate a check.

The pin, its shape and the specification's syntax are the shared reader's work,
not this module's: ``gnn.importers`` reads the pin and validates the
specification from the pinned revision, and ``./run.sh gnn`` runs it before the
checks below. What remains here is what only this repository can assert: that
the extracted specification matches ``active_infer_ants``' agent. The reader is
imported lazily, because ``./run.sh test-fast`` runs without a GNN checkout.

Two entry points share this module:

- ``tests/test_gnn_conformance.py`` — pytest checks (the pinned-parser half
  skips cleanly when the GNN checkout or its interpreter is unavailable; the
  specification-vs-package checks run against the package's own agent);
- ``scripts/validate_gnn_spec.py`` — the strict local gate (fails, never
  skips).

The continuous (linear-Gaussian) extraction needs a Python with GNN's runtime
dependencies; ``GNN_PYTHON`` selects it, and the GNN checkout's own virtualenv
is used by default when present.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any

import numpy as np

if TYPE_CHECKING:  # the reader lives in the pinned checkout, imported lazily
    from gnn.importers import ImporterPin

REPO_ROOT = Path(__file__).resolve().parent
PIN_PATH = REPO_ROOT / "gnn" / "upstream.json"
SPEC_PATH = REPO_ROOT / "gnn" / "gaussian_agent.gnn.md"
DEFAULT_GNN_ROOT = REPO_ROOT.parent / "Generalized_Notation_Notation"

# The headless extractor contract consumed here: gnn.extract returns the model
# mapping described by this schema version. Major version 1 is required; minor
# versions may append keys.
REQUIRED_EXTRACT_SCHEMA_MAJOR = "1"


class ConformanceError(RuntimeError):
    """The specification does not conform to the pinned GNN revision or the package."""


class GnnUnavailable(ConformanceError):
    """The pinned GNN checkout or a suitable interpreter is not available."""


def _shared_reader(root: Path | str | None = None) -> Any:
    """Return ``gnn.importers`` from the pinned GNN source tree.

    The reader is imported from the checkout the pin materializes, so this
    repository validates against the parser its pin names and carries no second
    copy of the pin-reading logic.
    """

    checkout = resolve_gnn_root(root)
    source = checkout / "src"
    if str(source) not in sys.path:
        sys.path.insert(0, str(source))
    try:
        from gnn import importers
    except ImportError as exc:  # the pin predates the reader, or is not a checkout
        raise GnnUnavailable(
            f"the GNN checkout at {checkout} supplies no gnn.importers module "
            f"({exc}); gnn/upstream.json must name a revision that ships it"
        ) from exc
    return importers


def pinned_revision(root: Path | str | None = None) -> "ImporterPin":
    """Read the repository-local GNN pin with the shared reader."""

    importers = _shared_reader(root)
    try:
        return importers.read_pin(PIN_PATH)
    except importers.PinError as exc:
        raise ConformanceError(str(exc)) from exc


def resolve_gnn_root(explicit: Path | str | None = None) -> Path:
    """Return the GNN checkout path (``--gnn-root``, ``GNN_ROOT``, then sibling)."""

    candidates = [explicit, os.environ.get("GNN_ROOT"), DEFAULT_GNN_ROOT]
    for candidate in candidates:
        if not candidate:
            continue
        root = Path(candidate).expanduser().resolve()
        if (root / "src" / "gnn" / "__init__.py").is_file():
            return root
    raise GnnUnavailable(
        "no GNN checkout found; set GNN_ROOT or clone "
        "ActiveInferenceInstitute/Generalized_Notation_Notation next to this "
        f"repository ({DEFAULT_GNN_ROOT})"
    )


def pinned_source(root: Path, pin: "ImporterPin", destination: Path) -> Path:
    """Extract the pinned ``src/gnn`` tree into ``destination`` and return it."""

    destination.mkdir(parents=True, exist_ok=True)
    archive = subprocess.Popen(
        ["git", "-C", str(root), "archive", pin.commit, "src/gnn"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    extract = subprocess.run(
        ["tar", "-x", "-C", str(destination)],
        stdin=archive.stdout,
        capture_output=True,
        text=True,
        check=False,
    )
    assert archive.stdout is not None
    archive.stdout.close()
    archive_stderr = archive.stderr.read().decode() if archive.stderr else ""
    archive.wait()
    if archive.returncode != 0 or extract.returncode != 0:
        raise ConformanceError(
            f"could not extract pinned GNN source: {archive_stderr.strip()} "
            f"{extract.stderr.strip()}"
        )
    source = destination / "src"
    if not (source / "gnn" / "__init__.py").is_file():
        raise ConformanceError(f"pinned GNN extraction is incomplete at {source}")
    return source


def resolve_interpreter(root: Path) -> Path:
    """Return the Python used to run the pinned extractor.

    ``GNN_PYTHON`` wins; otherwise the GNN checkout's own virtualenv; otherwise
    the interpreter running this module. This repository's model is continuous
    (linear-Gaussian), which needs GNN's runtime dependencies, so the fallback
    only works when those are already installed.
    """

    explicit = os.environ.get("GNN_PYTHON")
    if explicit:
        interpreter = Path(explicit).expanduser()
        if not interpreter.is_file():
            raise GnnUnavailable(f"GNN_PYTHON does not exist: {interpreter}")
        return interpreter
    venv_python = root / ".venv" / "bin" / "python"
    if venv_python.is_file():
        return venv_python
    return Path(sys.executable)


def extract_spec(
    spec: Path = SPEC_PATH,
    gnn_root: Path | str | None = None,
    interpreter: Path | str | None = None,
) -> dict:
    """Parse ``spec`` with the pinned GNN extractor and return the mapping."""

    root = resolve_gnn_root(gnn_root)
    pin = pinned_revision(root)
    python = Path(interpreter) if interpreter else resolve_interpreter(root)
    spec = Path(spec).resolve()
    with tempfile.TemporaryDirectory(prefix="gnn-pinned-") as temporary:
        source = pinned_source(root, pin, Path(temporary))
        environment = dict(os.environ)
        existing = environment.get("PYTHONPATH")
        environment["PYTHONPATH"] = (
            f"{source}{os.pathsep}{existing}" if existing else str(source)
        )
        result = subprocess.run(
            [str(python), "-m", "gnn.extract", str(spec)],
            capture_output=True,
            text=True,
            env=environment,
            check=False,
        )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        if "could not be imported" in message or "environment is broken" in message:
            raise GnnUnavailable(
                f"the pinned GNN extractor cannot run with {python}: {message}"
            )
        raise ConformanceError(
            f"pinned GNN extractor failed (exit {result.returncode}): {message}"
        )
    model = json.loads(result.stdout)
    if isinstance(model, dict) and model.get("status") == "error":
        raise ConformanceError(
            f"pinned GNN extractor rejected {spec}: {model['error']}"
        )
    schema = str(model.get("extraction_schema_version", ""))
    if schema.split(".")[0] != REQUIRED_EXTRACT_SCHEMA_MAJOR:
        raise ConformanceError(
            f"unexpected extraction schema version {schema!r}; "
            f"this repository consumes major version {REQUIRED_EXTRACT_SCHEMA_MAJOR}"
        )
    return model


def spec_sha256(spec: Path = SPEC_PATH) -> str:
    """Return the SHA-256 of the specification bytes."""

    return hashlib.sha256(Path(spec).read_bytes()).hexdigest()


def _import_agent_class():
    """Import the framework agent (package installed from this repository)."""

    from active_infer_ants import ActiveInferenceAgent

    return ActiveInferenceAgent


def _parameter(model: dict, name: str) -> float:
    parameters = model.get("model_parameters") or {}
    if name not in parameters:
        raise ConformanceError(f"ModelParameters must declare {name}")
    return float(parameters[name])


def canonical_model(agent=None) -> dict:
    """Build the extractor-shaped mapping for the package agent's defaults.

    Used by the always-run checks and by tests; the extracted specification
    must match this mapping key by key.
    """

    ActiveInferenceAgent = _import_agent_class()
    agent = agent or ActiveInferenceAgent(seed=0)
    dimension = int(agent.n_dims)
    process_noise = (np.eye(dimension) / agent.prior_precision).tolist()
    return {
        "extraction_schema_version": "1.0.0",
        "model_kind": "continuous",
        "num_states": dimension,
        "num_observations": dimension,
        "initial_parameterization": {
            "F": np.eye(dimension).tolist(),
            "H": np.eye(dimension).tolist(),
            "Q": process_noise,
            "R": (np.eye(dimension) / agent.sensory_precision).tolist(),
            "prior_mean": agent.preferred.tolist(),
            "prior_cov": process_noise,
        },
        "model_parameters": {
            "num_states": dimension,
            "num_observations": dimension,
            "num_timesteps": 1,
            "prior_precision": agent.prior_precision,
            "sensory_precision": agent.sensory_precision,
            "learning_rate": agent.learning_rate,
        },
    }


def check_conformance(model: dict) -> list[str]:
    """Check the extracted specification against the framework agent.

    Returns the list of passed check names; raises :class:`ConformanceError` on
    the first mismatch.
    """

    ActiveInferenceAgent = _import_agent_class()
    agent = ActiveInferenceAgent(seed=0)
    passed: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            raise ConformanceError(message)

    require(model.get("model_kind") == "continuous", "model kind must be continuous")
    parameters = model.get("initial_parameterization") or {}
    require(
        set(parameters) >= {"F", "H", "Q", "R", "prior_mean", "prior_cov"},
        f"continuous parameterization is incomplete: {sorted(parameters)}",
    )
    transition = np.asarray(parameters["F"], dtype=float)
    readout = np.asarray(parameters["H"], dtype=float)
    process_noise = np.asarray(parameters["Q"], dtype=float)
    observation_noise = np.asarray(parameters["R"], dtype=float)
    prior_mean = np.asarray(parameters["prior_mean"], dtype=float)
    prior_cov = np.asarray(parameters["prior_cov"], dtype=float)

    dimension = int(agent.n_dims)
    require(
        int(model["num_states"]) == dimension == int(model["num_observations"]),
        f"dimensions: spec {model['num_states']}/{model['num_observations']} vs agent {dimension}",
    )
    for name, matrix in (
        ("F", transition),
        ("H", readout),
        ("Q", process_noise),
        ("R", observation_noise),
        ("prior_cov", prior_cov),
    ):
        require(
            matrix.shape == (dimension, dimension),
            f"{name} must be {dimension}x{dimension}",
        )
    require(
        prior_mean.shape == (dimension,), f"prior_mean must have length {dimension}"
    )
    passed.append(f"dimensions match the package agent (n_dims = {dimension})")

    require(
        np.allclose(transition, np.eye(dimension))
        and np.allclose(readout, np.eye(dimension)),
        "F and H must be identity (static latent, identity readout)",
    )
    passed.append("F and H are identity (static latent, identity readout)")

    prior_precision = _parameter(model, "prior_precision")
    sensory_precision = _parameter(model, "sensory_precision")
    require(
        prior_precision == agent.prior_precision
        and sensory_precision == agent.sensory_precision,
        "ModelParameters must match the agent's default precisions",
    )
    require(
        np.allclose(process_noise, np.eye(dimension) / prior_precision),
        "Q must be (1 / prior_precision) I",
    )
    require(
        np.allclose(observation_noise, np.eye(dimension) / sensory_precision),
        "R must be (1 / sensory_precision) I",
    )
    require(
        np.allclose(prior_cov, process_noise),
        "prior_cov must equal Q (the static latent's prior covariance)",
    )
    require(
        np.allclose(prior_mean, agent.preferred),
        "prior_mean must be the agent's initial preferred state",
    )
    passed.append("Q, R, prior_mean and prior_cov match the agent's Gaussian model")

    posterior_precision = 1.0 / np.diag(observation_noise) + 1.0 / np.diag(
        process_noise
    )
    for observation in (
        np.array([1.0, 2.0, 3.0]),
        np.array([-1.0, 0.5, 0.25]),
    ):
        action = agent.infer(observation)
        expected_mean = (
            agent.preferred / np.diag(process_noise)
            + observation / np.diag(observation_noise)
        ) / posterior_precision
        require(
            np.allclose(agent.pi, posterior_precision),
            "the agent's posterior precision does not match the declared Q and R",
        )
        require(
            np.allclose(agent.mu, expected_mean),
            "the agent's posterior mean does not match the declared Gaussian update",
        )
        require(
            np.allclose(action, agent.mu),
            "the agent's action must be the posterior mean",
        )
    passed.append("infer() performs the declared Gaussian posterior update")

    return passed


def receipt(model: dict, checks: list[str], spec: Path = SPEC_PATH) -> dict:
    """Build a JSON-serializable receipt for the validation run."""

    pin = pinned_revision()
    return {
        "spec": str(Path(spec).resolve().relative_to(REPO_ROOT)),
        "spec_sha256": spec_sha256(spec),
        "pin": {
            "repository": pin.repository or "",
            "tag": pin.tag or "",
            "commit": pin.commit,
        },
        "extraction_schema_version": model.get("extraction_schema_version"),
        "model_kind": model.get("model_kind"),
        "dimensions": {
            "num_states": model.get("num_states"),
            "num_observations": model.get("num_observations"),
        },
        "checks": checks,
    }
