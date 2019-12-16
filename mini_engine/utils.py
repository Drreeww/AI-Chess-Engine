import chess

UNICODE_PIECE_SYMBOLS = {
        "R": u"♖", "r": u"♜",
        "N": u"♘", "n": u"♞",
        "B": u"♗", "b": u"♝",
        "Q": u"♕", "q": u"♛",
        "K": u"♔", "k": u"♚",
        "P": u"♙", "p": u"♟",
    }

pawnstable = [
 0,  0,  0,  0,  0,  0,  0,  0,
 5, 10, 10,-20,-20, 10, 10,  5,
 5, -5,-10,  0,  0,-10, -5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5,  5, 10, 25, 25, 10,  5,  5,
10, 10, 20, 30, 30, 20, 10, 10,
50, 50, 50, 50, 50, 50, 50, 50,
 0,  0,  0,  0,  0,  0,  0,  0]

knightstable = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  5,  5,  0,-20,-40,
-30,  5, 10, 15, 15, 10,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 10, 15, 15, 10,  0,-30,
-40,-20,  0,  0,  0,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50]

bishopstable = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  5,  0,  0,  0,  0,  5,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10,-10,-10,-10,-10,-20]

rookstable = [
  0,  0,  0,  5,  5,  0,  0,  0,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  5, 10, 10, 10, 10, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]

queenstable = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  5,  5,  5,  5,  5,  0,-10,
  0,  0,  5,  5,  5,  5,  0, -5,
 -5,  0,  5,  5,  5,  5,  0, -5,
-10,  0,  5,  5,  5,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20]

kingstable = [
 20, 30, 10,  0,  0, 10, 30, 20,
 20, 20,  0,  0,  0,  0, 20, 20,
-10,-20,-20,-20,-20,-20,-20,-10,
-20,-30,-30,-40,-40,-30,-30,-20,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30]

def enumerate_moves(board, x, y):
    # Not A DRY function
    """
    A generator for generating valid moves with tag for each cell\n
    rtype:	((row, col), tag)\n
    tag:\n
        d : cell in Danger\n
        c : current cell / chosen cell\n
        p : path of the chosen piece\n
    
    """
    def genBishop(piece):
        if piece.islower():
            for i,j in iter([(x+i, y+i) for i in range(1,8) if 0<=x<8 and 0<=y<8]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].isupper():	yield ((i,j), "d");		break
                    elif board[i][j]==".":   yield ((i,j), "p")
                    else:	break
            for i,j in iter([(x+i, y-i) for i in range(1,8) if 0<=x<8 and 0<=y<8]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].isupper():	yield ((i,j), "d");		break
                    elif board[i][j]==".":   yield ((i,j), "p")
                    else:	break
            for i,j in iter([(x-i, y+i) for i in range(1,8) if 0<=x<8 and 0<=y<8]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].isupper():	yield ((i,j), "d");		break
                    elif board[i][j]==".":   yield ((i,j), "p")
                    else:	break
            for i,j in iter([(x-i, y-i) for i in range(1,8) if 0<=x<8 and 0<=y<8]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].isupper():	yield ((i,j), "d");		break
                    elif board[i][j]==".":   yield ((i,j), "p")
                    else:	break
        else:
            for i,j in iter([(x+i, y+i) for i in range(1,8) if 0<=x<8 and 0<=y<8]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].islower():	yield ((i,j), "d");		break
                    elif board[i][j]==".":   yield ((i,j), "p")
                    else:	break
            for i,j in iter([(x+i, y-i) for i in range(1,8) if 0<=x<8 and 0<=y<8]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].islower():	yield ((i,j), "d");		break
                    elif board[i][j]==".":   yield ((i,j), "p")
                    else:	break
            for i,j in iter([(x-i, y+i) for i in range(1,8) if 0<=x<8 and 0<=y<8]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].islower():	yield ((i,j), "d");		break
                    elif board[i][j]==".":   yield ((i,j), "p")
                    else:	break
            for i,j in iter([(x-i, y-i) for i in range(1,8) if 0<=x<8 and 0<=y<8]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].islower():	yield ((i,j), "d");		break
                    elif board[i][j]==".":   yield ((i,j), "p")
                    else:	break
    def genRook(piece):
        if piece.isupper():
            for i,j in iter([(x, y+i) for i in range(1,8) if 0<=x<8 and 0<=y<8]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].islower():	yield ((i,j), "d");		break
                    elif board[i][j]==".":   yield ((i,j), "p")
                    else:	break
            for i,j in iter([(x, y-i) for i in range(1,8) if 0<=x<8 and 0<=y<8]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].islower():	yield ((i,j), "d");		break
                    elif board[i][j]==".":   yield ((i,j), "p")
                    else:	break
            for i,j in iter([(x-i, y) for i in range(1,8) if 0<=x<8 and 0<=y<8]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].islower():	yield ((i,j), "d");		break
                    elif board[i][j]==".":   yield ((i,j), "p")
                    else:	break
            for i,j in iter([(x+i, y) for i in range(1,8) if 0<=x<8 and 0<=y<8]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].islower():	yield ((i,j), "d");		break
                    elif board[i][j]==".":   yield ((i,j), "p")
                    else:	break
        else:
            for i,j in iter([(x, y+i) for i in range(1,8) if 0<=x<8 and 0<=y<8]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].isupper():	yield ((i,j), "d");		break
                    elif board[i][j]==".":   yield ((i,j), "p")
                    else:	break
            for i,j in iter([(x, y-i) for i in range(1,8) if 0<=x<8 and 0<=y<8]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].isupper():	yield ((i,j), "d");		break
                    elif board[i][j]==".":   yield ((i,j), "p")
                    else:	break
            for i,j in iter([(x-i, y) for i in range(1,8) if 0<=x<8 and 0<=y<8]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].isupper():	yield ((i,j), "d");		break
                    elif board[i][j]==".":   yield ((i,j), "p")
                    else:	break
            for i,j in iter([(x+i, y) for i in range(1,8) if 0<=x<8 and 0<=y<8]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].isupper():	yield ((i,j), "d");		break
                    elif board[i][j]==".":   yield ((i,j), "p")
                    else:	break
    
