"""Configuration Management for Hexlore VPS Bot"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


class Config:
    """Base configuration class"""

    # Project Structure
    BASE_DIR = Path(__file__).parent
    LOGS_DIR = BASE_DIR / "logs"
    BACKUPS_DIR = BASE_DIR / "backups"
    DATA_DIR = BASE_DIR / "data"

    # Ensure directories exist
    LOGS_DIR.mkdir(exist_ok=True)
    BACKUPS_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)

    # =====================================================
    # DISCORD BOT SETTINGS
    # =====================================================
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
    COMMAND_PREFIX: str = os.getenv("COMMAND_PREFIX", "!")
    OWNER_ID: int = int(os.getenv("OWNER_ID", "0"))

    # =====================================================
    # DATABASE SETTINGS
    # =====================================================
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "hexlore_vps")

    # =====================================================
    # DOCKER SETTINGS
    # =====================================================
    DOCKER_SOCKET: str = os.getenv("DOCKER_SOCKET", "/var/run/docker.sock")
    DOCKER_REGISTRY: str = os.getenv("DOCKER_REGISTRY", "docker.io")
    DOCKER_API_BASE_URL: str = os.getenv(
        "DOCKER_API_BASE_URL", "unix:///var/run/docker.sock"
    )

    # =====================================================
    # API SETTINGS
    # =====================================================
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_KEY_LENGTH: int = int(os.getenv("API_KEY_LENGTH", "32"))

    # =====================================================
    # SECURITY SETTINGS
    # =====================================================
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", "")
    SESSION_TIMEOUT: int = int(os.getenv("SESSION_TIMEOUT", "3600"))
    RATE_LIMIT_CALLS: int = int(os.getenv("RATE_LIMIT_CALLS", "10"))
    RATE_LIMIT_PERIOD: int = int(os.getenv("RATE_LIMIT_PERIOD", "60"))
    MAX_LOGIN_ATTEMPTS: int = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))

    # =====================================================
    # LOGGING SETTINGS
    # =====================================================
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", str(LOGS_DIR / "bot.log"))
    LOG_FILE_SIZE: int = int(os.getenv("LOG_FILE_SIZE", "10")) * 1024 * 1024
    LOG_BACKUP_COUNT: int = int(os.getenv("LOG_BACKUP_COUNT", "5"))

    # =====================================================
    # FEATURE FLAGS
    # =====================================================
    ENABLE_PREMIUM: bool = os.getenv("ENABLE_PREMIUM", "true").lower() == "true"
    ENABLE_BILLING: bool = os.getenv("ENABLE_BILLING", "true").lower() == "true"
    ENABLE_AUTO_BACKUPS: bool = (
        os.getenv("ENABLE_AUTO_BACKUPS", "true").lower() == "true"
    )
    ENABLE_HEALTH_CHECKS: bool = (
        os.getenv("ENABLE_HEALTH_CHECKS", "true").lower() == "true"
    )

    # =====================================================
    # VPS LIMITS
    # =====================================================
    MAX_VPS_PER_USER: int = int(os.getenv("MAX_VPS_PER_USER", "5"))
    MAX_VPS_PER_USER_PREMIUM: int = int(os.getenv("MAX_VPS_PER_USER_PREMIUM", "20"))
    DEFAULT_RAM_MB: int = int(os.getenv("DEFAULT_RAM_MB", "512"))
    DEFAULT_CPU_SHARES: int = int(os.getenv("DEFAULT_CPU_SHARES", "1024"))
    DEFAULT_DISK_GB: int = int(os.getenv("DEFAULT_DISK_GB", "10"))

    # =====================================================
    # NODE SETTINGS
    # =====================================================
    DEFAULT_NODE_HOST: str = os.getenv("DEFAULT_NODE_HOST", "localhost")
    DEFAULT_NODE_PORT: int = int(os.getenv("DEFAULT_NODE_PORT", "2375"))
    NODE_HEALTH_CHECK_INTERVAL: int = int(
        os.getenv("NODE_HEALTH_CHECK_INTERVAL", "300")
    )

    # =====================================================
    # BACKUP SETTINGS
    # =====================================================
    BACKUP_STORAGE_PATH: str = os.getenv("BACKUP_STORAGE_PATH", str(BACKUPS_DIR))
    AUTO_BACKUP_INTERVAL: int = int(os.getenv("AUTO_BACKUP_INTERVAL", "24"))
    BACKUP_RETENTION_DAYS: int = int(os.getenv("BACKUP_RETENTION_DAYS", "30"))

    # =====================================================
    # BILLING SETTINGS
    # =====================================================
    CURRENCY: str = os.getenv("CURRENCY", "USD")
    PRICE_PER_GB_MONTH: float = float(os.getenv("PRICE_PER_GB_MONTH", "0.50"))
    BILLING_CYCLE_DAYS: int = int(os.getenv("BILLING_CYCLE_DAYS", "30"))

    # =====================================================
    # MAINTENANCE
    # =====================================================
    MAINTENANCE_MODE: bool = os.getenv("MAINTENANCE_MODE", "false").lower() == "true"
    MAINTENANCE_MESSAGE: str = os.getenv(
        "MAINTENANCE_MESSAGE", "Bot is under maintenance. Please try again later."
    )

    @classmethod
    def validate(cls) -> list[str]:
        """Validate configuration and return list of errors"""
        errors = []

        if not cls.DISCORD_TOKEN:
            errors.append("DISCORD_TOKEN is not set")

        if not cls.ENCRYPTION_KEY:
            errors.append("ENCRYPTION_KEY is not set")

        if not cls.OWNER_ID:
            errors.append("OWNER_ID is not set")

        if not Path(cls.DOCKER_SOCKET).exists():
            errors.append(f"Docker socket not found at {cls.DOCKER_SOCKET}")

        return errors


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    LOG_LEVEL = "INFO"


class TestingConfig(Config):
    """Testing configuration"""

    DEBUG = True
    MONGO_DB_NAME = "hexlore_vps_test"
    TESTING = True


def get_config() -> Config:
    """Get configuration based on environment"""
    env = os.getenv("ENV", "development").lower()

    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()


# Default config instance
config = get_config()
