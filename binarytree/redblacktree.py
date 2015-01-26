from .binarytree import Node, BinarySearchTree

BLACK = 'black'
RED = 'red'

class RedBlackNode(Node):
    def __init__(self, value):
        self.color = BLACK
        super(RedBlackNode, self).__init__(value)

    def _print_node(self):
      return "%s:%s" % (self.color, self.value)

    @property
    def uncle(self):
        granny = self.grandparent
        if granny:
            return granny.right if granny.left == self.parent else granny.left
        else:
            return None


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
            /  \ 
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