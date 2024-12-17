from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from enum import Enum as PyEnum
from typing import Optional, Dict, Any

from app.database import Base

class TriggerType(PyEnum):
    """トリガーの種類を定義する列挙型"""
    TIME = "time"
    EVENT = "event"
    CONDITION = "condition"

class ActionType(PyEnum):
    """アクションの種類を定義する列挙型"""
    EFFECT = "effect"
    NOTIFICATION = "notification"
    API_CALL = "api_call"

class Trigger(Base):
    """トリガーのメインモデル"""
    __tablename__ = "triggers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    type = Column(Enum(TriggerType), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # リレーションシップ
    conditions = relationship("EventCondition", back_populates="trigger")
    actions = relationship("TriggerAction", back_populates="trigger")

    def to_dict(self) -> Dict[str, Any]:
        """トリガーオブジェクトを辞書に変換"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type.value,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class EventCondition(Base):
    """トリガー条件のモデル"""
    __tablename__ = "event_conditions"

    id = Column(Integer, primary_key=True, index=True)
    trigger_id = Column(Integer, ForeignKey("triggers.id", ondelete="CASCADE"))
    condition_type = Column(String(50), nullable=False)
    parameters = Column(JSON, nullable=False)  # 条件のパラメータをJSON形式で保存
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # リレーションシップ
    trigger = relationship("Trigger", back_populates="conditions")

    def to_dict(self) -> Dict[str, Any]:
        """条件オブジェクトを辞書に変換"""
        return {
            "id": self.id,
            "trigger_id": self.trigger_id,
            "condition_type": self.condition_type,
            "parameters": self.parameters,
            "created_at": self.created_at
        }

class TriggerAction(Base):
    """トリガーアクションのモデル"""
    __tablename__ = "trigger_actions"

    id = Column(Integer, primary_key=True, index=True)
    trigger_id = Column(Integer, ForeignKey("triggers.id", ondelete="CASCADE"))
    action_type = Column(Enum(ActionType), nullable=False)
    parameters = Column(JSON, nullable=False)  # アクションのパラメータをJSON形式で保存
    order = Column(Integer, default=0)  # アクションの実行順序
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # リレーションシップ
    trigger = relationship("Trigger", back_populates="actions")

    def to_dict(self) -> Dict[str, Any]:
        """アクションオブジェクトを辞書に変換"""
        return {
            "id": self.id,
            "trigger_id": self.trigger_id,
            "action_type": self.action_type.value,
            "parameters": self.parameters,
            "order": self.order,
            "created_at": self.created_at
        }