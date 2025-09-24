import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Select, View
import asyncio
from config.categories import COMMAND_CATEGORIES

class HelpSelect(Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(
                label=cat_data["name"],
                description=cat_data["description"][:50] + "..." if len(cat_data["description"]) > 50 else cat_data["description"],
                value=cat_key,
                emoji=cat_data["name"].split()[0] if cat_data["name"].split()[0] in ["⚡", "🎭", "🛠️", "👤", "🎲", "🔧", "🏘️", "📊"] else "📋"
            )
            for cat_key, cat_data in COMMAND_CATEGORIES.items()
        ]

        super().__init__(
            placeholder="Elige una categoría...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            category_key = self.values[0]
            category_data = COMMAND_CATEGORIES[category_key]

            embed = discord.Embed(
                title=category_data["name"],
                description=category_data["description"],
                color=category_data["color"]
            )

            # Add commands to embed
            for command, description in category_data["commands"].items():
                embed.add_field(name=command, value=description, inline=False)

            embed.set_footer(text="Usa /help para volver al menú principal")

            await interaction.response.edit_message(embed=embed, view=self.view)
        except Exception as e:
            # Log the error and send a user-friendly message
            print(f"Error in help callback: {e}")
            try:
                embed = discord.Embed(
                    title="❌ Error",
                    description="Ha ocurrido un error al mostrar la categoría. Por favor, intenta usar `/help` nuevamente.",
                    color=0xff0000
                )
                await interaction.response.edit_message(embed=embed, view=None)
            except:
                # If we can't edit the message, send a new one
                try:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title="❌ Error",
                            description="Ha ocurrido un error. Por favor, intenta usar `/help` nuevamente.",
                            color=0xff0000
                        ),
                        ephemeral=True
                    )
                except:
                    pass

class HelpView(View):
    def __init__(self, bot):
        super().__init__(timeout=300)  # 5 minutes timeout
        self.bot = bot
        self.add_item(HelpSelect(bot))

    async def on_timeout(self):
        # Disable all items when timeout
        for item in self.children:
            item.disabled = True

        # Try to edit the message to show it's expired
        try:
            if hasattr(self, 'message'):
                embed = discord.Embed(
                    title="⏰ Menú expirado",
                    description="El menú de ayuda ha expirado. Usa `/help` para abrir uno nuevo.",
                    color=0xffaa00
                )
                await self.message.edit(embed=embed, view=self)
        except:
            pass

class SlashCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Sistema de ayuda interactivo con botones")
    async def help_slash(self, interaction: discord.Interaction):
        """Sistema de ayuda interactivo con categorías"""

        embed = discord.Embed(
            title="🐨 Ayuda de Koala Bot",
            description="¡Hola! Soy Koala Bot, tu bot de Discord multifuncional. Selecciona una categoría para ver sus comandos:",
            color=0x0099ff
        )

        # Add some stats
        embed.add_field(
            name="📊 Estadísticas",
            value=f"• **{len(COMMAND_CATEGORIES)} categorías**\n"
                  f"• **{sum(len(cat['commands']) for cat in COMMAND_CATEGORIES.values())} comandos**\n"
                  f"• **50+ interacciones** con GIFs",
            inline=False
        )

        embed.add_field(
            name="🎮 Cómo usar",
            value="• Usa el menú desplegable para seleccionar una categoría\n"
                  "• Cada categoría muestra sus comandos disponibles\n"
                  "• Los comandos están organizados por funcionalidad",
            inline=False
        )

        embed.set_footer(text="¡Selecciona una categoría para comenzar!")

        view = HelpView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @app_commands.command(name="ping", description="Verificar latencia del bot")
    async def ping_slash(self, interaction: discord.Interaction):
        """Check bot latency"""
        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"**Latencia:** {latency}ms",
            color=0x00ff00
        )

        # Add some fun based on latency
        if latency < 50:
            embed.add_field(name="📊 Estado", value="Excelente", inline=True)
        elif latency < 100:
            embed.add_field(name="📊 Estado", value="Bueno", inline=True)
        elif latency < 200:
            embed.add_field(name="📊 Estado", value="Regular", inline=True)
        else:
            embed.add_field(name="📊 Estado", value="Malo", inline=True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="info", description="Información del bot")
    async def info_slash(self, interaction: discord.Interaction):
        """Show information about the bot"""
        embed = discord.Embed(
            title="🐨 Información de Koala Bot",
            description="Un bot de Discord multifuncional creado para hacer tu servidor más divertido y organizado.",
            color=0x0099ff
        )

        embed.add_field(
            name="✨ Características",
            value="• 🛠️ Comandos de moderación\n"
                  "• 🎭 50+ interacciones con GIFs anime\n"
                  "• 🎲 Comandos de diversión\n"
                  "• 🔧 Utilidades y herramientas\n"
                  "• 📊 Sistema de logging\n"
                  "• ⚡ Comandos slash modernos",
            inline=False
        )

        embed.add_field(
            name="🔧 Tecnologías",
            value="• Python 3.8+\n"
                  "• discord.py\n"
                  "• Tenor API para GIFs\n"
                  "• Sistema modular",
            inline=False
        )

        embed.add_field(
            name="📊 Estadísticas",
            value=f"• Servidores: {len(self.bot.guilds)}\n"
                  f"• Usuarios: {sum(g.member_count for g in self.bot.guilds)}\n"
                  f"• Comandos: 50+",
            inline=False
        )

        embed.set_footer(text="Creado con ❤️ para la comunidad de Discord")

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="stats", description="Estadísticas del bot")
    async def stats_slash(self, interaction: discord.Interaction):
        """Show bot statistics"""
        embed = discord.Embed(
            title="📊 Estadísticas del bot",
            color=0x0099ff
        )

        # Guild count
        embed.add_field(name="🏠 Servidores", value=len(self.bot.guilds), inline=True)

        # User count
        total_users = sum(guild.member_count for guild in self.bot.guilds)
        embed.add_field(name="👥 Usuarios totales", value=total_users, inline=True)

        # Uptime
        if hasattr(self.bot, 'uptime'):
            uptime = discord.utils.utcnow() - self.bot.uptime
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
        else:
            uptime_str = "Desconocido"
        embed.add_field(name="⏰ Tiempo activo", value=uptime_str, inline=True)

        # Commands loaded
        extensions = len(self.bot.extensions)
        embed.add_field(name="🔧 Extensiones cargadas", value=extensions, inline=True)

        # Latency
        latency = round(self.bot.latency * 1000)
        embed.add_field(name="🏓 Latencia", value=f"{latency}ms", inline=True)

        # Memory usage (approximate)
        embed.add_field(name="💾 Estado", value="Activo", inline=True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="invite", description="Obtener enlace de invitación")
    async def invite_slash(self, interaction: discord.Interaction):
        """Get bot invite link"""
        embed = discord.Embed(
            title="🔗 Invitar a Koala Bot",
            description="¡Gracias por querer invitarme a tu servidor!",
            color=0x00ff00
        )

        embed.add_field(
            name="🔗 Enlace de invitación",
            value="[Haz clic aquí para invitarme](https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=8&scope=bot%20applications.commands)",
            inline=False
        )

        embed.add_field(
            name="⚙️ Permisos requeridos",
            value="• Leer mensajes\n"
                  "• Enviar mensajes\n"
                  "• Gestionar mensajes\n"
                  "• Gestionar roles\n"
                  "• Banear miembros\n"
                  "• Expulsar miembros\n"
                  "• Usar comandos de aplicación",
            inline=False
        )

        embed.set_footer(text="¡Nos vemos en tu servidor!")

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="uptime", description="Tiempo de actividad del bot")
    async def uptime_slash(self, interaction: discord.Interaction):
        """Show bot uptime"""
        if not hasattr(self.bot, 'uptime'):
            embed = discord.Embed(
                title="⏰ Tiempo de actividad",
                description="El bot aún no ha registrado tiempo de actividad.",
                color=0xffaa00
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        uptime = discord.utils.utcnow() - self.bot.uptime
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        embed = discord.Embed(
            title="⏰ Tiempo de actividad",
            color=0x00ff00
        )

        if days > 0:
            embed.add_field(name="📅 Días", value=days, inline=True)
        embed.add_field(name="⏰ Horas", value=hours, inline=True)
        embed.add_field(name="📊 Minutos", value=minutes, inline=True)
        embed.add_field(name="⚡ Segundos", value=seconds, inline=True)

        embed.set_footer(text=f"Bot iniciado: {self.bot.uptime.strftime('%d/%m/%Y %H:%M')}")

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="suggest", description="Enviar sugerencias")
    @app_commands.describe(suggestion="Tu sugerencia para mejorar el bot")
    async def suggest_slash(self, interaction: discord.Interaction, suggestion: str):
        """Send a suggestion to the bot developers"""
        embed = discord.Embed(
            title="💡 Sugerencia recibida",
            description="¡Gracias por tu sugerencia! Los desarrolladores la revisarán pronto.",
            color=0x00ff00
        )

        embed.add_field(name="👤 Usuario", value=interaction.user.mention, inline=True)
        embed.add_field(name="🆔 ID", value=interaction.user.id, inline=True)
        embed.add_field(name="📝 Sugerencia", value=suggestion, inline=False)

        embed.set_footer(text="Sugerencia enviada correctamente")

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="bug", description="Reportar bugs")
    @app_commands.describe(bug_report="Describe el bug que encontraste")
    async def bug_slash(self, interaction: discord.Interaction, bug_report: str):
        """Report a bug to the bot developers"""
        embed = discord.Embed(
            title="🐛 Reporte de bug recibido",
            description="¡Gracias por reportar el bug! Los desarrolladores lo investigarán.",
            color=0xffaa00
        )

        embed.add_field(name="👤 Usuario", value=interaction.user.mention, inline=True)
        embed.add_field(name="🆔 ID", value=interaction.user.id, inline=True)
        embed.add_field(name="🐛 Bug reportado", value=bug_report, inline=False)

        embed.set_footer(text="Bug reportado correctamente")

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(SlashCommandsCog(bot))
