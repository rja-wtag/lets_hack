import os

from dotenv import load_dotenv
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

load_dotenv(os.environ["ENV_PATH"])

API_KEY = os.getenv('API_KEY')
api_key_header = APIKeyHeader(name="x-api-key")


def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API key")
    return api_key
