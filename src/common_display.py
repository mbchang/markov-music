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
import random
import math

# A menu button.
class MenuButton(Button):
    def __init__(self, pos_hint, size_hint, label):
        super(MenuButton, self).__init__(pos_hint=pos_hint, size_hint=size_hint, text=label)
        self.label = label
        self.background_normal = ''
        self.background_color = [0, .7, 0, .8]

    def set_background_color(self, rgba):
        self.background_color = rgba

    def set_text_color(self, rgb):
        sel.color = rgb

    def set_callback(self, callback):
        self.bind(on_press=callback)

# A button representing a node in the graph (either a chord or phrase.)
class NodeButton(Button):
    def __init__(self, pos_hint, size_hint, block, preview=False):
        super(NodeButton, self).__init__(pos_hint=pos_hint, size_hint=size_hint, text=block.get_name())
        self.block = block
        self.background_normal = ''
        if preview:
            self.background_color = [0, .2, .8, .8]
            # self.background_color = [.8, 0, .2, .8]
        else:
            self.background_color = [0, .2, .8, .8]

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

class RandomMovingBubble(InstructionGroup):
    def __init__(self, pos, size=40):
        super(RandomMovingBubble, self).__init__()
        self.pos = pos
        self.size = size
        h = random.random()
        self.color = Color(hsv=(h,1,1))
        self.add(self.color)
        self.ellipse = CEllipse(cpos=pos, csize=(1, 1))
        self.add(self.ellipse)
        self.angle = random.random() * 2 * math.pi
        total_distance = ((Window.height ** 2 + Window.width ** 2) ** 0.5) / 2.
        final_pos_x = self.pos[0] + total_distance * math.sin(self.angle)
        final_pos_y = self.pos[1] + total_distance * math.cos(self.angle)
        self.pos_anim = KFAnim((0,self.pos[0],self.pos[1]),(1.5,final_pos_x,final_pos_y))
        self.size_anim = KFAnim((0,0),(0.2, self.size),(1.5,0))
        self.time = 0

    def on_update(self, dt):
        self.time += dt
        new_pos = self.pos_anim.eval(self.time)
        new_size = self.size_anim.eval(self.time)
        self.ellipse.cpos = new_pos
        self.ellipse.csize = (new_size,new_size)
        return self.pos_anim.is_active(self.time)


