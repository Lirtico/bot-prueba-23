import discord
from discord.ext import commands
from discord.ui import Button, View, Select
import os
import random
import asyncio
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.moderation = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Log configuration storage (guild_id -> channel_id)
log_channels = {}

# Slash Commands
@bot.tree.command(name="logs", description="Configure logging for server events")
@commands.has_permissions(administrator=True)
async def setup_logs(interaction: discord.Interaction, channel: discord.TextChannel):
    """Set up logging for server events"""
    guild_id = interaction.guild.id

    # Store the log channel for this guild
    log_channels[guild_id] = channel.id

    embed = discord.Embed(
        title="📋 Logging Configured",
        description=f"✅ Server logs will now be sent to {channel.mention}",
        color=0x00ff00
    )

    embed.add_field(
        name="📊 Events Logged",
        value="• Member joins/leaves\n"
              "• Messages deleted\n"
              "• Role changes\n"
              "• Channel updates\n"
              "• Moderation actions",
        inline=False
    )

    embed.set_footer(text="Use /logs-disable to stop logging")

    await interaction.response.send_message(embed=embed, ephemeral=True)

    # Send a test message to the log channel
    test_embed = discord.Embed(
        title="🔧 Logging System Activated",
        description="Server logging has been configured and is now active.",
        color=0x0099ff
    )
    test_embed.add_field(name="📝 Log Channel", value=channel.mention, inline=True)
    test_embed.add_field(name="⚙️ Configured by", value=interaction.user.mention, inline=True)
    test_embed.set_footer(text=f"Server: {interaction.guild.name}")

    try:
        await channel.send(embed=test_embed)
    except discord.Forbidden:
        await interaction.followup.send("❌ I don't have permission to send messages to the log channel.", ephemeral=True)

@bot.tree.command(name="logs-disable", description="Disable logging for server events")
@commands.has_permissions(administrator=True)
async def disable_logs(interaction: discord.Interaction):
    """Disable logging for server events"""
    guild_id = interaction.guild.id

    if guild_id not in log_channels:
        await interaction.response.send_message("❌ Logging is not currently configured for this server.", ephemeral=True)
        return

    # Remove the log channel configuration
    del log_channels[guild_id]

    embed = discord.Embed(
        title="📋 Logging Disabled",
        description="✅ Server logging has been disabled.",
        color=0xff0000
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)

    # Send a notification to the previously configured channel
    try:
        channel = bot.get_channel(log_channels.get(guild_id))
        if channel:
            disable_embed = discord.Embed(
                title="🔧 Logging System Deactivated",
                description="Server logging has been disabled.",
                color=0xff0000
            )
            disable_embed.add_field(name="⚙️ Disabled by", value=interaction.user.mention, inline=True)
            await channel.send(embed=disable_embed)
    except:
        pass  # If we can't send to the channel, just continue

@bot.tree.command(name="logs-status", description="Check logging status")
async def logs_status(interaction: discord.Interaction):
    """Check the current logging status"""
    guild_id = interaction.guild.id

    if guild_id in log_channels:
        channel = bot.get_channel(log_channels[guild_id])
        embed = discord.Embed(
            title="📊 Logging Status: Active",
            description=f"✅ Server logs are being sent to {channel.mention}",
            color=0x00ff00
        )
    else:
        embed = discord.Embed(
            title="📊 Logging Status: Inactive",
            description="❌ Server logging is not configured.\nUse `/logs #channel` to set up logging.",
            color=0xff0000
        )

    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="setup", description="Create koala setup category with logs-server and jail channels")
@commands.has_permissions(administrator=True)
async def setup_koala_system(interaction: discord.Interaction):
    """Create a koala setup category with logs-server and jail channels"""
    guild_id = interaction.guild.id

    # Check if logging is already configured
    if guild_id in log_channels:
        channel = bot.get_channel(log_channels[guild_id])
        await interaction.response.send_message(
            f"❌ Logging is already configured for {channel.mention}. Use `/logs-disable` first if you want to reconfigure.",
            ephemeral=True
        )
        return

    try:
        # Create the koala setup category
        category = await interaction.guild.create_category(
            name="koala setup",
            reason="Auto-created by setup command"
        )

        # Create the logs-server channel
        logs_overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
        }

        logs_channel = await interaction.guild.create_text_channel(
            name="logs-server",
            category=category,
            overwrites=logs_overwrites,
            reason="Auto-created by setup command"
        )

        # Create the jail channel
        jail_overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True, manage_channels=True)
        }

        jail_channel = await interaction.guild.create_text_channel(
            name="jail",
            category=category,
            overwrites=jail_overwrites,
            reason="Auto-created by setup command"
        )

        # Configure logging to use the logs channel
        log_channels[guild_id] = logs_channel.id

        embed = discord.Embed(
            title="🐨 Koala Setup Complete",
            description=f"✅ Created **koala setup** category with {logs_channel.mention} and {jail_channel.mention}!",
            color=0x00ff00
        )

        embed.add_field(
            name="📊 Logs Channel",
            value="• Server events logging\n"
                  "• Member joins/leaves\n"
                  "• Messages deleted\n"
                  "• Role changes\n"
                  "• Moderation actions",
            inline=False
        )

        embed.add_field(
            name="🔒 Jail Channel",
            value="• Isolated moderation space\n"
                  "• Jailed users can communicate\n"
                  "• Only bot can manage messages",
            inline=False
        )

        embed.add_field(
            name="🔧 Channel Permissions",
            value="• **Logs:** Everyone can read, only bot can send\n"
                  "• **Jail:** Hidden from everyone except jailed users and bot\n"
                  "• **Category:** Organized under 'koala setup'",
            inline=False
        )

        embed.set_footer(text="Use /logs-disable to stop logging")

        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Send a test message to the log channel
        test_embed = discord.Embed(
            title="🔧 Koala System Activated",
            description="Koala setup category has been created and logging is now active.",
            color=0x0099ff
        )
        test_embed.add_field(name="📝 Log Channel", value=logs_channel.mention, inline=True)
        test_embed.add_field(name="🔒 Jail Channel", value=jail_channel.mention, inline=True)
        test_embed.add_field(name="⚙️ Configured by", value=interaction.user.mention, inline=True)
        test_embed.add_field(name="📁 Category", value="koala setup", inline=True)
        test_embed.set_footer(text=f"Server: {interaction.guild.name}")

        await logs_channel.send(embed=test_embed)

        # Send welcome message to jail channel
        jail_embed = discord.Embed(
            title="🔒 Koala Jail System",
            description="This is the jail channel for moderated users.\n\n"
                       "Users sent here can communicate with each other and moderators.\n"
                       "Contact a moderator if you believe this is a mistake.",
            color=0xff0000
        )
        jail_embed.set_footer(text="Koala Jail System - Part of koala setup category")

        await jail_channel.send(embed=jail_embed)

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ I don't have permission to create channels or categories in this server.",
            ephemeral=True
        )
    except discord.HTTPException as e:
        await interaction.response.send_message(
            f"❌ Failed to create koala setup: {e}",
            ephemeral=True
        )

