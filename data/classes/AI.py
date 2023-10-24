import random
import math
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
        print(self.evaluate_position(board))
        self.squares_with_piece = board.save_own_square_pieces(self.color)

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
                board.calculate_valid_moves(piece, square.rank, square.file, bool=False)

                if not piece.moves:
                    self.squares_with_piece.remove(square)
                    if isinstance(piece, Pawn):
                        pawns.remove(square)
                else:
                    move = None
                    if_statements = [lambda m: abs(m.initial_square.file - m.final_square.file) == 1,
                                     lambda m: abs(m.initial_square.rank - m.final_square.rank) == 2,
                                     lambda m: abs(m.initial_square.rank - m.final_square.rank) == 1]

                    for condition in if_statements:
                        if move is not None:
                            break
                        for m in piece.moves:
                            if isinstance(piece, Pawn) and condition(m):
                                move = m
                                break

                    if not move:
                        move = random.choice(piece.moves)

                    if board.valid_move(piece, move):
                        promotion_piece = self.promotion_pieces[0]
                        board.ai_move(piece, move, promotion_piece)
                        return

        def play_berserk_killer():
            capture_moves = []
            global move
            global piece
            move = None
            piece = None

            for square in self.squares_with_piece:
                piece = square.piece
                board.calculate_valid_moves(piece, square.rank, square.file, bool=True)
                for m in piece.moves:
                    if board.squares[m.final_square.rank][m.final_square.file].piece:
                        capture_moves.append(m)

            if capture_moves:
                move = random.choice(capture_moves)
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece
            else:
                while True:
                    square = random.choice(self.squares_with_piece)
                    piece = square.piece
                    board.calculate_valid_moves(piece, square.rank, square.file, bool=True)

                    if not piece.moves:
                        self.squares_with_piece.remove(square)
                    else:
                        move = random.choice(piece.moves)
                        break

            if board.valid_move(piece, move):
                promotion_piece = random.choice(self.promotion_pieces)
                board.ai_move(piece, move, promotion_piece)

        def play_interstellar():
            moves = self.minimax(board, 4, -math.inf, math.inf, True, True, [[], 0])

            if len(moves) == 0:
                return False
            best_score = max(moves[0], key=lambda x: x[2])[2]
            piece_and_move = random.choice([move for move in moves[0] if move[2] == best_score])
            piece = piece_and_move[0]
            move = piece_and_move[1]
            if piece and len(move) > 0 and isinstance(move, tuple):
                board.ai_move(piece, move)
            return True

        # engine names
        if engine == 'alea iacta est':  # plays random moves throughout the game
            play_random()

        if engine == 'ambitious promoter':  # tries to promote at every opportunity
            play_try_to_promote_pawns()

        if engine == 'berserk killer':  # tries to kill at every opportunity
            play_berserk_killer()

        if engine == 'interstellar calculator':  # best engine
            play_interstellar()

        if engine == 'AI annihilator':  # best engine-like engine (or is it?)
            play_random()

    def evaluate_position(self, board):
        pieces = board.save_all_pieces()
        position_value = 0
        for piece in pieces:
            position_value += piece.value

        if self.color == 'white':
            return round(position_value, 3)
        else:
            return - round(position_value, 3)

    def minimax(self, board, depth, alpha, beta, maximizing_player, save_move, data):
        print('minimax starting')
        if depth == 0 or board.check_game_end(self.color):
            print('game ended??? or depth == 0???')
            data[1] = self.evaluate_position(board)
            print('lets return')
            return data

        if maximizing_player:
            print('minimax for max')
            max_eval = -math.inf

            for rank in range(ranks):
                for file in range(files):
                    piece = board.squares[rank][file].piece
                    if piece and piece.color != self.color:
                        print('calc valid moves')
                        board.calculate_valid_moves(piece, rank, file, bool=True)
                        for move in piece.moves:
                            # wie machen wir das mit der promotion????
                            board.ai_move(piece, move, self.promotion_pieces[0], True)
                            eval = self.minimax(board, depth - 1, alpha, beta, False, False, data)[1]
                            if save_move:
                                if eval >= max_eval:
                                    if eval > data[1]:
                                        data.clear()
                                        data[1] = eval
                                        data[0] = [piece, move, eval]
                                    elif eval == data[1]:
                                        data[0].append([piece, move, eval])
                            board.unmake_move(piece, move)
                            max_eval = max(max_eval, eval)
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                break
            print(data)
            return data

        else:
            print('minimax for min')
            min_eval = math.inf

            for rank in range(ranks):
                for file in range(files):
                    piece = board.squares[rank][file].piece
                    if piece and piece.color == self.color:
                        print('calc valid moves')
                        board.calculate_valid_moves(piece, rank, file, bool=True)
                        for move in piece.moves:
                            board.ai_move(piece, move, self.promotion_pieces[0], True)
                            eval = self.minimax(board, depth - 1, alpha, beta, True, False, data)[1]
                            board.unmake_move(piece, move)
                            min_eval = min(min_eval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                break
            print(data)
            return data



