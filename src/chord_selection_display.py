''' This file contains all necessary elements that are specific to chord
selection display. '''

from common_display import *

class ChordSelectionDisplay(InstructionGroup):
    def __init__(self):
        super(ChordSelectionDisplay, self).__init__()
        # Add a translate. This can be used to switch between chord selection
        # mode and playback mode.
        self.translate = Translate()
        self.add(self.translate)
        # Testing that this pipeline of graphics stuff works...
        # TODO: remove this random bubble when we put in real graphics.
        self.add(Bubble((50,50), (1.0, 0, 0), 40))

        # A list of BlockDisplays.
        self.block_displays = []
        # A block bank display.
        self.block_bank_display = BlockBankDisplay()
        # Need something to display the phrase or sentence that we have built
        # so far...

    def activate(self):
        # Move display back into on screen position.
        self.translate.y = 0

    def inactivate(self):
        # Move this entire display off screen.
        self.translate.y = -10000

    # TODO - is this the right way to do this?
    # Get positions to pass to parent ChordSelection for click detection.
    def get_block_positions():
        # Return a list of positions, doesn't have to be entire BlockDisplay
        # object.
        pass

    # Changes the set of blocks that we are displaying.
    def set_blocks(self, blocks):
        # Create a BlockDisplay for each block.
        pass

    def select_block(self, block_idx):
        pass

    def add_block_to_bank(self, block):
        pass

    def on_update(self, dt):
        pass

# Display a single block, as in when displaying choices.
class BlockDisplay(InstructionGroup):
    def __init__(self, pos, rgb):
        super(BlockDisplay, self).__init__()

# Display the bank of blocks the user has already created.
class BlockBankDisplay(InstructionGroup):
    def __init__(self):
        super(BlockBankDisplay, self).__init__()
        # Probably want a line for the divider, and then an array of blocks.
        # Have set positions for the blocks.
