

class Square:

    def __init__(self, rank, file, piece=None):
        self.rank = rank
        self.file = file
        self.piece = piece

    def __eq__(self, other):
        return self.rank == other.rank and self.file == other.file

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

