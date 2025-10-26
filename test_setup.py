"""Test script to verify setup and configuration."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from src.config import settings
        print("✅ Config module imported")

        from src.agents import ClaudeAgent, ResearchAgent, ScriptwriterAgent
        print("✅ Agent modules imported")

        from src.models import Base, Script, init_db, get_db
        print("✅ Model modules imported")

        from src.services import ScriptService
        print("✅ Service modules imported")

        from src.utils import validate_topic, ValidationError
        print("✅ Utility modules imported")

        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False


def test_configuration():
    """Test configuration validation."""
    print("\nTesting configuration...")
    try:
        from src.config import settings

        if not settings.ANTHROPIC_API_KEY:
            print("⚠️  Warning: ANTHROPIC_API_KEY not set in .env")
            return False

        print(f"✅ API key configured")
        print(f"✅ Model: {settings.CLAUDE_MODEL}")
        print(f"✅ Database: {settings.DATABASE_URL}")

        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def test_validators():
    """Test validation functions."""
    print("\nTesting validators...")
    try:
        from src.utils import (
            validate_topic,
            validate_style,
            validate_duration,
            ValidationError
        )

        # Test valid inputs
        validate_topic("How to start a business")
        validate_style("educational")
        validate_duration("10-15 minutes")
        print("✅ Valid inputs pass validation")

        # Test invalid inputs
        try:
            validate_topic("abc")  # Too short
            print("❌ Short topic validation failed")
            return False
        except ValidationError:
            print("✅ Short topic correctly rejected")

        try:
            validate_style("invalid")  # Invalid style
            print("❌ Invalid style validation failed")
            return False
        except ValidationError:
            print("✅ Invalid style correctly rejected")

        return True
    except Exception as e:
        print(f"❌ Validator error: {e}")
        return False


async def test_database():
    """Test database initialization."""
    print("\nTesting database...")
    try:
        from src.models import init_db

        await init_db()
        print("✅ Database initialized successfully")

        # Check if database file was created
        db_path = Path("data/scripts.db")
        if db_path.exists():
            print(f"✅ Database file created: {db_path}")
        else:
            print("⚠️  Database file not found (using in-memory)")

        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False


async def run_tests():
    """Run all tests."""
    print("=" * 60)
    print("AI Script Agent - Setup Verification")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_configuration()))
    results.append(("Validators", test_validators()))
    results.append(("Database", await test_database()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20s}: {status}")

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nTo start the application:")
        print("  python -m src.main")
        print("  OR")
        print("  uvicorn src.main:app --reload")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("Make sure you have:")
        print("  1. Installed all dependencies (pip install -r requirements.txt)")
        print("  2. Created .env file with ANTHROPIC_API_KEY")

    return passed == total


if __name__ == "__main__":
    import asyncio
    success = asyncio.run(run_tests())
    sys.exit(0 if success else 1)
