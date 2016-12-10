''' This file contains all necessary elements that are specific to chord
selection display. '''

from common_display import *
from building_block import *

class ChordSelectionScreen(Widget):
    def __init__(self):
        super(ChordSelectionScreen, self).__init__()

        # Contains two layouts, each that has a change mode button.
        self.current_progression_layout = CurrentProgressionLayout((20, Window.height - 200),
                                                                   (Window.width - 40, 200))
        self.chord_selection_layout = ChordSelectionLayout((20, 20),
                                                           (Window.width - 40, Window.height - 200))
        self.add_widget(self.current_progression_layout)
        self.add_widget(self.chord_selection_layout)

    def reset(self):
        self.current_progression_layout.reset()
        self.chord_selection_layout.reset()

    def inactivate(self):
        self.remove_widget(self.current_progression_layout)
        self.remove_widget(self.chord_selection_layout)

    def activate(self):
        self.add_widget(self.current_progression_layout)
        self.add_widget(self.chord_selection_layout)

    def set_phrase_controls(self):
        self.chord_selection_layout.set_phrase_controls()

    def set_chords(self, chords):
        self.chord_selection_layout.set_chords(chords)

    def pop_preview_button(self):
        self.current_progression_layout.pop_preview_button()

    def set_change_mode_button_callback(self, callback):
        self.chord_selection_layout.set_change_mode_button_callback(callback)

    def set_preview_button_callback(self, callback):
        self.current_progression_layout.set_preview_button_callback(callback)

    def set_node_button_callback(self, callback):
        self.chord_selection_layout.set_node_button_callback(callback)

    def set_phrase_control_callback(self, callback):
        self.chord_selection_layout.set_phrase_control_callback(callback)

    def set_play_button_callback(self, callback):
        self.current_progression_layout.set_play_button_callback(callback)

    def set_undo_button_callback(self, callback):
        self.current_progression_layout.set_undo_button_callback(callback)

    def set_save_button_callback(self, callback):
        self.current_progression_layout.set_save_button_callback(callback)

    def add_node_to_progression(self, block, mode):
        self.current_progression_layout.add_preview_button(block, mode)

    def set_phrase_length(self, phrase_length):
        self.current_progression_layout.set_phrase_length(phrase_length)

    def show_save_button(self):
        self.current_progression_layout.show_save_button()

    def hide_save_button(self):
        self.current_progression_layout.hide_save_button()

    def show_change_mode_button(self):
        self.chord_selection_layout.show_change_mode_button()

    def hide_change_mode_button(self):
        self.chord_selection_layout.hide_chnage_mode_button()

    def set_change_mode_button_text(self, text):
        self.chord_selection_layout.set_change_mode_button_text(text)

    def on_update(self, dt):
        pass

class CurrentProgressionLayout(RelativeLayout):
    def __init__(self, pos, size, phrase_length=8):
        super(CurrentProgressionLayout, self).__init__()
        self.pos = pos
        self.size = size
        self.phrase_length = phrase_length
        # self.canvas.add(Color(1.0, 0, 0))
        #self.canvas.add(Rectangle(size=self.size))

        # Add preview buttons (to play the chord when clicked).
        self.preview_buttons = []
        self.preview_button_callback = None
        self.max_blocks = 40

        # Add menu buttons.
        play_pos_hint = {'center_x': .9, 'center_y': .25}
        play_size_hint = (.15, .2)
        self.play_button = MenuButton(play_pos_hint, play_size_hint, 'Play')
        self.add_widget(self.play_button)

        undo_pos_hint = {'center_x': .9, 'center_y': .5}
        undo_size_hint = (.15, .2)
        self.undo_button = MenuButton(undo_pos_hint, undo_size_hint, 'Undo')
        self.add_widget(self.undo_button)

        # Do not show save button on initialization.
        save_pos_hint = {'center_x': .9, 'center_y': .75}
        save_size_hint = (.15, .2)
        self.save_button = MenuButton(save_pos_hint, save_size_hint, 'Save')

    def reset(self):
        for button in self.preview_buttons:
            self.remove_widget(button)
        self.preview_buttons = []

    def add_preview_button(self, block, mode):
        if len(self.preview_buttons) >= self.max_blocks:
            print "Cannot add, max number of blocks reached!"
            return
        if mode == 'chords':
            # TODO: buttons are not vertically centered.
            pos_hint = {'center_x': .8*((1.0 + len(self.preview_buttons))/(1.0+self.phrase_length)), 'center_y': .5}
            size_hint = (1.0/(1 + self.phrase_length)*.75, .6)
        elif mode == 'phrases':
            row = int(len(self.preview_buttons) / self.phrase_length)
            col = len(self.preview_buttons) % self.phrase_length
            x_pos = .8*((1.0 + col)/(1.0+self.phrase_length))
            pos_hint = {'center_x': x_pos, 'center_y': 1 - .15 * (row + 1)}
            size_hint = (1.0/(1 + self.phrase_length)*.75, .15)
            # MICHAEL LOOK AT THIS: this implements rows
        else:
            raise Exception('Bad mode.')
        preview_button = NodeButton(pos_hint, size_hint, block, preview=True)
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

    def set_save_button_callback(self, callback):
        self.save_button.set_callback(callback)

    def set_phrase_length(self, phrase_length):
        self.phrase_length = phrase_length

    def show_save_button(self):
        self.add_widget(self.save_button)

    def hide_save_button(self):
        self.remove_widget(self.save_button)


