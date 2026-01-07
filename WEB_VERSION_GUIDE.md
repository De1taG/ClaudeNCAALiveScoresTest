# NCAA Sports Tracker - Web Version Guide 🌐

Run the NCAA Sports Tracker directly in your web browser - no executable needed!

## Quick Start

### Windows
1. **Double-click `run_web.bat`**
2. Browser opens automatically to http://localhost:8501
3. Start tracking!

### Mac/Linux
1. **Run `./run_web.sh`** (or `python3 run_web.py`)
2. Browser opens automatically to http://localhost:8501
3. Start tracking!

---

## Installation

### First Time Setup

```bash
# Install dependencies (only needed once)
pip install streamlit requests

# Or use the requirements file
pip install -r requirements_web.txt
```

### Running the App

**Option 1: Quick Launch Scripts**
- Windows: Double-click `run_web.bat`
- Mac/Linux: `./run_web.sh`

**Option 2: Direct Command**
```bash
streamlit run app_streamlit.py
```

**Option 3: Python Launcher**
```bash
python run_web.py
```

---

## Features

### 🎯 Everything from the Desktop Version, Plus:

✅ **Access from Any Browser** - Chrome, Firefox, Safari, Edge
✅ **No Installation Required** - Just Python + Streamlit
✅ **Modern Web Interface** - Responsive design
✅ **Live Auto-Refresh** - Automatic data updates
✅ **Direct Download** - XML downloads right from browser
✅ **Mobile-Friendly** - Works on tablets and phones
✅ **Real-Time Updates** - See changes instantly

### 🌟 Web-Specific Features:

- **One-Click Add/Remove** - Buttons for each event
- **Live Statistics** - Real-time event counts
- **Inline Preview** - See XML before downloading
- **Quick Filters** - Instant filtering (no reload needed)
- **Auto-Refresh Mode** - Continuous data updates
- **Download Manager** - Browser handles file saving

---

## User Interface Guide

### Sidebar (Left Panel)

**⚙️ Filters & Settings**
- Sport selector dropdown
- Division selector dropdown
- Date picker with quick buttons (Today, Tomorrow, +7 Days)
- Week number input (optional)
- Top 25 filter checkbox
- Conference filter text box
- **🔄 Fetch Events** button (blue, primary action)

**🔄 Auto-Refresh**
- Enable/disable toggle
- Interval slider (10-300 seconds)
- Status indicator

### Main Panel (Center)

**📋 Available Events**
- Statistics bar (Total, Filtered, Selected counts)
- Event cards with full details:
  - Teams with rankings
  - Date and time
  - Conference information
  - Venue location
  - TV broadcast info
  - Team records
- **➕ Add** button (or **✓ Added** if selected)

### Right Panel

**✅ Selected Events**
- Count of selected events
- **🗑️ Clear All** button
- List of selected events with remove buttons
- **👁️ Preview XML** button
- **💾 Download XML** button (primary)
- **⬇️ Download XML File** button (after generation)

---

## Step-by-Step Tutorial

### 1️⃣ Launch the App (30 seconds)

```bash
# Windows
run_web.bat

# Mac/Linux
./run_web.sh
```

Browser opens to http://localhost:8501

### 2️⃣ Fetch Your First Events (1 minute)

1. In the sidebar, select:
   - **Sport**: Women's Basketball (default)
   - **Division**: Division I (default)
2. Click **"Today"** button for today's date
3. Click **"🔄 Fetch Events"** button
4. Events appear in the center panel!

### 3️⃣ Filter Events (30 seconds)

1. Check **"Top 25 Only"** to see ranked matchups
2. Or type **"SEC"** in Conference filter
3. Events automatically filter

### 4️⃣ Select Events (1 minute)

1. Browse the event cards
2. Click **"➕ Add"** on events you want
3. Watch them appear in the right panel
4. Click **"❌"** to remove any
5. Use **"🗑️ Clear All"** to start over

