# 🎯 START HERE - NCAA Sports Tracker

Welcome! You now have **TWO ways** to run this application:

---

## 🌐 WEB VERSION (Recommended for Testing!)

**The easiest way to get started - runs in your browser!**

### Quick Start (30 seconds)

```bash
# Step 1: Install Streamlit (one-time only)
pip install streamlit requests

# Step 2: Run the app
streamlit run app_streamlit.py
```

**That's it!** Browser opens automatically to http://localhost:8501

### Or Use Quick Launch

- **Windows**: Double-click `run_web.bat`
- **Mac/Linux**: Double-click `run_web.sh` or run `./run_web.sh`

### Why Choose Web Version?

✅ **No build process** - Just run it!
✅ **Works everywhere** - Windows, Mac, Linux
✅ **Modern interface** - Beautiful, responsive design
✅ **Mobile-friendly** - Works on tablets and phones
✅ **Easy updates** - Just edit the file and refresh
✅ **Perfect for testing** - See changes instantly

### Full Documentation

📖 **[WEB_VERSION_GUIDE.md](WEB_VERSION_GUIDE.md)** - Complete guide with tutorials
📄 **[WEB_QUICK_START.txt](WEB_QUICK_START.txt)** - Quick reference

---

## 🖥️ DESKTOP VERSION (For Distribution)

**Build a standalone .exe file for Windows**

### Quick Build

```bash
# Windows - Just double-click this file:
build.bat

# Or manually:
pip install pyinstaller requests
python build_exe.py
```

The .exe will be in the `dist` folder.

### Why Choose Desktop Version?

✅ **Standalone executable** - No Python needed on target machine
✅ **Offline capable** - Runs without server
✅ **Professional** - Distribute as .exe
✅ **Faster startup** - No server initialization

### Full Documentation

📖 **[README.md](README.md)** - Complete documentation
📄 **[INSTALLATION.txt](INSTALLATION.txt)** - Build instructions
📝 **[QUICK_START.md](QUICK_START.md)** - User guide

---

## 📊 Feature Comparison

| Feature | Web Version | Desktop Version |
|---------|-------------|-----------------|
| **Setup Time** | 30 seconds | 2-3 minutes |
| **Platform** | Any (Win/Mac/Linux) | Windows only |
| **Browser Access** | ✅ Yes | ❌ No |
| **Mobile Support** | ✅ Yes | ❌ No |
| **Offline Use** | ❌ No | ✅ Yes |
| **File Size** | ~10 MB | ~50-100 MB |
| **Updates** | Edit & refresh | Rebuild required |
| **Distribution** | Share code | Share .exe |

---

## 🎓 What Does It Do?

This application helps you:

1. **Fetch NCAA Sports Data** from NCAA.com's official API
2. **Filter Events** by sport, division, date, conference, Top 25
3. **Select Events** to include in your export
4. **Generate XML** with pretty printing
5. **Auto-Update** XML files with live scores

### Supported Sports (12+)

- 🏀 Women's & Men's Basketball
- 🏈 Football
- ⚾ Baseball & Softball
- 🏐 Volleyball
- ⚽ Soccer (Men's & Women's)
- 🥍 Lacrosse (Men's & Women's)
- 🏒 Ice Hockey
- 🤼 Wrestling

---

## 🚀 Recommended Quick Start

**For first-time testing:**

1. Run the **WEB VERSION** (fastest way to try it)
2. Play around with the interface
3. Try fetching events for different sports
4. Generate and download some XML files

**Once satisfied:**

1. Build the **DESKTOP VERSION** if you need:
   - A standalone executable
   - Offline capability
   - Distribution to others

---

## 📁 Project Files Overview

```
📦 NCAA_Sports_Tracker/
│
├── 🌐 WEB VERSION FILES
│   ├── app_streamlit.py         ← Main web app
│   ├── run_web.py               ← Python launcher
│   ├── run_web.bat              ← Windows quick-start
│   └── run_web.sh               ← Mac/Linux quick-start
│
├── 🖥️ DESKTOP VERSION FILES
│   ├── main_tkinter.py          ← Main desktop app
│   ├── build_exe.py             ← Build script
│   └── build.bat                ← Windows builder
│
├── ⚙️ CORE FILES (Used by both)
│   ├── ncaa_api.py              ← API client
│   ├── xml_generator.py         ← XML creator
│   └── config_manager.py        ← Settings
│
└── 📚 DOCUMENTATION
    ├── START_HERE.md            ← You are here!
    ├── README.md                ← Main documentation
    ├── WEB_VERSION_GUIDE.md     ← Web guide
    ├── QUICK_START.md           ← Desktop guide
    └── INSTALLATION.txt         ← Install help
```

---

## 💡 Common Questions

**Q: Which version should I use?**
A: Start with the **web version** for quick testing. Build the **desktop version** if you need a standalone .exe.

**Q: Can I use both?**
A: Absolutely! They both use the same core files and can coexist.

**Q: Which is better?**
A:
- Web = Easier, faster, more flexible
- Desktop = More professional, distributable, offline

**Q: Do I need to install anything?**
A:
- Web: Just `pip install streamlit requests`
- Desktop: Python (for building), nothing on target machine after build

**Q: Can I run this on Mac/Linux?**
A:
- Web: ✅ Yes! Works perfectly
- Desktop: Only for building. The .exe is Windows-only.

---

## 🎯 Your Next Steps

### Option 1: Quick Test (Web Version)

```bash
pip install streamlit requests
streamlit run app_streamlit.py
```

**Time: 30 seconds** | Browser opens → Start using!

### Option 2: Build Executable (Desktop Version)

```bash
# Windows
run build.bat

# Mac/Linux (for building)
pip install pyinstaller requests
python build_exe.py
```

**Time: 2-3 minutes** | Creates .exe in `dist` folder

---

## 📞 Need Help?

1. **Web Version Issues**: See [WEB_VERSION_GUIDE.md](WEB_VERSION_GUIDE.md)
2. **Desktop Version Issues**: See [INSTALLATION.txt](INSTALLATION.txt)
3. **General Questions**: See [README.md](README.md)
4. **Quick Reference**: See [QUICK_START.md](QUICK_START.md)

---

## ✨ Ready to Start?

Pick your version and let's go! 🚀

**Recommended**: Start with web version for instant gratification!

```bash
streamlit run app_streamlit.py
```

Enjoy tracking NCAA sports! 🏀🏈⚾
