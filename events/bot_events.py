import discord
from discord.ext import commands
from datetime import datetime

class BotEventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when the bot is ready and connected"""
        print(f'{self.bot.user.name} has connected to Discord!')
        print(f'Bot ID: {self.bot.user.id}')
        print(f'Connected to {len(self.bot.guilds)} servers')
        print('------')

        # Set uptime
        self.bot.uptime = datetime.now()

        # Sync slash commands with Discord
        try:
            synced = await self.bot.tree.sync()
            print(f'Synced {len(synced)} command(s)')
        except Exception as e:
            print(f'Failed to sync commands: {e}')

    @commands.Cog.listener()
    async def on_command(self, ctx):
        """Called when a command is invoked"""
        print(f"Command invoked: {ctx.command.name} by {ctx.author.name}#{ctx.author.discriminator} in {ctx.guild.name if ctx.guild else 'DM'}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Global error handler for commands"""
        if isinstance(error, commands.CommandNotFound):
            # Don't show error for unknown commands
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="❌ Argumento faltante",
                description=f"Falta el argumento requerido: `{error.param.name}`",
                color=0xff0000
            )
            embed.add_field(name="Uso correcto", value=f"`{ctx.prefix}{ctx.command.name} {ctx.command.signature}`", inline=False)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="❌ Argumento inválido",
                description="El argumento proporcionado no es válido.",
                color=0xff0000
            )
            embed.add_field(name="Uso correcto", value=f"`{ctx.prefix}{ctx.command.name} {ctx.command.signature}`", inline=False)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="❌ Permisos insuficientes",
                description="No tienes los permisos necesarios para usar este comando.",
                color=0xff0000
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                title="❌ Permisos del bot",
                description="No tengo los permisos necesarios para ejecutar este comando.",
                color=0xff0000
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="⏰ Comando en cooldown",
                description=f"Este comando está en cooldown. Intenta de nuevo en {error.retry_after:.1f} segundos.",
                color=0xffaa00
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title="❌ Solo para el dueño",
                description="Este comando solo puede ser usado por el dueño del bot.",
                color=0xff0000
            )
            await ctx.send(embed=embed)

        else:
            # Log unexpected errors
            print(f"Unexpected error in command {ctx.command.name}: {error}")

            embed = discord.Embed(
                title="❌ Error inesperado",
                description="Ha ocurrido un error inesperado. Por favor, contacta a un administrador.",
                color=0xff0000
            )
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Called when the bot joins a new guild"""
        print(f"Joined new guild: {guild.name} (ID: {guild.id})")
        print(f"Guild has {guild.member_count} members")

        # Send welcome message to system channel
        if guild.system_channel:
            embed = discord.Embed(
                title="🐨 ¡Hola! Soy Koala Bot",
                description="¡Gracias por invitarme a tu servidor! Soy un bot multifuncional con muchos comandos divertidos y útiles.",
                color=0x0099ff
            )

            embed.add_field(
                name="🚀 Para empezar",
                value="• Usa `!help` para ver todos mis comandos\n"
                      "• Usa `!setup` para configurar el sistema de moderación\n"
                      "• Usa `!invite` para obtener mi enlace de invitación",
                inline=False
            )

            embed.add_field(
                name="✨ Características principales",
                value="• 🛠️ Comandos de moderación\n"
                      "• 🎭 Interacciones con GIFs anime\n"
                      "• 🎲 Comandos de diversión\n"
                      "• 🔧 Utilidades y herramientas\n"
                      "• 📊 Sistema de logging",
                inline=False
            )

            embed.set_footer(text="¡Espero poder ayudar a hacer tu servidor más divertido!")

            try:
                await guild.system_channel.send(embed=embed)
            except discord.Forbidden:
                print(f"Cannot send welcome message to {guild.name}: Forbidden")
            except Exception as e:
                print(f"Error sending welcome message to {guild.name}: {e}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """Called when the bot leaves a guild"""
        print(f"Left guild: {guild.name} (ID: {guild.id})")

        # Clean up guild-specific data
        guild_id = guild.id

        # Remove log channels
        if guild_id in self.bot.log_channels:
            del self.bot.log_channels[guild_id]

        # Remove jail data
        if guild_id in self.bot.jail_data:
            del self.bot.jail_data[guild_id]

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        """Called when a member is banned"""
        guild_id = guild.id

        if guild_id in self.bot.log_channels:
            log_channel = self.bot.get_channel(self.bot.log_channels[guild_id])

            embed = discord.Embed(
                title="🔨 Usuario baneado",
                description=f"{user.mention} fue baneado del servidor",
                color=0xff0000
            )

            embed.add_field(name="👤 Usuario", value=f"{user.name}#{user.discriminator}", inline=True)
            embed.add_field(name="🆔 ID", value=user.id, inline=True)

            embed.timestamp = datetime.now()

            try:
                await log_channel.send(embed=embed)
            except discord.Forbidden:
                pass

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        """Called when a member is unbanned"""
        guild_id = guild.id

        if guild_id in self.bot.log_channels:
            log_channel = self.bot.get_channel(self.bot.log_channels[guild_id])

            embed = discord.Embed(
                title="✅ Usuario desbaneado",
                description=f"{user.mention} fue desbaneado del servidor",
                color=0x00ff00
            )

            embed.add_field(name="👤 Usuario", value=f"{user.name}#{user.discriminator}", inline=True)
            embed.add_field(name="🆔 ID", value=user.id, inline=True)

            embed.timestamp = datetime.now()

            try:
                await log_channel.send(embed=embed)
            except discord.Forbidden:
                pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Called when a member's voice state changes"""
        guild_id = member.guild.id

        if guild_id not in self.bot.log_channels:
            return

        log_channel = self.bot.get_channel(self.bot.log_channels[guild_id])

        # User joined a voice channel
        if before.channel is None and after.channel is not None:
            embed = discord.Embed(
                title="🎤 Usuario se unió a voz",
                description=f"{member.mention} se unió a {after.channel.mention}",
                color=0x00ff00
            )

            embed.add_field(name="👤 Usuario", value=f"{member.name}#{member.discriminator}", inline=True)
            embed.add_field(name="📺 Canal", value=after.channel.name, inline=True)

            embed.timestamp = datetime.now()

            try:
                await log_channel.send(embed=embed)
            except discord.Forbidden:
                pass

        # User left a voice channel
        elif before.channel is not None and after.channel is None:
            embed = discord.Embed(
                title="🎤 Usuario salió de voz",
                description=f"{member.mention} salió de {before.channel.mention}",
                color=0xff0000
            )

            embed.add_field(name="👤 Usuario", value=f"{member.name}#{member.discriminator}", inline=True)
            embed.add_field(name="📺 Canal", value=before.channel.name, inline=True)

            embed.timestamp = datetime.now()

            try:
                await log_channel.send(embed=embed)
            except discord.Forbidden:
                pass

        # User moved between voice channels
        elif before.channel != after.channel and before.channel is not None and after.channel is not None:
            embed = discord.Embed(
                title="🎤 Usuario cambió de canal",
                description=f"{member.mention} se movió de {before.channel.mention} a {after.channel.mention}",
                color=0x3498db
            )

            embed.add_field(name="👤 Usuario", value=f"{member.name}#{member.discriminator}", inline=True)
            embed.add_field(name="📺 Desde", value=before.channel.name, inline=True)
            embed.add_field(name="📺 Hacia", value=after.channel.name, inline=True)

            embed.timestamp = datetime.now()

            try:
                await log_channel.send(embed=embed)
            except discord.Forbidden:
                pass

async def setup(bot):
    await bot.add_cog(BotEventsCog(bot))
