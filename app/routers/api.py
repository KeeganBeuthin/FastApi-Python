from fastapi import APIRouter, Depends
from kinde_sdk.kinde_api_client import KindeApiClient
from ..dependencies import get_kinde_client

router = APIRouter(tags=["api"])

@router.get("/items/{item_id}")
def read_item(
    item_id: int,
    kinde_client: KindeApiClient = Depends(get_kinde_client)
):
    return {"item_id": item_id, "authenticated": True}

