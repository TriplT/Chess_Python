import os


class Piece:

    def __init__(self, name, color, value, img=None, img_rect=None):
        self.name = name
        self.color = color

        # gibt neg value den gegnerischen pieces und pos den verbündeten. für ai gedacht
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign

        self.moves = []
        self.moved = False

        self.img = img
        self.set_img()
        self.img_rect = img_rect


    def set_img(self):
        self.img = os.path.join(f'images/{self.color}_{self.name}.png')

    # append a move into the self.moves list
    def add_moves(self, move):
        self.moves.append(move)

    King = 1
    Pawn = 2
    Knight = 3
    Bishop = 4
    Rook = 5
    Queen = 6

    White = 8
    Black = 16

    @staticmethod
    def is_colour(piece):
        if piece > 8:
            return True

    @staticmethod
    def get_colour(piece):
        if 7 < piece < 16:
            return 8
        elif 16 < piece < 23:
            return 16
        else:
            return None

    @staticmethod
    def get_piece_type(piece):
        piece_type = piece % 8
        return piece_type



