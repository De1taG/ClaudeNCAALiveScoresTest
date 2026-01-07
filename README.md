# NCAA Sports Tracker

A modern desktop application for tracking and managing NCAA sports events with XML export capabilities.

## Features

- **Fetch NCAA Sports Data**: Retrieve event data from NCAA.com's official API
- **Multi-Sport Support**: Women's/Men's Basketball, Football, Baseball, Softball, Volleyball, Soccer, Lacrosse, Ice Hockey, and Wrestling
- **Smart Filtering**: Filter by sport, division, date, week, conference, and Top 25 rankings
- **Event Selection**: Click to select multiple events for export
- **XML Export**: Generate pretty-printed XML files with selected events
- **Auto-Update**: Automatically refresh and update XML files at custom intervals
- **Persistent Settings**: Remembers your last save directory
- **Modern UI**: Clean, intuitive interface with dark theme

## Requirements

- Python 3.7 or higher
- Internet connection to fetch NCAA data

## Installation & Building the Executable

### Quick Build (Windows)

1. **Double-click `build.bat`** - This will automatically:
   - Install required Python packages
   - Build the executable
   - Create `NCAA_Sports_Tracker.exe` in the `dist` folder

### Manual Build

1. **Install Dependencies**:
   ```bash
   pip install requests pyinstaller
   ```

2. **Build the Executable**:
   ```bash
   python build_exe.py
   ```

3. **Run the Application**:
   - Navigate to the `dist` folder
   - Double-click `NCAA_Sports_Tracker.exe`

### Running from Source (Without Building)

If you prefer to run the Python script directly:

```bash
python main_tkinter.py
```

## Usage Guide

### 1. Fetching Events

1. **Select Sport**: Choose from 12+ NCAA sports
2. **Select Division**: Division I, II, or III
3. **Set Date**: Enter date (MM/DD/YYYY) or use quick buttons (Today, Tomorrow, +7 Days)
4. **Optional Week**: Leave blank to use date, or enter week number
5. **Click "Fetch Events"**: Retrieves current events

### 2. Filtering Events

- **Top 25 Only**: Check this box to show only games with ranked teams
- **Conference Filter**: Enter conference name (e.g., "SEC", "Big Ten", "ACC")
- **Click "Apply Filters"**: Updates the display

### 3. Selecting Events

- **Click any event** in the "Available Events" section to add it to your selection
- Selected events appear in the "Selected Events" section below
- **Click on selected events** to remove them
- Use **"Clear Selected"** to remove all selections

### 4. Generating XML

**Preview XML**:
- Click "Preview XML" to see the formatted XML before saving
- Review the structure and content

**Save XML**:
- Click "💾 Save XML" to export your selected events
- Choose a location and filename
- The app remembers your last save directory for next time

### 5. Auto-Update Feature

For live event tracking:

1. **Select events** and **save XML** at least once
2. **Set update interval** (in seconds, minimum 5)
3. **Click "▶ Start Auto-Update"**
4. The app will automatically:
   - Fetch fresh data at your interval
   - Update scores and event status
   - Overwrite the XML file with current data
5. **Click "⏹ Stop"** to stop auto-updates

## XML Output Structure

```xml
<?xml version="1.0" ?>
<NCAASports>
  <Metadata>
    <Sport>Women's Basketball</Sport>
    <Division>Division I</Division>
    <Date>01/07/2026</Date>
    <TotalEvents>5</TotalEvents>
    <GeneratedAt>2026-01-07 15:30:00</GeneratedAt>
  </Metadata>
  <Contests count="5">
    <Contest id="12345">
      <Date>01/07/2026</Date>
      <Time>7:00 PM</Time>
      <Venue>Cameron Indoor Stadium</Venue>
      <HomeTeam>
        <Name>Duke Blue Devils</Name>
        <Score>75</Score>
        <Rank>3</Rank>
        <Conference>ACC</Conference>
        <Record>15-2</Record>
      </HomeTeam>
      <AwayTeam>
        <Name>North Carolina Tar Heels</Name>
        <Score>72</Score>
        <Rank>8</Rank>
        <Conference>ACC</Conference>
        <Record>13-4</Record>
      </AwayTeam>
    </Contest>
    <!-- More contests... -->
  </Contests>
</NCAASports>
```

## API Information

This application uses NCAA.com's public GraphQL API:
- **Endpoint**: `https://sdataprod.ncaa.com/`
- **Data includes**: Teams, scores, rankings, conferences, venues, broadcast info

### Supported Sport Codes

| Sport | Code |
|-------|------|
| Women's Basketball | WBB |
| Men's Basketball | MBB |
| Football | MFB |
| Baseball | MBA |
| Softball | WSB |
| Women's Volleyball | WVB |
| Men's Soccer | MSO |
| Women's Soccer | WSO |
| Women's Lacrosse | WLA |
| Men's Lacrosse | MLA |
| Ice Hockey | MIH |
| Wrestling | MWR |

## Configuration

The app stores settings in `config.json`:
- Last save directory
- Default update interval
- Sport/division preferences

This file is automatically created and updated.

## Troubleshooting

### "No events found"
- Check your internet connection
- Verify the date format (MM/DD/YYYY)
- Try a different date (some dates may have no scheduled games)
- Ensure the sport/division combination has scheduled events

### "Failed to fetch contests"
- Check internet connectivity
- NCAA API may be temporarily unavailable
- Try again in a few moments

### Build Issues
- Ensure Python 3.7+ is installed
- Run `python --version` to verify
- Install missing packages: `pip install requests pyinstaller`

### Auto-Update Not Working
- Make sure you've saved XML at least once first
- Check that the interval is at least 5 seconds
- Verify you have write permissions to the save directory

## File Structure

```
NCAA_Sports_Tracker/
├── main_tkinter.py       # Main application (standard tkinter)
├── ncaa_api.py           # NCAA API client
├── xml_generator.py      # XML generation logic
├── config_manager.py     # Configuration management
├── config.json           # User settings (auto-generated)
├── build_exe.py          # Build script
├── build.bat             # Windows build helper
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Technical Details

- **GUI Framework**: Tkinter (Python standard library - no external dependencies)
- **HTTP Client**: requests library
- **XML Generation**: xml.etree.ElementTree with pretty printing
- **Threading**: Used for async API calls and auto-updates
- **Packaging**: PyInstaller creates standalone executable

## License

This application is provided as-is for personal and educational use. NCAA and NCAA.com are trademarks of the National Collegiate Athletic Association.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the console output for error messages
3. Ensure you're using the latest version of Python and dependencies

## Version History

### v1.0.0 (2026-01-07)
- Initial release
- Multi-sport support with 12+ sports
- Advanced filtering (Top 25, conference, date, week)
- XML export with pretty printing
- Auto-update functionality
- Modern dark-themed UI
- Persistent configuration

---

**Enjoy tracking NCAA sports! 🏀🏈⚾**