# Jail System Storage (guild_id -> {user_id -> jail_data})
jail_data = {}

@bot.command(name='jail')
@commands.has_permissions(manage_roles=True)
async def jail(ctx, member: discord.Member = None, *, reason=None):
    """Jail a user - works with mentions or replies"""
    # Handle reply context
    if member is None and ctx.message.reference:
        try:
            replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            member = replied_message.author
        except:
            pass

    if member is None:
        await ctx.send("❌ Please mention a user or reply to their message to jail them.")
        return

    if member == ctx.author:
        await ctx.send("❌ You can't jail yourself!")
        return

    if member.bot:
        await ctx.send("❌ You can't jail bots!")
        return

    if ctx.author.top_role <= member.top_role:
        await ctx.send("❌ You can't jail someone with a higher or equal role!")
        return

    guild_id = ctx.guild.id

    # Check if user is already jailed
    if guild_id in jail_data and member.id in jail_data[guild_id]:
        await ctx.send(f"❌ {member.mention} is already in jail!")
        return

    try:
        # Create jail channel if it doesn't exist
        jail_channel = None
        for channel in ctx.guild.channels:
            if channel.name == "jail":
                jail_channel = channel
                break

        if jail_channel is None:
            # Create jail channel
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True, manage_channels=True),
                member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }

            jail_channel = await ctx.guild.create_text_channel(
                name="jail",
                overwrites=overwrites,
                reason=f"Jail channel created for {member.name}"
            )

        # Store original roles
        original_roles = [role.id for role in member.roles if role != ctx.guild.default_role]

        # Remove all roles except @everyone
        for role in member.roles[:]:  # Copy the list to avoid modification issues
            if role != ctx.guild.default_role:
                try:
                    await member.remove_roles(role, reason=f"User jailed by {ctx.author.name}")
                except discord.Forbidden:
                    await ctx.send("❌ I don't have permission to remove roles from this user.")
                    return
                except discord.HTTPException as e:
                    await ctx.send(f"❌ Failed to remove roles: {e}")
                    return

        # Store jail data
        if guild_id not in jail_data:
            jail_data[guild_id] = {}

        jail_data[guild_id][member.id] = {
            'original_roles': original_roles,
            'jailed_by': ctx.author.id,
            'reason': reason,
            'timestamp': datetime.now().timestamp()
        }

        # Send jail notification
        embed = discord.Embed(
            title="🔒 User Jailed",
            description=f"{member.mention} has been sent to jail!",
            color=0xff0000
        )

        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)

        embed.add_field(name="Jailed by", value=ctx.author.mention, inline=True)
        embed.add_field(name="Jail Channel", value=jail_channel.mention, inline=True)
        embed.add_field(name="Original Roles", value=len(original_roles), inline=True)

        embed.set_footer(text=f"Use !unjail {member.mention} to release the user")

        await ctx.send(embed=embed)

        # Send message to jail channel
        jail_embed = discord.Embed(
            title="🔒 Welcome to Jail",
            description=f"{member.mention}, you have been sent to jail!",
            color=0xff0000
        )

        if reason:
            jail_embed.add_field(name="Reason", value=reason, inline=False)

        jail_embed.add_field(name="Jailed by", value=ctx.author.mention, inline=True)
        jail_embed.add_field(name="Time", value=datetime.now().strftime("%B %d, %Y %H:%M"), inline=True)

        jail_embed.set_footer(text="Contact a moderator if you believe this is a mistake")

        await jail_channel.send(embed=jail_embed)

        # Log the jail action if logging is enabled
        if guild_id in log_channels:
            log_channel = bot.get_channel(log_channels[guild_id])
            log_embed = discord.Embed(
                title="🔒 User Jailed",
                description=f"{member.mention} was sent to jail",
                color=0xff0000
            )
            log_embed.add_field(name="👤 User", value=f"{member.name}#{member.discriminator}", inline=True)
            log_embed.add_field(name="🆔 User ID", value=member.id, inline=True)
            log_embed.add_field(name="👮 Jailed by", value=ctx.author.mention, inline=True)
            if reason:
                log_embed.add_field(name="📝 Reason", value=reason, inline=False)

            try:
                await log_channel.send(embed=log_embed)
            except discord.Forbidden:
                pass

    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to create channels or manage roles.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ Failed to jail user: {e}")

@bot.command(name='unjail')
@commands.has_permissions(manage_roles=True)
async def unjail(ctx, member: discord.Member = None, *, reason=None):
    """Release a user from jail - works with mentions or replies"""
    # Handle reply context
    if member is None and ctx.message.reference:
        try:
            replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            member = replied_message.author
        except:
            pass

    if member is None:
        await ctx.send("❌ Please mention a user or reply to their message to unjail them.")
        return

    guild_id = ctx.guild.id

    # Check if user is actually jailed
    if guild_id not in jail_data or member.id not in jail_data[guild_id]:
        await ctx.send(f"❌ {member.mention} is not in jail!")
        return

    try:
        jail_info = jail_data[guild_id][member.id]

        # Restore original roles
        for role_id in jail_info['original_roles']:
            role = ctx.guild.get_role(role_id)
            if role:
                try:
                    await member.add_roles(role, reason=f"User released from jail by {ctx.author.name}")
                except discord.Forbidden:
                    await ctx.send(f"❌ I don't have permission to restore the role: {role.name}")
                except discord.HTTPException as e:
                    await ctx.send(f"❌ Failed to restore role {role.name}: {e}")

        # Remove from jail data
        del jail_data[guild_id][member.id]

        # Send unjail notification
        embed = discord.Embed(
            title="🔓 User Released",
            description=f"{member.mention} has been released from jail!",
            color=0x00ff00
        )

        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)

        embed.add_field(name="Released by", value=ctx.author.mention, inline=True)
        embed.add_field(name="Time in Jail", value=f"{(datetime.now().timestamp() - jail_info['timestamp']) / 3600:.1f} hours", inline=True)

        embed.set_footer(text="User has been restored to their original roles")

        await ctx.send(embed=embed)

        # Find jail channel and send release message
        jail_channel = None
        for channel in ctx.guild.channels:
            if channel.name == "jail":
                jail_channel = channel
                break

        if jail_channel:
            release_embed = discord.Embed(
                title="🔓 Released from Jail",
                description=f"{member.mention}, you have been released from jail!",
                color=0x00ff00
            )

            if reason:
                release_embed.add_field(name="Reason", value=reason, inline=False)

            release_embed.add_field(name="Released by", value=ctx.author.mention, inline=True)
            release_embed.add_field(name="Time Served", value=f"{(datetime.now().timestamp() - jail_info['timestamp']) / 3600:.1f} hours", inline=True)

            try:
                await jail_channel.send(embed=release_embed)
            except discord.Forbidden:
                pass

        # Log the unjail action if logging is enabled
        if guild_id in log_channels:
            log_channel = bot.get_channel(log_channels[guild_id])
            log_embed = discord.Embed(
                title="🔓 User Released from Jail",
                description=f"{member.mention} was released from jail",
                color=0x00ff00
            )
            log_embed.add_field(name="👤 User", value=f"{member.name}#{member.discriminator}", inline=True)
            log_embed.add_field(name="🆔 User ID", value=member.id, inline=True)
            log_embed.add_field(name="👮 Released by", value=ctx.author.mention, inline=True)
            log_embed.add_field(name="⏱️ Time Served", value=f"{(datetime.now().timestamp() - jail_info['timestamp']) / 3600:.1f} hours", inline=True)

            try:
                await log_channel.send(embed=log_embed)
            except discord.Forbidden:
                pass

    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to manage roles.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ Failed to unjail user: {e}")

