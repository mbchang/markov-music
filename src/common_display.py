# This file contains the common graphical elements that can be used by both
# ChordSelectionDisplay and PlaybackDisplay.

import sys
from common.gfxutil import *

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate

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

