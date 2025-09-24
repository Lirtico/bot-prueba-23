import discord
from discord.ext import commands
from gif_api import gif_api
from config.settings import nsfw_settings

class InteractionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='slap')
    async def slap(self, ctx, member: discord.Member):
        """Slap a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes abofetearte a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime slap")
            print(f"DEBUG: Slap GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="👋 Bofetada!",
                description=f"{ctx.author.mention} le dio una bofetada a {member.mention}!",
                color=0xff6b6b
            )
            embed.set_footer(text="¡Ay! Eso tuvo que doler!")

            embed.set_image(url=gif_url)
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in slap command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"👋 **Bofetada!** {ctx.author.mention} le dio una bofetada a {member.mention}!\n¡Ay! Eso tuvo que doler!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in slap: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='hug')
    async def hug(self, ctx, member: discord.Member):
        """Hug a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes abrazarte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime hug")
        print(f"DEBUG: Hug GIF URL: {gif_url}")  # Debug line

        embed = discord.Embed(
            title="🤗 Abrazo!",
            description=f"{ctx.author.mention} abrazó a {member.mention}!",
            color=0xffb3ba
        )
        embed.set_footer(text="¡Aww, qué lindo!")

        embed.set_image(url=gif_url)

        try:
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error sending hug embed: {e}")
            # Fallback: send just the text and URL
            await ctx.send(f"🤗 **Abrazo!** {ctx.author.mention} abrazó a {member.mention}!\n¡Aww, qué lindo!\n{gif_url}")

    @commands.command(name='kiss')
    async def kiss(self, ctx, member: discord.Member):
        """Kiss a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes besarte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime kiss")
        print(f"DEBUG: Kiss GIF URL: {gif_url}")  # Debug line

        embed = discord.Embed(
            title="💋 Beso!",
            description=f"{ctx.author.mention} besó a {member.mention}!",
            color=0xff69b4
        )
        embed.set_footer(text="¡Qué romántico!")

        embed.set_image(url=gif_url)

        try:
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error sending kiss embed: {e}")
            # Fallback: send just the text and URL
            await ctx.send(f"💋 **Beso!** {ctx.author.mention} besó a {member.mention}!\n¡Qué romántico!\n{gif_url}")

    @commands.command(name='pat')
    async def pat(self, ctx, member: discord.Member):
        """Pat a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes acariciarte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime pat")
        print(f"DEBUG: Pat GIF URL: {gif_url}")  # Debug line

        embed = discord.Embed(
            title="👋 Caricia!",
            description=f"{ctx.author.mention} acarició a {member.mention}!",
            color=0x98d8c8
        )
        embed.set_footer(text="¡Buen trabajo!")

        embed.set_image(url=gif_url)

        try:
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error sending pat embed: {e}")
            # Fallback: send just the text and URL
            await ctx.send(f"👋 **Caricia!** {ctx.author.mention} acarició a {member.mention}!\n¡Buen trabajo!\n{gif_url}")

    @commands.command(name='tickle')
    async def tickle(self, ctx, member: discord.Member):
        """Tickle a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes hacerte cosquillas a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime tickle")
            print(f"DEBUG: Tickle GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="😂 Cosquillas!",
                description=f"{ctx.author.mention} le hizo cosquillas a {member.mention}!",
                color=0xf7dc6f
            )
            embed.set_footer(text="¡Para! ¡Me muero de risa!")

            embed.set_image(url=gif_url)
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in tickle command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"😂 **Cosquillas!** {ctx.author.mention} le hizo cosquillas a {member.mention}!\n¡Para! ¡Me muero de risa!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in tickle: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='feed')
    async def feed(self, ctx, member: discord.Member):
        """Feed a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes alimentarte a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime feed")
            print(f"DEBUG: Feed GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="🍜 Alimentar!",
                description=f"{ctx.author.mention} alimentó a {member.mention}!",
                color=0xf8c471
            )
            embed.set_footer(text="¡Ñam ñam!")

            embed.set_image(url=gif_url)
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in feed command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"🍜 **Alimentar!** {ctx.author.mention} alimentó a {member.mention}!\n¡Ñam ñam!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in feed: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='punch')
    async def punch(self, ctx, member: discord.Member):
        """Punch a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes golpearte a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime punch")
            print(f"DEBUG: Punch GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="👊 Golpe!",
                description=f"{ctx.author.mention} golpeó a {member.mention}!",
                color=0xe74c3c
            )
            embed.set_footer(text="¡Uff! Eso dolió!")

            embed.set_image(url=gif_url)
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in punch command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"👊 **Golpe!** {ctx.author.mention} golpeó a {member.mention}!\n¡Uff! Eso dolió!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in punch: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='highfive')
    async def highfive(self, ctx, member: discord.Member):
        """High five a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes chocar los cinco contigo mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime high five")
            print(f"DEBUG: Highfive GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="✋ Choca esos cinco!",
                description=f"{ctx.author.mention} chocó los cinco con {member.mention}!",
                color=0x85c1e9
            )
            embed.set_footer(text="¡Genial!")

            embed.set_image(url=gif_url)
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in highfive command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"✋ **Choca esos cinco!** {ctx.author.mention} chocó los cinco con {member.mention}!\n¡Genial!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in highfive: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='bite')
    async def bite(self, ctx, member: discord.Member):
        """Bite a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes morderte a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime bite")
            print(f"DEBUG: Bite GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="🦷 Mordida!",
                description=f"{ctx.author.mention} mordió a {member.mention}!",
                color=0xd7bde2
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Ay! Eso dejó marca!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in bite command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"🦷 **Mordida!** {ctx.author.mention} mordió a {member.mention}!\n¡Ay! Eso dejó marca!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in bite: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='shoot')
    async def shoot(self, ctx, member: discord.Member):
        """Shoot a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes dispararte a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime shoot")
            print(f"DEBUG: Shoot GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="🔫 Disparo!",
                description=f"{ctx.author.mention} disparó a {member.mention}!",
                color=0x2c3e50
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Bang! ¡Estás muerto!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in shoot command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"🔫 **Disparo!** {ctx.author.mention} disparó a {member.mention}!\n¡Bang! ¡Estás muerto!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in shoot: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='wave')
    async def wave(self, ctx, member: discord.Member):
        """Wave at a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes saludarte a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime wave")
            print(f"DEBUG: Wave GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="👋 Saludo!",
                description=f"{ctx.author.mention} saludó a {member.mention}!",
                color=0x85c1e9
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Hola!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in wave command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"👋 **Saludo!** {ctx.author.mention} saludó a {member.mention}!\n¡Hola!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in wave: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='happy')
    async def happy(self, ctx, member: discord.Member):
        """Show happiness to a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes estar feliz contigo mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime happy")
            print(f"DEBUG: Happy GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="😊 Feliz!",
                description=f"{ctx.author.mention} está feliz con {member.mention}!",
                color=0xf7dc6f
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Yay!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in happy command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"😊 **Feliz!** {ctx.author.mention} está feliz con {member.mention}!\n¡Yay!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in happy: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='peck')
    async def peck(self, ctx, member: discord.Member):
        """Peck a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes picotearte a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime peck")
            print(f"DEBUG: Peck GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="💋 Picoteo!",
                description=f"{ctx.author.mention} picoteó a {member.mention}!",
                color=0xff69b4
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Qué lindo!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in peck command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"💋 **Picoteo!** {ctx.author.mention} picoteó a {member.mention}!\n¡Qué lindo!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in peck: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='lurk')
    async def lurk(self, ctx, member: discord.Member):
        """Lurk at a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes acecharte a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime lurk")
            print(f"DEBUG: Lurk GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="👀 Acechando!",
                description=f"{ctx.author.mention} está acechando a {member.mention}!",
                color=0x34495e
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Te estoy vigilando!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in lurk command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"👀 **Acechando!** {ctx.author.mention} está acechando a {member.mention}!\n¡Te estoy vigilando!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in lurk: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='sleep')
    async def sleep(self, ctx, member: discord.Member):
        """Sleep with a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes dormir contigo mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime sleep")
            print(f"DEBUG: Sleep GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="😴 Durmiendo!",
                description=f"{ctx.author.mention} está durmiendo con {member.mention}!",
                color=0x5d6d7e
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Shh! No hagas ruido!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in sleep command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"😴 **Durmiendo!** {ctx.author.mention} está durmiendo con {member.mention}!\n¡Shh! No hagas ruido!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in sleep: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='wink')
    async def wink(self, ctx, member: discord.Member):
        """Wink at a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes guiñarte a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime wink")
            print(f"DEBUG: Wink GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="😉 Guiño!",
                description=f"{ctx.author.mention} le guiñó a {member.mention}!",
                color=0xf39c12
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Te entiendo!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in wink command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"😉 **Guiño!** {ctx.author.mention} le guiñó a {member.mention}!\n¡Te entiendo!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in wink: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='yawn')
    async def yawn(self, ctx, member: discord.Member):
        """Yawn at a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes bostezar contigo mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime yawn")
            print(f"DEBUG: Yawn GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="😪 Bostezando!",
                description=f"{ctx.author.mention} bostezó con {member.mention}!",
                color=0x95a5a6
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Qué sueño!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in yawn command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"😪 **Bostezando!** {ctx.author.mention} bostezó con {member.mention}!\n¡Qué sueño!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in yawn: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='nom')
    async def nom(self, ctx, member: discord.Member):
        """Nom a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes nom contigo mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime nom")
            print(f"DEBUG: Nom GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="🍖 Nom!",
                description=f"{ctx.author.mention} nom a {member.mention}!",
                color=0xe67e22
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Ñam ñam ñam!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in nom command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"🍖 **Nom!** {ctx.author.mention} nom a {member.mention}!\n¡Ñam ñam ñam!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in nom: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='yeet')
    async def yeet(self, ctx, member: discord.Member):
        """Yeet a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes yeet a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime yeet")
            print(f"DEBUG: Yeet GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="🚀 Yeet!",
                description=f"{ctx.author.mention} yeeteó a {member.mention}!",
                color=0x9b59b6
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Vuela!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in yeet command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"🚀 **Yeet!** {ctx.author.mention} yeeteó a {member.mention}!\n¡Vuela!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in yeet: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='think')
    async def think(self, ctx, member: discord.Member):
        """Think about a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes pensar en ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime think")
            print(f"DEBUG: Think GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="🤔 Pensando!",
                description=f"{ctx.author.mention} está pensando en {member.mention}!",
                color=0x3498db
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¿Qué estará pensando?")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in think command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"🤔 **Pensando!** {ctx.author.mention} está pensando en {member.mention}!\n¿Qué estará pensando?\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in think: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='bored')
    async def bored(self, ctx, member: discord.Member):
        """Be bored with a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes aburrirte contigo mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime bored")
            print(f"DEBUG: Bored GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="😴 Aburrido!",
                description=f"{ctx.author.mention} está aburrido con {member.mention}!",
                color=0x7f8c8d
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Qué aburrimiento!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in bored command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"😴 **Aburrido!** {ctx.author.mention} está aburrido con {member.mention}!\n¡Qué aburrimiento!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in bored: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='blush')
    async def blush(self, ctx, member: discord.Member):
        """Blush at a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes sonrojarte contigo mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime blush")
            print(f"DEBUG: Blush GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="😊 Sonrojado!",
                description=f"{ctx.author.mention} se sonrojó con {member.mention}!",
                color=0xffb3ba
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Qué lindo!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in blush command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"😊 **Sonrojado!** {ctx.author.mention} se sonrojó con {member.mention}!\n¡Qué lindo!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in blush: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='stare')
    async def stare(self, ctx, member: discord.Member):
        """Stare at a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes mirarte a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime stare")
            print(f"DEBUG: Stare GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="👀 Mirando!",
                description=f"{ctx.author.mention} está mirando a {member.mention}!",
                color=0x34495e
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¿Qué miras?")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in stare command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"👀 **Mirando!** {ctx.author.mention} está mirando a {member.mention}!\n¿Qué miras?\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in stare: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='nod')
    async def nod(self, ctx, member: discord.Member):
        """Nod at a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes asentir contigo mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime nod")
            print(f"DEBUG: Nod GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="👍 Asintiendo!",
                description=f"{ctx.author.mention} asintió a {member.mention}!",
                color=0x27ae60
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡De acuerdo!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in nod command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"👍 **Asintiendo!** {ctx.author.mention} asintió a {member.mention}!\n¡De acuerdo!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in nod: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='handhold')
    async def handhold(self, ctx, member: discord.Member):
        """Hold hands with a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes tomar tu propia mano!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime handhold")
            print(f"DEBUG: Handhold GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="🤝 Tomando la mano!",
                description=f"{ctx.author.mention} tomó la mano de {member.mention}!",
                color=0xf8c471
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Qué romántico!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in handhold command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"🤝 **Tomando la mano!** {ctx.author.mention} tomó la mano de {member.mention}!\n¡Qué romántico!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in handhold: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='smug')
    async def smug(self, ctx, member: discord.Member):
        """Be smug at a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes ser presumido contigo mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime smug")
            print(f"DEBUG: Smug GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="😏 Presumido!",
                description=f"{ctx.author.mention} está siendo presumido con {member.mention}!",
                color=0x8e44ad
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Ja! ¡Te gané!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in smug command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"😏 **Presumido!** {ctx.author.mention} está siendo presumido con {member.mention}!\n¡Ja! ¡Te gané!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in smug: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='fuck')
    async def fuck(self, ctx, member: discord.Member):
        """Fuck a user with an anime GIF (NSFW)"""
        if member == ctx.author:
            await ctx.send("❌ No puedes follarte a ti mismo!")
            return

        # Check NSFW setting
        guild_id = ctx.guild.id
        if guild_id in nsfw_settings and not nsfw_settings[guild_id]:
            await ctx.send("❌ Los comandos NSFW están desactivados en este servidor. Usa `!togglensfw` para activarlos.")
            return

        try:
            gif_url = gif_api.get_gif_url("anime fuck")
            print(f"DEBUG: Fuck GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="🔞 Follando!",
                description=f"{ctx.author.mention} folló a {member.mention}!",
                color=0xe74c3c
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Qué caliente!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in fuck command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"🔞 **Follando!** {ctx.author.mention} folló a {member.mention}!\n¡Qué caliente!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in fuck: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='spank')
    async def spank(self, ctx, member: discord.Member):
        """Spank a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes azotarte a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime spank")
            print(f"DEBUG: Spank GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="👋 Azotando!",
                description=f"{ctx.author.mention} azotó a {member.mention}!",
                color=0xff6b6b
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Eso dolió!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in spank command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"👋 **Azotando!** {ctx.author.mention} azotó a {member.mention}!\n¡Eso dolió!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in spank: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='nutkick')
    async def nutkick(self, ctx, member: discord.Member):
        """Nutkick a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes patearte las bolas a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime nutkick")
            print(f"DEBUG: Nutkick GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="🥜 Patada en las bolas!",
                description=f"{ctx.author.mention} le dio una patada en las bolas a {member.mention}!",
                color=0x2c3e50
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Ay! ¡Mis bolas!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in nutkick command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"🥜 **Patada en las bolas!** {ctx.author.mention} le dio una patada en las bolas a {member.mention}!\n¡Ay! ¡Mis bolas!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in nutkick: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='shrug')
    async def shrug(self, ctx, member: discord.Member):
        """Shrug at a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes encogerte de hombros contigo mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime shrug")
            print(f"DEBUG: Shrug GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="🤷 Encogerse de hombros!",
                description=f"{ctx.author.mention} se encogió de hombros con {member.mention}!",
                color=0x95a5a6
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="No sé...")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in shrug command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"🤷 **Encogerse de hombros!** {ctx.author.mention} se encogió de hombros con {member.mention}!\nNo sé...\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in shrug: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='poke')
    async def poke(self, ctx, member: discord.Member):
        """Poke a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes picarte a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime poke")
            print(f"DEBUG: Poke GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="👆 Picando!",
                description=f"{ctx.author.mention} picó a {member.mention}!",
                color=0x3498db
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Hey! ¡Mírame!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in poke command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"👆 **Picando!** {ctx.author.mention} picó a {member.mention}!\n¡Hey! ¡Mírame!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in poke: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='smile')
    async def smile(self, ctx, member: discord.Member):
        """Smile at a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes sonreírte a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime smile")
            print(f"DEBUG: Smile GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="😊 Sonriendo!",
                description=f"{ctx.author.mention} sonrió a {member.mention}!",
                color=0xf7dc6f
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Qué linda sonrisa!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in smile command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"😊 **Sonriendo!** {ctx.author.mention} sonrió a {member.mention}!\n¡Qué linda sonrisa!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in smile: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='facepalm')
    async def facepalm(self, ctx, member: discord.Member):
        """Facepalm at a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes hacer facepalm contigo mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime facepalm")
            print(f"DEBUG: Facepalm GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="🤦 Facepalm!",
                description=f"{ctx.author.mention} hizo facepalm con {member.mention}!",
                color=0x95a5a6
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Dios mío!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in facepalm command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"🤦 **Facepalm!** {ctx.author.mention} hizo facepalm con {member.mention}!\n¡Dios mío!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in facepalm: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='cuddle')
    async def cuddle(self, ctx, member: discord.Member):
        """Cuddle a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes acurrucarte contigo mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime cuddle")
            print(f"DEBUG: Cuddle GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="🤗 Acurrucando!",
                description=f"{ctx.author.mention} acurrucó a {member.mention}!",
                color=0xffb3ba
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Qué tierno!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in cuddle command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"🤗 **Acurrucando!** {ctx.author.mention} acurrucó a {member.mention}!\n¡Qué tierno!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in cuddle: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='baka')
    async def baka(self, ctx, member: discord.Member):
        """Call someone baka with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes llamarte baka a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime baka")
            print(f"DEBUG: Baka GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="💢 Baka!",
                description=f"{ctx.author.mention} llamó baka a {member.mention}!",
                color=0xe74c3c
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Baka baka!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in baka command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"💢 **Baka!** {ctx.author.mention} llamó baka a {member.mention}!\n¡Baka baka!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in baka: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='angry')
    async def angry(self, ctx, member: discord.Member):
        """Be angry at a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes enojarte contigo mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime angry")
            print(f"DEBUG: Angry GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="😠 Enojado!",
                description=f"{ctx.author.mention} está enojado con {member.mention}!",
                color=0xe74c3c
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Grr!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in angry command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"😠 **Enojado!** {ctx.author.mention} está enojado con {member.mention}!\n¡Grr!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in angry: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='run')
    async def run(self, ctx, member: discord.Member):
        """Run with a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes correr contigo mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime run")
            print(f"DEBUG: Run GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="🏃 Corriendo!",
                description=f"{ctx.author.mention} está corriendo con {member.mention}!",
                color=0x3498db
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Corre!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in run command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"🏃 **Corriendo!** {ctx.author.mention} está corriendo con {member.mention}!\n¡Corre!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in run: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='nope')
    async def nope(self, ctx, member: discord.Member):
        """Nope at a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes nope contigo mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime nope")
            print(f"DEBUG: Nope GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="❌ Nope!",
                description=f"{ctx.author.mention} dijo nope a {member.mention}!",
                color=0x95a5a6
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡No!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in nope command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"❌ **Nope!** {ctx.author.mention} dijo nope a {member.mention}!\n¡No!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in nope: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='handshake')
    async def handshake(self, ctx, member: discord.Member):
        """Handshake with a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes estrechar tu propia mano!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime handshake")
            print(f"DEBUG: Handshake GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="🤝 Estrechando la mano!",
                description=f"{ctx.author.mention} estrechó la mano con {member.mention}!",
                color=0x27ae60
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Encantado de conocerte!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in handshake command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"🤝 **Estrechando la mano!** {ctx.author.mention} estrechó la mano con {member.mention}!\n¡Encantado de conocerte!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in handshake: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='cry')
    async def cry(self, ctx, member: discord.Member):
        """Cry with a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes llorar contigo mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime cry")
            print(f"DEBUG: Cry GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="😢 Llorando!",
                description=f"{ctx.author.mention} está llorando con {member.mention}!",
                color=0x5d6d7e
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Buu!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in cry command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"😢 **Llorando!** {ctx.author.mention} está llorando con {member.mention}!\n¡Buu!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in cry: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='pout')
    async def pout(self, ctx, member: discord.Member):
        """Pout at a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes hacer pucheros contigo mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime pout")
            print(f"DEBUG: Pout GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="😣 Pucheros!",
                description=f"{ctx.author.mention} hizo pucheros con {member.mention}!",
                color=0xffb3ba
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡No es justo!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in pout command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"😣 **Pucheros!** {ctx.author.mention} hizo pucheros con {member.mention}!\n¡No es justo!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in pout: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='thumbsup')
    async def thumbsup(self, ctx, member: discord.Member):
        """Thumbs up at a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes dar thumbs up a ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime thumbs up")
            print(f"DEBUG: Thumbsup GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="👍 Thumbs Up!",
                description=f"{ctx.author.mention} dio thumbs up a {member.mention}!",
                color=0x27ae60
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Bien hecho!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in thumbsup command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"👍 **Thumbs Up!** {ctx.author.mention} dio thumbs up a {member.mention}!\n¡Bien hecho!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in thumbsup: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

    @commands.command(name='laugh')
    async def laugh(self, ctx, member: discord.Member):
        """Laugh at a user with an anime GIF"""
        if member == ctx.author:
            await ctx.send("❌ No puedes reírte de ti mismo!")
            return

        try:
            gif_url = gif_api.get_gif_url("anime laugh")
            print(f"DEBUG: Laugh GIF URL: {gif_url}")  # Debug line

            embed = discord.Embed(
                title="😂 Riendo!",
                description=f"{ctx.author.mention} se rió de {member.mention}!",
                color=0xf7dc6f
            )
            embed.set_image(url=gif_url)
            embed.set_footer(text="¡Ja ja ja!")

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in laugh command: {e}")
            try:
                # Fallback: send just the text and URL
                await ctx.send(f"😂 **Riendo!** {ctx.author.mention} se rió de {member.mention}!\n¡Ja ja ja!\n*(Error al cargar el GIF)*")
            except Exception as fallback_error:
                print(f"Fallback error in laugh: {fallback_error}")
                await ctx.send("¡Error al ejecutar el comando!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(InteractionsCog(bot))