@bot.command(name='jailstatus')
@commands.has_permissions(manage_roles=True)
async def jailstatus(ctx):
    """Check who is currently in jail"""
    guild_id = ctx.guild.id

    if guild_id not in jail_data or not jail_data[guild_id]:
        embed = discord.Embed(
            title="🔒 Jail Status",
            description="✅ No users are currently in jail.",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(
        title="🔒 Jail Status",
        description=f"📊 **Total jailed users:** {len(jail_data[guild_id])}",
        color=0xff9900
    )

    for user_id, jail_info in jail_data[guild_id].items():
        try:
            user = await bot.fetch_user(user_id)
            time_in_jail = datetime.now().timestamp() - jail_info['timestamp']
            hours = time_in_jail / 3600

            embed.add_field(
                name=f"{user.name}#{user.discriminator}",
                value=f"**ID:** {user_id}\n"
                      f"**Jailed by:** <@{jail_info['jailed_by']}>\n"
                      f"**Time:** {hours:.1f} hours\n"
                      f"**Reason:** {jail_info['reason'] or 'No reason provided'}",
                inline=False
            )
        except:
            embed.add_field(
                name=f"Unknown User ({user_id})",
                value=f"**Time:** {(datetime.now().timestamp() - jail_info['timestamp']) / 3600:.1f} hours\n"
                      f"**Reason:** {jail_info['reason'] or 'No reason provided'}",
                inline=False
            )

    embed.set_footer(text="Use !unjail @user to release a user")
    await ctx.send(embed=embed)

# Event Listeners for Logging
@bot.event
async def on_member_join(member):
    """Log when a member joins the server"""
    guild_id = member.guild.id

    if guild_id in log_channels:
        channel = bot.get_channel(log_channels[guild_id])

        embed = discord.Embed(
            title="👋 Member Joined",
            description=f"{member.mention} joined the server",
            color=0x00ff00
        )

        embed.add_field(name="👤 User", value=f"{member.name}#{member.discriminator}", inline=True)
        embed.add_field(name="🆔 User ID", value=member.id, inline=True)
        embed.add_field(name="📅 Account Created", value=member.created_at.strftime("%B %d, %Y"), inline=True)

        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"Member count: {member.guild.member_count}")

        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass  # Can't send to channel

@bot.event
async def on_member_remove(member):
    """Log when a member leaves the server"""
    guild_id = member.guild.id

    if guild_id in log_channels:
        channel = bot.get_channel(log_channels[guild_id])

        embed = discord.Embed(
            title="👋 Member Left",
            description=f"{member.mention} left the server",
            color=0xff0000
        )

        embed.add_field(name="👤 User", value=f"{member.name}#{member.discriminator}", inline=True)
        embed.add_field(name="🆔 User ID", value=member.id, inline=True)
        embed.add_field(name="📅 Joined", value=member.joined_at.strftime("%B %d, %Y") if member.joined_at else "Unknown", inline=True)

        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"Member count: {member.guild.member_count}")

        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass  # Can't send to channel

@bot.event
async def on_message_delete(message):
    """Log when a message is deleted"""
    guild_id = message.guild.id if message.guild else None

    if guild_id and guild_id in log_channels and message.author.bot == False:
        channel = bot.get_channel(log_channels[guild_id])

        embed = discord.Embed(
            title="🗑️ Message Deleted",
            description=f"Message deleted in {message.channel.mention}",
            color=0xff9900
        )

        embed.add_field(name="👤 Author", value=f"{message.author.mention}", inline=True)
        embed.add_field(name="📝 Channel", value=message.channel.name, inline=True)
        embed.add_field(name="🕐 Time", value=message.created_at.strftime("%H:%M:%S"), inline=True)

        if message.content:
            embed.add_field(name="📄 Content", value=message.content[:1024], inline=False)

        if message.attachments:
            embed.add_field(name="📎 Attachments", value=f"{len(message.attachments)} file(s)", inline=True)

        embed.set_footer(text=f"Message ID: {message.id}")

        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass  # Can't send to channel

@bot.event
async def on_bulk_message_delete(messages):
    """Log when multiple messages are deleted"""
    if not messages:
        return

    guild_id = messages[0].guild.id if messages[0].guild else None

    if guild_id and guild_id in log_channels:
        channel = bot.get_channel(log_channels[guild_id])

        embed = discord.Embed(
            title="🗑️ Bulk Message Delete",
            description=f"{len(messages)} messages deleted in {messages[0].channel.mention}",
            color=0xff6600
        )

        embed.add_field(name="📝 Channel", value=messages[0].channel.name, inline=True)
        embed.add_field(name="👥 Affected Users", value=len(set(msg.author for msg in messages if not msg.author.bot)), inline=True)

        # Show some sample content if available
        content_samples = []
        for msg in messages[:3]:  # Show first 3 messages
            if msg.content and not msg.author.bot:
                content_samples.append(f"{msg.author.display_name}: {msg.content[:100]}...")

        if content_samples:
            embed.add_field(name="📄 Sample Content", value="\n".join(content_samples), inline=False)

        embed.set_footer(text=f"Channel: {messages[0].channel.name}")

        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass  # Can't send to channel

