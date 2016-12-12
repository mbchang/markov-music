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
from kivy.uix.label import Label

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


class BubbleWiggleToCenter(InstructionGroup):
    def __init__(self, pos, r, color, duration = 3):
        super(BubbleWiggleToCenter, self).__init__()

        center_x = Window.width/2
        center_y = Window.height/2
        x = []
        x.append((0,r))
        # this creates a bunch of tuples so that we can make a kfanim across
        # a lot of different points. It basically adds a sin wave on top of the
        # regularly scheduled decrease in radius
        for i in range(100):
            time = .1 + i*duration/100.
            radius = 2 * r * (100. - i) / 100 * (1 + 0.2 * np.sin(i / 2.))
            x.append((time, radius))

        self.radius_anim = KFAnim(*x)

        # the position still goes linearly
        self.pos_anim = KFAnim((0, pos[0], pos[1]), (duration, center_x, center_y))

        self.color = Color(*color)
        self.add(self.color)

        self.circle = CEllipse(cpos = pos, size = (2*r, 2*r), segments = 40)
        self.add(self.circle)

        self.time = 0
        self.on_update(0)

    def on_update(self, dt):
        # animate radius
        rad = self.radius_anim.eval(self.time)
        self.circle.csize = (2*rad, 2*rad)

        # animate position
        pos = self.pos_anim.eval(self.time)
        self.circle.cpos = pos

        # advance time
        self.time += dt
        # continue flag
        return self.radius_anim.is_active(self.time)




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

class LineDivider(InstructionGroup):
    def __init__(self,first_point,second_point,rgba):
        super(LineDivider, self).__init__()
        self.first_point = first_point
        self.second_point = second_point
        self.color = Color(*rgba)
        self.add(self.color)
        self.points = [first_point[0],first_point[1],second_point[0],second_point[1]]
        self.line = Line(points=self.points,width=5)
        self.add(self.line)

    def on_update(self, dt):
        return True

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


