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
        self.display.set_undo_phrase_ctrl_button_callback(self.on_undo_phrase_ctrl_button_click)

        self.active = False

        # Mode is either 'chords' or 'phrases'
        self.mode = 'chords'

        # The block_builder builds phrases together and clears after each
        # phrase is made.
        # The song_builder builds the entire song and persistently stores it.
        self.block_builder = BlockBuilder()
        self.song_builder = BlockBuilder()

        # phrase length
        # this controls the phrase length
        self.phrase_length = None
        self.display.set_phrase_control_callback(self.on_phrase_control_button_click)
        self.display.set_phrase_length_csl_callback(self.on_phrase_length_csl_button_click)
        self.display.set_start_chord_select_callback(self.on_start_chord_button_click)
        self.display.set_end_chord_select_callback(self.on_end_chord_button_click)


        # Initialize graph
        self.display.set_phrase_controls()

        # For voice leading.
        self.chords_with_voice_leading = []
        self.chords_to_save = []

    def get_children_from_graph(self):
        self.chords_with_voice_leading = self.graph.get_children()
        next_chords = map(lambda x: x[0], self.chords_with_voice_leading)
        return next_chords

    def get_progression_from_chord(self, chord):
        """
            Return the entire progression with inversions, when the user
            selects a particular chord.
        """
        progression = None
        for c, p in self.chords_with_voice_leading:
            if c == chord:
                progression = p
                break
        assert(progression is not None)
        return progression

    # Reset the display to the beginning of chord building.
    # Does not erase the entire song, because the entire song is persistent
    # and we may want to switch back to it later.
    def reset_chord_building(self):
        self.graph.reset()
        self.block_builder.clear_blocks()
        self.display.reset()
        self.display.set_phrase_controls()
        self.display.info.text = ""

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
            # Only do anything if there are actually blocks in the block_builder.
            if self.block_builder.get_num_blocks() > 0:
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
                self.display.set_chords(self.get_children_from_graph())
                self.toggle_undo_button()
                self.toggle_play_button()
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
            self.display.hide_undo_phrase_ctrl_button()
            self.audio_control.play_chord(instance.block)
            # Get the progression with correct inversions.
            chords_to_save = self.get_progression_from_chord(instance.block)
            # If this exceeds max number of blocks allowed, return.
            if self.block_builder.set_blocks(chords_to_save) < 0:
                return
            self.chords_to_save = chords_to_save
            self.display.reset()
            for c in self.chords_to_save:
                self.display.add_node_to_progression(c, self.mode)
            # Get next set of possible chords.
            self.graph.make_selection(instance.block)
            # if not self.graph.at_end:
            self.display.set_chords(self.get_children_from_graph())
            self.toggle_undo_button()
            self.toggle_play_button()
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

    def toggle_play_button(self):
        if self.block_builder.get_num_blocks() > 0:
            self.display.show_play_button()
        else:
            self.display.hide_play_button()

    def toggle_undo_button(self):
        if self.block_builder.get_num_blocks() > 0:
            self.display.show_undo_button()
        else:
            self.display.hide_undo_button()

    def toggle_save_button(self):
        if self.block_builder.get_num_blocks() > 1:
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
            self.reset_chord_building()  # this is a problem
            self.audio_control.clear_previous_previews()
            self.display.set_change_mode_button_text('Go To Phrase Mode')
        elif self.mode == 'chords':
            # Switch back to phrase building mode.
            # Requires reloading the previously saved song.
            self.mode = 'phrases'
            self.load_phrase_builder()
            self.display.hide_undo_phrase_ctrl_button()
            self.display.show_save_button()
            self.display.show_undo_button()
            self.display.show_play_button()
            self.display.set_change_mode_button_text('Go To Chord Mode')
        else:
            raise ModeException()

    def on_phrase_control_button_click(self, instance):
        if instance.label == 'Unconstrained':
            self.phrase_length = 8
            self.display.add_phrase_length_label(self.phrase_length)
            self.create_graph_and_builders(self.phrase_length)
        else:
            self.display.set_phrase_length_csl()  # this will set self.phrase_length and do everything else

    def create_graph_and_builders(self, phrase_length, start_chord_name=None, end_chord_name=None):
        # add constraints based on start and end
        self.display.chord_selection_layout.instructions.text = ""
        self.graph.set_max_steps(phrase_length)
        if start_chord_name is not None:
            self.graph.set_chord(1, start_chord_name)  # 1 indexed
        if end_chord_name is not None:
            self.graph.set_chord(phrase_length, end_chord_name)

        # here you should restart if there is no path
        if self.graph.no_path:
            self.display.info.text = "These constraints are not possible!"
            self.reset_chord_building()
            return

        self.display.set_phrase_length(phrase_length)

        # The block_builder builds phrases together and clears after each
        # phrase is made.
        # The song_builder builds the entire song and persistently stores it.
        # self.block_builder = BlockBuilder(phrase_length=phrase_length)
        # self.song_builder = BlockBuilder(phrase_length=phrase_length*5)
        self.block_builder.set_phrase_length(phrase_length)
        self.song_builder.set_phrase_length(40)
        self.display.set_chords(self.get_children_from_graph())

    def on_phrase_length_csl_button_click(self, instance):
        self.phrase_length = int(instance.label)
        self.display.add_phrase_length_label(self.phrase_length)
        self.display.set_chord_preselect('start')

    def on_start_chord_button_click(self, instance):
        self.start_chord_name = instance.label
        self.display.add_start_chord_label(self.start_chord_name)
        self.display.set_chord_preselect('end')

    def on_end_chord_button_click(self, instance):
        self.end_chord_name = instance.label
        self.display.add_end_chord_label(self.end_chord_name)
        self.create_graph_and_builders(self.phrase_length, self.start_chord_name, self.end_chord_name)

    def on_undo_phrase_ctrl_button_click(self, instance):
        # Reset everything.
        self.reset_chord_building()

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
