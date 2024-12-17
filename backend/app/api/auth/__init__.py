from fastapi import APIRouter
from typing import Optional
from pydantic import BaseSettings
from core.security import create_access_token, verify_jwt_token
from core.config import get_settings

# ルーターの初期化
router = APIRouter()

class AuthConfig(BaseSettings):
    """認証設定を管理するクラス"""
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_KEY_NAME: str = "X-API-Key"
    OAUTH_PROVIDERS: dict = {
        "github": {
            "client_id": "",
            "client_secret": "",
            "authorize_url": "https://github.com/login/oauth/authorize",
            "token_url": "https://github.com/login/oauth/access_token"
        }
    }

    class Config:
        env_file = ".env"

def setup_api_keys() -> dict:
    """APIキーの設定を初期化する関数
    
    Returns:
        dict: 設定されたAPIキーの情報
    """
    settings = get_settings()
    api_keys = {
        "enabled": True,
        "key_name": AuthConfig().API_KEY_NAME,
        "keys": settings.API_KEYS if hasattr(settings, 'API_KEYS') else []
    }
    return api_keys

def configure_oauth(provider: str = None) -> dict:
    """OAuth設定を構成する関数
    
    Args:
        provider (str, optional): プロバイダー名. Defaults to None.
    
    Returns:
        dict: OAuth設定情報
    """
    auth_config = AuthConfig()
    if provider and provider in auth_config.OAUTH_PROVIDERS:
        return auth_config.OAUTH_PROVIDERS[provider]
    return auth_config.OAUTH_PROVIDERS

def initialize_auth() -> None:
    """認証システムを初期化する関数"""
    # APIキーの設定
    api_keys = setup_api_keys()
    
    # OAuth設定の初期化
    oauth_config = configure_oauth()
    
    # ルートの登録
    from .endpoints import login, oauth, api_key
    
    # 各エンドポイントをルーターに登録
    router.include_router(login.router, tags=["authentication"])
    router.include_router(oauth.router, prefix="/oauth", tags=["oauth"])
    router.include_router(api_key.router, prefix="/api-keys", tags=["api-keys"])
    
    # 初期化完了のログ
    print("Authentication system initialized successfully")

# 初期化の実行
initialize_auth()