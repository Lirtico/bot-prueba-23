import discord
from discord.ext import commands
import requests
import json
import math
from datetime import datetime, timedelta
import asyncio

class CommunityCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = {}  # Store reminders (user_id -> list of reminders)

    @commands.command(name='poll')
    async def poll(self, ctx, *, question):
        """Create a poll with reactions"""
        embed = discord.Embed(
            title="🗳️ Encuesta",
            description=question,
            color=0x0099ff
        )
        embed.set_footer(text=f"Encuesta creada por {ctx.author.display_name}")
        embed.timestamp = datetime.now()

        # Create the poll message
        poll_message = await ctx.send(embed=embed)

        # Add reactions
        await poll_message.add_reaction("✅")
        await poll_message.add_reaction("❌")
        await poll_message.add_reaction("🤷")

        # Delete the original command message
        await ctx.message.delete()

    @commands.command(name='remind')
    async def remind(self, ctx, minutes: int, *, message):
        """Set a reminder"""
        if minutes < 1:
            await ctx.send("❌ Los minutos deben ser al menos 1.")
            return

        if minutes > 1440:  # 24 hours
            await ctx.send("❌ No puedes establecer recordatorios de más de 24 horas.")
            return

        # Calculate reminder time
        reminder_time = datetime.now() + timedelta(minutes=minutes)

        embed = discord.Embed(
            title="⏰ Recordatorio establecido",
            description=f"Te recordaré: **{message}**",
            color=0x00ff00
        )
        embed.add_field(name="⏱️ Tiempo", value=f"{minutes} minutos", inline=True)
        embed.add_field(name="🕐 Hora", value=f"<t:{int(reminder_time.timestamp())}:F>", inline=True)

        await ctx.send(embed=embed)

        # Store reminder
        user_id = ctx.author.id
        if user_id not in self.reminders:
            self.reminders[user_id] = []

        self.reminders[user_id].append({
            'message': message,
            'time': reminder_time,
            'channel_id': ctx.channel.id
        })

        # Wait for the reminder time
        await asyncio.sleep(minutes * 60)

        # Send reminder (if still in reminders)
        if user_id in self.reminders and message in [r['message'] for r in self.reminders[user_id]]:
            try:
                channel = self.bot.get_channel(ctx.channel.id)
                if channel:
                    reminder_embed = discord.Embed(
                        title="⏰ Recordatorio",
                        description=f"¡Hola {ctx.author.mention}! Te recuerdo: **{message}**",
                        color=0xffaa00
                    )
                    await channel.send(ctx.author.mention, embed=reminder_embed)

                    # Remove reminder from list
                    self.reminders[user_id] = [r for r in self.reminders[user_id] if r['message'] != message]
            except:
                pass

    @commands.command(name='weather')
    async def weather(self, ctx, *, city):
        """Get weather information for a city"""
        try:
            # Using wttr.in API (text-based weather)
            url = f"http://wttr.in/{city}?format=j1"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                # Extract weather data
                current = data['current_condition'][0]
                location = data['nearest_area'][0]

                temp_c = current['temp_C']
                temp_f = current['temp_F']
                condition = current['weatherDesc'][0]['value']
                humidity = current['humidity']
                wind_speed = current['windspeedKmph']

                embed = discord.Embed(
                    title=f"🌤️ Clima en {location['areaName'][0]}",
                    color=0x87ceeb
                )

                embed.add_field(name="🌡️ Temperatura", value=f"{temp_c}°C / {temp_f}°F", inline=True)
                embed.add_field(name="🌥️ Condición", value=condition, inline=True)
                embed.add_field(name="💧 Humedad", value=f"{humidity}%", inline=True)
                embed.add_field(name="💨 Viento", value=f"{wind_speed} km/h", inline=True)

                # Add weather icon
                weather_icons = {
                    'Sunny': '☀️',
                    'Clear': '🌙',
                    'Partly cloudy': '⛅',
                    'Cloudy': '☁️',
                    'Overcast': '☁️',
                    'Mist': '🌫️',
                    'Patchy rain possible': '🌦️',
                    'Patchy snow possible': '🌨️',
                    'Patchy sleet possible': '🌨️',
                    'Patchy freezing drizzle possible': '🌨️',
                    'Thundery outbreaks possible': '⛈️',
                    'Blowing snow': '🌨️',
                    'Blizzard': '🌨️',
                    'Fog': '🌫️',
                    'Freezing fog': '🌫️',
                    'Patchy light drizzle': '🌦️',
                    'Light drizzle': '🌦️',
                    'Freezing drizzle': '🌨️',
                    'Heavy freezing drizzle': '🌨️',
                    'Patchy light rain': '🌦️',
                    'Light rain': '🌦️',
                    'Moderate rain at times': '🌦️',
                    'Moderate rain': '🌧️',
                    'Heavy rain at times': '🌧️',
                    'Heavy rain': '🌧️',
                    'Light freezing rain': '🌨️',
                    'Moderate or heavy freezing rain': '🌨️',
                    'Light sleet': '🌨️',
                    'Moderate or heavy sleet': '🌨️',
                    'Patchy light snow': '🌨️',
                    'Light snow': '🌨️',
                    'Patchy moderate snow': '🌨️',
                    'Moderate snow': '🌨️',
                    'Patchy heavy snow': '🌨️',
                    'Heavy snow': '🌨️',
                    'Ice pellets': '🧊',
                    'Light rain shower': '🌦️',
                    'Moderate or heavy rain shower': '🌧️',
                    'Torrential rain shower': '🌧️',
                    'Light sleet showers': '🌨️',
                    'Moderate or heavy sleet showers': '🌨️',
                    'Light snow showers': '🌨️',
                    'Moderate or heavy snow showers': '🌨️',
                    'Light showers of ice pellets': '🧊',
                    'Moderate or heavy showers of ice pellets': '🧊',
                    'Patchy light rain with thunder': '⛈️',
                    'Moderate or heavy rain with thunder': '⛈️',
                    'Patchy light snow with thunder': '⛈️',
                    'Moderate or heavy snow with thunder': '⛈️'
                }

                icon = weather_icons.get(condition, '🌤️')
                embed.add_field(name="🌈 Icono", value=icon, inline=True)

                embed.set_footer(text="Datos proporcionados por wttr.in")

            else:
                embed = discord.Embed(
                    title="❌ Error",
                    description="No se pudo obtener la información del clima. Verifica el nombre de la ciudad.",
                    color=0xff0000
                )

            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description="No se pudo obtener la información del clima. Intenta con otro nombre de ciudad.",
                color=0xff0000
            )
            await ctx.send(embed=embed)

    @commands.command(name='calc')
    async def calc(self, ctx, *, expression):
        """Simple calculator"""
        try:
            # Basic security: only allow numbers, operators, and parentheses
            allowed_chars = set('0123456789+-*/(). ')
            if not all(c in allowed_chars for c in expression):
                await ctx.send("❌ Caracteres no permitidos en la expresión.")
                return

            # Evaluate the expression
            result = eval(expression)

            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 4)

            embed = discord.Embed(
                title="🧮 Calculadora",
                color=0x3498db
            )
            embed.add_field(name="📝 Expresión", value=expression, inline=False)
            embed.add_field(name="📊 Resultado", value=str(result), inline=False)

            await ctx.send(embed=embed)

        except ZeroDivisionError:
            await ctx.send("❌ Error: División por cero.")
        except SyntaxError:
            await ctx.send("❌ Error: Expresión matemática inválida.")
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

    @commands.command(name='urban')
    async def urban(self, ctx, *, term):
        """Search Urban Dictionary"""
        try:
            # Urban Dictionary API
            url = f"http://api.urbandictionary.com/v0/define?term={term.replace(' ', '+')}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                if data['list']:
                    definition = data['list'][0]
                    word = definition['word']
                    meaning = definition['definition'][:1000]  # Limit length
                    example = definition['example'][:500]  # Limit length

                    embed = discord.Embed(
                        title=f"📖 Urban Dictionary: {word}",
                        color=0xff69b4
                    )

                    embed.add_field(name="📝 Definición", value=meaning, inline=False)

                    if example:
                        embed.add_field(name="💬 Ejemplo", value=example, inline=False)

                    embed.add_field(name="👍 Thumbs Up", value=definition['thumbs_up'], inline=True)
                    embed.add_field(name="👎 Thumbs Down", value=definition['thumbs_down'], inline=True)

                    embed.set_footer(text="Fuente: Urban Dictionary")
                else:
                    embed = discord.Embed(
                        title="❌ No encontrado",
                        description=f"No se encontró la definición de '{term}' en Urban Dictionary.",
                        color=0xff0000
                    )

                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Error al consultar Urban Dictionary.")

        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description="No se pudo consultar Urban Dictionary en este momento.",
                color=0xff0000
            )
            await ctx.send(embed=embed)

    @commands.command(name='translate')
    async def translate(self, ctx, target_lang, *, text):
        """Translate text to another language"""
        try:
            # Using Google Translate (free tier)
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': 'auto',
                'tl': target_lang,
                'dt': 't',
                'q': text
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                translated_text = data[0][0][0]

                embed = discord.Embed(
                    title="🌐 Traductor",
                    color=0x9b59b6
                )

                embed.add_field(name="📝 Texto original", value=text, inline=False)
                embed.add_field(name="🌍 Idioma destino", value=target_lang.upper(), inline=True)
                embed.add_field(name="📊 Traducción", value=translated_text, inline=False)

                embed.set_footer(text="Fuente: Google Translate")
            else:
                embed = discord.Embed(
                    title="❌ Error",
                    description="No se pudo traducir el texto. Verifica el código de idioma.",
                    color=0xff0000
                )

            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description="No se pudo traducir el texto en este momento.",
                color=0xff0000
            )
            await ctx.send(embed=embed)

    @commands.command(name='covid')
    async def covid(self, ctx, *, country="world"):
        """Get COVID-19 statistics"""
        try:
            url = f"https://disease.sh/v3/covid-19/countries/{country.lower()}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                embed = discord.Embed(
                    title=f"🦠 COVID-19 en {data['country']}",
                    color=0xff0000
                )

                embed.add_field(name="📊 Casos totales", value=f"{data['cases']:,}", inline=True)
                embed.add_field(name="💚 Recuperados", value=f"{data['recovered']:,}", inline=True)
                embed.add_field(name="💔 Muertes", value=f"{data['deaths']:,}", inline=True)
                embed.add_field(name="🏥 Activos", value=f"{data['active']:,}", inline=True)
                embed.add_field(name="🩺 Críticos", value=f"{data['critical']:,}", inline=True)
                embed.add_field(name="🧪 Tests", value=f"{data['tests']:,}", inline=True)

                embed.set_footer(text=f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                embed.timestamp = datetime.now()

            else:
                embed = discord.Embed(
                    title="❌ Error",
                    description="No se pudo obtener información de COVID-19. Verifica el nombre del país.",
                    color=0xff0000
                )

            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description="No se pudo obtener información de COVID-19 en este momento.",
                color=0xff0000
            )
            await ctx.send(embed=embed)

    @commands.command(name='jokeapi')
    async def jokeapi(self, ctx, category="Any"):
        """Get a joke from JokeAPI"""
        try:
            categories = ["Any", "Misc", "Programming", "Dark", "Pun", "Spooky", "Christmas"]
            if category not in categories:
                await ctx.send(f"❌ Categoría inválida. Categorías disponibles: {', '.join(categories)}")
                return

            url = f"https://v2.jokeapi.dev/joke/{category}?type=single"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                joke = data['joke']

                embed = discord.Embed(
                    title="😂 Chiste de JokeAPI",
                    description=joke,
                    color=0xe67e22
                )
                embed.set_footer(text=f"Categoría: {category}")
            else:
                embed = discord.Embed(
                    title="❌ Error",
                    description="No se pudo obtener un chiste de JokeAPI.",
                    color=0xff0000
                )

            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description="No se pudo obtener un chiste en este momento.",
                color=0xff0000
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CommunityCommandsCog(bot))
