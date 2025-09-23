import discord
from discord.ext import commands
import os
import random
import asyncio
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Bot events
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print(f'Bot ID: {bot.user.id}')
    print(f'Connected to {len(bot.guilds)} servers')
    print('------')

@bot.event
async def on_command(ctx):
    """Log when commands are executed"""
    print(f'Command executed: {ctx.command.name} by {ctx.author.name}#{ctx.author.discriminator}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing required arguments. Use `!help` for command usage.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `!help` for available commands.")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")
        print(f"Error: {error}")

# Utility Commands
@bot.command(name='ping')
async def ping(ctx):
    """Check bot latency"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency: {latency}ms",
        color=0x00ff00
    )
    await ctx.send(embed=embed)

# Store last help command execution time per user
last_help_execution = {}

@bot.command(name='help')
async def help_command(ctx):
    """Show available commands"""
    user_id = ctx.author.id
    current_time = datetime.now()

    # Check if user recently executed help command (5 second cooldown)
    if user_id in last_help_execution:
        time_diff = (current_time - last_help_execution[user_id]).total_seconds()
        if time_diff < 5:
            print(f"[DEBUG] Help command blocked - too recent for user {ctx.author.name}")
            return

    # Update last execution time
    last_help_execution[user_id] = current_time

    print(f"[DEBUG] Help command executed by {ctx.author.name} at {current_time}")

    try:
        # Create embed with all command information
        embed = discord.Embed(
            title="🤖 Bot Commands",
            description="Here are all available commands:",
            color=0x0099ff
        )

        # Moderation commands
        embed.add_field(
            name="🛠️ Moderation",
            value="`!purge <amount>` - Delete messages\n"
                  "`!kick <user> [reason]` - Kick a user\n"
                  "`!ban <user> [reason]` - Ban a user\n"
                  "`!unban <user_id>` - Unban a user",
            inline=False
        )

        # User commands
        embed.add_field(
            name="👤 User Commands",
            value="`!avatar [@user]` - Get user avatar\n"
                  "`!userinfo [@user]` - Get user information\n"
                  "`!banner [@user]` - Get user banner\n"
                  "`!serverinfo` - Get server information",
            inline=False
        )

        # Fun commands
        embed.add_field(
            name="🎲 Fun Commands",
            value="`!roll <dice>` - Roll dice (e.g., 1d20)\n"
                  "`!coinflip` - Flip a coin",
            inline=False
        )

        # Utility commands
        embed.add_field(
            name="🔧 Utility",
            value="`!say <message>` - Make bot say something\n"
                  "`!ping` - Check bot latency\n"
                  "`!help` - Show this message\n"
                  "`!commands` - Show all commands in a list",
            inline=False
        )

        # Additional moderation commands
        embed.add_field(
            name="⚠️ Moderation+",
            value="`!warn <user> [reason]` - Warn a user\n"
                  "`!poll <question>` - Create a poll\n"
                  "`!remind <minutes> <message>` - Set a reminder",
            inline=False
        )

        # Community commands
        embed.add_field(
            name="🎯 Community",
            value="`!weather <city>` - Get weather info\n"
                  "`!joke` - Get a random joke\n"
                  "`!fact` - Get a random fact\n"
                  "`!meme` - Get a programmer meme",
            inline=False
        )

        # Information commands
        embed.add_field(
            name="📊 Information",
            value="`!roleinfo <role>` - Get role information\n"
                  "`!channelinfo [channel]` - Get channel info\n"
                  "`!serverstats` - Detailed server statistics\n"
                  "`!calc <expression>` - Simple calculator",
            inline=False
        )

        embed.set_footer(text="Use ! before each command")

        print(f"[DEBUG] About to send help embed at {datetime.now()}")
        # Send the embed once and store the message
        message = await ctx.send(embed=embed)
        print(f"[DEBUG] Help embed sent successfully at {datetime.now()}, message ID: {message.id}")

        # Add reactions to the message for better interaction
        await message.add_reaction("✅")

    except Exception as e:
        print(f"[ERROR] Failed to send help embed: {e}")
        await ctx.send("❌ Sorry, there was an error displaying the help message.")

@bot.command(name='commands')
async def commands_list(ctx):
    """Show all available commands in a simple list"""
    commands_list = [
        "🛠️ **Moderation:**",
        "• `!purge <amount>` - Delete messages",
        "• `!kick <user> [reason]` - Kick a user",
        "• `!ban <user> [reason]` - Ban a user",
        "• `!unban <user_id>` - Unban a user",
        "• `!warn <user> [reason]` - Warn a user",
        "",
        "👤 **User Commands:**",
        "• `!avatar [@user]` - Get user avatar",
        "• `!userinfo [@user]` - Get user information",
        "• `!banner [@user]` - Get user banner",
        "• `!serverinfo` - Get server information",
        "• `!roleinfo <role>` - Get role information",
        "• `!channelinfo [channel]` - Get channel info",
        "",
        "🎲 **Fun Commands:**",
        "• `!roll <dice>` - Roll dice (e.g., 1d20)",
        "• `!coinflip` - Flip a coin",
        "• `!joke` - Get a random joke",
        "• `!fact` - Get a random fact",
        "• `!meme` - Get a programmer meme",
        "",
        "🔧 **Utility:**",
        "• `!say <message>` - Make bot say something",
        "• `!ping` - Check bot latency",
        "• `!help` - Show detailed help with categories",
        "• `!commands` - Show this simple list",
        "",
        "⚠️ **Community:**",
        "• `!poll <question>` - Create a poll",
        "• `!remind <minutes> <message>` - Set a reminder",
        "• `!weather <city>` - Get weather info",
        "• `!calc <expression>` - Simple calculator",
        "• `!urban <term>` - Search Urban Dictionary",
        "• `!serverstats` - Detailed server statistics"
    ]

    embed = discord.Embed(
        title="📋 All Bot Commands",
        description="\n".join(commands_list),
        color=0x00ff00
    )

    embed.set_footer(text="Total Commands: 30+ | Use ! before each command")
    await ctx.send(embed=embed)

# Moderation Commands
@bot.command(name='purge')
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    """Delete a specified number of messages"""
    if amount > 100:
        await ctx.send("❌ You can only delete up to 100 messages at once.")
        return

    if amount < 1:
        await ctx.send("❌ Please specify a positive number.")
        return

    deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
    confirmation = await ctx.send(f"✅ Deleted {len(deleted) - 1} messages.")
    await asyncio.sleep(3)
    await confirmation.delete()

@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kick a user from the server"""
    if member == ctx.author:
        await ctx.send("❌ You can't kick yourself!")
        return

    if ctx.author.top_role <= member.top_role:
        await ctx.send("❌ You can't kick someone with a higher or equal role!")
        return

    try:
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="👢 User Kicked",
            description=f"{member.mention} has been kicked.",
            color=0xff9900
        )
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to kick this user.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ Failed to kick user: {e}")

