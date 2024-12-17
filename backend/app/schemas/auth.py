from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ApiKeyCreate(BaseModel):
    """APIキー作成のためのスキーマ"""
    name: str = Field(..., description="APIキーの名前", min_length=1, max_length=100)
    expires_at: Optional[datetime] = Field(None, description="APIキーの有効期限")
    scopes: List[str] = Field(default=[], description="APIキーのスコープ")

    class Config:
        schema_extra = {
            "example": {
                "name": "Production API Key",
                "expires_at": "2024-12-31T23:59:59",
                "scopes": ["read:effects", "write:effects"]
            }
        }

class TokenValidation(BaseModel):
    """トークン検証のためのスキーマ"""
    token: str = Field(..., description="検証するトークン")
    token_type: str = Field(
        default="bearer",
        description="トークンタイプ",
        regex="^(bearer|api_key)$"
    )

    class Config:
        schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIs...",
                "token_type": "bearer"
            }
        }

class AuthResponse(BaseModel):
    """認証レスポンスのスキーマ"""
    access_token: str = Field(..., description="アクセストークン")
    token_type: str = Field(default="bearer", description="トークンタイプ")
    expires_in: int = Field(..., description="トークンの有効期間（秒）")
    refresh_token: Optional[str] = Field(None, description="リフレッシュトークン")
    scope: Optional[str] = Field(None, description="付与されたスコープ")

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIs...",
                "token_type": "bearer",
                "expires_in": 3600,
                "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
                "scope": "read:effects write:effects"
            }
        }

class TokenPayload(BaseModel):
    """トークンペイロードのスキーマ"""
    sub: str = Field(..., description="トークンの対象者（ユーザーID等）")
    exp: int = Field(..., description="有効期限（UNIX時間）")
    scopes: List[str] = Field(default=[], description="付与されたスコープのリスト")
    iat: Optional[int] = Field(None, description="トークン発行時刻")
    jti: Optional[str] = Field(None, description="トークンの一意識別子")

    class Config:
        schema_extra = {
            "example": {
                "sub": "user_123",
                "exp": 1671217200,
                "scopes": ["read:effects", "write:effects"],
                "iat": 1671213600,
                "jti": "unique-token-id-123"
            }
        }