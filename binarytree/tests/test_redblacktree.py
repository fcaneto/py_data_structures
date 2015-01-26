class RedBlackInsertTestCase(unittest.TestCase):

    def testInsertBaseCase(self):
        tree = RedBlackTree(10)
        self.assertEqual(str(tree), 'black:10')

    def testInsertBlackParent(self):
        tree = RedBlackTree(10)

        tree.insert(15)
        self.assertEqual(str(tree), 'black:10 -> [None | red:15]')

        tree.insert(5)
        self.assertEqual(str(tree), 'black:10 -> [red:5 | red:15]')

    def testInsertRedParent(self):

        tree = RedBlackTree(10)
        tree.insert(15)
        tree.insert(5)
        tree.insert(2)

        self.assertEqual(str(tree), 'red:10 -> [black:5 -> [red:2 | None] | black:15]')

        # setting up a two generation verification
        tree.insert(6)
        self.assertEqual(str(tree), 'red:10 -> [black:5 -> [red:2 | red:6] | black:15]')

        # # this inserting will have to execute case 1 twice
        tree.insert(1)
        self.assertEqual(str(tree), 'red:10 -> [red:5 -> [black:2 -> [red:1 | None] | black:6] | black:15]')



    def testRightRotation(self):
        """
        Test tree is:

             A
            / \  
           B   z
          / \
         x   y

        """
        node_A = RedBlackTree('A')

        node_B = RedBlackTree('B')
        leaf_x = RedBlackTree('x')
        node_B.set_left(leaf_x) 
        leaf_y = RedBlackTree('y')
        node_B.set_right(leaf_y)

        node_A.left = node_B
        leaf_z = RedBlackTree('z')
        node_A.set_right(leaf_z)

        self.assertEqual(str(node_A), 'black:A -> [black:B -> [black:x | black:y] | black:z]')

        rotated_tree = node_A.rotate(rotate_right=True)
        self.assertEqual(str(rotated_tree), 'black:B -> [black:x | black:A -> [black:y | black:z]]')

    def testLeftRotation(self):
        """
        Test tree is:

             B
            / \  
           x   A
              / \
             y   z

        """
        node_B = RedBlackTree('B')

        leaf_x = RedBlackTree('x')
        node_B.set_left(leaf_x)
        
        node_A = RedBlackTree('A')
        leaf_y = RedBlackTree('y')
        node_A.set_left(leaf_y)
        leaf_z = RedBlackTree('z')
        node_A.set_right(leaf_z)

        node_B.set_right(node_A)
        self.assertEqual(str(node_B), 'black:B -> [black:x | black:A -> [black:y | black:z]]')

        rotated_tree = node_B.rotate(rotate_right=False)
        self.assertEqual(str(rotated_tree), 'black:A -> [black:B -> [black:x | black:y] | black:z]')