@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """Ban a user from the server"""
    if member == ctx.author:
        await ctx.send("❌ You can't ban yourself!")
        return

    if ctx.author.top_role <= member.top_role:
        await ctx.send("❌ You can't ban someone with a higher or equal role!")
        return

    try:
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="🔨 User Banned",
            description=f"{member.mention} has been banned.",
            color=0xff0000
        )
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to ban this user.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ Failed to ban user: {e}")

@bot.command(name='unban')
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    """Unban a user from the server"""
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        embed = discord.Embed(
            title="✅ User Unbanned",
            description=f"{user.mention} has been unbanned.",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    except discord.NotFound:
        await ctx.send("❌ User not found or not banned.")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to unban users.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ Failed to unban user: {e}")

# User Commands
@bot.command(name='avatar')
async def avatar(ctx, member: discord.Member = None):
    """Get a user's avatar"""
    if member is None:
        member = ctx.author

    embed = discord.Embed(
        title=f"{member.display_name}'s Avatar",
        color=0x0099ff
    )
    embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="User", value=member.mention, inline=True)
    embed.add_field(name="User ID", value=member.id, inline=True)
    await ctx.send(embed=embed)

@bot.command(name='userinfo')
async def userinfo(ctx, member: discord.Member = None):
    """Get information about a user"""
    if member is None:
        member = ctx.author

    # Calculate relative time for created and joined dates
    def get_relative_time(date):
        now = datetime.now(date.tzinfo)
        diff = now - date

        years = diff.days // 365
        months = diff.days // 30
        days = diff.days
        hours = diff.seconds // 3600

        if years > 0:
            return f"{years} year(s) ago"
        elif months > 0:
            return f"{months} month(s) ago"
        elif days > 0:
            return f"{days} day(s) ago"
        else:
            return f"{hours} hour(s) ago"

    embed = discord.Embed(color=0x2f3136)  # Dark gray color like Discord

    # Set user avatar as the main image (left side)
    embed.set_author(
        name=f"{member.name} #{member.discriminator}",
        icon_url=member.avatar.url if member.avatar else member.default_avatar.url
    )

    # Add Discord icon/branding (using a Discord emoji or similar)
    embed.add_field(
        name="\u200B",
        value=f"**{member.mention}**",
        inline=False
    )

    # Add activity/status information if available
    if member.activity:
        activity_text = f"Playing **{member.activity.name}**"
        if hasattr(member.activity, 'details') and member.activity.details:
            activity_text += f"\n*{member.activity.details}*"
        embed.add_field(name="\u200B", value=activity_text, inline=False)

    # Add created and joined dates with relative time
    created_relative = get_relative_time(member.created_at)
    joined_relative = get_relative_time(member.joined_at)

    embed.add_field(
        name="📅 Created",
        value=f"{created_relative}\n*{member.created_at.strftime('%m/%d/%Y, %I:%M %p')}*",
        inline=True
    )

    embed.add_field(
        name="📅 Joined",
        value=f"{joined_relative}\n*{member.joined_at.strftime('%m/%d/%Y, %I:%M %p')}*",
        inline=True
    )

    # Add empty field for spacing
    embed.add_field(name="\u200B", value="\u200B", inline=True)

    # Add user information
    embed.add_field(
        name="👤 User Information",
        value=f"**Display Name:** {member.display_name}\n"
              f"**User ID:** {member.id}\n"
              f"**Bot:** {'Yes' if member.bot else 'No'}\n"
              f"**Status:** {str(member.status).title()}",
        inline=False
    )

    # Add role information if they have roles
    if len(member.roles) > 1:  # More than just @everyone
        roles = [role.mention for role in member.roles[1:]]  # Skip @everyone
        embed.add_field(
            name="🏆 Roles",
            value=", ".join(roles[:5]) + ("..." if len(roles) > 5 else ""),
            inline=False
        )

    # Add footer with links
    embed.set_footer(text="Created • Joined • Links • Avatar")

    await ctx.send(embed=embed)

