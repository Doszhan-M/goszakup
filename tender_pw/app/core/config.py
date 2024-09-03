from pathlib import Path
from dotenv import load_dotenv
from functools import lru_cache
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv(f"{BASE_DIR.parent.parent}/env/tender.env")


class Settings(BaseSettings):
    OPENAPI_USER: str = "admin"
    OPENAPI_PASS: str = "aCiOnIQuArdE"
    HEADLESS_DRIVER: bool = False
    BASE_DIR: str = str(BASE_DIR)
    SIGNER_HOST: str = "127.0.0.1:50051"


settings = Settings()


@lru_cache()
def get_settings():
    return settings
