from redis import ConnectionPool, Redis

from core.config import settings


redis_pool: ConnectionPool = ConnectionPool.from_url(
    f"redis://{settings.REDIS_HOST}",
    db=settings.REDIS_DB,
    decode_responses=True,
)


def get_redis() -> Redis:
    """Get an instance of CustomRedis with the configured connection pool."""

    return Redis(connection_pool=redis_pool)
