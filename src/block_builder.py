''' This class is responsible for handling the assembly of building blocks
into larger blocks, e.g. assembling chords into phrases. '''

class BlockBuilder(object):
    def __init__(self, phrase_length=8):
        super(BlockBuilder, self).__init__()
        # Contains the primitives we connected so far.
        self.blocks = []
        self.phrase_length = phrase_length

    def get_num_blocks(self):
        return len(self.blocks)

    def set_phrase_length(self, length):
        self.phrase_length = length

    def add_block(self, block):
        if len(self.blocks) >= self.phrase_length:
            return -1
        self.blocks.append(block)
        return 0

    # Remove the last block, and return that block to the caller.
    def remove_block(self):
        if len(self.blocks) == 0:
            return None
        else:
            return self.blocks.pop()

    def get_current_blocks(self):
        return self.blocks

    def clear_blocks(self):
        self.blocks = []
