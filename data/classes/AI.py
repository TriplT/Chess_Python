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
        # print(board.evaluate_position(self.color))
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
            eval, move = self.minimax(board, 6, -math.inf, math.inf, True)
            print(move)
            print(eval)
            piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

            print(f'this is the final move: {move}')
            print(f'initial sq: ({move.initial_square.rank}, {move.initial_square.file}) final sq: ({move.final_square.rank}, {move.final_square.file})')
            print(f'this is the final eval: {eval}')

            if move:
                board.ai_move(piece, move, self.promotion_pieces[0], False)
                print(' ')
                print('AI MOVE PLAYED')
                print(' ')
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

    def minimax(self, board, depth, alpha, beta, max_player, best_move=Move((7, 7), (7, 8))):

        if max_player:
            player_color = self.color
        else:
            if self.color == 'white':
                player_color = 'black'
            else:
                player_color = 'white'

        if board.check_game_end(player_color, max_player):
            print(f'game end eval: {board.evaluation}')
            return board.evaluation, best_move
        elif depth == 0:
            print(' ')
            print('depth reached')
            print(' ')
            board.evaluate_position(player_color)
            return board.evaluation, best_move

        if max_player:
            max_eval = -math.inf
            max_move = -math.inf

            for move in board.calculate_all_valid_moves(player_color):
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                print(f'depth: {depth}')
                print(f'{player_color} move: {piece.name} to ({move.final_square.rank, move.final_square.file})')

                board.ai_move_simulation(piece, move, self.promotion_pieces[0], True)
                evaluation = self.minimax(board, depth - 1, alpha, beta, False)
                board.unmake_move(piece, move)

                max_eval = max(max_eval, evaluation[0])
                if max_eval > max_move:
                    max_move = max_eval
                    best_max_move = move

                alpha = max(alpha, evaluation[0])
                if beta <= alpha:
                    break
            return max_eval, best_max_move

        else:
            min_eval = math.inf
            min_move = math.inf

            for move in board.calculate_all_valid_moves(player_color):
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                print(f'depth: {depth}')
                print(f'{player_color} move: {piece.name} to ({move.final_square.rank, move.final_square.file})')

                board.ai_move_simulation(piece, move, self.promotion_pieces[0], True)
                evaluation = self.minimax(board, depth - 1, alpha, beta, True)
                board.unmake_move(piece, move)

                min_eval = min(min_eval, evaluation[0])
                if min_eval < min_move:
                    min_move = min_eval
                    best_min_move = move

                beta = min(beta, evaluation[0])
                if beta <= alpha:
                    break
            return min_eval, best_min_move

    def minimax_copy(self, board, depth, alpha, beta, max_player, best_move=Move((7, 7), (7, 8))):

        if max_player:
            player_color = self.color
        else:
            if self.color == 'white':
                player_color = 'black'
            else:
                player_color = 'white'

        if depth == 0 or board.check_game_end(player_color):
            return board.evaluate_position(player_color), best_move

        if max_player:
            max_eval = -math.inf
            max_move = -math.inf

            for move in board.get_movess(player_color):
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                board.ai_move_simulation(piece, move, self.promotion_pieces[0], True)
                evaluation = self.minimax(board, depth - 1, alpha, beta, False)
                board.unmake_move(piece, move)

                max_eval = max(max_eval, evaluation[0])
                if max_eval > max_move:
                    max_move = max_eval
                    best_max_move = move

                alpha = max(alpha, evaluation[0])
                if beta <= alpha:
                    break
            return max_eval, best_max_move

        else:
            min_eval = math.inf
            min_move = math.inf

            for move in board.get_movess(player_color):
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                board.ai_move_simulation(piece, move, self.promotion_pieces[0], True)
                evaluation = self.minimax(board, depth - 1, alpha, beta, True)
                board.unmake_move(piece, move)

                min_eval = min(min_eval, evaluation[0])

                if min_eval < min_move:
                    min_move = min_eval
                    best_min_move = move

                beta = min(beta, evaluation[0])
                if beta <= alpha:
                    break
            return min_eval, best_min_move

    def minimax_copy_2(self, board, depth, alpha, beta, max_player, best_move=Move((7, 7), (7, 8))):

        if max_player:
            player_color = self.color
        else:
            if self.color == 'white':
                player_color = 'black'
            else:
                player_color = 'white'

        if depth == 0 or board.check_game_end(player_color):
            return board.evaluate_position(player_color), best_move

        if max_player:
            max_eval = -math.inf
            max_move = -math.inf

            for move in board.get_movess(player_color):
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                print(piece.name)
                print(f'move self: ({move.initial_square.rank}, {move.initial_square.file}) to ({move.final_square.rank}, {move.final_square.file})')

                board.ai_move(piece, move, self.promotion_pieces[0], True)
                evaluation = self.minimax(board, depth - 1, alpha, beta, False)
                board.unmake_move(piece, move)

                print(f'max eval : {max_eval}, evaluation: {evaluation}')
                max_eval = max(max_eval, evaluation)
                if max_eval > max_move:
                    max_move = max_eval
                    best_max_move = move

                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval, best_max_move

        else:
            min_eval = math.inf

            for move in board.get_movess(player_color):
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                print(piece.name)
                print(f'move enemy: ({move.initial_square.rank}, {move.initial_square.file}) to ({move.final_square.rank}, {move.final_square.file})')

                board.ai_move(piece, move, self.promotion_pieces[0], True)
                evaluation = self.minimax(board, depth - 1, alpha, beta, True)[0]
                board.unmake_move(piece, move)

                print(f'min eval : {min_eval}, evaluation: {evaluation}')
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval

    def minimax_copy_3(self, board, depth, alpha, beta, max_player, best_move=Move((7, 7), (7, 8))):

        print(' ')
        print('minimax starting')

        if max_player:
            player_color = self.color
        else:
            if self.color == 'white':
                player_color = 'black'
            else:
                player_color = 'white'

        if depth == 0 or board.check_game_end(player_color):
            return board.evaluate_position(player_color), best_move

        if max_player:
            max_eval = -math.inf
            max_move = -math.inf

            for move in board.get_movess(player_color):
                print(f'move self: ({move.initial_square.rank}, {move.initial_square.file}) to ({move.final_square.rank}, {move.final_square.file})')
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece
                print(piece.name)

                board.ai_move(piece, move, self.promotion_pieces[0], True)
                evaluation = self.minimax(board, depth - 1, alpha, beta, False)
                board.unmake_move(piece, move)

                print(f'max eval : {max_eval}, evaluation: {evaluation}')
                max_eval = max(max_eval, evaluation)
                print('max eval and move')
                print(max_eval)
                print(max_move)
                if max_eval > max_move:
                    max_move = max_eval
                    best_max_move = move
                    print(best_max_move)

                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval, best_max_move

        else:
            min_eval = math.inf

            for move in board.get_movess(player_color):
                print(f'move enemy: ({move.initial_square.rank}, {move.initial_square.file}) to ({move.final_square.rank}, {move.final_square.file})')
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece
                print(piece.name)

                board.ai_move(piece, move, self.promotion_pieces[0], True)
                evaluation = self.minimax(board, depth - 1, alpha, beta, True)[0]
                board.unmake_move(piece, move)

                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval

    def minomax(self, board, depth, alpha, beta, max_player, save_move, data):
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
                            if save_move:
                                print(' ')
                                print(f'max eval: {data[1]}')
                                print(' ')
                            print(' ')
                            print(player_color, depth)
                            print(f'current eval: {max_eval}')
                            print(f'data eval: {data[1]}')
                            print(f'calc eval of move self (max) ({move.initial_square.rank}, {move.initial_square.file}) to ({move.final_square.rank}, {move.final_square.file})')
                            # wie machen wir das mit der promotion????
                            board.ai_move(piece, move, self.promotion_pieces[0], True)
                            evaluation = self.minimax(board, depth - 1, alpha, beta, False, False, data)[1]
                            if save_move:
                                if not data[0]:
                                    data[0] = [piece, move, evaluation]
                                print(evaluation)
                                print(data[1])
                                if evaluation >= max_eval:
                                    if evaluation > data[0][2]:
                                        print('new data')
                                        data = [[], 0]
                                        data[1] = evaluation
                                        data[0] = [piece, move, evaluation]
                                    elif evaluation == data[0][2]:
                                        print('add data')
                                        data[0].append([piece, move, evaluation])
                            board.unmake_move(piece, move)
                            max_eval = max(max_eval, evaluation)

                            print(f'winning eval: {max_eval}')

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
                            print(' ')
                            print(player_color, depth)
                            print(f'current eval: {min_eval}')
                            print(f'data eval: {data[1]}')
                            print(f'calc eval of move enemy (min) ({move.initial_square.rank}, {move.initial_square.file}) to ({move.final_square.rank}, {move.final_square.file})')
                            board.ai_move(piece, move, self.promotion_pieces[0], True)
                            evaluation = self.minimax(board, depth - 1, alpha, beta, True, False, data)[1]
                            board.unmake_move(piece, move)

                            min_eval = min(min_eval, evaluation)

                            print(f'winning eval: {min_eval}')

                            beta = min(beta, evaluation)
                            if beta <= alpha:
                                break
            return data


