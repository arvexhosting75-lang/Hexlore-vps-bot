"""Main Hexlore VPS Bot Entry Point"""

import asyncio
import sys
from pathlib import Path

import discord
from discord.ext import commands

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from utils.logger import setup_logging, get_logger
from database.connection import connect_database, close_database
from docker_manager.engine import DockerEngine

# Setup logging
setup_logging()
logger = get_logger(__name__)


class HexloreVPSBot(commands.Bot):
    """Main Hexlore VPS Bot class"""

    def __init__(self, *args, **kwargs):
        """Initialize bot"""
        # Bot intents
        intents = discord.Intents.all()

        # Initialize parent
        super().__init__(
            command_prefix=config.COMMAND_PREFIX,
            intents=intents,
            help_command=None,
            *args,
            **kwargs,
        )

        # Bot attributes
        self.db = None
        self.docker_engine = None
        self.start_time = discord.utils.utcnow()

    async def setup_hook(self):
        """Setup hook - runs before connection"""
        try:
            logger.info("Initializing bot setup...")

            # Connect to database
            logger.info("Connecting to MongoDB...")
            self.db = await connect_database(config.MONGO_URI, config.MONGO_DB_NAME)
            logger.info("✓ Database connected successfully")

            # Initialize Docker engine
            logger.info("Initializing Docker engine...")
            self.docker_engine = DockerEngine(config.DOCKER_SOCKET)
            await self.docker_engine.verify_connection()
            logger.info("✓ Docker engine initialized successfully")

            # Load cogs (extensions)
            logger.info("Loading cogs...")
            await self.load_cogs()
            logger.info("✓ All cogs loaded successfully")

        except Exception as e:
            logger.error(f"Failed to setup bot: {e}", exc_info=True)
            raise

    async def load_cogs(self):
        """Load all cogs from cogs directory"""
        cogs_dir = Path(__file__).parent / "cogs"

        if not cogs_dir.exists():
            logger.warning(f"Cogs directory not found: {cogs_dir}")
            return

        for cog_file in cogs_dir.glob("*.py"):
            if cog_file.name.startswith("_"):
                continue

            cog_name = cog_file.stem
            try:
                await self.load_extension(f"cogs.{cog_name}")
                logger.info(f"✓ Loaded cog: {cog_name}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog_name}: {e}", exc_info=True)

    async def on_ready(self):
        """Called when bot is ready"""
        logger.info(
            f"\n{'='*60}"
            f"\nBot logged in as {self.user}"
            f"\nBot ID: {self.user.id}"
            f"\nLatency: {self.latency * 1000:.2f}ms"
            f"\nServers: {len(self.guilds)}"
            f"\n{'='*60}\n"
        )

        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="/help | VPS Hosting"
            )
        )

    async def on_error(self, event_method, *args, **kwargs):
        """Error handler"""
        logger.error(f"Error in {event_method}", exc_info=True)

    async def close(self):
        """Cleanup on bot shutdown"""
        logger.info("Shutting down bot...")

        try:
            if self.db:
                await close_database()
                logger.info("✓ Database connection closed")
        except Exception as e:
            logger.error(f"Error closing database: {e}", exc_info=True)

        await super().close()
        logger.info("✓ Bot shutdown complete")


async def main():
    """Main bot startup function"""
    # Validate configuration
    errors = config.validate()
    if errors:
        logger.error("Configuration validation failed:")
        for error in errors:
            logger.error(f"  - {error}")
        sys.exit(1)

    logger.info(f"Starting Hexlore VPS Bot...")
    logger.info(f"Environment: {config.LOG_LEVEL}")

    # Create and run bot
    bot = HexloreVPSBot()

    try:
        async with bot:
            await bot.start(config.DISCORD_TOKEN)
    except discord.LoginFailure:
        logger.error("Invalid Discord token")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    # Run main function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot interrupted")
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)
        sys.exit(1)
