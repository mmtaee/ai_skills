"""
Redis configuration and lifecycle management.
Initializes the Redis client and provides a way to access it throughout the application.
"""

from typing import Optional

from config.settings import settings
from pkg.redis.client import RedisClient
from redis.asyncio import Redis

_redis_client: Optional[RedisClient] = None


def init_redis():
    """
    Initialize the global Redis client.
    Called during application startup.
    """
    global _redis_client
    client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=True,
    )
    _redis_client = RedisClient(client)


def get_redis() -> RedisClient:
    """
    Get the global Redis client.
    Raises an error if the client hasn't been initialized.
    """
    if _redis_client is None:
        raise RuntimeError("Redis client is not initialized. Call init_redis() first.")
    return _redis_client


async def close_redis():
    """
    Close the Redis connection.
    Called during application shutdown.
    """
    global _redis_client
    if _redis_client:
        await _redis_client.client.close()
        _redis_client = None
