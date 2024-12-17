from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import json
import logging
from pathlib import Path

from app.core.minecraft_bridge import MinecraftConnection
from app.core.effect_engine import EffectEngine

# ルーターの初期化
router = APIRouter()

class EffectConfig(BaseModel):
    """エフェクト設定を管理するクラス"""
    name: str
    type: str
    parameters: Dict[str, any]
    duration: int = Field(ge=0, le=3600)  # 最大1時間
    intensity: float = Field(ge=0.0, le=1.0)
    is_enabled: bool = True
    
    class Config:
        schema_extra = {
            "example": {
                "name": "sparkle",
                "type": "particle",
                "parameters": {"color": "#FF0000", "speed": 1.0},
                "duration": 60,
                "intensity": 0.5,
                "is_enabled": True
            }
        }

# グローバル変数
effect_engine: Optional[EffectEngine] = None
minecraft_connection: Optional[MinecraftConnection] = None

def load_presets() -> List[EffectConfig]:
    """プリセットエフェクトを読み込む"""
    try:
        preset_path = Path(__file__).parent / "presets" / "effects.json"
        with open(preset_path, "r") as f:
            presets = json.load(f)
        return [EffectConfig(**preset) for preset in presets]
    except Exception as e:
        logging.error(f"Failed to load effect presets: {e}")
        return []

def validate_effect_params(effect: EffectConfig) -> bool:
    """エフェクトパラメータを検証する"""
    try:
        # 基本的なバリデーション
        if effect.duration < 0 or effect.intensity < 0:
            return False
            
        # エフェクトタイプ固有のバリデーション
        if effect.type == "particle":
            if "color" not in effect.parameters:
                return False
        
        return True
    except Exception as e:
        logging.error(f"Effect validation failed: {e}")
        return False

async def initialize_effects():
    """エフェクトシステムを初期化する"""
    global effect_engine
    try:
        effect_engine = EffectEngine()
        presets = load_presets()
        for preset in presets:
            if validate_effect_params(preset):
                await effect_engine.register_effect(preset)
        logging.info("Effect system initialized successfully")
    except Exception as e:
        logging.error(f"Failed to initialize effect system: {e}")
        raise

async def setup_minecraft_connection(host: str = "localhost", port: int = 25565):
    """マインクラフトサーバーとの接続を設定する"""
    global minecraft_connection
    try:
        minecraft_connection = MinecraftConnection(host=host, port=port)
        await minecraft_connection.connect()
        logging.info(f"Successfully connected to Minecraft server at {host}:{port}")
        return minecraft_connection
    except Exception as e:
        logging.error(f"Failed to connect to Minecraft server: {e}")
        raise

# 初期化時に実行される処理
@router.on_event("startup")
async def startup_event():
    await initialize_effects()
    await setup_minecraft_connection()

# クリーンアップ処理
@router.on_event("shutdown")
async def shutdown_event():
    if minecraft_connection:
        await minecraft_connection.disconnect()
    if effect_engine:
        await effect_engine.cleanup()