import unittest

from ..binarytree import BinarySearchTree

class BSTInsertTestCase(unittest.TestCase):

    def test_insert(self):
        tree = BinarySearchTree(10)
        self.assertEqual(str(tree), '10')

        tree.insert(5)
        self.assertEqual(str(tree), '10 -> [5 | None]')     

        tree.insert(4)
        self.assertEqual(str(tree), '10 -> [5 -> [4 | None] | None]')

        tree.insert(11)
        self.assertEqual(str(tree), '10 -> [5 -> [4 | None] | 11]')

        tree.insert(6)
        self.assertEqual(str(tree), '10 -> [5 -> [4 | 6] | 11]')


class BSTDeleteTestCase(unittest.TestCase):

    def setUp(self):
        """
                10
              /    \ 
             5      13
            / \    /  \ 
           4   8  11   15   
              /    \ 
             6       12

        10 -> [5 -> [4 | 8 -> [6 | None]] | 13 -> [11 -> [None | 12] | 15]]
        """
        self.tree = BinarySearchTree(10)
        # map(lambda x: self.tree.insert(x), [5, 4, 8, 6, 13, 11, 12, 15])
        for x in [5, 4, 8, 6, 13, 11, 12, 15]:
            self.tree.insert(x)

    def test_not_found(self):
        tree_txt = str(self.tree)
        self.assertRaises(KeyError, self.tree.delete, 100)

    def test_delete_leaf(self):
        self.tree.delete(6)
        self.assertEqual(str(self.tree), '10 -> [5 -> [4 | 8] | 13 -> [11 -> [None | 12] | 15]]')
        self.tree.delete(15)
        self.assertEqual(str(self.tree), '10 -> [5 -> [4 | 8] | 13 -> [11 -> [None | 12] | None]]')

    def test_delete_single_child_parent(self):
        self.tree.delete(11)
        self.assertEqual(str(self.tree), '10 -> [5 -> [4 | 8 -> [6 | None]] | 13 -> [12 | 15]]')

    def test_delete_two_children_parent(self):
        self.tree.delete(13)
        self.assertEqual(str(self.tree), '10 -> [5 -> [4 | 8 -> [6 | None]] | 12 -> [11 | 15]]')

    def test_delete_root(self):
        self.tree.delete(10)
        self.assertEqual(str(self.tree), '8 -> [5 -> [4 | 6] | 13 -> [11 -> [None | 12] | 15]]')