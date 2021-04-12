from Status import Status
from StatusGenerator import Generator
from Tree import Tree
import threading

class MainViewController:

	def __init__(self, mainView):
		self.gameOver = False
		self.vsMachine = True
		self.status = None
		self.moves = [
			[-1, 0], #arriba
			[-1, 1], #arriba derecha
			[ 0, 1], #derecha
			[ 1, 1], #abajo derecha
			[ 1, 0], #abajo
			[ 1,-1], #abajo izquierda
			[ 0,-1], #izquierda
			[-1,-1], #arriba izquierda
			[-2, 0], #2 arriba
			[-2, 2], #2 arriba derecha
			[ 0, 2], #2 derecha
			[ 2, 2], #2 abajo derecha
			[ 2, 0], #2 abajo
			[ 2,-2], #2 abajo izquierda
			[ 0,-2], #2 izquierda
			[-2,-2], #2 arriba izquierda
		]
		self.generador = Generator()
		self.isPasive = True
		self.player = 1
		self.mainView = mainView
		self.mainView.paintMessage("passiveW")
		self.createBlocks()
		self.oldBlockPosition = None		
		self.newBlockPosition = (-1,-1,-1)		
		self.setStatus([[
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
		]])

	#Se encarga de crear las coordenadas para validaciones, cada uno de los bloques del juego
	def createBlocks(self):
		self.blocks = [
			[271, 55, 311, 85, (0, 0, 0)], 
			[319, 55, 359, 85, (0, 0, 1)], 
			[367, 55, 407, 85, (0, 0, 2)], 
			[415, 55, 455, 85, (0, 0, 3)], 
			[267, 91, 308, 122, (0, 1, 0)], 
			[316, 91, 357, 122, (0, 1, 1)], 
			[365, 91, 406, 122, (0, 1, 2)], 
			[414, 91, 455, 122, (0, 1, 3)], 
			[263, 127, 305, 159, (0, 2, 0)], 
			[313, 127, 355, 159, (0, 2, 1)], 
			[363, 127, 405, 159, (0, 2, 2)], 
			[413, 127, 455, 159, (0, 2, 3)], 
			[259, 163, 302, 196, (0, 3, 0)], 
			[310, 163, 353, 196, (0, 3, 1)], 
			[361, 163, 404, 196, (0, 3, 2)], 
			[412, 163, 455, 196, (0, 3, 3)], 
			[503, 55, 543, 85, (1, 0, 0)], 
			[551, 55, 591, 85, (1, 0, 1)], 
			[599, 55, 639, 85, (1, 0, 2)], 
			[647, 55, 687, 85, (1, 0, 3)], 
			[504, 91, 545, 122, (1, 1, 0)], 
			[553, 91, 594, 122, (1, 1, 1)], 
			[602, 91, 643, 122, (1, 1, 2)], 
			[651, 91, 692, 122, (1, 1, 3)], 
			[505, 127, 547, 159, (1, 2, 0)], 
			[555, 127, 597, 159, (1, 2, 1)], 
			[605, 127, 647, 159, (1, 2, 2)], 
			[655, 127, 697, 159, (1, 2, 3)], 
			[506, 163, 549, 196, (1, 3, 0)], 
			[557, 163, 600, 196, (1, 3, 1)], 
			[608, 163, 651, 196, (1, 3, 2)], 
			[659, 163, 702, 196, (1, 3, 3)], 
			[243, 280, 288, 318, (2, 0, 0)], 
			[297, 280, 342, 318, (2, 0, 1)], 
			[351, 280, 396, 318, (2, 0, 2)], 
			[405, 280, 450, 318, (2, 0, 3)], 
			[238, 328, 284, 367, (2, 1, 0)], 
			[293, 328, 339, 367, (2, 1, 1)], 
			[348, 328, 394, 367, (2, 1, 2)], 
			[403, 328, 449, 367, (2, 1, 3)], 
			[233, 376, 280, 416, (2, 2, 0)], 
			[289, 376, 336, 416, (2, 2, 1)], 
			[345, 376, 392, 416, (2, 2, 2)], 
			[401, 376, 448, 416, (2, 2, 3)], 
			[228, 424, 276, 465, (2, 3, 0)], 
			[285, 424, 333, 465, (2, 3, 1)], 
			[342, 424, 390, 465, (2, 3, 2)], 
			[399, 424, 447, 465, (2, 3, 3)], 
			[507, 280, 552, 318, (3, 0, 0)], 
			[561, 280, 606, 318, (3, 0, 1)], 
			[615, 280, 660, 318, (3, 0, 2)], 
			[669, 280, 714, 318, (3, 0, 3)], 
			[509, 328, 555, 367, (3, 1, 0)], 
			[564, 328, 610, 367, (3, 1, 1)], 
			[619, 328, 665, 367, (3, 1, 2)], 
			[674, 328, 720, 367, (3, 1, 3)], 
			[511, 376, 558, 416, (3, 2, 0)], 
			[567, 376, 614, 416, (3, 2, 1)], 
			[623, 376, 670, 416, (3, 2, 2)], 
			[679, 376, 726, 416, (3, 2, 3)], 
			[513, 424, 561, 465, (3, 3, 0)], 
			[570, 424, 618, 465, (3, 3, 1)], 
			[627, 424, 675, 465, (3, 3, 2)], 
			[684, 424, 732, 465, (3, 3, 3)], 
		]

	#Se encarga de validar la posicion del mouse, a medida que este se mueve.
	def	mouse_move(self, event):		
		for block in self.blocks:
			if(event.x >= block[0] and event.x <= block[2] and event.y >= block[1] and event.y <= block[3]):
				if block[4] != self.newBlockPosition:
					self.newBlockPosition = block[4]
					self.mainView.canvas['cursor']="hand2"
				return
		self.newBlockPosition = (-1,-1,-1)
		self.mainView.canvas['cursor']="arrow"		
		return

	def mouse_click(self, event):
		if not self.gameOver:
			if self.oldBlockPosition != None: #Si una ficha habia sido seleccionada anteriormente
				if self.newBlockPosition == (-1,-1,-1): #SI la nueva posicion es una posicion fuera de los tableros
					self.oldBlockPosition == None #?? Deberia cancelarce el momvimiento							
				else: #en caso de que la nueva posicion seleccionada es una posicion dentro de los tableros
					self.newPositionValue = self.status[self.newBlockPosition[0]][self.newBlockPosition[1]][self.newBlockPosition[2]]
					if self.oldBlockPosition == self.newBlockPosition:
						print("canceled move") #aqui el jugador no pierde el turno
						#self.isPasive = not self.isPasive
						
						if self.newPositionValue != 0:
							self.mainView.removePiece(self.newBlockPosition[0], self.newBlockPosition[1], self.newBlockPosition[2])
						self.status[self.newBlockPosition[0]][self.newBlockPosition[1]][self.newBlockPosition[2]] = self.selectedValue
						self.mainView.paintPiece(self.selectedValue, self.newBlockPosition[0], self.newBlockPosition[1], self.newBlockPosition[2])
						
						#self.status[self.newBlockPosition[0]][self.newBlockPosition[1]][self.newBlockPosition[2]] = self.selectedValue
						#self.setStatus(self.status)
						self.oldBlockPosition = None
					#move
					else:
						board = self.oldBlockPosition[0]
						newBoard = self.newBlockPosition[0]
						row = self.oldBlockPosition[1]
						column = self.oldBlockPosition[2]
						rowOperation = self.newBlockPosition[1] - self.oldBlockPosition[1]
						columnOperation = self.newBlockPosition[2] - self.oldBlockPosition[2]
						onSameBoard = self.oldBlockPosition[0] == self.newBlockPosition[0]
						#validacion
						if self.isPasive:
							if onSameBoard and self.isValidPassiveMove(self.status, board, row, column, rowOperation, columnOperation):

								#Logica de movimiento en GUI

								if self.newPositionValue != 0:
									self.mainView.removePiece(self.newBlockPosition[0], self.newBlockPosition[1], self.newBlockPosition[2])
								self.status[self.newBlockPosition[0]][self.newBlockPosition[1]][self.newBlockPosition[2]] = self.selectedValue
								self.mainView.paintPiece(self.selectedValue, self.newBlockPosition[0], self.newBlockPosition[1], self.newBlockPosition[2])

								#self.status[self.newBlockPosition[0]][self.newBlockPosition[1]][self.newBlockPosition[2]] = self.selectedValue
								#self.setStatus(self.status)

								self.oldBlockPosition = None
								self.isPasive = False
								if self.player == 1:
									self.mainView.paintMessage("agroW")
								else:
									self.mainView.paintMessage("agroB")

								self.oldPassive = self.generador.copyStatus(self.status)#--------
								self.generador.setPlayer(self.player)
								self.possibleAggresiveMoves = self.generador.findAggressiveMoves(self.status, board, rowOperation, columnOperation)								
							else:
								self.mainView.paintMessage
								self.mainView.paintMessage("invalid")
								print("Movimiento no valido")
						else: #Si el movimiento es de llegada y no es pasivo
							self.generador.setPlayer(self.player)
							aggresiveMove = self.generador.generateAggressiveMove(self.oldPassive, newBoard, row, column, rowOperation, columnOperation)
							
							isAggressiveValid = False
							if aggresiveMove != None:
								for possibleAggresiveMove in self.possibleAggresiveMoves:
									if possibleAggresiveMove == aggresiveMove:
										isAggressiveValid = True
										break

							if isAggressiveValid:
								#self.generador.printStatus(aggresiveMove)
								self.setStatus(aggresiveMove)
								'''
								if self.newPositionValue != 0:
									self.mainView.removePiece(self.newBlockPosition[0], self.newBlockPosition[1], self.newBlockPosition[2])
								self.status[self.newBlockPosition[0]][self.newBlockPosition[1]][self.newBlockPosition[2]] = self.selectedValue
								self.mainView.paintPiece(self.selectedValue, self.newBlockPosition[0], self.newBlockPosition[1], self.newBlockPosition[2])
								'''
								self.oldBlockPosition = None
								self.player = self.player % 2 + 1							
								self.isPasive = True

								if self.player == 1:
									self.mainView.paintMessage("passiveW")
								else:
									self.mainView.paintMessage("passiveB")

								#next player move
								if self.vsMachine:
									x = threading.Thread(target=self.machineMove)
									x.start()
							else:
								self.mainView.paintMessage("invalid") 
								print("No es un movimiento agresivo no valido")
			else: 
				if self.newBlockPosition != (-1,-1,-1):
					self.selectedValue = self.status[self.newBlockPosition[0]][self.newBlockPosition[1]][self.newBlockPosition[2]]
					board = self.newBlockPosition[0]
					#validar que no se puedan hacer movimientos que no se encuentren en las posibilidades de los agresivos
					if self.selectedValue != 0:
						if self.selectedValue == self.player:

							if self.isPasive:
								if (self.player == 1 and board != 2 and board != 3) or (self.player == 2 and board != 0 and board != 1):
									print("El movimiento debe ser en el homeboard")
									self.mainView.paintMessage("noHome")
								else:		
									self.status[self.newBlockPosition[0]][self.newBlockPosition[1]][self.newBlockPosition[2]] = 0
									self.mainView.removePiece(self.newBlockPosition[0], self.newBlockPosition[1], self.newBlockPosition[2])
									self.oldBlockPosition = self.newBlockPosition
							else:
								self.status[self.newBlockPosition[0]][self.newBlockPosition[1]][self.newBlockPosition[2]] = 0
								self.mainView.removePiece(self.newBlockPosition[0], self.newBlockPosition[1], self.newBlockPosition[2])
								self.oldBlockPosition = self.newBlockPosition
						else:
							print("El turno no es el de la ficha seleccionada")
							self.mainView.paintMessage("noToken")
				
	def isValidPassiveMove(self, status, board, row, column, rowOperation, columnOperation):
		isValidResult = False
		for move in self.moves:
			if move == [rowOperation, columnOperation]:				
				isValidResult = True
				break
		if not isValidResult:
			return False
		elif abs(rowOperation) == 1 or abs(columnOperation) == 1:
			return status[board][row + rowOperation][column + columnOperation] == 0
		else:
			rowMultiplier = int(rowOperation / -2)
			columnMultiplier = int(columnOperation / -2)
			if status[board][row + (rowOperation + 1 * rowMultiplier)][column + (columnOperation + 1*columnMultiplier)] == 0:
				if status[board][row + (rowOperation + 0 * rowMultiplier)][column + (columnOperation + 0*columnMultiplier)] == 0:
					return True
			else:
				return False

	def machineMove(self):
		print("Turno maquina")
		tree = Tree(self.status, self.player)
		choice = tree.choice
		if choice == None:
			gameOver = True
		else:
			self.setStatus(choice.getKey())
			self.player = self.player % 2 + 1
			self.mainView.paintMessage("passiveW")

	def setStatus(self, status):
		for tableIndex in range(4):
			for rowIndex in range(4):
				for columnIndex in range(4):
					value = status[tableIndex][rowIndex][columnIndex]
					if self.status == None:				
						if value != 0:
							self.mainView.paintPiece(value, tableIndex, rowIndex, columnIndex)
					else:
						if self.status[tableIndex][rowIndex][columnIndex] != status[tableIndex][rowIndex][columnIndex]:
							self.mainView.removePiece(tableIndex, rowIndex, columnIndex)
							if value != 0:
								self.mainView.paintPiece(value, tableIndex, rowIndex, columnIndex)
		self.status = status


