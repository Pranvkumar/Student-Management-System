#!/usr/bin/env python3
"""
Enhanced Study Buddy - Automated Setup Script
Automatically installs dependencies and sets up the application
"""

import subprocess
import sys
import os
import sqlite3
import json
from pathlib import Path

def print_banner():
    """Print application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║              📚 Enhanced Study Buddy Setup 📚               ║
║                                                              ║
║        Automated installation and configuration script       ║
║                     Version 2.0                             ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade Python and try again.")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected - Compatible!")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Upgrade pip first
        print("   Upgrading pip...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        
        # Install requirements
        if os.path.exists('requirements.txt'):
            print("   Installing packages from requirements.txt...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        else:
            print("   Installing essential packages...")
            packages = [
                'kivy==2.3.0',
                'kivymd==1.1.1', 
                'pillow==10.4.0',
                'requests==2.31.0',
                'matplotlib==3.8.4',
                'pandas==2.2.2',
                'numpy==1.26.4'
            ]
            
            for package in packages:
                print(f"   Installing {package}...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        
        print("✅ All dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_directories():
    """Create necessary application directories"""
    print("\n📁 Creating application directories...")
    
    directories = ['config', 'data', 'backups', 'assets', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ Created: {directory}/")
    
    return True

def setup_database():
    """Initialize the application database"""
    print("\n🗄️  Setting up database...")
    
    try:
        db_path = 'data/enhanced_study_helper.db'
        
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            
            # Create tables
            tables = [
                '''CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    description TEXT,
                    priority INTEGER DEFAULT 1,
                    category TEXT DEFAULT 'General',
                    due_date TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    completed_at TEXT,
                    done INTEGER DEFAULT 0,
                    archived INTEGER DEFAULT 0
                )''',
                
                '''CREATE TABLE IF NOT EXISTS test_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject TEXT NOT NULL,
                    test_name TEXT NOT NULL,
                    score REAL NOT NULL,
                    max_score REAL DEFAULT 100,
                    grade TEXT,
                    date TEXT NOT NULL,
                    semester TEXT,
                    notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )''',
                
                '''CREATE TABLE IF NOT EXISTS study_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject TEXT NOT NULL,
                    topic TEXT,
                    duration_minutes INTEGER NOT NULL,
                    focus_rating INTEGER,
                    notes TEXT,
                    date TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )''',
                
                '''CREATE TABLE IF NOT EXISTS goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    target_date TEXT,
                    category TEXT,
                    progress INTEGER DEFAULT 0,
                    completed INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )'''
            ]
            
            for table_sql in tables:
                c.execute(table_sql)
            
            conn.commit()
        
        print("✅ Database initialized successfully!")
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database setup error: {e}")
        return False

def create_config():
    """Create default application configuration"""
    print("\n⚙️  Creating configuration files...")
    
    default_config = {
        "theme": "dark_academic",
        "notifications": True,
        "auto_backup": True,
        "default_reminder_time": 30,
        "study_session_goals": {
            "daily_minutes": 120,
            "weekly_sessions": 5
        },
        "grade_scale": {
            "A+": 97, "A": 93, "A-": 90,
            "B+": 87, "B": 83, "B-": 80,
            "C+": 77, "C": 73, "C-": 70,
            "D+": 67, "D": 63, "D-": 60,
            "F": 0
        },
        "ui_settings": {
            "animations": True,
            "particles": True,
            "sound_effects": True,
            "auto_save": True
        },
        "privacy": {
            "analytics": False,
            "crash_reports": False,
            "usage_stats": False
        }
    }
    
    try:
        config_path = 'config/app_config.json'
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        print("✅ Configuration file created!")
        return True
        
    except IOError as e:
        print(f"❌ Configuration creation error: {e}")
        return False

def create_desktop_shortcut():
    """Create desktop shortcut (Windows only)"""
    if sys.platform == 'win32':
        print("\n🖥️  Creating desktop shortcut...")
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "Enhanced Study Buddy.lnk")
            target = os.path.join(os.getcwd(), "Enhanced_App.py")
            wDir = os.getcwd()
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{target}"'
            shortcut.WorkingDirectory = wDir
            shortcut.IconLocation = target
            shortcut.save()
            
            print("✅ Desktop shortcut created!")
            
        except ImportError:
            print("⚠️  Desktop shortcut creation skipped (requires pywin32)")
        except Exception as e:
            print(f"⚠️  Desktop shortcut creation failed: {e}")

def run_initial_test():
    """Test if the application launches correctly"""
    print("\n🧪 Running application test...")
    
    try:
        # Import test
        sys.path.append('.')
        import Enhanced_App
        print("✅ Application imports successfully!")
        
        # Database test
        db_path = 'data/enhanced_study_helper.db'
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            table_count = c.fetchone()[0]
            
            if table_count >= 4:
                print("✅ Database tables verified!")
            else:
                print(f"⚠️  Expected 4+ tables, found {table_count}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Application test failed: {e}")
        return False

def print_completion_message():
    """Print setup completion message with instructions"""
    completion_msg = """
╔══════════════════════════════════════════════════════════════╗
║                    🎉 Setup Complete! 🎉                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Your Enhanced Study Buddy is ready to use!                 ║
║                                                              ║
║  Quick Start:                                                ║
║  1. Run: python Enhanced_App.py                              ║
║  2. Add your first task or study goal                        ║
║  3. Explore the analytics and features                       ║
║                                                              ║
║  Features Available:                                         ║
║  ✅ Enhanced todo management                                 ║
║  ✅ Study analytics and tracking                             ║
║  ✅ Test score management                                    ║
║  ✅ Productivity insights                                    ║
║  ✅ Data backup and sync                                     ║
║                                                              ║
║  Need help? Check README.md for detailed instructions       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

🚀 Ready to boost your academic productivity!
"""
    print(completion_msg)

def main():
    """Main setup function"""
    print_banner()
    
    # Step 1: Check Python version
    if not check_python_version():
        return False
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        return False
    
    # Step 3: Create directories
    if not create_directories():
        print("\n❌ Setup failed at directory creation")
        return False
    
    # Step 4: Setup database
    if not setup_database():
        print("\n❌ Setup failed at database initialization")
        return False
    
    # Step 5: Create configuration
    if not create_config():
        print("\n❌ Setup failed at configuration creation")
        return False
    
    # Step 6: Create desktop shortcut (optional)
    create_desktop_shortcut()
    
    # Step 7: Test application
    if not run_initial_test():
        print("\n⚠️  Setup completed with warnings - application may not work correctly")
        return False
    
    # Step 8: Success message
    print_completion_message()
    return True

if __name__ == '__main__':
    try:
        success = main()
        if success:
            print("✅ Setup completed successfully!")
            
            # Ask if user wants to launch the app
            response = input("\n🚀 Would you like to launch the app now? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                print("\n🎯 Launching Enhanced Study Buddy...")
                subprocess.run([sys.executable, 'Enhanced_App.py'])
        else:
            print("❌ Setup failed - please check the errors above")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)