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
        # always represent chord in canonical triad form
        # use expand_chord() to generate other notes
        self.notes = notes  
        self.name = name
        self.root = notes[0]
        self.inversion = inversion
        self.scale_root = 0

    def get_scale_root(self):
        # TODO: make this combined with RomanNumeral
        rn_map = {'I': 0, 'ii': 2, 'iii': 4,
                'IV': 5, 'V': 7, 'vi': 9, 'vii0': 11}
        return self.notes[0]-rn_map[self.name]

    def get_possible_melody_notes(self):
        root_note = self.get_scale_root()
        rn_map = {'I': 0, 'ii': 2, 'iii': 4,
                'IV': 5, 'V': 7, 'vi': 9, 'vii0': 11}
        root_note += rn_map[self.name]
        major = True
        dim = False
        if self.name.upper() != self.name:
            major = False
        if '0' in self.name:
            dim = True
        base_notes = []
        if major:
            base_notes = [0,2,4,7,9,12,14,16,17,19,21,23,24]
        if not major:
            base_notes = [0,3,7,10,12,15,17,19,23,24]
        if dim:
            base_notes = [0,2,3,6,7,8,11,12,14,15,17,18,19,20,22,23,24]
        possible_melody_notes = [x+root_note for x in base_notes]
        return possible_melody_notes

    def set_notes(self, notes):
        self.notes = notes

    def get_notes(self):
        # may be different from triad form
        if self.inversion == 'R' or self.inversion == '7':
            notes = self.notes
        elif self.inversion == '6' or self.inversion == '65':
            notes = self.notes[1:]+self.notes[0]
        elif self.inversion == '64' or self.inversion == '43':
            notes = self.notes[2:]+self.notes[:1]
        elif self.inversion == '2':
            notes = self.notes[3:]+self.notes[:2]

        return self.expand_chord(notes)

    def get_bottom(self):
        if self.inversion == 'R' or self.inversion == '7':
            note = self.notes[0]
        elif self.inversion == '6' or self.inversion == '65':
            note = self.notes[1]
        elif self.inversion == '64' or self.inversion == '43':
            note = self.notes[2]
        elif self.inversion == '2':
            note = self.notes[3]

        return note

    def get_middle(self):
        if self.inversion == 'R' or self.inversion == '7':
            note = self.notes[1]
        elif self.inversion == '6' or self.inversion == '65':
            note = self.notes[2]
        elif self.inversion == '64' or self.inversion == '43':
            note = self.notes[0]
        elif self.inversion == '2':
            note = self.notes[0]  # TODO

        return note

    def get_top(self):
        if self.inversion == 'R' or self.inversion == '7':
            note = self.notes[2]
        elif self.inversion == '6' or self.inversion == '65':
            note = self.notes[0]
        elif self.inversion == '64' or self.inversion == '43':
            note = self.notes[1]
        elif self.inversion == '2':
            note = self.notes[1]  # TODO

        return note

    def expand_chord(self, notes):
        """
        Take canonical triad form and expand to different notes
        
        preserve root, but can be different octave
        """
        # hacky
        addition1 = [n + 12 for n in notes]
        addition2 = [n - 12 for n in notes]
        addition3 = [n + 24 for n in notes]
        addition4 = [n - 24 for n in notes]

        return notes + addition1 + addition2 + addition3 + addition4


    def get_chords(self):
        return [self]

    def set_name(self):
        self.name = name

    def get_name(self):
        return self.name

    def get_root(self):
        return self.root

    def get_inversion(self):
        return self.inversion

    def set_inversion(self, inversion):
        self.inversion = inversion



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


