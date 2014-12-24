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

    def insert(value):
        pass

    def __contains__(value):
        pass

    def delete(value):
        pass