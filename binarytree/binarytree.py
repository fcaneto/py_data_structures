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

	def has_one_child(self):
		return bool(self.left) != bool(self.right)

	def is_leaf(self):
		return not self.left and not self.right

	def __str__(self):
		txt = '[%s' % self.value
		if not self.is_leaf():
			left = str(self.left) if self.left else 'None'
			right = str(self.right) if self.right else 'None'
			txt += ' -> [%s | %s]' % (left, right) 
		txt += ']'

		return txt	


class BinarySearchTree(object):
	"""
	Basic binary search tree: 
	- each node has a left and right sub-nodes. 
	- every node has its parent link as well.
	- node.left < node < node.right invariant
	"""

	def __init__(self):
		self.root = None

	def __str__(self):
		str(self.root)

	def min(self):
		minimum = self
		current = self.left

		while current:
			minimum = current
			current = current.left

		return minimum

	def max(self):
		maximum = self
		current = self.right

		while current:
			maximum = current
			current = current.right

		return maximum

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

	# def visit_in_order(self, function):

	# 	if self.left:
	# 		self.left.visit_in_order(function)

	# 	function(self)

	# 	if self.right:
	# 		self.right.visit_in_order(function)

	def insert(self, value):
		if value < self.value:
			if self.left:
				return self.left.insert(value)
			else:
				self.left = Node(value)
				self.left.parent = self

		else:
			if self.right:
				return self.right.insert(value)
			else:
				self.right = Node(value)
				self.right.parent = self

	def delete(self, value):
		"""
		1. If it's a leaf, just remove it.
		2. If it has one child, substitute it by its child.
		3. If it has two children, substitute it by its in-order predecessor.
		"""
		is_left_child = None
		current = self

		# find it
		while current and current.value != value:
			if value < current.value:
				current = current.left
				is_left_child = True
			else:
				current = current.right
				is_left_child = False

		if not current:
			# not found
			return

		if current.is_leaf():
			if is_left_child:
				current.parent.left = None
			else:
				current.parent.right = None
			current.parent = None

		elif current.has_one_child():
			child = current.left if current.left else current.right
			if is_left_child:
				current.parent.left = child
			else:
				current.parent.right = child
			child.parent = current.parent
			current.parent = None

		else:
			in_order_predecessor = self.left.max()
			# ideally, should alternate with in_order_successor
			# in_order_successor = self.right.min()
			temp = in_order_predecessor.value
			self.delete(in_order_predecessor.value)
			self.value = temp

	
# @staticmethod
	# def is_valid_bst(node, min_val=None, max_val=None):
	# 	if min_val is None:
	# 		min_val = MIN_VAL
	# 	if max_val is None:
	# 		max_val = MAX_VAL

	# 	if node.value < max_val and node.value > min_val:
	# 		is_left_valid = True
	# 		if node.left:
	# 			is_left_valid = BinaryTree.is_valid_bst(node.left, min_val, node.value)

	# 		is_right_valid = True
	# 		if is_left_valid and node.right:
	# 			is_right_valid = BinaryTree.is_valid_bst(node.right, node.value, max_val)

	# 		return is_left_valid and is_right_valid

	# 	else:
	# 		return False
	# @staticmethod
	# def serialize(output, bst):
		
	# 	stack = []
	# 	if not bst:
	# 		return
		
	# 	stack.append(bst)
	# 	while stack:
	# 		current = stack.pop()
	# 		output.write("%s\n" % current.value)
	# 		if current.right:
	# 			stack.append(current.right)
	# 		if current.left:
	# 			stack.append(current.left)

	# @staticmethod
	# def deserialize(input_source):

	# 	value = input_source.readline()
	# 	print(value)

	# 	if not value:
	# 		return None

	# 	max_value = MAX_VAL
	# 	value = input_source.readline()
	# 	root = BinarySearchTree(value)

	# 	_deserialize_recursively(input_source, root)

	# @staticmethod
	# def _deserialize_recursively(input_source, current_node, max_val=None):

	# 	if max_val is None:
	# 		max_val = MAX_VAL

	# 	value = input_source.readline()
	# 	print(">> %s <<" % value)

	# 	if value < current_node.value:
	# 		# go left
	# 		current_node.left = BinarySearchTree(value)
	# 		value = _deserialize_recursively(input_source, current_node.left, current_node.value)

	# 	if value < max_val:
	# 		# go right
	# 		current_node.right = BinarySearchTree(value)
	# 		value = _deserialize_recursively(input_source, current_node.right, max_val)

	# 	return value
		

	# @staticmethod
	# def is_balanced(node, depth=0):
	# 	"""
	# 	No leaf should have height difference bigger than 1 to any other leaf.
	# 	"""
	# 	max_depth = None
	# 	is_balanced = True

	# 	# stack
	# 	nodes_to_visit = [(node, 0)]

	# 	while nodes_to_visit and is_balanced:
	# 		current, depth = nodes_to_visit.pop()

	# 		if current.left:
	# 			nodes_to_visit.append((current.left, depth+1))
	# 		if current.right:
	# 			nodes_to_visit.append((current.right, depth+1))

	# 		if current.is_leaf():
	# 			if not max_depth:
	# 				max_depth = depth
	# 			else: 
	# 				if abs(depth - max_depth) > 1:
	# 					is_balanced = False
	# 				elif depth > max_depth:
	# 					max_depth = depth

	# 	return is_balanced



