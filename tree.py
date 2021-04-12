from StatusGenerator import Generator
from Node import Node

class Tree:
	
	def __init__(self, root, player):
		self.root = Node(root)
		self.choice = None
		self.winner = None
		if self.isGoal(self.root):			
			self.winner = 1
		else:
			self.currentDeep = 0
			self.deep = 2
			self.player = player
			self.generador = Generator()
			self.old = [self.root]
			self.generateTree()
			value = self.alphaBeta(self.root)
			self.choice = self.getChoice(self.root)
			if self.isGoal(self.choice):
				self.winner = 2

	def generateTree(self):
		print(self.currentDeep, len(self.old))
		if self.currentDeep == self.deep:
			for node in self.new:
				node.setUtility(self.heuristica(self.root.getKey(), node.getKey()))
		else:
			self.new = []
			for node in self.old:
				for newNode in self.expand(node):
					self.new.append(newNode)
			self.old = self.new
			self.currentDeep += 1
			self.player = self.player % 2 + 1
			self.generateTree()

	def expand(self, node):
		childsAsNodes = []
		if self.isGoal(node):
			node.setUtility(self.heuristica(self.root.getKey(), node.getKey()))			
		else:			
			childsAsList = self.generador.generateStatuses(node.getKey(), self.player)			
			for child in childsAsList: #convertir a nodos
				childsAsNodes.append(Node(child))
			node.setChilds(childsAsNodes)
		if len(childsAsNodes) == 0:
			node.setUtility(self.heuristica(self.root.getKey(), node.getKey()))
		return childsAsNodes
		
	def isGoal(self, node):
		for board in node.getKey():
			contains2 = False
			contains1 = False
			for row in board:
				for value in row:
					if value == 1:
						contains1 = True
					if value == 2:
						contains2 = True
					if contains1 and contains2:
						break
			if not contains1:
				return True
			if not contains2:
				return True

	def getBrother(self, node):
		parent = node.getParent()
		if parent != None:
			childs = parent.getChilds()
			for i in range (len(childs)):
				if node == childs[i]:
					if (i-1)>=0:
						return childs[i-1]
					else:
						return None
		return None

	def remover_nodo(self, node):
		auxValue = 0
		parent = node.getParent()
		if parent != None:
			childs = parent.getChilds()
			for i in range (len(childs)):
				if node == childs[i]:
					auxValue = i+1
					break
			for i in range (len(childs)):
				if i>=auxValue:
					childs.remove(childs[auxValue])

	def alphaBeta(self, node):
		childs = node.getChilds()
		if childs == None:
			return node.getUtility()
		else:
			if(node.getType() == "max"):
				maxValue = -9223372036854775807
				for child in childs:
					value = self.alphaBeta(child)
					brother = self.getBrother(node)
					if value != None:
						if brother != None:
							if value < brother.getUtility():
								if value > maxValue:
									maxValue = value
							else:
								maxValue = value
								node.setUtility(maxValue)
								if node.getParent == None:
									best = node
								self.remover_nodo(child)
								return maxValue
						else:
							if value > maxValue:
								maxValue = value
				node.setUtility(maxValue)
				return maxValue
			else:
				minValue = 9223372036854775807
				for child in childs:
					value = self.alphaBeta(child)
					brother = self.getBrother(node)
					if value != None:
						if brother != None:
							if value > brother.getUtility():
								if value < minValue:
									minValue = value
							else:
								minValue = value
								node.setUtility(minValue)
								self.remover_nodo(child)
								return minValue
						else:
							if value < minValue:
								minValue = value
				node.setUtility(minValue)
				return minValue

	def getChoice(self, root):
		for child in root.getChilds():
			if child.getUtility() == root.getUtility():
				return child

	def contador(self, boards):
	    heuristica = 0
	    player1 = 0
	    player2 = 0
	    for board in boards:
	        for row in board:
	            for value in row:
	                if value == 1:
	                    player1 += 1
	                elif value == 2:
	                    player2 +=1
	    return player1, player2

	def heuristica(self, inicial, final):
	    p1i, p2i = self.contador(inicial)
	    p1c, p2c = self.contador(final)
	    heuristica = (p1i - p1c) - 2*(p2i - p2c)
	    return heuristica
'''
inicial =  [
		[
			[2,2,2,2],
			[0,0,0,0],
			[0,0,0,0],
			[1,1,1,1],
		], [
			[2,2,2,2],
			[0,0,1,0],
			[0,0,0,0],
			[0,1,1,1],
		], [
			[2,2,2,2],
			[0,0,1,0],
			[0,0,0,0],
			[0,1,1,1],
		], [
			[2,2,2,2],
			[0,0,0,0],
			[0,0,0,0],
			[1,1,1,1],
		] ]


tree = Tree(inicial, 2)
generador = Generator()
generador.printStatus(tree.root.getKey())
childs = tree.root.getChilds()
print("childs......")
for child in childs:
	generador.printStatus(child.getKey())
	print(child.getUtility())

generador.printStatus(tree.choice.getKey())
'''

