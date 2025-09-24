import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio

class UtilityCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='say')
    async def say(self, ctx, *, message):
        """Make the bot say something"""
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(name='ping')
    async def ping(self, ctx):
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

        await ctx.send(embed=embed)

    @commands.command(name='help')
    async def help(self, ctx, category: str = None):
        """Show help with organized categories"""
        from config.categories import COMMAND_CATEGORIES

        # Check if user has used help recently
        user_id = ctx.author.id
        if hasattr(self.bot, 'last_help_execution') and user_id in self.bot.last_help_execution:
            last_execution = self.bot.last_help_execution[user_id]
            if datetime.now().timestamp() - last_execution < 300:  # 5 minutes
                remaining = int(300 - (datetime.now().timestamp() - last_execution))
                embed = discord.Embed(
                    title="⏰ Espera un momento",
                    description=f"Ya usaste el comando help recientemente. Espera {remaining} segundos.",
                    color=0xffaa00
                )
                await ctx.send(embed=embed, ephemeral=True)
                return

        # Update last execution time
        self.bot.last_help_execution[user_id] = datetime.now().timestamp()

        if category:
            # Show specific category
            category_lower = category.lower()
            found_category = None

            for cat_key, cat_data in COMMAND_CATEGORIES.items():
                if cat_key == category_lower or cat_data["name"].lower().replace("🛠️ ", "").replace("👤 ", "").replace("🎲 ", "").replace("🔧 ", "").replace("🎯 ", "").replace("📊 ", "").replace("🎭 ", "").lower() == category_lower:
                    found_category = cat_data
                    break

            if found_category:
                embed = discord.Embed(
                    title=found_category["name"],
                    description=found_category["description"],
                    color=found_category["color"]
                )

                for command, description in found_category["commands"].items():
                    embed.add_field(name=command, value=description, inline=False)

                embed.set_footer(text="Usa !help para ver todas las categorías")
            else:
                embed = discord.Embed(
                    title="❌ Categoría no encontrada",
                    description="Categorías disponibles: " + ", ".join([cat["name"] for cat in COMMAND_CATEGORIES.values()]),
                    color=0xff0000
                )
        else:
            # Show all categories
            embed = discord.Embed(
                title="🐨 Ayuda de Koala Bot",
                description="¡Hola! Soy Koala Bot, tu bot de Discord multifuncional. Aquí tienes todos mis comandos organizados por categorías:",
                color=0x0099ff
            )

            for cat_key, cat_data in COMMAND_CATEGORIES.items():
                commands_list = "\n".join([f"• {cmd}" for cmd in cat_data["commands"].keys()])
                embed.add_field(
                    name=cat_data["name"],
                    value=f"{cat_data['description']}\n\n{commands_list}",
                    inline=False
                )

            embed.set_footer(text="Usa !help <categoría> para ver comandos específicos • Ejemplo: !help moderación")

        await ctx.send(embed=embed)

    @commands.command(name='commands')
    async def commands(self, ctx):
        """Show a simple list of all commands"""
        from config.categories import COMMAND_CATEGORIES

        embed = discord.Embed(
            title="📋 Lista de comandos",
            description="Aquí tienes todos los comandos disponibles:",
            color=0x0099ff
        )

        for cat_data in COMMAND_CATEGORIES.values():
            commands_list = ", ".join([cmd.split()[0].strip("`") for cmd in cat_data["commands"].keys()])
            embed.add_field(
                name=cat_data["name"],
                value=commands_list,
                inline=False
            )

        embed.set_footer(text="Usa !help para información detallada de cada comando")

        await ctx.send(embed=embed)

    @commands.command(name='invite')
    async def invite(self, ctx):
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

        await ctx.send(embed=embed)

    @commands.command(name='uptime')
    async def uptime(self, ctx):
        """Show bot uptime"""
        if not hasattr(self.bot, 'uptime'):
            self.bot.uptime = datetime.now()

        uptime = datetime.now() - self.bot.uptime
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

        await ctx.send(embed=embed)

    @commands.command(name='stats')
    async def stats(self, ctx):
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
            uptime = datetime.now() - self.bot.uptime
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

        await ctx.send(embed=embed)

    @commands.command(name='suggest')
    async def suggest(self, ctx, *, suggestion):
        """Send a suggestion to the bot developers"""
        embed = discord.Embed(
            title="💡 Sugerencia recibida",
            description="¡Gracias por tu sugerencia! Los desarrolladores la revisarán pronto.",
            color=0x00ff00
        )

        embed.add_field(name="👤 Usuario", value=ctx.author.mention, inline=True)
        embed.add_field(name="🆔 ID", value=ctx.author.id, inline=True)
        embed.add_field(name="📝 Sugerencia", value=suggestion, inline=False)

        embed.set_footer(text="Sugerencia enviada correctamente")

        await ctx.send(embed=embed)

        # Here you could add code to send the suggestion to a specific channel or user
        # For now, it just confirms receipt

    @commands.command(name='bug')
    async def bug(self, ctx, *, bug_report):
        """Report a bug to the bot developers"""
        embed = discord.Embed(
            title="🐛 Reporte de bug recibido",
            description="¡Gracias por reportar el bug! Los desarrolladores lo investigarán.",
            color=0xffaa00
        )

        embed.add_field(name="👤 Usuario", value=ctx.author.mention, inline=True)
        embed.add_field(name="🆔 ID", value=ctx.author.id, inline=True)
        embed.add_field(name="🐛 Bug reportado", value=bug_report, inline=False)

        embed.set_footer(text="Bug reportado correctamente")

        await ctx.send(embed=embed)

        # Here you could add code to send the bug report to a specific channel or user
        # For now, it just confirms receipt

    @commands.command(name='info')
    async def info(self, ctx):
        """Show information about the bot"""
        embed = discord.Embed(
            title="🐨 Información de Koala Bot",
            description="Un bot de Discord multifuncional creado para hacer tu servidor más divertido y organizado.",
            color=0x0099ff
        )

        embed.add_field(
            name="✨ Características",
            value="• Comandos de moderación\n"
                  "• Interacciones con GIFs anime\n"
                  "• Comandos de diversión\n"
                  "• Utilidades y herramientas\n"
                  "• Sistema de logging\n"
                  "• Sistema de cárcel\n"
                  "• Y mucho más!",
            inline=False
        )

        embed.add_field(
            name="🔧 Tecnologías",
            value="• Python 3.8+\n"
                  "• discord.py\n"
                  "• SQLite/PostgreSQL\n"
                  "• Tenor API para GIFs",
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

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UtilityCommandsCog(bot))
