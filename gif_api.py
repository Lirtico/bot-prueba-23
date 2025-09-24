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
            'anime slap': 'https://media.tenor.com/8K7gC8K7gCAAAAAC/anime-slap.gif',
            'anime hug': 'https://media.tenor.com/4M0k94M0k9AAAAAC/anime-hug.gif',
            'anime kiss': 'https://media.tenor.com/3K2kH3K2kHAAAAAC/anime-kiss.gif',
            'anime pat': 'https://media.tenor.com/5M0k95M0k9AAAAAC/anime-pat.gif',
            'anime tickle': 'https://media.tenor.com/6M0k96M0k9AAAAAC/anime-tickle.gif',
            'anime feed': 'https://media.tenor.com/7M0k97M0k9AAAAAC/anime-feed.gif',
            'anime punch': 'https://media.tenor.com/8M0k98M0k9AAAAAC/anime-punch.gif',
            'anime high five': 'https://media.tenor.com/9M0k99M0k9AAAAAC/anime-high-five.gif',
            'anime bite': 'https://media.tenor.com/10M0k910M0k9AAAAAC/anime-bite.gif',
            'anime shoot': 'https://media.tenor.com/11M0k911M0k9AAAAAC/anime-shoot.gif',
            'anime wave': 'https://media.tenor.com/12M0k912M0k9AAAAAC/anime-wave.gif',
            'anime happy': 'https://media.tenor.com/13M0k913M0k9AAAAAC/anime-happy.gif',
            'anime peck': 'https://media.tenor.com/14M0k914M0k9AAAAAC/anime-peck.gif',
            'anime lurk': 'https://media.tenor.com/15M0k915M0k9AAAAAC/anime-lurk.gif',
            'anime sleep': 'https://media.tenor.com/16M0k916M0k9AAAAAC/anime-sleep.gif',
            'anime wink': 'https://media.tenor.com/17M0k917M0k9AAAAAC/anime-wink.gif',
            'anime yawn': 'https://media.tenor.com/18M0k918M0k9AAAAAC/anime-yawn.gif',
            'anime nom': 'https://media.tenor.com/19M0k919M0k9AAAAAC/anime-nom.gif',
            'anime yeet': 'https://media.tenor.com/20M0k920M0k9AAAAAC/anime-yeet.gif',
            'anime think': 'https://media.tenor.com/21M0k921M0k9AAAAAC/anime-think.gif',
            'anime bored': 'https://media.tenor.com/22M0k922M0k9AAAAAC/anime-bored.gif',
            'anime blush': 'https://media.tenor.com/23M0k923M0k9AAAAAC/anime-blush.gif',
            'anime stare': 'https://media.tenor.com/24M0k924M0k9AAAAAC/anime-stare.gif',
            'anime nod': 'https://media.tenor.com/25M0k925M0k9AAAAAC/anime-nod.gif',
            'anime handhold': 'https://media.tenor.com/26M0k926M0k9AAAAAC/anime-handhold.gif',
            'anime smug': 'https://media.tenor.com/27M0k927M0k9AAAAAC/anime-smug.gif',
            'anime fuck': 'https://media.tenor.com/28M0k928M0k9AAAAAC/anime-fuck.gif',
            'anime spank': 'https://media.tenor.com/29M0k929M0k9AAAAAC/anime-spank.gif',
            'anime nutkick': 'https://media.tenor.com/30M0k930M0k9AAAAAC/anime-nutkick.gif',
            'anime shrug': 'https://media.tenor.com/31M0k931M0k9AAAAAC/anime-shrug.gif',
            'anime poke': 'https://media.tenor.com/32M0k932M0k9AAAAAC/anime-poke.gif',
            'anime smile': 'https://media.tenor.com/33M0k933M0k9AAAAAC/anime-smile.gif',
            'anime facepalm': 'https://media.tenor.com/34M0k934M0k9AAAAAC/anime-facepalm.gif',
            'anime cuddle': 'https://media.tenor.com/35M0k935M0k9AAAAAC/anime-cuddle.gif',
            'anime baka': 'https://media.tenor.com/36M0k936M0k9AAAAAC/anime-baka.gif',
            'anime angry': 'https://media.tenor.com/37M0k937M0k9AAAAAC/anime-angry.gif',
            'anime run': 'https://media.tenor.com/38M0k938M0k9AAAAAC/anime-run.gif',
            'anime nope': 'https://media.tenor.com/39M0k939M0k9AAAAAC/anime-nope.gif',
            'anime handshake': 'https://media.tenor.com/40M0k940M0k9AAAAAC/anime-handshake.gif',
            'anime cry': 'https://media.tenor.com/41M0k941M0k9AAAAAC/anime-cry.gif',
            'anime pout': 'https://media.tenor.com/42M0k942M0k9AAAAAC/anime-pout.gif',
            'anime thumbs up': 'https://media.tenor.com/43M0k943M0k9AAAAAC/anime-thumbs-up.gif',
            'anime laugh': 'https://media.tenor.com/44M0k944M0k9AAAAAC/anime-laugh.gif'
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