@bot.event
async def on_member_update(before, after):
    """Log when a member is updated (role changes, nickname changes, etc.)"""
    guild_id = after.guild.id

    if guild_id in log_channels:
        channel = bot.get_channel(log_channels[guild_id])

        # Check for nickname changes
        if before.nick != after.nick:
            embed = discord.Embed(
                title="📝 Nickname Changed",
                description=f"{after.mention}'s nickname was changed",
                color=0x0099ff
            )

            embed.add_field(name="👤 User", value=f"{after.name}#{after.discriminator}", inline=True)
            embed.add_field(name="🆔 User ID", value=after.id, inline=True)
            embed.add_field(name="📝 Before", value=before.nick or "None", inline=True)
            embed.add_field(name="📝 After", value=after.nick or "None", inline=True)

            embed.set_thumbnail(url=after.avatar.url if after.avatar else after.default_avatar.url)

            try:
                await channel.send(embed=embed)
            except discord.Forbidden:
                pass  # Can't send to channel

        # Check for role changes
        if before.roles != after.roles:
            added_roles = [role for role in after.roles if role not in before.roles]
            removed_roles = [role for role in before.roles if role not in after.roles]

            if added_roles:
                embed = discord.Embed(
                    title="➕ Role Added",
                    description=f"{after.mention} was given a role",
                    color=0x00ff00
                )

                embed.add_field(name="👤 User", value=f"{after.name}#{after.discriminator}", inline=True)
                embed.add_field(name="🆔 User ID", value=after.id, inline=True)
                embed.add_field(name="➕ Added Role", value=", ".join(role.mention for role in added_roles), inline=False)

                embed.set_thumbnail(url=after.avatar.url if after.avatar else after.default_avatar.url)

                try:
                    await channel.send(embed=embed)
                except discord.Forbidden:
                    pass  # Can't send to channel

            if removed_roles:
                embed = discord.Embed(
                    title="➖ Role Removed",
                    description=f"{after.mention} had a role removed",
                    color=0xff0000
                )

                embed.add_field(name="👤 User", value=f"{after.name}#{after.discriminator}", inline=True)
                embed.add_field(name="🆔 User ID", value=after.id, inline=True)
                embed.add_field(name="➖ Removed Role", value=", ".join(role.mention for role in removed_roles), inline=False)

                embed.set_thumbnail(url=after.avatar.url if after.avatar else after.default_avatar.url)

                try:
                    await channel.send(embed=embed)
                except discord.Forbidden:
                    pass  # Can't send to channel

@bot.event
async def on_guild_channel_create(channel):
    """Log when a channel is created"""
    guild_id = channel.guild.id

    if guild_id in log_channels:
        log_channel = bot.get_channel(log_channels[guild_id])

        embed = discord.Embed(
            title="📺 Channel Created",
            description=f"New channel created: {channel.mention}",
            color=0x00ff00
        )

        embed.add_field(name="📝 Channel Name", value=channel.name, inline=True)
        embed.add_field(name="📝 Channel Type", value=str(channel.type).title(), inline=True)
        embed.add_field(name="🆔 Channel ID", value=channel.id, inline=True)

        if hasattr(channel, 'category') and channel.category:
            embed.add_field(name="📁 Category", value=channel.category.name, inline=True)

        embed.set_footer(text=f"Created by: {channel.guild.name}")

        try:
            await log_channel.send(embed=embed)
        except discord.Forbidden:
            pass  # Can't send to channel

@bot.event
async def on_guild_channel_delete(channel):
    """Log when a channel is deleted"""
    guild_id = channel.guild.id

    if guild_id in log_channels:
        log_channel = bot.get_channel(log_channels[guild_id])

        embed = discord.Embed(
            title="📺 Channel Deleted",
            description=f"Channel deleted: #{channel.name}",
            color=0xff0000
        )

        embed.add_field(name="📝 Channel Name", value=channel.name, inline=True)
        embed.add_field(name="📝 Channel Type", value=str(channel.type).title(), inline=True)
        embed.add_field(name="🆔 Channel ID", value=channel.id, inline=True)

        if hasattr(channel, 'category') and channel.category:
            embed.add_field(name="📁 Category", value=channel.category.name, inline=True)

        embed.set_footer(text=f"Deleted from: {channel.guild.name}")

        try:
            await log_channel.send(embed=embed)
        except discord.Forbidden:
            pass  # Can't send to channel

# Bot events
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print(f'Bot ID: {bot.user.id}')
    print(f'Connected to {len(bot.guilds)} servers')
    print('------')

    # Sync slash commands with Discord
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
        print('Available commands:')
        for command in bot.tree.get_commands():
            print(f'  - /{command.name}: {command.description}')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.event
