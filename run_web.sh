#!/bin/bash

echo "========================================"
echo "NCAA Sports Tracker - Web Version"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3 from your package manager"
    exit 1
fi

echo "Starting web application..."
echo ""
echo "The app will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

python3 run_web.py
