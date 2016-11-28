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
        self.scale_root = 0

    def get_scale_root(self):
        # TODO: make this combined with RomanNumeral
        rn_map = {'I': 0, 'ii': 2, 'iii': 4,
                'IV': 5, 'V': 7, 'vi': 9, 'vii0': 11}
        return self.notes[0]-rn_map[self.name]

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

    def add_chords(self, chord_list):
        self.chords.extend(chord_list)

    def get_name(self):
        # First chord's name then an arrow then the last chord's name.
        if len(self.chords) == 0:
            return "Empty"
        # i removed this because i think the phrase should also be able
        # to encapsulate the idea of a song, so we can build a song up by
        # concatenating phrases together into a phrase -taylor
        # elif len(self.chords) != 4 or len(self.chords) != 8:
        #     raise Exception("Chord should only be of length 4 or 8.")
        else:
            return self.chords[0].get_name() + " -> " + self.chords[-1].get_name()


