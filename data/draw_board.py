import pygame
from classes.square import Square
from global_variables import *


def draw_board(screen):
    screen_x = 1920
    screen_y = 1080
    board = pygame.Surface((square_size * 8, square_size * 8))
    board.fill((118, 150, 86))
    for rank in range(ranks):
        if rank % 2 == 0:
            for file in range(0, 8, 2):
                pygame.draw.rect(board, (238, 238, 210),
                                 (square_size * file, square_size * rank, square_size, square_size))
        else:
            for file in range(1, 9, 2):
                pygame.draw.rect(board, (238, 238, 210),
                                 (square_size * file, square_size * rank, square_size, square_size))

    board_rect = board.get_rect()
    board_rect.center = (screen_x / 2, screen_y / 2)
    screen.blit(board, board_rect)

    for rank in range(ranks):
        for file in range(files):

            if file == 0:
                color = (118, 150, 86) if (rank + file) % 2 == 0 else (255, 255, 255)
                label = pygame.font.SysFont('monospace', 18, bold=True).render(str(ranks-rank), True, color)
                label_pos = ((screen_x / 2 - 4 * square_size) + 5,
                             (screen_y / 2 - 4 * square_size) + 5 + rank * square_size)

                screen.blit(label, label_pos)

            if rank == 7:
                color = (118, 150, 86) if (rank + file) % 2 == 0 else (255, 255, 255)
                label = pygame.font.SysFont('monospace', 18, bold=True).render(Square.get_letter(file), True, color)
                label_pos = ((screen_x / 2 - 4 * square_size) + (file + 1) * square_size - 17,
                             (screen_y / 2 - 4 * square_size) + files * square_size - 20)

                screen.blit(label, label_pos)