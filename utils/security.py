"""Security utilities"""

import secrets
import bcrypt
from cryptography.fernet import Fernet
from typing import Optional
from config import config
from utils.logger import get_logger

logger = get_logger(__name__)


class EncryptionManager:
    """Data encryption and decryption"""

    def __init__(self, key: Optional[str] = None):
        """Initialize encryption manager

        Args:
            key: Encryption key (base64 encoded)
        """
        if not key:
            key = config.ENCRYPTION_KEY

        try:
            self.cipher = Fernet(key.encode())
        except Exception as e:
            logger.error(f"Failed to initialize encryption: {e}")
            raise

    def encrypt(self, data: str) -> str:
        """Encrypt data

        Args:
            data: Data to encrypt

        Returns:
            Encrypted data (base64 encoded)
        """
        try:
            encrypted = self.cipher.encrypt(data.encode())
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data

        Args:
            encrypted_data: Encrypted data (base64 encoded)

        Returns:
            Decrypted data
        """
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise


class PasswordManager:
    """Password hashing and verification"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password

        Args:
            password: Password to hash

        Returns:
            Hashed password
        """
        try:
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode(), salt)
            return hashed.decode()
        except Exception as e:
            logger.error(f"Password hashing failed: {e}")
            raise

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password

        Args:
            password: Password to verify
            hashed: Hashed password

        Returns:
            True if password matches
        """
        try:
            return bcrypt.checkpw(password.encode(), hashed.encode())
        except Exception as e:
            logger.error(f"Password verification failed: {e}")
            return False


class TokenGenerator:
    """API token generation"""

    @staticmethod
    def generate_api_key(length: Optional[int] = None) -> str:
        """Generate API key

        Args:
            length: Key length (default from config)

        Returns:
            API key
        """
        if not length:
            length = config.API_KEY_LENGTH

        return secrets.token_hex(length // 2)

    @staticmethod
    def generate_session_token() -> str:
        """Generate session token

        Returns:
            Session token
        """
        return secrets.token_urlsafe(32)
