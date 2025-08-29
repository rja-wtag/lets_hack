import pytest
from fastapi import HTTPException, status

from backend.config.dependencies import get_api_key


def test_get_api_key_invalid():
    with pytest.raises(HTTPException) as exc_info:
        get_api_key(api_key="invalid-key")
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc_info.value.detail == "Could not validate API key"
