######################
#   Red Black Tree
######################
BLACK = 'black'
RED = 'red'

class RedBlackTree(BinarySearchTree):
    """
    A self-balancing binary tree where:

    - every node is either red or black (null leafs are black)
    - every path from a node to leaf has the same number of black nodes
    - red nodes may have only black children

    Example (parenthesized nodes are RED)

        (40)
        /  \
       30   50
             \
             (60)
    """

    def __init__(self, value):
        self.color = BLACK
        super(RedBlackTree, self).__init__(value)

    def __str__(self):
        txt = '%s:%s' % (self.color, self.value)
        if not self.is_leaf():
            left = str(self.left) if self.left else 'None'
            right = str(self.right) if self.right else 'None'
            txt += ' -> [%s | %s]' % (left, right)

        return txt

    def grandparent(self):
        if self.parent and self.parent.parent:
            return self.parent.parent
        else:
            return None

    def uncle(self):
        granny = self.grandparent()
        if granny:
            return granny.right if granny.left == self.parent else granny.left
        else:
            return None

    def insert_as_bst(self, new_node):
        if new_node.value < self.value:
            if self.left:
                return self.left.insert_as_bst(new_node)
            else:
                self.left = new_node
                new_node.parent = self

        else:
            if self.right:
                self.right.insert_as_bst(new_node)
            else:
                self.right = new_node
                new_node.parent = self

    def insert(self, value):
        """
        First, insert node as a regular BinarySearchTree would do.

        Always insert as RED to avoid black distance problem. 
        After inserting a given node n, there are three cases to be considered:

        1 - father of the inserted node and uncle is RED

             |
             x
           /   \
         (y)   (z)
           \
            (n)

        2 - uncle is BLACK and a child in the opposite direction

             |
             x
           /   \
         (y)    z
           \
            (n)

        3 - uncle is BLACK but in the same direction

              |
              x
            /   \
          (y)   z
          /  
        (n)

        """
        new_node = RedBlackTree(value)
        new_node.color = RED

        self.insert_as_bst(new_node)
        new_node.verify_insertion_case_1()

    def verify_insertion_case_1(self):
        """
             |             |
             G            (G)
           /   \         /   \
         (P)   (U)  =>  P     U
           \             \ 
            (n)          (n) 

        Solution: 
            - switch grandparent, parent and uncle colors. 
            - repeat process on grandparent
        """
        if self.parent and self.parent.color == RED:
            uncle = self.uncle()
            if uncle and uncle.color == RED:
                print('case 1 on %s' % self.value)
                granny = self.grandparent()
                granny.color = RED
                uncle.color = BLACK
                self.parent.color = BLACK
                print('calling again on %s' % granny.value)
                granny.verify_insertion_case_1()

        
    def rotate(self, rotate_right):
        """
        Given a subtree:

         (whatever)
             |
             A
            / \  
           B   z
          / \
         x   y

        where x,y,z are subtrees. Right-rotation is:

         (whatever)
             |
             B
            / \  
           x   A
              / \
             y   z

        Called on node A, returns node B (since it is the new root of the rotated subtree).
        Rotation to the left is the opposite operation.
        """
        # TODO: does not update parent links
        if rotate_right:
            if self.left:
                new_root = self.left
                y_subtree = new_root.right
                new_root.right = self
                self.left = y_subtree
                return new_root
            else:
                return self

        else:
            if self.right:
                new_root = self.right
                y_subtree = new_root.left
                new_root.left = self
                self.right = y_subtree
                return new_root
            else:
                return self

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