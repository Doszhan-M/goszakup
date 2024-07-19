from pathlib import Path
from dotenv import load_dotenv
from functools import lru_cache
from pydantic_settings import BaseSettings


load_dotenv(f"{Path(__file__).resolve().parent}/../../env/tender.env")


class Settings(BaseSettings):
    HEADLESS_DRIVER: bool = False
    BASE_DIR: str = str(Path(__file__).resolve().parent.parent)


settings = Settings()
