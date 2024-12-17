from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime
from typing import Dict, Any

class Effect(Base):
    """エフェクトモデル
    
    エフェクトの基本情報を管理するモデル
    """
    __tablename__ = "effects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    description = Column(String(500))
    created_at = Column(Float, default=datetime.utcnow().timestamp)
    updated_at = Column(Float, default=datetime.utcnow().timestamp)
    
    # リレーションシップ
    parameters = relationship("EffectParameter", back_populates="effect", cascade="all, delete-orphan")
    presets = relationship("EffectPreset", back_populates="effect", cascade="all, delete-orphan")

    def to_dict(self) -> Dict[str, Any]:
        """エフェクトをディクショナリ形式で返す"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "parameters": [param.to_dict() for param in self.parameters],
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class EffectPreset(Base):
    """エフェクトプリセットモデル
    
    エフェクトの事前設定を管理するモデル
    """
    __tablename__ = "effect_presets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    effect_id = Column(Integer, ForeignKey("effects.id"), nullable=False)
    settings = Column(JSON, nullable=False)  # プリセットのパラメータ設定をJSON形式で保存
    created_at = Column(Float, default=datetime.utcnow().timestamp)
    
    # リレーションシップ
    effect = relationship("Effect", back_populates="presets")

    def to_dict(self) -> Dict[str, Any]:
        """プリセットをディクショナリ形式で返す"""
        return {
            "id": self.id,
            "name": self.name,
            "effect_id": self.effect_id,
            "settings": self.settings,
            "created_at": self.created_at
        }

class EffectParameter(Base):
    """エフェクトパラメータモデル
    
    エフェクトの各パラメータを管理するモデル
    """
    __tablename__ = "effect_parameters"

    id = Column(Integer, primary_key=True, index=True)
    effect_id = Column(Integer, ForeignKey("effects.id"), nullable=False)
    name = Column(String(50), nullable=False)
    type = Column(String(30), nullable=False)  # number, string, color など
    default_value = Column(String(100))
    min_value = Column(Float)
    max_value = Column(Float)
    unit = Column(String(20))
    
    # リレーションシップ
    effect = relationship("Effect", back_populates="parameters")

    def to_dict(self) -> Dict[str, Any]:
        """パラメータをディクショナリ形式で返す"""
        return {
            "id": self.id,
            "effect_id": self.effect_id,
            "name": self.name,
            "type": self.type,
            "default_value": self.default_value,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "unit": self.unit
        }