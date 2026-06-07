"""Discord embed generators"""

import discord
from datetime import datetime
from typing import Optional, List


class EmbedGenerator:
    """Generate Discord embeds for the bot"""

    # Colors
    COLOR_SUCCESS = discord.Color.green()
    COLOR_ERROR = discord.Color.red()
    COLOR_INFO = discord.Color.blue()
    COLOR_WARNING = discord.Color.gold()
    COLOR_PREMIUM = discord.Color.purple()

    @staticmethod
    def vps_status(vps_data: dict) -> discord.Embed:
        """Generate VPS status embed

        Args:
            vps_data: VPS data dictionary

        Returns:
            Discord embed
        """
        embed = discord.Embed(
            title=f"🖥️ VPS: {vps_data.get('name', 'Unknown')}",
            color=EmbedGenerator.COLOR_INFO,
            timestamp=datetime.utcnow(),
        )

        # Status
        status = vps_data.get("status", "unknown").upper()
        status_emoji = "🟢" if status == "RUNNING" else "🔴"
        embed.add_field(name="Status", value=f"{status_emoji} {status}", inline=True)

        # Hostname
        embed.add_field(
            name="Hostname", value=vps_data.get("hostname", "N/A"), inline=True
        )

        # Resources
        embed.add_field(
            name="💾 Memory",
            value=f"{vps_data.get('ram_mb', 0)} MB",
            inline=True,
        )
        embed.add_field(
            name="⚙️ CPU",
            value=f"{vps_data.get('cpu_shares', 0)} shares",
            inline=True,
        )
        embed.add_field(
            name="💿 Disk",
            value=f"{vps_data.get('disk_gb', 0)} GB",
            inline=True,
        )

        return embed

    @staticmethod
    def error_embed(title: str, description: str) -> discord.Embed:
        """Generate error embed

        Args:
            title: Error title
            description: Error description

        Returns:
            Discord embed
        """
        return discord.Embed(
            title=f"❌ {title}",
            description=description,
            color=EmbedGenerator.COLOR_ERROR,
            timestamp=datetime.utcnow(),
        )

    @staticmethod
    def success_embed(title: str, description: str) -> discord.Embed:
        """Generate success embed

        Args:
            title: Success title
            description: Success description

        Returns:
            Discord embed
        """
        return discord.Embed(
            title=f"✅ {title}",
            description=description,
            color=EmbedGenerator.COLOR_SUCCESS,
            timestamp=datetime.utcnow(),
        )

    @staticmethod
    def info_embed(title: str, description: str, fields: Optional[dict] = None) -> discord.Embed:
        """Generate info embed

        Args:
            title: Info title
            description: Info description
            fields: Additional fields

        Returns:
            Discord embed
        """
        embed = discord.Embed(
            title=f"ℹ️ {title}",
            description=description,
            color=EmbedGenerator.COLOR_INFO,
            timestamp=datetime.utcnow(),
        )

        if fields:
            for name, value in fields.items():
                embed.add_field(name=name, value=value, inline=False)

        return embed
