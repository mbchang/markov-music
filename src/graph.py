class BuildingBlock():
    def __init__(self):
        pass

    def get_name():
        pass

    def get_children():
        pass

    def get_sound():
        pass


class Chord(BuildingBlock):
    def __init__(self):
        super(Chord, self).__init__()


# Phrase is a building block and a node group
class Phrase(BuildingBlock):
    def __init__(self):
        super(Chord, self).__init__()


# Manager
class Chord_Selection():
    def __init__(sefl):
        pass
        self.block_builder = None
        self.audio = None
        self.graphics = None
        self.graph = None

    pass
    # contains datastructures, memory, 

    # User Interface
    def on_click():
        # figure out what was selected, if something was selected
        pass

    def on_update():
        pass


class Block_Builder():
    pass
    # contains the primitives we connected so far

    def add_block(self):
        pass

    def remove_block(self, index):
        pass

    def get_current_block(self):
        pass


class Graph():
    pass

    def get_children(self):
        pass


class Chord_Graph(Graph):
    pass
    # query
    # viterbi

    # starting chord
    # ending chord
    # make selection

    def add_constraint(self):
        pass
        # make selection


    def get_children(self, chord):
        pass
        # reutrn 

    def viterbi(self, constraints):
        pass


class Phrase_Bank(Graph):
    pass

    def get_children(self, phrase):
        pass

    def get_phrases(self):
        pass



