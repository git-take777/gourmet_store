from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from app.services.auth_service import AuthService
from app.schemas.auth import (
    UserCreate,
    ApiKey,
    ValidationResult,
    Message
)
from app.core.dependencies import get_auth_service

router = APIRouter(prefix="/auth", tags=["authentication"])

class AuthController:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    async def generate_api_key(self, user_data: UserCreate) -> ApiKey:
        """
        新しいAPIキーを生成する
        
        Args:
            user_data: ユーザー作成データ
            
        Returns:
            生成されたAPIキー情報
            
        Raises:
            HTTPException: ユーザー作成に失敗した場合
        """
        try:
            return await self.auth_service.create_api_key(user_data)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to generate API key: {str(e)}"
            )

    async def validate_token(self, token: str) -> ValidationResult:
        """
        トークンの有効性を検証する
        
        Args:
            token: 検証対象のトークン
            
        Returns:
            トークンの検証結果
            
        Raises:
            HTTPException: トークンが無効な場合
        """
        try:
            return await self.auth_service.validate_token(token)
        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail=f"Invalid token: {str(e)}"
            )

    async def revoke_token(self, token: str) -> Message:
        """
        トークンを無効化する
        
        Args:
            token: 無効化対象のトークン
            
        Returns:
            処理結果メッセージ
            
        Raises:
            HTTPException: トークンの無効化に失敗した場合
        """
        try:
            return await self.auth_service.revoke_token(token)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to revoke token: {str(e)}"
            )

@router.post("/api-key", response_model=ApiKey)
async def generate_api_key(
    user_data: UserCreate,
    auth_controller: AuthController = Depends(lambda: AuthController(get_auth_service()))
):
    """APIキー生成エンドポイント"""
    return await auth_controller.generate_api_key(user_data)

@router.post("/validate", response_model=ValidationResult)
async def validate_token(
    token: str,
    auth_controller: AuthController = Depends(lambda: AuthController(get_auth_service()))
):
    """トークン検証エンドポイント"""
    return await auth_controller.validate_token(token)

@router.delete("/revoke", response_model=Message)
async def revoke_token(
    token: str,
    auth_controller: AuthController = Depends(lambda: AuthController(get_auth_service()))
):
    """トークン無効化エンドポイント"""
    return await auth_controller.revoke_token(token)