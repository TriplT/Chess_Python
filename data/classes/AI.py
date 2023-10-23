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
            print('move random')
            if self.pieces:
                while True:
                    if not self.pieces:
                        print('no pieces left, error')
                        print(self.color)
                        while True:
                            if self.difficulty == 8:
                                return

                    print('reset')
                    rank, file = random.choice(self.pieces)
                    piece = board.squares[rank][file].piece
                    board.calculate_valid_moves(piece, rank, file, bool=True)
                    print(piece, piece.color)
                    if piece.moves:
                        move = random.choice(piece.moves)
                        if board.valid_move(piece, move):
                            promotion_piece = random.choice(self.promotion_pieces)
                            board.ai_move(piece, move, promotion_piece)
                            return
                        else:
                            piece.moves.remove(move)
                            print('move removed')
                    else:
                        self.pieces.remove((rank, file))
                        print('piece removed')
            else:
                print('no pieces available for the ai')

        # engine names
        if engine == 'random':
            play_random()



