"""
Sorted Set implementation using binary search trees.

Just for fun I want to do a benchmark between random binary searches and balanced ones 
(implemented as red-black trees).

"""

class SortedSet(object):

    def __init__(self, dumb=False, immutable=False):
        if dumb:
            self.tree = BinarySearchTree()
        else:
            if immutable:
                # use Okasaki's version
                pass
            else:
                self.tree = RedBlackTree()

    def insert(self, value):
        self.tree.insert(value)

    def __contains__(self, value):
        return value in self.tree

    def delete(self, value):
        self.tree.delete(value)