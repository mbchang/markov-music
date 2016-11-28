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
        # Need a stack of chords to support undo functionality.
        # The last element of self.chord_stack is the current chord.
        self.chord_stack = []
        self.rn = RomanNumeral()
        self.scale_root = 0  # normalized

        self.T = 8
        self.S = 7
        self.TM = self._build_transition_matrix()

        # possible children: c[t,i,j] is 1 if j is a child of i
        # where j is at time t, t starts at 0
        # TODO: these indices need to be adjusted if you don't fix the first chord
        self.C = np.tile(self.TM,(self.T,1,1)) # [T-1, S, S]

        # TODO: add constraint for first chord
        # TODO: this "6" should be a 7, but depends on your indexing
        self.add_constraint(6,set([0,4]))  # it can only end in I or V

    def _build_transition_matrix(self):
            # t[i,j] is prob i transitions to j
            # we do not allow self loops for now

            t = np.zeros((7,7))

            rows, cols = [],[]

            # I: I, ii, iii, IV, V, vi, vii0
            rows.extend([0]*7)
            cols.extend(range(0,7))

            # ii: ii, V, vii0
            rows.extend([1]*2)
            cols.extend([4,6])

            # iii: iii, IV, vi
            rows.extend([2]*2)
            cols.extend([3,5])

            # IV: I, ii, IV, V, vii0
            rows.extend([3]*4)
            cols.extend([0,1,4,6])

            # V: I, V, vi
            rows.extend([4]*2)
            cols.extend([0,5])

            # vi: ii, IV, vi
            rows.extend([5]*2)
            cols.extend([1,3])

            # vii0: I, vii0
            rows.extend([6]*1)
            cols.extend([0])

            t[rows, cols] = 1

            return t


    def make_selection(self, chord):
        self.chord_stack.append(chord)

    # TODO: make an undo_constraint:
    # perhaps we can generate a stack of constraints: (chord_idx, original_vals, new_vals)
    # TODO: add safety mechanism such that the user cannot specify a constraint that kills all possible paths
    # TODO: if this is called by an outside method, then we'd need to figure out a mapping
    def add_constraint(self, t, values):
        """
            t: in range [0,7]
            chord_idx: in range [0,6] = [I, ii, iii, IV, V, vi, vii0]
            values: set of values that are in range [0,6] = [I, ii, iii, IV, V, vi, vii0]
        """
        if t < 0:
            return
        else:
            # i cannot take any value that is NOT in this set
            # although this set can include values that i cannot take
            for j in range(self.S):
                # so at j != v, we need to kill all the i whose j != v
                for i in range(self.S):
                    if j not in values:
                        self.C[t,i,j] = 0

            new_values = set()
            for j in range(self.S):
                for i in range(self.S):
                    if self.C[t,i,j] == 1:
                        new_values.add(i)

            # backpropagate change all the way to the beginning
            self.add_constraint(t-1, new_values)


    def undo_selection(self):
        self.chord_stack.pop()

    def reset(self):
        self.chord_stack = []

    def get_children(self):
        # Returns the set of next possible chords given current state.
        current_idx = len(self.chord_stack)
        current_chord = None if current_idx == 0 else self.chord_stack[-1]
        children = self._get_children(current_chord, current_idx-1)
        return children

    # can decide whether we want this to be in the chord class or not
    def _get_children(self, chord, current_idx):
        """ Gets children purely from chord transition rules. No viterbi

            TODO: can return other inversions
        """
        if current_idx == -1:
            assert chord is None
            sr = self.scale_root#60  # TODO: we should initialize graph with a key, or have a button that selects key
            return [self._generate_chord('I', sr, 'R')] # TODO can make this more interesting
        else:
            sr = chord.get_scale_root()
            chord_idx = self.rn.sd_rev_map[chord.get_name()]
            children_idx = list(self.C[current_idx, chord_idx].nonzero()[0])
            children = [self._generate_chord(self.rn.sd_map[ci], sr, 'R') for ci in children_idx]
            return children


    # Get the possible chords based on only the chord transition rules.
    def get_children_no_constraint(self, chord):
        sr = chord.get_scale_root()
        chord_idx = self.rn.sd_rev_map[chord.get_name()]
        transition_row = self.TM[chord_idx, :]
        children_idx = []
        for i in xrange(len(transition_row)):
            if transition_row[i] == 1:
                children_idx.append(i)
        children = [self._generate_chord(self.rn.sd_map[ci], sr, 'R') for ci in children_idx]
        return children

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


class RomanNumeral(object):
    def __init__(self):
        super(RomanNumeral, self).__init__()
        self.note_intervals = {'maj': [0,4,7],
                               'min': [0,3,7],
                               'aug': [0,4,8],
                               'dim': [0,3,6]}

        # TODO: may have to fine-tune these mappings if we have inversions
        self.rn_map = {'I': 0, 'ii': 2, 'iii': 4,
                'IV': 5, 'V': 7, 'vi': 9, 'vii0': 11}

        # scale degrees
        # TODO: perhaps move this to ChordGraph
        self.sd_map = {0:'I',1:'ii',2:'iii',3:'IV',4:'V',5:'vi',6:'vii0'}
        self.sd_rev_map = {v:k for k,v in self.sd_map.items()}

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
        return self.rn_map[rn]

    def rn_reverse_lookup(self,idx):
        return self.rn_rev_map[idx]

    def get_chord_notes(self, rn_root, rn_type):
        return [rn_root + x for x in self.note_intervals[rn_type]]


class PhraseBank(Graph):
    def __init__(self):
        super(PhraseBank, self).__init__()
        self.bank = []
        self.chord_graph = ChordGraph()
        self.prefixes = {}

    def add_to_bank(self, phrase):
        self.bank.append(phrase)
        if phrase.get_start().get_name() not in self.prefixes:
            self.prefixes[phrase.get_start().get_name()] = [phrase]
        else:
            self.prefixes[phrase.get_start().get_name()].append(phrase)

    def get_children(self, phrase):
        children = []
        for next_chord in self.chord_graph.get_children_no_constraint(phrase.get_end()):
            if next_chord.get_name() in self.prefixes:
                children += self.prefixes[next_chord.get_name()]
        return children

    def get_phrases(self):
        return self.bank

    def get_num_phrases(self):
        return len(self.bank)

    # Returns the options for the first phrase of a song.
    def get_starting_phrases(self):
        # For now, say that we can start the song with any phrase that begins
        # with a I chord.
        return self.prefixes[Chord().get_name()]

