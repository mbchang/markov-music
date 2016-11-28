# Main entry point for Markov Music.

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

class MarkovMusicWidget(BaseWidget):
    def __init__(self):
        super(MarkovMusicWidget, self).__init__()
        # Create audio control.
        self.audio_control = AudioController()

        # An info display, for debugging and possibly for actual info.
        self.info = topleft_label()
        # self.add_widget(self.info)

        # Create an instance of each display and add to canvas.
        self.cs_display = ChordSelectionScreen()
        self.add_widget(self.cs_display)


        # self.canvas.add(self.p_display)
        self.p_display = PlaybackDisplay(self.audio_control)
        self.add_widget(self.p_display)

        # Two main modes. ChordSelection and Playback.
        self.cs = ChordSelection(self.audio_control, self.cs_display)
        self.p = Playback(self.audio_control, self.p_display)

        # Flag for which mode we are in.
        # True = chord selection, False = playback.
        self.cs_mode = True
        # # Activate chord selection and keep playback deactivated.
        # self.change_mode_cs()

    # Handle any key events.
    def on_key_down(self, keycode, modifiers):

        if keycode[1] == 't':
            self.toggle_mode()

    def on_touch_down(self, touch):
        if self.cs_mode:
            self.cs_display.dispatch('on_touch_down', touch)
        else:
            self.p_display.dispatch('on_touch_down', touch)

    def on_key_up(self, keycode):
        pass

    # Switch between chord selection and playback modes.
    def toggle_mode(self):
        if self.cs_mode:
            self.change_mode_p()
        else:
            self.change_mode_cs()

    def change_mode_cs(self):
        self.p.inactivate()
        self.cs_mode = True
        self.cs.activate()

    def change_mode_p(self):
        self.cs.inactivate()
        song = self.cs.get_song()
        self.cs_mode = False
        self.p.activate()
        self.p.set_song(song)
        self.p.play()

    # Need to update all components.
    def on_update(self):
        self.info.text = "Markov Music!"

        if self.cs_mode:
            self.cs.on_update()
        else:
            self.p.on_update()

# Set to full screen (commented out because unnecessary while developing).
# Config.set('graphics', 'fullscreen', 0)
# Config.write()
run(MarkovMusicWidget)
