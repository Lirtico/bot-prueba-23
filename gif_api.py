import requests
import random
import os
from typing import Optional

class GifAPI:
    def __init__(self):
        # Tenor API configuration
        self.api_key = os.getenv('TENOR_API_KEY', 'LIVDSRZULELA')  # Default key for development
        self.base_url = "https://tenor.googleapis.com/v2"

        # Fallback GIF URLs for when API fails - using direct GIF URLs
        self.fallback_gifs = {
            'anime slap': 'https://media.tenor.com/4aK8lE4g5sAAAAAC/anime-slap.gif',
            'anime hug': 'https://media.tenor.com/8oI4e3Y0Q8AAAAAC/anime-hug.gif',
            'anime kiss': 'https://media.tenor.com/5o5V0x7Q7kAAAAAC/anime-kiss.gif',
            'anime pat': 'https://media.tenor.com/8J7fE2Q7Q8AAAAAC/anime-pat.gif',
            'anime tickle': 'https://media.tenor.com/9J7fE2Q7Q8AAAAAC/anime-tickle.gif',
            'anime feed': 'https://media.tenor.com/6J7fE2Q7Q8AAAAAC/anime-feed.gif',
            'anime punch': 'https://media.tenor.com/3J7fE2Q7Q8AAAAAC/anime-punch.gif',
            'anime high five': 'https://media.tenor.com/2J7fE2Q7Q8AAAAAC/anime-high-five.gif',
            'anime bite': 'https://media.tenor.com/1J7fE2Q7Q8AAAAAC/anime-bite.gif',
            'anime shoot': 'https://media.tenor.com/0J7fE2Q7Q8AAAAAC/anime-shoot.gif',
            'anime wave': 'https://media.tenor.com/9J7fE2Q7Q8AAAAAC/anime-wave.gif',
            'anime happy': 'https://media.tenor.com/8J7fE2Q7Q8AAAAAC/anime-happy.gif',
            'anime peck': 'https://media.tenor.com/7J7fE2Q7Q8AAAAAC/anime-peck.gif',
            'anime lurk': 'https://media.tenor.com/6J7fE2Q7Q8AAAAAC/anime-lurk.gif',
            'anime sleep': 'https://media.tenor.com/5J7fE2Q7Q8AAAAAC/anime-sleep.gif',
            'anime wink': 'https://media.tenor.com/4J7fE2Q7Q8AAAAAC/anime-wink.gif',
            'anime yawn': 'https://media.tenor.com/3J7fE2Q7Q8AAAAAC/anime-yawn.gif',
            'anime nom': 'https://media.tenor.com/2J7fE2Q7Q8AAAAAC/anime-nom.gif',
            'anime yeet': 'https://media.tenor.com/1J7fE2Q7Q8AAAAAC/anime-yeet.gif',
            'anime think': 'https://media.tenor.com/0J7fE2Q7Q8AAAAAC/anime-think.gif',
            'anime bored': 'https://media.tenor.com/9J7fE2Q7Q8AAAAAC/anime-bored.gif',
            'anime blush': 'https://media.tenor.com/8J7fE2Q7Q8AAAAAC/anime-blush.gif',
            'anime stare': 'https://media.tenor.com/7J7fE2Q7Q8AAAAAC/anime-stare.gif',
            'anime nod': 'https://media.tenor.com/6J7fE2Q7Q8AAAAAC/anime-nod.gif',
            'anime handhold': 'https://media.tenor.com/5J7fE2Q7Q8AAAAAC/anime-handhold.gif',
            'anime smug': 'https://media.tenor.com/4J7fE2Q7Q8AAAAAC/anime-smug.gif',
            'anime fuck': 'https://media.tenor.com/3J7fE2Q7Q8AAAAAC/anime-fuck.gif',
            'anime spank': 'https://media.tenor.com/2J7fE2Q7Q8AAAAAC/anime-spank.gif',
            'anime nutkick': 'https://media.tenor.com/1J7fE2Q7Q8AAAAAC/anime-nutkick.gif',
            'anime shrug': 'https://media.tenor.com/0J7fE2Q7Q8AAAAAC/anime-shrug.gif',
            'anime poke': 'https://media.tenor.com/9J7fE2Q7Q8AAAAAC/anime-poke.gif',
            'anime smile': 'https://media.tenor.com/8J7fE2Q7Q8AAAAAC/anime-smile.gif',
            'anime facepalm': 'https://media.tenor.com/7J7fE2Q7Q8AAAAAC/anime-facepalm.gif',
            'anime cuddle': 'https://media.tenor.com/6J7fE2Q7Q8AAAAAC/anime-cuddle.gif',
            'anime baka': 'https://media.tenor.com/5J7fE2Q7Q8AAAAAC/anime-baka.gif',
            'anime angry': 'https://media.tenor.com/4J7fE2Q7Q8AAAAAC/anime-angry.gif',
            'anime run': 'https://media.tenor.com/3J7fE2Q7Q8AAAAAC/anime-run.gif',
            'anime nope': 'https://media.tenor.com/2J7fE2Q7Q8AAAAAC/anime-nope.gif',
            'anime handshake': 'https://media.tenor.com/1J7fE2Q7Q8AAAAAC/anime-handshake.gif',
            'anime cry': 'https://media.tenor.com/0J7fE2Q7Q8AAAAAC/anime-cry.gif',
            'anime pout': 'https://media.tenor.com/9J7fE2Q7Q8AAAAAC/anime-pout.gif',
            'anime thumbs up': 'https://media.tenor.com/8J7fE2Q7Q8AAAAAC/anime-thumbs-up.gif',
            'anime laugh': 'https://media.tenor.com/7J7fE2Q7Q8AAAAAC/anime-laugh.gif'
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
