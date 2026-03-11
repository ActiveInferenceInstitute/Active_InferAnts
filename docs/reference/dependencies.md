# Dependencies

Python package dependencies for the Active InferAnts framework.

## Core Dependencies

| Package | Used In | Purpose |
|---------|---------|---------|
| `numpy` | All phases | Matrix operations, numerical computing |
| `matplotlib` | 2_OPERATE, 3_MEASURE | Visualization, animation |
| `pandas` | 2_OPERATE, 3_MEASURE | Data analysis, DataFrames |
| `seaborn` | 2_OPERATE, 3_MEASURE | Statistical visualization |
| `pymdp` | 1_PREPARE/Things | Active Inference inference and control |
| `scipy` | 2_OPERATE | Entropy calculations |
| `networkx` | 3_MEASURE | Graph-based categorization |
| `tabulate` | 1_PREPARE/Things | Formatted table output |

## API Dependencies

| Package | Used In | Purpose |
|---------|---------|---------|
| `fastapi` | 6_API | REST API framework |
| `pydantic` | 6_API | Data model validation |
| `sqlalchemy` | 6_API | PostgreSQL ORM |
| `pymongo` | 6_API | MongoDB driver |
| `motor` | 6_API | Async MongoDB driver |
| `redis` / `aioredis` | 6_API | Redis cache |
| `neo4j` | 6_API | Neo4j graph database |
| `elasticsearch` | 6_API | Search engine |
| `aiocache` | 6_API | Async caching |

## Optional Dependencies

| Package | Used In | Purpose |
|---------|---------|---------|
| `spacy` | 0_CONTEXT/Systems/William_Blake | NLP entity extraction |
| `requests` | 6_API, 1_PREPARE | HTTP client |
| `asyncio` | 4_REPORT, 5_FOLLOWUP, 6_API | Async execution |

## Installation

```bash
pip install numpy matplotlib pandas seaborn pymdp scipy networkx tabulate
pip install fastapi pydantic sqlalchemy pymongo redis neo4j elasticsearch  # For API
```
