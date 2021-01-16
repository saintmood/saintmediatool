from pydantic import BaseSettings


class Settings(BaseSettings):
    environment: str = 'development'
    media_bucket_name: str = 'saintmtool'
    domain: str = 'localhost'


class TestSettings(Settings):
    environment: str = 'test'
    media_bucket_name: str = 'test_saintmtool'



def settings() -> Settings:
    return Settings()


def test_settings() -> Settings:
    return TestSettings()