@bot.command(name='banner')
async def banner(ctx, member: discord.Member = None):
    """Get a user's banner"""
    if member is None:
        member = ctx.author

    embed = discord.Embed(
        title=f"{member.display_name}'s Banner",
        color=0x0099ff
    )

    # Set user avatar as thumbnail
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

    try:
        # Use Discord API to get user data including banner
        headers = {"Authorization": f"Bot {TOKEN}"}
        response = requests.get(f"https://discord.com/api/v10/users/{member.id}", headers=headers)

        if response.status_code == 200:
            user_data = response.json()

            # Check if user has a banner
            if user_data.get('banner'):
                banner_hash = user_data['banner']
                # Try GIF first (animated banner), then PNG (static banner)
                banner_gif_url = f"https://cdn.discordapp.com/banners/{member.id}/{banner_hash}.gif?size=1024"
                banner_png_url = f"https://cdn.discordapp.com/banners/{member.id}/{banner_hash}.png?size=1024"

                # Try to use the banner (Discord will redirect to the correct format)
                embed.set_image(url=banner_gif_url)
                embed.add_field(name="User", value=member.mention, inline=True)
                embed.add_field(name="User ID", value=member.id, inline=True)
                embed.add_field(name="Status", value="✅ Has Banner", inline=True)
            else:
                embed.set_image(url="https://i.imgur.com/3YcB3iV.png")  # Default banner image
                embed.add_field(name="User", value=member.mention, inline=True)
                embed.add_field(name="User ID", value=member.id, inline=True)
                embed.add_field(name="Status", value="❌ No Banner", inline=True)
        else:
            # If API call fails, show default image
            embed.set_image(url="https://i.imgur.com/3YcB3iV.png")  # Default banner image
            embed.add_field(name="User", value=member.mention, inline=True)
            embed.add_field(name="User ID", value=member.id, inline=True)
            embed.add_field(name="Status", value="❌ API Error", inline=True)

    except Exception as e:
        # If all methods fail, show default image
        embed.set_image(url="https://i.imgur.com/3YcB3iV.png")  # Default banner image
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Status", value="❌ Error Loading", inline=True)
        print(f"Error loading banner: {e}")

    embed.set_footer(text="Use !banner @user to see someone else's banner")
    await ctx.send(embed=embed)

