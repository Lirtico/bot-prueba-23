#!/usr/bin/env python3
"""
Test script to debug GIF API issues
"""
import os
import sys
import requests
from gif_api import gif_api

def test_gif_api():
    """Test the GIF API functionality"""
    print("Testing GIF API...")

    # Test a few different actions
    test_actions = ['anime slap', 'anime hug', 'anime kiss', 'anime laugh']

    for action in test_actions:
        print(f"\n--- Testing {action} ---")
        try:
            url = gif_api.get_gif_url(action)
            print(f"Generated URL: {url}")

            # Test if URL is accessible
            response = requests.head(url, timeout=5)
            print(f"URL Status: {response.status_code}")
            print(f"Content-Type: {response.headers.get('content-type', 'Unknown')}")

            if response.status_code == 200:
                print("✅ URL is accessible")
            else:
                print("❌ URL is not accessible")

        except Exception as e:
            print(f"❌ Error testing {action}: {e}")

def test_direct_apis():
    """Test the APIs directly"""
    print("\n\n--- Testing APIs directly ---")

    # Test Waifu.im API
    print("\nTesting Waifu.im API...")
    try:
        url = "https://api.waifu.im/search"
        params = {
            'included_tags': 'slap',
            'height': '>=200',
            'is_nsfw': 'false'
        }
        response = requests.get(url, params=params, timeout=5)
        print(f"Waifu.im Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
    except Exception as e:
        print(f"Waifu.im Error: {e}")

    # Test Tenor API
    print("\nTesting Tenor API...")
    try:
        url = "https://tenor.googleapis.com/v2/search"
        params = {
            'q': 'anime slap',
            'key': 'LIVDSRZULELA',
            'limit': 1,
            'media_filter': 'minimal'
        }
        response = requests.get(url, params=params, timeout=5)
        print(f"Tenor Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            if 'results' in data and len(data['results']) > 0:
                result = data['results'][0]
                print(f"First result keys: {list(result.keys())}")
                if 'media_formats' in result:
                    print(f"Media formats: {list(result['media_formats'].keys())}")
                    for format_name, format_data in result['media_formats'].items():
                        print(f"  {format_name}: {format_data.get('url', 'No URL')}")
                if 'url' in result:
                    print(f"Direct URL: {result['url']}")
    except Exception as e:
        print(f"Tenor Error: {e}")

if __name__ == "__main__":
    # Write output to file for debugging
    with open('gif_api_test_output.txt', 'w') as f:
        import sys
        original_stdout = sys.stdout
        sys.stdout = f

        test_gif_api()
        test_direct_apis()

        sys.stdout = original_stdout

    print("Test results written to gif_api_test_output.txt")
