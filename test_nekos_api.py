import requests
import json

# Test some common endpoints to understand the API structure
test_endpoints = [
    'neko', 'hug', 'kiss', 'pat', 'slap', 'tickle', 'feed', 'punch', 'bite', 'cuddle',
    'wave', 'wink', 'poke', 'smile', 'blush', 'stare', 'happy', 'dance', 'cringe',
    'cry', 'laugh', 'angry', 'smug', 'shy', 'sleep', 'bored', 'think', 'facepalm',
    'shrug', 'nod', 'nom', 'yeet', 'run', 'nope', 'handshake', 'handhold', 'thumbsup',
    'highfive', 'shoot', 'peck', 'lurk', 'yawn', 'baka', 'pout', 'spank', 'nutkick', 'fuck'
]

print("Testing Nekos.best API endpoints...")
print("=" * 50)

for endpoint in test_endpoints:
    try:
        url = f"https://nekos.best/api/v2/{endpoint}"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                item = data['data'][0]
                if 'url' in item:
                    print(f"✅ {endpoint}: {item['url']}")
                else:
                    print(f"⚠️  {endpoint}: Response format different")
            else:
                print(f"⚠️  {endpoint}: No data in response")
        else:
            print(f"❌ {endpoint}: HTTP {response.status_code}")

    except Exception as e:
        print(f"❌ {endpoint}: {str(e)}")

print("\n" + "=" * 50)
print("Test completed!")
