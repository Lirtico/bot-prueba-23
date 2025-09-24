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
                await ctx.send(embed=embed)
                return

        # Update last execution time
        self.bot.last_help_execution[user_id] = datetime.now().timestamp()

        if category:
            # Show specific category
            category_lower = category.lower()
            found_category = None

            for cat_key, cat_data in COMMAND_CATEGORIES.items():
                if cat_key == category_lower or cat_data["name"].lower().replace("🛠️ ", "").replace("👤 ", "").replace("🎲 ", "").replace("🔧 ", "").replace("🎯 ", "").replace("📊 ", "").replace("🎭 ", "").replace("⚡ ", "").replace("🏘️ ", "").lower() == category_lower:
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

async def setup(bot):
    await bot.add_cog(UtilityCommandsCog(bot))
