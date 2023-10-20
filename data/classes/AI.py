import random
from Pycharm_Projects.Chess_Test.data.classes.board import *


class AI:

    def __init__(self, engine, difficulty, depth, color):
        self.engine = engine
        self.difficulty = difficulty
        self.depth = depth
        self.color = color

        self.pieces = []

    def play_random(self, board):
        if self.pieces:
            while True:
                rank, file = random.choice(self.pieces)
                piece = board.squares[rank][file].piece
                board.calculate_valid_moves(piece, rank, file, bool=True)
                if piece.moves:
                    move = random.choice(piece.moves)
                    board.move(piece, move)
                    return
                else:
                    self.pieces.remove((rank, file))
        else:
            print('no pieces available for the ai')


