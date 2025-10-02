"""
Enhanced Study Buddy Application
A comprehensive productivity and study management app with modern features
Author: Pranvkumar Kshirsagar
Version: 2.0 Enhanced
"""

from datetime import datetime, timedelta
import sqlite3
import calendar
import random
import json
import os
from typing import Dict, List, Optional, Tuple
import threading

# Kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.properties import ObjectProperty, StringProperty
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.clock import Clock
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious
from kivy.metrics import dp

# Enhanced constants and configuration
DB_NAME = 'enhanced_study_helper.db'
CONFIG_FILE = 'app_config.json'
BACKUP_DIR = 'backups'

# Modern UI Theme - Dark Academic
COLORS = {
    'primary_bg': (0.08, 0.12, 0.18, 1),      # Deep navy
    'secondary_bg': (0.12, 0.16, 0.24, 1),    # Lighter navy
    'accent': (0.4, 0.7, 1, 1),               # Bright blue
    'accent_secondary': (0.6, 0.4, 0.9, 1),   # Purple
    'success': (0.2, 0.8, 0.4, 1),            # Green
    'warning': (1, 0.7, 0.2, 1),              # Orange
    'danger': (0.9, 0.3, 0.3, 1),             # Red
    'text_primary': (0.95, 0.95, 0.98, 1),    # Off-white
    'text_secondary': (0.7, 0.75, 0.85, 1),   # Light gray
    'text_disabled': (0.5, 0.55, 0.65, 1),    # Darker gray
    'button_primary': (0.15, 0.20, 0.30, 1),  # Button background
    'button_hover': (0.20, 0.25, 0.35, 1),    # Button hover
}

