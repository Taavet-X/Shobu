class Node:

	def __init__(self, key):
		self.parent = None
		self.key = key
		self.childs = None
		self.utility = None
		self.type = "max"

	def getKey(self):
		return self.key

	def setChilds(self, childs):
		for child in childs:
			child.setParent(self)
			if self.type == "max":
				child.setType("min")
			else:
				child.setType("max")
		self.childs = childs

	def setType(self, type):
		self.type = type

	def getType(self):
		return self.type

	def getChilds(self):
		return self.childs

	def setParent(self, parent):
		self.parent = parent

	def getParent(self):
		return self.parent

	def setUtility(self, utility):
		self.utility = utility

	def getUtility(self):
		return self.utility

a = Node(1)

b = Node(2)
c = Node(3)

d = Node(4)
e = Node(5)
f = Node(6)
g = Node(7)

a.setChilds([b, c])
b.setChilds([d, e])
c.setChilds([f, g])

d.setUtility(3)
e.setUtility(2)
f.setUtility(5)
g.setUtility(4)

tree = a

def recorrer_arbol(node):
	childs = node.getChilds()
	if childs == None:
		return node.getUtility(), None
	else:
		if(node.getType() == "max"):
			maxValue = -9223372036854775807
			for child in childs:
				value, selectedChild = recorrer_arbol(child)
				if value > maxValue:
					maxValue = value
					selectedChild = child
			return maxValue, selectedChild
		else:
			minValue = 9223372036854775807
			for child in childs:
				value, selectedChild = recorrer_arbol(child)
				if value < minValue:
					minValue = value
					selectedChild = child
			return minValue, selectedChild

value, node = recorrer_arbol(a)
print(value, node.getKey())

