# Music Commands Implementation TODO

## Steps to Complete

- [x] Update requirements.txt with music dependencies (yt-dlp, spotipy, google-api-python-client, lyricsgenius)
- [x] Read config/settings.py and add API keys if not present (Spotify client_id/secret, YouTube API key)
- [x] Create cogs/music.py with full music functionality (prefix and slash commands, queue system, voice handling, API integrations)
- [x] Update main.py to load 'cogs.music' in cogs_to_load list
- [x] Update config/categories.py to add "music" category with all commands listed
- [ ] Install new dependencies via pip install -r requirements.txt
- [ ] Test music commands (join VC, /play, /pause, /lyrics, etc.)
- [ ] Sync slash commands and verify in /help that music category appears
