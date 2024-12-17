from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.services import trigger_service
from app.schemas.trigger import (
    TriggerCreate,
    TriggerUpdate,
    Trigger,
    Message
)
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/triggers",
    tags=["triggers"]
)

class TriggerController:
    """トリガー制御のハンドラクラス"""
    
    @router.post("/create", response_model=Trigger)
    async def create_trigger(
        trigger_data: TriggerCreate,
        current_user: User = Depends(get_current_user)
    ) -> Trigger:
        """
        新しいトリガーを作成する
        
        Args:
            trigger_data: 作成するトリガーのデータ
            current_user: 現在のログインユーザー
            
        Returns:
            作成されたトリガーオブジェクト
        """
        try:
            trigger = await trigger_service.create_trigger(
                trigger_data=trigger_data,
                user_id=current_user.id
            )
            return trigger
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"トリガーの作成に失敗しました: {str(e)}"
            )

    @router.get("/list", response_model=List[Trigger])
    async def list_triggers(
        current_user: User = Depends(get_current_user)
    ) -> List[Trigger]:
        """
        ユーザーのトリガー一覧を取得する
        
        Args:
            current_user: 現在のログインユーザー
            
        Returns:
            トリガーオブジェクトのリスト
        """
        try:
            triggers = await trigger_service.list_triggers(user_id=current_user.id)
            return triggers
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"トリガー一覧の取得に失敗しました: {str(e)}"
            )

    @router.put("/{trigger_id}", response_model=Trigger)
    async def update_trigger(
        trigger_id: str,
        trigger_data: TriggerUpdate,
        current_user: User = Depends(get_current_user)
    ) -> Trigger:
        """
        既存のトリガーを更新する
        
        Args:
            trigger_id: 更新対象のトリガーID
            trigger_data: 更新するトリガーデータ
            current_user: 現在のログインユーザー
            
        Returns:
            更新されたトリガーオブジェクト
        """
        try:
            trigger = await trigger_service.update_trigger(
                trigger_id=trigger_id,
                trigger_data=trigger_data,
                user_id=current_user.id
            )
            return trigger
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"トリガーの更新に失敗しました: {str(e)}"
            )

    @router.delete("/{trigger_id}", response_model=Message)
    async def delete_trigger(
        trigger_id: str,
        current_user: User = Depends(get_current_user)
    ) -> Message:
        """
        トリガーを削除する
        
        Args:
            trigger_id: 削除対象のトリガーID
            current_user: 現在のログインユーザー
            
        Returns:
            削除完了メッセージ
        """
        try:
            message = await trigger_service.delete_trigger(
                trigger_id=trigger_id,
                user_id=current_user.id
            )
            return message
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"トリガーの削除に失敗しました: {str(e)}"
            )

trigger_controller = TriggerController()