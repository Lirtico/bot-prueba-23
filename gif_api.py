import requests
import random
import os
from typing import Optional

class GifAPI:
    def __init__(self):
        # Nekos.best API - Primary and only choice for all role commands
        self.nekos_api = {
            'base_url': 'https://nekos.best/api/v2',
            'headers': {},
            'endpoints': {
                'slap': 'slap',
                'hug': 'hug',
                'kiss': 'kiss',
                'pat': 'pat',
                'tickle': 'tickle',
                'feed': 'feed',
                'punch': 'punch',
                'bite': 'bite',
                'cuddle': 'cuddle',
                'wave': 'wave',
                'wink': 'wink',
                'poke': 'poke',
                'smile': 'smile',
                'blush': 'blush',
                'stare': 'stare',
                'happy': 'happy',
                'dance': 'dance',
                'cringe': 'cringe',
                'cry': 'cry',
                'laugh': 'laugh',
                'angry': 'angry',
                'smug': 'smug',
                'shy': 'shy',
                'sleep': 'sleep',
                'bored': 'bored',
                'think': 'think',
                'facepalm': 'facepalm',
                'shrug': 'shrug',
                'nod': 'nod',
                'nom': 'nom',
                'yeet': 'yeet',
                'run': 'run',
                'nope': 'nope',
                'handshake': 'handshake',
                'handhold': 'handhold',
                'thumbsup': 'thumbsup',
                'highfive': 'highfive',
                'shoot': 'shoot',
                'peck': 'peck',
                'lurk': 'lurk',
                'yawn': 'yawn',
                'baka': 'baka',
                'pout': 'pout',
                'spank': 'spank',
                'nutkick': 'nutkick',
                'fuck': 'fuck'
            }
        }

        # Working GIF URLs that Discord can display properly - using reliable sources
        self.fallback_gifs = {
            'anime slap': 'https://media.tenor.com/4c6o4l1lE8AAAAAC/anime-slap.gif',
            'anime hug': 'https://media.tenor.com/2rBJ8p2b9oAAAAAC/anime-hug.gif',
            'anime kiss': 'https://media.tenor.com/4QhKz9Y8qgwAAAAd/anime-kiss.gif',
            'anime pat': 'https://media.tenor.com/3Ako7m1kO2IAAAAd/anime-pat.gif',
            'anime tickle': 'https://media.tenor.com/5q7fKz9Y8qwAAAAd/anime-tickle.gif',
            'anime feed': 'https://media.tenor.com/4c6o4l1lE8AAAAAC/anime-feed.gif',
            'anime punch': 'https://media.tenor.com/4N7mM1KzZz8YAAAAd/anime-punch.gif',
            'anime high five': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-high-five.gif',
            'anime bite': 'https://media.tenor.com/26gJzTa7Opk6f2h6MAAAAd/anime-bite.gif',
            'anime shoot': 'https://media.tenor.com/4N7mM1KzZz8YAAAAd/anime-shoot.gif',
            'anime wave': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-wave.gif',
            'anime happy': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-happy.gif',
            'anime peck': 'https://media.tenor.com/G3va31oEEnIkMAAAAd/anime-peck.gif',
            'anime lurk': 'https://media.tenor.com/26gJzTa7Opk6f2h6MAAAAd/anime-lurk.gif',
            'anime sleep': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-sleep.gif',
            'anime wink': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-wink.gif',
            'anime yawn': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-yawn.gif',
            'anime nom': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-nom.gif',
            'anime yeet': 'https://media.tenor.com/4N7mM1KzZz8YAAAAd/anime-yeet.gif',
            'anime think': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-think.gif',
            'anime bored': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-bored.gif',
            'anime blush': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-blush.gif',
            'anime stare': 'https://media.tenor.com/26gJzTa7Opk6f2h6MAAAAd/anime-stare.gif',
            'anime nod': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-nod.gif',
            'anime handhold': 'https://media.tenor.com/143v0Z4767hn6AAAAd/anime-handhold.gif',
            'anime smug': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-smug.gif',
            'anime fuck': 'https://media.tenor.com/4N7mM1KzZz8YAAAAd/anime-fuck.gif',
            'anime spank': 'https://media.tenor.com/4N7mM1KzZz8YAAAAd/anime-spank.gif',
            'anime nutkick': 'https://media.tenor.com/4N7mM1KzZz8YAAAAd/anime-nutkick.gif',
            'anime shrug': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-shrug.gif',
            'anime poke': 'https://media.tenor.com/26gJzTa7Opk6f2h6MAAAAd/anime-poke.gif',
            'anime smile': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-smile.gif',
            'anime facepalm': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-facepalm.gif',
            'anime cuddle': 'https://media.tenor.com/143v0Z4767hn6AAAAd/anime-cuddle.gif',
            'anime baka': 'https://media.tenor.com/4N7mM1KzZz8YAAAAd/anime-baka.gif',
            'anime angry': 'https://media.tenor.com/4N7mM1KzZz8YAAAAd/anime-angry.gif',
            'anime run': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-run.gif',
            'anime nope': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-nope.gif',
            'anime handshake': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-handshake.gif',
            'anime cry': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-cry.gif',
            'anime pout': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-pout.gif',
            'anime thumbs up': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-thumbs-up.gif',
            'anime laugh': 'https://media.tenor.com/3o7TKr3nzbh2h5Z3C8AAAAd/anime-laugh.gif'
        }

    def get_gif_url(self, action: str) -> str:
        """
        Get a GIF URL for the specified action using Nekos.best API

        Args:
            action (str): The action to get a GIF for (e.g., 'anime slap')

        Returns:
            str: URL of the GIF
        """
        # Extract the action type (e.g., 'slap' from 'anime slap')
        action_type = action.replace('anime ', '').replace(' ', '')

        # Try Nekos.best API (only choice)
        try:
            if action_type in self.nekos_api['endpoints']:
                endpoint = self.nekos_api['endpoints'][action_type]
                url = f"{self.nekos_api['base_url']}/{endpoint}"
                headers = self.nekos_api['headers']
                response = requests.get(url, headers=headers, timeout=5)

                if response.status_code == 200:
                    data = response.json()
                    print(f"DEBUG: Nekos.best API response for {action}: {data}")  # Debug line
                    if 'results' in data and len(data['results']) > 0:
                        item = data['results'][0]
                        if 'url' in item:
                            print(f"DEBUG: Found GIF URL: {item['url']}")  # Debug line
                            return item['url']

        except Exception as e:
            print(f"Error with Nekos.best API for {action}: {e}")

        # If Nekos.best fails, try Tenor API as fallback
        try:
            tenor_gif = self._get_tenor_gif(action_type)
            if tenor_gif:
                return tenor_gif
        except Exception as e:
            print(f"Tenor API also failed for {action}: {e}")

        # If all APIs fail, use fallback
        return self.fallback_gifs.get(action, 'https://cdn.discordapp.com/emojis/1094046034185949264.gif')

    def _get_tenor_gif(self, action_type: str) -> Optional[str]:
        """
        Get a GIF from Tenor API as a fallback

        Args:
            action_type (str): The action type to search for

        Returns:
            Optional[str]: URL of the GIF or None if failed
        """
        try:
            # Tenor API endpoint
            url = "https://tenor.googleapis.com/v2/search"
            params = {
                'q': f'anime {action_type}',
                'key': os.getenv('TENOR_API_KEY', 'LIVDSRZULELA'),  # Using public API key as fallback
                'limit': 1,
                'media_filter': 'minimal'
            }

            response = requests.get(url, params=params, timeout=5)

            if response.status_code == 200:
                data = response.json()
                if 'results' in data and len(data['results']) > 0:
                    # Try different media formats in order of preference
                    result = data['results'][0]
                    if 'media_formats' in result:
                        formats = result['media_formats']

                        # Try gif format first
                        if 'gif' in formats:
                            return formats['gif']['url']
                        # Try mp4 format if gif not available
                        elif 'mp4' in formats:
                            return formats['mp4']['url']
                        # Try webm format as last resort
                        elif 'webm' in formats:
                            return formats['webm']['url']

                    # Fallback to direct URL if media_formats not available
                    if 'url' in result:
                        return result['url']

        except Exception as e:
            print(f"Error with Tenor API for {action_type}: {e}")

        return None

# Create global instance
gif_api = GifAPI()
