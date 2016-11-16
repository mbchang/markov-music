# This class handles all high level control and logic for the app while it is
# in chord selection mode (as opposed to playback mode).

from kivy.clock import Clock as kivyClock
from block_builder import *
from building_block import *

class ChordSelection(object):
    def __init__(self, audio_control, display):
        super(ChordSelection, self).__init__()
        self.audio_control = audio_control
        self.display = display
        self.block_builder = BlockBuilder()

        self.active = False

    def on_click(self, pos):
        # Handle clicks!!!
        pass

    # Just a testing function.
    def test_play_note(self):
        self.audio_control.play_note(60)

    def test_play_chord(self):
        chord = Chord()
        self.audio_control.play_chord(chord)

    def activate(self):
        self.active = True
        print 'cs activate'
        # Reactivate the display.
        self.display.activate()

    def inactivate(self):
        print 'cs inactivate'
        self.active = False
        # Tell this display to translate down to make room for the
        # playback display.
        self.display.inactivate()

    def on_update(self):
        # Update the display here instead of at the widget/canvas level.
        dt = kivyClock.frametime
        self.display.on_update(dt)
        self.audio_control.on_update()
