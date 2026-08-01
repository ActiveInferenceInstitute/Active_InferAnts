"""
Knowledge API — Active InferAnts knowledge management service.

FastAPI service for managing knowledge items across multiple databases with
automatic synchronization. Written to be parse-correct and internally coherent:
database access is consistently synchronous (SQLAlchemy + sync clients), CORS is
restricted to configured origins, and every credential comes from the
environment rather than being hardcoded in source.
"""

import hmac
import logging
import os
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import JSON, Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.orm import Session, declarative_base, sessionmaker


# --------------------------------------------------------------------------- #
# Configuration (all from environment; no secrets in source)
# --------------------------------------------------------------------------- #
def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


class Config:
    SQLALCHEMY_DATABASE_URL = _env(
        "KNOWLEDGE_DB_URL",
        "sqlite:///./knowledge.db",  # safe local default; override in production
    )
    MONGODB_URL = _env("KNOWLEDGE_MONGO_URL", "mongodb://localhost:27017/")
    MONGO_DB = _env("KNOWLEDGE_MONGO_DB", "knowledge_db")
    REDIS_URL = _env("KNOWLEDGE_REDIS_URL", "redis://localhost:6379/0")
    ELASTICSEARCH_URL = _env("KNOWLEDGE_ES_URL", "http://localhost:9200")
    ES_INDEX = _env("KNOWLEDGE_ES_INDEX", "knowledge")
    NEO4J_URL = _env("KNOWLEDGE_NEO4J_URL", "bolt://localhost:7687")
    NEO4J_USER = _env("KNOWLEDGE_NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = _env("KNOWLEDGE_NEO4J_PASSWORD", "")
    # No default API key: authentication is enabled only when X-API-KEY is set in
    # the environment. When unset the service still starts (local/dev use).
    API_KEY = _env("KNOWLEDGE_API_KEY", "")
    LOG_LEVEL = _env("KNOWLEDGE_LOG_LEVEL", "INFO")
    # Comma-separated list of allowed CORS origins; never '*'.
    ALLOW_ORIGINS = _env("KNOWLEDGE_ALLOW_ORIGINS", "http://localhost:8000")


config = Config()

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("knowledge_api")

# --------------------------------------------------------------------------- #
# App + CORS
# --------------------------------------------------------------------------- #
app = FastAPI(
    title="Knowledge API",
    description="API for managing knowledge across multiple databases",
    version="3.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in config.ALLOW_ORIGINS.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------------------------- #
# SQLAlchemy (consistently synchronous)
# --------------------------------------------------------------------------- #
engine = create_engine(
    config.SQLALCHEMY_DATABASE_URL,
    pool_size=20,
    max_overflow=0,
    connect_args={"check_same_thread": False}
    if config.SQLALCHEMY_DATABASE_URL.startswith("sqlite")
    else {},
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


class KnowledgeItem(Base):
    __tablename__ = "knowledge_items"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True, unique=True)
    content = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------------------------------- #
# API key authentication (constant-time compare; enabled only when configured)
# --------------------------------------------------------------------------- #
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_api_key(api_key_header: str | None = Depends(api_key_header)) -> str | None:
    if not config.API_KEY:
        # No key configured -> open (local/dev) mode.
        return None
    if api_key_header and hmac.compare_digest(api_key_header, config.API_KEY):
        return api_key_header
    raise HTTPException(status_code=403, detail="Could not validate API key")


# --------------------------------------------------------------------------- #
# Pydantic models
# --------------------------------------------------------------------------- #
class KnowledgeBase(BaseModel):
    source: str = Field(..., description="Unique identifier for the knowledge item")
    content: dict[str, Any] = Field(..., description="Content of the knowledge item")

    @field_validator("source")
    @classmethod
    def source_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError("Source must not be empty")
        return v

    model_config = ConfigDict(
        json_schema_extra={"example": {"source": "example_source", "content": {"key": "value"}}}
    )


# --------------------------------------------------------------------------- #
# Optional sync clients for the secondary stores (gracefully Optional)
# --------------------------------------------------------------------------- #
def _get_clients():
    """Return sync clients for the configured secondary stores.

    Each is lazy/optional: if the driver is unavailable or the store unreachable
    the corresponding entry is None, and the sync helper ignores it. This keeps a
    single-source installation (SQLite only) fully usable.
    """
    clients = {"mongo": None, "redis": None, "es": None, "neo4j": None}
    if config.MONGODB_URL:
        try:
            from pymongo import MongoClient

            clients["mongo"] = MongoClient(config.MONGODB_URL, serverSelectionTimeoutMS=1000)
        except Exception as e:  # pragma: no cover - env dependent
            logger.warning("Mongo unavailable: %s", e)
    if config.REDIS_URL:
        try:
            import redis

            clients["redis"] = redis.from_url(config.REDIS_URL, socket_connect_timeout=1)
        except Exception as e:  # pragma: no cover
            logger.warning("Redis unavailable: %s", e)
    if config.ELASTICSEARCH_URL:
        try:
            from elasticsearch import Elasticsearch

            clients["es"] = Elasticsearch(
                config.ELASTICSEARCH_URL, request_timeout=1, max_retries=0
            )
        except Exception as e:  # pragma: no cover
            logger.warning("Elasticsearch unavailable: %s", e)
    if config.NEO4J_URL:
        try:
            from neo4j import GraphDatabase

            clients["neo4j"] = GraphDatabase.driver(
                config.NEO4J_URL,
                auth=(config.NEO4J_USER, config.NEO4J_PASSWORD),
            )
        except Exception as e:  # pragma: no cover
            logger.warning("Neo4j unavailable: %s", e)
    return clients


def _sync_to_secondary(clients, knowledge: KnowledgeBase) -> None:
    """Best-effort synchronous write fan-out to the configured secondary stores."""
    payload = knowledge.model_dump()
    if clients["mongo"] is not None:
        try:
            clients["mongo"][config.MONGO_DB]["knowledge_items"].replace_one(
                {"source": knowledge.source}, payload, upsert=True
            )
        except Exception as e:
            logger.warning("Mongo write failed: %s", e)
    if clients["redis"] is not None:
        try:
            import json

            clients["redis"].set(f"knowledge:{knowledge.source}", json.dumps(payload))
        except Exception as e:
            logger.warning("Redis write failed: %s", e)
    if clients["es"] is not None:
        try:
            clients["es"].index(
                index=config.ES_INDEX, id=knowledge.source, document=payload
            )
        except Exception as e:
            logger.warning("Elasticsearch write failed: %s", e)
    if clients["neo4j"] is not None:
        try:
            with clients["neo4j"].session() as session:
                session.run(
                    "MERGE (k:Knowledge {source: $source}) SET k.content = $content",
                    source=knowledge.source, content=str(knowledge.content),
                )
        except Exception as e:
            logger.warning("Neo4j write failed: %s", e)


# --------------------------------------------------------------------------- #
# Endpoints
# --------------------------------------------------------------------------- #
@app.post("/api/knowledge/", response_model=dict[str, Any], status_code=201)
def create_knowledge(
    knowledge: KnowledgeBase,
    db: Session = Depends(get_db),
    _: str | None = Depends(get_api_key),
):
    try:
        existing = (
            db.query(KnowledgeItem).filter(KnowledgeItem.source == knowledge.source).first()
        )
        if existing:
            raise HTTPException(status_code=409, detail="Knowledge source already exists")
        item = KnowledgeItem(source=knowledge.source, content=knowledge.content)
        db.add(item)
        db.commit()
        db.refresh(item)
        _sync_to_secondary(_get_clients(), knowledge)
        logger.info("Knowledge created: %s", knowledge.source)
        return {"message": "Knowledge created successfully", "id": item.id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error creating knowledge: %s", e)
        raise HTTPException(status_code=500, detail="Error creating knowledge") from None


@app.get("/api/knowledge/{source}", response_model=dict[str, Any])
def read_knowledge(
    source: str,
    db: Session = Depends(get_db),
    _: str | None = Depends(get_api_key),
):
    try:
        item = db.query(KnowledgeItem).filter(KnowledgeItem.source == source).first()
        if not item:
            raise HTTPException(status_code=404, detail="Knowledge not found")
        return {"source": item.source, "content": item.content}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error retrieving knowledge: %s", e)
        raise HTTPException(status_code=500, detail="Error retrieving knowledge") from None


@app.put("/api/knowledge/{source}", response_model=dict[str, str])
def update_knowledge(
    source: str,
    knowledge: KnowledgeBase,
    db: Session = Depends(get_db),
    _: str | None = Depends(get_api_key),
):
    try:
        item = db.query(KnowledgeItem).filter(KnowledgeItem.source == source).first()
        if not item:
            raise HTTPException(status_code=404, detail="Knowledge not found")
        item.content = knowledge.content
        item.updated_at = func.now()
        db.commit()
        _sync_to_secondary(_get_clients(), knowledge)
        logger.info("Knowledge updated: %s", source)
        return {"message": "Knowledge updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error updating knowledge: %s", e)
        raise HTTPException(status_code=500, detail="Error updating knowledge") from None


@app.delete("/api/knowledge/{source}", response_model=dict[str, str])
def delete_knowledge(
    source: str,
    db: Session = Depends(get_db),
    _: str | None = Depends(get_api_key),
):
    try:
        item = db.query(KnowledgeItem).filter(KnowledgeItem.source == source).first()
        if not item:
            raise HTTPException(status_code=404, detail="Knowledge not found")
        db.delete(item)
        db.commit()
        logger.info("Knowledge deleted: %s", source)
        return {"message": "Knowledge deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error deleting knowledge: %s", e)
        raise HTTPException(status_code=500, detail="Error deleting knowledge") from None


@app.get("/api/knowledge/", response_model=list[dict[str, Any]])
def list_knowledge(
    skip: int = Query(0, description="Number of items to skip"),
    limit: int = Query(10, description="Number of items to return"),
    db: Session = Depends(get_db),
    _: str | None = Depends(get_api_key),
):
    try:
        items = db.query(KnowledgeItem).order_by(KnowledgeItem.id).offset(skip).limit(limit).all()
        return [
            {
                "id": item.id,
                "source": item.source,
                "content": item.content,
                "created_at": item.created_at.isoformat() if item.created_at else None,
                "updated_at": item.updated_at.isoformat() if item.updated_at else None,
            }
            for item in items
        ]
    except Exception as e:
        logger.error("Error listing knowledge: %s", e)
        raise HTTPException(status_code=500, detail="Error listing knowledge") from None


@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/api/docs")


@app.get("/api/health", include_in_schema=False)
def health_check():
    return {"status": "ok"}


# --------------------------------------------------------------------------- #
# Custom OpenAPI + entries
# --------------------------------------------------------------------------- #
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    schema["servers"] = [{"url": "/"}]
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
