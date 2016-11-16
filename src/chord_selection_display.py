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

    def set_node_button_callback(self, callback):
        self.chord_selection_layout.set_node_button_callback(callback)

    def on_update(self, dt):
        pass

class CurrentProgressionLayout(RelativeLayout):
    def __init__(self, pos, size):
        super(CurrentProgressionLayout, self).__init__()
        self.pos = pos
        self.size = size
        self.canvas.add(Color(1.0, 0, 0))
        self.canvas.add(Rectangle(size=self.size))


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
            button.bind(on_press=self.node_button_callback)
            self.add_widget(button)

    def set_node_button_callback(self, callback):
        self.node_button_callback = callback

class NodeButton(Button):
    def __init__(self, pos_hint, size_hint, chord):
        super(NodeButton, self).__init__(pos_hint=pos_hint, size_hint=size_hint, text=chord.get_name())
        self.chord = chord
