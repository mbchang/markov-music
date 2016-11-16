''' This file contains all necessary elements that are specific to chord
selection display. '''

from common_display import *
from building_block import *

class ChordSelectionScreen(Widget):
    def __init__(self):
        super(ChordSelectionScreen, self).__init__()

        # Contains two layouts.
        self.current_progression_layout = CurrentProgressionLayout((20, Window.height - 200),
                                                                   (Window.width - 40, 200))
        self.chord_selection_layout = ChordSelectionLayout((20, 20),
                                                           (Window.width - 40, Window.height - 200))
        self.add_widget(self.current_progression_layout)
        self.add_widget(self.chord_selection_layout)

    def set_chords(self, chords):
        self.chord_selection_layout.set_chords(chords)

    def pop_preview_button(self):
        self.current_progression_layout.pop_preview_button()

    def set_preview_button_callback(self, callback):
        self.current_progression_layout.set_preview_button_callback(callback)

    def set_node_button_callback(self, callback):
        self.chord_selection_layout.set_node_button_callback(callback)

    def set_play_button_callback(self, callback):
        self.current_progression_layout.set_play_button_callback(callback)

    def set_undo_button_callback(self, callback):
        self.current_progression_layout.set_undo_button_callback(callback)

    def add_node_to_progression(self, chord):
        self.current_progression_layout.add_preview_button(chord)

    def set_phrase_length(self, phrase_length):
        self.current_progression_layout.set_phrase_length(phrase_length)

    def on_update(self, dt):
        pass

class CurrentProgressionLayout(RelativeLayout):
    def __init__(self, pos, size, phrase_length=8):
        super(CurrentProgressionLayout, self).__init__()
        self.pos = pos
        self.size = size
        self.phrase_length = phrase_length
        self.canvas.add(Color(1.0, 0, 0))
        self.canvas.add(Rectangle(size=self.size))

        self.preview_buttons = []
        self.preview_button_callback = None

        play_pos_hint = {'center_x': .9, 'center_y': .3}
        play_size_hint = (.15, .3)
        self.play_button = MenuButton(play_pos_hint, play_size_hint, 'Play')
        self.add_widget(self.play_button)

        undo_pos_hint = {'center_x': .9, 'center_y': .6}
        undo_size_hint = (.15, .3)
        self.undo_button = MenuButton(undo_pos_hint, undo_size_hint, 'Undo')
        self.add_widget(self.undo_button)

    def add_preview_button(self, chord):
        # TODO: buttons are not vertically centered.
        pos_hint = {'center_x': .8*((1.0 + len(self.preview_buttons))/(1.0+self.phrase_length)), 'center_y': .5}
        size_hint = (1.0/(1 + self.phrase_length)*.75, .8)
        preview_button = NodeButton(pos_hint, size_hint, chord)
        self.preview_buttons.append(preview_button)
        self.add_widget(preview_button)
        preview_button.set_callback(self.preview_button_callback)

    def pop_preview_button(self):
        self.remove_widget(self.preview_buttons.pop())

    def set_preview_button_callback(self, callback):
        self.preview_button_callback = callback

    def set_play_button_callback(self, callback):
        self.play_button.set_callback(callback)

    def set_undo_button_callback(self, callback):
        self.undo_button.set_callback(callback)

    def set_phrase_length(self, phrase_length):
        self.phrase_length = phrase_length


class MenuButton(Button):
    def __init__(self, pos_hint, size_hint, label):
        super(MenuButton, self).__init__(pos_hint=pos_hint, size_hint=size_hint, text=label)
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback
        self.bind(on_press=self.callback)



class ChordSelectionLayout(RelativeLayout):
    def __init__(self, pos, size):
        super(ChordSelectionLayout, self).__init__()
        self.pos = pos
        self.size = size
        self.canvas.add(Color(0, 0, 1.0))
        self.canvas.add(Rectangle(size=self.size))

        self.node_button_callback = None
        self.chords = []
        self.buttons = []

    def set_chords(self, chords):
        self.chords = chords
        self.buttons = []
        for chord_idx in range(len(self.chords)):
            chord = self.chords[chord_idx]
            pos_hint = {'center_x': (1.0 + chord_idx)/(1+len(self.chords)), 'center_y': .5}
            size_hint = (1.0/(1 + len(self.chords))*.75, .2)
            self.buttons.append(NodeButton(pos_hint, size_hint, chord))
        for button in self.buttons:
            if self.node_button_callback is None:
                raise Exception("No node button callback.")
            button.set_callback(self.node_button_callback)
            self.add_widget(button)

    def set_node_button_callback(self, callback):
        self.node_button_callback = callback

class NodeButton(Button):
    def __init__(self, pos_hint, size_hint, chord):
        super(NodeButton, self).__init__(pos_hint=pos_hint, size_hint=size_hint, text=chord.get_name())
        self.chord = chord

    def set_callback(self, callback):
        self.bind(on_press=callback)
