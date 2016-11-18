''' Contains the backend structures that compute the next possible blocks
to display to the user given some optional input constraints. '''

from building_block import *
import numpy as np

# Abstract class.
class Graph(object):
    def __init__(self):
        super(Graph, self).__init__()

    def get_children(self):
        pass


class ChordGraph(Graph):

    def __init__(self):
        super(ChordGraph, self).__init__()
        # query
        # viterbi

        # starting chord
        # ending chord
        # make selection

        #This is for testing purposes
        self.index = 0
        self.current_chord = None

        self.rn = RomanNumeral()

    def make_selection(self, chord):
        self.index +=1
        self.current_chord = chord

    def add_constraint(self):
        pass
        # make selection

    def undo_selection(self):
        self.index -= 1

    def reset(self):
        self.index = 0

    def get_children(self):
        # Returns the set of next possible chords given current state.
        if self.index == 0:
            return self._get_unconstrained_children(self.current_chord)
        elif self.index == 1:
            return self._get_unconstrained_children(self.current_chord)
        elif self.index == 2:
            return self._get_unconstrained_children(self.current_chord)
        elif self.index == 3:
            return self._get_unconstrained_children(self.current_chord)
        else:
            return self._get_unconstrained_children(self.current_chord)

    # can decide whether we want this to be in the chord class or not
    def _get_unconstrained_children(self, chord):
        """ Gets children purely from chord transition rules. No viterbi

            TODO: can return other inversions
        """
        if not self.current_chord:
            sr = 60  # TODO: we should initialize graph with a key, or have a button that selects key
            return [self._generate_chord('I', sr, 'R')] # TODO can make this more interesting
        else:
            sr = chord.get_scale_root()
            if chord.get_name() == 'I':
                return [self._generate_chord('ii', sr, 'R'),
                        self._generate_chord('iii', sr, 'R'),
                        self._generate_chord('IV', sr, 'R'),
                        self._generate_chord('V', sr, 'R'),
                        self._generate_chord('vi', sr, 'R'),
                        self._generate_chord('vii0', sr, 'R')]
            elif chord.get_name() == 'ii':
                return [self._generate_chord('V', sr, 'R'),
                        self._generate_chord('vii0', sr, 'R')]
            elif chord.get_name() == 'iii':
                return [self._generate_chord('IV', sr, 'R'),
                        self._generate_chord('vi', sr, 'R')]
            elif chord.get_name() == 'IV':
                return [self._generate_chord('I', sr, 'R'),
                        self._generate_chord('ii', sr, 'R'),
                        self._generate_chord('V', sr, 'R'),
                        self._generate_chord('vii0', sr, 'R')]
            elif chord.get_name() == 'V':
                return [self._generate_chord('I', sr, 'R'),
                        self._generate_chord('vi', sr, 'R')]
            elif chord.get_name() == 'vi':
                return [self._generate_chord('ii', sr, 'R'),
                        self._generate_chord('IV', sr, 'R')]
            elif chord.get_name() == 'vii0':
                return [self._generate_chord('I', sr, 'R')]

    # need to generate notes given roman numeral, scale root, and inversion
    def _generate_chord(self, rn, sr, inv):
        """
            rn: roman_numeral
            sr: the MIDI number of the "I" chord in the scale
            inv: inversion
        """
        # first get the root of the chord
        chord_root = self.rn.rn_root_lookup(rn) + sr
        chord_notes = self.rn.get_chord_notes(chord_root, self.rn.get_rn_type(rn))
        return Chord(chord_notes, rn, inv)


    def _viterbi(self, constraints):
        pass

        # need a trellis
        # need start 
        # need end
        # need binary transition matrix


class Viterbi(object):
    def __init__(self):
        super(Viterbi, self).__init__()
        self.t = build_transition_matrix()

    def build_transition_matrix(self):
        t = np.array(7,7)
        for i in xrange(7):
            if i == 0:
                pass
            elif i == 1:
                pass
            elif i == 2:
                pass
            elif i == 3:
                pass
            elif i == 4:
                pass
            elif i == 5:
                pass
            elif i == 6:
                pass



class RomanNumeral(object):
    def __init__(self):
        super(RomanNumeral, self).__init__()
        self.note_intervals = {'maj': [0,4,7],
                               'min': [0,3,7],
                               'aug': [0,4,8],
                               'dim': [0,3,6]}

    def get_rn_type(self, rn):
        if '+' in rn:
            return 'aug'
        elif '0' in rn:
            return 'dim'
        # note that we are short-circuiting
        elif rn[0].islower():
            return 'min'
        elif rn[0].isupper():
            return 'maj'

    def rn_root_lookup(self, rn):
        # Perhaps make this an attribute?
        rn_map = {'I': 0, 'ii': 2, 'iii': 4, 
                'IV': 5, 'V': 7, 'vi': 9, 'vii0': 11}
        return rn_map[rn]

    def get_chord_notes(self, rn_root, rn_type):
        return [rn_root + x for x in self.note_intervals[rn_type]]


class PhraseBank(Graph):
    def __init__(self):
        super(PhraseBank, self).__init__()
        self.bank = []
        self.prefixes = {}

    def add_to_bank(self, phrase):
        self.bank.append(phrase)
        if phrase.get_start().get_name() not in self.prefixes:
            self.prefixes[phrase.get_start().get_name()] = [phrase]
        else:
            self.prefixes[phrase.get_start().get_name()].append(phrase)

    def get_children(self, phrase):
        return self.prefixes[phrase.get_start().get_name()]

    def get_phrases(self):
        return self.bank



