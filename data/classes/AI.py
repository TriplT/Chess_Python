import random
from Pycharm_Projects.Chess_Test.data.classes.board import *


class AI:

    def __init__(self, difficulty, depth, color):
        self.difficulty = difficulty
        self.depth = depth
        self.color = color

        self.pieces = []
        self.promotion_pieces = [Queen, Knight, Bishop, Rook]

    def play_moves(self, board, engine='random'):
        # engines
        def play_random():
            if self.pieces:
                while True:
                    if not self.pieces:
                        for rank in range(ranks):
                            for file in range(files):
                                print(board.squares[rank][file].piece)
                                if board.squares[rank][file].piece:
                                    print(board.squares[rank][file].piece.color)
                    print('reset')
                    rank, file = random.choice(self.pieces)
                    piece = board.squares[rank][file].piece
                    board.calculate_valid_moves(piece, rank, file, bool=True)
                    if piece.moves:
                        move = random.choice(piece.moves)
                        if board.valid_move(piece, move):
                            promotion_piece = random.choice(self.promotion_pieces)
                            board.ai_move(piece, move, promotion_piece)
                        return
                    else:
                        self.pieces.remove((rank, file))
            else:
                print('no pieces available for the ai')

        # engine names
        if engine == 'random':
            play_random()



