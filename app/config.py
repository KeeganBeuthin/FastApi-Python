# app/config.py
from pydantic_settings import BaseSettings
from kinde_sdk.kinde_api_client import GrantType
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    kinde_domain: str
    kinde_client_id: str
    kinde_client_secret: str
    site_url: str = "http://127.0.0.1:8000"
    kinde_callback_url: str = "http://127.0.0.1:8000/api/auth/kinde_callback"
    logout_redirect_url: str = "http://127.0.0.1:8000"
    secret_key: str = "your-secret-key-here"
    code_verifier: str = "your-code-verifier-string-longer-than-43-chars"
    grant_type: GrantType = GrantType.AUTHORIZATION_CODE_WITH_PKCE

    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    return Settings()