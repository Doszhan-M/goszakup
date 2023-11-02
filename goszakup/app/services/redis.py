from redis import StrictRedis, asyncio

from app.core.config import settings


aioredis = asyncio.Redis.from_url(
    f"redis://{settings.REDIS_HOST}",
    db=4,
)
redis = StrictRedis(
    host=settings.REDIS_HOST,
    port=6379,
    db=4,
    decode_responses=True,
)
