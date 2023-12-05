from Pycharm_Projects.Chess_Test.data.classes.board import *


class Player:

    def __init__(self, color):
        self.color = color
        self.left_castling = True
        self.right_castling = True