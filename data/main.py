import pygame
from sys import exit
from get_pygame_pos import get_pygame_pos
from draw_board import draw_board
from print_pieces import print_pieces
from move_preview_circle_display import move_preview_circle_display
from print_last_move import print_last_move
from print_current_move import print_current_move
from classes.dragger import *
from classes.board import *
from classes.square import *
from classes.piece import *
from classes.move import *
from classes.sound import *


pygame.init()
screen_x = 1920
screen_y = 1080
square_size = 100
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption('Chess')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)

Piece.preload_images()
print('leggo')

def main():
    dragger = Dragger()
    board = Board()
    player = 'white'
    while True:
        screen.fill((0, 0, 0))
        draw_board(screen)
        print_last_move(screen, board)
        print_current_move(screen, dragger)
        print_pieces(screen, board, dragger)

        if dragger.dragging:
            dragger.update_blit(screen)
            dragger.piece_clicked()
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
                            board.calc_current_moves(piece)
                            dragger.save_initial((clicked_rank, clicked_file))
                            dragger.drag_piece(piece)

                    if board.squares[clicked_rank][clicked_file].no_friendly_fire(player) and dragger.clicked:

                        initial = Square(dragger.initial_rank, dragger.initial_file)
                        final = Square(clicked_rank, clicked_file)
                        move = Move(initial, final)

                        if board.valid_current_move(move):
                            captured = board.squares[clicked_rank][clicked_file].occupied()
                            board.move(board.squares[dragger.initial_rank][dragger.initial_file].piece, move)
                            Sound().play(captured)
                            board.calc_current_moves()
                            screen.fill((0, 0, 0))
                            draw_board(screen)
                            print_last_move(screen, board)
                            print_pieces(screen, board, dragger)
                            if player == 'white':
                                player = 'black'
                            else:
                                player = 'white'

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
                        captured = board.squares[released_rank][released_file].occupied()
                        board.move(dragger.piece, move)
                        Sound().play(captured)
                        board.calc_current_moves()
                        screen.fill((0, 0, 0))
                        draw_board(screen)
                        print_last_move(screen, board)
                        print_pieces(screen, board, dragger)
                        if player == 'white':
                            player = 'black'
                        else:
                            player = 'white'
                dragger.undrag_piece()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        move_preview_circle_display(screen, dragger, board)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
