import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

class KoalaBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        intents.moderation = True
        intents.messages = True

        super().__init__(command_prefix='!', intents=intents, help_command=None)

        # Store log channels (guild_id -> channel_id)
        self.log_channels = {}

        # Store jail data (guild_id -> {user_id -> jail_data})
        self.jail_data = {}

        # Store last help command execution time per user
        self.last_help_execution = {}

    async def setup_hook(self):
        """Load all cogs when bot starts"""
        print("Loading cogs...")

        # Load all cogs
        cogs_to_load = [
            'cogs.moderation',
            'cogs.interactions',
            'cogs.user_commands',
            'cogs.fun_commands',
            'cogs.utility_commands',
            'cogs.community_commands',
            'events.logging_events',
            'events.bot_events'
        ]

        for cog in cogs_to_load:
            try:
                await self.load_extension(cog)
                print(f"✅ Loaded {cog}")
            except Exception as e:
                print(f"❌ Failed to load {cog}: {e}")

        print(f"Bot loaded with {len(cogs_to_load)} cogs")

    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord!')
        print(f'Bot ID: {self.user.id}')
        print(f'Connected to {len(self.guilds)} servers')
        print('------')

        # Sync slash commands with Discord
        try:
            synced = await self.tree.sync()
            print(f'Synced {len(synced)} command(s)')
        except Exception as e:
            print(f'Failed to sync commands: {e}')

# Create bot instance
bot = KoalaBot()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ DISCORD_BOT_TOKEN not found in environment variables.")
        print("Please create a .env file with your bot token:")
        print("DISCORD_BOT_TOKEN=your_bot_token_here")
