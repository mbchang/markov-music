''' Contains the backend structures that compute the next possible blocks
to display to the user given some optional input constraints. '''

from building_block import *

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

    def make_selection(self, chord):
        self.index +=1


    def add_constraint(self):
        pass
        # make selection

    def undo_selection(self):
        self.index -= 1

    def reset(self):
        self.index = 0

    def get_children(self):
        # Returns the set of next possible chords given current state.
        g = Chord([59,62,67],'V')
        a = Chord([60,64,69],'vi')
        f = Chord([60,65,69],'IV')
        e = Chord([59,64,67],'iii')
        d = Chord([62,65,69],'ii')
        c = Chord()
        b = Chord([59,62,65,69],'vii0')

        if self.index == 0:
            return [Chord()]
        elif self.index == 1:
            return [a,b,f,d,g]
        elif self.index == 2:
            return [c,d,e,g,a]
        elif self.index == 3:
            return [f,g]
        else:
            return [a,b,c,d,e,f,g]


    def viterbi(self, constraints):
        pass


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



