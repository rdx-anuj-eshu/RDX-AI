@echo off
chcp 65001 >nul
title AI Assistant - Self Dependent PC Manager

echo 🤖 AI Assistant - Self Dependent PC Manager
echo 🤖 AI सहायक - स्व-निर्भर PC प्रबंधक
echo ==========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed!
    echo Please install Python 3.7 or higher
    echo कृपया Python 3.7 या उससे ऊपर इंस्टॉल करें
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✅ Python %python_version% detected
echo ✅ Python %python_version% पाया गया

REM Launch the AI Assistant
echo 🚀 Launching AI Assistant...
echo 🚀 AI सहायक लॉन्च हो रहा है...

python start_ai_assistant.py

REM Check exit status
if errorlevel 1 (
    echo ❌ AI Assistant encountered an error
    echo ❌ AI सहायक में त्रुटि आई
) else (
    echo ✅ AI Assistant closed successfully
    echo ✅ AI सहायक सफलतापूर्वक बंद हो गया
)

pause