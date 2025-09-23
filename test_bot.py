#!/usr/bin/env python3
"""
Test script to verify bot functionality
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_imports():
    """Test that all modules can be imported successfully"""
    try:
        print("Testing imports...")

        # Test core imports
        from config import config_manager
        print("✅ Config module imported successfully")

        from database import db_manager
        print("✅ Database module imported successfully")

        from logging_config import log_manager
        print("✅ Logging module imported successfully")

        from detection import threat_detector
        print("✅ Detection module imported successfully")

        print("\n🎉 All imports successful!")
        return True

    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

async def test_database():
    """Test database connectivity"""
    try:
        print("\nTesting database connection...")

        from database import db_manager

        # Test database connection
        await db_manager.create_tables()
        print("✅ Database tables created successfully")

        # Test basic database operations
        test_guild = await db_manager.get_or_create_guild(123456789, {
            'name': 'Test Guild',
            'owner_id': 987654321,
            'member_count': 100
        })
        print("✅ Guild creation test successful")

        test_user = await db_manager.get_or_create_user(987654321, {
            'username': 'testuser',
            'discriminator': '1234',
            'display_name': 'Test User',
            'bot': False,
            'system': False
        })
        print("✅ User creation test successful")

        print("🎉 Database tests passed!")
        return True

    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

async def test_configuration():
    """Test configuration loading"""
    try:
        print("\nTesting configuration...")

        from config import config_manager

        print(f"✅ Environment: {config_manager.settings.environment}")
        print(f"✅ Debug mode: {config_manager.settings.debug}")
        print(f"✅ Command prefix: {config_manager.settings.discord.command_prefix}")

        print("🎉 Configuration tests passed!")
        return True

    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting Discord Bot Tests")
    print("=" * 50)

    tests = [
        test_imports,
        test_configuration,
        test_database
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if await test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Bot is ready to run.")
        print("\nNext steps:")
        print("1. Add your Discord bot token to the .env file")
        print("2. Run: python main.py")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    # Run tests
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
