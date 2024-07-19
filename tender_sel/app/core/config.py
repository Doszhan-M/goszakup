from pathlib import Path
from dotenv import load_dotenv
from functools import lru_cache
from pydantic_settings import BaseSettings


load_dotenv(f"{Path(__file__).resolve().parent}/.env")


class Settings(BaseSettings):
    HEADLESS_DRIVER: bool = True
    BASE_DIR: str = str(Path(__file__).resolve().parent.parent)
    ENVIRONMENT: str = "TUF17"


settings = Settings()


@lru_cache()
def get_settings():
    return settings