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


class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for rank in range(ranks)]
        self.create_squares()
        self.add_startposition('white')
        self.add_startposition('black')

# ersetzt jedes der 64 Nullen vom Board mit actual Square class instances. Also 64 Square classes erstellt
    def create_squares(self):
        for file in range(files):
            for rank in range(ranks):
                self.squares[file][rank] = Square(file, rank)

    # adds starting position to list of lists self.squares (chessboard)
    def add_startposition(self, color):
        if color == 'white':
            rank_pawn, rank_piece = (6, 7)
        else:
            rank_pawn, rank_piece = (1, 0)

        for file in range(files):
            self.squares[file][rank_pawn] = Square(file, rank_pawn, Pawn(color))

        self.squares[1][rank_piece] = Square(1, rank_piece, Knight(color))
        self.squares[6][rank_piece] = Square(6, rank_piece, Knight(color))

        self.squares[2][rank_piece] = Square(2, rank_piece, Bishop(color))
        self.squares[5][rank_piece] = Square(5, rank_piece, Bishop(color))

        self.squares[0][rank_piece] = Square(0, rank_piece, Rook(color))
        self.squares[7][rank_piece] = Square(7, rank_piece, Rook(color))

        self.squares[4][rank_piece] = Square(4, rank_piece, King(color))

        self.squares[3][rank_piece] = Square(3, rank_piece, Queen(color))


