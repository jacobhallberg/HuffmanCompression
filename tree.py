# Author: Jacob Hallberg
# Last Edited: 12/30/2017
class Tree():
    # Class Tree is used to create the huffman tree which will be traversed.
    def __init__(self, parent, left_child=None, right_child=None):
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child

