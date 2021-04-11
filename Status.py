class Status:

	def __init__(self, table0, table1, table2, table3):
		self.table0 = table0
		self.table1 = table1
		self.table2 = table2
		self.table3 = table3
		self.tables = [table0, table1, table2, table3]

	def getTables(self):
		return self.tables

	def getTableValue(self, table, row, column):
		return self.tables[table][row][column]

	def setTableValue(self, table, row, column, value):
		self.tables[table][row][column] = value
