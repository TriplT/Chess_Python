from ..piece import Piece


class King(Piece):
    def __init__(self, color):
        self.left_castling = True
        self.right_castling = True

        # to give back castling possibilities in unmake move
        self.lost_left_castling = False
        self.lost_right_castling = False

        super().__init__('king', color, 99999.0)
