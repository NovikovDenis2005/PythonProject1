from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.widget import Widget
from game import Game

class CellWidget(Button):
    def __init__(self, r, c, cell, **kwargs):
        super().__init__(**kwargs)
        self.r = r
        self.c = c
        self.cell = cell
        self.background_normal = ''
        self.background_color = [0, 0, 0, 0]
        self.text = ''
        with self.canvas.before:
            self.draw_cell(cell)

    def draw_cell(self, ch):
        self.canvas.before.clear()
        with self.canvas.before:
            if ch == '#':
                Color(0.2, 0.2, 0.2, 1)
                Rectangle(pos=self.pos, size=self.size)
            elif ch == '.':
                Color(1, 1, 1, 1)
                Rectangle(pos=self.pos, size=self.size)
            elif ch.lower() == 'r':
                Color(1, 0, 0, 1)
                Ellipse(pos=self.pos, size=self.size)
            elif ch.lower() == 'g':
                Color(0, 1, 0, 1)
                Ellipse(pos=self.pos, size=self.size)
            elif ch.lower() == 'b':
                Color(0, 0, 1, 1)
                Ellipse(pos=self.pos, size=self.size)
            elif ch.upper() in 'RGB':
                Color(0.8, 0.8, 0.8, 1)
                Rectangle(pos=self.pos, size=self.size)

    def on_size(self, *args):
        self.draw_cell(self.cell)

    def on_pos(self, *args):
        self.draw_cell(self.cell)

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid_widget = GridLayout(cols=1)
        self.add_widget(self.grid_widget)
        self.level = 1
        self.load_level()

    def load_level(self):
        try:
            self.game = Game.load_level(f"levels/level_0{self.level}.txt")
            self.update_grid()
        except FileNotFoundError:
            self.grid_widget.clear_widgets()
            self.grid_widget.add_widget(Button(text="Все уровни пройдены!"))

    def update_grid(self):
        self.grid_widget.clear_widgets()
        layout = GridLayout(cols=self.game.cols, size_hint=(1, 1))
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                cell = self.game.get_cell(r, c)
                btn = CellWidget(r, c, cell)
                btn.bind(on_press=self.make_handler(r, c))
                layout.add_widget(btn)
        self.grid_widget.add_widget(layout)

    def make_handler(self, r, c):
        def handler(instance):
            if not self.game.selected_ball:
                self.game.select_ball(r, c)
            else:
                self.game.move_selected(r, c)
                if self.game.check_win():
                    self.level += 1
                    self.load_level()
            self.update_grid()
        return handler

class KugameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(GameScreen(name='game'))
        return sm
