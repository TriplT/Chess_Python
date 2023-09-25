import pygame
from global_variables import *
from classes.board import *
from classes.dragger import *


def display_moves(screen, dragger):

    if dragger.dragging:
        for move in dragger.piece.moves:
            color = '#C86464' if (move.final_square.file + move.final_square.rank) % 2 == 0 else '#C84646'

            rect = ((1920 / 2 - 4 * sqsize) + move.final_square.file * sqsize,
                    (1080 / 2 - 4 * sqsize) + move.final_square.rank * sqsize, sqsize, sqsize)

            pygame.draw.rect(screen, color, rect)

