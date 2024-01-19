from ..piece import Piece


class Rook(Piece):
    def __init__(self, color):
        self.made_promotion = False
        super().__init__('rook', color, 5640)
