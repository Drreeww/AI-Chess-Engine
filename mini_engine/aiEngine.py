#%%
import chess
import chess.svg
import chess.polyglot

import sys
sys.path.append("mini_engine\\")
from utils import *
from itertools import product

#%%
class Chess():
    pieces = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]      # don't change ordering
    piecesTable = [pawnstable, knightstable, bishopstable, rookstable, queenstable, kingstable]      # don't change ordering
    weights = [100, 320, 330, 500, 900]     # don't change ordering
    
    def __init__(self,board=None,*args,**kwargs):
        if board:   self.board = chess.Board(board)
        else:       self.board = chess.Board()
        self.movesHistory = []
        self.undoMoves = []
        self.boardValue = self.initEvaluateBoard()
        
    def initEvaluateBoard(self):
        if self.board.is_checkmate():
            if self.board.turn:
                return -float('inf')
            else:
                return float('inf')
        if self.board.is_stalemate():
            return 0
        if self.board.is_insufficient_material():
            return 0
        
        material=0
        for weight, piece in zip(self.weights, self.pieces[:-1]):
            material += weight*(len(self.board.pieces(piece, chess.WHITE))-\
                        len(self.board.pieces(piece, chess.BLACK)))

        val=0
        for piece, table in zip(self.pieces[:-1], self.piecesTable[:-1]):
            val += sum([table[i] for i in self.board.pieces(piece, chess.WHITE)])+\
                    sum([-table[chess.square_mirror(i)] for i in self.board.pieces(piece, chess.BLACK)])

        val += sum([kingstable[i] for i in self.board.pieces(chess.KING, chess.WHITE)])+\
                    sum([-kingstable[chess.square_mirror(i)] for i in self.board.pieces(chess.KING, chess.BLACK)])

        return material + val

    def evaluateBoard(self):
        if self.board.is_checkmate():
            if self.board.turn: return -float('inf')
            else:   return float('inf')
        
        if self.board.is_stalemate():   return 0
        if self.board.is_insufficient_material():    return 0
        
        eval = self.boardValue
        if self.board.turn:  return eval
        return -eval

    def updateEval(self, mov, side):
        #update piecequares
        movingpiece = self.board.piece_type_at(mov.from_square)
        if side:
            self.boardValue -= self.piecesTable[movingpiece - 1][mov.from_square]
            #update castling
            if mov.from_square == chess.E1 and mov.to_square == chess.G1:
                self.boardValue -= rookstable[chess.H1]
                self.boardValue += rookstable[chess.F1]
            elif mov.from_square == chess.E1 and mov.to_square == chess.C1:
                self.boardValue -= rookstable[chess.A1]
                self.boardValue += rookstable[chess.D1]
        else:
            self.boardValue += self.piecesTable[movingpiece-1][mov.from_square]
            #update castling
            if mov.from_square == chess.E8 and mov.to_square == chess.G8:
                self.boardValue -= rookstable[chess.F8]
                self.boardValue += rookstable[chess.H8]
            elif mov.from_square == chess.E8 and mov.to_square == chess.C8:
                self.boardValue -= rookstable[chess.D8]
                self.boardValue += rookstable[chess.A8]
            
        if side:    self.boardValue += self.piecesTable[movingpiece-1][mov.to_square]
        else:   self.boardValue -= self.piecesTable[movingpiece-1][mov.to_square]
            
        
        #update material
        if mov.drop != None:
            if side:    self.boardValue += self.weights[mov.drop-1]
            else:   self.boardValue -= self.weights[mov.drop-1]
                
        #update promotion
        if mov.promotion != None:
            if side:
                self.boardValue += self.weights[mov.promotion-1] - self.weights[movingpiece-1]
                self.boardValue -= self.piecesTable[movingpiece - 1][mov.to_square]\
                                    +self.piecesTable[mov.promotion - 1][mov.to_square]
            else:
                self.boardValue -= self.weights[mov.promotion-1] + self.weights[movingpiece-1]
                self.boardValue += self.piecesTable[movingpiece - 1][mov.to_square]\
                                    -self.piecesTable[mov.promotion - 1][mov.to_square]
        return mov

    def makeMove(self, mov):
        self.updateEval(mov, self.board.turn)
        self.board.push(mov)
        return mov

    def unmakeMove(self):
        mov = self.board.pop()
        self.updateEval(mov, not self.board.turn)
        return mov

    def quiesce(self, alpha, beta):
        stand_pat = self.evaluateBoard()
        if stand_pat >= beta:   return beta
        alpha = max(stand_pat, alpha)

        for move in self.board.legal_moves:
            if self.board.is_capture(move):
                self.makeMove(move)
                score = -self.quiesce(-beta, -alpha)
                self.unmakeMove()
                if score >= beta:   return beta
                alpha = max(score, alpha)
        return alpha

    def alphaBeta(self, alpha, beta, depth):
        bestscore = -float('inf')
        if depth == 0:  return self.quiesce(alpha, beta)
        
        for move in self.board.legal_moves:
            self.makeMove(move)
            score = -self.alphaBeta(-beta, -alpha, depth-1)
            self.unmakeMove()
            if score >= beta:   return score
            bestscore=max(bestscore, score)
            alpha=max(alpha, score)
        return bestscore

    def selectMove(self, depth):
        try:
            move = chess.polyglot.MemoryMappedReader("E:\\dtu\\7thsem\\project\\Performance\\Performance.bin").weighted_choice(self.board).move()
            self.movesHistory.append(move)
            return move
        except:
            bestMove = chess.Move.null()
            alpha = -float('inf')
            bestValue = -float('inf')
            beta = float('inf')
            for move in self.board.legal_moves:
                self.makeMove(move)
                boardValue = -self.alphaBeta(-beta, -alpha, depth-1)
                if boardValue > bestValue:
                    bestValue = boardValue
                    bestMove = move
                alpha = max(boardValue, alpha)
                self.board.pop()
            self.movesHistory.append(bestMove)
            return bestMove

    def printBoard(self, move=None):
        """
        prints the board into ascii formate
        """
        if move:
            mFrom = [8-int(move[1]), ord(move[0])-ord('a')]
            mTo = [8-int(move[3]), ord(move[2])-ord('a')]
            
        board = str(self.board).replace(" ", "").split('\n')
        # print(board)
        xAxis ='   '+'  '.join([chr(ord('a')+i) for i in range(8)])
        upperLine = "┍"+"━"*28+"┑"
        lowerLine = "┕"+"━"*28+"┙"
        dashed = '-- '*8
        
        print(upperLine)
        print(xAxis)
        # print("   "+dashed)
        for row, piecesRow in iter(enumerate(board)):
            s = ""
            for col, c in enumerate(piecesRow):
                if c!=".":
                    s+=UNICODE_PIECE_SYMBOLS[c]
                else:
                    if move and (mFrom[0] == row and mFrom[1]==col):
                        s+="⛶"
                    else:
                        s+=c
            print(f'{8-row} │{" |".join(s)} │ {8-row}')
            # print("   "+dashed)
        print(xAxis)
        print(lowerLine)
    
    def playManually(self, playFirst=0, timeLimit=5):
        import chess.pgn
        import datetime
        import chess.engine
    
        engine = chess.engine.SimpleEngine.popen_uci("E:\\dtu\\7thsem\\project\\stockfish-10-win\\Windows\\stockfish.exe")
        limit = chess.engine.Limit(time=timeLimit)
        notKilled = 1       # checks if window is killed 

        game = chess.pgn.Game()
        game.headers["Event"] = "Example"
        game.headers["Site"] = "Laptop"
        game.headers["Date"] = str(datetime.datetime.now().date())
        game.headers["Round"] = 1
        game.headers["White"] = "MyMiniChess"
        game.headers["Black"] = str(engine.id.get("name"))
        if playFirst==0:
            game.headers["White"], game.headers["Black"]=game.headers["Black"], game.headers["White"]
        
        self.printBoard()
        print()
        
        while notKilled and (not self.board.is_game_over(claim_draw=True)):
            if playFirst:
                while notKilled:
                    try:
                        inp = input('Your Turn: ')
                        if inp=='exit':
                            notKilled = 0
                            engine.quit()
                            break

                        move = chess.Move.from_uci(inp)
                        moveStr=str(move)
                        mFrom = [int(moveStr[1])-1, ord(moveStr[0])-ord('a')]
                        p = str(self.board.piece_at(mFrom[0]*8 + mFrom[1]))

                        self.board.push(move)
                        self.movesHistory.append(move)
                        playFirst = not playFirst

                        print("━-"*17)
                        self.printBoard(move=str(move))
                        print(f"You: {UNICODE_PIECE_SYMBOLS[p]}  by {moveStr}")
                        break
                    except:
                        print("Wrong Move: consider uci formated move or \"exit\" to halt the game")
                        print()
                
            else:
                move = engine.play(self.board, limit=limit)
                self.movesHistory.append(move.move)
                
                moveStr=str(move.move)
                mFrom = [int(moveStr[1])-1, ord(moveStr[0])-ord('a')]
                p = str(self.board.piece_at(mFrom[0]*8 + mFrom[1]))
                
                self.board.push(move.move)
                playFirst = not playFirst
                self.printBoard(move=moveStr)
                
                print(f"AI: {UNICODE_PIECE_SYMBOLS[p]}  by {moveStr}")
                print()
                
        if notKilled:
            game.add_line(self.movesHistory)
            game.headers["Result"] = str(self.board.result(claim_draw=True))
            print(game)
            print(game, file=open("test.pgn", "w"), end="\n\n")
            print(chess)
        
        engine.quit()
        return
    
    def play(self, playFirst=0, timeLimit=5):
        import chess.pgn
        import datetime
        import chess.engine
    
        engine = chess.engine.SimpleEngine.popen_uci("E:\\dtu\\7thsem\\project\\stockfish-10-win\\Windows\\stockfish.exe")
        limit = chess.engine.Limit(time=0.02)
        
        game = chess.pgn.Game()
        game.headers["Event"] = "Example"
        game.headers["Site"] = "Laptop"
        game.headers["Date"] = str(datetime.datetime.now().date())
        game.headers["Round"] = 1
        game.headers["White"] = "MyMiniChess"
        game.headers["Black"] = str(engine.id.get("name"))
        
        lastMove = 1
        while not self.board.is_game_over(claim_draw=True):
            if self.board.turn:
                playFirst = not playFirst
                move = self.selectMove(depth=2)
                self.board.push(move)
                print("━-"*17)
                self.printBoard()
                lastMove = str(move)
                print(f"dumb AI: {lastMove}")

            else:
                move = engine.play(self.board, limit=limit)
                self.movesHistory.append(move.move)
                self.board.push(move.move)
                playFirst = not playFirst
                self.printBoard()
                print(f"stockfish: {str(move.move)}")
                print('\n\n')

        game.add_line(self.movesHistory)
        game.headers["Result"] = str(self.board.result(claim_draw=True))
        print(game)
        print(game, file=open("test.pgn", "w"), end="\n\n")
        self.printBoard()
        engine.quit()
        return


