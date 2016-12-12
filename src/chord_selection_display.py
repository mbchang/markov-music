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

        self.info = Label(text = "", valign='top', halign='left',font_size='20sp',
              pos=(Window.width * 0.65, Window.height * -0.4),
              text_size=(Window.width, Window.height))
        self.add_widget(self.info)


    def reset(self):
        self.current_progression_layout.reset()
        self.chord_selection_layout.reset()
        self.set_phrase_controls()

    def inactivate(self):
        self.remove_widget(self.current_progression_layout)
        self.remove_widget(self.chord_selection_layout)

    def activate(self):
        self.add_widget(self.current_progression_layout)
        self.add_widget(self.chord_selection_layout)

    def set_phrase_controls(self):
        self.chord_selection_layout.set_phrase_controls()
        self.show_undo_phrase_ctrl_button()

    def set_phrase_length_csl(self):
        self.chord_selection_layout.set_phrase_length_csl()

    def set_chord_preselect(self, mode):
        self.chord_selection_layout.set_chord_preselect(mode)

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

    def set_phrase_length_csl_callback(self, callback):
        self.chord_selection_layout.set_phrase_length_csl_callback(callback)

    def set_start_chord_select_callback(self, callback):
        self.chord_selection_layout.set_start_chord_select_callback(callback)

    def set_end_chord_select_callback(self, callback):
        self.chord_selection_layout.set_end_chord_select_callback(callback)

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

    def show_play_button(self):
        self.current_progression_layout.show_play_button()

    def hide_play_button(self):
        self.current_progression_layout.hide_play_button()

    def show_undo_phrase_ctrl_button(self):
        self.current_progression_layout.show_undo_phrase_ctrl_button()

    def hide_undo_phrase_ctrl_button(self):
        self.current_progression_layout.hide_undo_phrase_ctrl_button()

    def set_undo_phrase_ctrl_button_callback(self, callback):
        self.current_progression_layout.set_undo_phrase_ctrl_button_callback(callback)

    def show_undo_button(self):
        self.current_progression_layout.show_undo_button()

    def hide_undo_button(self):
        self.current_progression_layout.hide_undo_button()

    def show_change_mode_button(self):
        self.chord_selection_layout.show_change_mode_button()

    def hide_change_mode_button(self):
        self.chord_selection_layout.hide_chnage_mode_button()

    def set_change_mode_button_text(self, text):
        self.chord_selection_layout.set_change_mode_button_text(text)

    def add_phrase_length_label(self, phrase_length):
        text = "Phrase Length: " + str(phrase_length)
        self.info.text = text  # always the first thing

    def add_start_chord_label(self, start_chord):
        text = "    Start Chord: " + str(start_chord)
        self.info.text += text

    def add_end_chord_label(self, end_chord):
        text = "    End Chord: " + str(end_chord)
        self.info.text += text

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
        self.play_button_on = False
        # self.add_widget(self.play_button)  # add this afterwards

        undo_pos_hint = {'center_x': .9, 'center_y': .5}
        undo_size_hint = (.15, .2)
        self.undo_button = MenuButton(undo_pos_hint, undo_size_hint, 'Undo')
        self.undo_button_on = False
        # self.add_widget(self.undo_button)  # add this afterwards

        # phrase controls
        undo_phrase_ctrl_pos_hint = {'center_x': .9, 'center_y': .75}
        undo_phrase_ctrl_size_hint = (.15, .2)
        self.undo_phrase_ctrl_button = MenuButton(undo_phrase_ctrl_pos_hint, undo_phrase_ctrl_size_hint, 'Restart Phrase')
        self.undo_phrase_ctrl_button_on = False

        # Do not show save button on initialization.
        save_pos_hint = {'center_x': .9, 'center_y': .75}
        save_size_hint = (.15, .2)
        self.save_button = MenuButton(save_pos_hint, save_size_hint, 'Save')
        self.save_button_on = False

    def reset(self):
        for button in self.preview_buttons:
            self.remove_widget(button)
        self.preview_buttons = []
        self.hide_save_button()
        self.hide_play_button()
        self.hide_undo_button()

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

    def show_undo_phrase_ctrl_button(self):
        if not self.undo_phrase_ctrl_button_on:
            self.add_widget(self.undo_phrase_ctrl_button)
            self.undo_phrase_ctrl_button_on = True

    def hide_undo_phrase_ctrl_button(self):
        if self.undo_phrase_ctrl_button_on:
            self.remove_widget(self.undo_phrase_ctrl_button)
            self.undo_phrase_ctrl_button_on = False

    def show_play_button(self):
        if not self.play_button_on:
            self.add_widget(self.play_button)
            self.play_button_on = True

    def hide_play_button(self):
        if self.play_button_on:
            self.remove_widget(self.play_button)
            self.play_button_on = False

    def set_play_button_callback(self, callback):
        self.play_button.set_callback(callback)

    def show_undo_button(self):
        if not self.undo_button_on:
            self.add_widget(self.undo_button)
            self.undo_button_on = True

    def hide_undo_button(self):
        if self.undo_button_on:
            self.remove_widget(self.undo_button)
            self.undo_button_on = False

    def set_undo_button_callback(self, callback):
        self.undo_button.set_callback(callback)

    def set_save_button_callback(self, callback):
        self.save_button.set_callback(callback)

    def set_phrase_length(self, phrase_length):  # TODO
        self.phrase_length = phrase_length

    def set_undo_phrase_ctrl_button_callback(self, callback):
        self.undo_phrase_ctrl_button.set_callback(callback)

    def show_save_button(self):
        if not self.save_button_on:
            self.add_widget(self.save_button)
            self.save_button_on = True

    def hide_save_button(self):
        if self.save_button_on:
            self.remove_widget(self.save_button)
            self.save_button_on = False


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

        self.instructions = topleft_label()
        self.add_widget(self.instructions)

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
                raise Exception("No phrase control button callback.")
            button.set_callback(self.phrase_control_callback)
            self.add_widget(button)

    def set_phrase_length_csl(self):
        self.reset()
        print self.instructions
        self.instructions.text = "Select phrase length"
        max_length = 8
        for i in range(max_length-1):
            pos_hint = {'center_x': (1.0 + i)/(max_length), 'center_y': .5}
            size_hint = (1.0/(1 + max_length)*.75, .2)
            self.buttons.append(MenuButton(pos_hint, size_hint,str(i+2)))
        for button in self.buttons:
            if self.node_button_callback is None:
                raise Exception("No phrase control button callback.")
            button.set_callback(self.phrase_length_csl_callback)  # TODO
            self.add_widget(button)

    def set_chord_preselect(self, mode):
        self.reset()
        chords = ['I','ii','iii','IV','V','vi','vii0', 'NA']
        instructions = "Select " + mode + " length"
        self.instructions.text = instructions
        print chords
        for i in range(len(chords)):
            pos_hint = {'center_x': (1.0 + i)/(1+len(chords)), 'center_y': .5}
            size_hint = (1.0/(1 + len(chords))*.75, .2)
            self.buttons.append(MenuButton(pos_hint, size_hint, chords[i]))
        for button in self.buttons:
            if self.node_button_callback is None:
                raise Exception("No start or end button callback.")
            if mode == 'start':
                button.set_callback(self.start_chord_select_callback)
            elif mode == 'end':
                button.set_callback(self.end_chord_select_callback)
            else:
                raise Exception("unknown mode")
            self.add_widget(button)

    def show_change_mode_button(self):
        self.add_widget(self.change_mode_button)

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

    def set_phrase_length_csl_callback(self, callback):
        self.phrase_length_csl_callback = callback

    def set_start_chord_select_callback(self, callback):
        self.start_chord_select_callback = callback

    def set_end_chord_select_callback(self, callback):
        self.end_chord_select_callback = callback

class ChangeModeButton(Button):
    def __init__(self, pos_hint, size_hint, label):
        super(Button, self).__init__(pos_hint=pos_hint, size_hint=size_hint, text=label)
        self.background_normal = ''
        self.background_color = [0, 1.0, 1.0, .6]

    def set_callback(self, callback):
        self.bind(on_press=callback)

    def set_text(self, text):
        self.text = text

def topleft_label() :
    l = Label(text = "", valign='top',font_size='20sp',
              pos=(Window.width * 0.1, Window.height * -0.3),
              text_size=(Window.width, Window.height))
    return l
