from ..piece import Piece


class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5.0)
