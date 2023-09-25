import pygame.image

from global_variables import *
from classes.board import *
from classes.dragger import *


def print_pieces(screen, board, dragger):
    for file in range(files):
        for rank in range(ranks):
            if board.squares[file][rank].occupied():
                piece = board.squares[file][rank].piece

                if piece is not dragger.piece:
                    image_topleft = (screen_x / 2 - 4 * sqsize) + (file * sqsize), \
                                    (screen_y / 2 - 4 * sqsize) + (rank * sqsize)
                    piece.img_rect = piece.img.get_rect(topleft=image_topleft)
                    screen.blit(piece.img, piece.img_rect)


