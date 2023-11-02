import logging
from functools import wraps
from tenacity import (
    retry,
    wait_fixed,
    stop_after_delay,
    stop_after_attempt,
)


logger = logging.getLogger("fastapi")


def attempt_counter_log(retry_state):
    if retry_state.attempt_number < 1:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING
    logger.log(
        loglevel,
        "Retrying %s: attempt %s ended with: %s",
        retry_state.kwargs.get("iin_bin"),
        retry_state.attempt_number,
        retry_state.outcome,
    )


def tenacity_retry(func):
    """Retry decorator if any error occurs."""

    @wraps(func)
    @retry(
        stop=stop_after_attempt(3) | stop_after_delay(600),
        wait=wait_fixed(10),
        reraise=True,
        after=attempt_counter_log,
    )
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)

    return wrapper