@bot.command(name='serverinfo')
async def serverinfo(ctx):
    """Get information about the server"""
    guild = ctx.guild

    # Calculate member stats
    total_members = guild.member_count
    bot_count = len([m for m in guild.members if m.bot])
    human_count = total_members - bot_count

    # Calculate channel stats
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)

    embed = discord.Embed(
        title=f"{guild.name}",
        color=0x2f3136  # Dark gray like Discord
    )

    # Set server icon as thumbnail
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    # Description section
    embed.add_field(
        name="📝 Descripción",
        value=guild.description if guild.description else "No tiene descripción",
        inline=False
    )

    # Info General section
    embed.add_field(
        name="📋 Info General",
        value=f"🏷️ **Nombre:** {guild.name}\n"
              f"🆔 **ID:** {guild.id}\n"
              f"📅 **Creación:** {guild.created_at.strftime('%d de %B de %Y')} (hace {((datetime.now().date() - guild.created_at.date()).days // 30)} meses)\n"
              f"👑 **Propietario:** {guild.owner.mention}\n"
              f"🔗 **URL personalizada:** No tiene\n"
              f"🛡️ **MFA Level:** {guild.mfa_level}\n"
              f"🌍 **Región:** Unknown",
        inline=False
    )

    # Statistics section - Users
    embed.add_field(
        name="👥 Usuarios",
        value=f"👤 **Miembros:** {human_count}\n"
              f"🤖 **Bots:** {bot_count}\n"
              f"🎭 **Roles:** {len(guild.roles)}\n"
              f"🚫 **Baneados:** 0",
        inline=True
    )

    # Statistics section - Best of server
    embed.add_field(
        name="⭐ Mejores del servidor",
        value=f"⭐ **Nivel:** 0\n"
              f"😀 **Emojis:** {len(guild.emojis)}\n"
              f"🚀 **Boosts:** {guild.premium_subscription_count}",
        inline=True
    )

    # Statistics section - Channels
    embed.add_field(
        name=f"📺 Canales ({text_channels + voice_channels + categories})",
        value=f"💬 **Texto:** {text_channels}\n"
              f"🔊 **Voz:** {voice_channels}\n"
              f"📰 **Hilos:** 0\n"
              f"📁 **Categorías:** {categories}",
        inline=True
    )

    # Server features
    features = []
    if "COMMUNITY" in guild.features:
        features.append("🏘️ Comunidad")
    if "ANIMATED_ICON" in guild.features:
        features.append("🎨 Icono Animado")
    if "BANNER" in guild.features:
        features.append("🖼️ Banner")

    if features:
        embed.add_field(
            name="✨ Características",
            value="\n".join(features),
            inline=False
        )

    # Footer with server ID
    embed.set_footer(text=f"Fecha de tu ingreso: {ctx.author.joined_at.strftime('%d/%m/%Y %H:%M') if ctx.author.joined_at else 'Unknown'}")

    await ctx.send(embed=embed)

