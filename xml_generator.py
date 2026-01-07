"""XML generator for NCAA contest data"""
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import List, Dict
from datetime import datetime


class XMLGenerator:
    """Generates pretty-printed XML from contest data"""

    def __init__(self):
        pass

    def generate_xml(self, contests: List[Dict], metadata: Dict = None) -> str:
        """
        Generate pretty-printed XML from contest data

        Args:
            contests: List of contest dictionaries
            metadata: Optional metadata to include in XML

        Returns:
            Pretty-printed XML string
        """
        root = ET.Element('NCAASports')

        # Add metadata
        meta_elem = ET.SubElement(root, 'Metadata')
        if metadata:
            for key, value in metadata.items():
                meta_child = ET.SubElement(meta_elem, key)
                meta_child.text = str(value)

        # Add generation timestamp
        timestamp = ET.SubElement(meta_elem, 'GeneratedAt')
        timestamp.text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Add contests
        contests_elem = ET.SubElement(root, 'Contests')
        contests_elem.set('count', str(len(contests)))

        for contest in contests:
            self._add_contest(contests_elem, contest)

        # Pretty print
        return self._prettify_xml(root)

    def _add_contest(self, parent: ET.Element, contest: Dict):
        """Add a single contest to the XML tree"""
        contest_elem = ET.SubElement(parent, 'Contest')
        contest_elem.set('id', str(contest.get('id', '')))

        # Basic info
        for key in ['date', 'time', 'location', 'venue', 'status', 'broadcast',
                    'tournament', 'sport', 'division']:
            if contest.get(key):
                elem = ET.SubElement(contest_elem, key.replace('_', '').title())
                elem.text = str(contest[key])

        # Home team
        if contest.get('home_team'):
            home_elem = ET.SubElement(contest_elem, 'HomeTeam')
            self._add_team(home_elem, contest['home_team'])

        # Away team
        if contest.get('away_team'):
            away_elem = ET.SubElement(contest_elem, 'AwayTeam')
            self._add_team(away_elem, contest['away_team'])

    def _add_team(self, parent: ET.Element, team: Dict):
        """Add team information to XML"""
        for key, value in team.items():
            if value:
                elem = ET.SubElement(parent, key.replace('_', '').title())
                elem.text = str(value)

    def _prettify_xml(self, elem: ET.Element) -> str:
        """Return a pretty-printed XML string"""
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent='  ')

    def save_to_file(self, xml_string: str, file_path: str):
        """Save XML string to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(xml_string)
            return True
        except Exception as e:
            print(f"Error saving XML: {e}")
            return False
