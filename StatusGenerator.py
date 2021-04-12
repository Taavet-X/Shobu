class Generator:

	def __init__(self):
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

	#genera los posibles estados a los cuales puede llegarse
	#a partir de uno dado
	def generateStatuses(self, initialStatus, player):
		self.initialStatus = initialStatus
		self.player = player
		self.passiveMoves, self.operations = self.findPassiveMoves(self.initialStatus)
		statuses = []
		for i in range(len(self.passiveMoves)):
			status = self.passiveMoves[i]
			board = self.operations[i][0]
			rowOperation = self.operations[i][1]
			columnOperation = self.operations[i][2]
			posibleAggressiveMoves = self.findAggressiveMoves(status, board, rowOperation, columnOperation)
			if len(posibleAggressiveMoves) != 0:
				for posibleAggressiveMove in posibleAggressiveMoves:
					statuses.append(posibleAggressiveMove)
		return statuses

	#se encarga de encontrar los posibles movimientos pasivos
	def findPassiveMoves(self, status):
		homeboardPieces = self.findHomeboardPieces(status)
		statuses = []
		operations = []
		for homeboardPiece in homeboardPieces: #por cada pieza en el homeboard
			board = homeboardPiece[0]
			row = homeboardPiece[1]
			column = homeboardPiece[2]
			for move in self.moves: #por cada movimiento posible en el juego	
				rowOperation = move[0] #representa el movimiento que se hara en las filas
				columnOperation = move[1] #representa el moviento en las columnas
				if ( (row + rowOperation) >= 0) and ( (row + rowOperation) <= 3) and ( (column + columnOperation) >= 0) and ( (column + columnOperation) <= 3):
					if self.isValidPassiveMove(status, board, row, column, rowOperation, columnOperation):
						statusCopy = self.copyStatus(status)					
						statusCopy[board][ row ][ column ] = 0
						statusCopy[board][ row + rowOperation ][ column + columnOperation ] = self.player
						statuses.append(statusCopy)
						operations.append((board,rowOperation,columnOperation))
		return statuses, operations
	
	#Se encarga de buscar las fichas del homeboard del jugador en turno,
	def findHomeboardPieces(self, status):
		homeboardPieces = []
		homeboards = []
		if self.player == 1:
			homeboards = [2, 3]
		else:
			homeboards = [0, 1]
		for board in homeboards:
			for row in range(4):
				for column in range(4):
					if status[board][row][column] == self.player: 
						homeboardPieces.append((board,row,column))
		return homeboardPieces

	#Valida si un movimiento pasivo es valido
	def isValidPassiveMove(self, status, board, row, column, rowOperation, columnOperation):
		if abs(rowOperation) == 1 or abs(columnOperation) == 1:
			return status[board][row + rowOperation][column + columnOperation] == 0
		else:
			rowMultiplier = int(rowOperation / -2)
			columnMultiplier = int(columnOperation / -2)
			if status[board][row + (rowOperation + 1 * rowMultiplier)][column + (columnOperation + 1*columnMultiplier)] == 0:
				if status[board][row + (rowOperation + 0 * rowMultiplier)][column + (columnOperation + 0*columnMultiplier)] == 0:
					return True
			else:
				return False

	#Encuentra los posibles movimientos agresivos, retorna la lista de estos.
	#recibe el estado que supone es luego del movimiento pasivo.
	def findAggressiveMoves(self, status, boardOperation, rowOperation, columnOperation):
		posibleAggressiveMoves = [] #estados
		aggressiveMovePieces = self.findAggressiveMovePieces(status, boardOperation)		
		for aggressiveMovePiece in aggressiveMovePieces:
			boardOperation = aggressiveMovePiece[0]
			row = aggressiveMovePiece[1]
			column = aggressiveMovePiece[2]
			if ((row + rowOperation) >= 0) and ((row + rowOperation) <= 3) and ((column + columnOperation) >= 0) and ((column + columnOperation) <= 3):
				newStatus = self.generateAggressiveMove(status, boardOperation, row, column, rowOperation, columnOperation)
				if newStatus != None:
					posibleAggressiveMoves.append(newStatus)					
		return posibleAggressiveMoves

	#busca las fichas con las cuales se puede hacer un movimiento agresivo
	def findAggressiveMovePieces(self, status, boardOperation):
		posibleboards = []
		if ((boardOperation == 0) or (boardOperation == 2)):
			posibleboards = [1, 3]
		else:
			posibleboards = [0, 2]
		aggressiveMovePieces = []
		for boardOperation in posibleboards:
			for row in range(4):
				for column in range(4):
					if status[boardOperation][row][column] == self.player: 
						aggressiveMovePieces.append((boardOperation,row,column))
		return aggressiveMovePieces

	#crea el movimiento agresivo posible a partir de operaciones dadas
	#si las operaciones dadas no tienen un movimiento agresivo posible
	#entonces retorna 'None'
	def generateAggressiveMove(self, status, board, row, column, rowOperation, columnOperation):
		status = self.copyStatus(status)
		if abs(rowOperation) == 1 or abs(columnOperation) == 1: #cuando la casilla se mueve 1 bloque unicamente
			tarjetValue = status[board][row + rowOperation][column + columnOperation]
			if tarjetValue == 0: #si la casilla a la que se mueve esta vacia
				status[board][row][column] = 0
				status[board][row+rowOperation][column+columnOperation] = self.player
				return status #Se puede mover
			elif tarjetValue != self.player: # si la casilla esta ocupada por ficha del oponente
				
				nextRow = row + 2 * rowOperation
				nextColumn = column + 2 * columnOperation
				if nextRow >= 0 and nextRow <= 3 and nextColumn >= 0 and nextColumn <= 3: #validacion de la posicion siguiente

					if status[board][nextRow][nextColumn] == 0: #Move
						status[board][row][column] = 0 
						status[board][row+rowOperation][column+columnOperation] = self.player
						status[board][nextRow][nextColumn] = self.getOpossitePlayer(self.player)
						return status
					else: #Movimiento no valido
						return None 
				else: # caso de que la posicion siguiente este por fuera del tablero
					#saca ficha
					status[board][row][column] = 0
					status[board][row+rowOperation][column+columnOperation] = self.player
					return status #Se puede mover
				 
			else: #si la casilla esta ocupada por ficha del mismo jugador				
				return None #movimiento no valido

		else: # condiciones para jugadas de 2 bloques
			tarjetValue = status[board][row + rowOperation][column + columnOperation]
			if tarjetValue == 0: #si la casilla a la que se mueve esta vacia

				previousRow = row + rowOperation + int(rowOperation/(-2))
				previousColumn = column + columnOperation + int(columnOperation/(-2))			
				if status[board][previousRow][previousColumn] == 0: # la anterior tambien esta vacia
					status[board][row][column] = 0
					status[board][row+rowOperation][column+columnOperation] = self.player
					return status #Se puede mover
				elif status[board][previousRow][previousColumn] == self.player:
					return None
				else:
					#print(row, column, rowOperation, columnOperation)
					nextRow = row + rowOperation + int(rowOperation/(2))
					nextColumn = column + columnOperation +int(columnOperation/(2))
					if nextRow >= 0 and nextRow <= 3 and nextColumn >= 0 and nextColumn <= 3:
						if status[board][nextRow][nextColumn] == 0:
							status[board][row][column] = 0 
							status[board][row+rowOperation][column+columnOperation] = self.player
							status[board][previousRow][previousColumn] = 0
							status[board][nextRow][nextColumn] = self.getOpossitePlayer(self.player)
							return status
						else:
							return None
					else: #saca la ficha
						status[board][previousRow][previousColumn] = 0
						status[board][row][column] = 0
						status[board][row+rowOperation][column+columnOperation] = self.player
						return status #Se puede mover

			elif tarjetValue != self.player: # si la casilla esta ocupada por ficha del oponente
				previousRow = row + rowOperation + int(rowOperation/(-2))
				previousColumn = column + columnOperation + int(columnOperation/(-2))
				if status[board][previousRow][previousColumn] == 0:
					nextRow = row + rowOperation + int(rowOperation/(2))
					nextColumn = column + columnOperation + int(columnOperation/(2))
					#validar que sean posiciones posibles
					if nextRow >= 0 and nextRow <= 3 and nextColumn >= 0 and nextColumn <= 3:
						if status[board][nextRow][nextColumn] == 0:
							status[board][row][column] = 0 
							status[board][row+rowOperation][column+columnOperation] = self.player
							status[board][nextRow][nextColumn] = self.getOpossitePlayer(self.player)
							return status
						else:
							return None
					else:
						status[board][row][column] = 0 
						status[board][row+rowOperation][column+columnOperation] = self.player
						return status
				else:
					return None

			else: #si la casilla esta ocupada por ficha del mismo jugador
				return None #movimiento no valido

	#devuelve el jugador opuesto
	def getOpossitePlayer(self, currentPlayer):
		return currentPlayer % 2 + 1

	#Crea la copia de una matriz
	def copyStatus(self, status):
		newStaus = []
		for board in range(4):
			newboard = []
			for row in range(4):
				newRow = []
				for column in range(4):
					newRow.append(status[board][row][column])
				newboard.append(newRow)
			newStaus.append(newboard)
		return newStaus

	#se encarga de definir el jugador sobre el 
	#cual se generan los posibles estados en un nodo
	def setPlayer(self, player):
		self.player = player

	#Imprime un estado en la consola
	def printStatus(self, status):
		print(str(status[0][0]) + "\t" + str(status[1][0]) )
		print(str(status[0][1]) + "\t" + str(status[1][1]) )
		print(str(status[0][2]) + "\t" + str(status[1][2]) )
		print(str(status[0][3]) + "\t" + str(status[1][3]) )
		print("----------------------------")
		print(str(status[2][0]) + "\t" + str(status[3][0]) )
		print(str(status[2][1]) + "\t" + str(status[3][1]) )
		print(str(status[2][2]) + "\t" + str(status[3][2]) )
		print(str(status[2][3]) + "\t" + str(status[3][3]) )
		print("____________________________\n" )

'''
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
			[2,2,2,0],
			[0,0,0,1],
			[0,0,0,2],
			[1,1,1,0],
		], [
			[2,2,2,2],
			[0,0,0,0],
			[0,0,0,0],
			[1,1,1,1],
		] ]
generador = Generator()
generador.setPlayer(1)
#moves = generador.findPassiveMoves(inicial)[0]
moves = generador.findAggressiveMoves(inicial, 3, 2, 0)
for status in moves:
	generador.printStatus(status)
'''