import requests
import random
import os
from typing import Optional

class GifAPI:
    def __init__(self):
        # Multiple API configurations for reliability
        self.apis = {
            'fluxpoint': {
                'base_url': 'https://gallery.fluxpoint.dev/api/v1',
                'headers': {'Authorization': os.getenv('FLUXPOINT_API_KEY', 'your-api-key-here')},
                'endpoints': {
                    'slap': '/sfw/img/anime/slap',
                    'hug': '/sfw/img/anime/hug',
                    'kiss': '/sfw/img/anime/kiss',
                    'pat': '/sfw/img/anime/pat',
                    'tickle': '/sfw/img/anime/tickle',
                    'feed': '/sfw/img/anime/feed',
                    'punch': '/sfw/img/anime/punch',
                    'bite': '/sfw/img/anime/bite',
                    'cuddle': '/sfw/img/anime/cuddle',
                    'wave': '/sfw/img/anime/wave',
                    'wink': '/sfw/img/anime/wink',
                    'poke': '/sfw/img/anime/poke',
                    'smile': '/sfw/img/anime/smile',
                    'blush': '/sfw/img/anime/blush',
                    'stare': '/sfw/img/anime/stare',
                    'happy': '/sfw/img/anime/happy',
                    'dance': '/sfw/img/anime/dance',
                    'cringe': '/sfw/img/anime/cringe',
                    'cry': '/sfw/img/anime/cry',
                    'laugh': '/sfw/img/anime/laugh',
                    'angry': '/sfw/img/anime/angry',
                    'smug': '/sfw/img/anime/smug',
                    'shy': '/sfw/img/anime/shy',
                    'sleep': '/sfw/img/anime/sleep',
                    'bored': '/sfw/img/anime/bored',
                    'think': '/sfw/img/anime/think',
                    'facepalm': '/sfw/img/anime/facepalm',
                    'shrug': '/sfw/img/anime/shrug',
                    'nod': '/sfw/img/anime/nod',
                    'nom': '/sfw/img/anime/nom',
                    'yeet': '/sfw/img/anime/yeet',
                    'run': '/sfw/img/anime/run',
                    'nope': '/sfw/img/anime/nope',
                    'handshake': '/sfw/img/anime/handshake',
                    'handhold': '/sfw/img/anime/handhold',
                    'thumbsup': '/sfw/img/anime/thumbsup',
                    'highfive': '/sfw/img/anime/highfive',
                    'shoot': '/sfw/img/anime/shoot',
                    'peck': '/sfw/img/anime/peck',
                    'lurk': '/sfw/img/anime/lurk',
                    'yawn': '/sfw/img/anime/yawn',
                    'baka': '/sfw/img/anime/baka',
                    'pout': '/sfw/img/anime/pout',
                    'spank': '/nsfw/img/anime/spank',
                    'nutkick': '/nsfw/img/anime/nutkick',
                    'fuck': '/nsfw/img/anime/fuck'
                }
            },
            'waifu': {
                'base_url': 'https://api.waifu.im/search',
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
                    'pout': 'pout'
                }
            }
        }

        # Working GIF URLs that Discord can display properly
        self.fallback_gifs = {
            'anime slap': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime hug': 'https://i.giphy.com/media/143v0Z4767hn6/giphy.gif',
            'anime kiss': 'https://i.giphy.com/media/G3va31oEEnIkM/giphy.gif',
            'anime pat': 'https://i.giphy.com/media/109ltuoSQT212E/giphy.gif',
            'anime tickle': 'https://i.giphy.com/media/26gJzTa7Opk6f2h6M/giphy.gif',
            'anime feed': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime punch': 'https://i.giphy.com/media/4N7mM1KzZz8Y/giphy.gif',
            'anime high five': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime bite': 'https://i.giphy.com/media/26gJzTa7Opk6f2h6M/giphy.gif',
            'anime shoot': 'https://i.giphy.com/media/4N7mM1KzZz8Y/giphy.gif',
            'anime wave': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime happy': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime peck': 'https://i.giphy.com/media/G3va31oEEnIkM/giphy.gif',
            'anime lurk': 'https://i.giphy.com/media/26gJzTa7Opk6f2h6M/giphy.gif',
            'anime sleep': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime wink': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime yawn': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime nom': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime yeet': 'https://i.giphy.com/media/4N7mM1KzZz8Y/giphy.gif',
            'anime think': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime bored': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime blush': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime stare': 'https://i.giphy.com/media/26gJzTa7Opk6f2h6M/giphy.gif',
            'anime nod': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime handhold': 'https://i.giphy.com/media/143v0Z4767hn6/giphy.gif',
            'anime smug': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime fuck': 'https://i.giphy.com/media/4N7mM1KzZz8Y/giphy.gif',
            'anime spank': 'https://i.giphy.com/media/4N7mM1KzZz8Y/giphy.gif',
            'anime nutkick': 'https://i.giphy.com/media/4N7mM1KzZz8Y/giphy.gif',
            'anime shrug': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime poke': 'https://i.giphy.com/media/26gJzTa7Opk6f2h6M/giphy.gif',
            'anime smile': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime facepalm': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime cuddle': 'https://i.giphy.com/media/143v0Z4767hn6/giphy.gif',
            'anime baka': 'https://i.giphy.com/media/4N7mM1KzZz8Y/giphy.gif',
            'anime angry': 'https://i.giphy.com/media/4N7mM1KzZz8Y/giphy.gif',
            'anime run': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime nope': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime handshake': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime cry': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime pout': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime thumbs up': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif',
            'anime laugh': 'https://i.giphy.com/media/3o7TKr3nzbh2h5Z3C8/giphy.gif'
        }

    def get_gif_url(self, action: str) -> str:
        """
        Get a GIF URL for the specified action using multiple APIs

        Args:
            action (str): The action to get a GIF for (e.g., 'anime slap')

        Returns:
            str: URL of the GIF
        """
        # Extract the action type (e.g., 'slap' from 'anime slap')
        action_type = action.replace('anime ', '').replace(' ', '')

        # Try each API in order - Waifu.im first (more reliable)
        for api_name, api_config in self.apis.items():
            try:
                if action_type in api_config['endpoints']:
                    endpoint = api_config['endpoints'][action_type]

                    if api_name == 'waifu':
                        # Waifu.im API - Primary choice
                        url = api_config['base_url']
                        params = {
                            'included_tags': endpoint,
                            'height': '>=200',
                            'is_nsfw': 'false'
                        }
                        response = requests.get(url, params=params, timeout=5)

                        if response.status_code == 200:
                            data = response.json()
                            if 'images' in data and len(data['images']) > 0:
                                return data['images'][0]['url']

                    elif api_name == 'fluxpoint':
                        # Fluxpoint API - Secondary choice
                        url = f"{api_config['base_url']}{endpoint}"
                        headers = api_config['headers']
                        response = requests.get(url, headers=headers, timeout=5)

                        if response.status_code == 200:
                            try:
                                data = response.json()
                                if 'file' in data:
                                    return data['file']
                            except ValueError:
                                # If response is not valid JSON, skip this API
                                continue

                # If this API doesn't have the endpoint, continue to next
                continue

            except Exception as e:
                print(f"Error with {api_name} API for {action}: {e}")
                continue

        # If all APIs fail, try Tenor API as final fallback
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
        Get a GIF from Tenor API as a final fallback

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
                'key': os.getenv('TENOR_API_KEY', 'your-tenor-api-key-here'),
                'limit': 1,
                'media_filter': 'minimal'
            }

            response = requests.get(url, params=params, timeout=5)

            if response.status_code == 200:
                data = response.json()
                if 'results' in data and len(data['results']) > 0:
                    return data['results'][0]['media_formats']['gif']['url']

        except Exception as e:
            print(f"Error with Tenor API for {action_type}: {e}")

        return None

# Create global instance
gif_api = GifAPI()
