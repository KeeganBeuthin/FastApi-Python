from fastapi import Request, HTTPException, status
from kinde_sdk.kinde_api_client import KindeApiClient
from kinde_sdk import Configuration
from .config import get_settings

settings = get_settings()

# User clients dictionary to store Kinde clients for each user
user_clients = {}

# Initialize Kinde configuration
configuration = Configuration(host=settings.kinde_domain)
kinde_api_client_params = {
    "configuration": configuration,
    "domain": settings.kinde_domain,
    "client_id": settings.kinde_client_id,
    "client_secret": settings.kinde_client_secret,
    "grant_type": settings.grant_type,
    "callback_url": settings.kinde_callback_url,
    "code_verifier": settings.code_verifier
}

def get_kinde_client(request: Request) -> KindeApiClient:
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    if user_id not in user_clients:
        user_clients[user_id] = KindeApiClient(**kinde_api_client_params)

    kinde_client = user_clients[user_id]
    if not kinde_client.is_authenticated():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    return kinde_client