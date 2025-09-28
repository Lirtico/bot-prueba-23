import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
import lyricsgenius
import asyncio
import logging
from config.settings import API_KEYS

logger = logging.getLogger(__name__)

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}  # guild_id -> list of tracks
        self.now_playing = {}  # guild_id -> current track
        self.autoplay = {}  # guild_id -> bool
        self.loop = {}  # guild_id -> bool
        self.volume = {}  # guild_id -> float (0.0 to 1.0)

        # Setup APIs
        self.spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=API_KEYS['spotify_client_id'],
            client_secret=API_KEYS['spotify_client_secret']
        ))
        self.youtube = build('youtube', 'v3', developerKey=API_KEYS['youtube_api_key'])
        try:
            token = API_KEYS.get('genius_access_token', '')
            if token and token != 'your_genius_token_here':
                self.genius = lyricsgenius.Genius(token)
            else:
                self.genius = None
                logger.warning("Genius token not configured. Lyrics feature disabled.")
        except Exception as e:
            logger.error(f"Failed to initialize Genius: {e}")
            self.genius = None

        # yt-dlp options
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
        }

    def get_queue(self, guild_id):
        if guild_id not in self.queues:
            self.queues[guild_id] = []
        return self.queues[guild_id]

    def get_autoplay(self, guild_id):
        return self.autoplay.get(guild_id, False)

    def set_autoplay(self, guild_id, value):
        self.autoplay[guild_id] = value

    def get_loop(self, guild_id):
        return self.loop.get(guild_id, False)

    def set_loop(self, guild_id, value):
        self.loop[guild_id] = value

    def get_volume(self, guild_id):
        return self.volume.get(guild_id, 0.5)

    def set_volume(self, guild_id, value):
        self.volume[guild_id] = max(0.0, min(1.0, value))

    async def search_youtube(self, query):
        try:
            request = self.youtube.search().list(
                part='snippet',
                q=query,
                type='video',
                maxResults=1,
                order='relevance'
            )
            response = request.execute()
            if response['items']:
                item = response['items'][0]
                video_id = item['id']['videoId']
                return {
                    'title': item['snippet']['title'],
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'duration': 0,  # API doesn't provide duration in search; can add separate call if needed
                    'thumbnail': item['snippet']['thumbnails']['default']['url'],
                    'uploader': item['snippet']['channelTitle']
                }
        except Exception as e:
            logger.error(f"YouTube API search error: {e}")
        return None

    async def search_spotify(self, query):
        try:
            results = self.spotify.search(q=query, type='track', limit=1)
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                title = f"{track['name']} - {', '.join([a['name'] for a in track['artists']])}"
                # Search YouTube for the title
                youtube_track = await self.search_youtube(title)
                if youtube_track:
                    return youtube_track
        except Exception as e:
            logger.error(f"Spotify search error: {e}")
        return None

    async def get_lyrics(self, song_title):
        if self.genius is None:
            return "Lyrics unavailable - Genius API not configured. Get a free token from https://genius.com/developers and add to config/settings.py"
        try:
            song = self.genius.search_song(song_title)
            if song:
                return song.lyrics
        except Exception as e:
            logger.error(f"Lyrics error: {e}")
        return "Lyrics not found."

    async def get_related(self, video_id):
        try:
            request = self.youtube.search().list(
                part='snippet',
                relatedToVideoId=video_id,
                type='video',
                maxResults=5
            )
            response = request.execute()
            return [item['snippet']['title'] for item in response['items']]
        except Exception as e:
            logger.error(f"Related videos error: {e}")
        return []

    async def play_next(self, ctx):
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        if not queue:
            if self.get_autoplay(guild_id):
                # Auto-queue logic (simplified: search for similar)
                current = self.now_playing.get(guild_id)
                if current:
                    related = await self.get_related(current['url'].split('v=')[1] if 'v=' in current['url'] else '')
                    if related:
                        next_track = await self.search_youtube(related[0])
                        if next_track:
                            queue.append(next_track)
            if not queue:
                return

        track = queue.pop(0)
        self.now_playing[guild_id] = track

        vc = ctx.voice_client
        if vc and vc.is_connected():
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(track['url'], download=False)
                url = info['url']
                vc.play(discord.FFmpegPCMAudio(url, **{'options': '-vn'}), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
                vc.source.volume = self.get_volume(guild_id)

    # Prefix commands
    @commands.command(name='play')
    async def play_prefix(self, ctx, *, query):
        await self.play(ctx, query)

    @commands.command(name='pause')
    async def pause_prefix(self, ctx):
        await self.pause(ctx)

    @commands.command(name='stop')
    async def stop_prefix(self, ctx):
        await self.stop(ctx)

    @commands.command(name='autoplay')
    async def autoplay_prefix(self, ctx):
        await self.autoplay_cmd(ctx)

    @commands.command(name='disconnect')
    async def disconnect_prefix(self, ctx):
        await self.disconnect(ctx)

    @commands.command(name='lyrics')
    async def lyrics_prefix(self, ctx, *, song):
        await self.lyrics_cmd(ctx, song)

    @commands.command(name='related')
    async def related_prefix(self, ctx, *, song):
        await self.related_cmd(ctx, song)

    @commands.command(name='queue')
    async def queue_prefix(self, ctx):
        await self.queue_cmd(ctx)

    @commands.command(name='skip')
    async def skip_prefix(self, ctx):
        await self.skip(ctx)

    @commands.command(name='volume')
    async def volume_prefix(self, ctx, vol: float = None):
        await self.volume_cmd(ctx, vol)

    @commands.command(name='join')
    async def join_prefix(self, ctx):
        await self.join(ctx)

    @commands.command(name='leave')
    async def leave_prefix(self, ctx):
        await self.disconnect(ctx)

    @commands.command(name='nowplaying')
    async def nowplaying_prefix(self, ctx):
        await self.nowplaying_cmd(ctx)

    @commands.command(name='shuffle')
    async def shuffle_prefix(self, ctx):
        await self.shuffle(ctx)

    @commands.command(name='loop')
    async def loop_prefix(self, ctx):
        await self.loop_cmd(ctx)

    @commands.command(name='resume')
    async def resume_prefix(self, ctx):
        await self.resume(ctx)

    @commands.command(name='seek')
    async def seek_prefix(self, ctx, time: str):
        await self.seek(ctx, time)

    @commands.command(name='rewind')
    async def rewind_prefix(self, ctx, time: str):
        await self.rewind(ctx, time)

    @commands.command(name='previous')
    async def previous_prefix(self, ctx):
        await self.previous(ctx)

    @commands.command(name='grab')
    async def grab_prefix(self, ctx):
        await self.grab(ctx)

    @commands.command(name='removedupes')
    async def removedupes_prefix(self, ctx):
        await self.removedupes(ctx)

    @commands.command(name='top-songs')
    async def top_songs_prefix(self, ctx):
        await self.top_songs(ctx)

    @commands.command(name='search')
    async def search_prefix(self, ctx, *, query):
        await self.search(ctx, query)

    @commands.command(name='play-file')
    async def play_file_prefix(self, ctx, url):
        await self.play_file(ctx, url)

    @commands.command(name='tts')
    async def tts_prefix(self, ctx, *, text):
        await self.tts(ctx, text)

    @commands.command(name='music-panel')
    async def music_panel_prefix(self, ctx):
        await self.music_panel(ctx)

    @commands.command(name='fastforward')
    async def fastforward_prefix(self, ctx, time: str):
        await self.fastforward(ctx, time)

    @commands.command(name='jump')
    async def jump_prefix(self, ctx, position: int):
        await self.jump(ctx, position)

    @commands.command(name='leavecleanup')
    async def leavecleanup_prefix(self, ctx):
        await self.leavecleanup(ctx)

    @commands.command(name='debug')
    async def debug_prefix(self, ctx):
        await self.debug(ctx)

    # Slash commands
    @app_commands.command(name='play', description='Reproduce una canción')
    async def play_slash(self, interaction: discord.Interaction, song: str):
        ctx = await commands.Context.from_interaction(interaction)
        await self.play(ctx, song)

    @app_commands.command(name='pause', description='Pausa o reanuda la reproducción')
    async def pause_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.pause(ctx)

    @app_commands.command(name='stop', description='Detiene la reproducción y limpia la cola')
    async def stop_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.stop(ctx)

    @app_commands.command(name='autoplay', description='Activa o desactiva la reproducción automática')
    async def autoplay_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.autoplay_cmd(ctx)

    @app_commands.command(name='disconnect', description='Desconecta el bot del canal de voz')
    async def disconnect_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.disconnect(ctx)

    @app_commands.command(name='lyrics', description='Muestra la letra de una canción')
    async def lyrics_slash(self, interaction: discord.Interaction, song: str):
        ctx = await commands.Context.from_interaction(interaction)
        await self.lyrics_cmd(ctx, song)

    @app_commands.command(name='related', description='Muestra videos relacionados')
    async def related_slash(self, interaction: discord.Interaction, song: str):
        ctx = await commands.Context.from_interaction(interaction)
        await self.related_cmd(ctx, song)

    @app_commands.command(name='queue', description='Muestra la cola de reproducción')
    async def queue_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.queue_cmd(ctx)

    @app_commands.command(name='skip', description='Salta a la siguiente canción')
    async def skip_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.skip(ctx)

    @app_commands.command(name='volume', description='Ajusta el volumen (0.0-1.0)')
    async def volume_slash(self, interaction: discord.Interaction, vol: float = None):
        ctx = await commands.Context.from_interaction(interaction)
        await self.volume_cmd(ctx, vol)

    @app_commands.command(name='join', description='Une el bot al canal de voz')
    async def join_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.join(ctx)

    @app_commands.command(name='nowplaying', description='Muestra la canción actual')
    async def nowplaying_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.nowplaying_cmd(ctx)

    @app_commands.command(name='shuffle', description='Mezcla la cola')
    async def shuffle_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.shuffle(ctx)

    @app_commands.command(name='loop', description='Activa o desactiva el bucle')
    async def loop_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.loop_cmd(ctx)

    @app_commands.command(name='resume', description='Reanuda la reproducción')
    async def resume_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.resume(ctx)

    @app_commands.command(name='seek', description='Salta a un tiempo específico')
    async def seek_slash(self, interaction: discord.Interaction, time: str):
        ctx = await commands.Context.from_interaction(interaction)
        await self.seek(ctx, time)

    @app_commands.command(name='rewind', description='Retrocede en la canción')
    async def rewind_slash(self, interaction: discord.Interaction, time: str):
        ctx = await commands.Context.from_interaction(interaction)
        await self.rewind(ctx, time)

    @app_commands.command(name='previous', description='Reproduce la canción anterior')
    async def previous_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.previous(ctx)

    @app_commands.command(name='grab', description='Guarda la canción actual')
    async def grab_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.grab(ctx)

    @app_commands.command(name='removedupes', description='Elimina duplicados de la cola')
    async def removedupes_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.removedupes(ctx)

    @app_commands.command(name='top-songs', description='Muestra las canciones más populares')
    async def top_songs_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.top_songs(ctx)

    @app_commands.command(name='search', description='Busca canciones')
    async def search_slash(self, interaction: discord.Interaction, query: str):
        ctx = await commands.Context.from_interaction(interaction)
        await self.search(ctx, query)

    @app_commands.command(name='play-file', description='Reproduce desde URL')
    async def play_file_slash(self, interaction: discord.Interaction, url: str):
        ctx = await commands.Context.from_interaction(interaction)
        await self.play_file(ctx, url)

    @app_commands.command(name='tts', description='Texto a voz')
    async def tts_slash(self, interaction: discord.Interaction, text: str):
        ctx = await commands.Context.from_interaction(interaction)
        await self.tts(ctx, text)

    @app_commands.command(name='music-panel', description='Panel de control de música')
    async def music_panel_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.music_panel(ctx)

    @app_commands.command(name='fastforward', description='Avanza en la canción')
    async def fastforward_slash(self, interaction: discord.Interaction, time: str):
        ctx = await commands.Context.from_interaction(interaction)
        await self.fastforward(ctx, time)

    @app_commands.command(name='jump', description='Salta a una posición en la cola')
    async def jump_slash(self, interaction: discord.Interaction, position: int):
        ctx = await commands.Context.from_interaction(interaction)
        await self.jump(ctx, position)

    @app_commands.command(name='leavecleanup', description='Limpia al salir')
    async def leavecleanup_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.leavecleanup(ctx)

    @app_commands.command(name='debug', description='Información de debug')
    async def debug_slash(self, interaction: discord.Interaction):
        ctx = await commands.Context.from_interaction(interaction)
        await self.debug(ctx)

    # Implementations
    async def play(self, ctx, query):
        if not ctx.author.voice:
            await ctx.send("Debes estar en un canal de voz!")
            return

        vc = await ctx.author.voice.channel.connect() if not ctx.voice_client else ctx.voice_client

        track = await self.search_spotify(query) or await self.search_youtube(query)
        if not track:
            await ctx.send("No se encontró la canción.")
            return

        queue = self.get_queue(ctx.guild.id)
        queue.append(track)
        await ctx.send(f"Agregado a la cola: {track['title']}")

        if not vc.is_playing():
            await self.play_next(ctx)

    async def pause(self, ctx):
        vc = ctx.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await ctx.send("Pausado.")
        elif vc and vc.is_paused():
            vc.resume()
            await ctx.send("Reanudado.")
        else:
            await ctx.send("No hay nada reproduciendo.")

    async def stop(self, ctx):
        vc = ctx.voice_client
        if vc:
            vc.stop()
            self.queues[ctx.guild.id] = []
            self.now_playing[ctx.guild.id] = None
            await ctx.send("Detenido y cola limpiada.")
        else:
            await ctx.send("No estoy en un canal de voz.")

    async def autoplay_cmd(self, ctx):
        current = self.get_autoplay(ctx.guild.id)
        self.set_autoplay(ctx.guild.id, not current)
        await ctx.send(f"Autoplay {'activado' if not current else 'desactivado'}.")

    async def disconnect(self, ctx):
        vc = ctx.voice_client
        if vc:
            await vc.disconnect()
            self.queues[ctx.guild.id] = []
            self.now_playing[ctx.guild.id] = None
            await ctx.send("Desconectado.")
        else:
            await ctx.send("No estoy conectado.")

    async def lyrics_cmd(self, ctx, song):
        lyrics = await self.get_lyrics(song)
        if len(lyrics) > 2000:
            lyrics = lyrics[:1997] + "..."
        await ctx.send(f"**Letra de {song}:**\n{lyrics}")

    async def related_cmd(self, ctx, song):
        track = await self.search_youtube(song)
        if track:
            video_id = track['url'].split('v=')[1].split('&')[0]
            related = await self.get_related(video_id)
            if related:
                await ctx.send(f"**Videos relacionados a {song}:**\n" + "\n".join(f"- {r}" for r in related[:5]))
            else:
                await ctx.send("No se encontraron videos relacionados.")
        else:
            await ctx.send("Canción no encontrada.")

    async def queue_cmd(self, ctx):
        queue = self.get_queue(ctx.guild.id)
        if not queue:
            await ctx.send("La cola está vacía.")
            return
        embed = discord.Embed(title="Cola de reproducción", color=0x1db954)
        for i, track in enumerate(queue[:10]):
            embed.add_field(name=f"{i+1}. {track['title']}", value=f"Duración: {track['duration']}s", inline=False)
        if len(queue) > 10:
            embed.set_footer(text=f"Y {len(queue)-10} más...")
        await ctx.send(embed=embed)

    async def skip(self, ctx):
        vc = ctx.voice_client
        if vc and vc.is_playing():
            vc.stop()
            await ctx.send("Saltado.")
        else:
            await ctx.send("No hay nada reproduciendo.")

    async def volume_cmd(self, ctx, vol):
        if vol is None:
            current = self.get_volume(ctx.guild.id)
            await ctx.send(f"Volumen actual: {current}")
        else:
            self.set_volume(ctx.guild.id, vol)
            if ctx.voice_client and ctx.voice_client.source:
                ctx.voice_client.source.volume = vol
            await ctx.send(f"Volumen ajustado a {vol}.")

    async def join(self, ctx):
        if not ctx.author.voice:
            await ctx.send("Debes estar en un canal de voz!")
            return
        await ctx.author.voice.channel.connect()
        await ctx.send("Conectado.")

    async def nowplaying_cmd(self, ctx):
        current = self.now_playing.get(ctx.guild.id)
        if current:
            embed = discord.Embed(title="Reproduciendo ahora", description=current['title'], color=0x1db954)
            embed.set_thumbnail(url=current['thumbnail'])
            embed.add_field(name="Duración", value=f"{current['duration']}s")
            embed.add_field(name="Subido por", value=current['uploader'])
            await ctx.send(embed=embed)
        else:
            await ctx.send("No hay nada reproduciendo.")

    async def shuffle(self, ctx):
        import random
        queue = self.get_queue(ctx.guild.id)
        random.shuffle(queue)
        await ctx.send("Cola mezclada.")

    async def loop_cmd(self, ctx):
        current = self.get_loop(ctx.guild.id)
        self.set_loop(ctx.guild.id, not current)
        await ctx.send(f"Bucle {'activado' if not current else 'desactivado'}.")

    async def resume(self, ctx):
        vc = ctx.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await ctx.send("Reanudado.")
        else:
            await ctx.send("No está pausado.")

    async def seek(self, ctx, time):
        await ctx.send("Seek no implementado aún.")

    async def rewind(self, ctx, time):
        await ctx.send("Rewind no implementado aún.")

    async def previous(self, ctx):
        await ctx.send("Previous no implementado aún.")

    async def grab(self, ctx):
        current = self.now_playing.get(ctx.guild.id)
        if current:
            await ctx.author.send(f"Guardado: {current['title']} - {current['url']}")
            await ctx.send("Canción guardada en DM.")
        else:
            await ctx.send("No hay canción reproduciendo.")

    async def removedupes(self, ctx):
        queue = self.get_queue(ctx.guild.id)
        seen = set()
        new_queue = []
        for track in queue:
            if track['url'] not in seen:
                seen.add(track['url'])
                new_queue.append(track)
        self.queues[ctx.guild.id] = new_queue
        await ctx.send("Duplicados eliminados.")

    async def top_songs(self, ctx):
        await ctx.send("Top songs no implementado aún.")

    async def search(self, ctx, query):
        track = await self.search_youtube(query)
        if track:
            await ctx.send(f"Encontrado: {track['title']} - {track['url']}")
        else:
            await ctx.send("No encontrado.")

    async def play_file(self, ctx, url):
        await ctx.send("Play file no implementado aún.")

    async def tts(self, ctx, text):
        await ctx.send("TTS no implementado aún.")

    async def music_panel(self, ctx):
        embed = discord.Embed(title="Panel de Música", color=0x1db954)
        embed.add_field(name="Comandos", value="Usa !help music o /help para ver comandos.")
        await ctx.send(embed=embed)

    async def fastforward(self, ctx, time):
        await ctx.send("Fastforward no implementado aún.")

    async def jump(self, ctx, position):
        queue = self.get_queue(ctx.guild.id)
        if 0 < position <= len(queue):
            track = queue.pop(position-1)
            queue.insert(0, track)
            await ctx.send(f"Saltado a posición {position}.")
        else:
            await ctx.send("Posición inválida.")

    async def leavecleanup(self, ctx):
        await ctx.send("Leave cleanup no implementado aún.")

    async def debug(self, ctx):
        info = f"Queue: {len(self.get_queue(ctx.guild.id))}, Autoplay: {self.get_autoplay(ctx.guild.id)}, Loop: {self.get_loop(ctx.guild.id)}"
        await ctx.send(f"Debug: {info}")

async def setup(bot):
    await bot.add_cog(MusicCog(bot))
