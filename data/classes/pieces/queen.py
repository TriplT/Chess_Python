from ..piece import Piece


class Queen(Piece):
    def __init__(self, color):
        self.made_promotion = False
        super().__init__('queen', color, 14736)
