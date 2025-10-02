from datetime import datetime
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
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Ellipse, Rectangle
import sqlite3
import calendar
import random

DB_NAME = 'Study_Helper.db'

# Starry night colors
NIGHT_BG = (0.05, 0.07, 0.15, 1)
NIGHT_PANEL = (0.10, 0.13, 0.22, 1)
NIGHT_BTN = (0.13, 0.17, 0.28, 1)
NIGHT_BTN_ACTIVE = (0.18, 0.22, 0.35, 1)
STAR_COLOR = (1, 1, 1, 0.7)
ACCENT = (0.5, 0.7, 1, 1)
ACCENT2 = (0.7, 0.5, 1, 1)
LIGHT_TEXT = (0.95, 0.97, 1, 1)
DISABLED_TEXT = (0.5, 0.5, 0.7, 1)

class StarryBackground(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*NIGHT_BG)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            # Draw random stars
            for _ in range(80):
                Color(1, 1, 1, random.uniform(0.3, 0.8))
                x = random.randint(0, 1920)
                y = random.randint(0, 1080)
                r = random.uniform(1, 2.5)
                Ellipse(pos=(x, y), size=(r, r))
        self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class TodoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = sqlite3.connect(DB_NAME)
        self.c = self.conn.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                done INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

        root = StarryBackground(orientation='vertical', padding=10, spacing=10)
        root.add_widget(Label(text="To Prepare and not waste", font_size=24, color=ACCENT))

        entry_layout = BoxLayout(size_hint_y=None, height=40, spacing=5)
        self.task_input = TextInput(hint_text="Enter a task", multiline=False,
                                    background_color=NIGHT_PANEL, foreground_color=LIGHT_TEXT, cursor_color=ACCENT)
        entry_layout.add_widget(self.task_input)
        add_btn = Button(text="Add Task", size_hint_x=None, width=100, background_color=ACCENT, color=LIGHT_TEXT)
        add_btn.bind(on_release=self.add_task)
        entry_layout.add_widget(add_btn)
        root.add_widget(entry_layout)

        self.scroll = ScrollView()
        self.tasks_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))
        self.scroll.add_widget(self.tasks_layout)
        root.add_widget(self.scroll)

        del_btn = Button(text="Delete All Tasks", background_color=NIGHT_BTN, color=ACCENT)
        del_btn.bind(on_release=self.delete_all_tasks)
        root.add_widget(del_btn)

        root.add_widget(Label(text="Karmanye vadhikaraste Ma"
        "  Phalenshu Kadachana, "
        "Ma Karmaphalaheturbhurma Te"
        "Sangostvakarmani", font_size=20, color=ACCENT2))

        self.add_widget(root)
        self.load_tasks()

    def add_task(self, _):
        task = self.task_input.text.strip()
        if task:
            self.c.execute('INSERT INTO todos (task) VALUES (?)', (task,))
            self.conn.commit()
            self.task_input.text = ''
            self.load_tasks()
        else:
            self.show_popup("Please enter a task.")

    def load_tasks(self):
        self.tasks_layout.clear_widgets()
        self.c.execute('SELECT id, task, done FROM todos')
        for tid, task, done in self.c.fetchall():
            row = BoxLayout(size_hint_y=None, height=40)
            cb = CheckBox(active=bool(done), color=ACCENT)
            cb.bind(active=lambda _, value, tid=tid: self.toggle_task(tid, value))
            row.add_widget(cb)
            lbl = Label(text=task, color=DISABLED_TEXT if done else LIGHT_TEXT)
            row.add_widget(lbl)
            self.tasks_layout.add_widget(row)

    def toggle_task(self, tid, value):
        self.c.execute('UPDATE todos SET done=? WHERE id=?', (1 if value else 0, tid))
        self.conn.commit()
        self.load_tasks()

    def delete_all_tasks(self, _):
        popup = Popup(title='Delete All',
                      content=Label(text='Are you sure you want to delete all tasks?', color=LIGHT_TEXT),
                      size_hint=(0.7, 0.3),
                      auto_dismiss=False)
        btn_yes = Button(text='Yes', background_color=ACCENT, color=LIGHT_TEXT)
        btn_no = Button(text='No', background_color=NIGHT_BTN, color=LIGHT_TEXT)
        btn_yes.bind(on_release=lambda _: self.confirm_delete_all(popup))
        btn_no.bind(on_release=popup.dismiss)
        btns = BoxLayout()
        btns.add_widget(btn_yes)
        btns.add_widget(btn_no)
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(Label(text='Are you sure you want to delete all tasks?', color=LIGHT_TEXT))
        popup_content.add_widget(btns)
        popup.content = popup_content
        popup.open()

    def confirm_delete_all(self, popup):
        self.c.execute('DELETE FROM todos')
        self.conn.commit()
        self.load_tasks()
        popup.dismiss()

    def show_popup(self, message):
        popup = Popup(title='Oops!', content=Label(text=message, color=LIGHT_TEXT),
                      size_hint=(0.7, 0.3))
        popup.open()

    def on_leave(self):
        self.conn.close()

class WeeklyPlannerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(StarryBackground())

class AppState:
    selected_date = datetime.today().date()

app_state = AppState()

def get_day_indicators(_):
    return False

class CalendarScreen(Screen):
    month_label = ObjectProperty(None)
    calendar_grid = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_year = datetime.today().year
        self.current_month = datetime.today().month
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        layout = StarryBackground(orientation='vertical', padding=10, spacing=10)

        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        prev_btn = Button(text='<', size_hint_x=None, width=50, on_release=self.prev_month,
                          background_color=NIGHT_BTN, color=LIGHT_TEXT)
        next_btn = Button(text='>', size_hint_x=None, width=50, on_release=self.next_month,
                          background_color=NIGHT_BTN, color=LIGHT_TEXT)
        today_btn = Button(text='Today', size_hint_x=None, width=80, on_release=self.goto_today,
                           background_color=ACCENT, color=LIGHT_TEXT)
        self.month_label = Label(text=self.get_month_year_str(), font_size=20, color=ACCENT)
        header.add_widget(prev_btn)
        header.add_widget(self.month_label)
        header.add_widget(today_btn)
        header.add_widget(next_btn)
        layout.add_widget(header)

        days_grid = GridLayout(cols=7, size_hint_y=None, height=30)
        for day in calendar.day_abbr:
            days_grid.add_widget(Label(text=day, bold=True, color=ACCENT2))
        layout.add_widget(days_grid)

        self.calendar_grid = GridLayout(cols=7, spacing=2)
        self.populate_calendar()
        layout.add_widget(self.calendar_grid)

        self.add_widget(layout)

    def get_month_year_str(self):
        return datetime(self.current_year, self.current_month, 1).strftime('%B %Y')

    def populate_calendar(self):
        self.calendar_grid.clear_widgets()
        cal = calendar.Calendar()
        month_days = cal.itermonthdates(self.current_year, self.current_month)
        today = datetime.today().date()
        for date in month_days:
            btn = Button(
                text=str(date.day),
                background_normal='',
                background_color=NIGHT_BTN,
                color=LIGHT_TEXT,
                on_release=lambda _, d=date: self.on_date_selected(d)
            )
            if date.month != self.current_month:
                btn.background_color = NIGHT_PANEL
                btn.color = DISABLED_TEXT
                btn.disabled = True
            if date == today:
                btn.background_color = ACCENT2
                btn.color = NIGHT_BG
            if get_day_indicators(date):
                btn.text += " •"
                btn.color = (1, 0.7, 0.2, 1)
            self.calendar_grid.add_widget(btn)

    def prev_month(self, _):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.month_label.text = self.get_month_year_str()
        self.populate_calendar()

    def next_month(self, _):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.month_label.text = self.get_month_year_str()
        self.populate_calendar()

    def goto_today(self, _):
        today = datetime.today()
        self.current_year = today.year
        self.current_month = today.month
        self.month_label.text = self.get_month_year_str()
        self.populate_calendar()

    def on_date_selected(self, date):
        app_state.selected_date = date
        self.manager.current = 'daily_planner'

class DailyPlannerScreen(Screen):
    def on_pre_enter(self):
        self.clear_widgets()
        layout = StarryBackground(orientation='vertical', spacing=10, padding=10)
        date_str = app_state.selected_date.strftime('%A, %B %d, %Y')
        layout.add_widget(Label(text=f"Daily Planner for {date_str}", font_size=24, color=ACCENT2))

        self.task_input = TextInput(hint_text="Enter your task here", size_hint_y=None, height=40,
                                    background_color=NIGHT_PANEL, foreground_color=LIGHT_TEXT, cursor_color=ACCENT)
        layout.add_widget(self.task_input)

        add_btn = Button(text="Add Task", size_hint_y=None, height=40, on_release=self.add_task,
                         background_color=ACCENT, color=LIGHT_TEXT)
        layout.add_widget(add_btn)

        back_btn = Button(text="Back to Calendar", size_hint_y=None, height=50, on_release=self.go_back,
                          background_color=NIGHT_BTN, color=ACCENT)
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def add_task(self, _):
        task = self.task_input.text
        if task:
            print(f"Task for {app_state.selected_date}: {task}")
            self.task_input.text = ""

    def go_back(self, _):
        self.manager.current = 'calendar'

class MonthlyPlannerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager()
        self.sm.add_widget(CalendarScreen(name='calendar'))
        self.sm.add_widget(DailyPlannerScreen(name='daily_planner'))
        self.add_widget(self.sm)

class TimetableScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(StarryBackground())

class TestScoreScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(TestScoreMainWidget())

class TestScoreMainWidget(StarryBackground):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.input_form = ScoreInputForm(self)
        self.list_view = ScoreListView(self)
        self.add_widget(self.input_form)
        self.add_widget(Label(text="--- Test Scores ---", size_hint_y=None, height=30, color=ACCENT2))
        self.add_widget(self.list_view)

class ScoreInputForm(BoxLayout):
    def __init__(self, parent_widget, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.parent_widget = parent_widget
        self.subject = TextInput(hint_text="Subject Name", background_color=NIGHT_PANEL, foreground_color=LIGHT_TEXT, cursor_color=ACCENT)
        self.test_name = TextInput(hint_text="Test Name / Type", background_color=NIGHT_PANEL, foreground_color=LIGHT_TEXT, cursor_color=ACCENT)
        self.score = TextInput(hint_text="Score (0-100)", input_filter='int', background_color=NIGHT_PANEL, foreground_color=LIGHT_TEXT, cursor_color=ACCENT)
        self.notes = TextInput(hint_text="Notes (optional)", multiline=True, background_color=NIGHT_PANEL, foreground_color=LIGHT_TEXT, cursor_color=ACCENT)
        self.add_widget(self.subject)
        self.add_widget(self.test_name)
        self.add_widget(self.score)
        self.add_widget(self.notes)
        self.add_widget(Button(text="Submit", on_press=self.submit_score, background_color=ACCENT, color=LIGHT_TEXT))
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            subject TEXT,
            test_name TEXT,
            score INTEGER,
            notes TEXT
        )''')
        conn.commit()
        conn.close()

    def submit_score(self, _):
        try:
            score_val = int(self.score.text)
            if not (0 <= score_val <= 100):
                raise ValueError
        except ValueError:
            Popup(title="Error", content=Label(text="Score must be 0-100", color=LIGHT_TEXT),
                  size_hint=(0.6, 0.3)).open()
            return

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO scores (date, subject, test_name, score, notes) VALUES (?, ?, ?, ?, ?)",
                  (datetime.now().strftime("%Y-%m-%d"),
                   self.subject.text,
                   self.test_name.text,
                   score_val,
                   self.notes.text))
        conn.commit()
        conn.close()
        self.subject.text = ""
        self.test_name.text = ""
        self.score.text = ""
        self.notes.text = ""
        self.parent_widget.list_view.refresh_list()

class ScoreListView(ScrollView):
    def __init__(self, parent_widget, **kwargs):
        super().__init__(**kwargs)
        self.parent_widget = parent_widget
        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)
        self.refresh_list()

    def refresh_list(self):
        self.layout.clear_widgets()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id, date, subject, test_name, score, notes FROM scores ORDER BY date DESC")
        for row in c.fetchall():
            score_id, date, subject, test_name, score, notes = row
            item_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=60)
            label = Label(
                text=f"{date} | {subject} | {test_name} | Score: {score}\nNotes: {notes}",
                size_hint_x=0.8, color=LIGHT_TEXT
            )
            delete_btn = Button(text="Delete", size_hint_x=0.2, background_color=(0.7, 0.2, 0.2, 1), color=LIGHT_TEXT)
            delete_btn.bind(on_press=lambda _, sid=score_id: self.delete_score(sid))
            item_box.add_widget(label)
            item_box.add_widget(delete_btn)
            self.layout.add_widget(item_box)
        conn.close()

    def delete_score(self, score_id):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM scores WHERE id=?", (score_id,))
        conn.commit()
        conn.close()
        self.refresh_list()

class StudyBuddyApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(TodoScreen(name='todo'))
        self.sm.add_widget(WeeklyPlannerScreen(name='weekly'))
        self.sm.add_widget(MonthlyPlannerScreen(name='monthly'))
        self.sm.add_widget(TimetableScreen(name='timetable'))
        self.sm.add_widget(TestScoreScreen(name='testscore'))

        root = StarryBackground(orientation='vertical')
        nav = BoxLayout(size_hint_y=None, height=50)
        for name, label in [
            ('todo', 'To-Do List'),
            ('weekly', 'Weekly Planner'),
            ('monthly', 'Monthly Planner'),
            ('timetable', 'Timetable'),
            ('testscore', 'Test Scores')
        ]:
            btn = Button(text=label, background_color=NIGHT_BTN, color=ACCENT2)
            btn.bind(on_release=lambda _, name=name: setattr(self.sm, 'current', name))
            nav.add_widget(btn)
        root.add_widget(nav)
        root.add_widget(self.sm)
        return root

if __name__ == '__main__':
    StudyBuddyApp().run()
