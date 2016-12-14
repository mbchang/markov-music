''' This class is responsible for handling the assembly of building blocks
into larger blocks, e.g. assembling chords into phrases. '''

from building_block import *

class BlockBuilder(object):
    def __init__(self, phrase_length=None):
        super(BlockBuilder, self).__init__()
        # Contains the primitives we connected so far.
        self.blocks = []
        self.phrase_length = phrase_length
        if self.phrase_length is None:
            # Some reasonable upper bound.
            self.phrase_length = 64

    def get_num_blocks(self):
        return len(self.blocks)

    def set_phrase_length(self, length):
        self.phrase_length = length

    def add_block(self, block):
        if len(self.blocks) >= self.phrase_length:
            return -1
        self.blocks.append(block)
        return 0

    def get_last_block(self):
        if len(self.blocks) < 1:
            return None
        else:
            return self.blocks[-1]

    # Remove the last block, and return that block to the caller.
    def remove_block(self):
        if len(self.blocks) == 0:
            return None
        else:
            return self.blocks.pop()

    def get_current_blocks(self):
        return self.blocks

    def set_blocks(self, blocks):
        '''
            Set the blocks to be the given blocks.
            If length of the blocks exceeds the phrase length, return 0 and
            do not update the blocks.
        '''
        if len(blocks) > self.phrase_length:
            return -1
        self.blocks = blocks
        return 0

    # Returns an array of the chords, in order.
    # If the blocks are phrases, this flattens them and returns just an array of chords.
    def get_flattened_chords(self):
        flattened_chords = []
        for block in self.blocks:
            if isinstance(block, Chord):
                flattened_chords.append(block)
            elif isinstance(block, Phrase):
                flattened_chords += block.get_chords()
            else:
                raise Exception("A block must be either a Chord or a Phrase")
        return flattened_chords

    def clear_blocks(self):
        self.blocks = []
