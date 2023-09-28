import pygame
from Pycharm_Projects.Chess_Test.data.classes.piece import Piece
from Pycharm_Projects.Chess_Test.data.classes.pieces.pawn import Pawn
from Pycharm_Projects.Chess_Test.data.classes.pieces.king import King
from Pycharm_Projects.Chess_Test.data.classes.pieces.knight import Knight
from Pycharm_Projects.Chess_Test.data.classes.pieces.bishop import Bishop
from Pycharm_Projects.Chess_Test.data.classes.pieces.rook import Rook
from Pycharm_Projects.Chess_Test.data.classes.pieces.queen import Queen
from Pycharm_Projects.Chess_Test.data.classes.square import Square
from Pycharm_Projects.Chess_Test.data.global_variables import *
from Pycharm_Projects.Chess_Test.data.classes.move import Move


class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for rank in range(ranks)]
        self.create_squares()
        self.add_startposition('white')
        self.add_startposition('black')

    def create_squares(self):
        for rank in range(ranks):
            for file in range(files):
                self.squares[rank][file] = Square(rank, file)

    def calculate_valid_moves(self, piece, rank, file):

        def pawn_moves():
            pass

        def king_moves():
            pass

        def queen_moves():
            pass

        def bishop_moves():
            pass

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

                        move = Move(Square(rank, file), Square(move_rank, move_file))
                        piece.add_move(move)




        def rook_moves():
            pass

        if isinstance(piece, Pawn):
            pass
        elif isinstance(piece, King):
            pass
        elif isinstance(piece, Queen):
            pass
        elif isinstance(piece, Bishop):
            pass
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Rook):
            pass

    # adds starting position to list of lists self.squares (chessboard)
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
