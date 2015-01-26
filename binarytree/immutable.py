
from .binarytree import BinaryTree
from .redblacktree import RedBlackNode


class ImmutableRedBlackTree(BinaryTree):

    def insert(self, value):
        pass

    def delete(self, value):
        pass


def insert(node, value):
    new = None

    if value > node.value:
        if node.right:
            return insert(node.right, value)
        else:
            new = RBTNode(value, color=RED, parent=node)
            node.right = new

    else:
        if node.left:
            return insert(node.left, value)
        else:
            new = RBTNode(value, color=RED, parent=node)
            node.left = new

    return rebalance(new)
    

def rebalance(node):
    """
    Okasaki's balance method.

    Consider that x < y < z (nodes) and a < b < c < d (subtrees).
    There are four ways rebalance is needed (parenthized nodes are RED):

      Case I:     Case II:       Case3:         Case 4
           z           z            x               x
          / \         / \          / \             / \ 
        (y)  d      (x)  d        a  (z)          a  (y) 
        / \         / \              /  \            / \ 
      (x)  c       a  (y)         (y)    d          b  (z)
      / \             / \         /  \                 / \ 
     a   b           b   c       b    c               c   d

    For all patterns above, the resulting tree is:

            (y)
           /   \ 
          x     z
         / \   / \ 
        a   b c   d

    Recursion goes bottom-up.
    """
    if node.is_root:
        if node.is_red: 
            # base case: root is red => recolor it  
            node.color = BLACK
        
        return node

    if node.is_leaf or not node.has_grandchildren or node.is_black:
        return rebalance(node.parent)

    if node.is_black:
        case1 = node.left and node.left.is_red and node.left.left and node.left.left.is_red
        case2 = node.left and node.left.is_red and node.left.right and node.left.right.is_red
        case3 = node.right and node.right.is_red and node.right.left and node.right.left.is_red
        case4 = node.right and node.right.is_red and node.right.right and node.right.right.is_red

        parent = node.parent
        if case1:
            x = node.left.left
            y = node.left
            z = node
            a = x.left
            b = y.right
            c = y.right
            d = node.right
        elif case2:
            x = node.left
            y = node.left.right
            z = node
            a = x.left
            b = y.left
            c = y.right
            d = z.right
        elif case3:
            x = node
            y = x.right
            z = y.left
            a = x.left
            b = z.left
            c = z.right
            d = y.right
        elif case4:
            x = node
            y = x.right
            z = y.right
            a = x.left
            b = y.left
            c = z.left
            d = z.right
        
        if case1 or case2 or case3 or case4:
            return RBTNode(value=y.value, 
                           parent=parent,
                           color=RED,   
                           left=RTBNode(value=x.node, color=BLACK, left=a, right=b), 
                           right=RTBNode(value=z.node, color=BLACK, left=c, right=d))
        else:
            return node


class RBTNodeTestCase(unittest.TestCase):

    def test(self):
        root = RBTNode(10)
        print(root)
        print(insert(root, 11))
        print(insert(root, 5))
        print(insert(root, 1))


if __name__ == '__main__':
    unittest.main()





        
