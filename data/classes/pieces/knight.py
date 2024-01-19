from ..piece import Piece


class Knight(Piece):
    def __init__(self, color):
        self.made_promotion = False
        super().__init__('knight', color, 4152.0)
