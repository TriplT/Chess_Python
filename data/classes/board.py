import copy

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


class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for rank in range(ranks)]
        self.last_move = None
        self.current_moves = []
        self.create_squares()
        self.add_startposition('white')
        self.add_startposition('black')

    def create_squares(self):
        for rank in range(ranks):
            for file in range(files):
                self.squares[rank][file] = Square(rank, file)

    def calc_current_moves(self, piece=None):
        if piece:
            self.current_moves = piece.moves

        if not piece:
            self.current_moves = []

    def move(self, piece, move):

        self.squares[move.initial_square.rank][move.initial_square.file].piece = None
        self.squares[move.final_square.rank][move.final_square.file].piece = piece

        if isinstance(piece, Pawn):
            self.pawn_promotion(screen, piece, move.final_square)

        if isinstance(piece, King):
            if self.castling(move.initial_square, move.final_square):
                diff = move.final_square.file - move.initial_square.file
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        piece.moved = True
        piece.clear_moves()
        self.current_moves = []

        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def valid_current_move(self, move):
        return move in self.current_moves

    def pawn_promotion(self, screen, piece, last):
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

    def castling(self, initial, final):
        return abs(initial.file - final.file) == 2
    '''
        def in_checkkkk(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)

        temp_board.move(temp_piece, move)

        for rank in range(ranks):
            for file in range(files):
                if temp_board.squares[rank][file].occupied_by_opponent(piece.color):
                    p = temp_board.squares[rank][file].piece
                    temp_board.calculate_valid_moves(p, rank, file, bool=False)
                    for m in p.moves:
                        if isinstance(m.final_square.piece, King):
                            return True
        return False
    '''
    def move_check_simulation(self, piece, move):

        self.squares[move.initial_square.rank][move.initial_square.file].piece = None
        self.squares[move.final_square.rank][move.final_square.file].piece = piece

    def in_check(self, piece, move, initial_pos, final_pos):
        final_pos_piece = self.squares[final_pos.rank][final_pos.file].piece
        print('in_check aufgerufen')
        self.move_check_simulation(piece, move)

        for rank in range(ranks):
            for file in range(files):
                if self.squares[rank][file].occupied_by_opponent(piece.color):
                    p = self.squares[rank][file].piece
                    self.calculate_valid_moves(p, rank, file, bool=False)
                    print('berechnung moves gegnerischer pieces')

                    for m in p.moves:
                        if isinstance(m.final_square.piece, King):
                            print('king wird von gegnerischen piece angegriffen')
                            self.squares[initial_pos.rank][initial_pos.file].piece = piece
                            self.squares[final_pos.rank][final_pos.file].piece = final_pos_piece
                            p.moves = []
                            return True
                    p.moves = []

        self.squares[initial_pos.rank][initial_pos.file].piece = piece
        self.squares[final_pos.rank][final_pos.file].piece = final_pos_piece
        print('xxx')
        return False

    def calculate_valid_moves(self, piece, rank, file, bool):
        print('calc')

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
                            if not self.in_check(piece, move, initial_pos, final_pos):
                                print('no check')
                                piece.add_move(move)
                        else:
                            print('simulation')
                            piece.add_move(move)

                    # pawn is blocked by piece
                    else:
                        break
                # move is not in range
                else:
                    break

            # diagonal moves
            possible_move_rank = rank + piece.direction
            possible_move_files = [file-1, file+1]

            for possible_move_file in possible_move_files:
                if Square.in_range(possible_move_rank, possible_move_file):
                    if self.squares[possible_move_rank][possible_move_file].occupied_by_opponent(piece.color):
                        initial_pos = Square(rank, file)
                        final_piece = self.squares[possible_move_rank][possible_move_file].piece
                        final_pos = Square(possible_move_rank, possible_move_file, final_piece)

                        move = Move(initial_pos, final_pos)
                        piece.add_move(move)

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
                            piece.add_move(move)
                        elif self.squares[possible_move_rank][possible_move_file].occupied_by_opponent(piece.color):
                            piece.add_move(move)
                            break
                        elif self.squares[possible_move_rank][possible_move_file].occupied_by_teammate(piece.color):
                            break
                    else: break

                    possible_move_rank = possible_move_rank + rank_inc
                    possible_move_file = possible_move_file + file_inc

        def king_moves():
            moves = [
                (rank-1, file-1),
                (rank-1, file+0),
                (rank-1, file+1),
                (rank+1, file-1),
                (rank+1, file+0),
                (rank+1, file+1),
                (rank+0, file-1),
                (rank+0, file+1),
            ]

            for move in moves:
                possible_move_rank, possible_move_file = move
                if Square.in_range(possible_move_rank, possible_move_file):
                    if self.squares[possible_move_rank][possible_move_file].no_friendly_fire(piece.color):

                        initial = Square(rank, file)
                        final = Square(possible_move_rank, possible_move_file)
                        move = Move(initial, final)
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
                                move = Move(initial, final)
                                left_rook.add_move(move)

                                initial = Square(rank, file)
                                final = Square(rank, 2)
                                move = Move(initial, final)
                                piece.add_move(move)

                right_rook = self.squares[rank][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.squares[rank][c].occupied():
                                break
                            if c == 6:
                                print('yes')
                                piece.right_rook = right_rook

                                initial = Square(rank, 7)
                                final = Square(rank, 5)
                                move = Move(initial, final)
                                right_rook.add_move(move)

                                initial = Square(rank, file)
                                final = Square(rank, 6)
                                move = Move(initial, final)
                                piece.add_move(move)

        if isinstance(piece, Pawn): pawn_moves()
        elif isinstance(piece, King): king_moves()
        elif isinstance(piece, Queen): strait_line_moves([
                (-1, 1),
                (-1, -1),
                (1, -1),
                (1, 1),
                (-1, 0),
                (0, 1),
                (0, -1),
                (1, 0)
            ])
        elif isinstance(piece, Bishop): strait_line_moves([
            (-1, 1),
            (-1, -1),
            (1, -1),
            (1, 1)
        ])
        elif isinstance(piece, Knight): knight_moves()
        elif isinstance(piece, Rook): strait_line_moves([
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 0)])

    def add_startposition(self, color):
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


