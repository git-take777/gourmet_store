from fastapi import APIRouter
from typing import Dict, List, Optional
from pydantic import BaseModel
from core.event_system import EventSystem
from services.trigger_service import TriggerService

router = APIRouter()

class TriggerConfig(BaseModel):
    """トリガー設定を管理するクラス"""
    event_type: str
    condition: Dict
    action: Dict
    priority: Optional[int] = 0
    is_active: bool = True
    description: Optional[str] = None

class EventTriggerSystem:
    def __init__(self):
        self.event_system = EventSystem()
        self.trigger_service = TriggerService()
        self._registered_event_types: List[str] = []

    async def register_event_types(self) -> None:
        """
        システムで使用される基本イベントタイプを登録
        """
        basic_event_types = [
            "effect_created",
            "effect_updated",
            "effect_deleted",
            "system_alert",
            "user_action"
        ]
        
        for event_type in basic_event_types:
            if event_type not in self._registered_event_types:
                await self.event_system.register_event_type(event_type)
                self._registered_event_types.append(event_type)

    async def setup_listeners(self) -> None:
        """
        イベントリスナーの設定と初期化
        """
        await self.trigger_service.setup_default_listeners()
        
        # システムアラート用のグローバルリスナーを設定
        async def global_system_monitor(event_data: Dict):
            if event_data.get("severity") == "critical":
                # クリティカルイベントの処理
                await self.trigger_service.handle_critical_event(event_data)
        
        await self.event_system.add_listener("system_alert", global_system_monitor)

async def initialize_triggers() -> None:
    """
    トリガーシステムの初期化とセットアップを行う
    """
    trigger_system = EventTriggerSystem()
    
    # イベントタイプの登録
    await trigger_system.register_event_types()
    
    # リスナーのセットアップ
    await trigger_system.setup_listeners()
    
    # トリガーサービスの初期化
    await trigger_system.trigger_service.initialize()

# APIルートの設定
@router.post("/triggers")
async def create_trigger(trigger_config: TriggerConfig):
    """新しいトリガーを作成"""
    return await TriggerService().create_trigger(trigger_config)

@router.get("/triggers")
async def get_triggers():
    """登録されているトリガーの一覧を取得"""
    return await TriggerService().get_all_triggers()

@router.get("/triggers/{trigger_id}")
async def get_trigger(trigger_id: str):
    """特定のトリガーの詳細を取得"""
    return await TriggerService().get_trigger(trigger_id)

@router.delete("/triggers/{trigger_id}")
async def delete_trigger(trigger_id: str):
    """トリガーを削除"""
    return await TriggerService().delete_trigger(trigger_id)