# Fun Commands
@bot.command(name='roll')
async def roll(ctx, dice: str = "1d6"):
    """Roll dice (format: NdM)"""
    try:
        parts = dice.lower().split('d')
        if len(parts) != 2:
            await ctx.send("❌ Invalid format. Use: `!roll NdM` (e.g., 2d20)")
            return

        num_dice = int(parts[0])
        num_sides = int(parts[1])

        if num_dice > 20:
            await ctx.send("❌ You can roll a maximum of 20 dice.")
            return

        if num_sides > 1000:
            await ctx.send("❌ Dice can have a maximum of 1000 sides.")
            return

        if num_dice < 1 or num_sides < 2:
            await ctx.send("❌ Invalid dice configuration.")
            return

        results = [random.randint(1, num_sides) for _ in range(num_dice)]
        total = sum(results)

        embed = discord.Embed(
            title="🎲 Dice Roll",
            description=f"Rolling {dice}",
            color=0xff9900
        )

        if len(results) <= 10:
            embed.add_field(name="Results", value=", ".join(map(str, results)), inline=False)
        else:
            embed.add_field(name="Results", value=f"Too many to show individually", inline=False)

        embed.add_field(name="Total", value=str(total), inline=True)
        embed.add_field(name="Average", value=f"{total/num_dice:.1f}", inline=True)

        await ctx.send(embed=embed)

    except ValueError:
        await ctx.send("❌ Invalid format. Use: `!roll NdM` (e.g., 2d20)")

@bot.command(name='coinflip')
async def coinflip(ctx):
    """Flip a coin"""
    result = random.choice(["Heads", "Tails"])

    embed = discord.Embed(
        title="🪙 Coin Flip",
        description=f"Result: **{result}**",
        color=0xffd700
    )

    await ctx.send(embed=embed)

# Utility Commands
@bot.command(name='say')
async def say(ctx, *, message):
    """Make the bot say something"""
    # Delete the original command message
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass  # If we can't delete, just continue

    # Create embed for better formatting
    embed = discord.Embed(
        description=message,
        color=0x0099ff
    )
    embed.set_footer(text=f"Requested by {ctx.author.display_name}")

    await ctx.send(embed=embed)

# Community Bot Commands
@bot.command(name='warn')
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    """Warn a user"""
    embed = discord.Embed(
        title="⚠️ User Warned",
        description=f"{member.mention} has been warned.",
        color=0xffaa00
    )
    if reason:
        embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_footer(text=f"Warned by {ctx.author.display_name}")
    await ctx.send(embed=embed)

@bot.command(name='poll')
async def poll(ctx, *, question):
    """Create a poll"""
    embed = discord.Embed(
        title="📊 Poll",
        description=question,
        color=0x00ff00
    )
    embed.set_footer(text=f"Poll created by {ctx.author.display_name}")

    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")

@bot.command(name='remind')
async def remind(ctx, time: int, *, message):
    """Set a reminder (time in minutes)"""
    if time < 1 or time > 1440:  # Max 24 hours
        await ctx.send("❌ Time must be between 1 minute and 24 hours.")
        return

    embed = discord.Embed(
        title="⏰ Reminder Set",
        description=f"I'll remind you in {time} minutes: {message}",
        color=0x00aaff
    )
    await ctx.send(embed=embed)

    await asyncio.sleep(time * 60)

    embed = discord.Embed(
        title="⏰ Reminder",
        description=message,
        color=0xffaa00
    )
    embed.set_footer(text=f"Reminder for {ctx.author.display_name}")
    await ctx.author.send(embed=embed)

