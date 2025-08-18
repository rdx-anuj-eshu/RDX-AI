#!/bin/bash

# AI Assistant Launcher Script
# स्क्रिप्ट लॉन्चर AI सहायक

echo "🤖 AI Assistant - Self Dependent PC Manager"
echo "🤖 AI सहायक - स्व-निर्भर PC प्रबंधक"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed!"
    echo "Please install Python 3.7 or higher"
    echo "कृपया Python 3.7 या उससे ऊपर इंस्टॉल करें"
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.7"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python $required_version or higher is required!"
    echo "Current version: $python_version"
    echo "वर्तमान संस्करण: $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"
echo "✅ Python $python_version पाया गया"

# Launch the AI Assistant
echo "🚀 Launching AI Assistant..."
echo "🚀 AI सहायक लॉन्च हो रहा है..."

python3 start_ai_assistant.py

# Check exit status
if [ $? -eq 0 ]; then
    echo "✅ AI Assistant closed successfully"
    echo "✅ AI सहायक सफलतापूर्वक बंद हो गया"
else
    echo "❌ AI Assistant encountered an error"
    echo "❌ AI सहायक में त्रुटि आई"
fi