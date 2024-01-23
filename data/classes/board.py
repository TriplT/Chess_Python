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
        # chess board representation
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for rank in range(ranks)]

        # variables for get_valid_moves and ai in general
        self.enemy_attacking_squares = [[0, 0, 0, 0, 0, 0, 0, 0] for rank in range(ranks)]
        self.enemy_checking_squares = []
        self.queen_is_attacked = False
        self.king_must_move = False
        self.king_rank = False
        self.king_file = False
        self.queen_rank = False
        self.queen_file = False
        self.ai_game_ended = False
        self.evaluation = None

        self.move_played = False
        self.move_counter = 0
        self.fifty_move_counter = 0  # 50 move rule variable
        self.played_moves = 0  # needed for bug fixing
        self.endgame = False

        self.last_moves = []
        self.piece_positions = {}

        self.repetition_counter = 0
        self.game_ended = False
        self.win_message = False

        self.create_squares()
        self.add_startposition()
        self.init_piece_positions()

    def create_squares(self):
        for rank in range(ranks):
            for file in range(files):
                self.squares[rank][file] = Square(rank, file)

    def init_piece_positions(self):
        priority_order = {
            'king': 0,
            'pawn': 1,
            'rook': 2,
            'queen': 3,
            'knight': 4,
            'bishop': 5,
        }

        self.piece_positions = {}
        for rank in range(ranks):
            for file in range(files):
                piece = self.squares[rank][file].piece
                if piece:
                    piece_type = piece.name
                    priority = priority_order.get(piece_type, float('inf'))
                    self.piece_positions[(rank, file)] = piece

        # Sort the piece_positions dictionary based on priority_order
        self.piece_positions = dict(
            sorted(self.piece_positions.items(), key=lambda x: priority_order.get(x[1].name, float('inf'))))

    def reset_board(self):
        for rank in range(ranks):
            for file in range(files):
                self.squares[rank][file].piece = None
        self.last_moves = []
        self.move_counter = 0
        self.fifty_move_counter = 0
        self.move_played = False
        self.win_message = False
        self.game_ended = False
        self.ai_game_ended = False
        self.endgame = False
        self.add_startposition()
        self.init_piece_positions()

    def move(self, piece, move, player, game=None):
        if player:
            self.save_last_eaten_piece(self.squares[move.final_square.rank][move.final_square.file].piece)
        else:
            # 50 move rule
            if self.squares[move.final_square.rank][move.final_square.file].occupied():
                self.fifty_move_counter = - 1  # is turned to 0 at the bottom

        # remove castling for captured rooks
        if isinstance(self.squares[move.final_square.rank][move.final_square.file].piece, Rook):
            rank = 7 if piece.color == 'black' else 0
            possible_king = self.squares[rank][4].piece
            if isinstance(possible_king, King):
                if not possible_king.lost_left_castling and move.final_square.file == 0:
                    possible_king.lost_left_castling = self.move_counter
                    possible_king.left_castling = False
                elif not possible_king.lost_right_castling and move.final_square.file == 7:
                    possible_king.lost_right_castling = self.move_counter
                    possible_king.right_castling = False

        # move piece on board
        self.squares[move.initial_square.rank][move.initial_square.file].piece = None
        self.squares[move.final_square.rank][move.final_square.file].piece = piece

        # modify piece dict accordingly
        initial_position = (move.initial_square.rank, move.initial_square.file)
        final_position = (move.final_square.rank, move.final_square.file)

        if initial_position in self.piece_positions:
            del self.piece_positions[initial_position]
        self.piece_positions[final_position] = piece

        # en passant  & promotion logic
        if isinstance(piece, Pawn):
            last_move = self.get_last_move() if self.move_counter != 0 else False
            self.en_passant(piece, move, last_move)
            if player:
                self.player_promotion(screen, piece, move.final_square, game)
                self.fifty_move_counter = -1
            else:
                self.ai_promotion(piece, move)

        # castling logic
        if isinstance(piece, King):
            file_diff = abs(move.final_square.file - move.initial_square.file)
            if not piece.lost_left_castling and piece.left_castling:
                piece.left_castling = False
                piece.lost_left_castling = self.move_counter
            elif not piece.lost_right_castling and piece.right_castling:
                piece.right_castling = False
                piece.lost_right_castling = self.move_counter

            if file_diff == 2:
                if move.final_square.file == 2:
                    rank = 0 if piece.color == 'black' else 7
                    file = 0
                    rook = self.squares[rank][file].piece
                    # move rook
                    self.squares[rank][file].piece = None
                    self.squares[rank][3].piece = rook

                    del self.piece_positions[(rank, file)]
                    self.piece_positions[(rank, 3)] = piece

                if move.final_square.file == 6:
                    rank = 0 if piece.color == 'black' else 7
                    file = 7
                    rook = self.squares[rank][file].piece
                    # move rook
                    self.squares[rank][file].piece = None
                    self.squares[rank][5].piece = rook

                    del self.piece_positions[(rank, file)]
                    self.piece_positions[(rank, 5)] = piece

        if isinstance(piece, Rook):
            rank = 0 if piece.color == 'black' else 7
            possible_king = self.squares[rank][4].piece
            if isinstance(possible_king, King):
                if not possible_king.lost_left_castling and move.initial_square.file == 0:
                    possible_king.lost_left_castling = self.move_counter
                    possible_king.left_castling = False
                elif not possible_king.lost_right_castling and move.initial_square.file == 7:
                    possible_king.lost_right_castling = self.move_counter
                    possible_king.right_castling = False

        if player:
            self.move_played = True
            self.fifty_move_counter += 1
            self.played_moves += 1

        self.save_last_move(move)
        # unfortunately doesn't work for player, for ai keep it at all costs
        # thus:
        # self.last_moves = [move]
        # but it does work???
        self.move_counter += 1

        '''
        for position, piece in self.piece_positions.items():
            print(f"Position: {position}, Piece: {piece.color} {piece.name}")
        print(f"Number of pieces in piece_positions: {len(self.piece_positions)}")
        '''

    def minimax_move(self, piece, move):
        self.save_last_eaten_piece(self.squares[move.final_square.rank][move.final_square.file].piece)

        # remove castling for captured rooks
        if isinstance(self.squares[move.final_square.rank][move.final_square.file].piece, Rook):
            rank = 7 if piece.color == 'black' else 0
            possible_king = self.squares[rank][4].piece
            if isinstance(possible_king, King):
                if not possible_king.lost_left_castling and move.final_square.file == 0:
                    possible_king.lost_left_castling = self.move_counter
                    possible_king.left_castling = False
                elif not possible_king.lost_right_castling and move.final_square.file == 7:
                    possible_king.lost_right_castling = self.move_counter
                    possible_king.right_castling = False

        # move piece on board
        self.squares[move.initial_square.rank][move.initial_square.file].piece = None
        self.squares[move.final_square.rank][move.final_square.file].piece = piece

        # modify piece dict accordingly
        initial_position = (move.initial_square.rank, move.initial_square.file)
        final_position = (move.final_square.rank, move.final_square.file)

        del self.piece_positions[initial_position]
        self.piece_positions[final_position] = piece

        # en passant & promotion logic
        if isinstance(piece, Pawn):
            last_move = self.get_last_move() if self.move_counter != 0 else False
            self.en_passant(piece, move, last_move)
            self.ai_promotion(piece, move)

        # castling logic
        if isinstance(piece, King):
            file_diff = abs(move.final_square.file - move.initial_square.file)
            if not piece.lost_left_castling and piece.left_castling:
                piece.left_castling = False
                piece.lost_left_castling = self.move_counter
            elif not piece.lost_right_castling and piece.right_castling:
                piece.right_castling = False
                piece.lost_right_castling = self.move_counter

            if file_diff == 2:
                if move.final_square.file == 2:
                    rank = 0 if piece.color == 'black' else 7
                    file = 0
                    rook = self.squares[rank][file].piece
                    # move rook
                    self.squares[rank][file].piece = None
                    self.squares[rank][3].piece = rook

                    del self.piece_positions[(rank, file)]
                    self.piece_positions[(rank, 3)] = piece

                if move.final_square.file == 6:
                    rank = 0 if piece.color == 'black' else 7
                    file = 7
                    rook = self.squares[rank][file].piece
                    # move rook
                    self.squares[rank][file].piece = None
                    self.squares[rank][5].piece = rook

                    del self.piece_positions[(rank, file)]
                    self.piece_positions[(rank, 5)] = piece

        if isinstance(piece, Rook):
            rank = 0 if piece.color == 'black' else 7
            possible_king = self.squares[rank][4].piece
            if isinstance(possible_king, King):
                if not possible_king.lost_left_castling and move.initial_square.file == 0:
                    possible_king.lost_left_castling = self.move_counter
                    possible_king.left_castling = False
                elif not possible_king.lost_right_castling and move.initial_square.file == 7:
                    possible_king.lost_right_castling = self.move_counter
                    possible_king.right_castling = False

        self.move_counter += 1
        self.save_last_move(move)

        '''
        for position, piece in self.piece_positions.items():
            print(f"Position: {position}, Piece: {piece.color} {piece.name}")
        print(f"Number of pieces in piece_positions: {len(self.piece_positions)}")
        '''

    def unmake_move(self, piece, move):
        last_eaten_piece = self.get_last_eaten_piece()
        self.pop_last_move()
        self.move_counter -= 1

        # revert move on board
        self.squares[move.initial_square.rank][move.initial_square.file].piece = piece
        self.squares[move.final_square.rank][move.final_square.file].piece = last_eaten_piece

        # modify piece dict accordingly
        initial_position = (move.initial_square.rank, move.initial_square.file)
        final_position = (move.final_square.rank, move.final_square.file)

        if last_eaten_piece:
            self.piece_positions[final_position] = self.squares[move.final_square.rank][move.final_square.file].piece
        else:
            del self.piece_positions[final_position]
        self.piece_positions[initial_position] = self.squares[move.initial_square.rank][move.initial_square.file].piece

        # revert eaten piece in en passant
        if isinstance(piece, Pawn):
            if piece.made_en_passant == self.move_counter and self.move_counter != 0:
                piece.made_en_passant = False  # theoretically makes no difference
                opposite_color = 'white' if piece.color == 'black' else 'black'
                rank = move.initial_square.rank
                file = move.final_square.file

                self.squares[rank][file].piece = Pawn(opposite_color)
                self.piece_positions[(rank, file)] = self.squares[rank][file].piece

        # revert promotion
        if isinstance(piece, (Queen, Bishop, Knight, Rook)):
            self.revert_promotion(move.initial_square.rank, move.initial_square.file, piece)

        # revert castling
        if isinstance(piece, King):
            if piece.lost_left_castling == self.move_counter:
                piece.left_castling = True
                piece.lost_left_castling = False
            elif piece.lost_right_castling == self.move_counter:
                piece.right_castling = True
                piece.lost_right_castling = False

            if abs(move.final_square.file - move.initial_square.file) == 2:
                rank = 0 if piece.color == 'black' else 7
                initial_file = 0 if move.final_square.file == 2 else 7
                final_file = 3 if move.final_square.file == 2 else 5

                rook = self.squares[rank][final_file].piece
                # unmake rook
                self.squares[rank][initial_file].piece = rook
                self.squares[rank][final_file].piece = None

                self.piece_positions[(rank, initial_file)] = self.squares[rank][initial_file].piece
                del self.piece_positions[(rank, final_file)]

        if isinstance(piece, Rook):
            rank = 0 if piece.color == 'black' else 7
            possible_king = self.squares[rank][4].piece
            if isinstance(possible_king, King):
                if possible_king.lost_left_castling == self.move_counter:
                    possible_king.left_castling = True
                    possible_king.lost_left_castling = False
                elif possible_king.lost_right_castling == self.move_counter:
                    possible_king.right_castling = True
                    possible_king.lost_right_castling = False

    def ai_promotion(self, piece, move):
        if isinstance(piece, Pawn) and (move.final_square.rank == 0 or move.final_square.rank == 7):
            self.squares[move.final_square.rank][move.final_square.file].piece = move.promotion_piece(piece.color)
            self.squares[move.final_square.rank][move.final_square.file].piece.made_promotion = self.move_counter
            self.piece_positions[(move.final_square.rank, move.final_square.file)] = self.squares[move.final_square.rank][move.final_square.file].piece

    def revert_promotion(self, rank, file, piece):
        if piece.made_promotion == self.move_counter and self.move_counter != 0:
            self.squares[rank][file].piece = Pawn(piece.color)
            self.piece_positions[(rank, file)] = self.squares[rank][file].piece

    def player_promotion(self, screen, piece, last, game):
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
                            self.piece_positions[(last.rank, last.file)] = self.squares[last.rank][last.file].piece
                            return
                        elif (screen_x / 2 + 5) < x < (screen_x / 2 + 95) and (screen_y / 2 - 95) < y < (
                                screen_y / 2 + - 5):
                            self.squares[last.rank][last.file].piece = Rook(piece.color)
                            self.piece_positions[(last.rank, last.file)] = self.squares[last.rank][last.file].piece
                            return
                        elif (screen_x / 2 - 95) < x < (screen_x / 2 - 5) and (screen_y / 2 + 5) < y < (
                                screen_y / 2 + 95):
                            self.squares[last.rank][last.file].piece = Bishop(piece.color)
                            self.piece_positions[(last.rank, last.file)] = self.squares[last.rank][last.file].piece
                            return
                        elif (screen_x / 2 + 5) < x < (screen_x / 2 + 95) and (screen_y / 2 + 5) < y < (
                                screen_y / 2 + 95):
                            self.squares[last.rank][last.file].piece = Knight(piece.color)
                            self.piece_positions[(last.rank, last.file)] = self.squares[last.rank][last.file].piece
                            return

    def en_passant(self, piece, move, last_move):
        if piece.en_passant:
            if move.final_square.file == last_move.final_square.file:
                self.squares[last_move.final_square.rank][last_move.final_square.file].piece = None
                del self.piece_positions[(last_move.final_square.rank, last_move.final_square.file)]
                piece.made_en_passant = self.move_counter

    def getPiece(self, rank, file):
        return self.squares[rank][file].piece

    def getPieceMoveInitial(self, move):
        return self.squares[move.initial_square.rank][move.initial_square.file].piece

    def getPieceMoveFinal(self, move):
        return self.squares[move.final_square.rank][move.final_square.file].piece

    def get_piece(self, rank, file):
        return self.piece_positions.get((rank, file))

    def get_own_pieces(self, color):
        lst = []
        for rank in range(ranks):
            for file in range(files):
                if self.squares[rank][file].occupied_by_teammate(color):
                    lst.append(self.squares[rank][file])
        return lst

    def get_amount_of_pieces(self):
        counter = 0
        for rank in range(ranks):
            for file in range(files):
                if self.squares[rank][file].piece:
                    counter += 1
        self.last_num_of_pieces = counter

    def save_last_move(self, move):
        self.last_moves.append(move)

    def get_last_move(self):
        return self.last_moves[-1]

    def pop_last_move(self):
        self.last_moves.pop()

    def save_last_eaten_piece(self, piece):
        self.last_eaten_piece.append(piece)

    def get_last_eaten_piece(self):
        return self.last_eaten_piece.pop()

    def evaluate_position(self, color):
        position_value = 0
        for position, piece in self.piece_positions.items():
            piece_sq_eval = self.get_piece_square_table(position[0], position[1], piece, color)
            if piece.color == color:
                position_value += piece_sq_eval
                position_value += piece.value
            else:
                position_value -= piece_sq_eval
                position_value -= piece.value

        self.evaluation = round(position_value, 3)

    def add_startposition(self):
        colors = ('white', 'black')
        for color in colors:
            if color == 'white':
                rank_pawn, rank_piece = (6, 7)
            else:
                rank_pawn, rank_piece = (1, 0)

            self.squares[rank_pawn][0] = Square(rank_pawn, 0, Pawn(color))
            self.squares[rank_pawn][1] = Square(rank_pawn, 1, Pawn(color))
            self.squares[rank_pawn][2] = Square(rank_pawn, 2, Pawn(color))
            self.squares[rank_pawn][3] = Square(rank_pawn, 3, Pawn(color))
            self.squares[rank_pawn][4] = Square(rank_pawn, 4, Pawn(color))
            self.squares[rank_pawn][5] = Square(rank_pawn, 5, Pawn(color))
            self.squares[rank_pawn][6] = Square(rank_pawn, 6, Pawn(color))
            self.squares[rank_pawn][7] = Square(rank_pawn, 7, Pawn(color))

            self.squares[rank_piece][1] = Square(rank_piece, 1, Knight(color))
            self.squares[rank_piece][6] = Square(rank_piece, 6, Knight(color))

            self.squares[rank_piece][2] = Square(rank_piece, 2, Bishop(color))
            self.squares[rank_piece][5] = Square(rank_piece, 5, Bishop(color))

            self.squares[rank_piece][0] = Square(rank_piece, 0, Rook(color))
            self.squares[rank_piece][7] = Square(rank_piece, 7, Rook(color))

            self.squares[rank_piece][4] = Square(rank_piece, 4, King(color))

            self.squares[rank_piece][3] = Square(rank_piece, 3, Queen(color))

    def add_startpositio(self):
        colors = ('white', 'black')
        for color in colors:
            if color == 'white':
                self.squares[7][7] = Square(7, 7, Pawn(color))
                self.squares[2][7] = Square(2, 7, Pawn(color))
                self.squares[6][5] = Square(6, 5, Pawn(color))
                self.squares[6][4] = Square(6, 4, Pawn(color))
                self.squares[3][4] = Square(3, 4, Pawn(color))

                self.squares[6][1] = Square(6, 1, Knight(color))
                # self.squares[1][6] = Square(1, 6, Knight(color))

                self.squares[3][2] = Square(3, 2, Bishop(color))
                self.squares[7][5] = Square(7, 5, Bishop(color))

                self.squares[2][0] = Square(2, 0, Rook(color))
                self.squares[4][7] = Square(4, 7, Rook(color))

                self.squares[7][4] = Square(7, 4, King(color))

                self.squares[2][5] = Square(2, 5, Queen(color))
            else:
                self.squares[1][2] = Square(1, 2, Pawn(color))
                self.squares[1][3] = Square(1, 3, Pawn(color))
                self.squares[6][6] = Square(6, 6, Pawn(color))
                self.squares[5][6] = Square(5, 6, Pawn(color))

                self.squares[1][0] = Square(1, 0, Knight(color))
                self.squares[3][6] = Square(3, 6, Knight(color))

                self.squares[6][2] = Square(6, 2, Bishop(color))
                self.squares[0][1] = Square(0, 1, Bishop(color))

                self.squares[5][0] = Square(5, 0, Rook(color))
                self.squares[6][7] = Square(6, 7, Rook(color))

                self.squares[0][0] = Square(0, 0, King(color))

                self.squares[4][4] = Square(4, 4, Queen(color))

    def game_end(self, player):
        insufficient_material = False
        valid_piece = False
        white_counter = 0
        black_counter = 0

        if len(self.piece_positions) <= 4:
            for position, piece in self.piece_positions.items():
                if isinstance(piece, (Queen, Pawn, Rook)):
                    valid_piece = True
                    break
                if isinstance(piece, (Bishop, Knight, King)):
                    if piece.color == 'white':
                        white_counter += 1
                    else:
                        black_counter += 1
            if white_counter <= 2 and black_counter <= 2 and not valid_piece:
                insufficient_material = True

        if player:
            if insufficient_material:
                self.game_ended = True
                self.win_message = 'insufficient material'
            elif self.repetition_counter == 4:
                self.game_ended = True
                self.win_message = 'repetition'
            elif self.fifty_move_counter == 50:
                self.game_ended = True
                self.win_message = '50 move-rule'

            self.move_played = False
        else:
            if insufficient_material:
                self.evaluation = 0.0
                self.ai_game_ended = True
            elif self.repetition_counter >= 4:
                self.evaluation = 0.0
                self.ai_game_ended = True

    def get_valid_moves(self, color, eval_color=False):
        if not self.endgame:
            if len(self.piece_positions) >= 15:
                self.endgame = True

        self.calculate_enemy_attacking_moves('white' if color == 'black' else 'black')
        if self.enemy_checking_squares:
            # because the king is in check there will only be moves calculated that put the king out of check
            return self.in_check_valid_moves(color, eval_color)
        else:
            # because the king is NOT in check moves can be calculated easily
            return self.no_check_valid_moves(color, eval_color)

    def calculate_enemy_attacking_moves(self, color):

        def pawn_moves():
            possible_move_rank = rank + piece.direction
            possible_move_files = [file - 1, file + 1]

            for possible_move_file in possible_move_files:
                if Square.in_range(possible_move_rank, possible_move_file):
                    self.enemy_attacking_squares[possible_move_rank][possible_move_file] = 1
                    if self.squares[possible_move_rank][possible_move_file].occupied_by_opponent(piece.color):
                        if possible_move_rank == self.king_rank and possible_move_file == self.king_file:
                            if self.enemy_checking_squares:
                                self.king_must_move = True
                            else:
                                self.enemy_checking_squares.append((rank, file))
                        elif possible_move_rank == self.queen_rank and possible_move_file == self.queen_file:
                            self.queen_is_attacked = True

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
                    self.enemy_attacking_squares[move_rank][move_file] = 1
                    if self.squares[move_rank][move_file].no_friendly_fire(color):
                        if move_rank == self.king_rank and move_file == self.king_file:
                            if self.enemy_checking_squares:
                                self.king_must_move = True
                            else:
                                self.enemy_checking_squares.append((rank, file))
                        elif move_rank == self.queen_rank and move_file == self.queen_file:
                            self.queen_is_attacked = True

        def strait_line_moves(increments):
            for increment in increments:
                rank_inc, file_inc = increment
                possible_move_rank = rank + rank_inc
                possible_move_file = file + file_inc

                end_reached = False
                # usually we could just stop the increments as soon as we have a piece that's blocking the path
                # but we need to account for pinned pieces, for whose we have to continue the search in case a king
                # is behind our blocking piece.
                # end reached prevents several functions to look out for checks when a blocking piece was already found.
                # after end reach we're only checking for potential pinned pieces
                king_reached = False
                pinning_pieces = 0
                pinned_piece = None
                temp_pinning_squares = [(rank, file)]
                temp_checking_squares = [(rank, file)]
                while True:
                    if Square.in_range(possible_move_rank, possible_move_file):
                        if self.squares[possible_move_rank][possible_move_file].occupied_by_noone():
                            if not end_reached:
                                self.enemy_attacking_squares[possible_move_rank][possible_move_file] = 1
                            if not king_reached:
                                temp_pinning_squares.append((possible_move_rank, possible_move_file))
                            if not king_reached and not end_reached:
                                temp_checking_squares.append((possible_move_rank, possible_move_file))

                        elif self.squares[possible_move_rank][possible_move_file].occupied_by_opponent(color):
                            # calculate squares that are being attacked by an enemy piece,
                            # calculate squares that need to be prevented through blocking or killing the piece on it
                            # and calculate squares of pinned pieces

                            # little note for the calculation of attacking squares
                            # if a friendly piece is in front of the king, the attack is successfully stopped
                            # but be careful:
                            # the king can't stop the laser fire of the increments with its previous self
                            # let's say the own king is being attacked on a vertical. if the enemy_attacking_squares
                            # are stopped on the kings square, the king will think it can move one square back
                            # to be safe since a friendly piece is protecting the king.
                            # Obviously the king isn't safe anywhere on that vertical
                            # and cannot use its previous self as a target dummy.
                            # in our code we need to be aware that moving one square back on the vertical
                            # won't get the king out of check

                            if possible_move_rank == self.king_rank and possible_move_file == self.king_file:
                                king_reached = True

                                # enemy attacking squares
                                if not end_reached:
                                    self.enemy_attacking_squares[possible_move_rank][possible_move_file] = 1
                                    if possible_move_rank == self.queen_rank and possible_move_file == self.queen_file:
                                        self.queen_is_attacked = True
                                # pins
                                if pinning_pieces == 1:
                                    pinned_piece.pinned = temp_pinning_squares

                                # enemy checking squares
                                if not end_reached:
                                    if self.enemy_checking_squares:
                                        self.king_must_move = True
                                    else:
                                        self.enemy_checking_squares = temp_checking_squares

                            else:
                                if not end_reached:
                                    self.enemy_attacking_squares[possible_move_rank][possible_move_file] = 1
                                    end_reached = True

                                if not king_reached:
                                    pinned_piece = self.squares[possible_move_rank][possible_move_file].piece
                                    pinning_pieces += 1

                        elif self.squares[possible_move_rank][possible_move_file].occupied_by_teammate(color):
                            # we can exclude any vertical/diagonal checks since an enemy piece blocks its own
                            # diagonal/vertical vision
                            if not end_reached:
                                self.enemy_attacking_squares[possible_move_rank][possible_move_file] = 1
                                end_reached = True

                            if not king_reached:
                                pinned_piece = self.squares[possible_move_rank][possible_move_file].piece
                                pinning_pieces += 1

                            if isinstance(self.squares[possible_move_rank][possible_move_file].piece, Pawn):
                                pass
                            # mach es mit pinned pieces (dem count)
                            # wenn der count 0 ist und das eigene piece ein bauer fetz den count hoch oder so
                            # bei count 1 und das nächste piece ein gegnerischer bauer der auf dem gleichen rank steht
                            # nach en passant überprüfen
                            # dann weiterschauen
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
                    self.enemy_attacking_squares[possible_move_rank][possible_move_file] = 1

        self.enemy_attacking_squares = [[0, 0, 0, 0, 0, 0, 0, 0] for rank in range(ranks)]  # clear list
        self.enemy_checking_squares = []
        self.king_must_move = False
        self.queen_is_attacked = False
        for position in self.piece_positions:
            rank = position[0]
            file = position[1]
            piece = self.squares[rank][file].piece
            piece.pinned = []
            if isinstance(piece, King) and piece.color != color:
                self.king_rank = rank
                self.king_file = file
            elif isinstance(piece, Queen) and piece.color != color:
                self.queen_rank = rank
                self.queen_file = file

        for position in self.piece_positions:
            rank = position[0]
            file = position[1]
            piece = self.squares[rank][file].piece
            if piece.color == color:
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

    # parameter eval color used for game over (stale-/checkmate)
    def in_check_valid_moves(self, color, eval_color=False):
        def pawn_moves():
            promotion_pieces = [Queen, Knight, Bishop, Rook]
            piece.en_passant = False
            if (color == 'white' and rank == 6) or (color == 'black' and rank == 1):
                steps = 2
            else:
                steps = 1

            # vertical moves
            start = rank + piece.direction
            end = rank + (piece.direction * steps)

            for possible_move_rank in range(start, end + piece.direction, piece.direction):

                if Square.in_range(possible_move_rank):
                    if self.squares[possible_move_rank][file].occupied_by_noone():
                        for square in self.enemy_checking_squares:
                            if possible_move_rank == square[0] and file == square[1]:
                                initial_pos = Square(rank, file)
                                final_pos = Square(possible_move_rank, file)
                                move = Move(initial_pos, final_pos)
                                if not piece.pinned or (possible_move_rank, file) in piece.pinned:
                                    if final_pos.rank == 0 or final_pos.rank == 7:
                                        for promotion_piece in promotion_pieces:
                                            move = Move(initial_pos, final_pos, promotion_piece)
                                            valid_moves.append(move)
                                    else:
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
                    if self.squares[possible_move_rank][possible_move_file].occupied_by_opponent(color):
                        for square in self.enemy_checking_squares:
                            if possible_move_rank == square[0] and possible_move_file == square[1]:
                                initial_pos = Square(rank, file)
                                final_pos = Square(possible_move_rank, possible_move_file)
                                move = Move(initial_pos, final_pos)
                                if not piece.pinned or (possible_move_rank, possible_move_file) in piece.pinned:
                                    if final_pos.rank == 0 or final_pos.rank == 7:
                                        for promotion_piece in promotion_pieces:
                                            move = Move(initial_pos, final_pos, promotion_piece)
                                            valid_moves.append(move)
                                    else:
                                        valid_moves.append(move)

            # please add special case en passant and check whether the pawn that's being killed is a pinned piece
            last_move = self.get_last_move() if self.move_counter != 0 else None
            if last_move:
                last_initial = last_move.initial_square
                last_final = last_move.final_square
                last_piece = self.squares[last_final.rank][last_final.file].piece

                if isinstance(last_piece, Pawn):
                    if abs(last_final.rank - last_initial.rank) == 2 and last_final.rank == rank:
                        for possible_move_file in possible_move_files:
                            if Square.in_range(possible_move_rank, possible_move_file):
                                if self.squares[rank][possible_move_file].piece == last_piece:
                                    for square in self.enemy_checking_squares:
                                        if possible_move_rank == square[0] and possible_move_file == square[1]:
                                            initial_pos = Square(rank, file)
                                            final_pos = Square(possible_move_rank, possible_move_file)
                                            move = Move(initial_pos, final_pos)
                                            if piece.pinned or (possible_move_rank, possible_move_file) in piece.pinned:
                                                valid_moves.append(move)
                                                piece.en_passant = True

        def knight_moves():
            if not piece.pinned:
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
                        if self.squares[move_rank][move_file].no_friendly_fire(color):
                            for square in self.enemy_checking_squares:
                                if move_rank == square[0] and move_file == square[1]:
                                    move = Move(Square(rank, file), Square(move_rank, move_file))
                                    valid_moves.append(move)

        def strait_line_moves(increments):
            for increment in increments:
                rank_inc, file_inc = increment
                possible_move_rank = rank + rank_inc
                possible_move_file = file + file_inc

                while True:
                    if Square.in_range(possible_move_rank, possible_move_file):

                        if self.squares[possible_move_rank][possible_move_file].occupied_by_noone():
                            for square in self.enemy_checking_squares:
                                if possible_move_rank == square[0] and possible_move_file == square[1]:
                                    initial = Square(rank, file)
                                    final = Square(possible_move_rank, possible_move_file)
                                    move = Move(initial, final)
                                    if not piece.pinned or (possible_move_rank, possible_move_file) in piece.pinned:
                                        valid_moves.append(move)

                        elif self.squares[possible_move_rank][possible_move_file].occupied_by_opponent(color):
                            for square in self.enemy_checking_squares:
                                if possible_move_rank == square[0] and possible_move_file == square[1]:
                                    initial = Square(rank, file)
                                    final = Square(possible_move_rank, possible_move_file)
                                    move = Move(initial, final)
                                    if not piece.pinned or (possible_move_rank, possible_move_file) in piece.pinned:
                                        valid_moves.append(move)
                            break

                        elif self.squares[possible_move_rank][possible_move_file].occupied_by_teammate(color):
                            break
                    else:
                        break

                    possible_move_rank += rank_inc
                    possible_move_file += file_inc

        def king_moves():
            moves = [
                (self.king_rank - 1, self.king_file - 1),
                (self.king_rank - 1, self.king_file + 0),
                (self.king_rank - 1, self.king_file + 1),
                (self.king_rank + 1, self.king_file - 1),
                (self.king_rank + 1, self.king_file + 0),
                (self.king_rank + 1, self.king_file + 1),
                (self.king_rank + 0, self.king_file - 1),
                (self.king_rank + 0, self.king_file + 1),
            ]

            for move in moves:
                possible_move_rank, possible_move_file = move
                if Square.in_range(possible_move_rank, possible_move_file):
                    if self.squares[possible_move_rank][possible_move_file].no_friendly_fire(color):
                        if self.enemy_attacking_squares[possible_move_rank][possible_move_file] == 0:

                            initial = Square(self.king_rank, self.king_file)
                            final = Square(possible_move_rank, possible_move_file)
                            move = Move(initial, final)
                            valid_moves.append(move)

        valid_moves = []
        if self.king_must_move:
            print('king is attacked by multiple pieces --> board.king_must_move (in_check_valid_moves)')
            # the king is attacked by multiple pieces
            # so no piece has the ability to capture all checking pieces in one move
            # or to block all their attacking paths at once
            # --> the king HAS to move, meaning we can only return his valid moves
            # calculate checkmate
            king_moves()
            if not valid_moves:
                if not eval_color:
                    self.win_message = 'checkmate'
                    self.game_ended = True
                else:
                    self.ai_game_ended = True
                    if eval_color == 'white':
                        self.evaluation = - 99999.0 + self.move_counter
                    elif eval_color == 'black':
                        self.evaluation = 99999.0 - self.move_counter
            return valid_moves

        for position in sorted(self.piece_positions, reverse=True):
            rank = position[0]
            file = position[1]
            piece = self.squares[rank][file].piece
            if piece.color == color:
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

        # calculate checkmate
        if not valid_moves:
            if not eval_color:
                self.win_message = 'checkmate'
                self.game_ended = True
            else:
                self.ai_game_ended = True
                if eval_color == 'white':
                    self.evaluation = - 99999.0 - self.move_counter
                elif eval_color == 'black':
                    self.evaluation = 99999.0 + self.move_counter

        return valid_moves

    def no_check_valid_moves(self, color, eval_color=False):
        valid_moves = []

        def pawn_moves():
            promotion_pieces = [Queen, Knight, Bishop, Rook]
            piece.en_passant = False
            if (color == 'white' and rank == 6) or (color == 'black' and rank == 1):
                steps = 2
            else:
                steps = 1

            # vertical moves
            start = rank + piece.direction
            end = rank + (piece.direction * steps)

            for possible_move_rank in range(start, end + piece.direction, piece.direction):
                if Square.in_range(possible_move_rank):
                    if self.squares[possible_move_rank][file].occupied_by_noone():
                        initial_pos = Square(rank, file)
                        final_pos = Square(possible_move_rank, file)
                        move = Move(initial_pos, final_pos)
                        if not piece.pinned or (possible_move_rank, file) in piece.pinned:
                            if final_pos.rank == 0 or final_pos.rank == 7:
                                for promotion_piece in promotion_pieces:
                                    move = Move(initial_pos, final_pos, promotion_piece)
                                    valid_moves.append(move)
                            else:
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
                        final_pos = Square(possible_move_rank, possible_move_file)
                        move = Move(initial_pos, final_pos)
                        if not piece.pinned or (possible_move_rank, possible_move_file) in piece.pinned:
                            if final_pos.rank == 0 or final_pos.rank == 7:
                                for promotion_piece in promotion_pieces:
                                    move = Move(initial_pos, final_pos, promotion_piece)
                                    valid_moves.append(move)
                            else:
                                valid_moves.append(move)

            last_move = self.get_last_move() if self.move_counter != 0 else None
            if last_move:
                last_initial = last_move.initial_square
                last_final = last_move.final_square
                last_piece = self.squares[last_final.rank][last_final.file].piece

                if isinstance(last_piece, Pawn):
                    if abs(last_final.rank - last_initial.rank) == 2 and last_final.rank == rank:
                        for possible_move_file in possible_move_files:
                            if Square.in_range(possible_move_rank, possible_move_file):
                                if self.squares[rank][possible_move_file].piece == last_piece:
                                    initial_pos = Square(rank, file)
                                    final_pos = Square(possible_move_rank, possible_move_file)
                                    move = Move(initial_pos, final_pos)
                                    if not piece.pinned or (possible_move_rank, possible_move_file) in piece.pinned:
                                        valid_moves.append(move)
                                        piece.en_passant = True

        def knight_moves():
            if not piece.pinned:
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
                            move = Move(Square(rank, file), Square(move_rank, move_file))
                            valid_moves.append(move)

        def strait_line_moves(increments):
            for increment in increments:
                rank_inc, file_inc = increment
                possible_move_rank = rank + rank_inc
                possible_move_file = file + file_inc

                while True:
                    if Square.in_range(possible_move_rank, possible_move_file):

                        initial = Square(rank, file)
                        final = Square(possible_move_rank, possible_move_file)
                        move = Move(initial, final)

                        if self.squares[possible_move_rank][possible_move_file].occupied_by_noone():
                            if not piece.pinned or (possible_move_rank, possible_move_file) in piece.pinned:
                                if self.queen_is_attacked and isinstance(piece, Queen):
                                    valid_moves.insert(0, move)
                                else:
                                    valid_moves.append(move)
                        elif self.squares[possible_move_rank][possible_move_file].occupied_by_opponent(piece.color):
                            if not piece.pinned or (possible_move_rank, possible_move_file) in piece.pinned:
                                if self.queen_is_attacked and isinstance(piece, Queen):
                                    valid_moves.insert(0, move)
                                else:
                                    valid_moves.append(move)
                            break
                        elif self.squares[possible_move_rank][possible_move_file].occupied_by_teammate(piece.color):
                            break
                    else:
                        break

                    possible_move_rank += rank_inc
                    possible_move_file += file_inc

        def king_moves():
            moves = [
                (self.king_rank - 1, self.king_file - 1),
                (self.king_rank - 1, self.king_file + 0),
                (self.king_rank - 1, self.king_file + 1),
                (self.king_rank + 1, self.king_file - 1),
                (self.king_rank + 1, self.king_file + 0),
                (self.king_rank + 1, self.king_file + 1),
                (self.king_rank + 0, self.king_file - 1),
                (self.king_rank + 0, self.king_file + 1),
            ]

            for move in moves:
                possible_move_rank, possible_move_file = move
                if Square.in_range(possible_move_rank, possible_move_file):
                    if self.squares[possible_move_rank][possible_move_file].no_friendly_fire(color):
                        if self.enemy_attacking_squares[possible_move_rank][possible_move_file] == 0:

                            initial = Square(self.king_rank, self.king_file)
                            final = Square(possible_move_rank, possible_move_file)
                            move = Move(initial, final)
                            valid_moves.append(move)

            if (color == 'white' and self.king_rank == 7 and self.king_file == 4) \
                    or (color == 'black' and self.king_rank == 0 and self.king_file == 4):
                king = self.squares[self.king_rank][self.king_file].piece
                if king.left_castling and self.enemy_attacking_squares[self.king_rank][self.king_file] == 0:
                    squares = [1, 2, 3]
                    can_castle = True
                    for square in squares:
                        if self.squares[self.king_rank][square].occupied() \
                                    or self.enemy_attacking_squares[self.king_rank][square] == 1:
                            can_castle = False
                    if can_castle:
                        initial = Square(self.king_rank, self.king_file)
                        final = Square(self.king_rank, 2)
                        move = Move(initial, final)
                        valid_moves.append(move)

                if king.right_castling and self.enemy_attacking_squares[self.king_rank][self.king_file] == 0:
                    squares = [5, 6]
                    can_castle = True
                    for square in squares:
                        if self.squares[self.king_rank][square].occupied() \
                                    or self.enemy_attacking_squares[self.king_rank][square] == 1:
                            can_castle = False
                    if can_castle:
                        initial = Square(self.king_rank, self.king_file)
                        final = Square(self.king_rank, 6)
                        move = Move(initial, final)
                        valid_moves.append(move)

        for position in sorted(self.piece_positions, reverse=True):
            rank = position[0]
            file = position[1]
            piece = self.squares[rank][file].piece
            if piece.color == color:
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

        # calculate stalemate

        if not valid_moves:
            if not eval_color:
                self.win_message = 'stalemate'
                self.game_ended = True
            else:
                self.ai_game_ended = True
                self.evaluation = 0

        return valid_moves

    def get_piece_square_table(self, rank, file, piece, color):
        def pawn():
            # midgame
            if not self.endgame:
                table = [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [98, 134, 61, 95, 68, 126, 34, -11],
                    [-6, 7, 26, 31, 65, 56, 25, -20],
                    [-14, 13, 6, 21, 23, 12, 17, -23],
                    [-27, -2, -5, 12, 17, 6, 10, -25],
                    [-26, -4, -4, -10, 3, 3, 33, -12],
                    [-35, -1, -20, -23, -15, 24, 38, -22],
                    [0, 0, 0, 0, 0, 0, 0, 0]
                ]
            # endgame
            else:
                table = [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [178, 173, 158, 134, 147, 132, 165, 187],
                    [94, 100, 85, 67, 56, 53, 82, 84],
                    [32, 24, 13, 5, -2, 4, 17, 17],
                    [13, 9, -3, -7, -7, -8, 3, -1],
                    [4, 7, -6, 1, 0, -5, -1, -8],
                    [13, 8, 8, 10, 13, 0, 2, -7],
                    [0, 0, 0, 0, 0, 0, 0, 0]
                ]
                return table[rank][file]

        def bishop():
            if not self.endgame:
                table = [
                    [-29, 4, -82, -37, -25, -42, 7, -8],
                    [-26, 16, -18, -13, 30, 59, 18, -47],
                    [-16, 37, 43, 40, 35, 50, 37, -2],
                    [-4, 5, 19, 50, 37, 37, 7, -2],
                    [-6, 13, 13, 26, 34, 12, 10, 4],
                    [0, 15, 15, 15, 14, 27, 18, 10],
                    [4, 15, 16, 0, 7, 21, 33, 1],
                    [-33, -3, -14, -21, -13, -12, -39, -21]
                ]
            else:
                table = [
                    [-14, -21, -11, -8, -7, -9, -17, -24],
                    [-8, -4, 7, -12, -3, -13, -4, -14],
                    [2, -8, 0, -1, -2, 6, 0, 4],
                    [-3, 9, 12, 9, 14, 10, 3, 2],
                    [-6, 3, 13, 19, 7, 10, -3, -9],
                    [-12, -3, 8, 10, 13, 3, -7, -15],
                    [-14, -18, -7, -1, 4, -9, -15, -27],
                    [-23, -9, -23, -5, -9, -16, -5, -17]
                ]
                return table[rank][file]

        def knight():
            if not self.endgame:
                table = [
                    [-167, -89, -34, -49, 61, -97, -15, -107],
                    [-73, -41, 72, 36, 23, 62, 7, -17],
                    [-47, 60, 37, 65, 84, 129, 73, 44],
                    [-9, 17, 19, 53, 37, 69, 18, 22],
                    [-13, 4, 16, 13, 28, 19, 21, -8],
                    [-23, -9, 12, 10, 19, 17, 25, -16],
                    [-29, -53, -12, -3, -1, 18, -14, -19],
                    [-105, -21, -58, -33, -17, -28, -19, -23]
                ]
            else:
                table = [
                    [-58, -38, -13, -28, -31, -27, -63, -99],
                    [-25, -8, -25, -2, -9, -25, -24, -52],
                    [-24, -20, 10, 9, -1, -9, -19, -41],
                    [-17, 3, 22, 22, 22, 11, 8, -18],
                    [-18, -6, 16, 25, 16, 17, 4, -18],
                    [-23, -3, -1, 15, 10, -3, -20, -22],
                    [-42, -20, -10, -5, -2, -20, -23, -44],
                    [-29, -51, -23, -15, -22, -18, -50, -64]
                ]
                return table[rank][file]

        def rook():
            if not self.endgame:
                table = [
                    [32, 42, 32, 51, 63, 9, 31, 43],
                    [27, 32, 58, 62, 80, 67, 26, 44],
                    [-5, 19, 26, 36, 17, 45, 61, 16],
                    [-24, -11, 7, 26, 24, 35, -8, -20],
                    [-36, -26, -12, -1, 9, -7, 6, -23],
                    [-45, -25, -16, -17, 3, 0, -5, -33],
                    [-44, -16, -20, -9, -1, 11, -6, -71],
                    [-19, -13, 1, 17, 16, 7, -37, -26]
                ]
            else:
                table = [
                    [13, 10, 18, 15, 12, 12, 8, 5],
                    [11, 13, 13, 11, -3, 3, 8, 3],
                    [7, 7, 7, 5, 4, -3, -5, -3],
                    [4, 3, 13, 1, 2, 1, -1, 2],
                    [3, 5, 8, 4, -5, -6, -8, -11],
                    [-4, 0, -5, -1, -7, -12, -8, -16],
                    [-6, -6, 0, 2, -9, -9, -11, -3],
                    [-9, 2, 3, -1, -5, -13, 4, -20]
                ]
                return table[rank][file]

        def queen():
            if not self.endgame:
                table = [
                    [-28, 0, 29, 12, 59, 44, 43, 45],
                    [-24, -39, -5, 1, -16, 57, 28, 54],
                    [-13, -17, 7, 8, 29, 56, 47, 57],
                    [-27, -27, -16, -16, -1, 17, -2, 1],
                    [-9, -26, -9, -10, -2, -4, 3, -3],
                    [-14, 2, -11, -2, -5, 2, 14, 5],
                    [-35, -8, 11, 2, 8, 15, -3, 1],
                    [-1, -18, -9, 10, -15, -25, -31, -50]
                ]
            else:
                table = [
                    [-9, 22, 22, 27, 27, 19, 10, 20],
                    [-17, 20, 32, 41, 58, 25, 30, 0],
                    [-20, 6, 9, 49, 47, 35, 19, 9],
                    [3, 22, 24, 45, 57, 40, 57, 36],
                    [-18, 28, 19, 47, 31, 34, 39, 23],
                    [-16, -27, 15, 6, 9, 17, 10, 5],
                    [-22, -23, -30, -16, -16, -23, -36, -32],
                    [-33, -28, -22, -43, -5, -32, -20, -41]
                ]
                return table[rank][file]

        def king():
            if not self.endgame:
                table = [
                    [-65, 23, 16, -15, -56, -34, 2, 13],
                    [29, -1, -20, -7, -8, -4, -38, -29],
                    [-9, 24, 2, -16, -20, 6, 22, -22],
                    [-17, -20, -12, -27, -30, -25, -14, -36],
                    [-49, -1, -27, -39, -46, -44, -33, -51],
                    [-14, -14, -22, -46, -44, -30, -15, -27],
                    [1, 7, -8, -64, -43, -16, 9, 8],
                    [-15, 36, 12, -54, 8, -28, 24, 14]
                ]
            else:
                table = [
                    [-74, -35, -18, -18, -11, 15, 4, -17],
                    [-12, 17, 14, 17, 17, 38, 23, 11],
                    [10, 17, 23, 15, 20, 45, 44, 13],
                    [-8, 22, 24, 27, 26, 33, 26, 3],
                    [-18, -4, 21, 24, 27, 23, 9, -11],
                    [-19, -3, 11, 21, 23, 16, 7, -9],
                    [-27, -11, 4, 13, 14, 4, -5, -17],
                    [-53, -34, -21, -11, -28, -14, -24, -43]
                ]
                return table[rank][file]

        if color == 'black':
            rank = 7 - rank
            file = 7 - file
        eval = 0
        if isinstance(piece, Pawn):
            eval = pawn()
        elif isinstance(piece, King):
            eval = king()
        elif isinstance(piece, Queen):
            eval = queen()
        elif isinstance(piece, Bishop):
            eval = bishop()
        elif isinstance(piece, Knight):
            eval = knight()
        elif isinstance(piece, Rook):
            eval = rook()
        return eval
