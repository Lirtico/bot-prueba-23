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

        # Fallback URLs for when APIs fail
        self.fallback_gifs = {
            'anime slap': 'https://cdn.discordapp.com/emojis/1094046034185949264.gif',
            'anime hug': 'https://cdn.discordapp.com/emojis/1094046034185949265.gif',
            'anime kiss': 'https://cdn.discordapp.com/emojis/1094046034185949266.gif',
            'anime pat': 'https://cdn.discordapp.com/emojis/1094046034185949267.gif',
            'anime tickle': 'https://cdn.discordapp.com/emojis/1094046034185949268.gif',
            'anime feed': 'https://cdn.discordapp.com/emojis/1094046034185949269.gif',
            'anime punch': 'https://cdn.discordapp.com/emojis/1094046034185949270.gif',
            'anime high five': 'https://cdn.discordapp.com/emojis/1094046034185949271.gif',
            'anime bite': 'https://cdn.discordapp.com/emojis/1094046034185949272.gif',
            'anime shoot': 'https://cdn.discordapp.com/emojis/1094046034185949273.gif',
            'anime wave': 'https://cdn.discordapp.com/emojis/1094046034185949274.gif',
            'anime happy': 'https://cdn.discordapp.com/emojis/1094046034185949275.gif',
            'anime peck': 'https://cdn.discordapp.com/emojis/1094046034185949276.gif',
            'anime lurk': 'https://cdn.discordapp.com/emojis/1094046034185949277.gif',
            'anime sleep': 'https://cdn.discordapp.com/emojis/1094046034185949278.gif',
            'anime wink': 'https://cdn.discordapp.com/emojis/1094046034185949279.gif',
            'anime yawn': 'https://cdn.discordapp.com/emojis/1094046034185949280.gif',
            'anime nom': 'https://cdn.discordapp.com/emojis/1094046034185949281.gif',
            'anime yeet': 'https://cdn.discordapp.com/emojis/1094046034185949282.gif',
            'anime think': 'https://cdn.discordapp.com/emojis/1094046034185949283.gif',
            'anime bored': 'https://cdn.discordapp.com/emojis/1094046034185949284.gif',
            'anime blush': 'https://cdn.discordapp.com/emojis/1094046034185949285.gif',
            'anime stare': 'https://cdn.discordapp.com/emojis/1094046034185949286.gif',
            'anime nod': 'https://cdn.discordapp.com/emojis/1094046034185949287.gif',
            'anime handhold': 'https://cdn.discordapp.com/emojis/1094046034185949288.gif',
            'anime smug': 'https://cdn.discordapp.com/emojis/1094046034185949289.gif',
            'anime fuck': 'https://cdn.discordapp.com/emojis/1094046034185949290.gif',
            'anime spank': 'https://cdn.discordapp.com/emojis/1094046034185949291.gif',
            'anime nutkick': 'https://cdn.discordapp.com/emojis/1094046034185949292.gif',
            'anime shrug': 'https://cdn.discordapp.com/emojis/1094046034185949293.gif',
            'anime poke': 'https://cdn.discordapp.com/emojis/1094046034185949294.gif',
            'anime smile': 'https://cdn.discordapp.com/emojis/1094046034185949295.gif',
            'anime facepalm': 'https://cdn.discordapp.com/emojis/1094046034185949296.gif',
            'anime cuddle': 'https://cdn.discordapp.com/emojis/1094046034185949297.gif',
            'anime baka': 'https://cdn.discordapp.com/emojis/1094046034185949298.gif',
            'anime angry': 'https://cdn.discordapp.com/emojis/1094046034185949299.gif',
            'anime run': 'https://cdn.discordapp.com/emojis/1094046034185949300.gif',
            'anime nope': 'https://cdn.discordapp.com/emojis/1094046034185949301.gif',
            'anime handshake': 'https://cdn.discordapp.com/emojis/1094046034185949302.gif',
            'anime cry': 'https://cdn.discordapp.com/emojis/1094046034185949303.gif',
            'anime pout': 'https://cdn.discordapp.com/emojis/1094046034185949304.gif',
            'anime thumbs up': 'https://cdn.discordapp.com/emojis/1094046034185949305.gif',
            'anime laugh': 'https://cdn.discordapp.com/emojis/1094046034185949306.gif'
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

        # If all APIs fail, use fallback
        return self.fallback_gifs.get(action, 'https://cdn.discordapp.com/emojis/1094046034185949264.gif')

# Create global instance
gif_api = GifAPI()
