import random
from Pycharm_Projects.Chess_Test.data.classes.board import *


class AI:

    def __init__(self, engine, difficulty, depth, board, color='white'):
        self.engine = engine
        self.difficulty = difficulty
        self.depth = depth
        self.color = color
        self.board = board

        self.pieces = self.board.save_pieces(self.color)

    def play_random(self):
        while True:
            rank, file = random.choice(self.pieces)
            piece = self.board.squares[rank][file].piece
            self.board.calculate_valid_moves(piece, rank, file, bool=True)
            if piece.moves:
                move = random.choice(piece.moves)
                self.board.move(piece, move)

            else:
                self.pieces.remove((rank, file))
