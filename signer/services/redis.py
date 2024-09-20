from time import sleep
from contextlib import contextmanager
from redis import ConnectionPool, Redis
from redis.exceptions import ConnectionError

from core.config import settings
from core.logging import CustomLogger


logger = CustomLogger.setup()
redis_pool: ConnectionPool = ConnectionPool.from_url(
    f"redis://{settings.REDIS_HOST}",
    db=settings.REDIS_DB,
    decode_responses=True,
)


def get_redis() -> Redis:
    """Get an instance of Redis with the connection pool."""

    max_retries = 60
    retry_delay = 1
    attempt = 0
    while attempt < max_retries:
        try:
            redis = Redis(connection_pool=redis_pool)
            redis.ping()
            logger.info("Successfully connected to Redis")
            return redis
        except ConnectionError as e:
            attempt += 1
            logger.error(
                f"Failed {attempt} from {max_retries} attempts to connect to Redis: {e}"
            )
            sleep(retry_delay)
    raise ConnectionError(f"Could not connect to Redis after {max_retries} attempts")


redis = get_redis()


@contextmanager
def redis_lock(lock_key, lock_timeout=15, sleep_time=0.1, max_retries=50):
    """
    Контекстный менеджер для управления блокировками Redis.
    """
    lock = redis.lock(
        lock_key,
        timeout=lock_timeout,
        sleep=sleep_time,
        blocking_timeout=max_retries * sleep_time
    )
    acquired = lock.acquire(blocking=True)
    try:
        if acquired:
            logger.info(f"Блокировка захвачена: {lock_key}")
            yield
        else:
            logger.info(f"Не удалось захватить блокировку: {lock_key}")
    finally:
        if acquired:
            lock.release()
            logger.info(f"Блокировка освобождена: {lock_key}")
            