''' Contains the backend structures that compute the next possible blocks
to display to the user given some optional input constraints. '''

# Abstract class.
class Graph():
    pass

    def get_children(self):
        pass


class ChordGraph(Graph):
    pass
    # query
    # viterbi

    # starting chord
    # ending chord
    # make selection

    def add_constraint(self):
        pass
        # make selection


    def get_children(self, chord):
        pass
        # reutrn

    def viterbi(self, constraints):
        pass


class PhraseBank(Graph):
    pass

    def get_children(self, phrase):
        pass

    def get_phrases(self):
        pass



