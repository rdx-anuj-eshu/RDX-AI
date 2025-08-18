#!/usr/bin/env python3
"""
Test Script for AI Assistant
AI सहायक के लिए परीक्षण स्क्रिप्ट
"""

import sys
import os
import platform

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required. Current:", sys.version)
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - Compatible")
    return True

def test_imports():
    """Test if required modules can be imported"""
    print("\n📦 Testing module imports...")
    
    modules = [
        ("tkinter", "GUI Framework"),
        ("threading", "Threading Support"),
        ("json", "JSON Support"),
        ("logging", "Logging Support"),
        ("datetime", "DateTime Support"),
        ("os", "OS Interface"),
        ("sys", "System Interface"),
        ("platform", "Platform Info")
    ]
    
    all_imported = True
    
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - {description}")
        except ImportError as e:
            print(f"❌ {module_name} - {description} - {e}")
            all_imported = False
    
    return all_imported

def test_optional_modules():
    """Test optional modules that will be installed"""
    print("\n🔧 Testing optional modules...")
    
    optional_modules = [
        ("speech_recognition", "Voice Recognition"),
        ("pyttsx3", "Text-to-Speech"),
        ("psutil", "System Monitoring"),
        ("pyautogui", "GUI Automation"),
        ("cv2", "Computer Vision"),
        ("numpy", "Numerical Computing"),
        ("PIL", "Image Processing")
    ]
    
    available_modules = []
    
    for module_name, description in optional_modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - {description} (Already installed)")
            available_modules.append(module_name)
        except ImportError:
            print(f"⏳ {module_name} - {description} (Will be installed)")
    
    return available_modules

def test_system_info():
    """Test system information gathering"""
    print("\n💻 Testing system information...")
    
    try:
        print(f"✅ OS: {platform.system()} {platform.release()}")
        print(f"✅ Architecture: {platform.machine()}")
        print(f"✅ Python: {platform.python_version()}")
        print(f"✅ Executable: {sys.executable}")
        print(f"✅ Working Directory: {os.getcwd()}")
        return True
    except Exception as e:
        print(f"❌ System info test failed: {e}")
        return False

def test_file_access():
    """Test file system access"""
    print("\n📁 Testing file system access...")
    
    try:
        # Test current directory
        current_dir = os.getcwd()
        print(f"✅ Current directory: {current_dir}")
        
        # Test if we can list files
        files = os.listdir(current_dir)
        print(f"✅ Directory listing: {len(files)} files found")
        
        # Test if we can create a test file
        test_file = "test_access.tmp"
        with open(test_file, 'w') as f:
            f.write("test")
        
        if os.path.exists(test_file):
            os.remove(test_file)
            print("✅ File creation/deletion: Working")
        
        return True
    except Exception as e:
        print(f"❌ File system test failed: {e}")
        return False

def test_gui_support():
    """Test GUI support"""
    print("\n🖥️ Testing GUI support...")
    
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Test basic GUI functionality
        label = tk.Label(root, text="Test")
        label.pack()
        label.destroy()
        
        root.destroy()
        print("✅ GUI support: Working")
        return True
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False

def run_all_tests():
    """Run all system tests"""
    print("🧪 AI Assistant System Test")
    print("=" * 40)
    
    tests = [
        ("Python Version", test_python_version),
        ("Module Imports", test_imports),
        ("Optional Modules", test_optional_modules),
        ("System Information", test_system_info),
        ("File System Access", test_file_access),
        ("GUI Support", test_gui_support)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Results Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for AI Assistant.")
        print("🚀 You can now run: python3 start_ai_assistant.py")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        print("🔧 Run the startup script to install missing dependencies.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)