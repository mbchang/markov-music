''' Contains the backend structures that compute the next possible blocks
to display to the user given some optional input constraints. '''

from building_block import *
import numpy as np
import sys

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
        self.constraints = {}

        # Viterbi matrix for current chords, for voice leading.
        self.vm = []

        self.T = 8  # default
        self.S = 7
        self.TM = self._build_transition_matrix()

        # possible children: c[t,i,j] is 1 if j is a child of i
        # where j is at time t, t starts at 0
        self.set_max_steps(self.T)
        self.no_path = False


    def set_max_steps(self, t):
        # like a reset
        self.T = t
        self.C = np.tile(self.TM,(self.T,1,1)) # [T-1, S, S]  # perhaps you can rebuild every time you do get_children
        self.constraints = {}

    def _build_transition_matrix(self):
            # t[i,j] is prob i transitions to j
            # we do not allow self loops for now

            t = np.zeros((self.S,self.S))

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
        print self.constraints
        self._update_voice_leading_viterbi()

    # TODO: make an undo_constraint:
    # perhaps we can generate a stack of constraints: (chord_idx, original_vals, new_vals)
    # TODO: add safety mechanism such that the user cannot specify a constraint that kills all possible paths
    # TODO: if this is called by an outside method, then we'd need to figure out a mapping
    def add_constraint(self, t, values, external):
        """
            t: in range [0,7]
            chord_idx: in range [0,6] = [I, ii, iii, IV, V, vi, vii0]
            values: set of values that are in range [0,6] = [I, ii, iii, IV, V, vi, vii0]
        """
        if external:
            self.constraints[t] = values
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

            print 'self.constraints', self.constraints

            # backpropagate change all the way to the beginning
            self.add_constraint(t-1, new_values, False)

        # check if there is a path through the graph. If not, start over
        if np.linalg.norm(reduce(np.dot,self.C)) == 0:
            self.no_path = True

    def set_chord(self, t, chord_name):

        # t-1 to map it to 0-indexed. it is originally 1-indexed
        if chord_name != 'NA':
            self.add_constraint(t-1, [self.rn.sd_rev_map[chord_name]], True)


    def undo_selection(self):
        self.chord_stack.pop()
        self._update_voice_leading_viterbi()

    def reset(self):
        self.chord_stack = []
        self.no_path = False
        self._update_voice_leading_viterbi()

    def get_children(self):
        # Returns the set of next possible chords given current state.
        current_idx = len(self.chord_stack)
        if current_idx >= self.T:
            return []
        current_chord = None if current_idx == 0 else self.chord_stack[-1]

        children = self._get_children(current_chord, current_idx)
        children_with_voice_leading = self._voice_leading(children)
        return children_with_voice_leading

    def _get_chord_name(self, chord):
        name = chord.get_name()
        if name[-1] == '7':
            return name[:-1]
        else:
            return name

    # can decide whether we want this to be in the chord class or not
    def _get_children(self, chord, current_idx):
        """ Gets children purely from chord transition rules. No viterbi

        """
        if current_idx == 0:
            assert chord is None
            first_chords = self._sample_first_chords()
            return first_chords
        else:
            sr = chord.get_scale_root()
            chord_idx = self.rn.sd_rev_map[self._get_chord_name(chord)]
            children_idx = list(self.C[current_idx, chord_idx].nonzero()[0])
            children = [self._generate_chord(self.rn.sd_map[ci], sr, 0) for ci in children_idx]
            return children

    def _sample_first_chords(self):
        sr = self.scale_root
        if self.constraints.has_key(0):
            first_notes = [self.rn.sd_map[x] for x in self.constraints[0]]
        else:
            first_notes = ['I','ii','iii','IV','V','vi','vii0'] #+ ['I']*100  # TODO
        first_chords = [self._generate_chord(n, sr, 0) for n in first_notes]
        return first_chords


    # Get the possible chords based on only the chord transition rules.
    def get_children_no_constraint(self, chord):
        sr = chord.get_scale_root()
        chord_idx = self.rn.sd_rev_map[self._get_chord_name(chord)]
        transition_row = self.TM[chord_idx, :]
        children_idx = []
        for i in xrange(len(transition_row)):
            if transition_row[i] == 1:
                children_idx.append(i)
        children = [self._generate_chord(self.rn.sd_map[ci], sr, 0) for ci in children_idx]
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

        # here with some probability change the chord to 7th.
        chord = Chord(chord_notes, rn, inv)
        chord.possibly_add_seventh()

        return chord

    def _voice_leading(self, next_chords):
        """
            Input: an array of next possible chords following the current chord_stack.
            Output: an array containing an entry for each possible next chord. The entry
                    is a tuple of the next chord (with correct inversion), and an array
                    that is the current chord stack + the next chord, all with inversions.
        """
        chords_with_voice_leading = []

        for next_chord in next_chords:
            voice_lead_chords = self._do_voice_leading(next_chord)
            chords_with_voice_leading.append((voice_lead_chords[-1], voice_lead_chords))
        return chords_with_voice_leading

    def _do_voice_leading(self, chords):
        """
            Performs Viterbi on the given chords to output the optimal inversions
            for each chord. Optimal is defined as minimizing the overall distance traveled
            among the chords, while still guaranteeing that the given chord ends in root position.
        """
        # Each chord has a name, notes, and an inversion.
        # Assume the last chord is going to be in root position.
        # Use Viterbi to find best inversions for all chords.
        pass

    def _update_voice_leading_viterbi(self):
        """
            Updates the self.voice_leading_viterbi matrix, based on the current
            self.chord_stack.

            Should be called after adding or popping a chord from the chord stack.
            And also needs to be called during reset().
        """
        # If chord_stack is empty, just clear the matrix.
        if len(self.chord_stack) == 0:
            self.vm = []
            return
        # Initialize matrix with one row per chord in self.chord_stack.
        self.vm = [None for i in xrange(len(self.chord_stack))]
        for i in xrange(len(self.chord_stack)):
            num_inversions = self.chord_stack[i].get_number_inversions()
            # Each entry in the row is itself an array, of length num_inversions
            # possible for that chord.
            self.vm[i] = [None for j in xrange(num_inversions)]
            chord = self.chord_stack[i]
            for j in xrange(num_inversions):
                ch = chord.duplicate()
                # Create a chord for this particular inversion.
                ch.set_inversion(j)
                # The entry in the matrix is a tuple of the cost, the chord, and the parent
                # pointer, which should be the j index of the entry in the previous row that
                # leads to this entry in the lowest cost path.
                if i == 0:
                    cost = 0
                else:
                    cost = sys.maxint
                self.vm[i][j] = [cost, ch, None]
        # Run Viterbi. Nothing to do if there's only one chord.
        if len(self.chord_stack) == 1:
            return
        # Fill in the matrix appropriately,
        # Basically, self.vm[i][j] is the min of the previous optimal + distance
        # for each of the possible previous chords leading to that one.
        for i in xrange(1, len(self.chord_stack)):
            for j in xrange(len(self.vm[i])):
                min_cost = sys.maxint
                min_parent = None
                for k in xrange(len(self.vm[i-1])):
                    # The previous optimal, plus the distance to get from there to here.
                    cost = self.vm[i-1][k][0] + self._get_distance(self.vm[i-1][k][1], self.vm[i][j][1])
                    if cost < min_cost:
                        min_cost = cost
                        min_parent = k
                self.vm[i][j][0] = min_cost
                self.vm[i][j][2] = min_parent

    def _get_distance(self, chord1, chord2):
        """
            Returns distance between the chords. If two chords have same number
            of notes, then just sum the pairwise distances. Otherwise, for each
            note in one chord, count the distance as the min distance to any
            note in the other chord.
        """
        distance = None
        n1, n2 = chord1.get_notes(), chord2.get_notes()
        if len(n1) == len(n2):
            distance = sum([abs(n1[i] - n2[i]) for i in xrange(len(n1))])
        else:
            # Just make it so that n1 is longer, for convenience.
            if len(n1) < len(n2):
                n1, n2 = n2, n1
            distance = 0
            for i in xrange(len(n1)):
                # The first and last notes must connect to first and last notes
                # of the other chord.
                if i == 0:
                    d = abs(n1[i] - n2[i])
                elif i == len(n1) - 1:
                    d = abs(n1[i] - n2[len(n2) - 1])
                # Only consider distances from the corresponding note in the other
                # chord, or the note that comes one index before, so [i, i-1].
                else:
                    d = min([abs(n1[i] - n2[j]) for j in [i, i-1]])
                distance += d
        return distance

    def _do_voice_leading(self, chord):
        """
            Performs Viterbi to output the optimal inversions for each chord.
            Optimal is defined as minimizing the overall distance traveled
            among the chords, while still guaranteeing that the given chord ends
            in root position.

            The input is a chord that will be the next chord after the current
            chord_stack.

            Returns an array of the best chord progression that includes all of the
            notes in the current chord_stack plus the given input chord.
        """
        # Each chord has a name, notes, and an inversion.
        # Assume the last chord is going to be in root position.
        # Use Viterbi to find best inversions for all chords.
        # Uses self.vm, the viterbi matrix for the current chord stack.
        if len(self.vm) < 1:
            return [chord]
        I = len(self.vm) - 1
        # Expect root position chords.
        assert(chord.inversion == 0)
        chord_progression = [chord]
        min_cost = sys.maxint
        min_parent = None
        for j in xrange(len(self.vm[I])):
            cost = self.vm[I][j][0] + self._get_distance(self.vm[I][j][1], chord)
            if cost < min_cost:
                min_cost = cost
                min_parent = j
        # Backtrace to get the entire progression.
        for i in xrange(I, -1, -1):
            chord_progression.append(self.vm[i][j][1])
            # Get next parent pointer.
            j = self.vm[i][j][2]
        # Reverse the chord progression because we built it in reverse.
        chord_progression = chord_progression[::-1]
        return chord_progression

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
        return self.prefixes.values()[0]

