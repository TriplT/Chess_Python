from ..piece import Piece


class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9.0)
