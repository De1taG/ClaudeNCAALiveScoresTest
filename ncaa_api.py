"""NCAA API client for fetching sports event data"""
import requests
from datetime import datetime
from typing import List, Dict, Optional


class NCAAAPIClient:
    """Client for interacting with NCAA.com API"""

    BASE_URL = "https://sdataprod.ncaa.com/"
    QUERY_HASH = "7287cda610a9326931931080cb3a604828febe6fe3c9016a7e4a36db99efdb7c"

    # Sport codes mapping
    SPORT_CODES = {
        "Women's Basketball": "WBB",
        "Men's Basketball": "MBB",
        "Football": "MFB",
        "Baseball": "MBA",
        "Softball": "WSB",
        "Women's Volleyball": "WVB",
        "Men's Soccer": "MSO",
        "Women's Soccer": "WSO",
        "Women's Lacrosse": "WLA",
        "Men's Lacrosse": "MLA",
        "Ice Hockey": "MIH",
        "Wrestling": "MWR"
    }

    DIVISIONS = {
        "Division I": 1,
        "Division II": 2,
        "Division III": 3
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_contests(self, sport_code: str, division: int = 1,
                      season_year: int = 2025, contest_date: Optional[str] = None,
                      week: Optional[int] = None) -> Dict:
        """
        Fetch contests from NCAA API

        Args:
            sport_code: Sport code (e.g., 'WBB', 'MBB')
            division: Division number (1, 2, or 3)
            season_year: Season year (e.g., 2025)
            contest_date: Date in MM/DD/YYYY format
            week: Week number (optional)

        Returns:
            Dict containing contest data
        """
        params = {
            "meta": "GetContests_web",
            "extensions": f'{{"persistedQuery":{{"version":1,"sha256Hash":"{self.QUERY_HASH}"}}}}',
            "variables": f'{{"sportCode":"{sport_code}","division":{division},"seasonYear":{season_year},"contestDate":"{contest_date}","week":{week}}}'
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching contests: {e}")
            return {"data": {"contests": []}}

    def parse_contests(self, response_data: Dict) -> List[Dict]:
        """
        Parse contest data from API response

        Args:
            response_data: Raw API response

        Returns:
            List of parsed contest dictionaries
        """
        contests = []

        try:
            if 'data' in response_data and 'contests' in response_data['data']:
                for contest in response_data['data']['contests']:
                    parsed = self._parse_single_contest(contest)
                    if parsed:
                        contests.append(parsed)
        except Exception as e:
            print(f"Error parsing contests: {e}")

        return contests

    def _parse_single_contest(self, contest: Dict) -> Optional[Dict]:
        """Parse a single contest from API response"""
        try:
            # Extract basic contest info
            parsed = {
                'id': contest.get('id', ''),
                'date': contest.get('startDate', ''),
                'time': contest.get('startTime', ''),
                'location': contest.get('location', ''),
                'venue': contest.get('venue', ''),
                'status': contest.get('contestState', ''),
                'broadcast': contest.get('broadcast', ''),
                'tournament': contest.get('tournament', ''),
                'sport': contest.get('sport', ''),
                'division': contest.get('division', ''),
                'home_team': {},
                'away_team': {}
            }

            # Extract home team info
            if 'home' in contest:
                home = contest['home']
                parsed['home_team'] = {
                    'name': home.get('names', {}).get('full', ''),
                    'short_name': home.get('names', {}).get('short', ''),
                    'score': home.get('score', ''),
                    'rank': home.get('rank', ''),
                    'conference': home.get('conferences', [{}])[0].get('conferenceName', '') if home.get('conferences') else '',
                    'record': home.get('currentRecord', '')
                }

            # Extract away team info
            if 'away' in contest:
                away = contest['away']
                parsed['away_team'] = {
                    'name': away.get('names', {}).get('full', ''),
                    'short_name': away.get('names', {}).get('short', ''),
                    'score': away.get('score', ''),
                    'rank': away.get('rank', ''),
                    'conference': away.get('conferences', [{}])[0].get('conferenceName', '') if away.get('conferences') else '',
                    'record': away.get('currentRecord', '')
                }

            return parsed
        except Exception as e:
            print(f"Error parsing single contest: {e}")
            return None

    def is_top_25(self, contest: Dict) -> bool:
        """Check if contest involves a top 25 ranked team"""
        try:
            home_rank = contest.get('home_team', {}).get('rank')
            away_rank = contest.get('away_team', {}).get('rank')

            if home_rank and isinstance(home_rank, (int, str)):
                if int(str(home_rank).strip()) <= 25:
                    return True
            if away_rank and isinstance(away_rank, (int, str)):
                if int(str(away_rank).strip()) <= 25:
                    return True
        except (ValueError, TypeError):
            pass

        return False

    @staticmethod
    def format_date(date_str: str) -> str:
        """Format date string to MM/DD/YYYY"""
        try:
            if '/' in date_str:
                return date_str
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            return dt.strftime('%m/%d/%Y')
        except:
            return date_str
