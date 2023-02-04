from pydantic import (
    BaseSettings,
)


class Settings(BaseSettings):
    api_id: str
    api_hash: str
    bot_token: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = 'app_'


settings = Settings()
