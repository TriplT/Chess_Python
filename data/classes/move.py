class Move:

    def __init__(self, initial_square, final_square, promotion_piece=None):
        self.initial_square = initial_square
        self.final_square = final_square
        self.promotion_piece = promotion_piece

    def __eq__(self, other):
        if other is None:
            return False
        return self.initial_square == other.initial_square and self.final_square == other.final_square