class DatabaseManager:
    """Enhanced database management with connection pooling and error handling"""
    
    def __init__(self, db_name: str = DB_NAME):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize all database tables"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                c = conn.cursor()
                
                # Enhanced todos table
                c.execute('''
                    CREATE TABLE IF NOT EXISTS todos (
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
                    )
                ''')
                
                # Enhanced test scores table
                c.execute('''
                    CREATE TABLE IF NOT EXISTS test_scores (
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
                    )
                ''')
                
                # Study sessions table
                c.execute('''
                    CREATE TABLE IF NOT EXISTS study_sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        subject TEXT NOT NULL,
                        topic TEXT,
                        duration_minutes INTEGER NOT NULL,
                        focus_rating INTEGER,
                        notes TEXT,
                        date TEXT NOT NULL,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Goals table
                c.execute('''
                    CREATE TABLE IF NOT EXISTS goals (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        target_date TEXT,
                        category TEXT,
                        progress INTEGER DEFAULT 0,
                        completed INTEGER DEFAULT 0,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Daily planners table
                c.execute('''
                    CREATE TABLE IF NOT EXISTS daily_plans (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        task_title TEXT NOT NULL,
                        task_description TEXT,
                        time_slot TEXT,
                        priority INTEGER DEFAULT 1,
                        completed INTEGER DEFAULT 0,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")

class ConfigManager:
    """Application configuration management"""
    
    def __init__(self, config_file: str = CONFIG_FILE):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """Load configuration from file"""
        default_config = {
            'theme': 'dark_academic',
            'notifications': True,
            'auto_backup': True,
            'default_reminder_time': 30,
            'study_session_goals': {
                'daily_minutes': 120,
                'weekly_sessions': 5
            },
            'grade_scale': {
                'A+': 97, 'A': 93, 'A-': 90,
                'B+': 87, 'B': 83, 'B-': 80,
                'C+': 77, 'C': 73, 'C-': 70,
                'D+': 67, 'D': 63, 'D-': 60,
                'F': 0
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults for any missing keys
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Config load error: {e}")
        
        return default_config
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            print(f"Config save error: {e}")
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """Set configuration value"""
        self.config[key] = value
        self.save_config()

class AnalyticsManager:
    """Study analytics and progress tracking"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def get_productivity_stats(self, days: int = 7) -> Dict:
        """Get productivity statistics for the last n days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        try:
            with sqlite3.connect(self.db.db_name) as conn:
                c = conn.cursor()
                
                # Tasks completed
                c.execute('''
                    SELECT COUNT(*) FROM todos 
                    WHERE done = 1 AND completed_at >= ? AND completed_at <= ?
                ''', (start_date.isoformat(), end_date.isoformat()))
                completed_tasks = c.fetchone()[0]
                
                # Study time
                c.execute('''
                    SELECT SUM(duration_minutes) FROM study_sessions 
                    WHERE date >= ? AND date <= ?
                ''', (start_date.date().isoformat(), end_date.date().isoformat()))
                study_minutes = c.fetchone()[0] or 0
                
                # Average test score
                c.execute('''
                    SELECT AVG(score * 100.0 / max_score) FROM test_scores 
                    WHERE date >= ? AND date <= ?
                ''', (start_date.date().isoformat(), end_date.date().isoformat()))
                avg_score = c.fetchone()[0] or 0
                
                return {
                    'completed_tasks': completed_tasks,
                    'study_hours': round(study_minutes / 60, 1),
                    'average_score': round(avg_score, 1),
                    'productivity_score': min(100, (completed_tasks * 10) + (study_minutes / 12))
                }
        except sqlite3.Error as e:
            print(f"Analytics error: {e}")
            return {'completed_tasks': 0, 'study_hours': 0, 'average_score': 0, 'productivity_score': 0}

class EnhancedBackground(BoxLayout):
    """Enhanced animated background with particles"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.particles = []
        
        with self.canvas.before:
            Color(*COLORS['primary_bg'])
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            
            # Create animated particles
            self.create_particles()
        
        self.bind(pos=self._update_bg, size=self._update_bg)
        Clock.schedule_interval(self.animate_particles, 1/60)  # 60 FPS
    
    def create_particles(self):
        """Create floating particles for background animation"""
        for _ in range(50):
            Color(1, 1, 1, random.uniform(0.1, 0.3))
            x = random.randint(0, 1200)
            y = random.randint(0, 800)
            r = random.uniform(1, 3)
            particle = Ellipse(pos=(x, y), size=(r, r))
            self.particles.append({
                'graphic': particle,
                'x': x, 'y': y, 'size': r,
                'velocity_x': random.uniform(-0.5, 0.5),
                'velocity_y': random.uniform(-0.5, 0.5),
                'alpha': random.uniform(0.1, 0.3)
            })
    
    def animate_particles(self, dt):
        """Animate background particles"""
        for particle in self.particles:
            particle['x'] += particle['velocity_x']
            particle['y'] += particle['velocity_y']
            
            # Wrap around screen
            if particle['x'] < 0:
                particle['x'] = 1200
            elif particle['x'] > 1200:
                particle['x'] = 0
            
            if particle['y'] < 0:
                particle['y'] = 800
            elif particle['y'] > 800:
                particle['y'] = 0
            
            particle['graphic'].pos = (particle['x'], particle['y'])
    
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class ModernButton(Button):
    """Custom styled button with hover effects"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = COLORS['button_primary']
        self.color = COLORS['text_primary']
        self.size_hint_y = None
        self.height = dp(40)

class EnhancedTodoScreen(Screen):
    """Enhanced todo screen with categories, priorities, and analytics"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DatabaseManager()
        self.config = ConfigManager()
        self.analytics = AnalyticsManager(self.db)
        self.build_ui()
    
    def build_ui(self):
        """Build the enhanced todo interface"""
        root = EnhancedBackground(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Header with analytics
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80))
        
        title_section = BoxLayout(orientation='vertical')
        title_section.add_widget(Label(
            text="Enhanced Study Planner", 
            font_size=dp(24), 
            color=COLORS['accent'],
            size_hint_y=None, height=dp(40)
        ))
        
        # Quick stats
        stats = self.analytics.get_productivity_stats(7)
        stats_text = f"Week: {stats['completed_tasks']} tasks • {stats['study_hours']}h study • {stats['average_score']:.1f}% avg"
        title_section.add_widget(Label(
            text=stats_text, 
            font_size=dp(14), 
            color=COLORS['text_secondary'],
            size_hint_y=None, height=dp(30)
        ))
        
        header.add_widget(title_section)
        
        # Productivity progress bar
        progress_section = BoxLayout(orientation='vertical', size_hint_x=0.3)
        progress_section.add_widget(Label(
            text=f"Productivity: {stats['productivity_score']:.0f}%", 
            font_size=dp(12), 
            color=COLORS['text_secondary']
        ))
        progress_bar = ProgressBar(
            max=100, 
            value=stats['productivity_score'],
            size_hint_y=None, 
            height=dp(20)
        )
        progress_section.add_widget(progress_bar)
        header.add_widget(progress_section)
        
        root.add_widget(header)
        
        # Enhanced task input section
        input_section = self.create_task_input_section()
        root.add_widget(input_section)
        
        # Filter and sort options
        filter_section = self.create_filter_section()
        root.add_widget(filter_section)
        
        # Task list
        self.create_task_list()
        root.add_widget(self.task_scroll)
        
        # Action buttons
        action_section = self.create_action_buttons()
        root.add_widget(action_section)
        
        # Motivational quote
        root.add_widget(Label(
            text="\"Success is the sum of small efforts repeated day in and day out.\" - Robert Collier",
            font_size=dp(14), 
            color=COLORS['accent_secondary'],
            text_size=(None, None),
            halign='center'
        ))
        
        self.add_widget(root)
        self.load_tasks()
    
    def create_task_input_section(self):
        """Create enhanced task input with priority and category"""
        section = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(160), spacing=dp(5))
        
        # Task title input
        self.task_input = TextInput(
            hint_text="Enter your task...", 
            multiline=False,
            size_hint_y=None, 
            height=dp(40),
            background_color=COLORS['secondary_bg'], 
            foreground_color=COLORS['text_primary'], 
            cursor_color=COLORS['accent']
        )
        section.add_widget(self.task_input)
        
        # Task description
        self.description_input = TextInput(
            hint_text="Task description (optional)...", 
            multiline=True,
            size_hint_y=None, 
            height=dp(60),
            background_color=COLORS['secondary_bg'], 
            foreground_color=COLORS['text_primary'], 
            cursor_color=COLORS['accent']
        )
        section.add_widget(self.description_input)
        
        # Priority and category row
        options_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(10))
        
        self.priority_spinner = Spinner(
            text='Medium',
            values=['Low', 'Medium', 'High', 'Urgent'],
            size_hint_x=0.3,
            background_color=COLORS['button_primary'],
            color=COLORS['text_primary']
        )
        options_row.add_widget(self.priority_spinner)
        
        self.category_input = TextInput(
            hint_text="Category (e.g., Study, Personal)",
            background_color=COLORS['secondary_bg'], 
            foreground_color=COLORS['text_primary']
        )
        options_row.add_widget(self.category_input)
        
        add_btn = ModernButton(
            text="Add Task", 
            size_hint_x=0.3,
            background_color=COLORS['accent']
        )
        add_btn.bind(on_release=self.add_enhanced_task)
        options_row.add_widget(add_btn)
        
        section.add_widget(options_row)
        
        return section
    
    def create_filter_section(self):
        """Create task filtering and sorting options"""
        section = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(10))
        
        section.add_widget(Label(text="Filter:", color=COLORS['text_secondary'], size_hint_x=0.2))
        
        self.filter_spinner = Spinner(
            text='All',
            values=['All', 'Pending', 'Completed', 'High Priority', 'Urgent'],
            size_hint_x=0.4,
            background_color=COLORS['button_primary'],
            color=COLORS['text_primary']
        )
        self.filter_spinner.bind(text=self.on_filter_change)
        section.add_widget(self.filter_spinner)
        
        sort_btn = ModernButton(text="Sort by Priority", size_hint_x=0.4)
        sort_btn.bind(on_release=self.sort_tasks_by_priority)
        section.add_widget(sort_btn)
        
        return section
    
    def create_task_list(self):
        """Create scrollable task list"""
        self.task_scroll = ScrollView()
        self.tasks_layout = GridLayout(
            cols=1, 
            spacing=dp(8), 
            size_hint_y=None,
            padding=[0, dp(10)]
        )
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))
        self.task_scroll.add_widget(self.tasks_layout)
    
    def create_action_buttons(self):
        """Create action buttons section"""
        section = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        
        clear_completed_btn = ModernButton(
            text="Clear Completed", 
            background_color=COLORS['warning']
        )
        clear_completed_btn.bind(on_release=self.clear_completed_tasks)
        section.add_widget(clear_completed_btn)
        
        archive_btn = ModernButton(
            text="Archive Old", 
            background_color=COLORS['button_primary']
        )
        archive_btn.bind(on_release=self.archive_old_tasks)
        section.add_widget(archive_btn)
        
        backup_btn = ModernButton(
            text="Backup Data", 
            background_color=COLORS['success']
        )
        backup_btn.bind(on_release=self.backup_data)
        section.add_widget(backup_btn)
        
        return section
    
    def add_enhanced_task(self, _):
        """Add task with enhanced features"""
        task = self.task_input.text.strip()
        description = self.description_input.text.strip()
        priority = self.priority_spinner.text
        category = self.category_input.text.strip() or "General"
        
        if not task:
            self.show_popup("Error", "Please enter a task title.")
            return
        
        priority_map = {'Low': 1, 'Medium': 2, 'High': 3, 'Urgent': 4}
        priority_num = priority_map.get(priority, 2)
        
        try:
            with sqlite3.connect(self.db.db_name) as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT INTO todos (task, description, priority, category, created_at) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (task, description, priority_num, category, datetime.now().isoformat()))
                conn.commit()
            
            # Clear inputs
            self.task_input.text = ''
            self.description_input.text = ''
            self.category_input.text = ''
            self.priority_spinner.text = 'Medium'
            
            self.load_tasks()
            self.show_popup("Success", f"Task '{task}' added successfully!", success=True)
            
        except sqlite3.Error as e:
            self.show_popup("Error", f"Failed to add task: {e}")
    
    def load_tasks(self, filter_type='All'):
        """Load tasks with filtering"""
        self.tasks_layout.clear_widgets()
        
        try:
            with sqlite3.connect(self.db.db_name) as conn:
                c = conn.cursor()
                
                base_query = '''
                    SELECT id, task, description, priority, category, due_date, done, created_at 
                    FROM todos WHERE archived = 0
                '''
                
                if filter_type == 'Pending':
                    base_query += ' AND done = 0'
                elif filter_type == 'Completed':
                    base_query += ' AND done = 1'
                elif filter_type == 'High Priority':
                    base_query += ' AND priority >= 3 AND done = 0'
                elif filter_type == 'Urgent':
                    base_query += ' AND priority = 4 AND done = 0'
                
                base_query += ' ORDER BY priority DESC, created_at DESC'
                
                c.execute(base_query)
                tasks = c.fetchall()
                
                if not tasks:
                    self.tasks_layout.add_widget(Label(
                        text="No tasks found. Add some tasks to get started!",
                        color=COLORS['text_secondary'],
                        size_hint_y=None,
                        height=dp(60)
                    ))
                    return
                
                for task_data in tasks:
                    task_widget = self.create_task_widget(task_data)
                    self.tasks_layout.add_widget(task_widget)
                    
        except sqlite3.Error as e:
            self.show_popup("Error", f"Failed to load tasks: {e}")
    
    def create_task_widget(self, task_data):
        """Create individual task widget with enhanced UI"""
        tid, task, description, priority, category, due_date, done, created_at = task_data
        
        # Main container
        main_box = BoxLayout(
            orientation='vertical', 
            size_hint_y=None, 
            height=dp(100),
            padding=[dp(10), dp(5)],
            spacing=dp(5)
        )
        
        # Add colored background based on priority
        priority_colors = {
            4: COLORS['danger'],      # Urgent
            3: COLORS['warning'],     # High
            2: COLORS['accent'],      # Medium
            1: COLORS['success']      # Low
        }
        
        with main_box.canvas.before:
            Color(*priority_colors.get(priority, COLORS['button_primary']))
            main_box.bg_rect = Rectangle(pos=main_box.pos, size=main_box.size)
        
        main_box.bind(pos=lambda *args: setattr(main_box.bg_rect, 'pos', main_box.pos),
                     size=lambda *args: setattr(main_box.bg_rect, 'size', main_box.size))
        
        # Top row: checkbox, title, delete button
        top_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        
        cb = CheckBox(
            active=bool(done), 
            size_hint_x=None, 
            width=dp(40),
            color=COLORS['accent']
        )
        cb.bind(active=lambda _, value, tid=tid: self.toggle_task(tid, value))
        top_row.add_widget(cb)
        
        task_text = task
        if done:
            task_text = f"[s]{task}[/s]"  # Strikethrough completed tasks
        
        task_label = Label(
            text=task_text,
            markup=True,
            color=COLORS['text_disabled'] if done else COLORS['text_primary'],
            text_size=(None, None),
            halign='left'
        )
        top_row.add_widget(task_label)
        
        delete_btn = Button(
            text="×", 
            size_hint_x=None, 
            width=dp(40),
            height=dp(40),
            background_color=COLORS['danger'],
            color=COLORS['text_primary']
        )
        delete_btn.bind(on_release=lambda _, tid=tid: self.delete_task(tid))
        top_row.add_widget(delete_btn)
        
        main_box.add_widget(top_row)
        
        # Bottom row: description, category, priority
        if description or category:
            bottom_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30))
            
            info_text = ""
            if description:
                info_text += f"📝 {description[:50]}{'...' if len(description) > 50 else ''}"
            if category:
                info_text += f" | 📂 {category}"
            
            priority_names = {4: 'URGENT', 3: 'HIGH', 2: 'MEDIUM', 1: 'LOW'}
            info_text += f" | 🔥 {priority_names.get(priority, 'UNKNOWN')}"
            
            info_label = Label(
                text=info_text,
                font_size=dp(12),
                color=COLORS['text_secondary'],
                text_size=(None, None),
                halign='left'
            )
            bottom_row.add_widget(info_label)
            
            main_box.add_widget(bottom_row)
        
        return main_box
    
    def toggle_task(self, tid, value):
        """Toggle task completion status"""
        try:
            with sqlite3.connect(self.db.db_name) as conn:
                c = conn.cursor()
                completed_at = datetime.now().isoformat() if value else None
                c.execute('UPDATE todos SET done=?, completed_at=? WHERE id=?', 
                         (1 if value else 0, completed_at, tid))
                conn.commit()
            self.load_tasks(self.filter_spinner.text)
        except sqlite3.Error as e:
            self.show_popup("Error", f"Failed to update task: {e}")
    
    def delete_task(self, tid):
        """Delete task with confirmation"""
        def confirm_delete(_):
            try:
                with sqlite3.connect(self.db.db_name) as conn:
                    c = conn.cursor()
                    c.execute('DELETE FROM todos WHERE id=?', (tid,))
                    conn.commit()
                self.load_tasks(self.filter_spinner.text)
                popup.dismiss()
                self.show_popup("Success", "Task deleted successfully!", success=True)
            except sqlite3.Error as e:
                popup.dismiss()
                self.show_popup("Error", f"Failed to delete task: {e}")
        
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        content.add_widget(Label(
            text="Are you sure you want to delete this task?",
            color=COLORS['text_primary']
        ))
        
        buttons = BoxLayout(orientation='horizontal', spacing=dp(10))
        yes_btn = Button(
            text="Yes, Delete", 
            background_color=COLORS['danger'], 
            color=COLORS['text_primary']
        )
        no_btn = Button(
            text="Cancel", 
            background_color=COLORS['button_primary'], 
            color=COLORS['text_primary']
        )
        
        popup = Popup(
            title='Confirm Delete',
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        
        yes_btn.bind(on_release=confirm_delete)
        no_btn.bind(on_release=popup.dismiss)
        
        buttons.add_widget(yes_btn)
        buttons.add_widget(no_btn)
        content.add_widget(buttons)
        
        popup.open()
    
    def on_filter_change(self, spinner, text):
        """Handle filter changes"""
        self.load_tasks(text)
    
    def sort_tasks_by_priority(self, _):
        """Sort tasks by priority"""
        self.load_tasks(self.filter_spinner.text)
    
    def clear_completed_tasks(self, _):
        """Clear all completed tasks"""
        try:
            with sqlite3.connect(self.db.db_name) as conn:
                c = conn.cursor()
                c.execute('DELETE FROM todos WHERE done = 1')
                conn.commit()
            self.load_tasks(self.filter_spinner.text)
            self.show_popup("Success", "Completed tasks cleared!", success=True)
        except sqlite3.Error as e:
            self.show_popup("Error", f"Failed to clear tasks: {e}")
    
    def archive_old_tasks(self, _):
        """Archive tasks older than 30 days"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=30)).isoformat()
            with sqlite3.connect(self.db.db_name) as conn:
                c = conn.cursor()
                c.execute('UPDATE todos SET archived = 1 WHERE created_at < ? AND done = 1', (cutoff_date,))
                archived_count = c.rowcount
                conn.commit()
            
            self.load_tasks(self.filter_spinner.text)
            self.show_popup("Success", f"Archived {archived_count} old tasks!", success=True)
        except sqlite3.Error as e:
            self.show_popup("Error", f"Failed to archive tasks: {e}")
    
    def backup_data(self, _):
        """Create backup of all data"""
        try:
            if not os.path.exists(BACKUP_DIR):
                os.makedirs(BACKUP_DIR)
            
            backup_file = os.path.join(BACKUP_DIR, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
            
            with sqlite3.connect(self.db.db_name) as source:
                with sqlite3.connect(backup_file) as backup:
                    source.backup(backup)
            
            self.show_popup("Success", f"Backup created: {backup_file}", success=True)
        except Exception as e:
            self.show_popup("Error", f"Backup failed: {e}")
    
    def show_popup(self, title, message, success=False):
        """Show popup with message"""
        color = COLORS['success'] if success else COLORS['danger']
        content = Label(text=message, color=COLORS['text_primary'])
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4),
            title_color=color
        )
        popup.open()
        
        # Auto-dismiss success popups
        if success:
            Clock.schedule_once(lambda dt: popup.dismiss(), 2)

class EnhancedStudyApp(App):
    """Main application class"""
    
    def build(self):
        """Build the main application"""
        self.title = "Enhanced Study Buddy - Academic Productivity Suite"
        
        # Initialize managers
        self.db = DatabaseManager()
        self.config = ConfigManager()
        
        # Create screen manager
        sm = ScreenManager()
        sm.add_widget(EnhancedTodoScreen(name='enhanced_todo'))
        
        # Main layout
        root = EnhancedBackground(orientation='vertical')
        
        # Navigation bar
        nav = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5), padding=[dp(10), dp(5)])
        
        nav_buttons = [
            ('Enhanced To-Do', 'enhanced_todo', COLORS['accent']),
            ('Analytics', 'analytics', COLORS['success']),
            ('Study Timer', 'timer', COLORS['warning']),
            ('Test Scores', 'scores', COLORS['accent_secondary']),
            ('Settings', 'settings', COLORS['text_secondary'])
        ]
        
        for label, screen_name, color in nav_buttons:
            btn = ModernButton(
                text=label, 
                background_color=color if screen_name == 'enhanced_todo' else COLORS['button_primary']
            )
            btn.bind(on_release=lambda _, name=screen_name: setattr(sm, 'current', name))
            nav.add_widget(btn)
        
        root.add_widget(nav)
        root.add_widget(sm)
        
        return root

if __name__ == '__main__':
    EnhancedStudyApp().run()