"""
Skip-list implementation.

Skip-lists is a cool way to achieve on average O(logn) search operations on a set without 
having to deal with colors and rotations (no balanced trees).

Think about the NYC subway: express lines!
All lists are ordered, but only the bottom one has all elements.
The other ones are shortcuts (see below for insertion).

0: [-INF] ---------------------------------------> [70]
     |                                              |
1: [-INF] ---------------> [10] -----------------> [70]
     |                      |                       |       
2: [-INF] -> [2] -> [5] -> [10] -> [13] -> [20] -> [70]

Searching for 20 goes like this:
level 0: -INFINTY -> down
level 1: -INFINITY -> 10 -> down
level 2: 10 -> 13 -> 20

Adding 43 goes like this:
- find position in the bottom list, stacking your way through. 
  For 43 we have the following stack: 
  [20, level 2], [10, level 1], [-INF, level 0]
- Insert to the left of the stack top
- Do a coin flip! Depending on the result, the new node may propagate to an upper level above or not.
- Propagations may create new lists on top. On average, about log(n) lists should be expected.

One possible result after adding 43:
0: [-INF] -----------------------------------------------> [70]
    |                                                       |
1: [-INF] ---------------> [10] -----------------> [43] -> [70]  ==> coin flips got 43 up to this level.
    |                        |                       |       |
2: [-INF] -> [2] -> [5] -> [10] -> [13] -> [20] -> [43] -> [70] 

"""
import random
import sys
from collections import deque

import unittest
from unittest.mock import MagicMock

MIN_INT = -sys.maxsize

class Node(object):
        def __init__(self, value=MIN_INT):
            self.value = value
            self.next = None
            self.down = None

        @property
        def next_value(self):
            if self.next is None:
                return None
            else:
                return self.next.value

        def insert_after(self, x):
            new_node = Node(x)
            if self.next:
                new_node.next = self.next

            self.next = new_node
            return new_node


class SkipList(object):

    def __init__(self, max_height=32):
        self.lists = deque()
        self.lists.append(Node())

    def find_position(self, x):
        """
        Returns a stack of nodes through which x should be positioned.
        If x is in the skip list, x will be returned in the top of the stack.
        Otherwise, the top of the stack will have the previous node of where x should be.
        """
        stack = deque()
        
        found = False
        current = self.lists[0]

        while current is not None:
            stack.appendleft(current)

            if x == current.value:
                found = True
                break
            else:
                if current.next_value:
                    if x < current.next_value:
                        current = current.down
                    else:
                        stack.popleft()
                        current = current.next
                else:
                    current = current.down

        return stack

    def _randomize(self):
        return random.randint(0, 1) == 1

    def insert(self, x):
        """
        - Search for x position in bottom list.
        - Insert x in bottom list, maintaining invariance.
        """            
        stack = self.find_position(x)

        assert stack, "Method find_position should return at least one element."
        
        position_found = stack.popleft()
        if position_found.value == x:
            # Element already exists
            return

        created_node = position_found.insert_after(x)

        # if lucky, keep adding element in an upper list
        while(self._randomize()):
            predecessor_upper_list = stack.popleft() if stack else None
            if predecessor_upper_list is not None:
                new_node = predecessor_upper_list.insert_after(x)
            else:
                # create a new list on top
                self.lists.appendleft(Node())
                self.lists[0].down = self.lists[1]
                new_node = self.lists[0].insert_after(x)

            new_node.down = created_node
            created_node = new_node 

    def __contains__(x):
        stack = self.find_position(x)
        return stack and stack.popleft() == x

    def __str__(self):
        txt = []
        current_line_head = self.lists[0]
        while current_line_head:
            current = current_line_head
            while current:
                txt.append('[%s] -> ' % (current.value if current.value != MIN_INT else '-INF'))
                current = current.next
            current_line_head = current_line_head.down
            if current_line_head:
                txt.append('\n')

        return ''.join(txt)


class InsertTestCase(unittest.TestCase):

    def testInsertOnEmptyNotCreatingUpperList(self):      
        return_values = [False]
        def side_effect(*args, **kwargs):
            return return_values.pop()

        s = SkipList()
        s._randomize = MagicMock(side_effect=side_effect)
        s.insert(1)

        self.assertEqual(len(s.lists), 1)
        self.assertEqual(s.lists[0].next_value, 1)
        self.assertIsNone(s.lists[0].down)
        self.assertIsNone(s.lists[0].next.down)

    def testInsertOnEmptyCreatingUpperLists(self):      
        return_values = [False, True, True] # will end with 3 layers
        def side_effect(*args, **kwargs):
            return return_values.pop()

        s = SkipList()
        s._randomize = MagicMock(side_effect=side_effect)
        s.insert(1)

        self.assertEqual(len(s.lists), 3)
        layer_0 = s.lists[0]
        self.assertEqual(layer_0.next_value, 1)
        self.assertIsNone(layer_0.next.next)

        layer_1 = s.lists[1]
        self.assertEqual(layer_1.next_value, 1)
        self.assertIsNone(layer_1.next.next)
        self.assertEqual(layer_0.down, layer_1)
        self.assertEqual(layer_0.next.down, layer_1.next)

        layer_2 = s.lists[2]
        self.assertEqual(layer_2.next_value, 1)
        self.assertIsNone(layer_2.next.next)
        self.assertEqual(layer_1.down, layer_2)
        self.assertEqual(layer_1.next.down, layer_2.next)

    def testInsertInMiddle(self):
        pass

    def InsertOnTail(self):
        pass


if __name__ == "__main__":
    unittest.main()



