import pygame
from global_variables import *
from classes.board import *
from classes.dragger import *


def move_preview_circle_display(screen, dragger, board):
    if dragger.clicked and board.current_moves:
        for move in board.current_moves:
            image_center = (screen_x / 2 - 4 * square_size) + (move.final_square.file * square_size) + (square_size / 2), \
                           (screen_y / 2 - 4 * square_size) + (move.final_square.rank * square_size) + (square_size / 2)
            screen.blit(Piece.other_images[f'move_preview_circle'],
                        Piece.other_images[f'move_preview_circle'].get_rect(center=image_center))





