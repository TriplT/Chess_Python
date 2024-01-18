import random
import math
from Pycharm_Projects.Chess_Test.data.classes.board import *
from Pycharm_Projects.Chess_Test.data.classes.game import *


class AI:

    promotion_pieces = [Queen, Knight, Bishop, Rook]
    count_moves = 0
    test_moves = []
    resulting_moves = 0
    counter = -1

    def __init__(self, engine, difficulty, depth, color):
        self.engine = engine
        self.difficulty = difficulty
        self.depth = depth
        self.color = color

        self.squares_with_piece = []
        self.moves = []
        self.promotion_pieces = [Queen, Knight, Bishop, Rook]

        self.minimax_count = 0
        self.alpha_beta_pruning_count = 0
        self.max_pruning_count = 0
        self.min_pruning_count = 0

    def play_moves(self, board, engine='alea iacta est'):
        # print(board.evaluate_position(self.color))
        self.squares_with_piece = board.save_own_square_pieces(self.color)
        self.moves = Game.player_valid_moves

        if not self.squares_with_piece:
            exit(0)

        # engines
        def play_random():
            moves = board.get_valid_moves(self.color, self.color)
            move = random.choice(moves)

            board.move(board.squares[move.initial_square.rank][move.initial_square.file].piece, move, False)
            return

        def random_test_improved():
            # random_move = random.choice(board.get_valid_moves(self.color))
            move_list = []
            for random_move in board.get_valid_moves(self.color, self.color):
                move_list.append(random_move)

            random_move = random.choice(move_list)
            piece = board.squares[random_move.initial_square.rank][random_move.initial_square.file].piece
            board.move(piece, random_move, False)

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
                        board.move(piece, move, False)
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
                board.move(piece, move, False)

        def play_interstellar():
            evaluation, final_move = self.minimax_2(board, 3, -math.inf, math.inf, True)

            print(' ')
            print(f'minimax count: {self.minimax_count}')
            print(f'alpha beta pruning count: {self.alpha_beta_pruning_count}')
            print(f'max_player pruning count: {self.max_pruning_count}')
            print(f'min_player pruning count: {self.min_pruning_count}')
            print(' ')
            print(f'this is the final eval: {evaluation}')
            print(f'this is the final move: {final_move}')
            print(f'initial sq: ({final_move.initial_square.rank}, {final_move.initial_square.file}) final sq: ({final_move.final_square.rank}, {final_move.final_square.file})')

            piece = board.squares[final_move.initial_square.rank][final_move.initial_square.file].piece

            if final_move:
                board.move(piece, final_move, False)
                print(' ')
                print('AI MOVE PLAYED')
                print(' ')
            return True

        def play_interstellar_improved():
            evaluation, final_move = self.minimax_ascended(board, 4, -math.inf, math.inf, True)

            print(' ')
            print(f'minimax count: {self.minimax_count}')
            print(f'alpha beta pruning count: {self.alpha_beta_pruning_count}')
            print(f'max_player pruning count: {self.max_pruning_count}')
            print(f'min_player pruning count: {self.min_pruning_count}')
            print(' ')
            print(f'this is the final eval: {evaluation}')
            print(f'this is the final move: {board.squares[final_move.initial_square.rank][final_move.initial_square.file].piece.color} '
                  f'{board.squares[final_move.initial_square.rank][final_move.initial_square.file].piece.name} '
                  f'initial sq: ({final_move.initial_square.rank}, {final_move.initial_square.file}) '
                  f'final sq: ({final_move.final_square.rank}, {final_move.final_square.file})')

            piece = board.squares[final_move.initial_square.rank][final_move.initial_square.file].piece

            self.minimax_count = 0
            self.alpha_beta_pruning_count = 0
            self.max_pruning_count = 0
            self.min_pruning_count = 0

            if final_move:
                board.move(piece, final_move, False)
                print(' ')
                print('AI MOVE PLAYED')
                print(' ')
            if board.squares[2][2].occupied():
                print(f'{board.squares[2][2].piece.color} {board.squares[2][2].piece.name} on square 2, 2')
            return True

        def move_amount():
            for move in board.get_valid_moves(self.color, self.color):
                print(f'{board.squares[move.initial_square.rank][move.initial_square.file].piece.name} '
                      f'from ({move.initial_square.rank}, {move.initial_square.file}) '
                      f'to ({move.final_square.rank}, {move.final_square.file})')
            print(f'valid_moves: {len(board.get_valid_moves(self.color, self.color))}')
            while True:
                x = 349737

        def test_moves():
            def calc_moves(turn, depth):
                if depth == 0:

                    return

                if turn:
                    player_color = self.color
                else:
                    if self.color == 'white':
                        player_color = 'black'
                    else:
                        player_color = 'white'

                valid_moves = board.get_valid_moves(player_color, player_color)

                for move in valid_moves:
                    piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                    if depth == 2:
                        AI.resulting_moves = 0
                        AI.test_moves.append([0, piece, move])
                        AI.counter += 1
                    elif depth == 1:
                        AI.resulting_moves += 1
                        AI.count_moves += 1
                        AI.test_moves[AI.counter][0] = AI.resulting_moves

                    board.minimax_move(piece, move, True)
                    calc_moves(False, depth - 1) if turn else calc_moves(True, depth - 1)
                    board.unmake_move(piece, move)
                return

            calc_moves(True, 4)
            print(f'amount of starting possibilities: {len(AI.test_moves)}')
            count = 0
            for move in AI.test_moves:
                print(f'{move[1]} from ({move[2].initial_square.rank}, {move[2].initial_square.file}) '
                      f'to ({move[2].final_square.rank}, {move[2].final_square.file}) results in a total of {move[0]} positions')
                count += move[0]
            print(f'end result calculated moves: {count}')

            print(f'final moves calculated: {AI.count_moves}')
            while True:
                x = 2344

        # engine names
        if engine == 'amount':  # bug fix
            move_amount()

        if engine == 'test':  # bug fix
            test_moves()

        if engine == 'alea iacta est':  # plays random moves throughout the game
            play_random()

        if engine == 'random test':  # plays random moves throughout the game
            random_test_improved()

        if engine == 'ambitious promoter':  # tries to promote at every opportunity
            play_try_to_promote_pawns()

        if engine == 'berserk killer':  # tries to kill at every opportunity
            play_berserk_killer()

        if engine == 'interstellar calculator':  # best engine
            play_interstellar()

        if engine == 'i':  # best engine
            play_interstellar_improved()

        if engine == 'AI annihilator':  # best engine-like engine (or is it?)
            play_random()

    def minimax_ascended(self, board, depth, alpha, beta, max_player, best_move='000000000 error 00000000'):

        print(' ')
        print(f'depth: {depth}')
        if depth == 0:
            board.evaluate_position(self.color)
            print(f'evaluate position: {board.evaluation}')

        # ready up for next bug
        '''
        if board.squares[2][2].occupied():
            if isinstance(board.squares[2][2].piece, Knight) or board.played moves < 3 or isinstance(board.squares[2][2].piece, Pawn):
                print(f'{board.squares[2][2].piece.color} {board.squares[2][2].piece.name} on square 2, 2')
            else:
                exit(1)
        '''
        if depth == 0:
            board.evaluate_position(self.color)
            return board.evaluation, best_move

        if max_player:
            player_color = self.color
        else:
            if self.color == 'white':
                player_color = 'black'
            else:
                player_color = 'white'

        board.game_end_minimax(player_color)
        if board.ai_game_ended:
            board.ai_game_ended = False
            return board.evaluation, best_move

        valid_moves = board.get_valid_moves(player_color, self.color)
        if board.ai_game_ended:
            board.ai_game_ended = False
            return board.evaluation, best_move

        self.minimax_count += 1

        print(f'minimax: {self.minimax_count}')
        print(f'color: {player_color}')

        '''
        if depth == 3:
            for move in valid_moves:
                print(board.squares[move.initial_square.rank][move.initial_square.file].piece.color, board.squares[move.initial_square.rank][move.initial_square.file].piece.name)
                print(f'{move.initial_square.rank, move.initial_square.file} to {move.final_square.rank, move.final_square.file}')
        '''

        if max_player:
            max_eval = -math.inf
            max_move = -math.inf

            for move in valid_moves:
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                print('move')
                # print(piece.color, piece.name)
                print((move.initial_square.rank, move.initial_square.file),
                (move.final_square.rank, move.final_square.file))
                # this line is here for bug fixing. remove this and uncomment to one before
                print(piece.color, piece.name)

                board.minimax_move(piece, move)
                evaluation = self.minimax_ascended(board, depth - 1, alpha, beta, False)

                print('unmake move')
                print(piece.color, piece.name)
                print((move.initial_square.rank, move.initial_square.file),
                (move.final_square.rank, move.final_square.file))

                board.unmake_move(piece, move)

                max_eval = max(max_eval, evaluation[0])
                if max_eval > max_move:
                    max_move = max_eval
                    best_max_move = move

                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    self.alpha_beta_pruning_count += 1
                    self.max_pruning_count += 1
                    break
            return max_eval, best_max_move

        else:
            min_eval = math.inf
            min_move = math.inf

            for move in valid_moves:
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                print('move')
                print(piece.color, piece.name)
                print((move.initial_square.rank, move.initial_square.file),
                (move.final_square.rank, move.final_square.file))

                board.minimax_move(piece, move)
                evaluation = self.minimax_ascended(board, depth - 1, alpha, beta, True)

                print('unmake move')
                print(piece.color, piece.name)
                print((move.initial_square.rank, move.initial_square.file),
                (move.final_square.rank, move.final_square.file))

                board.unmake_move(piece, move)

                min_eval = min(min_eval, evaluation[0])
                if min_eval < min_move:
                    min_move = min_eval
                    best_min_move = move

                beta = min(beta, min_eval)
                if beta <= alpha:
                    self.alpha_beta_pruning_count += 1
                    self.min_pruning_count += 1
                    break
            return min_eval, best_min_move
    def minimax_improved_3(self, board, depth, alpha, beta, max_player, best_move='000000000 error 00000000'):

        print(' ')
        print(f'depth: {depth}')
        if depth == 0:
            board.evaluate_position(self.color)
            print(f'evaluate position: {board.evaluation}')

        # make ready for next bug
        '''
        if board.squares[2][2].occupied():
            if isinstance(board.squares[2][2].piece, Knight) or board.played moves < 3 or isinstance(board.squares[2][2].piece, Pawn):
                print(f'{board.squares[2][2].piece.color} {board.squares[2][2].piece.name} on square 2, 2')
            else:
                exit(1)
        '''
        if depth == 0:
            board.evaluate_position(self.color)
            return board.evaluation, best_move
        elif board.ai_game_ended:
            board.ai_game_ended = False
            return board.evaluation, best_move


        if max_player:
            player_color = self.color
        else:
            if self.color == 'white':
                player_color = 'black'
            else:
                player_color = 'white'

        self.minimax_count += 1

        print(f'minimax: {self.minimax_count}')
        print(f'color: {player_color}')

        valid_moves = board.get_valid_moves(player_color, self.color)

        '''
        if depth == 3:
            for move in valid_moves:
                print(board.squares[move.initial_square.rank][move.initial_square.file].piece.color, board.squares[move.initial_square.rank][move.initial_square.file].piece.name)
                print(f'{move.initial_square.rank, move.initial_square.file} to {move.final_square.rank, move.final_square.file}')
        '''
        board.game_end_minimax(player_color)

        if max_player:
            max_eval = -math.inf
            max_move = -math.inf

            for move in valid_moves:
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                print('move')
                # print(piece.color, piece.name)
                print((move.initial_square.rank, move.initial_square.file),
                (move.final_square.rank, move.final_square.file))
                # this line is here for bug fixing. remove this and uncomment to one before
                print(piece.color, piece.name)

                board.minimax_move(piece, move)
                evaluation = self.minimax_ascended(board, depth - 1, alpha, beta, False)

                print('unmake move')
                print(piece.color, piece.name)
                print((move.initial_square.rank, move.initial_square.file),
                (move.final_square.rank, move.final_square.file))

                board.unmake_move(piece, move)

                max_eval = max(max_eval, evaluation[0])
                if max_eval > max_move:
                    max_move = max_eval
                    best_max_move = move

                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    self.alpha_beta_pruning_count += 1
                    self.max_pruning_count += 1
                    break
            return max_eval, best_max_move

        else:
            min_eval = math.inf
            min_move = math.inf

            for move in valid_moves:
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                print('move')
                print(piece.color, piece.name)
                print((move.initial_square.rank, move.initial_square.file),
                (move.final_square.rank, move.final_square.file))

                board.minimax_move(piece, move)
                evaluation = self.minimax_ascended(board, depth - 1, alpha, beta, True)

                print('unmake move')
                print(piece.color, piece.name)
                print((move.initial_square.rank, move.initial_square.file),
                (move.final_square.rank, move.final_square.file))

                board.unmake_move(piece, move)

                min_eval = min(min_eval, evaluation[0])
                if min_eval < min_move:
                    min_move = min_eval
                    best_min_move = move

                beta = min(beta, min_eval)
                if beta <= alpha:
                    self.alpha_beta_pruning_count += 1
                    self.min_pruning_count += 1
                    break
            return min_eval, best_min_move

    def minimax_improved_2(self, board, depth, alpha, beta, max_player, best_move='000000000 error 00000000'):

        if max_player:
            player_color = self.color
        else:
            if self.color == 'white':
                player_color = 'black'
            else:
                player_color = 'white'

        self.minimax_count += 1

        # board.game_end still fucking slow
        if board.game_end_minimax(player_color, max_player):
            return board.evaluation, best_move
        elif depth == 0:
            board.evaluate_position(player_color)
            return board.evaluation, best_move

        if max_player:
            max_eval = -math.inf
            max_move = -math.inf

            for move in board.get_valid_moves(player_color, False, max_player):
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                board.minimax_move(piece, move, True)
                evaluation = self.minimax_improved_2(board, depth - 1, alpha, beta, False)
                board.unmake_move(piece, move)

                max_eval = max(max_eval, evaluation[0])
                if max_eval > max_move:
                    max_move = max_eval
                    best_max_move = move

                alpha = max(alpha, evaluation[0])
                if beta <= alpha:
                    self.alpha_beta_pruning_count += 1
                    self.max_pruning_count += 1
                    break
            return max_eval, best_max_move

        else:
            min_eval = math.inf
            min_move = math.inf

            for move in board.get_valid_moves(player_color, False, max_player):
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                board.minimax_move(piece, move, True)
                evaluation = self.minimax_improved_2(board, depth - 1, alpha, beta, True)
                board.unmake_move(piece, move)

                min_eval = min(min_eval, evaluation[0])
                if min_eval < min_move:
                    min_move = min_eval
                    best_min_move = move

                beta = min(beta, evaluation[0])
                if beta <= alpha:
                    self.alpha_beta_pruning_count += 1
                    self.min_pruning_count += 1
                    break
            return min_eval, best_min_move

    def minimax_improved(self, board, depth, alpha, beta, max_player, best_move='000000000 error 00000000'):

        if max_player:
            player_color = self.color
        else:
            if self.color == 'white':
                player_color = 'black'
            else:
                player_color = 'white'

        print(f'minimax initiated; player: {player_color}')
        self.minimax_count += 1

        if board.game_end_minimax(player_color, max_player):
            print(f'GAME ENDED; eval: {board.evaluation}, player: {player_color}, max_player: {max_player}')
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

            for move in board.get_valid_moves(player_color, False, max_player):
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                print(f'depth: {depth}')
                print(f'{player_color} move: {piece.name} to ({move.final_square.rank, move.final_square.file})')

                board.minimax_move(piece, move, True)
                evaluation = self.minimax_improved(board, depth - 1, alpha, beta, False)
                board.unmake_move(piece, move)

                max_eval = max(max_eval, evaluation[0])
                print(f'current best eval: {max_eval}')
                print('calculating if max eval is THE BEST ONE CALCULATED YET')
                if max_eval > max_move:
                    print(f'we have a new all around best eval: {max_eval} which means the new best move is:'
                          f' {move.initial_square.rank}, {move.initial_square.file} to {move.final_square.rank}, {move.final_square.file}')

                    max_move = max_eval
                    best_max_move = move

                alpha = max(alpha, evaluation[0])
                if beta <= alpha:
                    self.alpha_beta_pruning_count += 1
                    self.max_pruning_count += 1
                    break
            print(f'best outcome max_player ({player_color}): {max_eval} with move: '
                  f'{board.squares[best_max_move.initial_square.rank][best_max_move.initial_square.file].piece.name}'
                  f' from ({best_max_move.initial_square.rank, best_max_move.initial_square.file})'
                  f' to ({best_max_move.final_square.rank, best_max_move.final_square.file})')
            return max_eval, best_max_move

        else:
            min_eval = math.inf
            min_move = math.inf

            for move in board.get_valid_moves(player_color, False, max_player):
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                print(f'depth: {depth}')
                print(f'{player_color} move: {piece.name if piece.name else None} to ({move.final_square.rank, move.final_square.file})')

                board.minimax_move(piece, move, True)
                evaluation = self.minimax_improved(board, depth - 1, alpha, beta, True)
                board.unmake_move(piece, move)

                min_eval = min(min_eval, evaluation[0])
                if min_eval < min_move:
                    min_move = min_eval
                    best_min_move = move

                beta = min(beta, evaluation[0])
                if beta <= alpha:
                    self.alpha_beta_pruning_count += 1
                    self.min_pruning_count += 1
                    break
            print(f'best outcome min_player ({player_color}): {min_eval} with move: '
                  f'{board.squares[best_min_move.initial_square.rank][best_min_move.initial_square.file].piece.name}'
                  f' from ({best_min_move.initial_square.rank, best_min_move.initial_square.file})'
                  f' to ({best_min_move.final_square.rank, best_min_move.final_square.file})')
            return min_eval, best_min_move

    def minimax(self, board, depth, alpha, beta, max_player, best_move='000000000 error 00000000'):

        if max_player:
            player_color = self.color
        else:
            if self.color == 'white':
                player_color = 'black'
            else:
                player_color = 'white'

        print(f'minimax initiated; player: {player_color}')
        self.minimax_count += 1

        if board.game_end_minimax(player_color, max_player):
            print(f'GAME ENDED; eval: {board.evaluation}, player: {player_color}, max_player: {max_player}')
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

                board.minimax_move(piece, move, True)
                evaluation = self.minimax(board, depth - 1, alpha, beta, False)
                board.unmake_move(piece, move)

                max_eval = max(max_eval, evaluation[0])
                print(f'current best eval: {max_eval}')
                print('calculating if max eval is THE BEST ONE CALCULATED YET')
                if max_eval > max_move:
                    print(f'we have a new all around best eval: {max_eval} which means the new best move is:'
                          f' {move.initial_square.rank}, {move.initial_square.file} to {move.final_square.rank}, {move.final_square.file}')

                    max_move = max_eval
                    best_max_move = move

                alpha = max(alpha, evaluation[0])
                if beta <= alpha:
                    self.alpha_beta_pruning_count += 1
                    self.max_pruning_count += 1
                    break
            print(f'best outcome max_player ({player_color}): {max_eval} with move: '
                  f'{board.squares[best_max_move.initial_square.rank][best_max_move.initial_square.file].piece.name}'
                  f' from ({best_max_move.initial_square.rank, best_max_move.initial_square.file})'
                  f' to ({best_max_move.final_square.rank, best_max_move.final_square.file})')
            return max_eval, best_max_move

        else:
            min_eval = math.inf
            min_move = math.inf

            for move in board.calculate_all_valid_moves(player_color):
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                print(f'depth: {depth}')
                print(f'{player_color} move: {piece.name if piece.name else None} to ({move.final_square.rank, move.final_square.file})')

                board.minimax_move(piece, move, True)
                evaluation = self.minimax(board, depth - 1, alpha, beta, True)
                board.unmake_move(piece, move)

                min_eval = min(min_eval, evaluation[0])
                if min_eval < min_move:
                    min_move = min_eval
                    best_min_move = move

                beta = min(beta, evaluation[0])
                if beta <= alpha:
                    self.alpha_beta_pruning_count += 1
                    self.min_pruning_count += 1
                    break
            print(f'best outcome min_player ({player_color}): {min_eval} with move: '
                  f'{board.squares[best_min_move.initial_square.rank][best_min_move.initial_square.file].piece.name}'
                  f' from ({best_min_move.initial_square.rank, best_min_move.initial_square.file})'
                  f' to ({best_min_move.final_square.rank, best_min_move.final_square.file})')
            return min_eval, best_min_move

    def minimax_2(self, board, depth, alpha, beta, max_player, best_move='000000000 error 00000000'):

        if max_player:
            player_color = self.color
        else:
            if self.color == 'white':
                player_color = 'black'
            else:
                player_color = 'white'

        self.minimax_count += 1

        if board.game_end_minimax(player_color, max_player):
            return board.evaluation, best_move
        elif depth == 0:
            board.evaluate_position(player_color)
            return board.evaluation, best_move

        if max_player:
            max_eval = -math.inf
            max_move = -math.inf

            for move in board.calculate_all_valid_moves(player_color):
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                board.minimax_move(piece, move, True)
                evaluation = self.minimax_2(board, depth - 1, alpha, beta, False)
                board.unmake_move(piece, move)

                max_eval = max(max_eval, evaluation[0])
                if max_eval > max_move:
                    max_move = max_eval
                    best_max_move = move

                alpha = max(alpha, evaluation[0])
                if beta <= alpha:
                    self.alpha_beta_pruning_count += 1
                    self.max_pruning_count += 1
                    break
            return max_eval, best_max_move

        else:
            min_eval = math.inf
            min_move = math.inf

            for move in board.calculate_all_valid_moves(player_color):
                piece = board.squares[move.initial_square.rank][move.initial_square.file].piece

                board.minimax_move(piece, move, True)
                evaluation = self.minimax_2(board, depth - 1, alpha, beta, True)
                board.unmake_move(piece, move)

                min_eval = min(min_eval, evaluation[0])
                if min_eval < min_move:
                    min_move = min_eval
                    best_min_move = move

                beta = min(beta, evaluation[0])
                if beta <= alpha:
                    self.alpha_beta_pruning_count += 1
                    self.min_pruning_count += 1
                    break
            return min_eval, best_min_move