@bot.command(name='weather')
async def weather(ctx, *, city):
    """Get weather information"""
    try:
        # Using a simple weather API (you'd need to replace with a real API key)
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=your_api_key&units=metric")
        data = response.json()

        if data.get("cod") != 200:
            await ctx.send("❌ City not found.")
            return

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]

        embed = discord.Embed(
            title=f"🌤️ Weather in {city}",
            color=0x87ceeb
        )
        embed.add_field(name="Temperature", value=f"{temp}°C", inline=True)
        embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
        embed.add_field(name="Condition", value=description.title(), inline=False)

        await ctx.send(embed=embed)
    except:
        await ctx.send("❌ Weather service temporarily unavailable.")

@bot.command(name='joke')
async def joke(ctx):
    """Get a random joke"""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "What do you call a bear with no teeth? A gummy bear!"
    ]

    embed = discord.Embed(
        title="😂 Random Joke",
        description=random.choice(jokes),
        color=0xff69b4
    )
    await ctx.send(embed=embed)

@bot.command(name='fact')
async def fact(ctx):
    """Get a random fact"""
    facts = [
        "A group of flamingos is called a 'flamboyance'.",
        "The shortest war in history lasted only 38-45 minutes.",
        "Octopuses have three hearts and blue blood.",
        "A day on Venus is longer than its year.",
        "There are more possible games of chess than atoms in the observable universe."
    ]

    embed = discord.Embed(
        title="🧠 Random Fact",
        description=random.choice(facts),
        color=0x9932cc
    )
    await ctx.send(embed=embed)

@bot.command(name='calc')
async def calc(ctx, *, expression):
    """Simple calculator"""
    try:
        # Basic security check
        if any(char in expression for char in ['import', 'exec', 'eval', '__']):
            await ctx.send("❌ Invalid expression.")
            return

        result = eval(expression)
        embed = discord.Embed(
            title="🧮 Calculator",
            description=f"**Expression:** {expression}\n**Result:** {result}",
            color=0x00ff7f
        )
        await ctx.send(embed=embed)
    except:
        await ctx.send("❌ Invalid mathematical expression.")

@bot.command(name='urban')
async def urban(ctx, *, term):
    """Search Urban Dictionary"""
    try:
        # This would need a real Urban Dictionary API
        embed = discord.Embed(
            title=f"📖 Urban Dictionary: {term}",
            description="Urban Dictionary API not configured.\nThis is a demo response.",
            color=0xff4500
        )
        embed.add_field(name="Definition", value="This would show the definition if API was configured.", inline=False)
        await ctx.send(embed=embed)
    except:
        await ctx.send("❌ Urban Dictionary service unavailable.")

@bot.command(name='meme')
async def meme(ctx):
    """Get a random meme"""
    memes = [
        "When you spend 2 hours on a bug that was just a missing semicolon",
        "Me: 'I'll just fix this quickly'\n*5 hours later*\nAlso me: 'It works... somehow'",
        "When you finally understand recursion:\n'I don't think about it too much'",
        "Git commit messages be like:\n'Fixed stuff'\n'Works now'\n'Please work'",
        "When you find a bug in production:\n*Pretends nothing happened*"
    ]

    embed = discord.Embed(
        title="😂 Programmer Meme",
        description=random.choice(memes),
        color=0xff1493
    )
    await ctx.send(embed=embed)

@bot.command(name='roleinfo')
async def roleinfo(ctx, role: discord.Role):
    """Get information about a role"""
    embed = discord.Embed(
        title=f"Role Information - {role.name}",
        color=role.color
    )

    embed.add_field(name="👥 Members", value=len(role.members), inline=True)
    embed.add_field(name="🎨 Color", value=str(role.color), inline=True)
    embed.add_field(name="📅 Created", value=role.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="🔼 Position", value=role.position, inline=True)
    embed.add_field(name="💬 Mentionable", value="Yes" if role.mentionable else "No", inline=True)
    embed.add_field(name="🗂️ Hoisted", value="Yes" if role.hoist else "No", inline=True)

    permissions = []
    if role.permissions.administrator:
        permissions.append("Administrator")
    if role.permissions.manage_guild:
        permissions.append("Manage Server")
    if role.permissions.manage_roles:
        permissions.append("Manage Roles")
    if role.permissions.manage_channels:
        permissions.append("Manage Channels")
    if role.permissions.kick_members:
        permissions.append("Kick Members")
    if role.permissions.ban_members:
        permissions.append("Ban Members")

    if permissions:
        embed.add_field(name="🔑 Key Permissions", value=", ".join(permissions), inline=False)

    await ctx.send(embed=embed)

