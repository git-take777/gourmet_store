from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel
from app.database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    """ユーザーモデル"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # リレーションシップ
    api_keys = relationship("ApiKey", back_populates="user")
    permissions = relationship("Permission", back_populates="user")

    @property
    def password_hash(self):
        raise AttributeError('password is not a readable attribute')

    def set_password(self, password):
        """パスワードをハッシュ化して保存"""
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password):
        """パスワードの検証"""
        return pwd_context.verify(password, self.hashed_password)

class ApiKey(Base):
    """APIキーモデル"""
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

    # リレーションシップ
    user = relationship("User", back_populates="api_keys")

class Permission(Base):
    """権限モデル"""
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resource = Column(String)  # リソース名（例: "effects", "users"）
    action = Column(String)    # アクション（例: "read", "write", "delete"）
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # リレーションシップ
    user = relationship("User", back_populates="permissions")

# Pydanticモデル（APIレスポンス用）
class UserBase(BaseModel):
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True