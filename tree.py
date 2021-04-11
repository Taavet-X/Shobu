from StatusGenerator import Generator
from Node import Node

class Tree:
	
	def __init__(self, root):
		self.root = Node(root)
		self.currentDeep = 0
		self.deep = 2
		self.player = 2
		self.generador = Generator()
		self.old = [self.root]		
		return self.generateTree()

	def generateTree(self):
		print(self.currentDeep, len(self.old))
		if self.currentDeep == self.deep:
			return self.root
		else:
			new = []
			for node in self.old:
				for newNode in self.expand(node):
					new.append(newNode)
			self.old = new
			self.currentDeep += 1
			self.player = self.player % 2 + 1
			self.generateTree()

	def expand(self, node):
		#Pregunta si es meta.
		childsAsNodes = []
		if not self.isGoal(node):
			childsAsList = self.generador.generateStatuses(node.getKey(), self.player)
			
			for child in childsAsList: #convertir a nodos
				childsAsNodes.append(Node(child))
			node.setChilds(childsAsNodes)
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
				print("Gano Jugador 2")
				return True
			if not contains2:
				print("Gano Jugador 1")
				return True

inicial =  [
		[
			[2,2,2,2],
			[0,0,0,0],
			[0,0,0,0],
			[1,1,1,1],
		], [
			[2,2,2,2],
			[0,0,0,0],
			[0,0,0,0],
			[1,1,1,1],
		], [
			[2,2,2,2],
			[0,0,0,0],
			[0,0,0,0],
			[1,1,1,1],
		], [
			[2,2,2,2],
			[0,0,0,0],
			[0,0,0,0],
			[1,1,1,1],
		] ]

tree = Tree(inicial)
print(tree)
