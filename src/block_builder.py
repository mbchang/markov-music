''' This class is responsible for handling the assembly of building blocks
into larger blocks, e.g. assembling chords into phrases. '''

class BlockBuilder(object):
    def __init__(self):
        super(BlockBuilder, self).__init__()
        # Contains the primitives we connected so far.
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)

    # Remove the last block, and return that block to the caller.
    def remove_block(self):
        if len(self.blocks == 0):
            return None
        else:
            return self.blocks.pop()

    def get_current_blocks(self):
        return self.blocks

    def clear_blocks(self):
        self.blocks = []
