from ..piece import Piece


class King(Piece):
    def __init__(self, color):
        super().__init__('king', color, 100000.0)
