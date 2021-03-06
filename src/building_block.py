''' These classes are the building blocks for making phrases and sentences.'''

import random

class BuildingBlock(object):
    def __init__(self):
        pass

    def get_name():
        pass

    def get_children():
        pass

    def get_sound():
        pass

# For reference:
#
#  C   D   E   F   G   A   B  C
# [60, 62, 64, 65, 67, 69, 71, 72]
# chord_notes_map = {
#     'I': [60, 64, 67],
#     'ii': [62, 65, 69],
#     'iii': [64, 67, 71],
#     'IV': [65, 69, 72],
#     'V': [67, 71, 74],
#     'vi': [69, 72, 76],
#     'vii0': [71, 74, 77]
# }


class Chord(BuildingBlock):
    def __init__(self, notes=[0, 4, 7], name='I',inversion=0):
        super(Chord, self).__init__()
        # always represent chord in canonical triad form
        # use expand_chord() to generate other notes
        self.notes = notes
        self.name = name
        self.root = notes[0]
        # Inversion is 0 for root position, 1 for first inversion, etc.
        self.inversion = inversion
        # Scale_root is the offset from 60 for the root of the scale.
        # It will always be 0, so we are always working in C major,
        # and if desired, any modulation is done at the audio control.
        self.scale_root = 0
        # Set the min and max notes, so we stay in generally the same
        # octave no matter what inversion we're in.
        # Then, we can use the expand chords function to fill multiple octaves.
        self.min_note = 48 # C below middle C
        self.max_note = 84 # C two octaves above middle C

    def get_scale_root(self):
        return self.scale_root

    def get_number_inversions(self):
        # TODO: Update this function if we introduce more types of chords.
        if '7' in self.name:
            return 4
        # All others are triads.
        else:
            return 3

    def get_possible_melody_notes(self):
        root_note = self.get_scale_root()
        rn_map = {'I': 0, 'ii': 2, 'iii': 4,
                'IV': 5, 'V': 7, 'vi': 9, 'vii0': 11}
        name = ""
        if '7' in self.name:
            name = self.name[:-1]
        else:
            name = self.name

        root_note += rn_map[name]
        major = True
        dim = False
        if self.name.upper() != self.name:
            major = False
        if '0' in self.name:
            dim = True
        base_notes = []
        if major:
            base_notes = [0,2,4,7,9,12,14,16,17,19,21,24]
        if not major:
            base_notes = [0,2,3,7,10,12,15,17,19,22,24]
        if dim:
            base_notes = [0,1,3,6,8,12,13,15,18,20,22,24]
        possible_melody_notes = [x+root_note for x in base_notes]
        return possible_melody_notes

    def set_notes(self, notes):
        self.notes = notes
        if max(notes) > self.max_note:
            raise Exception("Max note is 76, cannot have %d" % max(notes))
        if min(notes) < self.min_note:
            raise Exception("Min note is 55, cannot have %d" % min(notes))

    def possibly_add_seventh(self):
        # most common sevenths are V7, iim7, vim7
        # all involve adding a minor 7th on top
        if self.name in ['ii','vi','V']:
            # flip a coin
            if random.random() < 0.5:
                self.notes += [self.root+10]
                self.name += '7'

    def _get_canonical_notes(self):
        # may be different from triad form
        if self.inversion == 0:
            notes = self.notes
        elif self.inversion == 1:
            notes = self.notes[1:]+self.notes[0]
        elif self.inversion == 2:
            notes = self.notes[2:]+self.notes[:1]
        elif self.inversion == 3:
            notes = self.notes[3:]+self.notes[:2]
        new_notes = self.notes[self.inversion:] + self.notes[:self.inversion]
        assert new_notes == notes
        return notes

    def get_notes(self):
        return self.notes

    def get_expanded_notes(self):
        return self.expand_chord(self.notes)

    def get_expanded_canonical_notes(self):
        canonical_notes = self._get_canonical_notes()
        return self.expand_chord(canonical_notes)

    def get_bottom(self):
        canonical_notes = self._get_canonical_notes()
        return canonical_notes[0]

    def get_middle(self):
        canonical_notes = self._get_canonical_notes()
        return canonical_notes[1]  # TODO for 7th chords

    def get_top(self):
        canonical_notes = self._get_canonical_notes()
        return canonical_notes[-1]


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
        """
            Set the inversion of a chord, and updates the notes.
        """
        assert(inversion >= 0 and inversion < self.get_number_inversions())
        if self.inversion == inversion:
            return
        old_inversion = self.inversion
        # Rotate the notes appropriately.
        diff = inversion - old_inversion
        if diff < 0:
            diff = self.get_number_inversions() + diff
            # Drop an octave for the notes that have been rotated down.
            new_notes = map(lambda x: x - 12, self.notes[diff:]) + self.notes[:diff]
        else:
            # Add an octave for the notes that have been rotated up.
            new_notes = self.notes[diff:] + map(lambda x: x + 12, self.notes[:diff])
        # Wrap around if the notes are too high.
        if min(new_notes) < self.min_note:
            new_notes = map(lambda x: x + 12, new_notes)
        elif max(new_notes) > self.max_note:
            new_notes = map(lambda x: x - 12, new_notes)
        self.notes = new_notes

    def duplicate(self):
        return Chord(notes=self.notes, name=self.name, inversion=self.inversion)



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
        else:
            return self.chords[0].get_name() + " -> " + self.chords[-1].get_name()

