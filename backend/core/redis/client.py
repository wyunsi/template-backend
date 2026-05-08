from collections.abc import AsyncGenerator

import redis.asyncio as aioredis

from core.config import settings

_pool: aioredis.ConnectionPool | None = None


def _get_pool() -> aioredis.ConnectionPool:
    global _pool
    if _pool is None:
        _pool = aioredis.ConnectionPool.from_url(
            settings.redis.url,
            max_connections=settings.redis.max_connections,
            socket_timeout=settings.redis.socket_timeout,
            socket_connect_timeout=settings.redis.socket_connect_timeout,
            decode_responses=True,
        )
    return _pool


async def get_redis() -> AsyncGenerator[aioredis.Redis]:
    client = aioredis.Redis(connection_pool=_get_pool())
    try:
        yield client
    finally:
        await client.aclose()
