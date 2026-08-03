# Dependencies

Python package dependencies for the Active InferAnts framework.

The authoritative dependency lists are `pyproject.toml` and
`requirements.txt`; the tables below summarize where each package is used.

## Core Dependencies

Installed via `pip install -r requirements.txt` (also declared in
`pyproject.toml`):

| Package | Used In | Purpose |
|---------|---------|---------|
| `numpy` | All phases | Matrix operations, numerical computing |
| `scipy` | 2_OPERATE, 3_MEASURE | Scientific computing, entropy calculations |
| `matplotlib` | 2_OPERATE, 3_MEASURE | Visualization, animation |
| `pandas` | 2_OPERATE, 3_MEASURE | Data analysis, DataFrames |
| `seaborn` | 2_OPERATE, 3_MEASURE | Statistical visualization |
| `networkx` | 3_MEASURE | Graph-based categorization |
| `pyyaml` | Configuration | YAML parsing |
| `tqdm` | Benchmarking | Progress bars |
| `cryptography` | 1_PREPARE/Utils | Cryptographic operations |
| `argon2-cffi` | 1_PREPARE/Utils | Password hashing |
| `fastapi` | 6_API | REST API framework |
| `uvicorn` | 6_API | ASGI server |
| `sqlalchemy` | 6_API | RDBMS ORM |
| `pydantic` | 6_API | Data model validation |
| `requests` | 6_API, 1_PREPARE | HTTP client |

## API Extras (multi-database backends)

The Knowledge API uses these best-effort secondary stores. Install with
`pip install -e ".[api]"` or the corresponding lines of `requirements.txt`:

| Package | Used In | Purpose |
|---------|---------|---------|
| `pymongo` | 6_API | MongoDB driver (secondary store) |
| `redis` | 6_API | Redis cache (secondary store) |
| `elasticsearch` | 6_API | Search engine (secondary store) |
| `neo4j` | 6_API | Neo4j graph database (secondary store) |
| `motor` | 6_API | Async MongoDB driver (reserved) |
| `aiocache` | 6_API | Async caching (reserved) |
| `aioredis` | 6_API | Async Redis client (reserved) |
| `psutil` | Benchmarking | Process/memory metrics |

## Optional / Subsystem Dependencies

Not installed by default; required only by the named subsystem:

| Package | Used In | Purpose |
|---------|---------|---------|
| `pymdp` | 1_PREPARE/Things | PyMDP-based agents (`pymdp_Ant_1.py`, `Thing.py`) |
| `tabulate` | 1_PREPARE/Things | Formatted table output (pseudo-pymdp variants) |
| `spacy` | 0_CONTEXT/Systems/William_Blake | NLP entity extraction |

## Development Dependencies

Installed via `pip install -e ".[dev]"` or `requirements-dev.txt`:

| Package | Purpose |
|---------|---------|
| `pytest` | Test runner |
| `httpx` | TestClient HTTP backend |
| `ruff` | Linting and formatting (pre-commit + CI) |

## Installation

```bash
pip install -r requirements.txt                 # Core
pip install -e ".[api]"                          # API secondary stores
pip install -e ".[dev]"                          # Development tooling
pip install pymdp tabulate                       # PyMDP-based agents (optional)
```
