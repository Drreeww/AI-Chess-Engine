from mini_engine.aiEngine import *
from mini_engine.utils import *
from gui.chessGUI import *

import chess
import chess.pgn
import datetime, time
import chess.engine
import random

class MainChess():
	# ToDo: last move Done by opposite player
	
	def __init__(self, player2="You", player1="AI", board=None):
		"""
			player1: White Pieces\n
			Player2: Black Pieces\n
			board:	Predefined board
		"""
		if board:   self.chessBoard = Chess(board)
		else:       self.chessBoard = Chess()
		self.game = chess.pgn.Game()
		self.game.headers["Event"] =	"Example"
		self.game.headers["Site"]  =	"Laptop"
		self.game.headers["Date"]  =	str(datetime.datetime.now().date())
		self.game.headers["Round"] =	1
		self.game.headers["White"] =	player1
		self.game.headers["Black"] =	player2
		self.chessBoard.printBoard()
		self.gui = ChessGUI_pygame()
		self.engine = 	chess.engine.SimpleEngine.popen_uci("E:\\dtu\\7thsem\\project\\stockfish-10-win\\Windows\\stockfish.exe")
		self.limit =	chess.engine.Limit(time=2)

	def boardToList(self):
		"returns board as list"
		return str(self.chessBoard.board).replace(" ", "").split('\n')

	def getValidSquare(self, board, row, col):
		validSquares = set()
		if board[row][col].isupper():
			validSquares.add(((row, col), 'c'))
		for coord in enumerate_moves(board, row, col):
			if 0<=coord[0][0]<8 and 0<=coord[0][1]<8:
				validSquares.add(coord)
		return validSquares
		
	def rowColToUCI(self, move):
		return f"{chr(ord('a')+int(move[1]))}{8-move[0]}{chr(ord('a')+int(move[3]))}{8-move[2]}"

	def getPlayerInput(self, row, col, validSquares, player="You"):
		while 1:
			for e in pygame.event.get():
				if e.type is QUIT or (e.type is KEYDOWN and e.key is K_ESCAPE):
					pygame.quit();	return
				if e.type is MOUSEBUTTONDOWN:
					mouseX, mouseY = pygame.mouse.get_pos()
					row2, col2 = self.gui.GetClickedSquare(mouseX,mouseY)
					if 0 <= col2 < 8 and 0 <= row2 < 8:
						if ((row2,col2),"p") in validSquares or ((row2,col2),"d") in validSquares:
							inp = self.rowColToUCI((row,col,row2,col2))
							move = chess.Move.from_uci(inp)
							if not self.chessBoard.board.is_into_check(move):
								self.gui.PrintMessage(f"{player}: {inp}")
								self.chessBoard.board.push(move)
								self.chessBoard.movesHistory.append(move)
							return
						return
	def initialise(self, depth):
		t = random.uniform(1, 5*depth)
		return chess.engine.Limit(time=t)

	def testRoutine(self):
		self.gui.Draw(self.boardToList())
		while 1:
			for e in pygame.event.get():
				if e.type is QUIT or (e.type is KEYDOWN and e.key is K_ESCAPE):
					pygame.quit()
					return
				if e.type is MOUSEBUTTONDOWN:
					row, col = self.gui.GetClickedSquare(*pygame.mouse.get_pos())
					if 0 <= col < 8 and 0 <= row < 8:
						board = self.boardToList()
						if board[row][col].isupper():	# Only when it's the white player
							validSquares = self.getValidSquare(board, row, col)
							self.gui.Draw(board, validSquares)
							self.getPlayerInput(row, col, validSquares)
							self.gui.Draw(self.boardToList())	# update board
						else:	self.gui.Draw(board)
	
	def isCheck(self):
		"Returns if the current side to move is in check."
		return self.chessBoard.board.is_check()
	
	def isKingAttacked(self):
		"""
  		checks the position of kings and if they are being
		attacked and returns highlighted square
	 	"""
		t = set()
		for i, row in enumerate(self.boardToList()):
			for j, p in enumerate(row):
				if self.chessBoard.board.turn and p=="K":
					square = f"chess.{(chr(ord('a')+j)).upper()}{8-i}"
					if self.chessBoard.board.is_attacked_by(chess.BLACK, eval(square)):
						t.add(((i,j),"d"))
				
				if not self.chessBoard.board.turn and p=="k":
					square = f"chess.{(chr(ord('a')+j)).upper()}{8-i}"
					if self.chessBoard.board.is_attacked_by(chess.WHITE, eval(square)):
						t.add(((i,j),"d"))
		return t
	
	def savePGN(self, sleepFor=5):
		# print("Wait for 60 seconds")
		self.game.add_line(self.chessBoard.movesHistory)
		self.game.headers["Result"] = str(self.chessBoard.board.result(claim_draw=True))
		print(self.game)
		print(self.game, file=open("test.pgn", "w"), end="\n\n")
		time.sleep(60)
		return

	def undo(self):
		if len(self.chessBoard.movesHistory)>1:
			time.sleep(1)
			self.chessBoard.movesHistory.pop();	self.chessBoard.movesHistory.pop()
			self.chessBoard.undoMoves.append(self.chessBoard.board.pop())
			self.chessBoard.undoMoves.append(self.chessBoard.board.pop())
			self.gui.PrintMessage("UnDo")
		return
	
	def redo(self):
		if self.chessBoard.undoMoves:
			time.sleep(1)
			self.chessBoard.movesHistory.append(self.chessBoard.undoMoves.pop())
			self.chessBoard.movesHistory.append(self.chessBoard.undoMoves.pop())
			self.chessBoard.board.push(self.chessBoard.movesHistory[-2])
			self.chessBoard.board.push(self.chessBoard.movesHistory[-1])
			self.gui.PrintMessage("ReDo")
		return

	def _twoPlayer(self):
		"Manual Two player game"
		self.gui.Draw(self.boardToList())
		while 1:
			for e in pygame.event.get():
				if e.type is QUIT:	pygame.quit(); return
				if e.type == pygame.KEYDOWN:
					if e.key == pygame.K_LEFT:		self.undo()
					if e.key == pygame.K_RIGHT:		self.redo()
					if e.key == pygame.K_ESCAPE:	pygame.quit(); return

				if e.type is MOUSEBUTTONDOWN:
					row, col = self.gui.GetClickedSquare(*pygame.mouse.get_pos())
					if 0 <= col < 8 and 0 <= row < 8:
						board = self.boardToList()
						if board[row][col].isupper() and self.chessBoard.board.turn:
							# Only when it's the white player
							validSquares = self.getValidSquare(board, row, col)
							self.gui.Draw(board, validSquares)
							self.getPlayerInput(row, col, validSquares, "White")
							self.gui.Draw(self.boardToList())	# update board
						elif board[row][col].islower() and not self.chessBoard.board.turn:
							# Only when it's the black player
							validSquares = self.getValidSquare(board, row, col)
							self.gui.Draw(board, validSquares)
							self.getPlayerInput(row, col, validSquares, "Black")
							self.gui.Draw(self.boardToList())	# update board
						else:	self.gui.Draw(board)
		# self.engine.quit()
		pygame.quit()
		return

	def _singlePlayer(self, depth=3):
		
		self.gui.Draw(self.boardToList(), self.isKingAttacked())

		while not self.chessBoard.board.is_game_over(claim_draw=True):
			t = self.isKingAttacked()
			self.gui.Draw(self.boardToList(), t)
			
			if self.chessBoard.board.turn:
				for e in pygame.event.get():
					if e.type is QUIT:	self.engine.quit(); pygame.quit(); return
					if e.type == pygame.KEYDOWN:
						if e.key == pygame.K_LEFT:		self.undo()
						if e.key == pygame.K_RIGHT:		self.redo()
						if e.key == pygame.K_ESCAPE:	engine.quit(); pygame.quit(); return

					if e.type is MOUSEBUTTONDOWN:
						row, col = self.gui.GetClickedSquare(*pygame.mouse.get_pos())
						if 0 <= col < 8 and 0 <= row < 8:
							board = self.boardToList()
							if board[row][col].isupper() and self.chessBoard.board.turn:
								# Only when it's the white player
								validSquares = self.getValidSquare(board, row, col).union(t)
								self.gui.Draw(board, validSquares)
								self.getPlayerInput(row, col, validSquares, "White")
								self.gui.Draw(self.boardToList(), t)	# update board
							else:	self.gui.Draw(board, t)
			else:
				move = self.engine.play(self.chessBoard.board, limit=self.initialise(depth))
				self.chessBoard.board.push(move.move)
				self.chessBoard.movesHistory.append(move.move)
				self.gui.PrintMessage(f"AI: {str(move.move)}")
				self.gui.Draw(self.boardToList(), t)
		
		self.savePGN()
		self.engine.quit()
		pygame.quit()
		return

	def hackMode(self, timelimit=5, firstPlayer=1):
		if firstPlayer!=1:	self.chessBoard.board.turn = 0
		engine =	chess.engine.SimpleEngine.popen_uci("E:\\dtu\\7thsem\\project\\stockfish-10-win\\Windows\\stockfish.exe")
		limit =		chess.engine.Limit(time=timelimit)
		self.gui.Draw(self.boardToList(), self.isKingAttacked())

		while not self.chessBoard.board.is_game_over(claim_draw=True):
			t = self.isKingAttacked()
			self.gui.Draw(self.boardToList(), t)
			
			if not self.chessBoard.board.turn:
				for e in pygame.event.get():
					if e.type is QUIT:	engine.quit(); pygame.quit(); return
					if e.type == pygame.KEYDOWN:
						if e.key == pygame.K_LEFT:		self.undo()
						if e.key == pygame.K_RIGHT:		self.redo()
						if e.key == pygame.K_ESCAPE:	engine.quit(); pygame.quit(); return

					if e.type is MOUSEBUTTONDOWN:
						row, col = self.gui.GetClickedSquare(*pygame.mouse.get_pos())
						if 0 <= col < 8 and 0 <= row < 8:
							board = self.boardToList()
							if board[row][col].islower():
								# Only when it's the white player
								validSquares = self.getValidSquare(board, row, col).union(t)
								self.gui.Draw(board, validSquares)
								self.getPlayerInput(row, col, validSquares, "White")
								self.gui.Draw(self.boardToList(), t)	# update board
							else:	self.gui.Draw(board, t)
			else:
				move = engine.play(self.chessBoard.board, limit=limit)
				self.chessBoard.board.push(move.move)
				self.chessBoard.movesHistory.append(move.move)
				self.gui.PrintMessage(f"AI: {str(move.move)}")
				self.gui.Draw(self.boardToList(), t)
		
		self.savePGN()
		engine.quit()
		pygame.quit()
		return

if __name__ == "__main__":
	
	b=MainChess()
	b._singlePlayer(depth=2)
	# b._twoPlayer()
	
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
	# b=MainChess(board="r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")
	# b=MainChess(board='r2q3r/pp3k2/2p1n1pp/4Pp2/4pNnP/1QN1P3/PP3PP1/R3K2R b KQ - 4 17')
	# b=MainChess(board="2k5/p5p1/2pp4/5rb1/6b1/8/Pr4PP/4K2R w - - 1 32")
	# b.hackMode(timelimit=0.2, firstPlayer=1)
	# b.testRoutine()

	# c = chess.Board("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")
	# print(c.is_check())