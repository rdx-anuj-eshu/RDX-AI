# 🚀 Quick Start Guide - AI Assistant

## ⚡ Immediate Start (Linux/Mac)
```bash
# Make launcher executable
chmod +x launch.sh

# Run the AI Assistant
./launch.sh
```

## ⚡ Immediate Start (Windows)
```cmd
# Double click on launch.bat
# OR run in command prompt:
launch.bat
```

## 🔧 Manual Start
```bash
# Test system first
python3 test_system.py

# Start AI Assistant
python3 start_ai_assistant.py
```

## 🎯 What Happens Next

1. **System Check**: The startup script checks your system
2. **Dependencies**: Automatically installs required packages
3. **Launch**: Opens the AI Assistant GUI
4. **Start**: Click "Start AI Assistant" button
5. **Voice**: Speak commands or use manual controls

## 🎤 Quick Voice Commands

| Command | Action |
|---------|---------|
| "CPU" | Show system info |
| "Memory" | Clean up RAM |
| "Disk" | Clean up storage |
| "Optimize" | Optimize system |
| "Status" | Show current status |
| "Help" | Show help |

## ⚠️ First Time Setup

- **Microphone**: Allow microphone access when prompted
- **Internet**: Required for voice recognition
- **Permissions**: May need admin rights for system optimization

## 🆘 If Something Goes Wrong

1. **Check logs**: Look at `ai_assistant.log`
2. **Run test**: `python3 test_system.py`
3. **Reinstall**: Delete and re-clone the repository
4. **Manual install**: Install dependencies manually

## 📱 Features Available Immediately

- ✅ System monitoring
- ✅ Voice recognition (Hindi/English)
- ✅ Automatic optimization
- ✅ Memory management
- ✅ Disk cleanup
- ✅ Process management

## 🔄 Auto-Start (Optional)

To start AI Assistant automatically on boot:

**Linux:**
```bash
# Copy desktop file
cp ai-assistant.desktop ~/.local/share/applications/

# Or add to startup applications
./launch.sh &
```

**Windows:**
- Copy `launch.bat` to Startup folder
- Or create a scheduled task

---

**🎉 You're all set! The AI Assistant will now manage your PC automatically!**