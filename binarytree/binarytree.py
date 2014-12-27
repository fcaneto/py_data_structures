import sys

MAX_VAL = sys.maxsize
MIN_VAL = -MAX_VAL - 1


class Node(object):
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value
        self.parent = None

    def set_left(self, node):
        self.left = node
        node.parent = self

    def set_right(self, node):
        self.right = node
        node.parent = self

    def get_max_successor(self):
        max = self
        current = self.right
        while current:
            max = current
            current = current.right

        return max

    def get_inorder_predecessor(self):
        predecessor = None
        current = self.left

        while current:
            if current.right:
                predecessor = current.get_max_successor()
                break
            else:
                predecessor = current
                current = current.left

        return predecessor

    @property
    def has_one_child(self):
        return bool(self.left) != bool(self.right)

    @property
    def is_leaf(self):
        return not self.left and not self.right

    @property
    def grandparent(self):
        return None if not self.parent else self.parent.parent

    @property
    def is_leaf(self):
        return self.left is None and self.right is None

    @property
    def has_grandchildren(self):
        return ((self.left and (self.left.lett or self.right.left)) 
                or 
                (self.right and (self.right.left or self.right.left)))

    @property
    def is_left_child(self):
        return self.parent and self.parent.left == self

    @property
    def is_right_child(self):
        return self.parent and self.parent.right == self

    def _print_node(self):
        return "%s" % self.value

    def __str__(self):
        txt = '%s' % self._print_node()
        if not self.is_leaf:
            left = str(self.left) if self.left else 'None'
            right = str(self.right) if self.right else 'None'
            txt += ' -> [%s | %s]' % (left, right) 

        return txt  


class BinarySearchTree(object):
    """
    Basic binary search tree: 
    - each node has a left and right sub-nodes. 
    - every node has its parent link as well.
    - node.left < node < node.right invariant
    """

    def __init__(self, value):
        self.root = Node(value)

    def __str__(self):
        if self.root:
            return str(self.root)
        else:
            return "[]"

    def __contains__(self, value):
        try:
            self.find(value)
        raise KeyError:
            return False

        return True

    def find(self, value):
        current = self.root
        while current and current.value != value:
            if value < current.value:
                current = current.left
            else:
                current = current.right

        if not current:
            raise KeyError 
        
        return current

    def size(self):
        stack = [self]
        size = 0

        while stack:
            size += 1
            current = stack.pop()
            if current.left:
                stack.append(self.left)
            if self.right:
                current.append(self.right)

        return size

    def insert(self, value, node=None):
        if node is None:
            node = self.root

        if value < node.value:
            if node.left:
                return self.insert(value, node.left)
            else:
                node.left = Node(value)
                node.left.parent = node

        else:
            if node.right:
                return self.insert(value, node.right)
            else:
                node.right = Node(value)
                node.right.parent = node

    def _transplant(self, nodeA, nodeB):
        """
        Puts nodeB into nodeA's position, detaching nodeA from tree.
        """
        if nodeA == self.root:
            self.root = nodeB
        else:
            if nodeA.is_left_child:
                nodeA.parent.left = nodeB
            else:
                nodeA.parent.right = nodeB

        if nodeB is not None:
            nodeB.parent = nodeA.parent

        nodeA.parent = None
        nodeA.left = None
        nodeA.right = None

    def delete(self, value):
        """
        1. If it's a leaf, just remove it.
        2. If it has one child, substitute it by its child.
        3. If it has two children, substitute it by its in-order predecessor.
        """
        target = self.find(value)

        if target.is_leaf:
            self._transplant(target, None)

        elif target.has_one_child:
            if target.left:
                self._transplant(target, target.left)
            else:
                self._transplant(target, target.right)

        else:
            in_order_predecessor = target.get_inorder_predecessor()
            # ideally, should alternate with in_order_successor
            self._transplant(in_order_predecessor, in_order_predecessor.left)
            in_order_predecessor.left = target.left
            in_order_predecessor.right = target.right
            self._transplant(target, in_order_predecessor)
            

##########################
# Function playground
#
# A collection of functions on binary trees

def is_valid_bst(tree):

    def inspect(node, min_val=None, max_val=None):
        if min_val is None:
          min_val = MIN_VAL
        if max_val is None:
          max_val = MAX_VAL

        if node.value < max_val and node.value > min_val:
          is_left_valid = True
          if node.left:
              is_left_valid = inspect(node.left, min_val, node.value)

          is_right_valid = True
          if is_left_valid and node.right:
              is_right_valid = inspect(node.right, node.value, max_val)

          return is_left_valid and is_right_valid

        else:
          return False

    return loop(tree.root)
        

def is_balanced(tree):
    """
    No leaf should have height difference bigger than 1 to any other leaf.
    """
    max_depth = None
    is_balanced = True

    # stack
    nodes_to_visit = [(node, 0)]

    while nodes_to_visit and is_balanced:
      current, depth = nodes_to_visit.pop()

      if current.left:
          nodes_to_visit.append((current.left, depth+1))
      if current.right:
          nodes_to_visit.append((current.right, depth+1))

      if current.is_leaf():
          if not max_depth:
              max_depth = depth
          else: 
              if abs(depth - max_depth) > 1:
                  is_balanced = False
              elif depth > max_depth:
                  max_depth = depth

    return is_balanced



