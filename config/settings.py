# Bot configuration and settings

# Bot configuration
BOT_CONFIG = {
    'max_purge_amount': 100,
    'max_dice_sides': 1000,
    'max_dice_count': 20,
    'reminder_max_time': 1440,  # 24 hours in minutes
    'help_timeout': 300,  # 5 minutes
}

# API Keys for music functionality
API_KEYS = {
    'spotify_client_id': '51120b5915994a27af3b119f1a8641f8',
    'spotify_client_secret': '7cc725e0614d4b7b9a861672cea01e7e',
    'youtube_api_key': 'AIzaSyBCGPXm3ZmLKk3flredOC03GSWoWhZfgak'
}

# NSFW settings storage (guild_id -> boolean)
nsfw_settings = {}
