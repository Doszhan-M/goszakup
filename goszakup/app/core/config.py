from dotenv import load_dotenv
from functools import lru_cache
from os import path, environ, getenv

from pydantic_settings import BaseSettings


if getenv("IN_DOCKER") != "TRUE":
    load_dotenv(f"{path.dirname(__file__)}/.env.local")


class Settings(BaseSettings):
    IN_DOCKER: bool
    NCANODEURL: str


settings = Settings()


@lru_cache()
def get_settings():
    return settings


def clear_envs():
    """Clear environment variables after assigning BaseSettings."""

    env_variables: list = [
        attribute
        for attribute in dir(settings)
        if not attribute.startswith("_")
        and not attribute.startswith("__")
        and not callable(getattr(settings, attribute))
    ]
    [environ.pop(variable, None) for variable in env_variables]
