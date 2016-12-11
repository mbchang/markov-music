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

        # Initialize display with the node button callback.
        self.display.set_node_button_callback(self.on_node_button_click)
        self.display.set_play_button_callback(self.on_play_button_click)
        self.display.set_undo_button_callback(self.on_undo_button_click)
        self.display.set_save_button_callback(self.on_save_button_click)
        self.display.set_preview_button_callback(self.on_preview_button_click)
        self.display.set_change_mode_button_callback(self.on_change_mode_button_click)

        self.active = False

        # Mode is either 'chords' or 'phrases'
        self.mode = 'chords'

        # phrase length
        # this controls the phrase length
        self.phrase_length = None
        self.display.set_phrase_control_callback(self.on_phrase_control_button_click)
        self.display.set_phrase_length_csl_callback(self.on_phrase_length_csl_button_click)
        self.display.set_start_chord_select_callback(self.on_start_chord_button_click)
        self.display.set_end_chord_select_callback(self.on_end_chord_button_click)


        # Initialize graph
        self.display.set_phrase_controls()

        # all of this should be in the callback
        # {}
        # self.phrase_length = 8
        # self.graph.set_max_steps(self.phrase_length)
        # self.display.set_phrase_length(self.phrase_length)

        # # The block_builder builds phrases together and clears after each
        # # phrase is made.
        # # The song_builder builds the entire song and persistently stores it.
        # self.block_builder = BlockBuilder(phrase_length=8)
        # self.song_builder = BlockBuilder(phrase_length=40)

        # }



        # assert self.phrase_length is not None

        # Initialize some chords.
        # self.display.set_chords(self.graph.get_children())

    # Reset the display to the beginning of chord building.
    # Does not erase the entire song, because the entire song is persistent
    # and we may want to switch back to it later.
    def reset_chord_building(self):
        self.graph.reset()
        self.display.reset()
        self.display.set_chords(self.graph.get_children())
        self.block_builder.clear_blocks()

    # Loads phrase building mode, takes existing phrases in the song
    # and displays them so the user can pick up where they left off.
    def load_phrase_builder(self):
        self.reset_chord_building()
        # Add all the phrases that are already in the song.
        for phrase in self.song_builder.get_current_blocks():
            self.display.add_node_to_progression(phrase, self.mode)
        # Display the correct next options.
        if self.song_builder.get_num_blocks() > 0:
            self.display.set_chords(self.phrase_bank.get_children(self.song_builder.get_last_block()))
        else:
            self.display.set_chords(self.phrase_bank.get_starting_phrases())

    def on_save_button_click(self, instance):
        if self.mode == 'chords':
            self.phrase_bank.add_to_bank(Phrase(self.block_builder.get_current_blocks()))
            # After saving, reset everything.
            self.reset_chord_building()
            # If this was the first phrase we added, we can now show the change mode
            # button. And from here on out, it just stays visible.
            if self.phrase_bank.get_num_phrases() == 1:
                self.display.show_change_mode_button()
        elif self.mode == 'phrases':
            pass
        else:
            raise ModeException()

    def on_undo_button_click(self, instance):
        if self.mode == 'chords':
            if self.block_builder.remove_block() is not None:
                self.display.pop_preview_button()
                self.graph.undo_selection()
                self.display.set_chords(self.graph.get_children())
                self.toggle_save_button()
        elif self.mode == 'phrases':
            self.audio_control.clear_previous_previews()
            if self.song_builder.remove_block() is not None:
                self.display.pop_preview_button()
                if self.song_builder.get_num_blocks() == 0:
                    self.display.set_chords(self.phrase_bank.get_starting_phrases())
                else:
                    self.display.set_chords(self.phrase_bank.get_children(self.song_builder.get_last_block()))

    def on_play_button_click(self, instance):
        if self.mode == 'chords':
            self.audio_control.play_preview(self.block_builder.get_flattened_chords())
        elif self.mode == 'phrases':
            self.audio_control.play_preview(self.song_builder.get_flattened_chords())
        else:
            raise ModeException()

    def on_node_button_click(self, instance):
        if self.mode == 'chords':
            self.audio_control.play_chord(instance.block)
            # Make a selection: update both the block builder and the display.
            if self.block_builder.add_block(instance.block) < 0:
                # Already at max phrase length.
                return
            self.display.add_node_to_progression(instance.block, self.mode)
            # Get next set of possible chords.
            self.graph.make_selection(instance.block)
            self.display.set_chords(self.graph.get_children())
            # Show save button only when length of current phrase is 4 or 8.
            self.toggle_save_button()
        elif self.mode == 'phrases':
            self.audio_control.play_preview(instance.block.get_chords())
            if self.song_builder.add_block(instance.block) < 0:
                return
            # Add this phrase.
            self.display.add_node_to_progression(instance.block, self.mode)
            # Update the next options.
            self.display.set_chords(self.phrase_bank.get_children(instance.block))
        else:
            raise ModeException()

    def toggle_save_button(self):
        if self.block_builder.get_num_blocks() == 4 or self.block_builder.get_num_blocks() == 8:
            self.display.show_save_button()
        else:
            self.display.hide_save_button()

    def on_preview_button_click(self, instance):
        if self.mode == 'chords':
            self.audio_control.play_chord(instance.block)
        elif self.mode == 'phrases':
            self.audio_control.play_preview(instance.block.get_chords())
        else:
            raise ModeException()

    def on_change_mode_button_click(self, instance):
        # Toggle mode.
        if self.mode == 'phrases':
            self.mode = 'chords'
            # Switch back to chord building mode.
            self.reset_chord_building()
            self.audio_control.clear_previous_previews()
            self.display.set_change_mode_button_text('Go To Phrase Mode')
        elif self.mode == 'chords':
            # Switch back to phrase building mode.
            # Requires reloading the previously saved song.
            self.mode = 'phrases'
            self.load_phrase_builder()
            self.display.set_change_mode_button_text('Go To Chord Mode')
        else:
            raise ModeException()

    def on_phrase_control_button_click(self, instance):
        if instance.label == 'Unconstrained':
            self.phrase_length = 8
            self.create_graph_and_builders(self.phrase_length)
        else:
            self.phrase_length = 3  # you have to do something else here
            self.display.set_phrase_length_csl()  # this will set self.phrase_length and do everything else

    def create_graph_and_builders(self, phrase_length):
        # add constraints based on start and end

        self.graph.set_max_steps(phrase_length)
        self.display.set_phrase_length(phrase_length)

        # The block_builder builds phrases together and clears after each
        # phrase is made.
        # The song_builder builds the entire song and persistently stores it.
        self.block_builder = BlockBuilder(phrase_length=phrase_length)
        self.song_builder = BlockBuilder(phrase_length=phrase_length*5)
        self.display.set_chords(self.graph.get_children())      

    def on_phrase_length_csl_button_click(self, instance):
        self.phrase_length = int(instance.label)
        print 'phrase length', self.phrase_length
        self.display.set_chord_preselect('start')

    def on_start_chord_button_click(self, instance):
        self.start_chord_name = instance.label
        print 'start chord', self.start_chord_name
        self.display.set_chord_preselect('end')

    def on_end_chord_button_click(self, instance):
        self.end_chord_name = instance.label
        print 'end chord', self.end_chord_name
        self.create_graph_and_builders(self.phrase_length)

    # Just a testing function.
    def test_play_note(self):
        self.audio_control.play_note(60)

    def test_play_chord(self):
        chord = Chord()
        self.audio_control.play_chord(chord)

    # temporary method
    def get_song(self):
        return Phrase(chords=self.song_builder.get_flattened_chords())
        # return Phrase(chords=[Chord(),Chord(),Chord(),Chord()])

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

class ModeException(Exception):
    def __init__(self, text=''):
        super(ModeException, self).__init__('Mode should be one of phrases or chords. ' + text)
