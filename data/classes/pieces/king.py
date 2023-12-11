from ..piece import Piece


class King(Piece):
    def __init__(self, color):
        self.left_castling = False
        self.right_castling = False
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', color, 10000.0)
