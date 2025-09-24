import discord
from discord.ext import commands
from datetime import datetime

class LoggingEventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Log when a member joins the server"""
        guild_id = member.guild.id

        if guild_id in self.bot.log_channels:
            log_channel = self.bot.get_channel(self.bot.log_channels[guild_id])

            embed = discord.Embed(
                title="👋 Miembro se unió",
                description=f"{member.mention} se unió al servidor",
                color=0x00ff00
            )

            embed.add_field(name="👤 Usuario", value=f"{member.name}#{member.discriminator}", inline=True)
            embed.add_field(name="🆔 ID", value=member.id, inline=True)
            embed.add_field(name="📅 Cuenta creada", value=f"<t:{int(member.created_at.timestamp())}:F>", inline=False)

            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.timestamp = datetime.now()

            try:
                await log_channel.send(embed=embed)
            except discord.Forbidden:
                pass  # Can't send to log channel

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Log when a member leaves the server"""
        guild_id = member.guild.id

        if guild_id in self.bot.log_channels:
            log_channel = self.bot.get_channel(self.bot.log_channels[guild_id])

            embed = discord.Embed(
                title="👋 Miembro se fue",
                description=f"{member.name}#{member.discriminator} abandonó el servidor",
                color=0xff0000
            )

            embed.add_field(name="👤 Usuario", value=f"{member.name}#{member.discriminator}", inline=True)
            embed.add_field(name="🆔 ID", value=member.id, inline=True)
            embed.add_field(name="📅 Se unió", value=f"<t:{int(member.joined_at.timestamp())}:F>", inline=False)

            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.timestamp = datetime.now()

            try:
                await log_channel.send(embed=embed)
            except discord.Forbidden:
                pass

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Log when a message is deleted"""
        if message.author.bot:
            return  # Don't log bot messages

        guild_id = message.guild.id if message.guild else None

        if guild_id and guild_id in self.bot.log_channels:
            log_channel = self.bot.get_channel(self.bot.log_channels[guild_id])

            embed = discord.Embed(
                title="🗑️ Mensaje eliminado",
                description=f"Mensaje eliminado en {message.channel.mention}",
                color=0xffaa00
            )

            embed.add_field(name="👤 Autor", value=f"{message.author.name}#{message.author.discriminator}", inline=True)
            embed.add_field(name="📺 Canal", value=message.channel.name, inline=True)
            embed.add_field(name="🕐 Hora", value=f"<t:{int(message.created_at.timestamp())}:F>", inline=False)

            if message.content:
                embed.add_field(name="📝 Contenido", value=message.content[:1000], inline=False)

            if message.attachments:
                embed.add_field(name="📎 Adjuntos", value=f"{len(message.attachments)} archivo(s)", inline=True)

            embed.timestamp = datetime.now()

            try:
                await log_channel.send(embed=embed)
            except discord.Forbidden:
                pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Log when a message is edited"""
        if before.author.bot:
            return  # Don't log bot messages

        if before.content == after.content:
            return  # Don't log if only embeds changed

        guild_id = before.guild.id if before.guild else None

        if guild_id and guild_id in self.bot.log_channels:
            log_channel = self.bot.get_channel(self.bot.log_channels[guild_id])

            embed = discord.Embed(
                title="✏️ Mensaje editado",
                description=f"Mensaje editado en {before.channel.mention}",
                color=0x3498db
            )

            embed.add_field(name="👤 Autor", value=f"{before.author.name}#{before.author.discriminator}", inline=True)
            embed.add_field(name="📺 Canal", value=before.channel.name, inline=True)
            embed.add_field(name="🕐 Editado", value=f"<t:{int(after.edited_at.timestamp())}:F>", inline=False)

            if before.content:
                embed.add_field(name="📝 Antes", value=before.content[:500], inline=False)

            if after.content:
                embed.add_field(name="📝 Después", value=after.content[:500], inline=False)

            embed.timestamp = datetime.now()

            try:
                await log_channel.send(embed=embed)
            except discord.Forbidden:
                pass

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Log when a member updates their profile"""
        guild_id = after.guild.id

        if guild_id not in self.bot.log_channels:
            return

        log_channel = self.bot.get_channel(self.bot.log_channels[guild_id])

        # Check for nickname changes
        if before.nick != after.nick:
            embed = discord.Embed(
                title="📝 Cambio de nickname",
                description=f"{after.mention} cambió su nickname",
                color=0x9b59b6
            )

            embed.add_field(name="👤 Usuario", value=f"{after.name}#{after.discriminator}", inline=True)
            embed.add_field(name="📝 Antes", value=before.nick or "Ninguno", inline=True)
            embed.add_field(name="📝 Después", value=after.nick or "Ninguno", inline=True)

            embed.timestamp = datetime.now()

            try:
                await log_channel.send(embed=embed)
            except discord.Forbidden:
                pass

        # Check for role changes
        if set(before.roles) != set(after.roles):
            added_roles = [role for role in after.roles if role not in before.roles]
            removed_roles = [role for role in before.roles if role not in after.roles]

            if added_roles:
                embed = discord.Embed(
                    title="➕ Rol agregado",
                    description=f"{after.mention} recibió el rol {added_roles[0].mention}",
                    color=0x00ff00
                )

                embed.add_field(name="👤 Usuario", value=f"{after.name}#{after.discriminator}", inline=True)
                embed.add_field(name="📋 Rol", value=added_roles[0].name, inline=True)

                embed.timestamp = datetime.now()

                try:
                    await log_channel.send(embed=embed)
                except discord.Forbidden:
                    pass

            if removed_roles:
                embed = discord.Embed(
                    title="➖ Rol removido",
                    description=f"{after.mention} perdió el rol {removed_roles[0].mention}",
                    color=0xff0000
                )

                embed.add_field(name="👤 Usuario", value=f"{after.name}#{after.discriminator}", inline=True)
                embed.add_field(name="📋 Rol", value=removed_roles[0].name, inline=True)

                embed.timestamp = datetime.now()

                try:
                    await log_channel.send(embed=embed)
                except discord.Forbidden:
                    pass

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        """Log when a channel is created"""
        guild_id = channel.guild.id

        if guild_id in self.bot.log_channels:
            log_channel = self.bot.get_channel(self.bot.log_channels[guild_id])

            embed = discord.Embed(
                title="📺 Canal creado",
                description=f"Se creó el canal {channel.mention}",
                color=0x00ff00
            )

            embed.add_field(name="📺 Nombre", value=channel.name, inline=True)
            embed.add_field(name="📍 Tipo", value=type(channel).__name__, inline=True)

            if hasattr(channel, 'category') and channel.category:
                embed.add_field(name="📁 Categoría", value=channel.category.name, inline=True)

            embed.timestamp = datetime.now()

            try:
                await log_channel.send(embed=embed)
            except discord.Forbidden:
                pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        """Log when a channel is deleted"""
        guild_id = channel.guild.id

        if guild_id in self.bot.log_channels:
            log_channel = self.bot.get_channel(self.bot.log_channels[guild_id])

            embed = discord.Embed(
                title="📺 Canal eliminado",
                description=f"Se eliminó el canal #{channel.name}",
                color=0xff0000
            )

            embed.add_field(name="📺 Nombre", value=channel.name, inline=True)
            embed.add_field(name="📍 Tipo", value=type(channel).__name__, inline=True)

            if hasattr(channel, 'category') and channel.category:
                embed.add_field(name="📁 Categoría", value=channel.category.name, inline=True)

            embed.timestamp = datetime.now()

            try:
                await log_channel.send(embed=embed)
            except discord.Forbidden:
                pass

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        """Log when a role is created"""
        guild_id = role.guild.id

        if guild_id in self.bot.log_channels:
            log_channel = self.bot.get_channel(self.bot.log_channels[guild_id])

            embed = discord.Embed(
                title="📋 Rol creado",
                description=f"Se creó el rol {role.mention}",
                color=0x00ff00
            )

            embed.add_field(name="📋 Nombre", value=role.name, inline=True)
            embed.add_field(name="🆔 ID", value=role.id, inline=True)
            embed.add_field(name="🎨 Color", value=f"#{role.color.value:06x}" if role.color.value != 0 else "Default", inline=True)

            embed.timestamp = datetime.now()

            try:
                await log_channel.send(embed=embed)
            except discord.Forbidden:
                pass

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        """Log when a role is deleted"""
        guild_id = role.guild.id

        if guild_id in self.bot.log_channels:
            log_channel = self.bot.get_channel(self.bot.log_channels[guild_id])

            embed = discord.Embed(
                title="📋 Rol eliminado",
                description=f"Se eliminó el rol @{role.name}",
                color=0xff0000
            )

            embed.add_field(name="📋 Nombre", value=role.name, inline=True)
            embed.add_field(name="🆔 ID", value=role.id, inline=True)
            embed.add_field(name="🎨 Color", value=f"#{role.color.value:06x}" if role.color.value != 0 else "Default", inline=True)

            embed.timestamp = datetime.now()

            try:
                await log_channel.send(embed=embed)
            except discord.Forbidden:
                pass

async def setup(bot):
    await bot.add_cog(LoggingEventsCog(bot))
