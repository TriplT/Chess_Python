import pygame
from sys import exit
from get_pygame_pos import get_pygame_pos
from draw_board import draw_board
from print_pieces import print_pieces
from classes.dragger import *
from classes.board import *
from classes.square import *
from classes.piece import *


pygame.init()
screen_x = 1920
screen_y = 1080
square_size = 100
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption('Chess')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)
Piece.preload_images()

def main():

    dragger = Dragger()
    board = Board()
    while True:
        screen.fill((0, 0, 0))
        draw_board(screen, square_size)
        print_pieces(screen, board, dragger)

        if dragger.dragging:
            dragger.update_blit(screen)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                dragger.update_mouse(event.pos)
                if 560 < dragger.mouseX < 1360 and 140 < dragger.mouseY < 940:
                    clicked_file = (dragger.mouseX - (screen_x // 2 - 4 * square_size)) // square_size
                    clicked_rank = (dragger.mouseY - (screen_y // 2 - 4 * square_size)) // square_size

                    if board.squares[clicked_file][clicked_rank].is_occupied():
                        # piece = board.squares[clicked_file][clicked_rank].piece
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(board.squares[clicked_file][clicked_rank].piece)

            elif event.type == pygame.MOUSEMOTION:
                if dragger.dragging:
                    dragger.update_mouse(event.pos)
                    dragger.update_blit(screen)

            elif event.type == pygame.MOUSEBUTTONUP:
                dragger.undrag_piece()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
