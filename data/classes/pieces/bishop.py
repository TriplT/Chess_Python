from ..piece import Piece


class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 4848.0)
