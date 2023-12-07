import pygame
from global_variables import *
from classes.board import *
from classes.dragger import *


def move_preview_circle_display(screen, dragger, game):
    if dragger.clicked and game.player_valid_moves:
        moves = []
        for move in game.player_valid_moves:
            if move.initial_square.rank == dragger.initial_rank and move.initial_square.file == dragger.initial_file:
                moves.append(move)
        for m in moves:
            image_center = (screen_x / 2 - 4 * square_size) + (m.final_square.file * square_size) + (square_size / 2), \
                           (screen_y / 2 - 4 * square_size) + (m.final_square.rank * square_size) + (square_size / 2)
            screen.blit(Piece.other_images[f'move_preview_circle'],
                        Piece.other_images[f'move_preview_circle'].get_rect(center=image_center))





