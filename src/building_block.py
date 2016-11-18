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
        self.notes = notes  # always in canonical triad form
        self.name = name
        self.root = notes[0]
        self.inversion = inversion

    def set_notes(self, notes):
        self.notes = notes

    def get_notes(self, with_inversion=True):
        # may be different from triad form 
        if self.inversion == 'R' or self.inversion == '7' or not with_inversion:
            return self.notes
        elif self.inversion == '6' or self.inversion == '65':
            return self.notes[1:]+self.notes[0]
        elif self.inversion == '64' or self.inversion == '43':
            return self.notes[2:]+self.notes[:1]
        elif self.inversion == '2':
            return self.notes[3:]+self.notes[:2]

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
