#!/usr/bin/env python3
"""
Launch script for the Streamlit Blog Writing App
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        import streamlit
        print("✅ Streamlit already installed")
    except ImportError:
        print("📦 Installing Streamlit...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        print("✅ Streamlit installed successfully")

def launch_app():
    """Launch the Streamlit app"""
    print("🚀 Starting AI Blog Writing Team Web Interface...")
    print("📱 The app will open in your default browser")
    print("🔗 Access URL: http://localhost:8501")
    print("\n💡 Press Ctrl+C to stop the app")
    print("="*50)
    
    # Change to the project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Launch Streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])

if __name__ == "__main__":
    install_requirements()
    launch_app()