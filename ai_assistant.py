import speech_recognition as sr
import pyttsx3
import psutil
import pyautogui
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import json
import os
import sys
import subprocess
import platform
import logging
from datetime import datetime

class AIAssistant:
    def __init__(self):
        self.setup_logging()
        self.setup_voice()
        self.setup_system_monitoring()
        self.setup_automation_rules()
        self.is_running = False
        self.voice_enabled = True
        self.auto_mode = True
        
        # Initialize GUI
        self.setup_gui()
        
        # Start background monitoring
        self.start_background_monitoring()
    
    def setup_logging(self):
        """Setup logging for the AI system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ai_assistant.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("AI Assistant initialized")
    
    def setup_voice(self):
        """Setup voice recognition and speech synthesis"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Setup text-to-speech
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.8)
            
            # Get available voices and set Hindi voice if available
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'hindi' in voice.name.lower() or 'indian' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            
            self.logger.info("Voice system initialized successfully")
        except Exception as e:
            self.logger.error(f"Voice setup failed: {e}")
            self.voice_enabled = False
    
    def setup_system_monitoring(self):
        """Setup system monitoring parameters"""
        self.cpu_threshold = 80.0
        self.memory_threshold = 85.0
        self.disk_threshold = 90.0
        self.temperature_threshold = 80.0
        
        self.logger.info("System monitoring initialized")
    
    def setup_automation_rules(self):
        """Setup automation rules for PC management"""
        self.automation_rules = {
            'high_cpu': {
                'action': 'optimize_processes',
                'threshold': 80.0,
                'enabled': True
            },
            'low_memory': {
                'action': 'cleanup_memory',
                'threshold': 85.0,
                'enabled': True
            },
            'disk_full': {
                'action': 'cleanup_disk',
                'threshold': 90.0,
                'enabled': True
            },
            'idle_time': {
                'action': 'power_save',
                'threshold': 300,  # 5 minutes
                'enabled': True
            }
        }
        self.logger.info("Automation rules loaded")
    
    def setup_gui(self):
        """Setup the main GUI interface"""
        self.root = tk.Tk()
        self.root.title("AI Assistant - Self Dependent PC Manager")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TLabel', background='#2b2b2b', foreground='white')
        style.configure('TButton', background='#4a4a4a', foreground='white')
        
        self.create_gui_elements()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_gui_elements(self):
        """Create GUI elements"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🤖 AI Assistant - Self Dependent PC Manager", 
            font=("Arial", 16, "bold"),
            bg='#2b2b2b',
            fg='#00ff00'
        )
        title_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="System Status", padding=10)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # System info labels
        self.cpu_label = tk.Label(status_frame, text="CPU: Loading...", bg='#2b2b2b', fg='white')
        self.cpu_label.pack(anchor=tk.W)
        
        self.memory_label = tk.Label(status_frame, text="Memory: Loading...", bg='#2b2b2b', fg='white')
        self.memory_label.pack(anchor=tk.W)
        
        self.disk_label = tk.Label(status_frame, text="Disk: Loading...", bg='#2b2b2b', fg='white')
        self.disk_label.pack(anchor=tk.W)
        
        # Control frame
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Voice control
        self.voice_var = tk.BooleanVar(value=self.voice_enabled)
        voice_check = tk.Checkbutton(
            control_frame, 
            text="Voice Recognition", 
            variable=self.voice_var,
            bg='#2b2b2b',
            fg='white',
            selectcolor='#4a4a4a',
            command=self.toggle_voice
        )
        voice_check.pack(anchor=tk.W)
        
        # Auto mode control
        self.auto_var = tk.BooleanVar(value=self.auto_mode)
        auto_check = tk.Checkbutton(
            control_frame, 
            text="Auto Management Mode", 
            variable=self.auto_var,
            bg='#2b2b2b',
            fg='white',
            selectcolor='#4a4a4a',
            command=self.toggle_auto_mode
        )
        auto_check.pack(anchor=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.start_button = tk.Button(
            button_frame,
            text="Start AI Assistant",
            command=self.start_assistant,
            bg='#4a4a4a',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=5
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = tk.Button(
            button_frame,
            text="Stop AI Assistant",
            command=self.stop_assistant,
            bg='#8b0000',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=5,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Log text area
        self.log_text = tk.Text(
            log_frame,
            height=10,
            bg='#1e1e1e',
            fg='#00ff00',
            font=("Consolas", 10)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for log
        log_scrollbar = tk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=log_scrollbar.set)
        
        # Voice input frame
        voice_frame = ttk.LabelFrame(main_frame, text="Voice Commands", padding=10)
        voice_frame.pack(fill=tk.X)
        
        self.voice_status_label = tk.Label(
            voice_frame, 
            text="Voice: Ready", 
            bg='#2b2b2b', 
            fg='#00ff00'
        )
        self.voice_status_label.pack(side=tk.LEFT)
        
        self.listen_button = tk.Button(
            voice_frame,
            text="🎤 Listen",
            command=self.start_voice_listening,
            bg='#4a4a4a',
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=5
        )
        self.listen_button.pack(side=tk.RIGHT)
    
    def log_message(self, message):
        """Add message to log display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Limit log size
        if int(self.log_text.index(tk.END).split('.')[0]) > 1000:
            self.log_text.delete("1.0", "2.0")
        
        self.logger.info(message)
    
    def start_assistant(self):
        """Start the AI assistant"""
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            
            # Start voice recognition in background
            if self.voice_enabled:
                self.voice_thread = threading.Thread(target=self.voice_recognition_loop, daemon=True)
                self.voice_thread.start()
            
            self.log_message("AI Assistant started successfully!")
            self.speak("AI Assistant started. I'm ready to help you manage your PC.")
    
    def stop_assistant(self):
        """Stop the AI assistant"""
        if self.is_running:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            
            self.log_message("AI Assistant stopped.")
            self.speak("AI Assistant stopped.")
    
    def toggle_voice(self):
        """Toggle voice recognition on/off"""
        self.voice_enabled = self.voice_var.get()
        if self.voice_enabled:
            self.log_message("Voice recognition enabled")
        else:
            self.log_message("Voice recognition disabled")
    
    def toggle_auto_mode(self):
        """Toggle automatic management mode"""
        self.auto_mode = self.auto_var.get()
        if self.auto_mode:
            self.log_message("Auto management mode enabled")
        else:
            self.log_message("Auto management mode disabled")
    
    def speak(self, text):
        """Convert text to speech"""
        if self.voice_enabled:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                self.logger.error(f"Speech synthesis failed: {e}")
    
    def voice_recognition_loop(self):
        """Main voice recognition loop"""
        while self.is_running and self.voice_enabled:
            try:
                with self.microphone as source:
                    self.voice_status_label.config(text="Voice: Listening...", fg='#ffff00')
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                self.voice_status_label.config(text="Voice: Processing...", fg='#ffa500')
                
                # Recognize speech
                text = self.recognizer.recognize_google(audio, language='hi-IN')
                if text:
                    self.log_message(f"Voice input: {text}")
                    self.process_voice_command(text)
                
                self.voice_status_label.config(text="Voice: Ready", fg='#00ff00')
                
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                self.log_message(f"Voice recognition error: {e}")
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Voice recognition error: {e}")
                time.sleep(1)
    
    def start_voice_listening(self):
        """Start voice listening manually"""
        if self.voice_enabled:
            threading.Thread(target=self.manual_voice_listen, daemon=True).start()
    
    def manual_voice_listen(self):
        """Manual voice listening for button press"""
        try:
            with self.microphone as source:
                self.voice_status_label.config(text="Voice: Listening...", fg='#ffff00')
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            self.voice_status_label.config(text="Voice: Processing...", fg='#ffa500')
            
            text = self.recognizer.recognize_google(audio, language='hi-IN')
            if text:
                self.log_message(f"Voice input: {text}")
                self.process_voice_command(text)
            
            self.voice_status_label.config(text="Voice: Ready", fg='#00ff00')
            
        except Exception as e:
            self.voice_status_label.config(text="Voice: Error", fg='#ff0000')
            self.log_message(f"Voice listening failed: {e}")
            time.sleep(2)
            self.voice_status_label.config(text="Voice: Ready", fg='#00ff00')
    
    def process_voice_command(self, command):
        """Process voice commands"""
        command = command.lower()
        
        if 'cpu' in command or 'processor' in command:
            self.show_system_info()
        elif 'memory' in command or 'ram' in command:
            self.cleanup_memory()
        elif 'disk' in command or 'storage' in command:
            self.cleanup_disk()
        elif 'optimize' in command or 'performance' in command:
            self.optimize_system()
        elif 'status' in command or 'condition' in command:
            self.show_system_status()
        elif 'help' in command or 'help' in command:
            self.show_help()
        else:
            self.speak("Command not recognized. Please try again.")
            self.log_message(f"Unknown voice command: {command}")
    
    def start_background_monitoring(self):
        """Start background system monitoring"""
        self.monitoring_thread = threading.Thread(target=self.system_monitoring_loop, daemon=True)
        self.monitoring_thread.start()
    
    def system_monitoring_loop(self):
        """Continuous system monitoring loop"""
        while True:
            try:
                if self.auto_mode and self.is_running:
                    self.check_system_health()
                    self.update_system_display()
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                self.logger.error(f"System monitoring error: {e}")
                time.sleep(10)
    
    def check_system_health(self):
        """Check system health and take action if needed"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > self.cpu_threshold:
                self.log_message(f"High CPU usage detected: {cpu_percent}%")
                if self.automation_rules['high_cpu']['enabled']:
                    self.optimize_processes()
            
            # Memory usage
            memory = psutil.virtual_memory()
            if memory.percent > self.memory_threshold:
                self.log_message(f"High memory usage detected: {memory.percent}%")
                if self.automation_rules['low_memory']['enabled']:
                    self.cleanup_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            if disk.percent > self.disk_threshold:
                self.log_message(f"High disk usage detected: {disk.percent}%")
                if self.automation_rules['disk_full']['enabled']:
                    self.cleanup_disk()
            
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
    
    def update_system_display(self):
        """Update system information display"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            self.cpu_label.config(text=f"CPU: {cpu_percent:.1f}%")
            
            # Memory
            memory = psutil.virtual_memory()
            self.memory_label.config(text=f"Memory: {memory.percent:.1f}% ({memory.used // (1024**3):.1f}GB / {memory.total // (1024**3):.1f}GB)")
            
            # Disk
            disk = psutil.disk_usage('/')
            self.disk_label.config(text=f"Disk: {disk.percent:.1f}% ({disk.used // (1024**3):.1f}GB / {disk.total // (1024**3):.1f}GB)")
            
        except Exception as e:
            self.logger.error(f"Display update failed: {e}")
    
    def optimize_processes(self):
        """Optimize system processes"""
        try:
            self.log_message("Optimizing system processes...")
            
            # Get top CPU consuming processes
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            
            # Kill unnecessary high-CPU processes
            killed_count = 0
            for proc in processes[:10]:  # Top 10 processes
                if proc['cpu_percent'] > 50:  # High CPU usage
                    try:
                        p = psutil.Process(proc['pid'])
                        if p.name() not in ['system', 'explorer.exe', 'svchost.exe']:
                            p.terminate()
                            killed_count += 1
                            self.log_message(f"Terminated high-CPU process: {proc['name']}")
                    except:
                        pass
            
            if killed_count > 0:
                self.log_message(f"Optimization complete. Terminated {killed_count} high-CPU processes.")
                self.speak(f"System optimized. Terminated {killed_count} high-CPU processes.")
            else:
                self.log_message("No optimization needed.")
                
        except Exception as e:
            self.logger.error(f"Process optimization failed: {e}")
    
    def cleanup_memory(self):
        """Clean up system memory"""
        try:
            self.log_message("Cleaning up system memory...")
            
            # Get memory info
            memory = psutil.virtual_memory()
            
            if memory.percent > 85:
                # Force garbage collection
                import gc
                gc.collect()
                
                # Clear clipboard
                try:
                    import win32clipboard
                    win32clipboard.OpenClipboard()
                    win32clipboard.EmptyClipboard()
                    win32clipboard.CloseClipboard()
                except:
                    pass
                
                self.log_message("Memory cleanup completed.")
                self.speak("Memory cleanup completed.")
            else:
                self.log_message("Memory usage is normal.")
                
        except Exception as e:
            self.logger.error(f"Memory cleanup failed: {e}")
    
    def cleanup_disk(self):
        """Clean up disk space"""
        try:
            self.log_message("Cleaning up disk space...")
            
            # Get disk info
            disk = psutil.disk_usage('/')
            
            if disk.percent > 90:
                # Clean temp files
                temp_dirs = ['/tmp', '/var/tmp', os.path.expanduser('~/.cache')]
                cleaned_size = 0
                
                for temp_dir in temp_dirs:
                    if os.path.exists(temp_dir):
                        for root, dirs, files in os.walk(temp_dir):
                            for file in files:
                                try:
                                    file_path = os.path.join(root, file)
                                    file_size = os.path.getsize(file_path)
                                    os.remove(file_path)
                                    cleaned_size += file_size
                                except:
                                    pass
                
                if cleaned_size > 0:
                    self.log_message(f"Disk cleanup completed. Freed {cleaned_size // (1024**2)} MB.")
                    self.speak(f"Disk cleanup completed. Freed {cleaned_size // (1024**2)} MB.")
                else:
                    self.log_message("Disk cleanup completed.")
            else:
                self.log_message("Disk usage is normal.")
                
        except Exception as e:
            self.logger.error(f"Disk cleanup failed: {e}")
    
    def optimize_system(self):
        """General system optimization"""
        try:
            self.log_message("Starting system optimization...")
            
            # Run all optimization tasks
            self.optimize_processes()
            self.cleanup_memory()
            self.cleanup_disk()
            
            self.log_message("System optimization completed.")
            self.speak("System optimization completed.")
            
        except Exception as e:
            self.logger.error(f"System optimization failed: {e}")
    
    def show_system_info(self):
        """Show detailed system information"""
        try:
            info = f"""
System Information:
- OS: {platform.system()} {platform.release()}
- CPU: {platform.processor()}
- Memory: {psutil.virtual_memory().total // (1024**3)} GB
- Disk: {psutil.disk_usage('/').total // (1024**3)} GB
- Python: {platform.python_version()}
            """
            
            self.log_message("System information displayed.")
            self.speak("Here is your system information.")
            
            # Show in popup
            messagebox.showinfo("System Information", info)
            
        except Exception as e:
            self.logger.error(f"System info display failed: {e}")
    
    def show_system_status(self):
        """Show current system status"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            status = f"""
