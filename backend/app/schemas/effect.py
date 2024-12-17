from pydantic import BaseModel, Field
from typing import Optional, Dict

class EffectBase(BaseModel):
    """エフェクトの基本スキーマ"""
    name: str = Field(..., description="エフェクトの名前", min_length=1, max_length=100)
    type: str = Field(..., description="エフェクトのタイプ")
    parameters: Dict[str, any] = Field(
        ...,
        description="エフェクトのパラメータ",
        example={
            "color": "#FF0000",
            "duration": 1000,
            "intensity": 0.8
        }
    )

class EffectCreate(EffectBase):
    """エフェクト作成用スキーマ"""
    pass

class EffectUpdate(BaseModel):
    """エフェクト更新用スキーマ"""
    name: Optional[str] = Field(None, description="エフェクトの名前", min_length=1, max_length=100)
    type: Optional[str] = Field(None, description="エフェクトのタイプ")
    parameters: Optional[Dict[str, any]] = Field(
        None,
        description="エフェクトのパラメータ"
    )

    class Config:
        """部分的な更新を許可する設定"""
        extra = "allow"

class EffectResponse(EffectBase):
    """エフェクトレスポンス用スキーマ"""
    id: str = Field(..., description="エフェクトのユニークID")

    class Config:
        """Pydanticの設定"""
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Fade Effect",
                "type": "color_fade",
                "parameters": {
                    "color": "#FF0000",
                    "duration": 1000,
                    "intensity": 0.8
                }
            }
        }