from ..piece import Piece


class Rook(Piece):
    def __init__(self, color):
        self.moved = False
        super().__init__('rook', color, 5.0)
