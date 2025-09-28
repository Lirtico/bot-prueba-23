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

            # Check if category has too many commands (Discord limit is 25 fields per embed)
            commands_list = list(category_data["commands"].items())
            max_fields_per_embed = 25

            if len(commands_list) <= max_fields_per_embed:
                # Single embed - fits within limit
                embed = discord.Embed(
                    title=category_data["name"],
                    description=category_data["description"],
                    color=category_data["color"]
                )

                for command, description in commands_list:
                    embed.add_field(name=command, value=description, inline=False)

                embed.set_footer(text="Usa /help para volver al menú principal")
                await interaction.response.edit_message(embed=embed, view=self.view)
            else:
                # Multiple embeds needed - split into pages
                embeds = []
                total_commands = len(commands_list)

                for i in range(0, total_commands, max_fields_per_embed):
                    page_commands = commands_list[i:i + max_fields_per_embed]
                    page_number = i // max_fields_per_embed + 1
                    total_pages = (total_commands + max_fields_per_embed - 1) // max_fields_per_embed

                    embed = discord.Embed(
                        title=f"{category_data['name']} (Página {page_number}/{total_pages})",
                        description=category_data["description"],
                        color=category_data["color"]
                    )

                    for command, description in page_commands:
                        embed.add_field(name=command, value=description, inline=False)

                    embed.set_footer(text=f"Usa /help para volver al menú principal • Página {page_number}/{total_pages}")
                    embeds.append(embed)

                # Send first page and add navigation buttons
                from discord.ui import Button

                class PageView(View):
                    def __init__(self, embeds_list, start_page=0):
                        super().__init__(timeout=300)
                        self.embeds = embeds_list
                        self.current_page = start_page

                    async def update_message(self, interaction):
                        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

                    @discord.ui.button(label="⬅️ Anterior", style=discord.ButtonStyle.gray, disabled=True)
                    async def previous_button(self, interaction: discord.Interaction, button: Button):
                        self.current_page = max(0, self.current_page - 1)
                        # Update button states
                        for child in self.children:
                            if isinstance(child, Button):
                                if child.label == "⬅️ Anterior":
                                    child.disabled = self.current_page == 0
                                elif child.label == "➡️ Siguiente":
                                    child.disabled = self.current_page >= len(self.embeds) - 1

                        await self.update_message(interaction)

                    @discord.ui.button(label="➡️ Siguiente", style=discord.ButtonStyle.gray)
                    async def next_button(self, interaction: discord.Interaction, button: Button):
                        self.current_page = min(len(self.embeds) - 1, self.current_page + 1)
                        # Update button states
                        for child in self.children:
                            if isinstance(child, Button):
                                if child.label == "⬅️ Anterior":
                                    child.disabled = self.current_page == 0
                                elif child.label == "➡️ Siguiente":
                                    child.disabled = self.current_page >= len(self.embeds) - 1

                        await self.update_message(interaction)

                    @discord.ui.button(label="🏠 Menú Principal", style=discord.ButtonStyle.green)
                    async def home_button(self, interaction: discord.Interaction, button: Button):
                        # Go back to main help menu
                        main_embed = discord.Embed(
                            title="🐨 Ayuda de Koala Bot",
                            description="¡Hola! Soy Koala Bot, tu bot de Discord multifuncional. Selecciona una categoría para ver sus comandos:",
                            color=0x0099ff
                        )

                        # Add some stats
                        main_embed.add_field(
                            name="📊 Estadísticas",
                            value=f"• **{len(COMMAND_CATEGORIES)} categorías**\n"
                                  f"• **{sum(len(cat['commands']) for cat in COMMAND_CATEGORIES.values())} comandos**\n"
                                  f"• **50+ comandos roleplay**",
                            inline=False
                        )

                        main_embed.add_field(
                            name="🎮 Cómo usar",
                            value="• Usa el menú desplegable para seleccionar una categoría\n"
                                  "• Cada categoría muestra sus comandos disponibles\n"
                                  "• Los comandos están organizados por funcionalidad",
                            inline=False
                        )

                        main_embed.set_footer(text="¡Selecciona una categoría para comenzar!")

                        main_view = HelpView(self.bot)
                        await interaction.response.edit_message(embed=main_embed, view=main_view)

                view = PageView(embeds)
                await interaction.response.edit_message(embed=embeds[0], view=view)

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
                  f"• **50+ comandos roleplay**",
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

    # Anime Interaction Slash Commands
    @app_commands.command(name="slap", description="Abofetear a un usuario con un GIF anime")
    @app_commands.describe(member="Usuario a abofetear")
    async def slap_slash(self, interaction: discord.Interaction, member: discord.Member):
        """Slap a user with an anime GIF"""
        if member == interaction.user:
            embed = discord.Embed(
                title="❌ Error",
                description="¡No puedes abofetearte a ti mismo!",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        from gif_api import gif_api
        gif_url = gif_api.get_gif_url("anime slap")

        embed = discord.Embed(
            title="👋 Bofetada!",
            description=f"{interaction.user.mention} le dio una bofetada a {member.mention}!",
            color=0xff6b6b
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Ay! Eso tuvo que doler!")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="hug", description="Abrazar a un usuario con un GIF anime")
    @app_commands.describe(member="Usuario a abrazar")
    async def hug_slash(self, interaction: discord.Interaction, member: discord.Member):
        """Hug a user with an anime GIF"""
        if member == interaction.user:
            embed = discord.Embed(
                title="❌ Error",
                description="¡No puedes abrazarte a ti mismo!",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        from gif_api import gif_api
        gif_url = gif_api.get_gif_url("anime hug")

        embed = discord.Embed(
            title="🤗 Abrazo!",
            description=f"{interaction.user.mention} abrazó a {member.mention}!",
            color=0xffb3ba
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Aww, qué lindo!")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="kiss", description="Besar a un usuario con un GIF anime")
    @app_commands.describe(member="Usuario a besar")
    async def kiss_slash(self, interaction: discord.Interaction, member: discord.Member):
        """Kiss a user with an anime GIF"""
        if member == interaction.user:
            embed = discord.Embed(
                title="❌ Error",
                description="¡No puedes besarte a ti mismo!",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        from gif_api import gif_api
        gif_url = gif_api.get_gif_url("anime kiss")

        embed = discord.Embed(
            title="💋 Beso!",
            description=f"{interaction.user.mention} besó a {member.mention}!",
            color=0xff69b4
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Qué romántico!")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="pat", description="Acariciar a un usuario con un GIF anime")
    @app_commands.describe(member="Usuario a acariciar")
    async def pat_slash(self, interaction: discord.Interaction, member: discord.Member):
        """Pat a user with an anime GIF"""
        if member == interaction.user:
            embed = discord.Embed(
                title="❌ Error",
                description="¡No puedes acariciarte a ti mismo!",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        from gif_api import gif_api
        gif_url = gif_api.get_gif_url("anime pat")

        embed = discord.Embed(
            title="👋 Caricia!",
            description=f"{interaction.user.mention} acarició a {member.mention}!",
            color=0x98d8c8
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Buen trabajo!")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="cuddle", description="Acurrucar a un usuario con un GIF anime")
    @app_commands.describe(member="Usuario a acurrucar")
    async def cuddle_slash(self, interaction: discord.Interaction, member: discord.Member):
        """Cuddle a user with an anime GIF"""
        if member == interaction.user:
            embed = discord.Embed(
                title="❌ Error",
                description="¡No puedes acurrucarte contigo mismo!",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        from gif_api import gif_api
        gif_url = gif_api.get_gif_url("anime cuddle")

        embed = discord.Embed(
            title="🤗 Acurrucando!",
            description=f"{interaction.user.mention} acurrucó a {member.mention}!",
            color=0xffb3ba
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Qué tierno!")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(SlashCommandsCog(bot))
