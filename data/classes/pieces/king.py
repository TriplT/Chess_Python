from ..piece import Piece


class King(Piece):
    def __init__(self, color):
        self.moved = False
        self.left_castling = True
        self.right_castling = True
        super().__init__('king', color, 10000.0)
