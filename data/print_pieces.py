import pygame.image

from global_variables import *
from classes.board import *
from classes.dragger import *


def print_pieces(screen, board, dragger):
    for file in range(files):
        for rank in range(ranks):
            if board.squares[file][rank].is_occupied():
                piece = board.squares[file][rank].piece

                if piece is not dragger.piece:
                    image = pygame.image.load(piece.img).convert_alpha()
                    converted_image = pygame.transform.smoothscale(image, (100, 100))
                    image_topleft = (screen_x / 2 - 4 * sqsize) + (file * sqsize), \
                                    (screen_y / 2 - 4 * sqsize) + (rank * sqsize)
                    piece.img_rect = converted_image.get_rect(topleft=image_topleft)
                    screen.blit(converted_image, piece.img_rect)