Current System Status:
- CPU Usage: {cpu:.1f}%
- Memory Usage: {memory.percent:.1f}%
- Disk Usage: {disk.percent:.1f}%
- System Status: {'Healthy' if cpu < 80 and memory.percent < 85 and disk.percent < 90 else 'Needs Attention'}
            """
            
            self.log_message("System status displayed.")
            self.speak("Here is your current system status.")
            
            messagebox.showinfo("System Status", status)
            
        except Exception as e:
            self.logger.error(f"Status display failed: {e}")
    
    def show_help(self):
        """Show help information"""
        help_text = """
Voice Commands Available:
- "CPU" or "Processor" - Show system information
- "Memory" or "RAM" - Clean up memory
- "Disk" or "Storage" - Clean up disk space
- "Optimize" or "Performance" - Optimize system
- "Status" or "Condition" - Show system status
- "Help" - Show this help

The AI Assistant will automatically:
- Monitor system health
- Optimize performance when needed
- Clean up resources automatically
- Manage PC without user intervention
        """
        
        self.log_message("Help information displayed.")
        self.speak("Here are the available voice commands and features.")
        
        messagebox.showinfo("AI Assistant Help", help_text)
    
    def on_closing(self):
        """Handle application closing"""
        if self.is_running:
            self.stop_assistant()
        
        self.log_message("AI Assistant shutting down...")
        self.root.destroy()
    
    def run(self):
        """Start the GUI main loop"""
        try:
            self.log_message("AI Assistant GUI started. Ready to use!")
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"GUI error: {e}")

if __name__ == "__main__":
    try:
        assistant = AIAssistant()
        assistant.run()
    except Exception as e:
        print(f"Failed to start AI Assistant: {e}")
        logging.error(f"Failed to start AI Assistant: {e}")