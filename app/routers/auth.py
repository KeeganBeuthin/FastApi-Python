from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from kinde_sdk.kinde_api_client import KindeApiClient
from ..dependencies import kinde_api_client_params, user_clients
from ..config import get_settings

settings = get_settings()
router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.get("/login")
def login():
    kinde_client = KindeApiClient(**kinde_api_client_params)
    return RedirectResponse(kinde_client.get_login_url())

@router.get("/register")
def register():
    kinde_client = KindeApiClient(**kinde_api_client_params)
    return RedirectResponse(kinde_client.get_register_url())

@router.get("/kinde_callback")
def callback(request: Request):
    print("\n=== Callback Debug ===")
    print(f"[DEBUG] Callback router object: {id(router)}")
    print(f"[DEBUG] Callback routes: {[route.path for route in router.routes]}")
    print(f"[DEBUG] Current URL path: {request.url.path}")
    
    kinde_client = KindeApiClient(**kinde_api_client_params)
    kinde_client.fetch_token(authorization_response=str(request.url))
    user = kinde_client.get_user_details()
    request.session["user_id"] = user.get("id")
    user_clients[user.get("id")] = kinde_client
    
    print("[DEBUG] Attempting redirect to '/'")
    print("=== End Callback Debug ===\n")
    return RedirectResponse("/")

@router.get("/logout")
def logout(request: Request):
    user_id = request.session.get("user_id")
    if user_id in user_clients:
        kinde_client = user_clients[user_id]
        logout_url = kinde_client.logout(redirect_to=settings.logout_redirect_url)
        del user_clients[user_id]
        request.session.pop("user_id", None)
        return RedirectResponse(logout_url)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated"
    )