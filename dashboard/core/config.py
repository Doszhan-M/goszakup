from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    CELERY_BROKER_URL: str = "amqp://rabbitmq_user:rabbitmq_pass@localhost:5672/"


setup = Settings()

