import random
from Pycharm_Projects.Chess_Test.data.classes.board import *


class AI:

    def __init__(self, engine, difficulty, depth, color):
        self.engine = engine
        self.difficulty = difficulty
        self.depth = depth
        self.color = color

        self.squares_with_piece = []
        self.promotion_pieces = [Queen, Knight, Bishop, Rook]

    def play_moves(self, board, engine='alea iacta est'):
        self.squares_with_piece = board.save_own_pieces(self.color)

        if not self.squares_with_piece:
            exit(0)

        # engines
        def play_random():
            while True:
                square = random.choice(self.squares_with_piece)
                piece = square.piece
                board.calculate_valid_moves(piece, square.rank, square.file, bool=True)

                if not piece.moves:
                    self.squares_with_piece.remove(square)
                else:
                    move = random.choice(piece.moves)

                    if board.valid_move(piece, move):
                        promotion_piece = random.choice(self.promotion_pieces)
                        board.ai_move(piece, move, promotion_piece)
                        return

        def play_try_to_promote_pawns():
            pawns = []
            for square in self.squares_with_piece:
                if isinstance(square.piece, Pawn):
                    pawns.append(square)

            while True:
                if not pawns:
                    square = random.choice(self.squares_with_piece)
                else:
                    square = random.choice(pawns)

                piece = square.piece
                board.calculate_valid_moves(piece, square.rank, square.file, bool=True)

                if not piece.moves:
                    self.squares_with_piece.remove(square)
                    if isinstance(piece, Pawn):
                        pawns.remove(square)
                else:
                    chosen_moves = []
                    for move in piece.moves:
                        if isinstance(piece, Pawn):
                            if abs(move.initial_square.file - move.final_square.file) == 1:
                                chosen_moves.append(move)
                                break
                            elif abs(move.initial_square.rank - move.final_square.rank) == 2:
                                chosen_moves.append(move)
                                break
                            else:
                                chosen_moves.append(move)
                                break

                    else:
                        chosen_moves.append(random.choice(piece.moves))

                    if board.valid_move(piece, chosen_moves[0]):
                        promotion_piece = random.choice(self.promotion_pieces)
                        board.ai_move(piece, move, promotion_piece)
                        return

        # engine names
        if engine == 'alea iacta est':
            play_random()

        if engine == 'ambitious promoter':
            play_try_to_promote_pawns()




