import tkinter as tk
from PIL import ImageTk, Image #pip install pillow
import math
import threading
import time
from MainViewController import MainViewController

class MainFrame:
    
    def __init__(self):
        print("loading...")
        self.root = tk.Tk()
        self.root.title("Shobu")
        self.turn = None
        self.textImage = None
        self.loadImages()
        self.status = None
        self.createGUI(self.root)
        self.root.eval('tk::PlaceWindow . center')            
        
    def loadImages(self):
        self.board = Image.open("Images/Board.png")
        self.board = ImageTk.PhotoImage(self.board)
        self.images = []

        self.imgAgroB = Image.open("Images/Messages/agro-black.png")
        self.imgAgroB = ImageTk.PhotoImage(self.imgAgroB)

        self.imgAgroW = Image.open("Images/Messages/agro-white.png")
        self.imgAgroW = ImageTk.PhotoImage(self.imgAgroW)

        self.imgPasiveB = Image.open("Images/Messages/pasive-black.png")
        self.imgPasiveB = ImageTk.PhotoImage(self.imgPasiveB)

        self.imgPasiveW = Image.open("Images/Messages/pasive-white.png")
        self.imgPasiveW = ImageTk.PhotoImage(self.imgPasiveW)

        self.imgWinB = Image.open("Images/Messages/win-black.png")
        self.imgWinB = ImageTk.PhotoImage(self.imgWinB)

        self.imgWinW = Image.open("Images/Messages/win-white.png")
        self.imgWinW = ImageTk.PhotoImage(self.imgWinW)

        self.imgInvPlay = Image.open("Images/Messages/invalid-play.png")
        self.imgInvPlay = ImageTk.PhotoImage(self.imgInvPlay)

        self.imgNoHome = Image.open("Images/Messages/Nohome.png")
        self.imgNoHome = ImageTk.PhotoImage(self.imgNoHome)

        self.imgNoToken = Image.open("Images/Messages/no-token.png")
        self.imgNoToken = ImageTk.PhotoImage(self.imgNoToken)

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

    def paintMessage(self, mensaje):
        if mensaje == "invalid":
            self.message = self.imgInvPlay 
            x = threading.Thread(target=self.messageThread)
            x.start()
        elif mensaje == "noToken":
            self.message = self.imgNoToken
            x = threading.Thread(target=self.messageThread)
            x.start()
        elif mensaje == "noHome":
            self.message = self.imgNoHome
            x = threading.Thread(target=self.messageThread)
            x.start()
        elif mensaje == "WinB":
            self.paintWin(self.imgWinB)
        elif mensaje == "WinW":
            self.paintWin(self.imgWinW)
        elif mensaje == "agroB":
            self.paintTurn(self.imgAgroB)
        elif mensaje == "passiveB":
            self.paintTurn(self.imgPasiveB)
        elif mensaje == "agroW":
            self.paintTurn(self.imgAgroW)
        elif mensaje == "passiveW":
            self.paintTurn(self.imgPasiveW)

    def paintTurn(self, img):
        if self.turn != None:
            self.canvas.delete(self.turn)
        self.turn = self.canvas.create_image(480, 270, image=img)

    def paintWin(self, img):
        self.canvas.create_image(480, 270, image=img)

    def messageThread(self):
        img = self.canvas.create_image(480, 270, image=self.message)
        time.sleep(2)
        self.canvas.delete(img)

    def paintText(self, text):
        self.text = text
        x = threading.Thread(target=self.textThread)
        x.start()
        

    def textThread(self):
        if self.textImage != None:
            self.canvas.delete(self.textImage)
            self.textImage = None
        self.textImage = self.canvas.create_text(480,500, fill = "white", font="Times 20 italic bold", text = self.text)
        time.sleep(3)
        if self.textImage != None:
            self.canvas.delete(self.textImage)
            self.textImage = None


frame = MainFrame()
frame.root.mainloop()