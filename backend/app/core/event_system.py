from typing import Dict, List, Callable, Any
from dataclasses import dataclass
import logging
import asyncio
from datetime import datetime

# ロガーの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Event:
    """イベントデータを表すクラス"""
    type: str
    data: Dict[str, Any]
    timestamp: datetime = datetime.now()

class EventSystem:
    """イベント管理システム
    
    イベントの登録、処理、エフェクトの発動を管理するシステム
    """
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self._active = True
        self._event_queue = asyncio.Queue()
        
    def register_handler(self, event_type: str, handler: Callable) -> None:
        """イベントハンドラーを登録する
        
        Args:
            event_type (str): イベントタイプ
            handler (Callable): ハンドラー関数
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)
            logger.info(f"Registered handler for event type: {event_type}")

    async def process_event(self, event: Event) -> None:
        """イベントを処理する
        
        Args:
            event (Event): 処理するイベント
        """
        try:
            if event.type in self._handlers:
                handlers = self._handlers[event.type]
                for handler in handlers:
                    try:
                        await asyncio.create_task(self._execute_handler(handler, event))
                    except Exception as e:
                        logger.error(f"Error executing handler: {e}")
            else:
                logger.warning(f"No handlers registered for event type: {event.type}")
                
        except Exception as e:
            logger.error(f"Error processing event: {e}")

    async def _execute_handler(self, handler: Callable, event: Event) -> None:
        """ハンドラーを実行する
        
        Args:
            handler (Callable): 実行するハンドラー
            event (Event): イベントデータ
        """
        try:
            if asyncio.iscoroutinefunction(handler):
                await handler(event)
            else:
                handler(event)
        except Exception as e:
            logger.error(f"Handler execution error: {e}")

    async def trigger_effect(self, effect_type: str, parameters: Dict[str, Any]) -> None:
        """エフェクトを発動する
        
        Args:
            effect_type (str): エフェクトタイプ
            parameters (Dict[str, Any]): エフェクトのパラメータ
        """
        event = Event(
            type=effect_type,
            data={
                "parameters": parameters,
                "triggered_at": datetime.now().isoformat()
            }
        )
        
        await self._event_queue.put(event)
        await self.process_event(event)

    async def start(self) -> None:
        """イベントシステムを開始する"""
        self._active = True
        while self._active:
            try:
                event = await self._event_queue.get()
                await self.process_event(event)
            except Exception as e:
                logger.error(f"Error in event processing loop: {e}")

    async def stop(self) -> None:
        """イベントシステムを停止する"""
        self._active = False
        logger.info("Event system stopped")

# シングルトンインスタンスの作成
event_system = EventSystem()

async def example_handler(event: Event):
    print(f"Processing event: {event.type}")

# ハンドラーの登録
await event_system.register_handler("effect_activated", example_handler)

# エフェクトの発動
await event_system.trigger_effect("effect_activated", {
    "color": "blue",
    "duration": 5,
    "intensity": 0.8
})