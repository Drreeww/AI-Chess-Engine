import sys
sys.path.append("gui\\")
from ScrollingTextBox import ScrollingTextBox
import pygame
from pygame.locals import *

import os
current_path = os.path.dirname(__file__)+"\\images\\" # Where your .py file is located

class ChessGUI_pygame:
	def __init__(self):
		# self.Rules = ChessRules()
		pygame.init()
		pygame.display.init()
		self.screen = pygame.display.set_mode((800,500))
		self.boardStart_x = 50
		self.boardStart_y = 50
		pygame.display.set_caption('Python Chess')
		gameIcon = pygame.image.load(current_path+'\\'+'pawn.jpg')
		pygame.display.set_icon(gameIcon)
		self.textBox = ScrollingTextBox(self.screen,475,800,50,450)
		self.LoadImages()

	def LoadImages(self):
		self.white_square =	pygame.image.load(current_path+'\\'+'white_square.png')
		self.brown_square = pygame.image.load(current_path+'\\'+"brown_square.png")
		self.cyan_square  =	pygame.image.load(current_path+'\\'+"cyan_square.png")
		self.green_square = pygame.image.load(current_path+'\\'+"green.png")
		self.red_square   =	pygame.image.load(current_path+'\\'+"red.png")
		self.black_pawn   =	pygame.image.load(current_path+'\\'+"bPawn.png")
		self.black_rook   =	pygame.image.load(current_path+'\\'+"bRook.png")
		self.black_knight = pygame.image.load(current_path+'\\'+"bKnight.png")
		self.black_bishop = pygame.image.load(current_path+'\\'+"bBishop.png")
		self.black_king   =	pygame.image.load(current_path+'\\'+"bKing.png")
		self.black_queen  =	pygame.image.load(current_path+'\\'+"bQueen.png")
		self.white_pawn   =	pygame.image.load(current_path+'\\'+"wPawn.png")
		self.white_rook   =	pygame.image.load(current_path+'\\'+"wRook.png")
		self.white_knight = pygame.image.load(current_path+'\\'+"wKnight.png")
		self.white_bishop = pygame.image.load(current_path+'\\'+"wBishop.png")
		self.white_king   =	pygame.image.load(current_path+'\\'+"wKing.png")
		self.white_queen  =	pygame.image.load(current_path+'\\'+"wQueen.png")
		self.square_size  =	50 #all images must be images 50 x 50 pixels

	def PrintMessage(self, message):
		#prints a string to the area to the right of the board
		self.textBox.Add(message)

	def ConvertToScreenCoords(self,chessSquareTuple):
		#converts a (row,col) chessSquare into the pixel location of the upper-left corner of the square
		(row,col) = chessSquareTuple
		screenX = self.boardStart_x + col*self.square_size
		screenY = self.boardStart_y + row*self.square_size
		return (screenX,screenY)
		
	def ConvertToChessCoords(self,screenPositionTuple):
		# converts a screen pixel location (X,Y) into a chessSquare tuple (row,col)
		#x is horizontal, y is vertical	(x=0,y=0) is upper-left corner of the screen
		X, Y = screenPositionTuple
		row = (Y-self.boardStart_y) // self.square_size
		col = (X-self.boardStart_x) // self.square_size
		return row,col
		
	def Draw(self,board,highlightSquares=[]):
		self.textBox.Draw()
		boardSize = len(board) #board should be square.
		# boardSize should be always 8 for chess, but I dislike "magic numbers" :)
		
		#draw blank board
		current_square = 0
		for r in range(boardSize):
			for c in range(boardSize):
				(screenX,screenY) = self.ConvertToScreenCoords((r,c))
				if current_square:
					self.screen.blit(self.brown_square,(screenX,screenY))
					current_square = (current_square+1)%2
				else:
					self.screen.blit(self.white_square,(screenX,screenY))
					current_square = (current_square+1)%2

			current_square = (current_square+1)%2

		#highlight squares if specified
		for square, c in highlightSquares:
			(screenX,screenY) = self.ConvertToScreenCoords(square)
			if c=="c":		self.screen.blit(self.green_square,(screenX,screenY))
			elif c=="p":	self.screen.blit(self.cyan_square,(screenX,screenY))
			elif c=="d":	self.screen.blit(self.red_square,(screenX,screenY))
		
		#draw pieces
		for r in range(boardSize):
			for c in range(boardSize):
				(screenX,screenY) = self.ConvertToScreenCoords((r,c))
				if board[r][c] == 'p':		self.screen.blit(self.black_pawn,(screenX,screenY))
				elif board[r][c] == 'r':	self.screen.blit(self.black_rook,(screenX,screenY))
				elif board[r][c] == 'n':	self.screen.blit(self.black_knight,(screenX,screenY))
				elif board[r][c] == 'b':	self.screen.blit(self.black_bishop,(screenX,screenY))
				elif board[r][c] == 'q':	self.screen.blit(self.black_queen,(screenX,screenY))
				elif board[r][c] == 'k':	self.screen.blit(self.black_king,(screenX,screenY))
				elif board[r][c] == 'P':	self.screen.blit(self.white_pawn,(screenX,screenY))
				elif board[r][c] == 'R':	self.screen.blit(self.white_rook,(screenX,screenY))
				elif board[r][c] == 'N':	self.screen.blit(self.white_knight,(screenX,screenY))
				elif board[r][c] == 'B':	self.screen.blit(self.white_bishop,(screenX,screenY))
				elif board[r][c] == 'Q':	self.screen.blit(self.white_queen,(screenX,screenY))
				elif board[r][c] == 'K':	self.screen.blit(self.white_king,(screenX,screenY))
		pygame.display.flip()

	def GetClickedSquare(self,mouseX,mouseY):
		return self.ConvertToChessCoords((mouseX,mouseY))

	def TestRoutine(self):
		#test function
		while 1:
			for e in pygame.event.get():
				if e.type is QUIT:
					return
				if e.type is KEYDOWN:
					if e.key is K_ESCAPE:
						pygame.quit()
						return
				if e.type is MOUSEBUTTONDOWN:
					(mouseX,mouseY) = pygame.mouse.get_pos()
					# x is horizontal, y is vertical
					# (x=0,y=0) is upper-left corner of the screen
					row, col = self.GetClickedSquare(mouseX,mouseY)

if __name__ == "__main__":
	#try out some development / testing stuff if this file is run directly

	import chess
	testBoard = chess.Board()
	testBoard = str(testBoard).replace(" ", "").split('\n')
	
	validSquares = [((0,0), "c"),
                 	((1,1), "p"),
                  	((2,2), "p"),
                  	((3,3), "p"),
                  	((4,4), "p"),
                  	((5,5), "p"),
                	((7,6), "d")]
	game = ChessGUI_pygame()
	
	game.Draw(testBoard, validSquares)
	
	# game.Draw(testBoard)
	# game.TestRoutine()
	