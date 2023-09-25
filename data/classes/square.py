

class Square:

    def __init__(self, file, rank, piece=None):
        self.file = file
        self.rank = rank
        self.piece = piece

    def occupied(self):
        return self.piece != None

    def occupied_by_noone(self):
        return not self.occupied()

    def occupied_by_teammate(self, color):
        return self.occupied() and self.piece.color == color

    def occupied_by_opponent(self, color):
        return self.occupied() and self.piece.color != color

    def no_friendly_fire(self, color):
        return self.occupied_by_noone() or self.occupied_by_opponent(color)

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or 7 < arg:
                return False

        return True

