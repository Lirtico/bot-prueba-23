#!/usr/bin/env python3
"""
Test script to verify bot setup and slash commands
"""

import discord
from discord.ext import commands
import asyncio
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestBot(commands.Bot):
    """Test bot to verify setup"""

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        intents.guilds = True
        intents.voice_states = True

        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )

    async def on_ready(self):
        logger.info("🤖 Test Bot is ready!")
        logger.info(f"📝 Logged in as: {self.user.name}#{self.user.discriminator}")
        logger.info(f"🆔 Bot ID: {self.user.id}")

        # Test slash command sync
        try:
            synced = await self.tree.sync()
            logger.info(f"✅ Synced {len(synced)} slash commands")
            for cmd in synced:
                logger.info(f"  - / {cmd.name}")
        except Exception as e:
            logger.error(f"❌ Failed to sync slash commands: {e}")

        # List all loaded commands
        logger.info(f"📋 Loaded {len(self.commands)} regular commands:")
        for cmd in self.commands:
            logger.info(f"  - ! {cmd.name}")

        logger.info("✅ Bot setup test completed successfully!")
        await self.close()

async def test_bot():
    """Test bot setup"""
    TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your actual bot token

    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("❌ Please set your bot token in the TOKEN variable")
        sys.exit(1)

    bot = TestBot()

    try:
        logger.info("🚀 Starting test bot...")
        await bot.start(TOKEN)
    except discord.LoginFailure:
        logger.error("❌ Invalid bot token! Please check your token.")
    except Exception as e:
        logger.error(f"❌ Bot test failed: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(test_bot())
