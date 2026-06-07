"""Input validation utilities"""

import re
from typing import Optional
from utils.logger import get_logger

logger = get_logger(__name__)


class InputValidator:
    """Input validation functions"""

    # Patterns
    HOSTNAME_PATTERN = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")
    USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{3,32}$")
    DOMAIN_PATTERN = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$")
    PORT_PATTERN = re.compile(r"^[1-9][0-9]{0,4}$")

    @staticmethod
    def validate_hostname(hostname: str) -> bool:
        """Validate hostname

        Args:
            hostname: Hostname to validate

        Returns:
            True if valid
        """
        if not hostname or len(hostname) > 253:
            return False
        return bool(InputValidator.HOSTNAME_PATTERN.match(hostname))

    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username

        Args:
            username: Username to validate

        Returns:
            True if valid
        """
        if not username:
            return False
        return bool(InputValidator.USERNAME_PATTERN.match(username))

    @staticmethod
    def validate_port(port: int) -> bool:
        """Validate port number

        Args:
            port: Port number to validate

        Returns:
            True if valid
        """
        return 1 <= port <= 65535

    @staticmethod
    def validate_container_name(name: str) -> bool:
        """Validate container name

        Args:
            name: Container name to validate

        Returns:
            True if valid
        """
        if not name or len(name) > 63:
            return False
        return bool(re.match(r"^[a-zA-Z0-9_.-]+$", name))

    @staticmethod
    def sanitize_input(data: str, max_length: int = 1000) -> str:
        """Sanitize user input

        Args:
            data: Data to sanitize
            max_length: Maximum length

        Returns:
            Sanitized data
        """
        if not data:
            return ""

        # Truncate
        data = data[:max_length]

        # Remove null bytes
        data = data.replace("\x00", "")

        return data.strip()
