from fastapi import APIRouter, Depends

from backend.config.dependencies import get_api_key

router = APIRouter(tags=["v1/Health"])


@router.get("/health")
async def health_check(api_key: str = Depends(get_api_key)):
    return {"status": "v1 healthy"}
