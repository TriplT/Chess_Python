from ..piece import Piece


class Pawn(Piece):
    def __init__(self, color):
        self.en_passant = False
        if color == 'white':
            self.direction = -1
        else:
            self.direction = 1

        # we also need king half pawns
        super().__init__('pawn', color, 744)

    def get_move(self, board):
        pass
