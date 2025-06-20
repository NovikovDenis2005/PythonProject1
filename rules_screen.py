from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

class RulesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        scroll = ScrollView()
        label = Label(text=self.load_rules(), size_hint_y=None)
        label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        scroll.add_widget(label)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def load_rules(self):
        try:
            with open('rules.html', 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "Файл правил не найден."