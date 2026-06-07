"""Helper utility functions"""

import math
from typing import Optional, Tuple
from datetime import datetime, timedelta


class FormatHelper:
    """Formatting helper functions"""

    @staticmethod
    def format_bytes(bytes_: int) -> str:
        """Format bytes to human readable format

        Args:
            bytes_: Number of bytes

        Returns:
            Formatted string
        """
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if bytes_ < 1024.0:
                return f"{bytes_:.2f} {unit}"
            bytes_ /= 1024.0
        return f"{bytes_:.2f} PB"

    @staticmethod
    def format_uptime(seconds: int) -> str:
        """Format uptime in human readable format

        Args:
            seconds: Uptime in seconds

        Returns:
            Formatted string
        """
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"

    @staticmethod
    def format_percentage(value: float, total: float) -> str:
        """Format percentage

        Args:
            value: Current value
            total: Total value

        Returns:
            Formatted percentage string
        """
        if total == 0:
            return "0.0%"
        percentage = (value / total) * 100
        return f"{percentage:.1f}%"

    @staticmethod
    def format_progress_bar(value: float, total: float, width: int = 20) -> str:
        """Create a progress bar

        Args:
            value: Current value
            total: Total value
            width: Bar width in characters

        Returns:
            Progress bar string
        """
        percentage = value / total if total > 0 else 0
        filled = int(width * percentage)
        bar = "█" * filled + "░" * (width - filled)
        return f"{bar} {percentage*100:.1f}%"


class TimeHelper:
    """Time helper functions"""

    @staticmethod
    def get_relative_time(dt: datetime) -> str:
        """Get relative time (e.g., "5 minutes ago")

        Args:
            dt: Datetime object

        Returns:
            Relative time string
        """
        now = datetime.utcnow()
        delta = now - dt

        if delta.days > 0:
            return f"{delta.days}d ago"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            return f"{hours}h ago"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"{minutes}m ago"
        else:
            return "just now"

    @staticmethod
    def get_remaining_time(end_time: datetime) -> str:
        """Get remaining time until deadline

        Args:
            end_time: End time datetime

        Returns:
            Remaining time string
        """
        now = datetime.utcnow()
        if end_time <= now:
            return "Expired"

        delta = end_time - now

        if delta.days > 0:
            return f"{delta.days}d remaining"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            return f"{hours}h remaining"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"{minutes}m remaining"
        else:
            return f"{delta.seconds}s remaining"
