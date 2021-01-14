from pydantic import BaseSettings


class Settings(BaseSettings):

    media_bucket_name: str = 'saintmtool'


def settings() -> Settings:
    return Settings()