#%%
if __name__ == "__main__":
    # board = chess.Board()
    # print(board)

    # c = Chess()
    # c.play(playFirst=1, timeLimit=0.0005)
    # c.printBoard()
    # c.playManually(playFirst=0, timeLimit=0.02)
    
    positions = [
                "1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1",
                "3r1k2/4npp1/1ppr3p/p6P/P2PPPP1/1NR5/5K2/2R5 w - - 0 1",
                "2q1rr1k/3bbnnp/p2p1pp1/2pPp3/PpP1P1P1/1P2BNNP/2BQ1PRK/7R b - - 0 1",
                "rnbqkb1r/p3pppp/1p6/2ppP3/3N4/2P5/PPP1QPPP/R1B1KB1R w KQkq - 0 1",
                "r1b2rk1/2q1b1pp/p2ppn2/1p6/3QP3/1BN1B3/PPP3PP/R4RK1 w - - 0 1",
                "2r3k1/pppR1pp1/4p3/4P1P1/5P2/1P4K1/P1P5/8 w - - 0 1",
                "1nk1r1r1/pp2n1pp/4p3/q2pPp1N/b1pP1P2/B1P2R2/2P1B1PP/R2Q2K1 w - - 0 1",
                "4b3/p3kp2/6p1/3pP2p/2pP1P2/4K1P1/P3N2P/8 w - - 0 1",
                "2kr1bnr/pbpq4/2n1pp2/3p3p/3P1P1B/2N2N1Q/PPP3PP/2KR1B1R w - - 0 1",
                "3rr1k1/pp3pp1/1qn2np1/8/3p4/PP1R1P2/2P1NQPP/R1B3K1 b - - 0 1",
                "2r1nrk1/p2q1ppp/bp1p4/n1pPp3/P1P1P3/2PBB1N1/4QPPP/R4RK1 w - - 0 1",
                "r3r1k1/ppqb1ppp/8/4p1NQ/8/2P5/PP3PPP/R3R1K1 b - - 0 1",
                "r2q1rk1/4bppp/p2p4/2pP4/3pP3/3Q4/PP1B1PPP/R3R1K1 w - - 0 1",
                "rnb2r1k/pp2p2p/2pp2p1/q2P1p2/8/1Pb2NP1/PB2PPBP/R2Q1RK1 w - - 0 1",
                "2r3k1/1p2q1pp/2b1pr2/p1pp4/6Q1/1P1PP1R1/P1PN2PP/5RK1 w - - 0 1",
                "r1bqkb1r/4npp1/p1p4p/1p1pP1B1/8/1B6/PPPN1PPP/R2Q1RK1 w kq - 0 1",
                "r2q1rk1/1ppnbppp/p2p1nb1/3Pp3/2P1P1P1/2N2N1P/PPB1QP2/R1B2RK1 b - - 0 1",
                "r1bq1rk1/pp2ppbp/2np2p1/2n5/P3PP2/N1P2N2/1PB3PP/R1B1QRK1 b - - 0 1",
                "3rr3/2pq2pk/p2p1pnp/8/2QBPP2/1P6/P5PP/4RRK1 b - - 0 1",
                "r4k2/pb2bp1r/1p1qp2p/3pNp2/3P1P2/2N3P1/PPP1Q2P/2KRR3 w - - 0 1",
                "3rn2k/ppb2rpp/2ppqp2/5N2/2P1P3/1P5Q/PB3PPP/3RR1K1 w - - 0 1",
                "2r2rk1/1bqnbpp1/1p1ppn1p/pP6/N1P1P3/P2B1N1P/1B2QPP1/R2R2K1 b - - 0 1",
                "r1bqk2r/pp2bppp/2p5/3pP3/P2Q1P2/2N1B3/1PP3PP/R4RK1 b kq - 0 1",
                "r2qnrnk/p2b2b1/1p1p2pp/2pPpp2/1PP1P3/PRNBB3/3QNPPP/5RK1 w - - 0 1",
                ]
    solutions = ["Qd1+","d5","f5","e6","a4","g6","Nf6","f5","f5","Ne5","f4","Bf5","b4",
             "Qd2 Qe1","Qxg7+","Ne4","h5","Nb3","Rxe4","g4","Nh6","Bxe4","f6","f4"]
    
    # solved = 0
    # for board, sol in zip(positions, solutions):
    #     c = Chess(board=board)
    #     move = c.selectMove(5)
    #     print(sol, c.board.san(move), end=": ")
    #     if str(c.board.san(move)) in sol:
    #         solved+=1
    #         print("True", end="")
    #     print(" ")
    # print(f"solved: {solved}/{len(positions)}")
    



