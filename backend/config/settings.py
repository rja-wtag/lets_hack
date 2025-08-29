import os
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(os.environ["ENV_PATH"])


class Settings(BaseSettings):
    # Application
    app_name: str = os.environ.get('APP_NAME')
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    # Database
    database_url: Optional[str] = os.getenv('DB_URL')
    enable_persistence: bool = os.environ['ENABLE_PERSISTENCE']

    # Security
    secret_key: str = os.getenv('API_KEY')


@lru_cache()
def get_settings() -> Settings:
    return Settings()
