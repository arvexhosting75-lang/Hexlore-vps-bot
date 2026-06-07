"""Custom decorators"""

import time
from functools import wraps
from typing import Callable, Any, Dict
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from config import config
from utils.logger import get_logger

logger = get_logger(__name__)

# Rate limit storage
_rate_limits: Dict[int, list] = {}


def owner_only(func: Callable) -> Callable:
    """Decorator for owner-only commands"""

    @wraps(func)
    async def wrapper(ctx, *args, **kwargs):
        if ctx.author.id != config.OWNER_ID:
            await ctx.send("❌ This command is only available to the bot owner.")
            logger.warning(
                f"Unauthorized access attempt by {ctx.author.id} to {func.__name__}"
            )
            return
        return await func(ctx, *args, **kwargs)

    return wrapper


def admin_only(func: Callable) -> Callable:
    """Decorator for admin-only commands"""

    @wraps(func)
    async def wrapper(ctx, *args, **kwargs):
        if not ctx.author.guild_permissions.administrator and ctx.author.id != config.OWNER_ID:
            await ctx.send("❌ This command requires administrator permissions.")
            logger.warning(
                f"Unauthorized access attempt by {ctx.author.id} to {func.__name__}"
            )
            return
        return await func(ctx, *args, **kwargs)

    return wrapper


def rate_limit(calls: int = None, period: int = None):
    """Rate limiting decorator

    Args:
        calls: Number of calls allowed
        period: Time period in seconds
    """
    if calls is None:
        calls = config.RATE_LIMIT_CALLS
    if period is None:
        period = config.RATE_LIMIT_PERIOD

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(ctx, *args, **kwargs):
            user_id = ctx.author.id

            # Initialize rate limit list
            if user_id not in _rate_limits:
                _rate_limits[user_id] = []

            now = datetime.utcnow()
            # Remove old timestamps
            _rate_limits[user_id] = [
                ts
                for ts in _rate_limits[user_id]
                if now - ts < timedelta(seconds=period)
            ]

            # Check if rate limit exceeded
            if len(_rate_limits[user_id]) >= calls:
                await ctx.send(
                    f"❌ Rate limit exceeded. Try again in {period} seconds."
                )
                logger.warning(f"Rate limit exceeded for user {user_id}")
                return

            # Add current timestamp
            _rate_limits[user_id].append(now)

            return await func(ctx, *args, **kwargs)

        return wrapper

    return decorator


def error_handler(func: Callable) -> Callable:
    """Error handling decorator"""

    @wraps(func)
    async def wrapper(ctx, *args, **kwargs):
        try:
            return await func(ctx, *args, **kwargs)
        except commands.MissingRequiredArgument as e:
            await ctx.send(f"❌ Missing required argument: {e.param}")
        except commands.BadArgument as e:
            await ctx.send(f"❌ Invalid argument: {e}")
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            await ctx.send("❌ An error occurred while executing the command.")

    return wrapper
