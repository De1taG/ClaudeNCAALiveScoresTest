"""
Build script for creating NCAA Sports Tracker executable
"""
import os
import sys
import subprocess


def build_executable():
    """Build the executable using PyInstaller"""

    print("=" * 60)
    print("NCAA Sports Tracker - Build Script")
    print("=" * 60)
    print()

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller found")
    except ImportError:
        print("✗ PyInstaller not found")
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Build command
    build_command = [
        "pyinstaller",
        "--name=NCAA_Sports_Tracker",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        "main_tkinter.py"
    ]

    # Add icon if available
    if os.path.exists("icon.ico"):
        build_command.extend(["--icon=icon.ico"])

    # Add data files
    build_command.extend([
        "--add-data", "config.json:.",
    ])

    print("\nBuilding executable...")
    print(f"Command: {' '.join(build_command)}")
    print()

    try:
        subprocess.check_call(build_command)
        print("\n" + "=" * 60)
        print("✓ Build completed successfully!")
        print("=" * 60)
        print(f"\nExecutable location: {os.path.join('dist', 'NCAA_Sports_Tracker.exe')}")
        print("\nYou can now run the application by double-clicking NCAA_Sports_Tracker.exe")
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print("✗ Build failed!")
        print("=" * 60)
        print(f"Error: {e}")
        return False

    return True


if __name__ == "__main__":
    success = build_executable()
    sys.exit(0 if success else 1)
