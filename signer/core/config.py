from os import path
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(f"{path.dirname(__file__)}/../../../env/eds.env")


class Settings(BaseSettings):
    DEPLOY: bool
    BASE_DIR: str = str(Path(__file__).resolve().parent.parent)
    ENVIRONMENT: str = "VIVOBOOK"


settings = Settings()