def init_evaluate_board():
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    
    material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)
    
    pawnsq = sum([pawnstable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq= pawnsq + sum([-pawnstable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq= sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq= bishopsq + sum([-bishopstable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) 
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) 
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)]) 
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.KING, chess.BLACK)])
    
    boardvalue = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    
    return boardvalue

def evaluate_board():
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0
    
    eval = init_evaluate_board()
    if board.turn:
        return eval
    else:
        return -eval

piecetypes = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING ]
tables = [pawnstable, knightstable, bishopstable, rookstable, queenstable, kingstable]
piecevalues = [100,320,330,500,900]
def update_eval(mov, side):
    global boardvalue
    
    #update piecequares
    movingpiece = board.piece_type_at(mov.from_square)
    if side:
        boardvalue = boardvalue - tables[movingpiece - 1][mov.from_square]
        #update castling
        if (mov.from_square == chess.E1) and (mov.to_square == chess.G1):
            boardvalue = boardvalue - rookstable[chess.H1]
            boardvalue = boardvalue + rookstable[chess.F1]
        elif (mov.from_square == chess.E1) and (mov.to_square == chess.C1):
            boardvalue = boardvalue - rookstable[chess.A1]
            boardvalue = boardvalue + rookstable[chess.D1]
    else:
        boardvalue = boardvalue + tables[movingpiece - 1][mov.from_square]
        #update castling
        if (mov.from_square == chess.E8) and (mov.to_square == chess.G8):
            boardvalue = boardvalue + rookstable[chess.H8]
            boardvalue = boardvalue - rookstable[chess.F8]
        elif (mov.from_square == chess.E8) and (mov.to_square == chess.C8):
            boardvalue = boardvalue + rookstable[chess.A8]
            boardvalue = boardvalue - rookstable[chess.D8]
        
    if side:
        boardvalue = boardvalue + tables[movingpiece - 1][mov.to_square]
    else:
        boardvalue = boardvalue - tables[movingpiece - 1][mov.to_square]
        
     
    #update material
    if mov.drop != None:
        if side:
            boardvalue = boardvalue + piecevalues[mov.drop-1]
        else:
            boardvalue = boardvalue - piecevalues[mov.drop-1]
            
    #update promotion
    if mov.promotion != None:
        if side:
            boardvalue = boardvalue + piecevalues[mov.promotion-1] - piecevalues[movingpiece-1]
            boardvalue = boardvalue - tables[movingpiece - 1][mov.to_square] \
                + tables[mov.promotion - 1][mov.to_square]
        else:
            boardvalue = boardvalue - piecevalues[mov.promotion-1] + piecevalues[movingpiece-1]
            boardvalue = boardvalue + tables[movingpiece - 1][mov.to_square] \
                - tables[mov.promotion - 1][mov.to_square]
            
            
    return mov

