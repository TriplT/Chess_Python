from ..piece import Piece


class Pawn(Piece):
    def __init__(self, color):
        if color == 'white':
            self.direction = -1
        else:
            self.direction = 1

        super().__init__('pawn', color, 1.0)

    def get_move(self, board):
        pass
