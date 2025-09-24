import discord
from discord.ext import commands
from discord.ui import Button, View, Select
from datetime import datetime
import asyncio
import requests

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash Commands
    @discord.app_commands.command(name="logs", description="Configure logging for server events")
    @commands.has_permissions(administrator=True)
    async def setup_logs(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Set up logging for server events"""
        guild_id = interaction.guild.id

        # Store the log channel for this guild
        self.bot.log_channels[guild_id] = channel.id

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

    @discord.app_commands.command(name="logs-disable", description="Disable logging for server events")
    @commands.has_permissions(administrator=True)
    async def disable_logs(self, interaction: discord.Interaction):
        """Disable logging for server events"""
        guild_id = interaction.guild.id

        if guild_id not in self.bot.log_channels:
            await interaction.response.send_message("❌ Logging is not currently configured for this server.", ephemeral=True)
            return

        # Remove the log channel configuration
        del self.bot.log_channels[guild_id]

        embed = discord.Embed(
            title="📋 Logging Disabled",
            description="✅ Server logging has been disabled.",
            color=0xff0000
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Send a notification to the previously configured channel
        try:
            channel = self.bot.get_channel(self.bot.log_channels.get(guild_id))
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

    @discord.app_commands.command(name="logs-status", description="Check logging status")
    async def logs_status(self, interaction: discord.Interaction):
        """Check the current logging status"""
        guild_id = interaction.guild.id

        if guild_id in self.bot.log_channels:
            channel = self.bot.get_channel(self.bot.log_channels[guild_id])
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

    @discord.app_commands.command(name="setup", description="Create koala setup category with logs-server and jail channels")
    @commands.has_permissions(administrator=True)
    async def setup_koala_system(self, interaction: discord.Interaction):
        """Create a koala setup category with logs-server and jail channels"""
        guild_id = interaction.guild.id

        # Check if logging is already configured
        if guild_id in self.bot.log_channels:
            channel = self.bot.get_channel(self.bot.log_channels[guild_id])
            await interaction.response.send_message(
                f"❌ Logging is already configured for {channel.mention}. Use `/logs-disable` first if you want to reconfigure.",
                ephemeral=True
            )
            return

        # Defer the response to prevent timeout
        await interaction.response.defer(ephemeral=True)

        try:
            # Create the koala setup category
            category = await interaction.guild.create_category(
                name="koala setup",
                reason="Auto-created by setup command"
            )

            # Create the jailed role first
            jailed_role = await interaction.guild.create_role(
                name="jailed",
                color=0x808080,  # Gray color
                reason="Auto-created by setup command for jail system"
            )

            # Create the logs-server channel (private by default)
            logs_overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
                interaction.guild.owner: discord.PermissionOverwrite(read_messages=True, send_messages=False)
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
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True, manage_channels=True),
                jailed_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, view_channel=True)
            }

            jail_channel = await interaction.guild.create_text_channel(
                name="jail",
                category=category,
                overwrites=jail_overwrites,
                reason="Auto-created by setup command"
            )

            # Set up permissions for existing channels to hide them from jailed users
            for channel in interaction.guild.channels:
                if channel != jail_channel and channel != category:
                    # Deny view permissions for jailed role on all existing channels
                    await channel.set_permissions(jailed_role, view_channel=False, read_messages=False, send_messages=False)

            # Configure logging to use the logs channel
            self.bot.log_channels[guild_id] = logs_channel.id

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

            await interaction.followup.send(embed=embed, ephemeral=True)

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
            await interaction.followup.send(
                "❌ I don't have permission to create channels or categories in this server.",
                ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.followup.send(
                f"❌ Failed to create koala setup: {e}",
                ephemeral=True
            )

    @commands.command(name='jail')
    @commands.has_permissions(manage_roles=True)
    async def jail(self, ctx, member: discord.Member = None, *, reason=None):
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
        if guild_id in self.bot.jail_data and member.id in self.bot.jail_data[guild_id]:
            await ctx.send(f"❌ {member.mention} is already in jail!")
            return

        try:
            # Find jail channel in "koala setup" category
            jail_channel = None
            koala_category = None

            # Find the koala setup category
            for category in ctx.guild.categories:
                if category.name == "koala setup":
                    koala_category = category
                    break

            if koala_category:
                # Look for jail channel in the koala setup category
                for channel in koala_category.channels:
                    if channel.name == "jail":
                        jail_channel = channel
                        break

            if jail_channel is None:
                # Create jail channel in koala setup category if it exists
                if koala_category:
                    overwrites = {
                        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True, manage_channels=True),
                        member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                    }

                    jail_channel = await ctx.guild.create_text_channel(
                        name="jail",
                        category=koala_category,
                        overwrites=overwrites,
                        reason=f"Jail channel created for {member.name}"
                    )
                else:
                    # Fallback: create jail channel without category
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

            # Find and assign the "jailed" role
            jailed_role = None
            for role in ctx.guild.roles:
                if role.name == "jailed":
                    jailed_role = role
                    break

            if jailed_role:
                try:
                    await member.add_roles(jailed_role, reason=f"User jailed by {ctx.author.name}")
                except discord.Forbidden:
                    await ctx.send("❌ I don't have permission to assign the jailed role.")
                    return
                except discord.HTTPException as e:
                    await ctx.send(f"❌ Failed to assign jailed role: {e}")
                    return
            else:
                await ctx.send("❌ Could not find the 'jailed' role. Please run the setup command first.")
                return

            # Store jail data
            if guild_id not in self.bot.jail_data:
                self.bot.jail_data[guild_id] = {}

            self.bot.jail_data[guild_id][member.id] = {
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
            if guild_id in self.bot.log_channels:
                log_channel = self.bot.get_channel(self.bot.log_channels[guild_id])
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

    @commands.command(name='unjail')
    @commands.has_permissions(manage_roles=True)
    async def unjail(self, ctx, member: discord.Member = None, *, reason=None):
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
        if guild_id not in self.bot.jail_data or member.id not in self.bot.jail_data[guild_id]:
            await ctx.send(f"❌ {member.mention} is not in jail!")
            return

        try:
            jail_info = self.bot.jail_data[guild_id][member.id]

            # Find and remove the "jailed" role first
            jailed_role = None
            for role in ctx.guild.roles:
                if role.name == "jailed":
                    jailed_role = role
                    break

            if jailed_role:
                try:
                    await member.remove_roles(jailed_role, reason=f"User released from jail by {ctx.author.name}")
                except discord.Forbidden:
                    await ctx.send("❌ I don't have permission to remove the jailed role.")
                    return
                except discord.HTTPException as e:
                    await ctx.send(f"❌ Failed to remove jailed role: {e}")
                    return

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
            del self.bot.jail_data[guild_id][member.id]

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

            # Log the unjail action if logging is enabled
            if guild_id in self.bot.log_channels:
                log_channel = self.bot.get_channel(self.bot.log_channels[guild_id])
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

    @commands.command(name='jailstatus')
    @commands.has_permissions(manage_roles=True)
    async def jailstatus(self, ctx):
        """Check who is currently in jail"""
        guild_id = ctx.guild.id

        if guild_id not in self.bot.jail_data or not self.bot.jail_data[guild_id]:
            embed = discord.Embed(
                title="🔒 Jail Status",
                description="✅ No users are currently in jail.",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="🔒 Jail Status",
            description=f"📊 **Total jailed users:** {len(self.bot.jail_data[guild_id])}",
            color=0xff9900
        )

        for user_id, jail_info in self.bot.jail_data[guild_id].items():
            try:
                user = await self.bot.fetch_user(user_id)
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

    @commands.command(name='purge')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
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

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
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

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
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

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        """Unban a user from the server"""
        try:
            user = await self.bot.fetch_user(user_id)
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

    @commands.command(name='warn')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
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

    @commands.command(name='togglensfw')
    @commands.has_permissions(administrator=True)
    async def togglensfw(self, ctx):
        """Toggle NSFW commands on/off for this server"""
        from config.settings import nsfw_settings
        guild_id = ctx.guild.id

        if guild_id not in nsfw_settings:
            nsfw_settings[guild_id] = False

        nsfw_settings[guild_id] = not nsfw_settings[guild_id]

        status = "activados" if nsfw_settings[guild_id] else "desactivados"

        embed = discord.Embed(
            title="🔞 NSFW Toggle",
            description=f"Los comandos NSFW han sido **{status}** en este servidor.",
            color=0xff0000 if nsfw_settings[guild_id] else 0x00ff00
        )

        embed.set_footer(text="Solo administradores pueden cambiar esta configuración")

        await ctx.send(embed=embed)

    # Error handlers
    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You need `Manage Messages` permission to use this command.")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You need `Kick Members` permission to use this command.")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You need `Ban Members` permission to use this command.")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You need `Ban Members` permission to use this command.")

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