### 5️⃣ Generate & Download XML (1 minute)

1. Click **"👁️ Preview XML"** to see the output
2. Review the XML structure
3. Click **"💾 Download XML"** button
4. Click **"⬇️ Download XML File"**
5. Browser saves the file!

### 6️⃣ Enable Auto-Refresh (Optional)

1. Check **"Enable Auto-Refresh"** in sidebar
2. Set interval (e.g., 60 seconds)
3. App automatically fetches fresh data
4. Perfect for live game tracking!

**Total time: ~5 minutes to master!**

---

## Use Cases

### Scenario 1: Track Today's Top Games
```
1. Launch app
2. Click "Today" → Check "Top 25 Only" → Fetch Events
3. Add all games → Download XML
4. Done in under 2 minutes!
```

### Scenario 2: Monitor Conference Tournament
```
1. Select tournament date
2. Type conference name (e.g., "Big Ten")
3. Fetch → Add all → Download
4. Enable Auto-Refresh (60 sec interval)
5. XML updates automatically with live scores!
```

### Scenario 3: Multi-Sport Schedule
```
1. Select "Men's Basketball" → Fetch → Add games
2. Change to "Women's Basketball" → Fetch → Add games
3. Change to "Football" → Fetch → Add games
4. All sports in one XML!
```

### Scenario 4: Weekly Preview
```
1. Enter week number (e.g., "10")
2. Leave date blank
3. Fetch Events
4. Get entire week's schedule at once
```

---

## Advanced Features

### Auto-Refresh Mode

Perfect for live event tracking:

1. **Enable Auto-Refresh** in sidebar
2. **Set interval** (recommended: 60-120 seconds)
3. App fetches fresh data automatically
4. Scores and status update in real-time
5. Leave browser tab open and it keeps updating!

**Best Practices:**
- Use 60+ second intervals (avoid overloading API)
- Close other tabs to save resources
- Disable when not actively tracking

### Keyboard Shortcuts

- **Ctrl/Cmd + R**: Refresh page
- **Ctrl/Cmd + S**: Downloads happen automatically
- **Esc**: Close preview/dialogs

### Multi-Tab Support

You can run multiple instances:
- Different sports in different tabs
- Different dates simultaneously
- Compare divisions side-by-side

---

## Comparison: Web vs Desktop

| Feature | Web Version | Desktop Version |
|---------|-------------|-----------------|
| **Installation** | Streamlit only | Full build process |
| **Launch Speed** | ~5 seconds | Instant (exe) |
| **Access** | Any browser | Windows only |
| **Updates** | Automatic | Rebuild required |
| **File Size** | ~10 MB | ~50-100 MB exe |
| **Mobile Support** | ✅ Yes | ❌ No |
| **Multi-User** | ✅ Yes (shared server) | ❌ No |
| **Offline Use** | ❌ No (needs server) | ✅ Yes |

**Recommendation:**
- **Web version**: Quick testing, development, mobile access
- **Desktop version**: Production use, offline capability, distribution

---

## Troubleshooting

### App Won't Start

**Error: "Streamlit not found"**
```bash
pip install streamlit
```

**Error: "Port already in use"**
```bash
# Use different port
streamlit run app_streamlit.py --server.port 8502
```

**Error: "Module not found: requests"**
```bash
pip install requests
```

### No Events Showing

1. Check internet connection
2. Verify date has scheduled games
3. Try different sport/division
4. Check browser console for errors (F12)

### Download Not Working

1. Check browser download settings
2. Allow pop-ups if blocked
3. Try "Preview XML" then copy/paste
4. Check browser's download folder

### Auto-Refresh Not Working

1. Make sure checkbox is enabled
2. Wait full interval duration
3. Check if events were fetched first
4. Browser tab must stay active

### Slow Performance

1. Close other browser tabs
2. Clear browser cache (Ctrl+Shift+Del)
3. Reduce auto-refresh interval
4. Restart the Streamlit server

