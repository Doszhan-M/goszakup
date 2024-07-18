from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool
    CELERY_BROKER_URL: str
    MEDIA_PATH_ON_HOST: str
    GOSZAKUP_URL: str


setup = Settings()
