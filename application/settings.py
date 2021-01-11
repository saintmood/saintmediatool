from pydantic import BaseSettings


class Settings(BaseSettings):

    media_bucket_name: str = None


settings = Settings