def make_move(mov):
    update_eval(mov, board.turn)
    board.push(mov)
    return mov

def unmake_move():
    mov = board.pop()
    update_eval(mov, not board.turn)
    return mov

def quiesce( alpha, beta ):
    stand_pat = evaluate_board()
    if( stand_pat >= beta ):
        return beta
    if( alpha < stand_pat ):
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            make_move(move)        
            score = -quiesce( -beta, -alpha )
            unmake_move()

            if( score >= beta ):
                return beta
            if( score > alpha ):
                alpha = score  
    return alpha

def alphabeta( alpha, beta, depthleft ):
    bestscore = -9999
    if( depthleft == 0 ):
        return quiesce( alpha, beta )
    for move in board.legal_moves:
        make_move(move)   
        score = -alphabeta( -beta, -alpha, depthleft - 1 )
        unmake_move()
        if( score >= beta ):
            return score
        if( score > bestscore ):
            bestscore = score
        if( score > alpha ):
            alpha = score   
    return bestscore

import chess.polyglot

def selectmove(depth):
    try:
        move = chess.polyglot.MemoryMappedReader("E:\\dtu\\7thsem\\project\\Performance\\Performance.bin").weighted_choice(board).move()
        # movehistory.append(move)
        return move
    except:
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000
        for move in board.legal_moves:
            make_move(move)
            boardValue = -alphabeta(-beta, -alpha, depth-1)
            if boardValue > bestValue:
                bestValue = boardValue;
                bestMove = move
            if( boardValue > alpha ):
                alpha = boardValue
            unmake_move()
        # movehistory.append(bestMove)
        return bestMove


# for b in positions[:1]+positions[3:]:
#     c = Chess(board=b)
    
#     board = chess.Board(b)
#     boardvalue = init_evaluate_board()
    
#     # val = alphabeta(-5, 5, 2)
#     # mine = c.alphaBeta(-5, 5, 2)
    
#     val = selectmove(2)
#     mine = selectmove(2)
    
#     print(mine, val, mine==val)
b=Chess(board='r2q3r/pp3k2/2p1n1pp/4Pp2/4pNnP/1QN1P3/PP3PP1/R3K2R b KQ - 4 17')
b.printBoard()
# d=3
# c=Chess(board="1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1")
# # move = c.quiesce(95, -1)
# move = c.alphaBeta(100, -1, 1)
# print(move)

# # movehistory =[]
# board = chess.Board("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1")
# boardvalue = init_evaluate_board()
# # move = selectmove(d)     #a7a6
# move = alphabeta(100, -1, 1)
# print(move)