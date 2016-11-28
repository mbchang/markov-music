# This file contains the common graphical elements that can be used by both
# ChordSelectionDisplay and PlaybackDisplay.

import sys
from common.gfxutil import *

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button

# A menu button.
class MenuButton(Button):
    def __init__(self, pos_hint, size_hint, label):
        super(MenuButton, self).__init__(pos_hint=pos_hint, size_hint=size_hint, text=label)
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback
        self.bind(on_press=self.callback)

# A button representing a node in the graph (either a chord or phrase.)
class NodeButton(Button):
    def __init__(self, pos_hint, size_hint, block):
        super(NodeButton, self).__init__(pos_hint=pos_hint, size_hint=size_hint, text=block.get_name())
        self.block = block

    def set_callback(self, callback):
        self.bind(on_press=callback)

# A generic bubble.
class Bubble(InstructionGroup):
    def __init__(self, pos, rgb, size):
        super(Bubble, self).__init__()
        self.pos = pos
        self.size = size
        self.color = Color(*rgb)

        self.add(self.color)
        self.ellipse = CEllipse(cpos=pos, csize=(self.size, self.size))
        self.add(self.ellipse)

    def set_color(self, rgb):
        self.color.rgb = rgb

    def set_alpha(self, a):
        self.color.a = a

    def set_pos(self, pos):
        self.pos = pos
        self.ellipse.set_pos(pos)

    def on_update(self, dt):
        pass


