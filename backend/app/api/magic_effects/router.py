from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.services import effect_service
from app.schemas.effect import (
    Effect,
    EffectCreate,
    EffectUpdate,
    EffectPreset,
    TriggerData,
    EffectResult,
    Message
)
from app.core.minecraft_bridge import MinecraftBridge
from app.core.dependencies import get_minecraft_bridge

router = APIRouter(prefix="/effects", tags=["effects"])

class EffectController:
    def __init__(self, minecraft_bridge: MinecraftBridge = Depends(get_minecraft_bridge)):
        self.minecraft_bridge = minecraft_bridge
        self.effect_service = effect_service.EffectService(minecraft_bridge)

    async def create_effect(self, effect_data: EffectCreate) -> Effect:
        """新しいエフェクトを作成する"""
        try:
            return await self.effect_service.create_effect(effect_data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_presets(self) -> List[EffectPreset]:
        """利用可能なエフェクトプリセットのリストを取得する"""
        return await self.effect_service.get_presets()

    async def trigger_effect(self, effect_id: str, trigger_data: TriggerData) -> EffectResult:
        """指定されたエフェクトを実行する"""
        try:
            return await self.effect_service.trigger_effect(effect_id, trigger_data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except KeyError:
            raise HTTPException(status_code=404, detail="Effect not found")

    async def update_effect(self, effect_id: str, effect_data: EffectUpdate) -> Effect:
        """既存のエフェクトを更新する"""
        try:
            return await self.effect_service.update_effect(effect_id, effect_data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except KeyError:
            raise HTTPException(status_code=404, detail="Effect not found")

    async def delete_effect(self, effect_id: str) -> Message:
        """エフェクトを削除する"""
        try:
            await self.effect_service.delete_effect(effect_id)
            return Message(message=f"Effect {effect_id} successfully deleted")
        except KeyError:
            raise HTTPException(status_code=404, detail="Effect not found")

# ルートハンドラーのインスタンス化
controller = EffectController()

# エンドポイントの定義
@router.post("/create", response_model=Effect)
async def create_effect(effect_data: EffectCreate, controller: EffectController = Depends()):
    return await controller.create_effect(effect_data)

@router.get("/presets", response_model=List[EffectPreset])
async def get_presets(controller: EffectController = Depends()):
    return await controller.get_presets()

@router.post("/trigger", response_model=EffectResult)
async def trigger_effect(effect_id: str, trigger_data: TriggerData, controller: EffectController = Depends()):
    return await controller.trigger_effect(effect_id, trigger_data)

@router.put("/{effect_id}", response_model=Effect)
async def update_effect(effect_id: str, effect_data: EffectUpdate, controller: EffectController = Depends()):
    return await controller.update_effect(effect_id, effect_data)

@router.delete("/{effect_id}", response_model=Message)
async def delete_effect(effect_id: str, controller: EffectController = Depends()):
    return await controller.delete_effect(effect_id)