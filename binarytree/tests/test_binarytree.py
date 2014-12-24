import unittest

from binarytree import BinaryTree, BinarySearchTree

class BinaryTreeTestCase(unittest.TestCase):

    def test_is_bst_valid(self):
        root = BinaryTree(10)
        root.set_left(BinaryTree(8))
        root.left.set_left(BinaryTree(7))
        root.left.left.set_left(BinaryTree(6))
        root.left.set_right(BinaryTree(9))
        root.set_right(BinaryTree(15))
        root.right.set_left(BinaryTree(13))
        root.right.set_right(BinaryTree(17))

        self.assertTrue(BinaryTree.is_valid_bst(root))

    def test_is_bst_invalid(self):
        root = BinaryTree(10)
        root.set_left(BinaryTree(8))
        root.left.set_left(BinaryTree(11)) ## invalid node as left child
        root.left.left.set_left(BinaryTree(6))
        root.left.set_right(BinaryTree(9))
        root.set_right(BinaryTree(15))
        root.right.set_left(BinaryTree(13))
        root.right.set_right(BinaryTree(17))

        self.assertFalse(BinaryTree.is_valid_bst(root))

        root = BinaryTree(10)
        root.set_left(BinaryTree(8))
        root.left.set_left(BinaryTree(7))
        root.left.left.set_left(BinaryTree(6))
        root.left.set_right(BinaryTree(9))
        root.set_right(BinaryTree(15))
        root.right.set_left(BinaryTree(13))
        root.right.set_right(BinaryTree(12)) # invalid node as right child

        self.assertFalse(BinaryTree.is_valid_bst(root))


class BSTInsertTestCase(unittest.TestCase):

    def test_insert(self):
        root = BinarySearchTree(10)
        self.assertEqual(str(root), '[10]')

        root.insert(5)
        self.assertEqual(str(root), '[10 -> [[5] | None]]')     

class BSTDeleteTestCase(unittest.TestCase):

    def setUp(self):
        """
                10
              /    \
             5      13
            / \    /  \
           4   6  11   15   
                    \
                     12
                  
        """
        self.root = BinarySearchTree(10)
        map(lambda x: self.root.insert(x), [5, 4, 6, 13, 11, 12, 15])

    def test_not_found(self):
        tree_txt = str(self.root)
        self.root.delete(100)
        self.assertEqual(tree_txt, str(self.root))

    def test_delete_leaf(self):
        self.root.delete(4)
        self.assertEqual(str(self.root), '[10 -> [[5 -> [None | [6]]] | [13 -> [[11 -> [None | [12]]] | [15]]]]]')
        self.root.delete(15)
        self.assertEqual(str(self.root), '[10 -> [[5 -> [None | [6]]] | [13 -> [[11 -> [None | [12]]] | None]]]]')

    def test_delete_single_child_parent(self):
        self.root.delete(11)
        self.assertEqual(str(self.root), '[10 -> [[5 -> [[4] | [6]]] | [13 -> [[12] | [15]]]]]')
        
    def test_in_order_predecessor_is_leaf(self):
        import pdb
        pdb.set_trace()
        self.root.delete(10)
        self.assertEqual(str(self.root), '[6 -> [[5 -> [[4] | None]] | [13 -> [[11 -> [None | [12]]] | [15]]]]]')