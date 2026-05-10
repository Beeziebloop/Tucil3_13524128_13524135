from src.gui.components.button import Button
from src.gui.components.slider import Slider
from src.gui.components.panel import Panel
from src.gui.components.label import Label
from src.gui.constants import *

class PlaybackView:
    def __init__(self, app):
        self.app = app
        self.panel = Panel(320, 620, 930, 90)
        self.components = []
        self.build()

    def build(self):
        self.components.clear()
        x = 340
        first_btn = Button(x, 640, 50, 40,'<<', self.app.playback.first_step)

        x += 60
        prev_btn = Button(x, 640, 50, 40, '<',self.app.playback.prev_step)

        x += 60
        play_btn = Button(x, 640, 70, 40, 'PLAY', self.app.playback.toggle_play)
        self.play_button = play_btn

        x += 80
        next_btn = Button(x, 640, 50, 40,'>', self.app.playback.next_step)

        x += 60
        last_btn = Button(x, 640, 50, 40, '>>', self.app.playback.last_step)

        x += 100
        slider = Slider(x, 640 + 18, 220, 100, 2000, 500, self.change_speed)
        self.slider = slider

        self.components.extend([first_btn, prev_btn, play_btn, next_btn, last_btn, slider])

    def change_speed(self, value):
        self.app.playback.set_speed(value)

    def update(self):
        if self.app.playback.playing:
            self.play_button.text = 'PAUSE'
        else:
            self.play_button.text = 'PLAY'

    def handle_event(self, event):
        for component in self.components:
            if hasattr(component, 'handle_event'):
                component.handle_event(event)

    def draw(self, screen):
        self.panel.draw(screen)
        self.update()

        for component in self.components:
            component.draw(screen)
            
        Label(1090, 640, self.app.playback.get_progress_text(), 18).draw(screen)