class ChordSelectionLayout(RelativeLayout):
    def __init__(self, pos, size):
        super(ChordSelectionLayout, self).__init__()
        self.pos = pos
        self.size = size
        # self.canvas.add(Color(0, 0, 1.0))
        #self.canvas.add(Rectangle(size=self.size))

        # Add a change mode button that switches the app between building chords
        # to building phrases.
        mode_button_pos = {'center_x': .8, 'center_y': .1}
        mode_button_size = (.2, .1)
        self.change_mode_button = ChangeModeButton(mode_button_pos, mode_button_size,
                                                   'Go to Phrase Mode')

        self.node_button_callback = None
        self.chords = []
        self.buttons = []

    def reset(self):
        self.chords = []
        for button in self.buttons:
            self.remove_widget(button)
        self.buttons = []

    def set_chords(self, chords):
        self.reset()
        self.chords = chords
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

        # MICHALE LOOK AT THIS THIS IS WHERE WE ADD BUTTONS
        # instead of calling set_chords on initialization, show constrained/unconstrained progression
        # if unconstrained --> set_chords
        # if constrained --> show them input buttons: start chord, end chord, number of transitions
        # pos hint and size hint: relative to the size of layout
            # if layout is 200 x 200
            # size hint is 0.5, then it is 50% of layout
            # pos hint is 0.5, then it is at 50% layout
        # we can do multiple rows here too

    def set_phrase_controls(self):
        self.reset()
        self.buttons.append(MenuButton({'center_x':1.0/3, 'center_y':0.5}, (0.2,0.2), 'Constrained'))
        self.buttons.append(MenuButton({'center_x':2.0/3, 'center_y':0.5}, (0.2,0.2), 'Unconstrained'))
        for button in self.buttons:
            if self.node_button_callback is None:
                raise Exception("No node button callback.")
            button.set_callback(self.phrase_control_callback)
            self.add_widget(button)


    def show_change_mode_button(self):
        self.add_widget(self.change_mode_button)  # MICHAEL LOOK AT THIS add button, look at the callback

    def hide_change_mode_button(self):
        self.remove_widget(self.change_mode_button)

    def set_change_mode_button_text(self, text):
        self.change_mode_button.set_text(text)

    def set_node_button_callback(self, callback):
        self.node_button_callback = callback

    def set_change_mode_button_callback(self, callback):
        self.change_mode_button.set_callback(callback)

    def set_phrase_control_callback(self, callback):
        self.phrase_control_callback = callback

class ChangeModeButton(Button):
    def __init__(self, pos_hint, size_hint, label):
        super(Button, self).__init__(pos_hint=pos_hint, size_hint=size_hint, text=label)
        self.background_normal = ''
        self.background_color = [0, 1.0, 1.0, .6]

    def set_callback(self, callback):
        self.bind(on_press=callback)

    def set_text(self, text):
        self.text = text
