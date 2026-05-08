"""
Synchronous DB session for Celery workers.
Engine is lazily initialised via worker_process_init signal to avoid
inheriting parent-process connection pools across prefork.
"""

import logging
from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.config import settings

logger = logging.getLogger(__name__)

_sync_engine: Engine | None = None
_SessionLocal: sessionmaker[Session] | None = None


def _build_sync_url() -> str:
    return str(settings.db.url).replace("+asyncpg", "+psycopg")


def init_sync_engine() -> None:
    global _sync_engine, _SessionLocal
    _sync_engine = create_engine(
        _build_sync_url(),
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
        pool_pre_ping=settings.db.pool_pre_ping,
        pool_recycle=settings.db.pool_recycle,
        pool_timeout=settings.db.pool_timeout,
        echo=settings.db.echo,
    )
    _SessionLocal = sessionmaker(bind=_sync_engine, expire_on_commit=False)
    logger.info("Sync DB engine initialised (pid=%s)", __import__("os").getpid())


def dispose_sync_engine() -> None:
    global _sync_engine, _SessionLocal
    if _sync_engine is not None:
        _sync_engine.dispose()
        logger.info("Sync DB engine disposed (pid=%s)", __import__("os").getpid())
    _sync_engine = None
    _SessionLocal = None


@contextmanager
def get_db() -> Generator[Session]:
    if _SessionLocal is None:
        init_sync_engine()
    assert _SessionLocal is not None
    session = _SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
