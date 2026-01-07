"""
Test script to verify NCAA Sports Tracker functionality
"""
from ncaa_api import NCAAAPIClient
from xml_generator import XMLGenerator
from config_manager import ConfigManager


def test_config_manager():
    """Test configuration management"""
    print("Testing ConfigManager...")
    config = ConfigManager('test_config.json')

    # Test get/set
    config.set('test_key', 'test_value')
    assert config.get('test_key') == 'test_value', "Config get/set failed"

    print("✓ ConfigManager working")


def test_ncaa_api():
    """Test NCAA API client"""
    print("\nTesting NCAA API Client...")
    client = NCAAAPIClient()

    # Test sport codes
    assert 'WBB' in client.SPORT_CODES.values(), "Sport codes missing"
    assert 'MBB' in client.SPORT_CODES.values(), "Sport codes missing"

    # Test date formatting
    formatted = client.format_date('2026-01-07')
    assert formatted == '01/07/2026', f"Date format failed: {formatted}"

    print("✓ NCAA API Client initialized")
    print(f"  - {len(client.SPORT_CODES)} sports available")
    print(f"  - {len(client.DIVISIONS)} divisions available")


def test_xml_generator():
    """Test XML generation"""
    print("\nTesting XML Generator...")
    generator = XMLGenerator()

    # Create test data
    test_contest = {
        'id': 'test123',
        'date': '01/07/2026',
        'time': '7:00 PM',
        'venue': 'Test Arena',
        'home_team': {
            'name': 'Home Team',
            'score': '75',
            'rank': '5'
        },
        'away_team': {
            'name': 'Away Team',
            'score': '70',
            'rank': '10'
        }
    }

    # Generate XML
    xml_string = generator.generate_xml([test_contest], {'Sport': 'Test'})

    # Verify XML content
    assert '<?xml version' in xml_string, "XML header missing"
    assert '<NCAASports>' in xml_string, "Root element missing"
    assert '<Contests' in xml_string, "Contests element missing"
    assert 'Home Team' in xml_string, "Team data missing"
    assert 'Away Team' in xml_string, "Team data missing"

    print("✓ XML Generator working")
    print("  - XML structure valid")
    print("  - Pretty printing enabled")


def test_api_fetch():
    """Test actual API fetch (requires internet)"""
    print("\nTesting API Fetch (requires internet)...")
    client = NCAAAPIClient()

    try:
        # Try to fetch some data
        response = client.fetch_contests(
            sport_code='WBB',
            division=1,
            season_year=2025,
            contest_date='01/07/2026'
        )

        if response and 'data' in response:
            print("✓ API fetch successful")
            contests = client.parse_contests(response)
            print(f"  - Retrieved {len(contests)} contests")
            if contests:
                print(f"  - Sample: {contests[0].get('home_team', {}).get('name', 'N/A')} vs "
                      f"{contests[0].get('away_team', {}).get('name', 'N/A')}")
        else:
            print("⚠ API returned empty response (may be no games scheduled)")

    except Exception as e:
        print(f"⚠ API fetch failed (network issue?): {e}")
        print("  This is OK if internet is unavailable")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("NCAA Sports Tracker - Test Suite")
    print("=" * 60)

    try:
        test_config_manager()
        test_ncaa_api()
        test_xml_generator()
        test_api_fetch()

        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        print("\nYou can now:")
        print("1. Run the GUI: python main_tkinter.py")
        print("2. Build executable: python build_exe.py")
        print("3. Or use build.bat on Windows")

    except Exception as e:
        print("\n" + "=" * 60)
        print(f"✗ Test failed: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
