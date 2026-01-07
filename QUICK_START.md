# Quick Start Guide - NCAA Sports Tracker

## For Windows Users (Easiest Method)

### Step 1: Build the Executable
1. Open the project folder
2. **Double-click `build.bat`**
3. Wait for the build process to complete (1-2 minutes)

### Step 2: Run the Application
1. Open the `dist` folder
2. **Double-click `NCAA_Sports_Tracker.exe`**
3. The application will launch!

---

## For Mac/Linux Users

### Step 1: Install Python (if not already installed)
```bash
# Check if Python is installed
python3 --version

# If not installed, download from python.org
```

### Step 2: Install Dependencies
```bash
pip3 install requests pyinstaller
```

### Step 3: Build the Executable
```bash
python3 build_exe.py
```

### Step 4: Run
```bash
./dist/NCAA_Sports_Tracker
```

---

## 5-Minute Tutorial

### 1. Fetch Your First Events (30 seconds)
- Launch the app
- The default sport is "Women's Basketball"
- Click **"🔄 Fetch Events"**
- Events will appear in the main panel

### 2. Filter Events (15 seconds)
- Check **"Top 25 Only"** to see only ranked matchups
- Or type a conference name like "SEC" or "Big Ten"
- Click **"Apply Filters"**

### 3. Select Events (30 seconds)
- **Click on any event** in the top panel to add it
- It will appear in the "Selected Events" section below
- Click on selected events to remove them

### 4. Save XML (45 seconds)
- Click **"💾 Save XML"**
- Choose where to save your file
- Click Save
- Done! Your XML is ready

### 5. Enable Auto-Update (Optional - 30 seconds)
- Set update interval (e.g., 60 seconds)
- Click **"▶ Start Auto-Update"**
- The app will automatically refresh your XML with live data

---

## Common Use Cases

### Scenario 1: Track Today's Top 25 Games
1. Click "Today" button (sets today's date)
2. Check "Top 25 Only"
3. Click "Fetch Events"
4. Select the games you want
5. Save XML

### Scenario 2: Monitor a Conference Tournament
1. Enter the tournament dates
2. Type the conference name (e.g., "ACC")
3. Fetch and select all games
4. Save XML
5. Start auto-update with 60-second interval

### Scenario 3: Track Multiple Sports
1. Select first sport (e.g., "Men's Basketball")
2. Fetch and select events
3. Change to another sport (e.g., "Women's Basketball")
4. Fetch and select more events
5. All selections are kept!
6. Save one XML with all sports

### Scenario 4: Weekly Schedule
1. Enter week number (e.g., "5") instead of date
2. Leave date field as is
3. Fetch events
4. Gets all games for that week

---

## Tips & Tricks

### Date Selection
- **Today**: Instant button for current date
- **Tomorrow**: Next day's games
- **+7 Days**: Week ahead
- **Manual**: Type any date as MM/DD/YYYY

### Filtering
- Conference filter is case-insensitive ("sec" = "SEC")
- Partial matches work ("Big" finds "Big Ten", "Big 12")
- Use "All" to clear conference filter

### XML Management
- XML is pretty-printed (human-readable)
- Includes metadata (sport, date, event count)
- Auto-update overwrites the same file
- Each save remembers your directory

### Performance
- Fetching takes 1-3 seconds usually
- Auto-update runs in background (app stays responsive)
- Minimum update interval: 5 seconds
- Recommended interval: 30-60 seconds for live games

---

## Need Help?

**App won't launch?**
- Make sure Python 3.7+ is installed
- Try running `python main_tkinter.py` to see error messages

**No events found?**
- Check internet connection
- Try a different date (not all dates have games)
- Verify the sport/division combination

**Can't save XML?**
- Select at least one event first
- Check folder permissions
- Try saving to Desktop or Documents

**Auto-update not working?**
- Save XML manually first (at least once)
- Interval must be ≥5 seconds
- Check that the saved file still exists

---

## What's Next?

- Explore different sports (12+ available)
- Try different divisions (I, II, III)
- Set up auto-update for live game tracking
- Export multiple files for different dates/sports
- Share XML files with your team/application

**Enjoy your NCAA sports tracking! 🎉**
