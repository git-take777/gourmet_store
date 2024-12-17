from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from typing import Optional, Dict, Any
import secrets
from fastapi import Request, HTTPException
import hashlib
from cryptography.fernet import Fernet

class SecurityManager:
    def __init__(self):
        # パスワードハッシュ化のためのコンテキスト
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # JWT設定
        self.SECRET_KEY = secrets.token_urlsafe(32)
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        
        # 暗号化キーの生成
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)

    async def validate_request(self, request: Request) -> bool:
        """
        リクエストの検証を行う
        
        Args:
            request: FastAPIのリクエストオブジェクト
            
        Returns:
            bool: 検証結果
        """
        try:
            # ヘッダーの検証
            if not request.headers.get("Authorization"):
                raise HTTPException(status_code=401, detail="Authorization header missing")

            # トークンの検証
            token = request.headers["Authorization"].split(" ")[1]
            self.verify_token(token)

            # リクエスト元IPの検証
            client_ip = request.client.host
            if not self.is_allowed_ip(client_ip):
                raise HTTPException(status_code=403, detail="IP not allowed")

            return True

        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))

    def encrypt_data(self, data: str) -> str:
        """
        データの暗号化を行う
        
        Args:
            data: 暗号化する文字列
            
        Returns:
            str: 暗号化されたデータ
        """
        try:
            # データをバイト列に変換して暗号化
            encrypted_data = self.cipher_suite.encrypt(data.encode())
            return encrypted_data.decode()
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")

    def decrypt_data(self, encrypted_data: str) -> str:
        """
        暗号化されたデータの復号化を行う
        
        Args:
            encrypted_data: 暗号化されたデータ
            
        Returns:
            str: 復号化されたデータ
        """
        try:
            decrypted_data = self.cipher_suite.decrypt(encrypted_data.encode())
            return decrypted_data.decode()
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")

    def generate_token(self, data: Dict[str, Any]) -> str:
        """
        JWTトークンの生成
        
        Args:
            data: トークンに含めるデータ
            
        Returns:
            str: 生成されたJWTトークン
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(
            to_encode,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM
        )
        return encoded_jwt

    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        トークンの検証
        
        Args:
            token: 検証するトークン
            
        Returns:
            Dict[str, Any]: デコードされたトークンデータ
        """
        try:
            decoded_token = jwt.decode(
                token,
                self.SECRET_KEY,
                algorithms=[self.ALGORITHM]
            )
            return decoded_token
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def is_allowed_ip(self, ip: str) -> bool:
        """
        IPアドレスのホワイトリスト検証
        
        Args:
            ip: 検証するIPアドレス
            
        Returns:
            bool: 検証結果
        """
        # 実際の実装ではホワイトリストを設定
        allowed_ips = ["127.0.0.1", "localhost"]
        return ip in allowed_ips

# セキュリティマネージャーのインスタンスを作成
security_manager = SecurityManager()