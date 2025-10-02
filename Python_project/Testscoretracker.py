from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from datetime import datetime
import sqlite3

DB_PATH = "test_scores.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
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

class ScoreInputForm(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.subject = TextInput(hint_text="Subject Name")
        self.test_name = TextInput(hint_text="Test Name / Type")
        self.score = TextInput(hint_text="Score (0-100)", input_filter='int')
        self.notes = TextInput(hint_text="Notes (optional)", multiline=True)
        self.add_widget(self.subject)
        self.add_widget(self.test_name)
        self.add_widget(self.score)
        self.add_widget(self.notes)
        self.add_widget(Button(text="Submit", on_press=self.submit_score))

    def submit_score(self, instance):
        try:
            score_val = int(self.score.text)
            if not (0 <= score_val <= 100):
                raise ValueError
        except ValueError:
            Popup(title="Error", content=Label(text="Score must be 0-100"), size_hint=(0.6, 0.3)).open()
            return

        conn = sqlite3.connect(DB_PATH)
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
        App.get_running_app().root.ids.list_view.refresh_list()

class ScoreListView(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)
        self.refresh_list()

    def refresh_list(self):
        self.layout.clear_widgets()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT date, subject, test_name, score, notes FROM scores ORDER BY date DESC")
        for row in c.fetchall():
            date, subject, test_name, score, notes = row
            label = Label(
                text=f"{date} | {subject} | {test_name} | Score: {score}\nNotes: {notes}",
                size_hint_y=None, height=60
            )
            self.layout.add_widget(label)
        conn.close()

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.input_form = ScoreInputForm()
        self.list_view = ScoreListView()
        self.list_view.id = "list_view"
        self.ids = {"list_view": self.list_view}
        self.add_widget(self.input_form)
        self.add_widget(Label(text="--- Test Scores ---", size_hint_y=None, height=30))
        self.add_widget(self.list_view)
class ScoreListView(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)
        self.refresh_list()

    def refresh_list(self):
        self.layout.clear_widgets()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, date, subject, test_name, score, notes FROM scores ORDER BY date DESC")
        for row in c.fetchall():
            score_id, date, subject, test_name, score, notes = row
            item_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=60)
            label = Label(
                text=f"{date} | {subject} | {test_name} | Score: {score}\nNotes: {notes}",
                size_hint_x=0.8
            )
            delete_btn = Button(text="Delete", size_hint_x=0.2)
            delete_btn.bind(on_press=lambda instance, sid=score_id: self.delete_score(sid))
            item_box.add_widget(label)
            item_box.add_widget(delete_btn)
            self.layout.add_widget(item_box)
        conn.close()

    def delete_score(self, score_id):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM scores WHERE id=?", (score_id,))
        conn.commit()
        conn.close()
        self.refresh_list()

class TestScoreApp(App):
    def build(self):
        init_db()
        return MainScreen()

if __name__ == "__main__":
    TestScoreApp().run()
