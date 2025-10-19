from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=find_dotenv())

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    RMQ_HOST: str
    RMQ_USER: str
    RMQ_PASS: str
    RMQ_FOR_RETRIES: str
    RMX_FOR_RETRIES: str
    DLQ_FOR_RETRIES: str
    DLX_FOR_RETRIES: str
    RMQ_NOT_SOLVED: str
    TTL_FOR_RETRIES: int

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def rmq_url(self):
        return f"amqp://{self.RMQ_USER}:{self.RMQ_PASS}@{self.RMQ_HOST}/"


settings = Settings()
