from classes.board import *


def print_current_move(screen, dragger):
    if dragger.clicked:
        color = (186, 202, 68)
        rect = ((screen_x / 2 - 4 * square_size) + dragger.initial_file * square_size,
                (screen_y / 2 - 4 * square_size) + dragger.initial_rank * square_size,
                square_size,
                square_size)
        pygame.draw.rect(screen, color, rect)