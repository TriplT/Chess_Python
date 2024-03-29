import pygame
from sys import exit
from global_variables import *
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
from classes.game import *
from classes.move import *
from classes.sound import *
from classes.AI import *

pygame.init()
screen_x = 1920
screen_y = 1080
square_size = 100
pygame.display.set_caption('Chess')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)
Piece.preload_images()
global game_mode


def main():
    dragger = Dragger()
    board = Board()
    game = Game(board, 'pvp', 'white')
    '''
    AI: 'alea iacta est'
        'ambitious promoter'
        'berserk killer'
        'interstellar calculator'
        'AI annihilator'
        'test'
    '''

    ai_2 = AI('i', 0, 1, None)
    ai_1 = AI('i', 0, 1, None)

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
                game.check_game_mode_buttons(dragger, board, 350, 120, ai_1, ai_2)

                if 560 < dragger.mouseX < 1360 and 140 < dragger.mouseY < 940:
                    clicked_file = int((dragger.mouseX - (screen_x // 2 - 4 * square_size)) // square_size)
                    clicked_rank = int((dragger.mouseY - (screen_y // 2 - 4 * square_size)) // square_size)

                    if not board.game_ended:

                        if board.squares[clicked_rank][clicked_file].no_friendly_fire(game.player) and dragger.clicked:
                            initial = Square(dragger.initial_rank, dragger.initial_file)
                            final = Square(clicked_rank, clicked_file)
                            move = Move(initial, final)

                            if move in game.player_valid_moves:
                                captured = board.squares[clicked_rank][clicked_file].occupied()
                                board.move(board.squares[dragger.initial_rank][dragger.initial_file].piece, move, True, game)
                                Sound().play(captured)
                                screen.fill((0, 0, 0))
                                draw_board(screen)
                                print_last_move(screen, board)
                                print_pieces(screen, board, dragger)
                                game.turn_made(board)
                                game.calc_player_valid_moves()  # calculates the valid moves of the next player

                    if board.squares[clicked_rank][clicked_file].occupied():
                        piece = board.squares[clicked_rank][clicked_file].piece
                        if piece.color == game.player:
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

                    if move in game.player_valid_moves:
                        captured = board.squares[released_rank][released_file].occupied()
                        board.move(dragger.piece, move, True, game)
                        Sound().play(captured)
                        screen.fill((0, 0, 0))
                        draw_board(screen)
                        print_last_move(screen, board)
                        print_pieces(screen, board, dragger)
                        game.turn_made(board)
                        game.calc_player_valid_moves()
                dragger.undrag_piece()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if game.ai_turn(board, ai_1) or game.ai_turn(board, ai_2):
            screen.fill((0, 0, 0))
            draw_board(screen)
            print_last_move(screen, board)
            print_pieces(screen, board, dragger)

        if board.move_played:
            board.game_end(True)
        if board.win_message:
            if game.game_mode == '100ava':
                game.game_end_100ava(board)
            else:
                game.game_end_display(screen, board.win_message, 450, 130)

        move_preview_circle_display(screen, board, dragger, game)
        game.draw_game_mode_buttons(screen, 350, 120)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
