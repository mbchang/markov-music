''' These classes are the building blocks for making phrases and sentences.'''

class BuildingBlock(object):
    def __init__(self):
        pass

    def get_name():
        pass

    def get_children():
        pass

    def get_sound():
        pass


class Chord(BuildingBlock):
    def __init__(self, notes=[60, 64, 67], name='I'):
        super(Chord, self).__init__()
        self.notes = notes
        self.name = name

    def set_notes(self, notes):
        self.notes = notes

    def get_notes(self):
        return self.notes

    def set_name(self):
        self.name = name

    def get_name(self):
        return self.name




# Phrase is a building block and a node group.
class Phrase(BuildingBlock):
    def __init__(self):
        super(Chord, self).__init__()