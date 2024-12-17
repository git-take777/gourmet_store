import asyncio
import logging
from typing import Optional, Callable, Dict, Any
from mctools import RCONClient
import websockets
from websockets.exceptions import ConnectionClosed

logger = logging.getLogger(__name__)

class MinecraftConnection:
    """マインクラフトサーバーとの接続を管理するクラス"""
    
    def __init__(self, host: str, port: int, password: str):
        """
        初期化
        
        Args:
            host: マインクラフトサーバーのホスト名
            port: RCONポート
            password: RCONパスワード
        """
        self.host = host
        self.port = port
        self.password = password
        self.rcon_client: Optional[RCONClient] = None
        self.ws_connection = None
        self.event_handlers: Dict[str, Callable] = {}

    async def connect(self) -> bool:
        """
        マインクラフトサーバーに接続
        
        Returns:
            bool: 接続成功の場合True
        """
        try:
            self.rcon_client = RCONClient(self.host, self.port)
            success = self.rcon_client.login(self.password)
            
            if success:
                logger.info(f"Successfully connected to Minecraft server at {self.host}:{self.port}")
                return True
            else:
                logger.error("Failed to connect to Minecraft server")
                return False
                
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            return False

    async def send_effect(self, effect_data: Dict[str, Any]) -> bool:
        """
        エフェクトをマインクラフトサーバーに送信
        
        Args:
            effect_data: エフェクトデータ（type, parameters等を含む）
            
        Returns:
            bool: 送信成功の場合True
        """
        if not self.rcon_client:
            logger.error("Not connected to server")
            return False

        try:
            # エフェクトコマンドの構築
            command = self._build_effect_command(effect_data)
            
            # コマンド実行
            response = self.rcon_client.command(command)
            
            if response:
                logger.info(f"Successfully sent effect: {effect_data['name']}")
                return True
            return False

        except Exception as e:
            logger.error(f"Error sending effect: {str(e)}")
            return False

    async def listen_events(self, event_callback: Callable):
        """
        マインクラフトサーバーからのイベントをリッスン
        
        Args:
            event_callback: イベント受信時のコールバック関数
        """
        try:
            async with websockets.connect(f"ws://{self.host}:8080/events") as websocket:
                self.ws_connection = websocket
                
                while True:
                    try:
                        message = await websocket.recv()
                        await event_callback(message)
                    except ConnectionClosed:
                        logger.warning("WebSocket connection closed")
                        break
                    except Exception as e:
                        logger.error(f"Error in event listener: {str(e)}")
                        continue

        except Exception as e:
            logger.error(f"WebSocket connection error: {str(e)}")

    def _build_effect_command(self, effect_data: Dict[str, Any]) -> str:
        """
        エフェクトコマンドの構築
        
        Args:
            effect_data: エフェクトデータ
            
        Returns:
            str: マインクラフトコマンド文字列
        """
        effect_type = effect_data.get('type', '')
        params = effect_data.get('parameters', {})
        
        # 基本的なエフェクトコマンドを構築
        command = f"/effect give @a {effect_type} "
        
        # パラメータを追加
        duration = params.get('duration', 30)
        intensity = params.get('intensity', 1)
        command += f"{duration} {intensity}"
        
        return command

    async def close(self):
        """接続のクリーンアップ"""
        if self.rcon_client:
            self.rcon_client.stop()
        
        if self.ws_connection:
            await self.ws_connection.close()

async def main():
    mc = MinecraftConnection("localhost", 25575, "password")
    
    if await mc.connect():
        effect = {
            "name": "speed",
            "type": "speed",
            "parameters": {
                "duration": 30,
                "intensity": 2
            }
        }
        
        await mc.send_effect(effect)
        
        # イベントリスニングの例
        async def handle_event(event):
            print(f"Received event: {event}")
            
        await mc.listen_events(handle_event)