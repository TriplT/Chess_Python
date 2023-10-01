import pygame
from sys import exit
from get_pygame_pos import get_pygame_pos
from draw_board import draw_board
from print_pieces import print_pieces
from move_preview_circle_display import move_preview_circle_display
from classes.dragger import *
from classes.board import *
from classes.square import *
from classes.piece import *
from classes.move import *


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
    player = 'white'
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
                    clicked_file = int((dragger.mouseX - (screen_x // 2 - 4 * square_size)) // square_size)
                    clicked_rank = int((dragger.mouseY - (screen_y // 2 - 4 * square_size)) // square_size)

                    if board.squares[clicked_rank][clicked_file].occupied():
                        piece = board.squares[clicked_rank][clicked_file].piece
                        if piece.color == player:
                            board.calculate_valid_moves(piece, clicked_rank, clicked_file)
                            dragger.save_initial((clicked_rank, clicked_file))
                            dragger.drag_piece(piece)

            elif event.type == pygame.MOUSEMOTION:
                if dragger.dragging:
                    dragger.update_mouse(event.pos)
                    dragger.update_blit(screen)

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragger.dragging:
                    dragger.update_mouse(event.pos)
                    released_rank = int(dragger.mouseY - (screen_y / 2 - 4 * square_size)) // square_size
                    released_file = int(dragger.mouseX - (screen_x / 2 - 4 * square_size)) // square_size

                    initial = Square(dragger.initial_rank, dragger.initial_file)
                    final = Square(released_rank, released_file)
                    move = Move(initial, final)

                    if board.valid_move(dragger.piece, move):
                        board.move(dragger.piece, move)
                        screen.fill((0, 0, 0))
                        draw_board(screen, square_size)
                        print_pieces(screen, board, dragger)
                        if player == 'white':
                            player = 'black'
                        else:
                            player = 'white'
                dragger.undrag_piece()


            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        move_preview_circle_display(screen, dragger)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
