from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from functools import lru_cache
from pydantic_settings import BaseSettings


if getenv("IN_DOCKER") != "TRUE":
    load_dotenv(f"{Path(__file__).resolve().parent}/.env")


class Settings(BaseSettings):
    IN_DOCKER: bool = False
    HEADLESS_DRIVER: bool = True
    BASE_DIR: str = str(Path(__file__).resolve().parent.parent)
    DEVELOPMENT: bool = False


settings = Settings()


@lru_cache()
def get_settings():
    return settings
