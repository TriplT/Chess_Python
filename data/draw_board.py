import pygame


def draw_board(screen, square_size):
    screen_x = 1920
    screen_y = 1080
    board = pygame.Surface((square_size * 8, square_size * 8))
    board.fill((118, 150, 86))
    for column in range(0, 8):
        if column % 2 == 0:
            for row in range(0, 8, 2):
                pygame.draw.rect(board, (238, 238, 210),
                                 (square_size * column, square_size * row, square_size, square_size))
        else:
            for row in range(1, 9, 2):
                pygame.draw.rect(board, (238, 238, 210),
                                 (square_size * column, square_size * row, square_size, square_size))

    board_rect = board.get_rect()
    board_rect.center = (screen_x / 2, screen_y / 2)
    # board_top_left = (screen_x / 2 - 400, screen_y / 2 - 400)
    screen.blit(board, board_rect)
