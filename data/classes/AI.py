import random
from Pycharm_Projects.Chess_Test.data.classes.board import *


class AI:

    def __init__(self, engine, difficulty, depth, color):
        self.engine = engine
        self.difficulty = difficulty
        self.depth = depth
        self.color = color

        self.pieces = []
        self.promotion_pieces = [Queen, Knight, Bishop, Rook]

    def play_moves(self, board, engine='random'):
        self.pieces = board.save_own_pieces(self.color)

        if not self.pieces:
            exit(0)

        # engines
        def play_random():
            while True:
                square = random.choice(self.pieces)
                piece = square.piece
                board.calculate_valid_moves(piece, square.rank, square.file, bool=True)

                if not piece.moves:
                    self.pieces.remove(square)
                else:
                    move = random.choice(piece.moves)

                    if board.valid_move(piece, move):
                        promotion_piece = random.choice(self.promotion_pieces)
                        board.ai_move(piece, move, promotion_piece)
                        return

        # engine names
        if engine == 'random':
            play_random()



