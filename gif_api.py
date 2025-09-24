import requests
import random
import os
from typing import Optional

class GifAPI:
    def __init__(self):
        # Tenor API configuration
        self.api_key = os.getenv('TENOR_API_KEY', 'LIVDSRZULELA')  # Default key for development
        self.base_url = "https://tenor.googleapis.com/v2"

        # Fallback GIF URLs for when API fails
        self.fallback_gifs = {
            'anime slap': 'https://tenor.com/view/anime-slap-gif-123456789',
            'anime hug': 'https://tenor.com/view/anime-hug-gif-123456790',
            'anime kiss': 'https://tenor.com/view/anime-kiss-gif-123456791',
            'anime pat': 'https://tenor.com/view/anime-pat-gif-123456792',
            'anime tickle': 'https://tenor.com/view/anime-tickle-gif-123456793',
            'anime feed': 'https://tenor.com/view/anime-feed-gif-123456794',
            'anime punch': 'https://tenor.com/view/anime-punch-gif-123456795',
            'anime high five': 'https://tenor.com/view/anime-high-five-gif-123456796',
            'anime bite': 'https://tenor.com/view/anime-bite-gif-123456797',
            'anime shoot': 'https://tenor.com/view/anime-shoot-gif-123456798',
            'anime wave': 'https://tenor.com/view/anime-wave-gif-123456799',
            'anime happy': 'https://tenor.com/view/anime-happy-gif-123456800',
            'anime peck': 'https://tenor.com/view/anime-peck-gif-123456801',
            'anime lurk': 'https://tenor.com/view/anime-lurk-gif-123456802',
            'anime sleep': 'https://tenor.com/view/anime-sleep-gif-123456803',
            'anime wink': 'https://tenor.com/view/anime-wink-gif-123456804',
            'anime yawn': 'https://tenor.com/view/anime-yawn-gif-123456805',
            'anime nom': 'https://tenor.com/view/anime-nom-gif-123456806',
            'anime yeet': 'https://tenor.com/view/anime-yeet-gif-123456807',
            'anime think': 'https://tenor.com/view/anime-think-gif-123456808',
            'anime bored': 'https://tenor.com/view/anime-bored-gif-123456809',
            'anime blush': 'https://tenor.com/view/anime-blush-gif-123456810',
            'anime stare': 'https://tenor.com/view/anime-stare-gif-123456811',
            'anime nod': 'https://tenor.com/view/anime-nod-gif-123456812',
            'anime handhold': 'https://tenor.com/view/anime-handhold-gif-123456813',
            'anime smug': 'https://tenor.com/view/anime-smug-gif-123456814',
            'anime fuck': 'https://tenor.com/view/anime-fuck-gif-123456815',
            'anime spank': 'https://tenor.com/view/anime-spank-gif-123456816',
            'anime nutkick': 'https://tenor.com/view/anime-nutkick-gif-123456817',
            'anime shrug': 'https://tenor.com/view/anime-shrug-gif-123456818',
            'anime poke': 'https://tenor.com/view/anime-poke-gif-123456819',
            'anime smile': 'https://tenor.com/view/anime-smile-gif-123456820',
            'anime facepalm': 'https://tenor.com/view/anime-facepalm-gif-123456821',
            'anime cuddle': 'https://tenor.com/view/anime-cuddle-gif-123456822',
            'anime baka': 'https://tenor.com/view/anime-baka-gif-123456823',
            'anime angry': 'https://tenor.com/view/anime-angry-gif-123456824',
            'anime run': 'https://tenor.com/view/anime-run-gif-123456825',
            'anime nope': 'https://tenor.com/view/anime-nope-gif-123456826',
            'anime handshake': 'https://tenor.com/view/anime-handshake-gif-123456827',
            'anime cry': 'https://tenor.com/view/anime-cry-gif-123456828',
            'anime pout': 'https://tenor.com/view/anime-pout-gif-123456829',
            'anime thumbs up': 'https://tenor.com/view/anime-thumbs-up-gif-123456830',
            'anime laugh': 'https://tenor.com/view/anime-laugh-gif-123456831'
        }

    def get_gif_url(self, action: str) -> str:
        """
        Get a GIF URL for the specified action

        Args:
            action (str): The action to get a GIF for (e.g., 'anime slap')

        Returns:
            str: URL of the GIF
        """
        try:
            # Try to get from Tenor API first
            api_url = f"{self.base_url}/search"
            params = {
                'q': action,
                'key': self.api_key,
                'limit': 10,
                'media_filter': 'minimal',  # Only get GIFs, not videos
                'contentfilter': 'medium'   # Medium content filter
            }

            response = requests.get(api_url, params=params, timeout=5)

            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])

                if results:
                    # Pick a random GIF from the results
                    gif_data = random.choice(results)
                    return gif_data['media_formats']['gif']['url']

            # If API fails or no results, use fallback
            return self.fallback_gifs.get(action, 'https://tenor.com/view/anime-gif-123456789')

        except Exception as e:
            print(f"Error getting GIF for {action}: {e}")
            # Return fallback GIF
            return self.fallback_gifs.get(action, 'https://tenor.com/view/anime-gif-123456789')

# Create global instance
gif_api = GifAPI()
