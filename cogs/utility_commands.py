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

        embed.set_footer(text="Usa /help para información detallada de cada comando")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UtilityCommandsCog(bot))
