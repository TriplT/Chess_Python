import pygame
from Pycharm_Projects.Chess_Test.data.global_variables import *


class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_rank = 0
        self.initial_file = 0

    def update_blit(self, screen):
        img_center = (self.mouseX, self.mouseY)
        self.piece.img_rect = self.piece.img.get_rect(center=img_center)
        screen.blit(self.piece.img, self.piece.img_rect)

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos

    def save_initial(self, pos):
        self.initial_rank = pos[0]
        self.initial_file = pos[1]

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False


