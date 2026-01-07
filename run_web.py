"""
Launch script for NCAA Sports Tracker Web Version
"""
import subprocess
import sys
import os

def check_streamlit():
    """Check if Streamlit is installed"""
    try:
        import streamlit
        return True
    except ImportError:
        return False

def install_streamlit():
    """Install Streamlit"""
    print("Installing Streamlit...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        print("✓ Streamlit installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install Streamlit")
        return False

def run_app():
    """Run the Streamlit app"""
    print("\n" + "="*60)
    print("NCAA Sports Tracker - Web Version")
    print("="*60)
    print()

    # Check if Streamlit is installed
    if not check_streamlit():
        print("Streamlit is not installed.")
        response = input("Would you like to install it now? (y/n): ")
        if response.lower() == 'y':
            if not install_streamlit():
                print("\nPlease install Streamlit manually:")
                print("pip install streamlit")
                return False
        else:
            print("\nPlease install Streamlit manually:")
            print("pip install streamlit")
            return False

    # Run the app
    print("\nStarting NCAA Sports Tracker...")
    print("\nThe app will open in your web browser automatically.")
    print("If it doesn't, navigate to: http://localhost:8501")
    print("\nPress Ctrl+C to stop the server.")
    print("="*60)
    print()

    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "app_streamlit.py",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        print("Thank you for using NCAA Sports Tracker!")

    return True

if __name__ == "__main__":
    run_app()
