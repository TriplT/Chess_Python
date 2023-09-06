from ..piece import Piece


class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 3.0)
