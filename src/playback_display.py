''' This file contains the classes needed for graphics for playback mode. '''

from common_display import *

class PlaybackDisplay(Widget):
    def __init__(self, audio_control):
        super(PlaybackDisplay, self).__init__()
        self.audio_control = audio_control
        # Add a translate. This can be used to switch between chord selection
        # mode and playback mode.
        # self.translate = Translate()
        # self.add(self.translate)
        self.anim_group = AnimGroup()
        self.canvas.add(self.anim_group)
        self.audio_control.set_click_gfx(self.create_bubbles)
        self.audio_control.set_note_gfx(self.create_background_bubbles)
        self.last_touch_pos = None


    def on_touch_down(self, touch):
        x_pos, y_pos = touch.spos
        num_y_blocks = 4
        y_block = int(y_pos * num_y_blocks)
        num_x_blocks = 10
        x_block = int(x_pos * num_x_blocks)
        self.last_touch = touch
        self.audio_control.touch_down_block_handler(x_block,y_block,num_x_blocks)
        
    def create_bubbles(self):
        for i in range(8):
            rmb = RandomMovingBubble(self.last_touch.pos)
            self.anim_group.add(rmb)

    def create_background_bubbles(self):
        duration = 1.5
        fun_bubble1 = BubbleWiggleToCenter((0,0), 15, (0,1,0), duration = duration)
        fun_bubble2 = BubbleWiggleToCenter((Window.width,0), 15, (0,1,0), duration = duration)
        fun_bubble3 = BubbleWiggleToCenter((0,Window.height), 15, (0,1,0), duration = duration)
        fun_bubble4 = BubbleWiggleToCenter((Window.width,Window.height), 15, (0,1,0), duration = duration)

        self.anim_group.add(fun_bubble1)
        self.anim_group.add(fun_bubble2)
        self.anim_group.add(fun_bubble3)
        self.anim_group.add(fun_bubble4)


    def activate(self):
        self.line1 = LineDivider((-5,Window.height/4.),(Window.width+5,Window.height/4.),(1,0,0,0.6))
        self.line2 = LineDivider((-5,Window.height/2.),(Window.width+5,Window.height/2.),(1,0,0,0.6))
        self.line3 = LineDivider((-5,3*Window.height/4.),(Window.width+5,3*Window.height/4.),(1,0,0,0.6))
        self.anim_group.add(self.line1)
        self.anim_group.add(self.line2)
        self.anim_group.add(self.line3)



    def inactivate(self):
        self.anim_group.clear_all()

    def on_update(self, dt):
        self.anim_group.on_update()

