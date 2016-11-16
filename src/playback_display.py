''' This file contains the classes needed for graphics for playback mode. '''

from common_display import *

class PlaybackDisplay(InstructionGroup):
    def __init__(self):
        super(PlaybackDisplay, self).__init__()
        # Add a translate. This can be used to switch between chord selection
        # mode and playback mode.
        self.translate = Translate()
        self.add(self.translate)

    def activate(self):
        self.translate.y = 0

    def inactivate(self):
        self.translate.y = -10000

    def on_update(self, dt):
        pass