@bot.command(name='channelinfo')
async def channelinfo(ctx, channel: discord.TextChannel = None):
    """Get information about a channel"""
    if channel is None:
        channel = ctx.channel

    embed = discord.Embed(
        title=f"Channel Information - #{channel.name}",
        color=0x7289da
    )

    embed.add_field(name="📝 Topic", value=channel.topic or "No topic set", inline=False)
    embed.add_field(name="👥 Members", value=len(channel.members), inline=True)
    embed.add_field(name="📅 Created", value=channel.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="🔞 NSFW", value="Yes" if channel.nsfw else "No", inline=True)
    embed.add_field(name="📌 Pinned Messages", value=len(await channel.pins()), inline=True)

    # Channel permissions
    permissions = []
    if channel.permissions_for(ctx.guild.me).read_messages:
        permissions.append("Read Messages")
    if channel.permissions_for(ctx.guild.me).send_messages:
        permissions.append("Send Messages")
    if channel.permissions_for(ctx.guild.me).embed_links:
        permissions.append("Embed Links")

    embed.add_field(name="🤖 Bot Permissions", value=", ".join(permissions), inline=False)

    await ctx.send(embed=embed)

@bot.command(name='serverstats')
async def serverstats(ctx):
    """Get detailed server statistics"""
    guild = ctx.guild

    embed = discord.Embed(
        title=f"📊 Server Statistics - {guild.name}",
        color=0x00ff00
    )

    # Member stats
    total_members = guild.member_count
    bot_count = len([m for m in guild.members if m.bot])
    human_count = total_members - bot_count

    embed.add_field(name="👥 Total Members", value=total_members, inline=True)
    embed.add_field(name="👤 Humans", value=human_count, inline=True)
    embed.add_field(name="🤖 Bots", value=bot_count, inline=True)

    # Activity stats
    online_count = len([m for m in guild.members if str(m.status) == "online"])
    idle_count = len([m for m in guild.members if str(m.status) == "idle"])
    dnd_count = len([m for m in guild.members if str(m.status) == "dnd"])
    offline_count = len([m for m in guild.members if str(m.status) == "offline"])

    embed.add_field(name="🟢 Online", value=online_count, inline=True)
    embed.add_field(name="🟡 Idle", value=idle_count, inline=True)
    embed.add_field(name="🔴 Do Not Disturb", value=dnd_count, inline=True)
    embed.add_field(name="⚫ Offline", value=offline_count, inline=True)

    # Channel stats
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)

    embed.add_field(name="💬 Text Channels", value=text_channels, inline=True)
    embed.add_field(name="🔊 Voice Channels", value=voice_channels, inline=True)
    embed.add_field(name="📁 Categories", value=categories, inline=True)

    # Role stats
    role_count = len(guild.roles)
    embed.add_field(name="🎭 Roles", value=role_count, inline=True)

    # Emoji stats
    emoji_count = len(guild.emojis)
    embed.add_field(name="😀 Emojis", value=emoji_count, inline=True)

    embed.set_footer(text=f"Server ID: {guild.id} | Generated on {datetime.now().strftime('%B %d, %Y %H:%M')}")
    await ctx.send(embed=embed)

# Error handlers for missing permissions
@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need `Manage Messages` permission to use this command.")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need `Kick Members` permission to use this command.")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need `Ban Members` permission to use this command.")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need `Ban Members` permission to use this command.")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ DISCORD_BOT_TOKEN not found in environment variables.")
        print("Please create a .env file with your bot token:")
        print("DISCORD_BOT_TOKEN=your_bot_token_here")
