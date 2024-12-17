from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class TriggerBase(BaseModel):
    """基本トリガースキーマ"""
    name: str = Field(..., description="トリガーの名前", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="トリガーの説明")
    condition: Dict[str, Any] = Field(..., description="トリガーの条件")
    action_type: str = Field(..., description="トリガーのアクションタイプ")
    enabled: bool = Field(default=True, description="トリガーの有効/無効状態")

class TriggerCreate(TriggerBase):
    """トリガー作成スキーマ"""
    user_id: str = Field(..., description="トリガーを作成するユーザーのID")
    parameters: Optional[Dict[str, Any]] = Field(default={}, description="トリガーのパラメータ")

class TriggerUpdate(BaseModel):
    """トリガー更新スキーマ"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    condition: Optional[Dict[str, Any]] = None
    action_type: Optional[str] = None
    enabled: Optional[bool] = None
    parameters: Optional[Dict[str, Any]] = None

class TriggerResponse(TriggerBase):
    """トリガーレスポンススキーマ"""
    id: str = Field(..., description="トリガーの一意識別子")
    user_id: str = Field(..., description="トリガーの所有者ID")
    created_at: datetime = Field(..., description="トリガーの作成日時")
    updated_at: datetime = Field(..., description="トリガーの最終更新日時")
    parameters: Dict[str, Any] = Field(default={}, description="トリガーのパラメータ")
    last_triggered: Optional[datetime] = Field(None, description="最後にトリガーが実行された日時")

    class Config:
        orm_mode = True