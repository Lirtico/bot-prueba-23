import discord
from discord.ext import commands
from gif_api import gif_api
from config.settings import nsfw_settings

class InteractionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='slap')
    async def slap(self, ctx, member: discord.Member = None):
        """Slap a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para abofetear!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes abofetearte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime slap")

        embed = discord.Embed(
            title="👋 Bofetada!",
            description=f"{ctx.author.mention} le dio una bofetada a {member.mention}!",
            color=0xff6b6b
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Ay! Eso tuvo que doler!")

        await ctx.send(embed=embed)

    @commands.command(name='hug')
    async def hug(self, ctx, member: discord.Member = None):
        """Hug a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para abrazar!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes abrazarte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime hug")

        embed = discord.Embed(
            title="🤗 Abrazo!",
            description=f"{ctx.author.mention} abrazó a {member.mention}!",
            color=0xffb3ba
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Aww, qué lindo!")

        await ctx.send(embed=embed)

    @commands.command(name='kiss')
    async def kiss(self, ctx, member: discord.Member = None):
        """Kiss a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para besar!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes besarte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime kiss")

        embed = discord.Embed(
            title="💋 Beso!",
            description=f"{ctx.author.mention} besó a {member.mention}!",
            color=0xff69b4
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Qué romántico!")

        await ctx.send(embed=embed)

    @commands.command(name='pat')
    async def pat(self, ctx, member: discord.Member = None):
        """Pat a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para acariciar!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes acariciarte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime pat")

        embed = discord.Embed(
            title="👋 Caricia!",
            description=f"{ctx.author.mention} acarició a {member.mention}!",
            color=0x98d8c8
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Buen trabajo!")

        await ctx.send(embed=embed)

    @commands.command(name='tickle')
    async def tickle(self, ctx, member: discord.Member = None):
        """Tickle a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para hacer cosquillas!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes hacerte cosquillas a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime tickle")

        embed = discord.Embed(
            title="😂 Cosquillas!",
            description=f"{ctx.author.mention} le hizo cosquillas a {member.mention}!",
            color=0xf7dc6f
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Para! ¡Me muero de risa!")

        await ctx.send(embed=embed)

    @commands.command(name='feed')
    async def feed(self, ctx, member: discord.Member = None):
        """Feed a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para alimentar!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes alimentarte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime feed")

        embed = discord.Embed(
            title="🍜 Alimentar!",
            description=f"{ctx.author.mention} alimentó a {member.mention}!",
            color=0xf8c471
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Ñam ñam!")

        await ctx.send(embed=embed)

    @commands.command(name='punch')
    async def punch(self, ctx, member: discord.Member = None):
        """Punch a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para golpear!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes golpearte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime punch")

        embed = discord.Embed(
            title="👊 Golpe!",
            description=f"{ctx.author.mention} golpeó a {member.mention}!",
            color=0xe74c3c
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Uff! Eso dolió!")

        await ctx.send(embed=embed)

    @commands.command(name='highfive')
    async def highfive(self, ctx, member: discord.Member = None):
        """High five a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para chocar los cinco!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes chocar los cinco contigo mismo!")
            return

        gif_url = gif_api.get_gif_url("anime high five")

        embed = discord.Embed(
            title="✋ Choca esos cinco!",
            description=f"{ctx.author.mention} chocó los cinco con {member.mention}!",
            color=0x85c1e9
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Genial!")

        await ctx.send(embed=embed)

    @commands.command(name='bite')
    async def bite(self, ctx, member: discord.Member = None):
        """Bite a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para morder!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes morderte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime bite")

        embed = discord.Embed(
            title="🦷 Mordida!",
            description=f"{ctx.author.mention} mordió a {member.mention}!",
            color=0xd7bde2
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Ay! Eso dejó marca!")

        await ctx.send(embed=embed)

    @commands.command(name='shoot')
    async def shoot(self, ctx, member: discord.Member = None):
        """Shoot a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para disparar!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes dispararte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime shoot")

        embed = discord.Embed(
            title="🔫 Disparo!",
            description=f"{ctx.author.mention} disparó a {member.mention}!",
            color=0x2c3e50
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Bang! ¡Estás muerto!")

        await ctx.send(embed=embed)

    @commands.command(name='wave')
    async def wave(self, ctx, member: discord.Member = None):
        """Wave at a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para saludar!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes saludarte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime wave")

        embed = discord.Embed(
            title="👋 Saludo!",
            description=f"{ctx.author.mention} saludó a {member.mention}!",
            color=0x85c1e9
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Hola!")

        await ctx.send(embed=embed)

    @commands.command(name='happy')
    async def happy(self, ctx, member: discord.Member = None):
        """Show happiness to a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para estar feliz!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes estar feliz contigo mismo!")
            return

        gif_url = gif_api.get_gif_url("anime happy")

        embed = discord.Embed(
            title="😊 Feliz!",
            description=f"{ctx.author.mention} está feliz con {member.mention}!",
            color=0xf7dc6f
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Yay!")

        await ctx.send(embed=embed)

    @commands.command(name='peck')
    async def peck(self, ctx, member: discord.Member = None):
        """Peck a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para picotear!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes picotearte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime peck")

        embed = discord.Embed(
            title="💋 Picoteo!",
            description=f"{ctx.author.mention} picoteó a {member.mention}!",
            color=0xff69b4
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Qué lindo!")

        await ctx.send(embed=embed)

    @commands.command(name='lurk')
    async def lurk(self, ctx, member: discord.Member = None):
        """Lurk at a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para acechar!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes acecharte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime lurk")

        embed = discord.Embed(
            title="👀 Acechando!",
            description=f"{ctx.author.mention} está acechando a {member.mention}!",
            color=0x34495e
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Te estoy vigilando!")

        await ctx.send(embed=embed)

    @commands.command(name='sleep')
    async def sleep(self, ctx, member: discord.Member = None):
        """Sleep with a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para dormir!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes dormir contigo mismo!")
            return

        gif_url = gif_api.get_gif_url("anime sleep")

        embed = discord.Embed(
            title="😴 Durmiendo!",
            description=f"{ctx.author.mention} está durmiendo con {member.mention}!",
            color=0x5d6d7e
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Shh! No hagas ruido!")

        await ctx.send(embed=embed)

    @commands.command(name='wink')
    async def wink(self, ctx, member: discord.Member = None):
        """Wink at a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para guiñar!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes guiñarte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime wink")

        embed = discord.Embed(
            title="😉 Guiño!",
            description=f"{ctx.author.mention} le guiñó a {member.mention}!",
            color=0xf39c12
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Te entiendo!")

        await ctx.send(embed=embed)

    @commands.command(name='yawn')
    async def yawn(self, ctx, member: discord.Member = None):
        """Yawn at a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para bostezar!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes bostezar contigo mismo!")
            return

        gif_url = gif_api.get_gif_url("anime yawn")

        embed = discord.Embed(
            title="😪 Bostezando!",
            description=f"{ctx.author.mention} bostezó con {member.mention}!",
            color=0x95a5a6
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Qué sueño!")

        await ctx.send(embed=embed)

    @commands.command(name='nom')
    async def nom(self, ctx, member: discord.Member = None):
        """Nom a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para nom!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes nom contigo mismo!")
            return

        gif_url = gif_api.get_gif_url("anime nom")

        embed = discord.Embed(
            title="🍖 Nom!",
            description=f"{ctx.author.mention} nom a {member.mention}!",
            color=0xe67e22
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Ñam ñam ñam!")

        await ctx.send(embed=embed)

    @commands.command(name='yeet')
    async def yeet(self, ctx, member: discord.Member = None):
        """Yeet a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para yeet!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes yeet a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime yeet")

        embed = discord.Embed(
            title="🚀 Yeet!",
            description=f"{ctx.author.mention} yeeteó a {member.mention}!",
            color=0x9b59b6
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Vuela!")

        await ctx.send(embed=embed)

    @commands.command(name='think')
    async def think(self, ctx, member: discord.Member = None):
        """Think about a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para pensar!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes pensar en ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime think")

        embed = discord.Embed(
            title="🤔 Pensando!",
            description=f"{ctx.author.mention} está pensando en {member.mention}!",
            color=0x3498db
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¿Qué estará pensando?")

        await ctx.send(embed=embed)

    @commands.command(name='bored')
    async def bored(self, ctx, member: discord.Member = None):
        """Be bored with a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para aburrirte!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes aburrirte contigo mismo!")
            return

        gif_url = gif_api.get_gif_url("anime bored")

        embed = discord.Embed(
            title="😴 Aburrido!",
            description=f"{ctx.author.mention} está aburrido con {member.mention}!",
            color=0x7f8c8d
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Qué aburrimiento!")

        await ctx.send(embed=embed)

    @commands.command(name='blush')
    async def blush(self, ctx, member: discord.Member = None):
        """Blush at a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para sonrojar!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes sonrojarte contigo mismo!")
            return

        gif_url = gif_api.get_gif_url("anime blush")

        embed = discord.Embed(
            title="😊 Sonrojado!",
            description=f"{ctx.author.mention} se sonrojó con {member.mention}!",
            color=0xffb3ba
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Qué lindo!")

        await ctx.send(embed=embed)

    @commands.command(name='stare')
    async def stare(self, ctx, member: discord.Member = None):
        """Stare at a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para mirar!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes mirarte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime stare")

        embed = discord.Embed(
            title="👀 Mirando!",
            description=f"{ctx.author.mention} está mirando a {member.mention}!",
            color=0x34495e
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¿Qué miras?")

        await ctx.send(embed=embed)

    @commands.command(name='nod')
    async def nod(self, ctx, member: discord.Member = None):
        """Nod at a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para asentir!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes asentir contigo mismo!")
            return

        gif_url = gif_api.get_gif_url("anime nod")

        embed = discord.Embed(
            title="👍 Asintiendo!",
            description=f"{ctx.author.mention} asintió a {member.mention}!",
            color=0x27ae60
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡De acuerdo!")

        await ctx.send(embed=embed)

    @commands.command(name='handhold')
    async def handhold(self, ctx, member: discord.Member = None):
        """Hold hands with a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para tomar de la mano!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes tomar tu propia mano!")
            return

        gif_url = gif_api.get_gif_url("anime handhold")

        embed = discord.Embed(
            title="🤝 Tomando la mano!",
            description=f"{ctx.author.mention} tomó la mano de {member.mention}!",
            color=0xf8c471
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Qué romántico!")

        await ctx.send(embed=embed)

    @commands.command(name='smug')
    async def smug(self, ctx, member: discord.Member = None):
        """Be smug at a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para ser presumido!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes ser presumido contigo mismo!")
            return

        gif_url = gif_api.get_gif_url("anime smug")

        embed = discord.Embed(
            title="😏 Presumido!",
            description=f"{ctx.author.mention} está siendo presumido con {member.mention}!",
            color=0x8e44ad
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Ja! ¡Te gané!")

        await ctx.send(embed=embed)

    @commands.command(name='fuck')
    async def fuck(self, ctx, member: discord.Member = None):
        """Fuck a user with an anime GIF (NSFW)"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para follar!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes follarte a ti mismo!")
            return

        # Check NSFW setting
        guild_id = ctx.guild.id
        if guild_id in nsfw_settings and not nsfw_settings[guild_id]:
            await ctx.send("❌ Los comandos NSFW están desactivados en este servidor. Usa `!togglensfw` para activarlos.")
            return

        gif_url = gif_api.get_gif_url("anime fuck")

        embed = discord.Embed(
            title="🔞 Follando!",
            description=f"{ctx.author.mention} folló a {member.mention}!",
            color=0xe74c3c
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Qué caliente!")

        await ctx.send(embed=embed)

    @commands.command(name='spank')
    async def spank(self, ctx, member: discord.Member = None):
        """Spank a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para azotar!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes azotarte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime spank")

        embed = discord.Embed(
            title="👋 Azotando!",
            description=f"{ctx.author.mention} azotó a {member.mention}!",
            color=0xff6b6b
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Eso dolió!")

        await ctx.send(embed=embed)

    @commands.command(name='nutkick')
    async def nutkick(self, ctx, member: discord.Member = None):
        """Nutkick a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para patada en las bolas!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes patearte las bolas a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime nutkick")

        embed = discord.Embed(
            title="🥜 Patada en las bolas!",
            description=f"{ctx.author.mention} le dio una patada en las bolas a {member.mention}!",
            color=0x2c3e50
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Ay! ¡Mis bolas!")

        await ctx.send(embed=embed)

    @commands.command(name='shrug')
    async def shrug(self, ctx, member: discord.Member = None):
        """Shrug at a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para encogerse de hombros!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes encogerte de hombros contigo mismo!")
            return

        gif_url = gif_api.get_gif_url("anime shrug")

        embed = discord.Embed(
            title="🤷 Encogerse de hombros!",
            description=f"{ctx.author.mention} se encogió de hombros con {member.mention}!",
            color=0x95a5a6
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="No sé...")

        await ctx.send(embed=embed)

    @commands.command(name='poke')
    async def poke(self, ctx, member: discord.Member = None):
        """Poke a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para picar!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes picarte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime poke")

        embed = discord.Embed(
            title="👆 Picando!",
            description=f"{ctx.author.mention} picó a {member.mention}!",
            color=0x3498db
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Hey! ¡Mírame!")

        await ctx.send(embed=embed)

    @commands.command(name='smile')
    async def smile(self, ctx, member: discord.Member = None):
        """Smile at a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para sonreír!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes sonreírte a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime smile")

        embed = discord.Embed(
            title="😊 Sonriendo!",
            description=f"{ctx.author.mention} sonrió a {member.mention}!",
            color=0xf7dc6f
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Qué linda sonrisa!")

        await ctx.send(embed=embed)

    @commands.command(name='facepalm')
    async def facepalm(self, ctx, member: discord.Member = None):
        """Facepalm at a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para facepalm!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes hacer facepalm contigo mismo!")
            return

        gif_url = gif_api.get_gif_url("anime facepalm")

        embed = discord.Embed(
            title="🤦 Facepalm!",
            description=f"{ctx.author.mention} hizo facepalm con {member.mention}!",
            color=0x95a5a6
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Dios mío!")

        await ctx.send(embed=embed)

    @commands.command(name='cuddle')
    async def cuddle(self, ctx, member: discord.Member = None):
        """Cuddle a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para acurrucar!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes acurrucarte contigo mismo!")
            return

        gif_url = gif_api.get_gif_url("anime cuddle")

        embed = discord.Embed(
            title="🤗 Acurrucando!",
            description=f"{ctx.author.mention} acurrucó a {member.mention}!",
            color=0xffb3ba
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Qué tierno!")

        await ctx.send(embed=embed)

    @commands.command(name='baka')
    async def baka(self, ctx, member: discord.Member = None):
        """Call someone baka with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para llamar baka!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes llamarte baka a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime baka")

        embed = discord.Embed(
            title="💢 Baka!",
            description=f"{ctx.author.mention} llamó baka a {member.mention}!",
            color=0xe74c3c
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Baka baka!")

        await ctx.send(embed=embed)

    @commands.command(name='angry')
    async def angry(self, ctx, member: discord.Member = None):
        """Be angry at a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para enojarte!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes enojarte contigo mismo!")
            return

        gif_url = gif_api.get_gif_url("anime angry")

        embed = discord.Embed(
            title="😠 Enojado!",
            description=f"{ctx.author.mention} está enojado con {member.mention}!",
            color=0xe74c3c
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Grr!")

        await ctx.send(embed=embed)

    @commands.command(name='run')
    async def run(self, ctx, member: discord.Member = None):
        """Run with a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para correr!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes correr contigo mismo!")
            return

        gif_url = gif_api.get_gif_url("anime run")

        embed = discord.Embed(
            title="🏃 Corriendo!",
            description=f"{ctx.author.mention} está corriendo con {member.mention}!",
            color=0x3498db
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Corre!")

        await ctx.send(embed=embed)

    @commands.command(name='nope')
    async def nope(self, ctx, member: discord.Member = None):
        """Nope at a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para nope!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes nope contigo mismo!")
            return

        gif_url = gif_api.get_gif_url("anime nope")

        embed = discord.Embed(
            title="❌ Nope!",
            description=f"{ctx.author.mention} dijo nope a {member.mention}!",
            color=0x95a5a6
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡No!")

        await ctx.send(embed=embed)

    @commands.command(name='handshake')
    async def handshake(self, ctx, member: discord.Member = None):
        """Handshake with a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para estrechar la mano!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes estrechar tu propia mano!")
            return

        gif_url = gif_api.get_gif_url("anime handshake")

        embed = discord.Embed(
            title="🤝 Estrechando la mano!",
            description=f"{ctx.author.mention} estrechó la mano con {member.mention}!",
            color=0x27ae60
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Encantado de conocerte!")

        await ctx.send(embed=embed)

    @commands.command(name='cry')
    async def cry(self, ctx, member: discord.Member = None):
        """Cry with a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para llorar!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes llorar contigo mismo!")
            return

        gif_url = gif_api.get_gif_url("anime cry")

        embed = discord.Embed(
            title="😢 Llorando!",
            description=f"{ctx.author.mention} está llorando con {member.mention}!",
            color=0x5d6d7e
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Buu!")

        await ctx.send(embed=embed)

    @commands.command(name='pout')
    async def pout(self, ctx, member: discord.Member = None):
        """Pout at a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para hacer pucheros!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes hacer pucheros contigo mismo!")
            return

        gif_url = gif_api.get_gif_url("anime pout")

        embed = discord.Embed(
            title="😣 Pucheros!",
            description=f"{ctx.author.mention} hizo pucheros con {member.mention}!",
            color=0xffb3ba
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡No es justo!")

        await ctx.send(embed=embed)

    @commands.command(name='thumbsup')
    async def thumbsup(self, ctx, member: discord.Member = None):
        """Thumbs up at a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para thumbs up!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes dar thumbs up a ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime thumbs up")

        embed = discord.Embed(
            title="👍 Thumbs Up!",
            description=f"{ctx.author.mention} dio thumbs up a {member.mention}!",
            color=0x27ae60
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Bien hecho!")

        await ctx.send(embed=embed)

    @commands.command(name='laugh')
    async def laugh(self, ctx, member: discord.Member = None):
        """Laugh at a user with an anime GIF"""
        if member is None:
            await ctx.send("❌ Por favor menciona a un usuario para reír!")
            return

        if member == ctx.author:
            await ctx.send("❌ No puedes reírte de ti mismo!")
            return

        gif_url = gif_api.get_gif_url("anime laugh")

        embed = discord.Embed(
            title="😂 Riendo!",
            description=f"{ctx.author.mention} se rió de {member.mention}!",
            color=0xf7dc6f
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="¡Ja ja ja!")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(InteractionsCog(bot))
