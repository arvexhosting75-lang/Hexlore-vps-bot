"""MongoDB Models and Schemas"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class VPSStatus(str, Enum):
    """VPS status enum"""

    RUNNING = "running"
    STOPPED = "stopped"
    SUSPENDED = "suspended"
    ERROR = "error"
    CREATING = "creating"
    DELETING = "deleting"


class UserRole(str, Enum):
    """User role enum"""

    USER = "user"
    PREMIUM = "premium"
    MODERATOR = "moderator"
    ADMIN = "admin"
    OWNER = "owner"


class UserModel:
    """User model"""

    COLLECTION_NAME = "users"

    @staticmethod
    def schema():
        return {
            "user_id": int,
            "username": str,
            "email": Optional[str],
            "role": UserRole.USER.value,
            "premium": False,
            "balance": 0.0,
            "api_keys": [],
            "blacklisted": False,
            "created_at": datetime,
            "updated_at": datetime,
            "last_login": Optional[datetime],
            "vps_count": 0,
            "total_spent": 0.0,
            "settings": {
                "notifications": True,
                "auto_backup": True,
                "language": "en",
            },
        }


class ContainerModel:
    """Container/VPS model"""

    COLLECTION_NAME = "containers"

    @staticmethod
    def schema():
        return {
            "container_id": str,
            "user_id": int,
            "name": str,
            "hostname": str,
            "status": VPSStatus.STOPPED.value,
            "image": str,
            "node_id": str,
            "resources": {
                "ram_mb": 512,
                "cpu_shares": 1024,
                "disk_gb": 10,
            },
            "ports": [],
            "volumes": [],
            "networks": [],
            "ssh_enabled": True,
            "ssh_port": 22,
            "ssh_password": str,
            "custom_startup": Optional[str],
            "uptime_seconds": 0,
            "created_at": datetime,
            "started_at": Optional[datetime],
            "updated_at": datetime,
            "activity_logs": [],
        }


class BackupModel:
    """Backup model"""

    COLLECTION_NAME = "backups"

    @staticmethod
    def schema():
        return {
            "backup_id": str,
            "container_id": str,
            "user_id": int,
            "backup_path": str,
            "size_mb": 0,
            "created_at": datetime,
            "restored_at": Optional[datetime],
            "automatic": False,
        }


class LogModel:
    """Activity log model"""

    COLLECTION_NAME = "logs"

    @staticmethod
    def schema():
        return {
            "log_id": str,
            "user_id": int,
            "action": str,
            "target": str,
            "result": "success",
            "ip_address": str,
            "user_agent": str,
            "created_at": datetime,
            "details": {},
        }


class SessionModel:
    """Session model"""

    COLLECTION_NAME = "sessions"

    @staticmethod
    def schema():
        return {
            "session_id": str,
            "user_id": int,
            "api_key": str,
            "ip_address": str,
            "created_at": datetime,
            "expires_at": datetime,
            "last_used": datetime,
            "active": True,
        }


class NodeModel:
    """Docker node model"""

    COLLECTION_NAME = "nodes"

    @staticmethod
    def schema():
        return {
            "node_id": str,
            "name": str,
            "host": str,
            "port": 2375,
            "status": "online",
            "containers_count": 0,
            "total_ram_mb": 0,
            "total_cpu_shares": 0,
            "used_ram_mb": 0,
            "used_cpu_shares": 0,
            "created_at": datetime,
            "last_health_check": datetime,
            "active": True,
        }


class BillingModel:
    """Billing model"""

    COLLECTION_NAME = "billing"

    @staticmethod
    def schema():
        return {
            "billing_id": str,
            "user_id": int,
            "container_id": str,
            "amount": 0.0,
            "currency": "USD",
            "period_start": datetime,
            "period_end": datetime,
            "status": "pending",
            "paid_at": Optional[datetime],
            "created_at": datetime,
        }


class PlanModel:
    """Hosting plan model"""

    COLLECTION_NAME = "plans"

    @staticmethod
    def schema():
        return {
            "plan_id": str,
            "name": str,
            "description": str,
            "ram_mb": 512,
            "cpu_shares": 1024,
            "disk_gb": 10,
            "price_monthly": 0.0,
            "features": [],
            "max_containers": 5,
            "active": True,
            "created_at": datetime,
        }
