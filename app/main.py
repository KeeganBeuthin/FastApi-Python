from fastapi import FastAPI, Depends
from starlette.middleware.sessions import SessionMiddleware
from .routers import auth, api
from .dependencies import get_kinde_client
from kinde_sdk.kinde_api_client import KindeApiClient
from .config import get_settings

settings = get_settings()

app = FastAPI(title="Kinde FastAPI Demo")
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# Problematic setup - defining route directly on app
@app.get("/")
def read_root(kinde_client: KindeApiClient = Depends(get_kinde_client)):
    print("\n=== Root Endpoint Debug ===")
    print(f"[DEBUG] App router object: {id(app.router)}")
    print(f"[DEBUG] Available routes: {[route.path for route in app.routes]}")
    print("[DEBUG] Root endpoint called (on app)")
    print("=== End Root Endpoint Debug ===\n")
    return {"Hello": "World", "authenticated": True}

# Include routers
app.include_router(auth.router)
app.include_router(api.router)