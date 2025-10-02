from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
import calendar
from datetime import datetime

# Starlight palette colors
STARLIGHT_BG = (0.93, 0.96, 1, 1)
STARLIGHT_HEADER = (0.82, 0.87, 1, 1)    
STARLIGHT_BTN = (0.80, 0.85, 1, 1)       
STARLIGHT_BTN_TODAY = (0.68, 0.76, 0.98, 1)
STARLIGHT_EVENT = (0.76, 0.70, 0.98, 1)
STARLIGHT_TEXT = (0.25, 0.30, 0.45, 1)   

class AppState:
    selected_date = datetime.today().date()
    events = {}

app_state = AppState()

def get_day_indicators(date_obj):
    return date_obj in app_state.events and len(app_state.events[date_obj]) > 0

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
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        # Removed background_color from BoxLayout

        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        # Removed background_color from BoxLayout
        prev_btn = Button(text='<', size_hint_x=None, width=50, on_release=self.prev_month,
                          background_normal='', background_color=STARLIGHT_BTN, color=STARLIGHT_TEXT)
        next_btn = Button(text='>', size_hint_x=None, width=50, on_release=self.next_month,
                          background_normal='', background_color=STARLIGHT_BTN, color=STARLIGHT_TEXT)
        today_btn = Button(text='Today', size_hint_x=None, width=80, on_release=self.goto_today,
                           background_normal='', background_color=STARLIGHT_BTN, color=STARLIGHT_TEXT)
        self.month_label = Label(text=self.get_month_year_str(), font_size=20, color=STARLIGHT_TEXT)
        header.add_widget(prev_btn)
        header.add_widget(self.month_label)
        header.add_widget(today_btn)
        header.add_widget(next_btn)
        layout.add_widget(header)

        days_grid = GridLayout(cols=7, size_hint_y=None, height=30)
        for day in calendar.day_abbr:
            days_grid.add_widget(Label(text=day, bold=True, color=STARLIGHT_TEXT))
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
        for date_obj in month_days:
            btn = Button(
                text=str(date_obj.day),
                background_normal='',
                background_color=STARLIGHT_BTN,
                color=STARLIGHT_TEXT,
                on_release=lambda _, d=date_obj: self.on_date_selected(d)
            )
            if date_obj.month != self.current_month:
                btn.background_color = (0.95, 0.97, 1, 1)
                btn.disabled = True
            if date_obj == today:
                btn.background_color = STARLIGHT_BTN_TODAY
            if get_day_indicators(date_obj):
                btn.text += " •"
                btn.color = STARLIGHT_EVENT
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

    def on_date_selected(self, date_obj):
        app_state.selected_date = date_obj
        self.manager.current = 'daily_planner'

class DailyPlannerScreen(Screen):
    def on_pre_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        # Removed background_color from BoxLayout
        date_str = app_state.selected_date.strftime('%A, %B %d, %Y')
        layout.add_widget(Label(text=f"Daily Planner for {date_str}", font_size=24, color=STARLIGHT_TEXT))

        events = app_state.events.get(app_state.selected_date, [])
        for event in events:
            layout.add_widget(Label(text=f"- {event}", font_size=18, color=STARLIGHT_EVENT))

        self.task_input = TextInput(hint_text="Enter your event/task here", size_hint_y=None, height=40,
                                   background_color=(1, 1, 1, 1), foreground_color=STARLIGHT_TEXT)
        layout.add_widget(self.task_input)

        add_btn = Button(text="Add Event", size_hint_y=None, height=40, on_release=self.add_event,
                         background_normal='', background_color=STARLIGHT_BTN, color=STARLIGHT_TEXT)
        layout.add_widget(add_btn)

        back_btn = Button(text="Back to Calendar", size_hint_y=None, height=50, on_release=self.go_back,
                          background_normal='', background_color=STARLIGHT_HEADER, color=STARLIGHT_TEXT)
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def add_event(self, _):
        task = self.task_input.text.strip()
        if task:
            app_state.events.setdefault(app_state.selected_date, []).append(task)
            self.task_input.text = ""
            self.on_pre_enter()

    def go_back(self, _):
        self.manager.current = 'calendar'

class CalendarApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(CalendarScreen(name='calendar'))
        sm.add_widget(DailyPlannerScreen(name='daily_planner'))
        return sm

if __name__ == '__main__':
    CalendarApp().run()