async def on_command(ctx):
    """Log when commands are executed"""
    print(f'Command executed: {ctx.command.name} by {ctx.author.name}#{ctx.author.discriminator}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing required arguments. Use `!help` for command usage.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `!help` for available commands.")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")
        print(f"Error: {error}")

# Utility Commands
@bot.command(name='ping')
async def ping(ctx):
    """Check bot latency"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency: {latency}ms",
        color=0x00ff00
    )
    await ctx.send(embed=embed)

# Store last help command execution time per user
last_help_execution = {}

@bot.command(name='help')
async def help_command(ctx):
    """Interactive help with categories and buttons"""
    embed = discord.Embed(
        title="🤖 Comandos del Bot",
        description="¡Bienvenido al sistema de ayuda interactivo!\n\n"
                   "Usa los botones para navegar por las diferentes categorías de comandos.\n"
                   "Cada categoría contiene comandos relacionados agrupados por funcionalidad.",
        color=0x0099ff
    )

    embed.add_field(
        name="📊 Estadísticas",
        value=f"**Categorías:** 6\n"
              f"**Comandos totales:** 30+\n"
              f"**Última actualización:** {datetime.now().strftime('%d/%m/%Y')}",
        inline=False
    )

    embed.add_field(
        name="💡 Consejos",
        value="• Usa `!help` para ver todos los comandos en una lista\n"
              "• Usa `!commands` para una lista simple de comandos\n"
              "• Cada comando debe empezar con `!`",
        inline=False
    )

    embed.set_footer(text="Este menú se cerrará automáticamente en 5 minutos")

    view = HelpView(ctx)
    await ctx.send(embed=embed, view=view)

# Interactive Help Command with Categories
class HelpView(View):
    def __init__(self, ctx):
        super().__init__(timeout=300)  # 5 minutes timeout
        self.ctx = ctx
        self.current_category = None

    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author

    @discord.ui.button(label="📋 Categorías", style=discord.ButtonStyle.primary, emoji="📋")
    async def show_categories(self, interaction, button):
        embed = discord.Embed(
            title="📋 Lista de categorías",
            description="Selecciona una categoría para ver sus comandos:",
            color=0x0099ff
        )

        # Create select menu for categories
        select = Select(
            placeholder="Elige una categoría...",
            options=[
                discord.SelectOption(label="🛠️ Moderación", value="moderation", description="Comandos para moderar el servidor", emoji="🛠️"),
                discord.SelectOption(label="👤 Usuario", value="user", description="Comandos relacionados con usuarios", emoji="👤"),
                discord.SelectOption(label="🎲 Diversión", value="fun", description="Comandos de entretenimiento", emoji="🎲"),
                discord.SelectOption(label="🔧 Utilidad", value="utility", description="Comandos útiles y herramientas", emoji="🔧"),
                discord.SelectOption(label="🎯 Comunidad", value="community", description="Comandos para la comunidad", emoji="🎯"),
                discord.SelectOption(label="📊 Información", value="info", description="Comandos de información", emoji="📊"),
            ]
        )

        view = CategorySelectView(self.ctx, select)
        select.callback = view.category_select_callback

        embed.set_footer(text="Usa el menú desplegable para seleccionar una categoría")
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="❌ Cerrar", style=discord.ButtonStyle.danger, emoji="❌")
    async def close_help(self, interaction, button):
        await interaction.response.edit_message(content="❌ Ayuda cerrada.", embed=None, view=None)

class CategorySelectView(View):
    def __init__(self, ctx, select_component):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.add_item(select_component)

    async def category_select_callback(self, interaction):
        selected_category = interaction.data['values'][0]

        # Command categories
        categories = {
            "moderation": {
                "name": "🛠️ Moderación",
                "description": "Comandos para moderar el servidor",
                "commands": {
                    "`!purge <cantidad>`": "Eliminar mensajes",
                    "`!kick <usuario> [razón]`": "Expulsar a un usuario",
                    "`!ban <usuario> [razón]`": "Banear a un usuario",
                    "`!unban <user_id>`": "Desbanear a un usuario",
                    "`!warn <usuario> [razón]`": "Advertir a un usuario"
                },
                "color": 0xff0000
            },
            "user": {
                "name": "👤 Usuario",
                "description": "Comandos relacionados con usuarios",
                "commands": {
                    "`!avatar [@usuario]`": "Obtener el avatar de un usuario",
                    "`!userinfo [@usuario]`": "Obtener información de un usuario",
                    "`!banner [@usuario]`": "Obtener el banner de un usuario"
                },
                "color": 0x0099ff
            },
            "fun": {
                "name": "🎲 Diversión",
                "description": "Comandos de entretenimiento",
                "commands": {
                    "`!roll <dados>`": "Tirar dados (ej: 1d20)",
                    "`!coinflip`": "Lanzar una moneda",
                    "`!joke`": "Obtener un chiste aleatorio",
                    "`!fact`": "Obtener un dato curioso",
                    "`!meme`": "Obtener un meme de programador"
                },
                "color": 0xff9900
            },
            "utility": {
                "name": "🔧 Utilidad",
                "description": "Comandos útiles y herramientas",
                "commands": {
                    "`!say <mensaje>`": "Hacer que el bot diga algo",
                    "`!ping`": "Verificar la latencia del bot",
                    "`!help`": "Mostrar esta ayuda",
                    "`!commands`": "Lista simple de comandos"
                },
                "color": 0x00ff00
            },
            "community": {
                "name": "🎯 Comunidad",
                "description": "Comandos para la comunidad",
                "commands": {
                    "`!poll <pregunta>`": "Crear una encuesta",
                    "`!remind <minutos> <mensaje>`": "Establecer un recordatorio",
                    "`!weather <ciudad>`": "Obtener información del clima",
                    "`!calc <expresión>`": "Calculadora simple",
                    "`!urban <término>`": "Buscar en Urban Dictionary"
                },
                "color": 0xff69b4
            },
            "info": {
                "name": "📊 Información",
                "description": "Comandos de información",
                "commands": {
                    "`!serverinfo`": "Obtener información del servidor",
                    "`!serverstats`": "Estadísticas detalladas del servidor",
                    "`!roleinfo <rol>`": "Obtener información de un rol",
                    "`!channelinfo [canal]`": "Obtener información de un canal"
                },
                "color": 0x9932cc
            }
        }

        category = categories[selected_category]
        embed = discord.Embed(
            title=category["name"],
            description=category["description"],
            color=category["color"]
        )

        # Add commands to embed
        for command, description in category["commands"].items():
            embed.add_field(name=command, value=description, inline=False)

        embed.set_footer(text=f"Total de comandos: {len(category['commands'])} | Usa ! antes de cada comando")

        # Create back button
        view = View()
        back_button = Button(label="⬅️ Volver", style=discord.ButtonStyle.secondary, emoji="⬅️")
        async def back_callback(interaction):
            embed = discord.Embed(
                title="📋 Lista de categorías",
                description="Selecciona una categoría para ver sus comandos:",
                color=0x0099ff
            )
            embed.set_footer(text="Usa el menú desplegable para seleccionar una categoría")
            await interaction.response.edit_message(embed=embed, view=HelpView(self.ctx))

        back_button.callback = back_callback
        view.add_item(back_button)

        await interaction.response.edit_message(embed=embed, view=view)

@bot.command(name='help_interactive')
async def help_interactive(ctx):
    """Interactive help with categories and buttons"""
    embed = discord.Embed(
        title="🤖 Comandos del Bot",
        description="¡Bienvenido al sistema de ayuda interactivo!\n\n"
                   "Usa los botones para navegar por las diferentes categorías de comandos.\n"
                   "Cada categoría contiene comandos relacionados agrupados por funcionalidad.",
        color=0x0099ff
    )

    embed.add_field(
        name="📊 Estadísticas",
        value=f"**Categorías:** 6\n"
              f"**Comandos totales:** 30+\n"
              f"**Última actualización:** {datetime.now().strftime('%d/%m/%Y')}",
        inline=False
    )

    embed.add_field(
        name="💡 Consejos",
        value="• Usa `!help` para ver todos los comandos en una lista\n"
              "• Usa `!commands` para una lista simple de comandos\n"
              "• Cada comando debe empezar con `!`",
        inline=False
    )

    embed.set_footer(text="Este menú se cerrará automáticamente en 5 minutos")

    view = HelpView(ctx)
    await ctx.send(embed=embed, view=view)

@bot.command(name='commands')
async def commands_list(ctx):
    """Show all available commands in a simple list"""
    commands_list = [
        "🛠️ **Moderation:**",
        "• `!purge <amount>` - Delete messages",
        "• `!kick <user> [reason]` - Kick a user",
        "• `!ban <user> [reason]` - Ban a user",
        "• `!unban <user_id>` - Unban a user",
        "• `!warn <user> [reason]` - Warn a user",
        "",
        "👤 **User Commands:**",
        "• `!avatar [@user]` - Get user avatar",
        "• `!userinfo [@user]` - Get user information",
        "• `!banner [@user]` - Get user banner",
        "• `!serverinfo` - Get server information",
        "• `!roleinfo <role>` - Get role information",
        "• `!channelinfo [channel]` - Get channel info",
        "",
        "🎲 **Fun Commands:**",
        "• `!roll <dice>` - Roll dice (e.g., 1d20)",
        "• `!coinflip` - Flip a coin",
        "• `!joke` - Get a random joke",
        "• `!fact` - Get a random fact",
        "• `!meme` - Get a programmer meme",
        "",
        "🔧 **Utility:**",
        "• `!say <message>` - Make bot say something",
        "• `!ping` - Check bot latency",
        "• `!help` - Show detailed help with categories",
        "• `!commands` - Show this simple list",
        "",
        "⚠️ **Community:**",
        "• `!poll <question>` - Create a poll",
        "• `!remind <minutes> <message>` - Set a reminder",
        "• `!weather <city>` - Get weather info",
        "• `!calc <expression>` - Simple calculator",
        "• `!urban <term>` - Search Urban Dictionary",
        "• `!serverstats` - Detailed server statistics"
    ]

    embed = discord.Embed(
        title="📋 All Bot Commands",
        description="\n".join(commands_list),
        color=0x00ff00
    )

    embed.set_footer(text="Total Commands: 30+ | Use ! before each command")
    await ctx.send(embed=embed)

# Moderation Commands
@bot.command(name='purge')
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    """Delete a specified number of messages"""
    if amount > 100:
        await ctx.send("❌ You can only delete up to 100 messages at once.")
        return

    if amount < 1:
        await ctx.send("❌ Please specify a positive number.")
        return

    deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
    confirmation = await ctx.send(f"✅ Deleted {len(deleted) - 1} messages.")
    await asyncio.sleep(3)
    await confirmation.delete()

@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kick a user from the server"""
    if member == ctx.author:
        await ctx.send("❌ You can't kick yourself!")
        return

    if ctx.author.top_role <= member.top_role:
        await ctx.send("❌ You can't kick someone with a higher or equal role!")
        return

    try:
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="👢 User Kicked",
            description=f"{member.mention} has been kicked.",
            color=0xff9900
        )
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to kick this user.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ Failed to kick user: {e}")

