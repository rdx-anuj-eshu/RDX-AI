#!/usr/bin/env python3
"""
AI Assistant Startup Script
This script handles dependency installation and launches the AI Assistant
"""

import subprocess
import sys
import os
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    return True

def install_dependencies():
    """Install required dependencies"""
    print("🔧 Installing dependencies...")
    
    try:
        # Install pip if not available
        try:
            import pip
        except ImportError:
            print("Installing pip...")
            subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
        
        # Install required packages
        packages = [
            "speechrecognition",
            "pyttsx3", 
            "psutil",
            "pyautogui",
            "opencv-python",
            "numpy",
            "pillow"
        ]
        
        for package in packages:
            print(f"Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} installed successfully")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_system_requirements():
    """Check if system meets requirements"""
    print("🔍 Checking system requirements...")
    
    # Check OS
    system = platform.system()
    if system not in ["Linux", "Windows", "Darwin"]:
        print(f"⚠️  Warning: {system} is not officially supported")
    
    # Check microphone access
    try:
        import speech_recognition as sr
        mic = sr.Microphone()
        print("✅ Microphone access available")
    except Exception as e:
        print(f"❌ Microphone access failed: {e}")
        print("Voice features may not work properly")
    
    # Check display
    try:
        import tkinter
        print("✅ GUI support available")
    except Exception as e:
        print(f"❌ GUI support failed: {e}")
        return False
    
    return True

def launch_assistant():
    """Launch the AI Assistant"""
    print("🚀 Launching AI Assistant...")
    
    try:
        # Import and run the assistant
        from ai_assistant import AIAssistant
        
        assistant = AIAssistant()
        assistant.run()
        
    except ImportError as e:
        print(f"❌ Failed to import AI Assistant: {e}")
        print("Please ensure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Failed to launch AI Assistant: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🤖 AI Assistant - Self Dependent PC Manager")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check system requirements
    if not check_system_requirements():
        print("❌ System requirements not met")
        sys.exit(1)
    
    # Install dependencies if needed
    try:
        import speechrecognition
        import pyttsx3
        import psutil
        print("✅ All dependencies are already installed")
    except ImportError:
        if not install_dependencies():
            print("❌ Failed to install dependencies")
            sys.exit(1)
    
    # Launch the assistant
    if not launch_assistant():
        print("❌ Failed to launch AI Assistant")
        sys.exit(1)

if __name__ == "__main__":
    main()