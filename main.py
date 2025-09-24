"""
Koala Bot - Main Application
A modular Discord bot with comprehensive features
"""

import discord
from discord.ext import commands
import asyncio
import logging
from datetime import datetime

# Import configuration
from config.settings import BOT_CONFIG
from config.categories import COMMAND_CATEGORIES

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KoalaBot(commands.Bot):
    """Main Koala Bot class"""

    def __init__(self):
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        intents.guilds = True
        intents.voice_states = True

        # Initialize bot
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None,
            case_insensitive=True,
            strip_after_prefix=True
        )

        # Bot state
        self.uptime = None
        self.log_channels = {}  # guild_id -> channel_id
        self.jail_data = {}    # guild_id -> {user_id -> jail_info}
        self.last_help_execution = {}  # user_id -> timestamp

        # Load cogs
        self.load_cogs()

    def load_cogs(self):
        """Load all bot cogs"""
        cogs_to_load = [
            'cogs.moderation',
            'cogs.interactions',
            'cogs.user_commands',
            'cogs.fun_commands',
            'cogs.utility_commands',
            'cogs.community_commands',
            'cogs.slash_commands',
            'events.logging_events',
            'events.bot_events'
        ]

        for cog in cogs_to_load:
            try:
                self.load_extension(cog)
                logger.info(f"✅ Loaded cog: {cog}")
            except Exception as e:
                logger.error(f"❌ Failed to load cog {cog}: {e}")

    async def on_ready(self):
        """Called when bot is ready"""
        self.uptime = datetime.now()

        logger.info("🤖 Koala Bot is ready!")
        logger.info(f"📝 Logged in as: {self.user.name}#{self.user.discriminator}")
        logger.info(f"🆔 Bot ID: {self.user.id}")
        logger.info(f"🏠 Connected to {len(self.guilds)} servers")
        logger.info(f"👥 Serving {sum(guild.member_count for guild in self.guilds)} users")

        # Set bot presence
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="!help | Koala Bot"
            ),
            status=discord.Status.online
        )

    async def on_guild_join(self, guild):
        """Called when bot joins a new guild"""
        logger.info(f"🆕 Joined new guild: {guild.name} (ID: {guild.id})")

        # Send welcome message
        if guild.system_channel:
            embed = discord.Embed(
                title="🐨 ¡Hola! Soy Koala Bot",
                description="¡Gracias por invitarme a tu servidor! Soy un bot multifuncional con muchos comandos divertidos y útiles.",
                color=0x0099ff
            )

            embed.add_field(
                name="🚀 Para empezar",
                value="• Usa `!help` para ver todos mis comandos\n"
                      "• Usa `/help` para el sistema de ayuda interactivo\n"
                      "• Usa `!setup` para configurar el sistema de moderación\n"
                      "• Usa `!invite` para obtener mi enlace de invitación",
                inline=False
            )

            embed.add_field(
                name="✨ Características principales",
                value="• 🛠️ Comandos de moderación\n"
                      "• 🎭 50+ interacciones con GIFs anime\n"
                      "• 🎲 Comandos de diversión\n"
                      "• 🔧 Utilidades y herramientas\n"
                      "• ⚡ Comandos slash modernos\n"
                      "• 📊 Sistema de logging",
                inline=False
            )

            embed.set_footer(text="¡Espero poder ayudar a hacer tu servidor más divertido!")

            try:
                await guild.system_channel.send(embed=embed)
            except discord.Forbidden:
                logger.warning(f"Cannot send welcome message to {guild.name}: Forbidden")

    async def on_guild_remove(self, guild):
        """Called when bot leaves a guild"""
        logger.info(f"👋 Left guild: {guild.name} (ID: {guild.id})")

        # Clean up guild-specific data
        guild_id = guild.id

        if guild_id in self.log_channels:
            del self.log_channels[guild_id]

        if guild_id in self.jail_data:
            del self.jail_data[guild_id]

async def main():
    """Main function to run the bot"""
    # You'll need to set your bot token here or use environment variables
    TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your actual bot token

    bot = KoalaBot()

    try:
        logger.info("🚀 Starting Koala Bot...")
        await bot.start(TOKEN)
    except KeyboardInterrupt:
        logger.info("👋 Shutting down Koala Bot...")
    except Exception as e:
        logger.error(f"❌ Bot crashed: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