@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """Ban a user from the server"""
    if member == ctx.author:
        await ctx.send("❌ You can't ban yourself!")
        return

    if ctx.author.top_role <= member.top_role:
        await ctx.send("❌ You can't ban someone with a higher or equal role!")
        return

    try:
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="🔨 User Banned",
            description=f"{member.mention} has been banned.",
            color=0xff0000
        )
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to ban this user.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ Failed to ban user: {e}")

@bot.command(name='unban')
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    """Unban a user from the server"""
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        embed = discord.Embed(
            title="✅ User Unbanned",
            description=f"{user.mention} has been unbanned.",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    except discord.NotFound:
        await ctx.send("❌ User not found or not banned.")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to unban users.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ Failed to unban user: {e}")

# User Commands
@bot.command(name='avatar')
async def avatar(ctx, member: discord.Member = None):
    """Get a user's avatar"""
    if member is None:
        member = ctx.author

    embed = discord.Embed(
        title=f"{member.display_name}'s Avatar",
        color=0x0099ff
    )
    embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="User", value=member.mention, inline=True)
    embed.add_field(name="User ID", value=member.id, inline=True)
    await ctx.send(embed=embed)

@bot.command(name='userinfo')
async def userinfo(ctx, member: discord.Member = None):
    """Get information about a user"""
    if member is None:
        member = ctx.author

    # Calculate relative time for created and joined dates
    def get_relative_time(date):
        now = datetime.now(date.tzinfo)
        diff = now - date

        years = diff.days // 365
        months = diff.days // 30
        days = diff.days
        hours = diff.seconds // 3600

        if years > 0:
            return f"{years} year(s) ago"
        elif months > 0:
            return f"{months} month(s) ago"
        elif days > 0:
            return f"{days} day(s) ago"
        else:
            return f"{hours} hour(s) ago"

    embed = discord.Embed(color=0x2f3136)  # Dark gray color like Discord

    # Set user avatar as the main image (left side)
    embed.set_author(
        name=f"{member.name} #{member.discriminator}",
        icon_url=member.avatar.url if member.avatar else member.default_avatar.url
    )

    # Add Discord icon/branding (using a Discord emoji or similar)
    embed.add_field(
        name="\u200B",
        value=f"**{member.mention}**",
        inline=False
    )

    # Add activity/status information if available
    if member.activity:
        activity_text = f"Playing **{member.activity.name}**"
        if hasattr(member.activity, 'details') and member.activity.details:
            activity_text += f"\n*{member.activity.details}*"
        embed.add_field(name="\u200B", value=activity_text, inline=False)

    # Add created and joined dates with relative time
    created_relative = get_relative_time(member.created_at)
    joined_relative = get_relative_time(member.joined_at)

    embed.add_field(
        name="📅 Created",
        value=f"{created_relative}\n*{member.created_at.strftime('%m/%d/%Y, %I:%M %p')}*",
        inline=True
    )

    embed.add_field(
        name="📅 Joined",
        value=f"{joined_relative}\n*{member.joined_at.strftime('%m/%d/%Y, %I:%M %p')}*",
        inline=True
    )

    # Add empty field for spacing
    embed.add_field(name="\u200B", value="\u200B", inline=True)

    # Add user information
    embed.add_field(
        name="👤 User Information",
        value=f"**Display Name:** {member.display_name}\n"
              f"**User ID:** {member.id}\n"
              f"**Bot:** {'Yes' if member.bot else 'No'}\n"
              f"**Status:** {str(member.status).title()}",
        inline=False
    )

    # Add role information if they have roles
    if len(member.roles) > 1:  # More than just @everyone
        roles = [role.mention for role in member.roles[1:]]  # Skip @everyone
        embed.add_field(
            name="🏆 Roles",
            value=", ".join(roles[:5]) + ("..." if len(roles) > 5 else ""),
            inline=False
        )

    # Add footer with links
    embed.set_footer(text="Created • Joined • Links • Avatar")

    await ctx.send(embed=embed)

@bot.command(name='banner')
async def banner(ctx, member: discord.Member = None):
    """Get a user's banner"""
    if member is None:
        member = ctx.author

    embed = discord.Embed(
        title=f"{member.display_name}'s Banner",
        color=0x0099ff
    )

    # Set user avatar as thumbnail
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

    try:
        # Use Discord API to get user data including banner
        headers = {"Authorization": f"Bot {TOKEN}"}
        response = requests.get(f"https://discord.com/api/v10/users/{member.id}", headers=headers)

        if response.status_code == 200:
            user_data = response.json()

            # Check if user has a banner
            if user_data.get('banner'):
                banner_hash = user_data['banner']
                # Construct banner URL with larger size for better display
                banner_url = f"https://cdn.discordapp.com/banners/{member.id}/{banner_hash}.png?size=1024"

                # Set the banner image
                embed.set_image(url=banner_url)
                embed.add_field(name="User", value=member.mention, inline=True)
                embed.add_field(name="User ID", value=member.id, inline=True)
                embed.add_field(name="Status", value="✅ Has Banner", inline=True)
            else:
                # User doesn't have a banner, send simple message instead of embed
                await ctx.send(f"❌ {member.mention} doesn't have a banner set.")
                return
        else:
            # If API call fails, show default image
            embed.set_image(url="https://i.imgur.com/3YcB3iV.png")  # Default banner image
            embed.add_field(name="User", value=member.mention, inline=True)
            embed.add_field(name="User ID", value=member.id, inline=True)
            embed.add_field(name="Status", value="❌ API Error", inline=True)

    except Exception as e:
        # If all methods fail, show default image
        embed.set_image(url="https://i.imgur.com/3YcB3iV.png")  # Default banner image
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Status", value="❌ Error Loading", inline=True)
        print(f"Error loading banner: {e}")

    embed.set_footer(text="Use !banner @user to see someone else's banner")
    await ctx.send(embed=embed)