---

## Tips & Tricks

### Productivity Hacks

1. **Bookmark it**: http://localhost:8501
2. **Keyboard navigation**: Tab through fields
3. **Quick dates**: Use Today/Tomorrow buttons
4. **Batch operations**: Add multiple events before downloading
5. **Preview first**: Always preview before download

### Best Practices

1. **Start fresh**: Clear selected events between queries
2. **Save often**: Download XML frequently
3. **Name files**: Use descriptive filenames
4. **Check filters**: Review active filters regularly
5. **Auto-refresh wisely**: Use 60+ second intervals

### Power User Features

1. **URL Parameters**: Bookmark specific sports/divisions
2. **Multi-Window**: Compare different dates
3. **Export workflow**: Fetch → Filter → Select → Download
4. **Batch downloads**: Generate multiple XMLs for different sports

---

## System Requirements

### Minimum
- Python 3.7+
- 100 MB free RAM
- Modern web browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- Internet connection

### Recommended
- Python 3.9+
- 500 MB free RAM
- Chrome or Edge (best compatibility)
- 10+ Mbps internet

### Browser Support
- ✅ Chrome 90+ (Recommended)
- ✅ Edge 90+ (Recommended)
- ✅ Firefox 88+
- ✅ Safari 14+
- ⚠️ IE 11 (Not supported)

---

## Running on Network

Want to share with your team?

### Local Network Access

```bash
streamlit run app_streamlit.py --server.address 0.0.0.0
```

Others can access at: `http://YOUR_IP:8501`

### Find Your IP

**Windows:**
```cmd
ipconfig
```

**Mac/Linux:**
```bash
ifconfig
```

Look for your local IP (e.g., 192.168.1.100)

---

## Screenshots & Navigation

### Main Screen Layout

```
┌─────────────────┬──────────────────────────┬─────────────┐
│   SIDEBAR       │     AVAILABLE EVENTS     │  SELECTED   │
│                 │                          │   EVENTS    │
│  [Sport ▼]      │  ┌────────────────────┐  │             │
│  [Division ▼]   │  │ Event Card         │  │  1. Game 1  │
│                 │  │ Teams, Date, Venue │  │  2. Game 2  │
│  Date: [____]   │  │  [➕ Add]          │  │  3. Game 3  │
│  [Today] [+7]   │  └────────────────────┘  │             │
│                 │                          │  [Clear All]│
│  Top25: [✓]     │  ┌────────────────────┐  │             │
│  Conf: [___]    │  │ Event Card         │  │  [Preview]  │
│                 │  │  [✓ Added]         │  │  [Download] │
│  [Fetch Events] │  └────────────────────┘  │             │
└─────────────────┴──────────────────────────┴─────────────┘
```

---

## FAQ

**Q: Can I run this on my phone?**
A: Yes! If you run it on your computer, you can access from your phone's browser using your computer's IP address.

**Q: Does it save my preferences?**
A: Session state is maintained while the app runs. Close the browser/server to reset.

**Q: Can multiple people use it?**
A: Yes! If you run on a server and share the URL, multiple users can access simultaneously.

**Q: How do I update the app?**
A: Just update the Python files and restart the server.

**Q: Can I customize the interface?**
A: Yes! Edit `app_streamlit.py` to modify colors, layout, etc.

**Q: Is my data saved?**
A: Only the XML you download is saved. The app doesn't store data permanently.

---

## Next Steps

1. ✅ Launch the app with `run_web.bat` or `run_web.sh`
2. ✅ Follow the 5-minute tutorial above
3. ✅ Explore different sports and divisions
4. ✅ Try the auto-refresh feature
5. ✅ Generate your first XML!

**Enjoy the web version! 🎉**

For desktop version, see: `README.md`
For quick start: `QUICK_START.md`
For installation: `INSTALLATION.txt`
