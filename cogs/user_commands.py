import discord
from discord.ext import commands
import requests
from datetime import datetime

class UserCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='avatar')
    async def avatar(self, ctx, member: discord.Member = None):
        """Get a user's avatar"""
        if member is None:
            member = ctx.author

        embed = discord.Embed(
            title=f"Avatar de {member.display_name}",
            color=0x0099ff
        )

        # Get the highest quality avatar
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url

        embed.set_image(url=avatar_url)
        embed.add_field(name="👤 Usuario", value=member.mention, inline=True)
        embed.add_field(name="🆔 ID", value=member.id, inline=True)
        embed.add_field(name="📅 Se unió", value=f"<t:{int(member.created_at.timestamp())}:F>", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='userinfo')
    async def userinfo(self, ctx, member: discord.Member = None):
        """Get detailed user information"""
        if member is None:
            member = ctx.author

        # Calculate account age
        created_at = member.created_at
        now = datetime.now(created_at.tzinfo)
        age_days = (now - created_at).days

        # Get join date for server
        joined_at = member.joined_at
        if joined_at:
            joined_days = (now - joined_at).days
        else:
            joined_days = 0

        embed = discord.Embed(
            title=f"Información de {member.display_name}",
            color=0x0099ff
        )

        # Set thumbnail to user's avatar
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        # Basic info
        embed.add_field(name="👤 Nombre", value=member.name, inline=True)
        embed.add_field(name="🏷️ Nickname", value=member.nick or "Ninguno", inline=True)
        embed.add_field(name="🆔 ID", value=member.id, inline=True)

        # Account info
        embed.add_field(name="📅 Cuenta creada", value=f"<t:{int(created_at.timestamp())}:F>", inline=False)
        embed.add_field(name="📊 Edad de cuenta", value=f"{age_days} días", inline=True)

        if joined_at:
            embed.add_field(name="📅 Se unió al servidor", value=f"<t:{int(joined_at.timestamp())}:F>", inline=False)
            embed.add_field(name="📊 Tiempo en servidor", value=f"{joined_days} días", inline=True)

        # Status and activity
        status_emoji = {
            discord.Status.online: "🟢",
            discord.Status.idle: "🟡",
            discord.Status.dnd: "🔴",
            discord.Status.offline: "⚫"
        }

        status = status_emoji.get(member.status, "⚫")
        embed.add_field(name="📊 Estado", value=f"{status} {member.status.title()}", inline=True)

        # Activity
        if member.activity:
            activity_type = {
                discord.ActivityType.playing: "🎮 Jugando",
                discord.ActivityType.streaming: "🔴 Transmitiendo",
                discord.ActivityType.listening: "🎵 Escuchando",
                discord.ActivityType.watching: "📺 Viendo",
                discord.ActivityType.custom: "✨ Personalizado",
                discord.ActivityType.competing: "🏆 Compitiendo"
            }
            activity_emoji = activity_type.get(member.activity.type, "❓")
            embed.add_field(name="🎯 Actividad", value=f"{activity_emoji} {member.activity.name}", inline=True)
        else:
            embed.add_field(name="🎯 Actividad", value="Ninguna", inline=True)

        # Roles
        if member.roles:
            roles = [role.mention for role in member.roles if role != ctx.guild.default_role]
            if roles:
                roles_text = ", ".join(roles[:5])  # Limit to 5 roles
                if len(roles) > 5:
                    roles_text += f" y {len(roles) - 5} más"
                embed.add_field(name=f"📋 Roles ({len(member.roles)})", value=roles_text, inline=False)
            else:
                embed.add_field(name="📋 Roles", value="Ninguno", inline=False)

        # Permissions
        permissions = []
        if member.guild_permissions.administrator:
            permissions.append("👑 Administrador")
        if member.guild_permissions.manage_guild:
            permissions.append("⚙️ Gestionar Servidor")
        if member.guild_permissions.manage_channels:
            permissions.append("📺 Gestionar Canales")
        if member.guild_permissions.manage_roles:
            permissions.append("📋 Gestionar Roles")
        if member.guild_permissions.kick_members:
            permissions.append("👢 Expulsar Miembros")
        if member.guild_permissions.ban_members:
            permissions.append("🔨 Banear Miembros")
        if member.guild_permissions.manage_messages:
            permissions.append("📝 Gestionar Mensajes")

        if permissions:
            embed.add_field(name="🔑 Permisos clave", value="\n".join(permissions), inline=False)
        else:
            embed.add_field(name="🔑 Permisos clave", value="Ninguno", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='banner')
    async def banner(self, ctx, member: discord.Member = None):
        """Get a user's banner"""
        if member is None:
            member = ctx.author

        # Get user data including banner
        try:
            user_data = await self.bot.fetch_user(member.id)
            if user_data.banner:
                embed = discord.Embed(
                    title=f"Banner de {member.display_name}",
                    color=0x0099ff
                )
                embed.set_image(url=user_data.banner.url)
                embed.add_field(name="👤 Usuario", value=member.mention, inline=True)
                embed.add_field(name="🆔 ID", value=member.id, inline=True)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ {member.mention} no tiene un banner configurado.")
        except Exception as e:
            await ctx.send(f"❌ Error al obtener el banner: {e}")

    @commands.command(name='serverinfo')
    async def serverinfo(self, ctx):
        """Get detailed server information"""
        guild = ctx.guild

        # Calculate server age
        created_at = guild.created_at
        now = datetime.now(created_at.tzinfo)
        age_days = (now - created_at).days

        embed = discord.Embed(
            title=f"Información del servidor: {guild.name}",
            color=0x0099ff
        )

        # Server icon
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        # Basic info
        embed.add_field(name="🏷️ Nombre", value=guild.name, inline=True)
        embed.add_field(name="🆔 ID", value=guild.id, inline=True)
        embed.add_field(name="👑 Propietario", value=guild.owner.mention, inline=True)

        # Server stats
        embed.add_field(name="📅 Creado", value=f"<t:{int(created_at.timestamp())}:F>", inline=False)
        embed.add_field(name="📊 Edad del servidor", value=f"{age_days} días", inline=True)

        # Member counts
        total_members = guild.member_count
        online_members = len([m for m in guild.members if m.status != discord.Status.offline])
        bot_count = len([m for m in guild.members if m.bot])

        embed.add_field(name="👥 Miembros", value=f"**Total:** {total_members}\n**Online:** {online_members}\n**Bots:** {bot_count}", inline=True)

        # Channel counts
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)

        embed.add_field(name="📺 Canales", value=f"**Texto:** {text_channels}\n**Voz:** {voice_channels}\n**Categorías:** {categories}", inline=True)

        # Role count
        embed.add_field(name="📋 Roles", value=len(guild.roles), inline=True)

        # Boost info
        if guild.premium_subscription_count:
            embed.add_field(name="🚀 Boosts", value=f"**Nivel:** {guild.premium_tier}\n**Boosts:** {guild.premium_subscription_count}", inline=True)
        else:
            embed.add_field(name="🚀 Boosts", value="Ninguno", inline=True)

        # Security
        embed.add_field(name="🔒 Seguridad", value=f"**Verificación:** {'Alta' if guild.verification_level.name == 'high' else 'Media' if guild.verification_level.name == 'medium' else 'Baja'}\n**MFA:** {'Requerido' if guild.mfa_level else 'No requerido'}", inline=True)

        # Features
        features = []
        if "COMMUNITY" in guild.features:
            features.append("🏘️ Comunidad")
        if "DISCOVERABLE" in guild.features:
            features.append("🔍 Descubrible")
        if "FEATURABLE" in guild.features:
            features.append("⭐ Destacable")
        if "ANIMATED_ICON" in guild.features:
            features.append("🎭 Icono animado")
        if "BANNER" in guild.features:
            features.append("🖼️ Banner")
        if "VANITY_URL" in guild.features:
            features.append("🔗 URL personalizada")

        if features:
            embed.add_field(name="✨ Características", value="\n".join(features), inline=False)
        else:
            embed.add_field(name="✨ Características", value="Ninguna", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='serverstats')
    async def serverstats(self, ctx):
        """Get detailed server statistics"""
        guild = ctx.guild

        embed = discord.Embed(
            title=f"📊 Estadísticas de {guild.name}",
            color=0x0099ff
        )

        # Member statistics
        total_members = guild.member_count
        humans = len([m for m in guild.members if not m.bot])
        bots = len([m for m in guild.members if m.bot])

        # Status statistics
        online = len([m for m in guild.members if m.status == discord.Status.online])
        idle = len([m for m in guild.members if m.status == discord.Status.idle])
        dnd = len([m for m in guild.members if m.status == discord.Status.dnd])
        offline = len([m for m in guild.members if m.status == discord.Status.offline])

        embed.add_field(
            name="👥 Miembros",
            value=f"**Total:** {total_members}\n"
                  f"**Humanos:** {humans}\n"
                  f"**Bots:** {bots}",
            inline=True
        )

        embed.add_field(
            name="📊 Estados",
            value=f"**🟢 Online:** {online}\n"
                  f"**🟡 Ausente:** {idle}\n"
                  f"**🔴 No molestar:** {dnd}\n"
                  f"**⚫ Desconectado:** {offline}",
            inline=True
        )

        # Channel statistics
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)

        embed.add_field(
            name="📺 Canales",
            value=f"**Texto:** {text_channels}\n"
                  f"**Voz:** {voice_channels}\n"
                  f"**Categorías:** {categories}",
            inline=True
        )

        # Role statistics
        roles = len(guild.roles)
        roles_with_members = len([r for r in guild.roles if len(r.members) > 0])

        embed.add_field(
            name="📋 Roles",
            value=f"**Total:** {roles}\n"
                  f"**Con miembros:** {roles_with_members}",
            inline=True
        )

        # Activity statistics
        if hasattr(guild, 'approximate_member_count'):
            embed.add_field(
                name="📈 Actividad aproximada",
                value=f"**Miembros activos:** {guild.approximate_member_count}",
                inline=True
            )

        # Boost statistics
        if guild.premium_subscription_count:
            embed.add_field(
                name="🚀 Boosts",
                value=f"**Boosts:** {guild.premium_subscription_count}\n"
                      f"**Nivel:** {guild.premium_tier}",
                inline=True
            )

        # Emojis
        embed.add_field(
            name="😀 Emojis",
            value=f"**Total:** {len(guild.emojis)}",
            inline=True
        )

        await ctx.send(embed=embed)

    @commands.command(name='roleinfo')
    async def roleinfo(self, ctx, role: discord.Role):
        """Get information about a role"""
        embed = discord.Embed(
            title=f"Información del rol: {role.name}",
            color=role.color
        )

        # Role info
        embed.add_field(name="🆔 ID", value=role.id, inline=True)
        embed.add_field(name="🎨 Color", value=f"#{role.color.value:06x}" if role.color.value != 0 else "Default", inline=True)
        embed.add_field(name="📍 Posición", value=role.position, inline=True)

        # Permissions
        permissions = []
        if role.permissions.administrator:
            permissions.append("👑 Administrador")
        if role.permissions.manage_guild:
            permissions.append("⚙️ Gestionar Servidor")
        if role.permissions.manage_channels:
            permissions.append("📺 Gestionar Canales")
        if role.permissions.manage_roles:
            permissions.append("📋 Gestionar Roles")
        if role.permissions.kick_members:
            permissions.append("👢 Expulsar Miembros")
        if role.permissions.ban_members:
            permissions.append("🔨 Banear Miembros")
        if role.permissions.manage_messages:
            permissions.append("📝 Gestionar Mensajes")
        if role.permissions.mention_everyone:
            permissions.append("📢 Mencionar a todos")

        if permissions:
            embed.add_field(name="🔑 Permisos", value="\n".join(permissions), inline=False)
        else:
            embed.add_field(name="🔑 Permisos", value="Ninguno", inline=False)

        # Member count
        embed.add_field(name="👥 Miembros", value=len(role.members), inline=True)

        # Role creation date
        embed.add_field(name="📅 Creado", value=f"<t:{int(role.created_at.timestamp())}:F>", inline=True)

        # Hoisted status
        embed.add_field(name="📌 Mostrado separado", value="Sí" if role.hoist else "No", inline=True)

        # Mentionable status
        embed.add_field(name="🗣️ Mencionable", value="Sí" if role.mentionable else "No", inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='channelinfo')
    async def channelinfo(self, ctx, channel: discord.TextChannel = None):
        """Get information about a channel"""
        if channel is None:
            channel = ctx.channel

        embed = discord.Embed(
            title=f"Información del canal: #{channel.name}",
            color=0x0099ff
        )

        # Channel info
        embed.add_field(name="🆔 ID", value=channel.id, inline=True)
        embed.add_field(name="📍 Posición", value=channel.position, inline=True)
        embed.add_field(name="📅 Creado", value=f"<t:{int(channel.created_at.timestamp())}:F>", inline=True)

        # Channel type
        channel_type = {
            discord.ChannelType.text: "Texto",
            discord.ChannelType.voice: "Voz",
            discord.ChannelType.category: "Categoría",
            discord.ChannelType.news: "Noticias",
            discord.ChannelType.store: "Tienda",
            discord.ChannelType.stage_voice: "Escenario"
        }
        embed.add_field(name="📺 Tipo", value=channel_type.get(channel.type, "Desconocido"), inline=True)

        # Category
        if channel.category:
            embed.add_field(name="📁 Categoría", value=channel.category.name, inline=True)
        else:
            embed.add_field(name="📁 Categoría", value="Ninguna", inline=True)

        # NSFW status
        embed.add_field(name="🔞 NSFW", value="Sí" if channel.nsfw else "No", inline=True)

        # Slowmode
        embed.add_field(name="🐌 Modo lento", value=f"{channel.slowmode_delay}s" if channel.slowmode_delay > 0 else "Desactivado", inline=True)

        # Member count (for voice channels)
        if isinstance(channel, discord.VoiceChannel):
            embed.add_field(name="👥 Límite de usuarios", value=channel.user_limit if channel.user_limit > 0 else "Sin límite", inline=True)
            embed.add_field(name="🔊 Bitrate", value=f"{channel.bitrate//1000}kbps", inline=True)

        # Permissions
        permissions = []
        if channel.overwrites:
            for target, overwrite in channel.overwrites.items():
                if isinstance(target, discord.Role):
                    target_name = f"@{target.name}"
                else:
                    target_name = target.mention

                perms = []
                if overwrite.read_messages is False:
                    perms.append("❌ Ver mensajes")
                if overwrite.send_messages is False:
                    perms.append("❌ Enviar mensajes")
                if overwrite.manage_messages:
                    perms.append("✅ Gestionar mensajes")

                if perms:
                    permissions.append(f"{target_name}: {', '.join(perms)}")

        if permissions:
            embed.add_field(name="🔒 Permisos especiales", value="\n".join(permissions[:5]), inline=False)
            if len(permissions) > 5:
                embed.add_field(name="ℹ️", value=f"Y {len(permissions) - 5} más...", inline=False)
        else:
            embed.add_field(name="🔒 Permisos especiales", value="Ninguno", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UserCommandsCog(bot))