@bot.command(name='serverinfo')
async def serverinfo(ctx):
    """Get information about the server"""
    guild = ctx.guild

    # Calculate member stats
    total_members = guild.member_count
    bot_count = len([m for m in guild.members if m.bot])
    human_count = total_members - bot_count

    # Calculate channel stats
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)

    embed = discord.Embed(
        title=f"{guild.name}",
        color=0x2f3136  # Dark gray like Discord
    )

    # Set server icon as thumbnail
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    # Description section
    embed.add_field(
        name="📝 Descripción",
        value=guild.description if guild.description else "No tiene descripción",
        inline=False
    )

    # Info General section
    embed.add_field(
        name="📋 Info General",
        value=f"🏷️ **Nombre:** {guild.name}\n"
              f"🆔 **ID:** {guild.id}\n"
              f"📅 **Creación:** {guild.created_at.strftime('%d de %B de %Y')} (hace {((datetime.now().date() - guild.created_at.date()).days // 30)} meses)\n"
              f"👑 **Propietario:** {guild.owner.mention}\n"
              f"🔗 **URL personalizada:** No tiene\n"
              f"🛡️ **MFA Level:** {guild.mfa_level}\n"
              f"🌍 **Región:** Unknown",
        inline=False
    )

    # Statistics section - Users
    embed.add_field(
        name="👥 Usuarios",
        value=f"👤 **Miembros:** {human_count}\n"
              f"🤖 **Bots:** {bot_count}\n"
              f"🎭 **Roles:** {len(guild.roles)}\n"
              f"🚫 **Baneados:** 0",
        inline=True
    )

    # Statistics section - Best of server
    embed.add_field(
        name="⭐ Mejores del servidor",
        value=f"⭐ **Nivel:** 0\n"
              f"😀 **Emojis:** {len(guild.emojis)}\n"
              f"🚀 **Boosts:** {guild.premium_subscription_count}",
        inline=True
    )

    # Statistics section - Channels
    embed.add_field(
        name=f"📺 Canales ({text_channels + voice_channels + categories})",
        value=f"💬 **Texto:** {text_channels}\n"
              f"🔊 **Voz:** {voice_channels}\n"
              f"📰 **Hilos:** 0\n"
              f"📁 **Categorías:** {categories}",
        inline=True
    )

    # Server features
    features = []
    if "COMMUNITY" in guild.features:
        features.append("🏘️ Comunidad")
    if "ANIMATED_ICON" in guild.features:
        features.append("🎨 Icono Animado")
    if "BANNER" in guild.features:
        features.append("🖼️ Banner")

    if features:
        embed.add_field(
            name="✨ Características",
            value="\n".join(features),
            inline=False
        )

    # Footer with server ID
    embed.set_footer(text=f"Fecha de tu ingreso: {ctx.author.joined_at.strftime('%d/%m/%Y %H:%M') if ctx.author.joined_at else 'Unknown'}")

    await ctx.send(embed=embed)

# Fun Commands
@bot.command(name='roll')
async def roll(ctx, dice: str = "1d6"):
    """Roll dice (format: NdM)"""
    try:
        parts = dice.lower().split('d')
        if len(parts) != 2:
            await ctx.send("❌ Invalid format. Use: `!roll NdM` (e.g., 2d20)")
            return

        num_dice = int(parts[0])
        num_sides = int(parts[1])

        if num_dice > 20:
            await ctx.send("❌ You can roll a maximum of 20 dice.")
            return

        if num_sides > 1000:
            await ctx.send("❌ Dice can have a maximum of 1000 sides.")
            return

        if num_dice < 1 or num_sides < 2:
            await ctx.send("❌ Invalid dice configuration.")
            return

        results = [random.randint(1, num_sides) for _ in range(num_dice)]
        total = sum(results)

        embed = discord.Embed(
            title="🎲 Dice Roll",
            description=f"Rolling {dice}",
            color=0xff9900
        )

        if len(results) <= 10:
            embed.add_field(name="Results", value=", ".join(map(str, results)), inline=False)
        else:
            embed.add_field(name="Results", value=f"Too many to show individually", inline=False)

        embed.add_field(name="Total", value=str(total), inline=True)
        embed.add_field(name="Average", value=f"{total/num_dice:.1f}", inline=True)

        await ctx.send(embed=embed)

    except ValueError:
        await ctx.send("❌ Invalid format. Use: `!roll NdM` (e.g., 2d20)")

@bot.command(name='coinflip')
async def coinflip(ctx):
    """Flip a coin"""
    result = random.choice(["Heads", "Tails"])

    embed = discord.Embed(
        title="🪙 Coin Flip",
        description=f"Result: **{result}**",
        color=0xffd700
    )

    await ctx.send(embed=embed)

# Utility Commands
@bot.command(name='say')
async def say(ctx, *, message):
    """Make the bot say something"""
    # Delete the original command message
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass  # If we can't delete, just continue

    # Create embed for better formatting
    embed = discord.Embed(
        description=message,
        color=0x0099ff
    )
    embed.set_footer(text=f"Requested by {ctx.author.display_name}")

    await ctx.send(embed=embed)

# Community Bot Commands
@bot.command(name='warn')
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    """Warn a user"""
    embed = discord.Embed(
        title="⚠️ User Warned",
        description=f"{member.mention} has been warned.",
        color=0xffaa00
    )
    if reason:
        embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_footer(text=f"Warned by {ctx.author.display_name}")
    await ctx.send(embed=embed)

@bot.command(name='poll')
async def poll(ctx, *, question):
    """Create a poll"""
    embed = discord.Embed(
        title="📊 Poll",
        description=question,
        color=0x00ff00
    )
    embed.set_footer(text=f"Poll created by {ctx.author.display_name}")

    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")

@bot.command(name='remind')
async def remind(ctx, time: int, *, message):
    """Set a reminder (time in minutes)"""
    if time < 1 or time > 1440:  # Max 24 hours
        await ctx.send("❌ Time must be between 1 minute and 24 hours.")
        return

    embed = discord.Embed(
        title="⏰ Reminder Set",
        description=f"I'll remind you in {time} minutes: {message}",
        color=0x00aaff
    )
    await ctx.send(embed=embed)

    await asyncio.sleep(time * 60)

    embed = discord.Embed(
        title="⏰ Reminder",
        description=message,
        color=0xffaa00
    )
    embed.set_footer(text=f"Reminder for {ctx.author.display_name}")
    await ctx.author.send(embed=embed)

@bot.command(name='weather')
async def weather(ctx, *, city):
    """Get weather information"""
    try:
        # Using a simple weather API (you'd need to replace with a real API key)
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=your_api_key&units=metric")
        data = response.json()

        if data.get("cod") != 200:
            await ctx.send("❌ City not found.")
            return

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]

        embed = discord.Embed(
            title=f"🌤️ Weather in {city}",
            color=0x87ceeb
        )
        embed.add_field(name="Temperature", value=f"{temp}°C", inline=True)
        embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
        embed.add_field(name="Condition", value=description.title(), inline=False)

        await ctx.send(embed=embed)
    except:
        await ctx.send("❌ Weather service temporarily unavailable.")

@bot.command(name='joke')
async def joke(ctx):
    """Get a random joke"""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "What do you call a bear with no teeth? A gummy bear!"
    ]

    embed = discord.Embed(
        title="😂 Random Joke",
        description=random.choice(jokes),
        color=0xff69b4
    )
    await ctx.send(embed=embed)

