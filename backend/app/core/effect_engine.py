from typing import Dict, Any, Optional
import random
import logging
from dataclasses import dataclass

# エフェクトのパラメータを定義するデータクラス
@dataclass
class EffectParameters:
    color: str
    duration: float
    intensity: float

class EffectEngine:
    """
    エフェクト生成エンジン
    様々な視覚・音響効果を生成・管理するためのクラス
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # デフォルトのエフェクトパラメータ
        self.default_parameters = {
            'particle': EffectParameters(color='#FFFFFF', duration=1.0, intensity=1.0),
            'sound': EffectParameters(color='#000000', duration=2.0, intensity=0.8),
            'light': EffectParameters(color='#FFFF00', duration=1.5, intensity=0.9)
        }

    def create_particle_effect(self, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        パーティクルエフェクトを生成する
        
        Args:
            parameters: エフェクトのパラメータ（オプション）
            
        Returns:
            生成されたパーティクルエフェクトの情報
        """
        try:
            params = self._merge_parameters('particle', parameters)
            effect = {
                'type': 'particle',
                'id': self._generate_effect_id(),
                'parameters': {
                    'color': params.color,
                    'duration': params.duration,
                    'intensity': params.intensity,
                    'particles_count': random.randint(10, 50)
                }
            }
            self.logger.info(f"Created particle effect: {effect['id']}")
            return effect
        except Exception as e:
            self.logger.error(f"Failed to create particle effect: {str(e)}")
            raise

    def create_sound_effect(self, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        サウンドエフェクトを生成する
        
        Args:
            parameters: エフェクトのパラメータ（オプション）
            
        Returns:
            生成されたサウンドエフェクトの情報
        """
        try:
            params = self._merge_parameters('sound', parameters)
            effect = {
                'type': 'sound',
                'id': self._generate_effect_id(),
                'parameters': {
                    'volume': params.intensity,
                    'duration': params.duration,
                    'frequency': random.uniform(200, 2000)
                }
            }
            self.logger.info(f"Created sound effect: {effect['id']}")
            return effect
        except Exception as e:
            self.logger.error(f"Failed to create sound effect: {str(e)}")
            raise

    def create_light_effect(self, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        光エフェクトを生成する
        
        Args:
            parameters: エフェクトのパラメータ（オプション）
            
        Returns:
            生成された光エフェクトの情報
        """
        try:
            params = self._merge_parameters('light', parameters)
            effect = {
                'type': 'light',
                'id': self._generate_effect_id(),
                'parameters': {
                    'color': params.color,
                    'intensity': params.intensity,
                    'duration': params.duration,
                    'radius': random.uniform(1.0, 5.0)
                }
            }
            self.logger.info(f"Created light effect: {effect['id']}")
            return effect
        except Exception as e:
            self.logger.error(f"Failed to create light effect: {str(e)}")
            raise

    def _generate_effect_id(self) -> str:
        """
        ユニークなエフェクトIDを生成する
        """
        return f"effect_{random.randint(1000, 9999)}_{random.randint(1000, 9999)}"

    def _merge_parameters(self, effect_type: str, custom_params: Optional[Dict[str, Any]] = None) -> EffectParameters:
        """
        デフォルトパラメータとカスタムパラメータをマージする
        
        Args:
            effect_type: エフェクトタイプ
            custom_params: カスタムパラメータ
            
        Returns:
            マージされたパラメータ
        """
        default = self.default_parameters[effect_type]
        if not custom_params:
            return default

        return EffectParameters(
            color=custom_params.get('color', default.color),
            duration=custom_params.get('duration', default.duration),
            intensity=custom_params.get('intensity', default.intensity)
        )