import copy
import math

import pygame
from Pycharm_Projects.Chess_Test.data.global_variables import *
from Pycharm_Projects.Chess_Test.data.classes.piece import Piece
from Pycharm_Projects.Chess_Test.data.classes.pieces.pawn import Pawn
from Pycharm_Projects.Chess_Test.data.classes.pieces.king import King
from Pycharm_Projects.Chess_Test.data.classes.pieces.knight import Knight
from Pycharm_Projects.Chess_Test.data.classes.pieces.bishop import Bishop
from Pycharm_Projects.Chess_Test.data.classes.pieces.rook import Rook
from Pycharm_Projects.Chess_Test.data.classes.pieces.queen import Queen
from Pycharm_Projects.Chess_Test.data.classes.square import *
from Pycharm_Projects.Chess_Test.data.global_variables import *
from Pycharm_Projects.Chess_Test.data.classes.move import Move
from Pycharm_Projects.Chess_Test.data.classes.game import *


class Board:
    last_eaten_piece = []

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for rank in range(ranks)]
        self.move_played = False
        self.move_counter = 0  # 50 move-rule
        self.last_num_of_pieces = 0  # 50 move-rule
        self.last_move = None
        self.last_white_move = None
        self.last_black_move = None
        self.repetition_counter = 0
        self.last_piece = None
        self.win_message = False
        self.evaluation = None
        self.game_ended = False
        self.current_moves = []
        self.create_squares()
        self.add_startposition('white')
        self.add_startposition('black')
        self.save_number_of_pieces()

    def create_squares(self):
        for rank in range(ranks):
            for file in range(files):
                self.squares[rank][file] = Square(rank, file)

    def calc_current_moves(self, piece=None):
        if piece:
            self.current_moves = piece.moves

        if not piece:
            self.current_moves = []

    def player_move(self, piece, move, game=None):

        self.squares[move.initial_square.rank][move.initial_square.file].piece = None
        self.squares[move.final_square.rank][move.final_square.file].piece = piece

        if isinstance(piece, Pawn):
            self.en_passant(piece, move, self.last_move)
            self.player_pawn_promotion(screen, piece, move.final_square, game)

        if isinstance(piece, King):
            if self.castling(move.initial_square, move.final_square):
                diff = move.final_square.file - move.initial_square.file
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.player_move(rook, rook.moves[-1])

        self.move_played = True
        piece.moved = True
        piece.clear_moves()
        self.current_moves = []
        self.move_counter += 1

        self.last_piece = piece
        self.last_move = move

        # move repetition
        if piece.color == 'white':
            if (self.last_black_move and move.initial_square == self.last_white_move.final_square
                    and move.final_square == self.last_white_move.initial_square):
                self.repetition_counter += 1
            else:
                self.repetition_counter = 0

            self.last_white_move = move

        elif piece.color == 'black':
            if (self.last_black_move and move.initial_square == self.last_black_move.final_square
                    and move.final_square == self.last_black_move.initial_square):
                self.repetition_counter += 1
            else:
                self.repetition_counter = 0

            self.last_black_move = move
        else:
            print('unexpected error, piece.color not white or black')

    def ai_move(self, piece, move, promotion_piece=None, set_history=False):
        if set_history:
            last_piece = self.squares[move.final_square.rank][move.final_square.file].piece
            self.save_last_eaten_piece(last_piece)

        self.squares[move.initial_square.rank][move.initial_square.file].piece = None
        self.squares[move.final_square.rank][move.final_square.file].piece = piece

        if isinstance(piece, Pawn):
            self.en_passant(piece, move, self.last_move)
            self.ai_pawn_promotion(piece, move.final_square, promotion_piece)

        if isinstance(piece, King):
            if self.castling(move.initial_square, move.final_square):
                diff = move.final_square.file - move.initial_square.file
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.ai_move(rook, rook.moves[-1])

        self.move_played = True
        piece.moved = True
        piece.clear_moves()
        self.current_moves = []
        self.move_counter += 1

        self.last_piece = piece
        self.last_move = move

        # move repetition
        if piece.color == 'white':
            if (self.last_black_move and move.initial_square == self.last_white_move.final_square
                    and move.final_square == self.last_white_move.initial_square):
                self.repetition_counter += 1
            else:
                self.repetition_counter = 0

            self.last_white_move = move

        elif piece.color == 'black':
            if (self.last_black_move and move.initial_square == self.last_black_move.final_square
                    and move.final_square == self.last_black_move.initial_square):
                self.repetition_counter += 1
            else:
                self.repetition_counter = 0

            self.last_black_move = move
        else:
            print('unexpected error, piece.color not white or black')

    def ai_move_simulation(self, piece, move, promotion_piece=None, set_history=False):
        if set_history:
            last_piece = self.squares[move.final_square.rank][move.final_square.file].piece
            self.save_last_eaten_piece(last_piece)

        self.squares[move.initial_square.rank][move.initial_square.file].piece = None
        self.squares[move.final_square.rank][move.final_square.file].piece = piece

        if isinstance(piece, Pawn):
            self.en_passant(piece, move, self.last_move)
            self.ai_pawn_promotion(piece, move.final_square, promotion_piece)

        if isinstance(piece, King):
            if self.castling(move.initial_square, move.final_square):
                diff = move.final_square.file - move.initial_square.file
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.ai_move(rook, rook.moves[-1])

        self.move_played = True
        piece.moved = True
        piece.clear_moves()

    def save_last_eaten_piece(self, piece):
        # piece.moved ???
        self.last_eaten_piece.append(piece)

    def get_last_eaten_piece(self):
        return self.last_eaten_piece.pop()

    def unmake_move(self, piece, move):
        last_eaten_piece = self.get_last_eaten_piece()

        self.squares[move.initial_square.rank][move.initial_square.file].piece = piece
        if last_eaten_piece:
            self.squares[move.final_square.rank][move.final_square.file].piece = last_eaten_piece
        else:
            self.squares[move.final_square.rank][move.final_square.file].piece = None

        if isinstance(piece, Pawn):
            if move.final_square.rank - move.initial_square.rank == 2:
                piece.moved = False


    @staticmethod
    def valid_move(piece, move):
        return move in piece.moves

    def valid_current_move(self, move):
        return move in self.current_moves

    @staticmethod
    def castling(initial, final):
        return abs(initial.file - final.file) == 2

    def ai_pawn_promotion(self, piece, last, promotion_piece):
        if isinstance(piece, Pawn) and (last.rank == 0 or last.rank == 7):
            self.squares[last.rank][last.file].piece = promotion_piece(piece.color)

    def player_pawn_promotion(self, screen, piece, last, game):
        if isinstance(piece, Pawn) and (last.rank == 0 or last.rank == 7):
            # create border
            color = (255, 255, 255)
            pygame.draw.rect(screen, color,
                             pygame.Rect((screen_x / 2 - 120, screen_y / 2 - 120),
                                         (2 * square_size + 40, 2 * square_size + 40)))

            # create piece images
            piece_queen_image = Piece.piece_images[f'{piece.color}_queen']
            piece_rook_image = Piece.piece_images[f'{piece.color}_rook']
            piece_bishop_image = Piece.piece_images[f'{piece.color}_bishop']
            piece_knight_image = Piece.piece_images[f'{piece.color}_knight']

            variables = [((screen_x / 2 - 50), (screen_y / 2 - 50)),
                         ((screen_x / 2 + 50), (screen_y / 2 - 50)),
                         ((screen_x / 2 - 50), (screen_y / 2 + 50)),
                         ((screen_x / 2 + 50), (screen_y / 2 + 50))]

            screen.blit(piece_queen_image, piece_queen_image.get_rect(center=variables[0]))
            screen.blit(piece_rook_image, piece_rook_image.get_rect(center=variables[1]))
            screen.blit(piece_bishop_image, piece_bishop_image.get_rect(center=variables[2]))
            screen.blit(piece_knight_image, piece_knight_image.get_rect(center=variables[3]))
            game.draw_game_mode_buttons(screen, 350, 120)
            pygame.display.flip()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        if (screen_x / 2 - 95) < x < (screen_x / 2 + - 5) and (screen_y / 2 - 95) < y < (
                                screen_y / 2 - 5):
                            self.squares[last.rank][last.file].piece = Queen(piece.color)
                            return
                        elif (screen_x / 2 + 5) < x < (screen_x / 2 + 95) and (screen_y / 2 - 95) < y < (
                                screen_y / 2 + - 5):
                            self.squares[last.rank][last.file].piece = Rook(piece.color)
                            return
                        elif (screen_x / 2 - 95) < x < (screen_x / 2 - 5) and (screen_y / 2 + 5) < y < (
                                screen_y / 2 + 95):
                            self.squares[last.rank][last.file].piece = Bishop(piece.color)
                            return
                        elif (screen_x / 2 + 5) < x < (screen_x / 2 + 95) and (screen_y / 2 + 5) < y < (
                                screen_y / 2 + 95):
                            self.squares[last.rank][last.file].piece = Knight(piece.color)
                            return

    def en_passant(self, piece, move, last_move):
        if piece.en_passant and move.final_square.file == last_move.final_square.file:
            self.squares[last_move.final_square.rank][last_move.final_square.file].piece = None
            piece.en_passant = False

    def in_check(self, piece, move):
        final_pos_piece = self.squares[move.final_square.rank][move.final_square.file].piece

        self.squares[move.initial_square.rank][move.initial_square.file].piece = None
        self.squares[move.final_square.rank][move.final_square.file].piece = piece

        for rank in range(ranks):
            for file in range(files):
                if self.squares[rank][file].occupied_by_opponent(piece.color):
                    p = self.squares[rank][file].piece
                    self.calculate_valid_moves(p, rank, file, bool=False)

                    for m in p.moves:
                        if isinstance(self.squares[m.final_square.rank][m.final_square.file].piece, King):
                            self.squares[move.initial_square.rank][move.initial_square.file].piece = piece
                            self.squares[move.final_square.rank][move.final_square.file].piece = final_pos_piece
                            p.moves = []
                            return True
                    p.moves = []

        self.squares[move.initial_square.rank][move.initial_square.file].piece = piece
        self.squares[move.final_square.rank][move.final_square.file].piece = final_pos_piece
        return False

    def calculate_valid_moves(self, piece, rank, file, bool):

        def pawn_moves():
            steps = 1 if piece.moved else 2

            # vertical moves
            start = rank + piece.direction
            end = rank + (piece.direction * steps)

            for possible_move_rank in range(start, end + piece.direction, piece.direction):
                if Square.in_range(possible_move_rank):
                    if self.squares[possible_move_rank][file].occupied_by_noone():
                        initial_pos = Square(rank, file)
                        final_pos = Square(possible_move_rank, file)
                        move = Move(initial_pos, final_pos)

                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

                    # pawn is blocked by piece
                    else:
                        break
                # move is not in range
                else:
                    break

            # diagonal moves
            possible_move_rank = rank + piece.direction
            possible_move_files = [file - 1, file + 1]

            for possible_move_file in possible_move_files:
                if Square.in_range(possible_move_rank, possible_move_file):
                    if self.squares[possible_move_rank][possible_move_file].occupied_by_opponent(piece.color):
                        initial_pos = Square(rank, file)
                        final_piece = self.squares[possible_move_rank][possible_move_file].piece
                        final_pos = Square(possible_move_rank, possible_move_file, final_piece)
                        move = Move(initial_pos, final_pos)

                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            if self.last_move is not None:
                last_initial = self.last_move.initial_square
                last_final = self.last_move.final_square

                if isinstance(self.last_piece, Pawn):
                    if abs(last_final.rank - last_initial.rank) > 1 and last_final.rank == rank:
                        for possible_move_file in possible_move_files:
                            if Square.in_range(possible_move_rank, possible_move_file):
                                if self.squares[rank][possible_move_file].piece == self.last_piece:
                                    initial_pos = Square(rank, file)
                                    final_piece = self.squares[possible_move_rank][possible_move_file].piece
                                    final_pos = Square(possible_move_rank, possible_move_file, final_piece)
                                    move = Move(initial_pos, final_pos)

                                    if bool:
                                        if not self.in_check(piece, move):
                                            piece.add_move(move)
                                            piece.en_passant = True
                                    else:
                                        piece.add_move(move)
                                        piece.en_passant = True

        def knight_moves():
            possible_moves = [
                (rank - 2, file + 1),
                (rank - 1, file + 2),
                (rank + 1, file + 2),
                (rank + 2, file + 1),
                (rank + 2, file - 1),
                (rank + 1, file - 2),
                (rank - 1, file - 2),
                (rank - 2, file - 1)
            ]

            for move in possible_moves:
                move_rank, move_file = move

                if Square.in_range(move_rank, move_file):
                    if self.squares[move_rank][move_file].no_friendly_fire(piece.color):
                        final_piece = self.squares[move_rank][move_file].piece
                        move = Move(Square(rank, file), Square(move_rank, move_file, final_piece))
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)

        def strait_line_moves(increments):
            for increment in increments:
                rank_inc, file_inc = increment
                possible_move_rank = rank + rank_inc
                possible_move_file = file + file_inc

                while True:
                    if Square.in_range(possible_move_rank, possible_move_file):
                        initial = Square(rank, file)
                        final_piece = self.squares[possible_move_rank][possible_move_file].piece
                        final = Square(possible_move_rank, possible_move_file, final_piece)
                        move = Move(initial, final)
                        if self.squares[possible_move_rank][possible_move_file].occupied_by_noone():
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                        elif self.squares[possible_move_rank][possible_move_file].occupied_by_opponent(piece.color):
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break
                        elif self.squares[possible_move_rank][possible_move_file].occupied_by_teammate(piece.color):
                            break
                    else:
                        break

                    possible_move_rank = possible_move_rank + rank_inc
                    possible_move_file = possible_move_file + file_inc

        def king_moves():
            moves = [
                (rank - 1, file - 1),
                (rank - 1, file + 0),
                (rank - 1, file + 1),
                (rank + 1, file - 1),
                (rank + 1, file + 0),
                (rank + 1, file + 1),
                (rank + 0, file - 1),
                (rank + 0, file + 1),
            ]

            for move in moves:
                possible_move_rank, possible_move_file = move
                if Square.in_range(possible_move_rank, possible_move_file):
                    if self.squares[possible_move_rank][possible_move_file].no_friendly_fire(piece.color):

                        initial = Square(rank, file)
                        final = Square(possible_move_rank, possible_move_file)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):

                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            if not piece.moved:
                left_rook = self.squares[rank][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[rank][c].occupied():
                                break
                            if c == 3:
                                piece.left_rook = left_rook

                                initial = Square(rank, 0)
                                final = Square(rank, 3)
                                move_rook = Move(initial, final)

                                initial = Square(rank, file)
                                final = Square(rank, 2)
                                move_king = Move(initial, final)

                                # move to check whether the king moves through check when castling
                                between_move = Move(Square(rank, 3), Square(rank, 3))

                                if bool:
                                    if not self.in_check(piece, move_king) and not self.in_check(piece, between_move):
                                        left_rook.add_move(move_rook)
                                        piece.add_move(move_king)
                                else:
                                    left_rook.add_move(move_rook)
                                    piece.add_move(move_king)

                right_rook = self.squares[rank][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.squares[rank][c].occupied():
                                break
                            if c == 6:
                                piece.right_rook = right_rook

                                initial = Square(rank, 7)
                                final = Square(rank, 5)
                                move_rook = Move(initial, final)

                                initial = Square(rank, file)
                                final = Square(rank, 6)
                                move_king = Move(initial, final)

                                between_move = Move(Square(rank, 5), Square(rank, 5))

                                if bool:
                                    if not self.in_check(piece, move_king) and not self.in_check(piece, between_move):
                                        right_rook.add_move(move_rook)
                                        piece.add_move(move_king)
                                else:
                                    right_rook.add_move(move_rook)
                                    piece.add_move(move_king)

        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, King):
            king_moves()
        elif isinstance(piece, Queen):
            strait_line_moves([
                (-1, 1),
                (-1, -1),
                (1, -1),
                (1, 1),
                (-1, 0),
                (0, 1),
                (0, -1),
                (1, 0)
            ])
        elif isinstance(piece, Bishop):
            strait_line_moves([
                (-1, 1),
                (-1, -1),
                (1, -1),
                (1, 1)
            ])
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Rook):
            strait_line_moves([
                (-1, 0),
                (0, 1),
                (0, -1),
                (1, 0)])

    def calculate_all_valid_moves(self, color):
        valid_moves = []

        def pawn_moves():
            steps = 1 if piece.moved else 2

            # vertical moves
            start = rank + piece.direction
            end = rank + (piece.direction * steps)

            for possible_move_rank in range(start, end + piece.direction, piece.direction):
                if Square.in_range(possible_move_rank):
                    if self.squares[possible_move_rank][file].occupied_by_noone():
                        initial_pos = Square(rank, file)
                        final_pos = Square(possible_move_rank, file)
                        move = Move(initial_pos, final_pos)

                        # pawn promotion für ai

                        if not self.in_check(piece, move):
                            valid_moves.append(move)

                    # pawn is blocked by piece
                    else:
                        break
                # move is not in range
                else:
                    break

            # diagonal moves
            possible_move_rank = rank + piece.direction
            possible_move_files = [file - 1, file + 1]

            for possible_move_file in possible_move_files:
                if Square.in_range(possible_move_rank, possible_move_file):
                    if self.squares[possible_move_rank][possible_move_file].occupied_by_opponent(piece.color):
                        initial_pos = Square(rank, file)
                        final_piece = self.squares[possible_move_rank][possible_move_file].piece
                        final_pos = Square(possible_move_rank, possible_move_file, final_piece)
                        move = Move(initial_pos, final_pos)

                        if not self.in_check(piece, move):
                            valid_moves.append(move)

            if self.last_move is not None:
                last_initial = self.last_move.initial_square
                last_final = self.last_move.final_square

                if isinstance(self.last_piece, Pawn):
                    if abs(last_final.rank - last_initial.rank) > 1 and last_final.rank == rank:
                        for possible_move_file in possible_move_files:
                            if Square.in_range(possible_move_rank, possible_move_file):
                                if self.squares[rank][possible_move_file].piece == self.last_piece:
                                    initial_pos = Square(rank, file)
                                    final_piece = self.squares[possible_move_rank][possible_move_file].piece
                                    final_pos = Square(possible_move_rank, possible_move_file, final_piece)
                                    move = Move(initial_pos, final_pos)

                                    if not self.in_check(piece, move):
                                        valid_moves.append(move)
                                        piece.en_passant = True

        def knight_moves():
            possible_moves = [
                (rank - 2, file + 1),
                (rank - 1, file + 2),
                (rank + 1, file + 2),
                (rank + 2, file + 1),
                (rank + 2, file - 1),
                (rank + 1, file - 2),
                (rank - 1, file - 2),
                (rank - 2, file - 1)
            ]

            for move in possible_moves:
                move_rank, move_file = move

                if Square.in_range(move_rank, move_file):
                    if self.squares[move_rank][move_file].no_friendly_fire(piece.color):
                        final_piece = self.squares[move_rank][move_file].piece
                        move = Move(Square(rank, file), Square(move_rank, move_file, final_piece))
                        if not self.in_check(piece, move):
                            valid_moves.append(move)
                        else:
                            break

        def strait_line_moves(increments):
            for increment in increments:
                rank_inc, file_inc = increment
                possible_move_rank = rank + rank_inc
                possible_move_file = file + file_inc

                while True:
                    if Square.in_range(possible_move_rank, possible_move_file):

                        initial = Square(rank, file)
                        final_piece = self.squares[possible_move_rank][possible_move_file].piece
                        final = Square(possible_move_rank, possible_move_file, final_piece)
                        move = Move(initial, final)

                        if self.squares[possible_move_rank][possible_move_file].occupied_by_noone():
                            if not self.in_check(piece, move):
                                valid_moves.append(move)
                        elif self.squares[possible_move_rank][possible_move_file].occupied_by_opponent(piece.color):
                            if not self.in_check(piece, move):
                                valid_moves.append(move)
                            break
                        elif self.squares[possible_move_rank][possible_move_file].occupied_by_teammate(piece.color):
                            break
                    else:
                        break

                    possible_move_rank = possible_move_rank + rank_inc
                    possible_move_file = possible_move_file + file_inc

        def king_moves():
            moves = [
                (rank - 1, file - 1),
                (rank - 1, file + 0),
                (rank - 1, file + 1),
                (rank + 1, file - 1),
                (rank + 1, file + 0),
                (rank + 1, file + 1),
                (rank + 0, file - 1),
                (rank + 0, file + 1),
            ]

            for move in moves:
                possible_move_rank, possible_move_file = move
                if Square.in_range(possible_move_rank, possible_move_file):
                    if self.squares[possible_move_rank][possible_move_file].no_friendly_fire(piece.color):

                        initial = Square(rank, file)
                        final = Square(possible_move_rank, possible_move_file)
                        move = Move(initial, final)

                        if not self.in_check(piece, move):
                            valid_moves.append(move)

            if not piece.moved:
                left_rook = self.squares[rank][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[rank][c].occupied():
                                break
                            if c == 3:
                                piece.left_rook = left_rook

                                initial = Square(rank, 0)
                                final = Square(rank, 3)
                                move_rook = Move(initial, final)

                                initial = Square(rank, file)
                                final = Square(rank, 2)
                                move_king = Move(initial, final)

                                # move to check whether the king moves through check when castling
                                between_move = Move(Square(rank, 3), Square(rank, 3))

                                if not self.in_check(piece, move_king) and not self.in_check(piece, between_move):
                                    left_rook.add_move(move_rook)
                                    valid_moves.append(move_king)

                right_rook = self.squares[rank][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.squares[rank][c].occupied():
                                break
                            if c == 6:
                                piece.right_rook = right_rook

                                initial = Square(rank, 7)
                                final = Square(rank, 5)
                                move_rook = Move(initial, final)

                                initial = Square(rank, file)
                                final = Square(rank, 6)
                                move_king = Move(initial, final)

                                between_move = Move(Square(rank, 5), Square(rank, 5))

                                if not self.in_check(piece, move_king) and not self.in_check(piece, between_move):
                                    right_rook.add_move(move_rook)
                                    valid_moves.append(move_king)

        for rank in range(ranks):
            for file in range(files):
                if self.squares[rank][file].occupied_by_teammate(color):
                    piece = self.squares[rank][file].piece

                    if isinstance(piece, Pawn):
                        pawn_moves()
                    elif isinstance(piece, King):
                        king_moves()
                    elif isinstance(piece, Queen):
                        strait_line_moves([
                            (-1, 1),
                            (-1, -1),
                            (1, -1),
                            (1, 1),
                            (-1, 0),
                            (0, 1),
                            (0, -1),
                            (1, 0)
                        ])
                    elif isinstance(piece, Bishop):
                        strait_line_moves([
                            (-1, 1),
                            (-1, -1),
                            (1, -1),
                            (1, 1)
                        ])
                    elif isinstance(piece, Knight):
                        knight_moves()
                    elif isinstance(piece, Rook):
                        strait_line_moves([
                            (-1, 0),
                            (0, 1),
                            (0, -1),
                            (1, 0)])
        return valid_moves

    def check_game_end(self, color, max_player):
        checkmate = False
        stalemate = True
        piece_list = []
        insufficient_material = False

        for rank in range(ranks):
            for file in range(files):

                p = self.squares[rank][file].piece
                if self.squares[rank][file].occupied():
                    piece_list.append(p)

                # checkmate and stalemate
                if self.squares[rank][file].occupied_by_teammate(color):
                    self.calculate_valid_moves(p, rank, file, bool=True)
                    if p.moves:
                        stalemate = False
                    p.moves = []

                if self.squares[rank][file].occupied_by_opponent(color):
                    self.calculate_valid_moves(p, rank, file, bool=True)
                    for move in p.moves:
                        if isinstance(self.squares[move.final_square.rank][move.final_square.file].piece, King):
                            checkmate = True

        knight_counter = 0
        bishop_counter = 0

        if len(piece_list) == 2:
            insufficient_material = True
        elif len(piece_list) == 3:
            for piece in piece_list:
                if isinstance(piece, Bishop) or isinstance(piece, Knight):
                    insufficient_material = True
        elif len(piece_list) == 4:
            for piece in piece_list:
                if isinstance(piece, Knight):
                    knight_counter += 1
                elif isinstance(piece, Bishop):
                    bishop_counter += 1
                    color = piece.color
                    if bishop_counter == 2 and not color == piece.color:
                        insufficient_material = True
            if knight_counter == 2 or (bishop_counter == 1 and knight_counter == 1):
                insufficient_material = True

        if len(piece_list) != self.last_num_of_pieces:
            self.last_num_of_pieces = len(piece_list)
            self.move_counter = 0

        if checkmate:
            print('CHECKMATE')
            self.evaluation = -math.inf if max_player else math.inf
            return True
        elif insufficient_material:
            self.evaluation = 0.0
            return True
        elif self.repetition_counter == 4:
            self.evaluation = 0.0
            return True
        elif self.move_counter == 50:
            self.evaluation = 0.0
            return True
        elif stalemate:
            print('ghghghghgh')
            self.evaluation = 0.0
            return True

        return False

    def game_end(self, color):
        # stalemate
        checkmate = False
        stalemate = True
        piece_list = []
        insufficient_material = False

        for rank in range(ranks):
            for file in range(files):

                p = self.squares[rank][file].piece
                if self.squares[rank][file].occupied():
                    piece_list.append(p)

                # checkmate and stalemate
                if self.squares[rank][file].occupied_by_teammate(color):
                    self.calculate_valid_moves(p, rank, file, bool=True)
                    if p.moves:
                        stalemate = False
                    p.moves = []
                if self.squares[rank][file].occupied_by_opponent(color):
                    self.calculate_valid_moves(p, rank, file, bool=True)
                    for move in p.moves:
                        if isinstance(move.final_square.piece, King):
                            checkmate = True
                    p.moves = []

        # insufficient material
        knight_counter = 0
        bishop_counter = 0
        # king vs king
        if len(piece_list) == 2:
            insufficient_material = True
        elif len(piece_list) == 3:
            for piece in piece_list:
                if isinstance(piece, Bishop) or isinstance(piece, Knight):
                    insufficient_material = True
        elif len(piece_list) == 4:
            for piece in piece_list:
                if isinstance(piece, Knight):
                    knight_counter += 1
                elif isinstance(piece, Bishop):
                    bishop_counter += 1
                    color = piece.color
                    if bishop_counter == 2 and not color == piece.color:
                        insufficient_material = True
            if knight_counter == 2 or (bishop_counter == 1 and knight_counter == 1):
                insufficient_material = True

        # 50 move-rule
        if len(piece_list) != self.last_num_of_pieces:
            self.last_num_of_pieces = len(piece_list)
            self.move_counter = 0

        if insufficient_material:
            self.game_ended = True
            self.win_message = 'insufficient material'
        elif self.repetition_counter == 4:
            self.game_ended = True
            self.win_message = 'repetition'
        elif self.move_counter == 50:
            self.game_ended = True
            self.win_message = '50 move-rule'
        elif stalemate and checkmate:
            self.game_ended = True
            self.win_message = 'checkmate'
        elif stalemate:
            self.game_ended = True
            self.win_message = 'stalemate'

        self.move_played = False

    def reset_board(self):
        for rank in range(ranks):
            for file in range(files):
                self.squares[rank][file].piece = None
        self.current_moves = []
        self.last_move = None
        self.move_played = False
        self.win_message = False
        self.game_ended = False

    def save_own_square_pieces(self, color):
        lst = []
        for rank in range(ranks):
            for file in range(files):
                if self.squares[rank][file].occupied_by_teammate(color):
                    lst.append(self.squares[rank][file])
        return lst

    def save_all_pieces(self):
        lst = []
        for rank in range(ranks):
            for file in range(files):
                if self.squares[rank][file].occupied():
                    lst.append(self.squares[rank][file].piece)
        return lst

    def save_number_of_pieces(self):
        counter = 0
        for rank in range(ranks):
            for file in range(files):
                if self.squares[rank][file].piece:
                    counter += 1
        self.last_num_of_pieces = counter

    def get_moves(self, color):
        lst = []
        for rank in range(ranks):
            for file in range(files):
                if self.squares[rank][file].occupied_by_teammate(color):
                    piece = self.squares[rank][file].piece
                    self.calculate_valid_moves(piece, rank, file, bool=True)
                    for move in piece.moves:
                        lst.append(move)
        return lst

    def get_movess(self, color):
        lst = []
        for rank in range(ranks):
            for file in range(files):
                if self.squares[rank][file].occupied_by_teammate(color):

                    piece = self.squares[rank][file].piece
                    self.calculate_valid_moves(piece, rank, file, bool=True)

                    for move in piece.moves:
                        lst.append(move)
        return lst

    def evaluate_position(self, color):
        pieces = self.save_all_pieces()
        position_value = 0
        for piece in pieces:
            position_value += piece.value

        if color == 'white':
            self.evaluation = round(position_value, 3)
        else:
            self.evaluation = -round(position_value, 3)

    def add_startposition(self, color):
        # check_stale_and_checkmate

        if color == 'white':
            self.squares[7][7] = Square(7, 7, Rook(color))

            # self.squares[3][2] = Square(3, 2, Pawn(color))

            self.squares[2][1] = Square(2, 1, King(color))

        if color == 'black':
            self.squares[0][0] = Square(0, 0, King(color))

    def add_startpositio(self, color):

        if color == 'white':
            self.squares[2][0] = Square(2, 0, Knight(color))

            self.squares[5][0] = Square(5, 0, Pawn(color))

            self.squares[1][3] = Square(1, 3, Pawn(color))
            self.squares[2][3] = Square(2, 3, Pawn(color))
            self.squares[3][3] = Square(3, 3, Pawn(color))
            # self.squares[3][2] = Square(3, 2, Pawn(color))

            self.squares[2][2] = Square(2, 2, King(color))

        if color == 'black':
            self.squares[4][0] = Square(4, 0, Pawn(color))

            self.squares[0][3] = Square(0, 3, Pawn(color))

            self.squares[0][0] = Square(0, 0, King(color))


    def add_startpositio(self, color):
        if color == 'white':
            rank_pawn, rank_piece = (6, 7)
        else:
            rank_pawn, rank_piece = (1, 0)

        self.squares[rank_piece][1] = Square(rank_piece, 1, Knight(color))
        self.squares[rank_piece][6] = Square(rank_piece, 6, Knight(color))

        self.squares[rank_piece][2] = Square(rank_piece, 2, Bishop(color))
        self.squares[rank_piece][5] = Square(rank_piece, 5, Bishop(color))

        self.squares[rank_piece][0] = Square(rank_piece, 0, Rook(color))
        self.squares[rank_piece][7] = Square(rank_piece, 7, Rook(color))

        self.squares[rank_piece][4] = Square(rank_piece, 4, King(color))

        self.squares[rank_piece][3] = Square(rank_piece, 3, Queen(color))


    def add_startpositio(self, color):
        if color == 'white':
            rank_pawn, rank_piece = (6, 7)
        else:
            rank_pawn, rank_piece = (1, 0)

        for file in range(files):
            self.squares[rank_pawn][file] = Square(rank_pawn, file, Pawn(color))

        self.squares[rank_piece][1] = Square(rank_piece, 1, Knight(color))
        self.squares[rank_piece][6] = Square(rank_piece, 6, Knight(color))

        self.squares[rank_piece][2] = Square(rank_piece, 2, Bishop(color))
        self.squares[rank_piece][5] = Square(rank_piece, 5, Bishop(color))

        self.squares[rank_piece][0] = Square(rank_piece, 0, Rook(color))
        self.squares[rank_piece][7] = Square(rank_piece, 7, Rook(color))

        self.squares[rank_piece][4] = Square(rank_piece, 4, King(color))

        self.squares[rank_piece][3] = Square(rank_piece, 3, Queen(color))

    # functions for debugging:

    '''
        def add_startposition(self, color):
        # check_stale_and_checkmate
        
        if color == 'white':
            rank_pawn, rank_piece = (6, 7)
        else:
            rank_pawn, rank_piece = (1, 0)

        self.squares[rank_piece][0] = Square(rank_piece, 2, Pawn(color))

        self.squares[rank_piece][2] = Square(rank_piece, 2, Bishop('white'))
        self.squares[rank_piece][5] = Square(rank_piece, 5, Bishop('white'))
        self.squares[3][0] = Square(rank_piece, 2, Bishop('white'))
        self.squares[2][7] = Square(rank_piece, 2, Bishop('white'))

        self.squares[rank_piece][3] = Square(rank_piece, 2, Bishop('white'))
        self.squares[rank_piece][6] = Square(rank_piece, 5, Bishop('white'))
        self.squares[rank_piece][4] = Square(rank_piece, 4, King(color))
        
        
        def add_startposition(self, color):
        check insufficient material
        if color == 'white':
            rank_pawn, rank_piece = (6, 7)
        else:
            rank_pawn, rank_piece = (1, 0)

        self.squares[rank_piece][4] = Square(rank_piece, 4, King(color))

        if color == 'black':
            self.squares[6][3] = Square(rank_piece, 1, Knight('black'))
            self.squares[rank_piece][1] = Square(rank_piece, 1, Bishop('black'))
            self.squares[rank_piece][6] = Square(rank_piece, 1, Knight('white'))
        
        
        def add_startposition(self, color):
        # check pawn promotion
        if color == 'white':
            rank_pawn, rank_piece = (6, 4)
        else:
            rank_pawn, rank_piece = (1, 2)

        self.squares[rank_piece][1] = Square(rank_piece, 1, Knight(color))
        self.squares[rank_piece][6] = Square(rank_piece, 6, Bishop('white'))

        self.squares[rank_piece][4] = Square(rank_piece, 4, King(color))
        
            def add_startposition(self, color):
        if color == 'white':
            rank_pawn, rank_piece = (6, 7)
        else:
            rank_pawn, rank_piece = (1, 0)

        self.squares[rank_piece][7] = Square(rank_piece, 7, King(color))

        if color == 'white':
            self.squares[1][0] = Square(1, 0, Pawn('white'))
            self.squares[1][1] = Square(1, 1, Rook('white'))
    
    '''