@bot.command(name='fact')
async def fact(ctx):
    """Get a random fact"""
    facts = [
        "A group of flamingos is called a 'flamboyance'.",
        "The shortest war in history lasted only 38-45 minutes.",
        "Octopuses have three hearts and blue blood.",
        "A day on Venus is longer than its year.",
        "There are more possible games of chess than atoms in the observable universe."
    ]

    embed = discord.Embed(
        title="🧠 Random Fact",
        description=random.choice(facts),
        color=0x9932cc
    )
    await ctx.send(embed=embed)

@bot.command(name='calc')
async def calc(ctx, *, expression):
    """Simple calculator"""
    try:
        # Basic security check
        if any(char in expression for char in ['import', 'exec', 'eval', '__']):
            await ctx.send("❌ Invalid expression.")
            return

        result = eval(expression)
        embed = discord.Embed(
            title="🧮 Calculator",
            description=f"**Expression:** {expression}\n**Result:** {result}",
            color=0x00ff7f
        )
        await ctx.send(embed=embed)
    except:
        await ctx.send("❌ Invalid mathematical expression.")

@bot.command(name='urban')
async def urban(ctx, *, term):
    """Search Urban Dictionary"""
    try:
        # This would need a real Urban Dictionary API
        embed = discord.Embed(
            title=f"📖 Urban Dictionary: {term}",
            description="Urban Dictionary API not configured.\nThis is a demo response.",
            color=0xff4500
        )
        embed.add_field(name="Definition", value="This would show the definition if API was configured.", inline=False)
        await ctx.send(embed=embed)
    except:
        await ctx.send("❌ Urban Dictionary service unavailable.")

@bot.command(name='meme')
async def meme(ctx):
    """Get a random meme"""
    memes = [
        "When you spend 2 hours on a bug that was just a missing semicolon",
        "Me: 'I'll just fix this quickly'\n*5 hours later*\nAlso me: 'It works... somehow'",
        "When you finally understand recursion:\n'I don't think about it too much'",
        "Git commit messages be like:\n'Fixed stuff'\n'Works now'\n'Please work'",
        "When you find a bug in production:\n*Pretends nothing happened*"
    ]

    embed = discord.Embed(
        title="😂 Programmer Meme",
        description=random.choice(memes),
        color=0xff1493
    )
    await ctx.send(embed=embed)

@bot.command(name='roleinfo')
async def roleinfo(ctx, role: discord.Role):
    """Get information about a role"""
    embed = discord.Embed(
        title=f"Role Information - {role.name}",
        color=role.color
    )

    embed.add_field(name="👥 Members", value=len(role.members), inline=True)
    embed.add_field(name="🎨 Color", value=str(role.color), inline=True)
    embed.add_field(name="📅 Created", value=role.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="🔼 Position", value=role.position, inline=True)
    embed.add_field(name="💬 Mentionable", value="Yes" if role.mentionable else "No", inline=True)
    embed.add_field(name="🗂️ Hoisted", value="Yes" if role.hoist else "No", inline=True)

    permissions = []
    if role.permissions.administrator:
        permissions.append("Administrator")
    if role.permissions.manage_guild:
        permissions.append("Manage Server")
    if role.permissions.manage_roles:
        permissions.append("Manage Roles")
    if role.permissions.manage_channels:
        permissions.append("Manage Channels")
    if role.permissions.kick_members:
        permissions.append("Kick Members")
    if role.permissions.ban_members:
        permissions.append("Ban Members")

    if permissions:
        embed.add_field(name="🔑 Key Permissions", value=", ".join(permissions), inline=False)

    await ctx.send(embed=embed)

@bot.command(name='channelinfo')
async def channelinfo(ctx, channel: discord.TextChannel = None):
    """Get information about a channel"""
    if channel is None:
        channel = ctx.channel

    embed = discord.Embed(
        title=f"Channel Information - #{channel.name}",
        color=0x7289da
    )

    embed.add_field(name="📝 Topic", value=channel.topic or "No topic set", inline=False)
    embed.add_field(name="👥 Members", value=len(channel.members), inline=True)
    embed.add_field(name="📅 Created", value=channel.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="🔞 NSFW", value="Yes" if channel.nsfw else "No", inline=True)
    embed.add_field(name="📌 Pinned Messages", value=len(await channel.pins()), inline=True)

    # Channel permissions
    permissions = []
    if channel.permissions_for(ctx.guild.me).read_messages:
        permissions.append("Read Messages")
    if channel.permissions_for(ctx.guild.me).send_messages:
        permissions.append("Send Messages")
    if channel.permissions_for(ctx.guild.me).embed_links:
        permissions.append("Embed Links")

    embed.add_field(name="🤖 Bot Permissions", value=", ".join(permissions), inline=False)

    await ctx.send(embed=embed)

@bot.command(name='serverstats')
async def serverstats(ctx):
    """Get detailed server statistics"""
    guild = ctx.guild

    embed = discord.Embed(
        title=f"📊 Server Statistics - {guild.name}",
        color=0x00ff00
    )

    # Member stats
    total_members = guild.member_count
    bot_count = len([m for m in guild.members if m.bot])
    human_count = total_members - bot_count

    embed.add_field(name="👥 Total Members", value=total_members, inline=True)
    embed.add_field(name="👤 Humans", value=human_count, inline=True)
    embed.add_field(name="🤖 Bots", value=bot_count, inline=True)

    # Activity stats
    online_count = len([m for m in guild.members if str(m.status) == "online"])
    idle_count = len([m for m in guild.members if str(m.status) == "idle"])
    dnd_count = len([m for m in guild.members if str(m.status) == "dnd"])
    offline_count = len([m for m in guild.members if str(m.status) == "offline"])

    embed.add_field(name="🟢 Online", value=online_count, inline=True)
    embed.add_field(name="🟡 Idle", value=idle_count, inline=True)
    embed.add_field(name="🔴 Do Not Disturb", value=dnd_count, inline=True)
    embed.add_field(name="⚫ Offline", value=offline_count, inline=True)

    # Channel stats
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)

    embed.add_field(name="💬 Text Channels", value=text_channels, inline=True)
    embed.add_field(name="🔊 Voice Channels", value=voice_channels, inline=True)
    embed.add_field(name="📁 Categories", value=categories, inline=True)

    # Role stats
    role_count = len(guild.roles)
    embed.add_field(name="🎭 Roles", value=role_count, inline=True)

    # Emoji stats
    emoji_count = len(guild.emojis)
    embed.add_field(name="😀 Emojis", value=emoji_count, inline=True)

    embed.set_footer(text=f"Server ID: {guild.id} | Generated on {datetime.now().strftime('%B %d, %Y %H:%M')}")
    await ctx.send(embed=embed)

# Error handlers for missing permissions
@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need `Manage Messages` permission to use this command.")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need `Kick Members` permission to use this command.")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need `Ban Members` permission to use this command.")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need `Ban Members` permission to use this command.")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ DISCORD_BOT_TOKEN not found in environment variables.")
        print("Please create a .env file with your bot token:")
        print("DISCORD_BOT_TOKEN=your_bot_token_here")
