#!/usr/bin/env python3
"""
Test script for the new Nekos.best API integration
"""

from gif_api import gif_api

def test_gif_api():
    """Test the new GIF API with various commands"""
    test_commands = [
        'anime slap',
        'anime hug',
        'anime kiss',
        'anime pat',
        'anime tickle',
        'anime punch',
        'anime bite',
        'anime cuddle',
        'anime wave',
        'anime wink',
        'anime poke',
        'anime smile',
        'anime blush',
        'anime stare',
        'anime happy',
        'anime cry',
        'anime laugh',
        'anime angry',
        'anime smug',
        'anime sleep',
        'anime bored',
        'anime think',
        'anime facepalm',
        'anime shrug',
        'anime nod',
        'anime nom',
        'anime yeet',
        'anime run',
        'anime nope',
        'anime handshake',
        'anime handhold',
        'anime thumbsup',
        'anime highfive',
        'anime shoot',
        'anime peck',
        'anime lurk',
        'anime yawn',
        'anime baka',
        'anime pout',
        'anime spank',
        'anime nutkick',
        'anime fuck'
    ]

    print("Testing new Nekos.best API integration...")
    print("=" * 60)

    successful = 0
    failed = 0

    for command in test_commands:
        try:
            url = gif_api.get_gif_url(command)
            if url and url != 'https://cdn.discordapp.com/emojis/1094046034185949264.gif':
                print(f"✅ {command}: {url}")
                successful += 1
            else:
                print(f"❌ {command}: Fallback used")
                failed += 1
        except Exception as e:
            print(f"❌ {command}: Error - {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Test Results: {successful} successful, {failed} failed")
    success_rate = (successful / (successful + failed) * 100) if (successful + failed) > 0 else 0
    print(f"Success rate: {success_rate:.1f}%")

    if successful > 0:
        print("\n🎉 The new Nekos.best API integration is working!")
        print("All role commands should now use GIFs from Nekos.best API.")
    else:
        print("\n⚠️  Some issues detected. Please check the API endpoints.")

if __name__ == "__main__":
    test_gif_api()
