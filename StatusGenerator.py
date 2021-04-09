
class generator:

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

	def generateStatuses(self, initialStatus, player):
		self.initialStatus = initialStatus
		self.player = player
		self.homeboardPieces = []
		#validar fin del juego
		self.findHomeboardPieces()
		self.findPasiveMoves()
		#self.findAggressiveMoves()

	#Se encarga de buscar las fichas del homeboard del jugador en turno,
	#para posteriormente hacer las posibles combinaciones sobre estas.
	def findHomeboardPieces(self):
		homeboards = []
		if self.player == 1:
			homeboards = [2, 3]
		else:
			homeboards = [0, 1]
		for board in homeboards:
			for row in range(4):
				for column in range(4):
					if self.initialStatus[board][row][column] == self.player: 
						self.homeboardPieces.append((board,row,column))

	def findPasiveMoves(self):
		statuses = []

		for homeboardPiece in self.homeboardPieces:
			board = homeboardPiece[0]
			row = homeboardPiece[1]
			column = homeboardPiece[2]

			for move in self.moves:			
				rowOperation = move[0] #representa el movimiento que se hara en las filas
				columnOperation = move[1] #representa el moviento en las columnas
				if ( (row + rowOperation) >= 0) and ( (row + rowOperation) <= 3) and ( (column + columnOperation) >= 0) and ( (column + columnOperation) <= 3): #arriba
					if self.isValidPassiveMove(self.initialStatus, board, row, column, rowOperation, columnOperation):
						statusCopy = self.copyStatus(self.initialStatus)					
						statusCopy[board][ row ][ column ] = 0
						statusCopy[board][ row + rowOperation ][ column + columnOperation ] = self.player
						posibleAggressiveMoves = self.findAggressiveMoves(statusCopy, board, rowOperation, columnOperation)
						if len(posibleAggressiveMoves) != 0:
							for posibleAggressiveMove in posibleAggressiveMoves:
								statuses.append(posibleAggressiveMove)

		for status in statuses:
			self.printStatus(status)
		#self.printStatus(statuses[0])
					#validar movimiento agresivos

	#Valida si un movimiento pasivo es valido, tenindo en cuenta que este debe hacerse a una posicion no ocupada
	#o en la cual, su trayecto no se vea obstaculizada por otra ficha
	def isValidPassiveMove(self, status, board, row, column, rowOperation, columnOperation):
		if abs(rowOperation) or abs(columnOperation) == 1:
			return status[board][row + rowOperation][column + columnOperation] == 0
		else:
			rowMultiplier = int(rowOperation / -2)
			columnMultiplier = int(columnOperation / -2)
			if status[board][row + (rowOperation + 1 * rowMultiplier)][column + (columnOperation + 1*columnMultiplier)] == 0:
				if status[board][row + (rowOperation + 0 * rowMultiplier)][column + (columnOperation + 0*columnMultiplier)] == 0:
					return True
			else:
				return False


	def findAggressiveMoves(self, statusCopy, board, rowOperation, columnOperation):
		posibleAggressiveMoves = [] #estados
		posibleboards = []
		if ((board == 0) or (board == 2)):
			posibleboards = [1, 3]
		else:
			posibleboards = [0, 2]
		self.aggressiveMovePieces = []
		self.findAggressiveMovePieces(posibleboards)		
		for aggressiveMovePiece in self.aggressiveMovePieces:
			board = aggressiveMovePiece[0]
			row = aggressiveMovePiece[1]
			column = aggressiveMovePiece[2]

			if ((row + rowOperation) >= 0) and ((row + rowOperation) <= 3) and ((column + columnOperation) >= 0) and ((column + columnOperation) <= 3):

				newStatus = self.generateAggressiveMove(statusCopy, board, row, column, rowOperation, columnOperation)
				if newStatus != None:
					posibleAggressiveMoves.append(newStatus)
				#validar/crear movimiento agresivos
				'''
				if self.initialStatus[board][row + rowOperation][column + columnOperation] == 0:
					statusCopy2 = self.copyStatus(statusCopy)
					statusCopy2[board][row][column] = 0
					statusCopy2[board][row+rowOperation][column+columnOperation] = self.player
					posibleAggressiveMoves.append(statusCopy2)'''

					
		return posibleAggressiveMoves

	#busca las fichas con las cuales se puede hacer un movimiento agresivo para
	#entonces realizar las posibles combinaciones
	def findAggressiveMovePieces(self, posibleboards):
		for board in posibleboards:
			for row in range(4):
				for column in range(4):
					if self.initialStatus[board][row][column] == self.player: 
						self.aggressiveMovePieces.append((board,row,column))

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
				else:
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

			'''
			
			rowMultiplier = int(rowOperation / -2)
			columnMultiplier = int(columnOperation / -2)
			if status[board][row + (rowOperation + 1 * rowMultiplier)][column + (columnOperation + 1*columnMultiplier)] == 0:
				if status[board][row + (rowOperation + 0 * rowMultiplier)][column + (columnOperation + 0*columnMultiplier)] == 0:
					return True
			else:
				return False'''



	def getOpossitePlayer(self, currentPlayer):
		if currentPlayer == 1:
			return 2
		else:
			return 1

	#creates a matrix copy for the status
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

		#print(self.homeboardPieces)

inicial =  [
		[
			[0,2,2,2],
			[0,0,0,0],
			[0,0,0,0],
			[1,1,1,1],
		], [
			[2,2,2,2],
			[0,0,0,0],
			[1,0,0,0],
			[0,1,1,1],
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
generador = generator()
generador.generateStatuses(inicial, 1)

