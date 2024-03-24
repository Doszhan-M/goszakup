from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    CELERY_BROKER_URL: str = "amqp://rabbitmq_user:rabbitmq_pass@localhost:5672/"
    MEDIA_PATH_ON_HOST: str = "/projects/goszakup/dashboard/app/media/"


setup = Settings()

