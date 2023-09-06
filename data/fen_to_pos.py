from classes.piece import Piece
from classes.board import *


def fen_to_pos(fen):
    piece_type = {
        'k': Piece.King, 'p': Piece.Pawn, 'n': Piece.Knight,
        'b': Piece.Bishop, 'r': Piece.Rook, 'q': Piece.Queen
    }
    fen_string = fen.split('')
    file = 0
    rank = 7

    for char in fen_string:
        if char == '/':
            file = 0
            rank -= 1

        elif char.isdigit():
            file += char

        else:
            Piece.Colour = Piece.White if char.isupper() else Piece.Black
            Piece.Type = piece_type[char]
            board.Squares[rank * 8 + file] = Piece.Colour | Piece.Type
            file += 1
