import pygame
from global_variables import *
from classes.board import *
from classes.dragger import *


def move_preview_circle_display(screen, dragger):

    if dragger.dragging:
        for move in dragger.piece.moves:
            image_center = (screen_x / 2 - 4 * sqsize) + (move.final_square.file * sqsize) + (sqsize / 2), \
                            (screen_y / 2 - 4 * sqsize) + (move.final_square.rank * sqsize) + (sqsize / 2)
            screen.blit(Piece.circle_image[f'move_preview_circle'],
                        Piece.circle_image[f'move_preview_circle'].get_rect(center=image_center))