# PAWN	------------------------------------------------------------------------------
    # resolve pawn moves. 4 possible moves maximally
    if board[x][y] == "P" or board[x][y] == "p":
        
        if board[x][y] == "p":   # black piece
            if board[x+1][y]==".":	yield ((x+1, y), "p")
            
            if x == 1 and board[x+1][y]==".":  # if the pawn is in the second rank (has not moved)
                if board[x+2][y]!=".":
                    if board[x+2][y].upper():  yield ((x+2, y), "d")
                else:   yield ((x+2, y), "p")
                
            if x < 7 and y < 7 and board[x+1][y+1].isupper():   yield ((x+1, y+1), "d")
            if x < 7 and 0 < y and board[x+1][y-1].isupper():   yield ((x+1, y-1), "d")

        else:   # white piece
            if board[x-1][y]==".":	yield ((x-1, y), "p")
            
            if x == 6 and board[x-1][y]==".":  # if the pawn is in the second rank (has not moved)
                if board[x-2][y]!=".":
                    if board[x-2][y].islower():  yield ((x-2, y), "d")
                else:   yield ((x-2, y), "p")

            if 0<=x and 0<=y<7 and board[x-1][y+1].islower():   yield ((x-1, y+1), "d")
            if 0<=x and 0<=y<8 and board[x-1][y-1].islower():   yield ((x-1, y-1), "d")
            
# KNIGHT	------------------------------------------------------------------------------
    # resolve knight moves. 8 possible moves maximally
    elif board[x][y] == "N" or board[x][y] == "n":
        if board[x][y] == "N":
            for i, j in iter([(x+2, y+1), (x+2, y-1)
                            ,(x+1, y+2), (x+1, y-2)
                            ,(x-2, y-1), (x-2, y+1)
                            ,(x-1, y+2), (x-1, y-2)]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].islower():   yield ((i,j), "d")
                    elif board[i][j]==".":   yield ((i,j), "p")
        
        if board[x][y] == "n":
            for i, j in iter([(x+2, y+1), (x+2, y-1)
                            ,(x+1, y+2), (x+1, y-2)
                            ,(x-2, y-1), (x-2, y+1)
                            ,(x-1, y+2), (x-1, y-2)]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].isupper():   yield ((i,j), "d")
                    elif board[i][j]==".":   yield ((i,j), "p")

# BISHOP	 ------------------------------------------------------------------------------
    elif board[x][y] == "B" or board[x][y] == "b":
        if board[x][y] == "B":
            for i in genBishop("B"):	yield i
        else:
            for i in genBishop("b"):	yield i

# ROOK	 ------------------------------------------------------------------------------
    elif board[x][y] == "R" or board[x][y] == "r":
        if board[x][y] == "R":
            for i in genRook("R"):	yield i
        else:
            for i in genRook("r"):	yield i

# Queen	------------------------------------------------------------------------------
    elif board[x][y] == "Q" or board[x][y] == "q":
        if board[x][y] == "Q":
            for i in genBishop("Q"):	yield i
            for i in genRook("Q"):	yield i
        else:
            for i in genBishop("q"):	yield i
            for i in genRook("q"):	yield i
  
# ------------------------------------------------------------------------------        
    elif board[x][y] == "K" or board[x][y] == "k":
        if board[x][y] == "k":
            for i,j in iter([(x+1, y),(x+1, y+1),(x, y+1),(x-1, y+1),
                            (x-1, y),(x-1, y-1),(x, y-1),(x+1, y-1)]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].isupper():	yield ((i,j), "d")
                    elif board[i][j]==".":   yield ((i,j), "p")
        else:
            for i,j in iter([(x+1, y),(x+1, y+1),(x, y+1),(x-1, y+1),
                            (x-1, y),(x-1, y-1),(x, y-1),(x+1, y-1)]):
                if 0<=i<8 and 0<=j<8:
                    if board[i][j].islower():	yield ((i,j), "d")
                    elif board[i][j]==".":   yield ((i,j), "p")

# ------------------------------------------------------------------------------