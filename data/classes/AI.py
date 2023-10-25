import random
import math
from Pycharm_Projects.Chess_Test.data.classes.board import *


class AI:

    promotion_pieces = [Queen, Knight, Bishop, Rook]
    def __init__(self, engine, difficulty, depth, color):
        self.engine = engine
        self.difficulty = difficulty
        self.depth = depth
        self.color = color

        self.squares_with_piece = []
        self.moves = []
        self.promotion_pieces = [Queen, Knight, Bishop, Rook]

    def play_moves(self, board, engine='alea iacta est'):
        print(board.evaluate_position(self.color))
        self.squares_with_piece = board.save_own_square_pieces(self.color)
        self.moves = board.get_moves(self.color)

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
            print(best_score)
            print(moves[1])
            piece_and_move = random.choice(moves[0])
            board.ai_move(piece_and_move[0],piece_and_move[1], self.promotion_pieces[0], False)
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

    def minmax(self, board, depth, alpha, beta, max_player):
        if max_player:
            player_color = 'black'
        else:
            player_color = 'white'

        if depth == 0 or board.check_game_end(player_color):
            print('depth reached')
            return board.evaluate_position(player_color)

        moves = board.get_moves(player_color)
        print(f'minimax for: {player_color}, depth: {depth}, possibility for: {len(moves)} moves')
        if max_player:
            max_eval = -math.inf
            for curr_move in moves:
                curr_piece = board.squares[curr_move.initial_square.rank][curr_move.initial_square.file].piece
                print(f'eval calculated for: {curr_piece.name} moves '
                      f'from ({curr_move.initial_square.rank}, {curr_move.initial_square.file}) '
                      f'to ({curr_move.final_square.rank}, {curr_move.final_square.file})')
                board.ai_move(curr_piece, curr_move, self.promotion_pieces[0], True)
                evaluation = self.minmax(board, depth - 1, alpha, beta, False)
                board.unmake_move(curr_piece, curr_move)
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for curr_move in moves:
                curr_piece = board.squares[curr_move.initial_square.rank][curr_move.initial_square.file].piece
                print(f'eval calculated for: {curr_piece.name} moves '
                      f'from ({curr_move.initial_square.rank}, {curr_move.initial_square.file}) '
                      f'to ({curr_move.final_square.rank}, {curr_move.final_square.file})')
                board.ai_move(curr_piece, curr_move, self.promotion_pieces[0], True)
                evaluation = self.minmax(board, depth - 1, alpha, beta, True)
                board.unmake_move(curr_piece, curr_move)
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval

    def minimax(self, board, depth, alpha, beta, max_player, save_move, data):
        if max_player:
            player_color = self.color
        else:
            if self.color == 'white':
                player_color = 'black'
            else:
                player_color = 'white'

        if depth == 0 or board.check_game_end(player_color):
            data[1] = board.evaluate_position(player_color)
            return data

        if max_player:
            max_eval = -math.inf
            for rank in range(ranks):
                for file in range(files):
                    if board.squares[rank][file].occupied_by_teammate(player_color):
                        piece = board.squares[rank][file].piece
                        board.calculate_valid_moves(piece, rank, file, bool=True)
                        for move in piece.moves:
                            # wie machen wir das mit der promotion????
                            board.ai_move(piece, move, self.promotion_pieces[0], True)
                            evaluation = self.minimax(board, depth - 1, alpha, beta, False, False, data)[1]
                            if save_move:
                                if evaluation >= max_eval:
                                    if evaluation > data[1]:
                                        data.clear()
                                        data[1] = evaluation
                                        data[0] = [piece, move, evaluation]
                                    elif evaluation == data[1]:
                                        data[0].append([piece, move, evaluation])
                            board.unmake_move(piece, move)
                            max_eval = max(max_eval, evaluation)
                            alpha = max(alpha, evaluation)
                            if beta <= alpha:
                                break
            return data

        else:
            min_eval = math.inf

            for rank in range(ranks):
                for file in range(files):
                    if board.squares[rank][file].occupied_by_teammate(player_color):
                        piece = board.squares[rank][file].piece
                        board.calculate_valid_moves(piece, rank, file, bool=True)
                        for move in piece.moves:
                            board.ai_move(piece, move, self.promotion_pieces[0], True)
                            evaluation = self.minimax(board, depth - 1, alpha, beta, True, False, data)[1]
                            board.unmake_move(piece, move)
                            min_eval = min(min_eval, evaluation)
                            beta = min(beta, evaluation)
                            if beta <= alpha:
                                break
            return data



