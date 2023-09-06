import pygame


class Square:

    def __init__(self, file, rank, piece=None):
        self.file = file
        self.rank = rank
        self.piece = piece

    def is_occupied(self):
        return self.piece != None
