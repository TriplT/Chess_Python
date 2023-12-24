from ..piece import Piece


class Pawn(Piece):
    def __init__(self, color):
        self.en_passant = False
        self.made_en_passant = False
        if color == 'white':
            self.direction = -1
        else:
            self.direction = 1

        super().__init__('pawn', color, 744)

