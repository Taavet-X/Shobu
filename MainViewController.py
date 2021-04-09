from Status import Status

class MainViewController:

	def __init__(self, mainView):
		self.mainView = mainView
		self.createBlocks()
		self.selectedBlock = None		
		self.currentBlock = (-1,-1,-1)		
		self.setStatus(Status( [
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
		]))

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

	def	mouse_move(self, event):		
		for block in self.blocks:
			if(event.x >= block[0] and event.x <= block[2] and event.y >= block[1] and event.y <= block[3]):
				if block[4] != self.currentBlock:
					self.currentBlock = block[4]
					self.mainView.canvas['cursor']="hand2"
					#if self.selected:
					#	if self.currentBlock != (-1,-1,-1):
							#self.mainView.paintPiece(self.selectedValue, self.currentBlock[0], self.currentBlock[1], self.currentBlock[2])
					#self.mainView.paint()
				return
		self.currentBlock = (-1,-1,-1)
		self.mainView.canvas['cursor']="arrow"		
		return

	def mouse_click(self, event):
		if self.selectedBlock != None:
			if self.currentBlock == (-1,-1,-1):
				self.selectedBlock == None							
			else:
				if self.selectedBlock == self.currentBlock:
					print("canceled move")
				#move
				self.currentValue = self.status.getTableValue(self.currentBlock[0], self.currentBlock[1], self.currentBlock[2])
				if self.currentValue != 0:
					self.mainView.removePiece(self.currentBlock[0], self.currentBlock[1], self.currentBlock[2])
				self.status.setTableValue(self.currentBlock[0], self.currentBlock[1], self.currentBlock[2], self.selectedValue)
				self.mainView.paintPiece(self.selectedValue, self.currentBlock[0], self.currentBlock[1], self.currentBlock[2])
				self.selectedBlock = None
		else:
			if self.currentBlock != (-1,-1,-1):
				self.selectedValue = self.status.getTableValue(self.currentBlock[0], self.currentBlock[1], self.currentBlock[2])
				if self.selectedValue != 0:
					self.status.setTableValue(self.currentBlock[0], self.currentBlock[1], self.currentBlock[2], 0)
					self.mainView.removePiece(self.currentBlock[0], self.currentBlock[1], self.currentBlock[2])
					self.selectedBlock = self.currentBlock
			
					

		'''
		if self.currentBlock != (-1,-1,-1):
			if self.selected == False:
				self.selectedValue = self.status.getTableValue(self.currentBlock[0], self.currentBlock[1], self.currentBlock[2])
				if self.selectedValue != 0:
					self.status.setTableValue(self.currentBlock[0], self.currentBlock[1], self.currentBlock[2], 0)
					self.mainView.removePiece(self.currentBlock[0], self.currentBlock[1], self.currentBlock[2])
					self.selected = True
			else:
				self.targetValue = self.status.getTableValue(self.currentBlock[0], self.currentBlock[1], self.currentBlock[2])
				if self.selectedValue != self.targetValue: #en caso de que NO se seleccione otra ficha del mismo color como target
					self.selected = False
					self.mainView.paintPiece(self.selectedValue, self.currentBlock[0], self.currentBlock[1], self.currentBlock[2])
						
		#print(self.currentBlock)
		'''
	def setStatus(self, status):
		print("status set")
		self.status = status
		for tableIndex in range(4):
			for rowIndex in range(4):
				for columnIndex in range(4):
					value = self.status.getTableValue(tableIndex, rowIndex, columnIndex)
					if value != 0:
						self.mainView.paintPiece(value, tableIndex, rowIndex, columnIndex)
		

