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

    def on_touch_down(self, touch):
        x_pos, y_pos = touch.spos
        num_y_blocks = 4
        y_block = int(y_pos * num_y_blocks)
        num_x_blocks = 10
        x_block = int(x_pos * num_x_blocks)
        self.audio_control.touch_down_block_handler(x_block,y_block,num_x_blocks)
        rmb = RandomMovingBubble(touch.pos)
        self.anim_group.add(rmb)

    def activate(self):
        pass

    def inactivate(self):
        pass

    def on_update(self, dt):
        self.anim_group.on_update()

