# Created by https://t.me/vlasovdev settings file | Создано https://t.me/vlasovdev settings file


from typing import List, Set

from pydantic import BaseModel, BaseSettings, PostgresDsn, RedisDsn, validator


class Webhook(BaseModel):
    base_url: str
    webserver_host: str = "0.0.0.0"
    webserver_port: int
    path: str


class Settings(BaseSettings):
    bot_token: str
    webhook: Webhook = None

    postgres_dsn: PostgresDsn
    redis_dsn: RedisDsn

    class Config:
        # Immutable class
        allow_mutation = False
        env_file = ".env"
        env_nested_delimiter = "__"


settings = Settings()
