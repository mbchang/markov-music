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
    def __init__(self, notes=[60, 64, 67], name='I',inversion='R'):
        super(Chord, self).__init__()
        self.notes = notes
        self.name = name
        if inversion == 'R' or inversion == '7':
            self.root = notes[0]
        elif inversion == '6' or inversion == '65':
            self.root = notes[1]
        elif inversion == '64' or inversion == '43':
            self.root = notes[2]
        elif inversion == '2':
            self.root = notes[3]

    def set_notes(self, notes):
        self.notes = notes

    def get_notes(self):
        return self.notes

    def set_name(self):
        self.name = name

    def get_name(self):
        return self.name

    def get_root(self):
        return self.root

    def get_inversion(self):
        return self.inversion





# Phrase is a building block and a node group.
class Phrase(BuildingBlock):
    def __init__(self, chords=[]):
        super(Phrase, self).__init__()
        self.chords = chords

    def get_start(self):
        if len(self.chords) == 0:
            return None
        return self.chords[0]

    def get_end(self):
        if len(self.chords) == 0:
            return None
        return self.chords[-1]

    def get_chords(self):
        return self.chords
