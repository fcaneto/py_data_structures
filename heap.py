"""
An alternate heap implementation in Python.

TODO:
- benchmark against heapq (time and memory)
"""
import random
import math
from collections import deque

class Heap(object):
    """
    Invariant: P(N) <= N, P(N): parent of N
    """
    
    def __init__(self):
        self.array = []

    def _parent_of(self, i):
        return math.ceil(i/2) - 1

    def _left_of(self, i):
        return (i + 1) * 2 - 1

    def _right_of(self, i):
        return (i + 1) * 2  

    def _swap(self, i, j):
        self.array[i], self.array[j] = self.array[j], self.array[i]

    def extract_min(self):
        """
        Move the tail to the top and bubble-down. Run time: O(logn)
        """
        minimum = self.array[0]
        self._swap(0, len(self) - 1)
        self.array.pop()

        next = 0        
        while next is not None:
            left = self._left_of(next)
            right = self._right_of(next)
            print(next, ', ', left, ', ', right)

            if left >= len(self):
                # leaf
                next = None

            elif right >= len(self): 
                # single child to the left
                if self.array[next] < self.array[left]:
                    next = None
                else:
                    self._swap(next, left)
                    next = left

            else:
                # two children
                if self.array[next] < self.array[left] and self.array[next] < self.array[right]:
                    next = None
                else:
                    if self.array[left] < self.array[right]:
                        self._swap(next, left)
                        next = left
                    else:
                        self._swap(next, right)
                        next = right 

        return minimum

    def find_min(self):
        """
        O(1)
        """
        return self.array[0]

    def __len__(self):
        return len(self.array)

    def __repr__(self):
        return repr(self.array)

    def __iter__(self):
        return self

    def __next__(self):
        if self.heap:
            return self.extract_min()
        else:
            raise StopIteration

    def insert(self, item):
        """
        Insert at the tail and bubble-up. Run time: O(logn)
        """
        self.array.append(item)
        current = len(self.array) - 1
        while current:
            parent = self._parent_of(current)
            if self.array[current] < self.array[parent]:
                self._swap(current, parent)
            current = parent 
        print(self)

    def delete(self, item):
        """
        Not implemented, but can be done in O(logn).
        """
        pass

    def merge(self, other_heap):
        pass


if __name__ == "__main__":
    import random
    import time
    import heapq

    print("Benchmarking against heapq:")

    N = 100000
    sample = []
    for i in range(N):
        sample.append(random.randint(1, 1000))

    print('Sample has %s elements.', N)

    # print('Randomly distributing operations...')

    print('Running test for heapq:')

    expected = sorted(sample)

    now = time.time()

    heap = Heap()
    for n in sample:
        heap.insert(n)

    result = []
    while heap:
        heap.extract_min()

    # print('Expected: ', expected)
    # print('Result', result)




