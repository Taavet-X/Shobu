import tkinter as tk
from PIL import ImageTk, Image #pip install pillow
import math
import threading

from MainViewController import MainViewController

class MainFrame:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Shobu")
        
        self.loadImages()
        self.status = None
        self.createGUI(self.root)
        self.root.eval('tk::PlaceWindow . center')            
        
    def loadImages(self):
    	self.board = Image.open("Images/Board.png")
    	self.board = ImageTk.PhotoImage(self.board)
    	self.images = []

    	for i in range(1, 65):
    		if i<10: 
    			strValue = "0" + str(i) 
    		else: 
    			strValue = str(i)
    		img = Image.open("Images/Whites/00" + strValue + ".png")
    		img = ImageTk.PhotoImage(img)
    		self.images.append(img)
    	for i in range(1, 65):
    		if i<10: 
    			strValue = "0" + str(i) 
    		else: 
    			strValue = str(i)
    		img = Image.open("Images/Blacks/00" + strValue + ".png")
    		img = ImageTk.PhotoImage(img)
    		self.images.append(img)

    		
    def getImage(self, color, z, y, x):
    	index = x + 8*y + z % 2 * 4 + 32 * math.floor(z / 2)
    	if color == 2:
    		index += 64  
    	return self.images[index]

    def createGUI(self, root):
        frmMainContainer = tk.Frame(root)             
        frmMainContainer.pack(expand=True, fill=tk.BOTH)        
        self.createCanvas(frmMainContainer)

    def createCanvas(self, parent):
        canvasWidth = 960
        canvasHeight = 540
        self.canvas = tk.Canvas(parent, width = canvasWidth, height = canvasHeight)
        self.canvasItems = [[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
        self.canvas.create_image(480, 270, image=self.board)
        self.canvas.pack()
        self.controller = MainViewController(self)
        self.canvas.bind('<Motion>', self.controller.mouse_move)
        self.canvas.bind('<Button>', self.controller.mouse_click)

    def paintPiece(self, value, table, row, column):
    	self.canvasItems[table][row][column] = self.canvas.create_image(480, 270, image=self.getImage(value, table, row, column))

    def removePiece(self, table, row, column):
    	self.canvas.delete(self.canvasItems[table][row][column])
   
    #def paint(self):

    	'''
    	self.canvas.delete("all")
    	self.canvas.create_image(480, 270, image=self.board)   	
    	for tableIndex in range(4):
    		for rowIndex in range(4):
    			for columnIndex in range(4):
    				if self.status != None:
    					value = self.status.getTableValue(tableIndex, rowIndex, columnIndex)
    					if value != 0:
    						self.canvas.create_image(480, 270, image=self.getImage(value, tableIndex, rowIndex, columnIndex))
    	if self.controller.selected:
    		self.oldBlock = self.controller.oldBlock
    		self.selectedValue = self.controller.selectedValue
    		if (self.oldBlock != (-1,-1,-1)):
    			self.canvas.create_image(480, 270, image=self.getImage(self.selectedValue, self.oldBlock[0], self.oldBlock[1], self.oldBlock[2]))
    	'''





frame = MainFrame()
frame.root.mainloop()
