import pygame.image

from global_variables import *
from classes.board import *
from classes.dragger import *


def print_pieces(screen, board, dragger):
    for rank in range(ranks):
        for file in range(files):
            if board.squares[rank][file].occupied():
                piece = board.squares[rank][file].piece

                if piece is not dragger.piece:
                    image_center = (screen_x / 2 - 4 * square_size) + (file * square_size) + (square_size / 2), \
                                    (screen_y / 2 - 4 * square_size) + (rank * square_size) + (square_size / 2)
                    piece.img_rect = piece.img.get_rect(center=image_center)
                    screen.blit(piece.img, piece.img_rect)


