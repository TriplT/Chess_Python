from classes.board import *


def print_last_move(screen, board):
    if board.last_move:
        initial = board.last_move.initial_square
        final = board.last_move.final_square

        for pos in [initial, final]:
            color = (186,202,68)
            rect = ((screen_x / 2 - 4 * square_size) + pos.file * square_size,
                    (screen_y / 2 - 4 * square_size) + pos.rank * square_size,
                    square_size,
                    square_size)
            pygame.draw.rect(screen, color, rect)
