from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

# Placeholder screens for each module
class CalendarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Calendar Interface (Home)"))

class DailyPlannerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Daily Planner Page"))

class WeeklyPlannerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Weekly Planner Page"))

class TestScoreScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Test Score Tracker"))

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Settings"))

# Navigation bar at the bottom
class NavBar(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = 0.1
        buttons = [
            ("Home", "calendar"),
            ("Daily", "daily"),
            ("Weekly", "weekly"),
            ("Scores", "scores"),
            ("Settings", "settings"),
        ]
        for label, screen_name in buttons:
            btn = Button(text=label)
            def switch_screen(instance, sn=screen_name):
                screen_manager.current = sn
            btn.bind(on_release=switch_screen)
            self.add_widget(btn)

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.sm = ScreenManager()
        self.sm.add_widget(CalendarScreen(name="calendar"))
        self.sm.add_widget(DailyPlannerScreen(name="daily"))
        self.sm.add_widget(WeeklyPlannerScreen(name="weekly"))
        self.sm.add_widget(TestScoreScreen(name="scores"))
        self.sm.add_widget(SettingsScreen(name="settings"))
        self.add_widget(self.sm)
        self.add_widget(NavBar(self.sm))

class StudyPlannerApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    StudyPlannerApp().run()
