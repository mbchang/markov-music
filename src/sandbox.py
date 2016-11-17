import sys
sys.path.append('..')
from kivy.config import Config

# Import all necessary classes.
from chord_selection import *
from audio_control import *
from playback import *
from chord_selection_display import *
from playback_display import *

import random
import numpy as np

class MainTest(BaseWidget):
    def __init__(self):
        super(MainTest, self).__init__()
        self.test_widget = TestWidget()
        self.add_widget(self.test_widget)

class TestWidget(Widget):
    def __init__(self):
        super(TestWidget, self).__init__()
        self.test_layout = TestLayout((200,400), (800,300))
        self.add_widget(self.test_layout)

class TestLayout(RelativeLayout):
    def __init__(self, pos=(200,400), size=(800,300)):
        super(TestLayout, self).__init__()
        self.size = size
        self.pos = pos
        self.canvas.add(Color(1.0, 0, 0))
        print self.pos, self.size
        self.canvas.add(Rectangle(size=self.size))
        self.button = TestButton('Print Me', text='Press Me', size_hint=(.2,.2))
        self.add_widget(self.button)
        self.button.bind(on_press=self.button_callback)

    def button_callback(self, instance):
        print instance.string


class TestButton(Button):
    def __init__(self, string, **kwargs):
        super(TestButton, self).__init__(**kwargs)
        self.string = string

run(MainTest)