from os import path
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(f"{path.dirname(__file__)}/../../env/signer.env")


class Settings(BaseSettings):
    DEPLOY: bool
    BASE_DIR: str = str(Path(__file__).resolve().parent.parent)
    REDIS_HOST: str = "127.0.0.1:6379"
    REDIS_DB: int = 1
    ENVIRONMENT: str = "VIVOBOOK"


settings = Settings()
