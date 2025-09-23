"""
Enhanced Discord Bot Main Application
Modular bot with advanced features, database integration, and comprehensive logging.
"""

import asyncio
import signal
import sys
import os
from typing import Optional, Dict, Any, List
import discord
from discord.ext import commands
from discord import app_commands
import logging

# Import our enhanced modules
from config import config_manager, ConfigurationManager
from database import db_manager
from logging_config import log_manager
from detection import threat_detector

# Set up main logger
logger = log_manager.get_logger(__name__)

class EnhancedBot(commands.Bot):
    """Enhanced Discord bot with advanced features"""

    def __init__(self):
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        intents.guilds = True
        intents.voice_states = True

        # Initialize bot with command prefix
        super().__init__(
            command_prefix=config_manager.settings.discord.command_prefix,
            intents=intents,
            application_id=config_manager.settings.discord.application_id,
            help_command=None,  # We'll implement custom help
            case_insensitive=True,
            strip_after_prefix=True
        )

        # Bot state
        self.start_time = None
        self.guild_count = 0
        self.user_count = 0
        self.command_count = 0
        self._ready_event = asyncio.Event()
        self._shutdown_event = asyncio.Event()

        # Initialize components
        self.config_manager: ConfigurationManager = config_manager
        self.db_manager = db_manager
        self.log_manager = log_manager
        self.threat_detector = threat_detector

        # Track loaded cogs
        self.loaded_cogs: List[str] = []

        # Set up signal handlers
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """Set up signal handlers for graceful shutdown"""

        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, initiating graceful shutdown")
            asyncio.create_task(self.shutdown())

        # Register signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    async def setup_hook(self):
        """Setup hook called before bot starts"""
        logger.info("Setting up bot...")

        try:
            # Create database tables
            await self.db_manager.create_tables()

            # Load cogs
            await self._load_cogs()

            # Sync commands
            if config_manager.settings.discord.sync_commands_globally:
                await self.tree.sync()
                logger.info("Global command sync completed")
            else:
                # Sync to specific guild
                if config_manager.settings.discord.guild_id:
                    guild = discord.Object(id=config_manager.settings.discord.guild_id)
                    await self.tree.sync(guild=guild)
                    logger.info(f"Guild-specific command sync completed for guild {config_manager.settings.discord.guild_id}")

            logger.info("Bot setup completed successfully")

        except Exception as e:
            logger.error(f"Error during bot setup: {e}")
            raise

    async def _load_cogs(self):
        """Load all bot cogs"""
        cog_directory = "cogs"
        if not os.path.exists(cog_directory):
            os.makedirs(cog_directory)
            logger.info(f"Created cogs directory: {cog_directory}")

        # List of core cogs to load
        core_cogs = [
            "cogs.admin",
            "cogs.moderation",
            "cogs.logging",
            "cogs.jail",
            "cogs.utility",
            "cogs.fun",
            "cogs.community",
            "cogs.error_handler",
            "cogs.help"
        ]

        loaded_count = 0
        failed_cogs = []

        for cog_name in core_cogs:
            try:
                await self.load_extension(cog_name)
                self.loaded_cogs.append(cog_name)
                loaded_count += 1
                logger.info(f"Loaded cog: {cog_name}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog_name}: {e}")
                failed_cogs.append(cog_name)

        logger.info(f"Loaded {loaded_count}/{len(core_cogs)} cogs")

        if failed_cogs:
            logger.warning(f"Failed to load cogs: {failed_cogs}")

    async def on_ready(self):
        """Called when bot is ready and connected"""
        self.start_time = discord.utils.utcnow()

        # Update bot statistics
        self.guild_count = len(self.guilds)
        self.user_count = sum(guild.member_count for guild in self.guilds)

        logger.info("Bot is ready!")
        logger.info(f"Logged in as: {self.user} (ID: {self.user.id})")
        logger.info(f"Connected to {self.guild_count} guilds")
        logger.info(f"Serving {self.user_count} users")
        logger.info(f"Command prefix: {self.command_prefix}")

        # Set bot presence
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{self.command_prefix}help | {self.guild_count} servers"
            ),
            status=discord.Status.online
        )

        # Mark ready event
        self._ready_event.set()

        # Log to database
        await self.db_manager.log_event(
            guild_id=0,  # System event
            event_type="bot_ready",
            title="Bot Started",
            description=f"Bot {self.user} has started and is ready",
            severity="info"
        )

    async def on_guild_join(self, guild):
        """Called when bot joins a new guild"""
        logger.info(f"Joined new guild: {guild.name} (ID: {guild.id})")

        # Update statistics
        self.guild_count = len(self.guilds)
        self.user_count = sum(g.member_count for g in self.guilds)

        # Update presence
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{self.command_prefix}help | {self.guild_count} servers"
            )
        )

        # Create guild record in database
        await self.db_manager.get_or_create_guild(guild.id, {
            'name': guild.name,
            'owner_id': guild.owner_id,
            'member_count': guild.member_count
        })

        # Log event
        await self.db_manager.log_event(
            guild_id=guild.id,
            event_type="guild_join",
            title="Bot Joined Guild",
            description=f"Bot joined guild '{guild.name}' owned by {guild.owner}",
            severity="info"
        )

    async def on_guild_remove(self, guild):
        """Called when bot leaves a guild"""
        logger.info(f"Left guild: {guild.name} (ID: {guild.id})")

        # Update statistics
        self.guild_count = len(self.guilds)
        self.user_count = sum(g.member_count for g in self.guilds)

        # Update presence
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{self.command_prefix}help | {self.guild_count} servers"
            )
        )

        # Log event
        await self.db_manager.log_event(
            guild_id=guild.id,
            event_type="guild_leave",
            title="Bot Left Guild",
            description=f"Bot left guild '{guild.name}'",
            severity="info"
        )

    async def on_message(self, message):
        """Called when a message is sent"""
        # Ignore bot messages
        if message.author.bot:
            return

        # Process commands
        await self.process_commands(message)

        # Analyze message for threats
        if config_manager.settings.features.enable_logging:
            try:
                message_data = {
                    'guild_id': message.guild.id if message.guild else None,
                    'user_id': message.author.id,
                    'content': message.content,
                    'channel_id': message.channel.id,
                    'timestamp': message.created_at
                }

                detection_events = await self.threat_detector.analyze_message(message_data)

                # Handle detection events
                for event in detection_events:
                    await self._handle_detection_event(event, message)

            except Exception as e:
                logger.error(f"Error analyzing message: {e}")

    async def _handle_detection_event(self, event, message):
        """Handle a threat detection event"""
        logger.warning("Threat detected",
                      guild_id=event.guild_id,
                      user_id=event.user_id,
                      detection_type=event.detection_type.value,
                      threat_level=event.threat_level.value,
                      confidence=event.confidence)

        # Log to database
        await self.db_manager.log_event(
            guild_id=event.guild_id,
            user_id=event.user_id,
            event_type=f"threat_detected_{event.detection_type.value}",
            title=f"Threat Detected: {event.detection_type.value}",
            description=f"Threat level: {event.threat_level.value}, Confidence: {event.confidence:.2f}",
            severity=event.threat_level.value,
            metadata=event.details
        )

        # Take action based on threat level and configured response
        if event.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
            # More aggressive actions for high/critical threats
            if event.detection_type == DetectionType.RAID:
                # Handle raid detection
                await self._handle_raid_detection(event, message)
            elif event.detection_type == DetectionType.MALICIOUS_LINKS:
                # Handle malicious links
                await self._handle_malicious_links(event, message)
            elif event.detection_type == DetectionType.SPAM:
                # Handle spam
                await self._handle_spam_detection(event, message)

    async def _handle_raid_detection(self, event, message):
        """Handle raid detection"""
        try:
            guild = message.guild
            user = message.author

            # Check if user can be moderated
            if not guild.me.guild_permissions.manage_roles:
                logger.warning("Cannot moderate user due to insufficient permissions")
                return

            # Add user to jail if jail system is enabled
            if config_manager.settings.features.enable_jail_system:
                try:
                    jail_record = await self.db_manager.jail_user(
                        guild_id=guild.id,
                        user_id=user.id,
                        moderator_id=self.user.id,
                        reason=f"Automatic jail for raid detection (confidence: {event.confidence:.2f})"
                    )

                    # Try to DM the user
                    try:
                        embed = discord.Embed(
                            title="🚨 Raid Detection",
                            description="You have been temporarily jailed due to suspicious activity detected as a potential raid.",
                            color=discord.Color.red(),
                            timestamp=discord.utils.utcnow()
                        )
                        embed.add_field(name="Reason", value="Automated raid detection", inline=False)
                        embed.add_field(name="Confidence", value=f"{event.confidence:.2f}", inline=False)

                        await user.send(embed=embed)
                    except discord.Forbidden:
                        pass  # Cannot DM user

                    logger.info(f"User {user} jailed for raid detection")

                except Exception as e:
                    logger.error(f"Failed to jail user {user.id}: {e}")

        except Exception as e:
            logger.error(f"Error handling raid detection: {e}")

    async def _handle_malicious_links(self, event, message):
        """Handle malicious links detection"""
        try:
            # Delete the message
            try:
                await message.delete()
                logger.info(f"Deleted message with malicious links from {message.author}")
            except discord.Forbidden:
                logger.warning("Cannot delete message due to insufficient permissions")
            except discord.NotFound:
                pass  # Message already deleted

            # Warn the user
            try:
                embed = discord.Embed(
                    title="⚠️ Malicious Link Detected",
                    description="Your message contained a potentially malicious link and has been removed.",
                    color=discord.Color.orange(),
                    timestamp=discord.utils.utcnow()
                )
                embed.add_field(name="Action", value="Message deleted", inline=False)

                await message.author.send(embed=embed)
            except discord.Forbidden:
                pass  # Cannot DM user

        except Exception as e:
            logger.error(f"Error handling malicious links: {e}")

    async def _handle_spam_detection(self, event, message):
        """Handle spam detection"""
        try:
            # Delete the message
            try:
                await message.delete()
                logger.info(f"Deleted spam message from {message.author}")
            except discord.Forbidden:
                logger.warning("Cannot delete message due to insufficient permissions")
            except discord.NotFound:
                pass

            # Warn the user
            try:
                embed = discord.Embed(
                    title="🚫 Spam Detected",
                    description="Your message was detected as spam and has been removed.",
                    color=discord.Color.orange(),
                    timestamp=discord.utils.utcnow()
                )

                await message.author.send(embed=embed)
            except discord.Forbidden:
                pass

        except Exception as e:
            logger.error(f"Error handling spam detection: {e}")

    async def on_command(self, ctx):
        """Called when a command is invoked"""
        self.command_count += 1

        # Track command usage
        await self.db_manager.track_command_usage(
            guild_id=ctx.guild.id if ctx.guild else None,
            user_id=ctx.author.id,
            command_name=ctx.command.name,
            execution_time=0,  # Will be updated when command completes
            success=True
        )

        # Log command usage
        self.log_manager.log_command_usage(
            guild_id=ctx.guild.id if ctx.guild else None,
            user_id=ctx.author.id,
            command_name=ctx.command.name,
            execution_time=0,
            success=True
        )

        logger.debug(f"Command invoked: {ctx.command.name} by {ctx.author} in {ctx.guild}")

    async def on_command_error(self, ctx, error):
        """Called when a command raises an error"""
        # Track failed command
        await self.db_manager.track_command_usage(
            guild_id=ctx.guild.id if ctx.guild else None,
            user_id=ctx.author.id,
            command_name=ctx.command.name,
            execution_time=0,
            success=False,
            error_message=str(error)
        )

        # Log error
        self.log_manager.log_error(
            error=error,
            context={
                'command': ctx.command.name,
                'guild_id': ctx.guild.id if ctx.guild else None,
                'channel_id': ctx.channel.id
            },
            user_id=ctx.author.id,
            guild_id=ctx.guild.id if ctx.guild else None
        )

        logger.error(f"Command error: {ctx.command.name}", error=str(error))

    async def on_member_join(self, member):
        """Called when a member joins a guild"""
        logger.info(f"Member joined: {member} in {member.guild}")

        # Create/update user record
        await self.db_manager.get_or_create_user(member.id, {
            'username': member.name,
            'discriminator': member.discriminator,
            'display_name': member.display_name,
            'avatar_hash': member.avatar.key if member.avatar else None,
            'banner_hash': member.banner.key if member.banner else None,
            'bot': member.bot,
            'system': member.system
        })

        # Create guild member record
        await self.db_manager.get_or_create_guild(member.guild.id, {
            'name': member.guild.name,
            'owner_id': member.guild.owner_id,
            'member_count': member.guild.member_count
        })

        # Log event
        await self.db_manager.log_event(
            guild_id=member.guild.id,
            user_id=member.id,
            event_type="member_join",
            title="Member Joined",
            description=f"{member.mention} joined the server",
            severity="info"
        )

    async def on_member_remove(self, member):
        """Called when a member leaves a guild"""
        logger.info(f"Member left: {member} from {member.guild}")

        # Log event
        await self.db_manager.log_event(
            guild_id=member.guild.id,
            user_id=member.id,
            event_type="member_leave",
            title="Member Left",
            description=f"{member.mention} left the server",
            severity="info"
        )

    async def on_message_delete(self, message):
        """Called when a message is deleted"""
        if message.author.bot:
            return

        # Log message deletion
        await self.db_manager.log_event(
            guild_id=message.guild.id if message.guild else None,
            user_id=message.author.id,
            channel_id=message.channel.id,
            event_type="message_delete",
            title="Message Deleted",
            description=f"Message by {message.author.mention} was deleted",
            severity="info",
            metadata={
                'content': message.content[:500],  # Truncate long messages
                'attachments': len(message.attachments),
                'embeds': len(message.embeds)
            }
        )

    async def on_bulk_message_delete(self, messages):
        """Called when multiple messages are deleted"""
        if not messages:
            return

        guild = messages[0].guild
        channel = messages[0].channel

        # Log bulk deletion
        await self.db_manager.log_event(
            guild_id=guild.id if guild else None,
            channel_id=channel.id,
            event_type="bulk_message_delete",
            title="Bulk Message Deletion",
            description=f"{len(messages)} messages were deleted in {channel.mention}",
            severity="warning",
            metadata={
                'message_count': len(messages),
                'channel_id': channel.id,
                'channel_name': channel.name
            }
        )

    async def wait_until_ready(self):
        """Wait until bot is ready"""
        await self._ready_event.wait()

    async def shutdown(self):
        """Gracefully shutdown the bot"""
        logger.info("Initiating bot shutdown...")

        # Set shutdown event
        self._shutdown_event.set()

        try:
            # Shutdown logging
            await self.log_manager.shutdown()

            # Close database connections
            await self.db_manager._async_engine.dispose()

            # Close bot connection
            await self.close()

            logger.info("Bot shutdown completed successfully")

        except Exception as e:
            logger.error(f"Error during bot shutdown: {e}")
        finally:
            # Exit the process
            sys.exit(0)

    def get_uptime(self):
        """Get bot uptime"""
        if not self.start_time:
            return None
        return discord.utils.utcnow() - self.start_time

    def get_stats(self) -> Dict[str, Any]:
        """Get bot statistics"""
        return {
            'guilds': self.guild_count,
            'users': self.user_count,
            'commands_processed': self.command_count,
            'uptime': str(self.get_uptime()) if self.get_uptime() else None,
            'loaded_cogs': len(self.loaded_cogs),
            'latency': f"{self.latency * 1000:.2f}ms" if self.latency else None
        }

async def main():
    """Main function to run the bot"""
    bot = EnhancedBot()

    try:
        logger.info("Starting Enhanced Discord Bot...")
        logger.info(f"Environment: {config_manager.settings.environment}")
        logger.info(f"Debug mode: {config_manager.settings.debug}")

        # Start the bot
        await bot.start(config_manager.settings.discord.token)

    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
        await bot.shutdown()
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        await bot.shutdown()

if __name__ == "__main__":
    # Run the bot
    asyncio.run(main())
