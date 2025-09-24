import discord
from discord.ext import commands
import random
import requests
import json
import math

class FunCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll')
    async def roll(self, ctx, dice: str):
        """Roll dice (e.g., 1d20, 2d6+3)"""
        try:
            # Parse dice notation
            if '+' in dice:
                dice_part, modifier = dice.split('+', 1)
                modifier = int(modifier)
            else:
                dice_part = dice
                modifier = 0

            if 'd' in dice_part:
                count, sides = dice_part.split('d', 1)
                count = int(count) if count else 1
                sides = int(sides)
            else:
                count = 1
                sides = int(dice_part)

            # Validate input
            if count > 20:
                await ctx.send("❌ No puedes tirar más de 20 dados a la vez.")
                return
            if sides > 1000:
                await ctx.send("❌ Los dados no pueden tener más de 1000 caras.")
                return
            if count < 1 or sides < 2:
                await ctx.send("❌ Valores inválidos para dados.")
                return

            # Roll the dice
            rolls = [random.randint(1, sides) for _ in range(count)]
            total = sum(rolls) + modifier

            # Create response
            if count == 1:
                embed = discord.Embed(
                    title="🎲 Tirada de dados",
                    description=f"**{sides} caras:** {rolls[0]}",
                    color=0x3498db
                )
                if modifier:
                    embed.description += f" + {modifier} = **{total}**"
            else:
                embed = discord.Embed(
                    title="🎲 Tiradas de dados",
                    description=f"**{count}d{sides}:** {', '.join(map(str, rolls))}",
                    color=0x3498db
                )
                if modifier:
                    embed.description += f" + {modifier} = **{total}**"
                embed.add_field(name="Total", value=str(total), inline=True)
                embed.add_field(name="Promedio", value=f"{total/count:.1f}", inline=True)

            await ctx.send(embed=embed)

        except ValueError:
            await ctx.send("❌ Formato inválido. Usa: `!roll 1d20` o `!roll 2d6+3`")

    @commands.command(name='coinflip')
    async def coinflip(self, ctx):
        """Flip a coin"""
        result = random.choice(["Cara", "Cruz"])

        embed = discord.Embed(
            title="🪙 Lanzando moneda...",
            description=f"**{result}!**",
            color=0xf1c40f
        )

        await ctx.send(embed=embed)

    @commands.command(name='joke')
    async def joke(self, ctx):
        """Get a random joke"""
        try:
            response = requests.get("https://v2.jokeapi.dev/joke/Any?lang=es")
            if response.status_code == 200:
                data = response.json()
                if data["type"] == "single":
                    joke = data["joke"]
                else:
                    joke = f"{data['setup']}\n\n{data['delivery']}"

                embed = discord.Embed(
                    title="😂 Chiste aleatorio",
                    description=joke,
                    color=0xe67e22
                )
                embed.set_footer(text="Fuente: JokeAPI")
            else:
                embed = discord.Embed(
                    title="😂 Chiste aleatorio",
                    description="¿Por qué el programador no puede dormir?\n\n¡Porque tiene bugs en la cabeza!",
                    color=0xe67e22
                )

            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="😂 Chiste aleatorio",
                description="¿Por qué el programador no puede dormir?\n\n¡Porque tiene bugs en la cabeza!",
                color=0xe67e22
            )
            await ctx.send(embed=embed)

    @commands.command(name='fact')
    async def fact(self, ctx):
        """Get a random fact"""
        try:
            response = requests.get("https://uselessfacts.jsph.pl/random.json?language=es")
            if response.status_code == 200:
                data = response.json()
                fact = data["text"]

                embed = discord.Embed(
                    title="💡 Dato curioso",
                    description=fact,
                    color=0x9b59b6
                )
                embed.set_footer(text="Fuente: Useless Facts")
            else:
                embed = discord.Embed(
                    title="💡 Dato curioso",
                    description="¿Sabías que el primer programador fue una mujer? Ada Lovelace escribió el primer algoritmo en 1843.",
                    color=0x9b59b6
                )

            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="💡 Dato curioso",
                description="¿Sabías que el primer programador fue una mujer? Ada Lovelace escribió el primer algoritmo en 1843.",
                color=0x9b59b6
            )
            await ctx.send(embed=embed)

    @commands.command(name='meme')
    async def meme(self, ctx):
        """Get a random programming meme"""
        try:
            response = requests.get("https://programming-memes-images.p.rapidapi.com/v1/memes", headers={
                "X-RapidAPI-Key": "your-api-key-here"  # You'll need to get an API key
            })

            if response.status_code == 200:
                data = response.json()
                meme_url = data[0]["image"]

                embed = discord.Embed(
                    title="😂 Meme de programador",
                    color=0xe74c3c
                )
                embed.set_image(url=meme_url)
                embed.set_footer(text="Fuente: Programming Memes API")
            else:
                # Fallback memes
                memes = [
                    "https://i.imgur.com/1Za8c1Q.png",  # This is fine meme
                    "https://i.imgur.com/2QZ1Z3Q.png",  # Distracted boyfriend
                    "https://i.imgur.com/4Z3Z3Z3.png",  # Expanding brain
                    "https://i.imgur.com/5Y4Y4Y4.png",  # Drake hotline bling
                    "https://i.imgur.com/6X5X5X5.png"   # Success kid
                ]
                meme_url = random.choice(memes)

                embed = discord.Embed(
                    title="😂 Meme de programador",
                    color=0xe74c3c
                )
                embed.set_image(url=meme_url)
                embed.set_footer(text="Fuente: Colección de memes")

            await ctx.send(embed=embed)

        except Exception as e:
            # Fallback memes
            memes = [
                "https://i.imgur.com/1Za8c1Q.png",  # This is fine meme
                "https://i.imgur.com/2QZ1Z3Q.png",  # Distracted boyfriend
                "https://i.imgur.com/4Z3Z3Z3.png",  # Expanding brain
                "https://i.imgur.com/5Y4Y4Y4.png",  # Drake hotline bling
                "https://i.imgur.com/6X5X5X5.png"   # Success kid
            ]
            meme_url = random.choice(memes)

            embed = discord.Embed(
                title="😂 Meme de programador",
                color=0xe74c3c
            )
            embed.set_image(url=meme_url)
            embed.set_footer(text="Fuente: Colección de memes")

            await ctx.send(embed=embed)

    @commands.command(name='8ball')
    async def eightball(self, ctx, *, question):
        """Ask the magic 8-ball a question"""
        responses = [
            "Es cierto",
            "Definitivamente sí",
            "Sin duda",
            "Sí, definitivamente",
            "Puedes confiar en ello",
            "Como yo lo veo, sí",
            "Lo más probable",
            "Perspectiva buena",
            "Sí",
            "Las señales apuntan a sí",
            "Respuesta confusa, intenta de nuevo",
            "Pregunta más tarde",
            "Mejor no decirte ahora",
            "No se puede predecir ahora",
            "Concéntrate y pregunta de nuevo",
            "No cuentes con ello",
            "Mi respuesta es no",
            "Mis fuentes dicen que no",
            "Perspectiva no tan buena",
            "Muy dudoso"
        ]

        response = random.choice(responses)

        embed = discord.Embed(
            title="🔮 Magic 8-Ball",
            color=0x8e44ad
        )
        embed.add_field(name="❓ Pregunta", value=question, inline=False)
        embed.add_field(name="🔮 Respuesta", value=response, inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='choose')
    async def choose(self, ctx, *, options):
        """Choose between multiple options (separate with commas)"""
        choices = [choice.strip() for choice in options.split(',') if choice.strip()]

        if len(choices) < 2:
            await ctx.send("❌ Necesitas al menos 2 opciones separadas por comas.")
            return

        if len(choices) > 10:
            await ctx.send("❌ Máximo 10 opciones permitidas.")
            return

        choice = random.choice(choices)

        embed = discord.Embed(
            title="🎯 Elegir",
            description=f"**Opciones:** {', '.join(choices)}\n\n**Elegido:** {choice}",
            color=0x27ae60
        )

        await ctx.send(embed=embed)

    @commands.command(name='rate')
    async def rate(self, ctx, *, thing):
        """Rate something on a scale of 1-10"""
        rating = random.randint(1, 10)

        embed = discord.Embed(
            title="⭐ Calificación",
            description=f"Califico **{thing}** como **{rating}/10**",
            color=0xf39c12
        )

        # Add stars based on rating
        stars = "⭐" * rating + "☆" * (10 - rating)
        embed.add_field(name="Visual", value=stars, inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='reverse')
    async def reverse(self, ctx, *, text):
        """Reverse the given text"""
        reversed_text = text[::-1]

        embed = discord.Embed(
            title="🔄 Texto invertido",
            color=0x34495e
        )
        embed.add_field(name="Original", value=text, inline=False)
        embed.add_field(name="Invertido", value=reversed_text, inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='password')
    async def password(self, ctx, length: int = 12):
        """Generate a random password"""
        if length < 4:
            await ctx.send("❌ La longitud mínima es 4 caracteres.")
            return
        if length > 50:
            await ctx.send("❌ La longitud máxima es 50 caracteres.")
            return

        # Generate password with different character types
        lowercase = "abcdefghijklmnopqrstuvwxyz"
        uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numbers = "0123456789"
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"

        # Ensure at least one of each type
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(numbers),
            random.choice(symbols)
        ]

        # Fill the rest randomly
        all_chars = lowercase + uppercase + numbers + symbols
        for _ in range(length - 4):
            password.append(random.choice(all_chars))

        # Shuffle the password
        random.shuffle(password)
        final_password = ''.join(password)

        embed = discord.Embed(
            title="🔐 Generador de contraseñas",
            description=f"Contraseña generada de {length} caracteres:",
            color=0xe74c3c
        )
        embed.add_field(name="Contraseña", value=f"||{final_password}||", inline=False)
        embed.set_footer(text="⚠️ Copia la contraseña antes de que desaparezca")

        await ctx.send(embed=embed)

    @commands.command(name='color')
    async def color(self, ctx, hex_color: str = None):
        """Show information about a color or generate a random one"""
        if hex_color is None:
            # Generate random color
            hex_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        else:
            # Validate hex color
            if not hex_color.startswith('#'):
                hex_color = '#' + hex_color

            if len(hex_color) != 7:
                await ctx.send("❌ Formato de color inválido. Usa: #RRGGBB")
                return

            try:
                int(hex_color[1:], 16)
            except ValueError:
                await ctx.send("❌ Color hexadecimal inválido.")
                return

        # Convert hex to RGB
        hex_value = hex_color[1:]
        r = int(hex_value[0:2], 16)
        g = int(hex_value[2:4], 16)
        b = int(hex_value[4:6], 16)

        # Calculate brightness
        brightness = (r * 299 + g * 587 + b * 114) / 1000

        embed = discord.Embed(
            title="🎨 Información del color",
            color=int(hex_value, 16)
        )

        embed.add_field(name="🔢 Hex", value=hex_color.upper(), inline=True)
        embed.add_field(name="🔴 RGB", value=f"({r}, {g}, {b})", inline=True)
        embed.add_field(name="📊 Brillo", value=f"{brightness:.0f}/255", inline=True)

        # Add color name if possible
        if brightness > 128:
            embed.add_field(name="🌙 Contraste", value="Oscuro recomendado", inline=True)
        else:
            embed.add_field(name="☀️ Contraste", value="Claro recomendado", inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='emojify')
    async def emojify(self, ctx, *, text):
        """Convert text to emoji letters"""
        # Emoji letter mappings
        emoji_letters = {
            'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪', 'f': '🇫', 'g': '🇬', 'h': '🇭',
            'i': '🇮', 'j': '🇯', 'k': '🇰', 'l': '🇱', 'm': '🇲', 'n': '🇳', 'o': '🇴', 'p': '🇵',
            'q': '🇶', 'r': '🇷', 's': '🇸', 't': '🇹', 'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽',
            'y': '🇾', 'z': '🇿', '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣',
            '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣', '10': '🔟'
        }

        emojified = []
        for char in text.lower():
            if char in emoji_letters:
                emojified.append(emoji_letters[char])
            elif char == ' ':
                emojified.append('   ')
            elif char == '!':
                emojified.append('❗')
            elif char == '?':
                emojified.append('❓')
            else:
                emojified.append(char)

        result = ''.join(emojified)

        if len(result) > 2000:
            await ctx.send("❌ El texto es demasiado largo para convertir a emojis.")
            return

        embed = discord.Embed(
            title="🔤 Emojify",
            description=result,
            color=0xf39c12
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(FunCommandsCog(bot))
