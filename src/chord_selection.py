# This class handles all high level control and logic for the app while it is
# in chord selection mode (as opposed to playback mode).

from kivy.clock import Clock as kivyClock
from block_builder import *
from building_block import *
from chord_selection_display import *
from graph import ChordGraph, PhraseBank

class ChordSelection(object):
    def __init__(self, audio_control, display):
        super(ChordSelection, self).__init__()
        self.audio_control = audio_control
        self.display = display
        self.graph = ChordGraph()
        self.phrase_bank = PhraseBank()

        self.phrase_length = 8
        # Initialize display with the node button callback.
        self.display.set_node_button_callback(self.on_node_button_click)
        self.display.set_play_button_callback(self.on_play_button_click)
        self.display.set_undo_button_callback(self.on_undo_button_click)
        self.display.set_save_button_callback(self.on_save_button_click)
        self.display.set_preview_button_callback(self.on_preview_button_click)
        self.display.set_phrase_length(self.phrase_length)
        self.block_builder = BlockBuilder()

        self.active = False

        # Initialize some chords.
        self.display.set_chords(self.graph.get_children())

    def on_save_button_click(self, instance):
        self.phrase_bank.add_to_bank(Phrase(self.block_builder.get_current_blocks()))
        # After saving, reset everything.
        self.graph.reset()
        self.display.reset()
        self.display.set_chords(self.graph.get_children())
        self.block_builder.clear_blocks()

    def on_undo_button_click(self, instance):
        if self.block_builder.remove_block() is not None:
            self.display.pop_preview_button()
            self.graph.undo_selection()
            self.display.set_chords(self.graph.get_children())
            self.toggle_save_button()

    def on_play_button_click(self, instance):
        self.audio_control.play_progression(self.block_builder.get_current_blocks())

    def on_node_button_click(self, instance):
        self.audio_control.play_chord(instance.chord)
        # Make a selection: update both the block builder and the display.
        if self.block_builder.add_block(instance.chord) < 0:
            # Already at max phrase length.
            return
        self.display.add_node_to_progression(instance.chord)
        # Get next set of possible chords.
        self.graph.make_selection(instance.chord)
        self.display.set_chords(self.graph.get_children())
        # Show save button only when length of current phrase is 4 or 8.
        self.toggle_save_button()

    def toggle_save_button(self):
        if self.block_builder.get_num_blocks() == 4 or self.block_builder.get_num_blocks() == 8:
            self.display.show_save_button()
        else:
            self.display.hide_save_button()

    def on_preview_button_click(self, instance):
        self.audio_control.play_chord(instance.chord)

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
