from Pycharm_Projects.Chess_Test.data.global_variables import *
from Pycharm_Projects.Chess_Test.data.classes.board import *


class Game:
    player_valid_moves = False

    def __init__(self, board, game_mode='pvp', player='white'):
        self.board = board
        self.game_mode = game_mode
        self.player = player
        self.message = False
        self.game_run_through = 0
        self.white_wins = 0
        self.black_wins = 0
        self.draws = 0

        print(self.player)
        self.calc_player_valid_moves()

    def turn_made(self, board):
        if self.player == 'white':
            self.player = 'black'
        else:
            self.player = 'white'
        if not board.endgame:
            if len(board.piece_positions) <= 15:
                board.endgame = True
        if not board.finishgame:
            if len(board.piece_positions) <= 7:
                board.finishgame = True

    def calc_player_valid_moves(self):
        self.player_valid_moves = self.board.get_valid_moves(self.player)

    def ai_turn(self, board, ai):
        if self.player == ai.color and not board.game_ended and not board.move_played:
            ai.play_moves(board, ai.engine)
            self.turn_made(board)
            if self.game_mode == 'pva':
                self.calc_player_valid_moves()

    # check if self.player is indeed white when white wins or if it already changed to black
    def game_end_100ava(self, board):
        if self.game_run_through <= 99:
            if board.win_message == 'checkmate':
                if self.player == 'black':
                    self.white_wins += 1
                else:
                    self.black_wins += 1
            elif board.win_message == 'stalemate' or board.win_message == 'insufficient material' \
                    or board.win_message == 'repetition' or board.win_message == '50 move-rule':
                self.draws += 1

            if self.game_run_through == 99:
                print(self.game_run_through)
                print(f'white wins: {self.white_wins} draws: {self.draws} black wins: {self.black_wins}')
                self.game_run_through += 1
                self.white_wins = 0
                self.black_wins = 0
                self.draws = 0
                return
            else:
                self.game_run_through += 1
                print(self.game_run_through)
                print(f'white wins: {self.white_wins} draws: {self.draws} black wins: {self.black_wins}')
                board.reset_board()

    def game_end_display(self, screen, message, width, height):

        color_dark_green = (118, 150, 86)
        color_light_green = (238, 238, 210)

        font_1 = pygame.font.SysFont('times new roman', 50)
        font_2 = pygame.font.SysFont('times new roman', 30)

        text = font_1.render(message, True, color_light_green)
        text_rect = text.get_rect(center=(screen_x / 2, int(screen_y / 2 - height / 10)))

        personal_message = 'error'
        if message == 'checkmate':
            if self.player == 'white':
                personal_message = 'black won'
            if self.player == 'black':
                personal_message = 'white won'
        elif message == 'stalemate' or message == 'insufficient material' \
                or message == 'repetition' or message == '50 move-rule':
            personal_message = 'draw'

        text_2 = font_2.render(personal_message, True, color_light_green)
        text_2_rect = text_2.get_rect(center=(screen_x / 2, int(screen_y / 2 + height / 5)))

        pygame.draw.rect(screen, color_dark_green, pygame.Rect(screen_x / 2 - (width / 2), screen_y / 2 - (height / 2), width, height))

        screen.blit(text, text_rect)
        screen.blit(text_2, text_2_rect)

    def check_game_mode_buttons(self, dragger, board, width, height, ai_1, ai_2):
        x_coord = screen_x / 20
        y_coord = screen_y / 2

        if x_coord < dragger.mouseX < (x_coord + width) and y_coord - height - height - (height/4)\
                < dragger.mouseY < (y_coord - height - height - (height/4) + height):
            board.reset_board()
            self.game_mode = 'pvp'
            self.player = 'white'
            ai_1.color = None
            ai_2.color = None
            self.calc_player_valid_moves()
        elif x_coord < dragger.mouseX < (x_coord + width) and y_coord - height - (height / 4) \
                < dragger.mouseY < (y_coord - height - (height / 4) + height):
            board.reset_board()
            self.game_mode = 'pva'
            self.player = 'white'
            ai_1.color = 'black'
            ai_2.color = None
            self.calc_player_valid_moves()
        elif x_coord < dragger.mouseX < (x_coord + width) and y_coord + (height / 4) \
                < dragger.mouseY < (y_coord + (height / 4) + height):
            board.reset_board()
            self.game_mode = 'ava'
            ai_1.color = 'white'
            ai_2.color = 'black'
            self.player = 'white'
        elif x_coord < dragger.mouseX < (x_coord + width) and y_coord + height + (height * 3 / 4) \
                < dragger.mouseY < (y_coord + height + (height * 3 / 4) + height):
            board.reset_board()
            self.game_mode = '100ava'
            self.player = 'white'
            ai_1.color = 'white'
            ai_2.color = 'black'
            self.game_run_through = 0

    @staticmethod
    def draw_game_mode_buttons(screen, width, height):
        x_coord = screen_x / 20
        middle_x_coord = screen_x / 20 + (width / 2)
        y_coord = screen_y / 2

        font = pygame.font.SysFont('times new roman', 50)
        color_dark_green = (118, 150, 86)
        color_light_green = (238, 238, 210)

        top_text = font.render('Player vs Player', True, color_light_green)
        middle_top_text = font.render('Player vs AI', True, color_light_green)
        middle_bottom_text = font.render('AI vs AI', True, color_light_green)
        bottom_text = font.render('100 AI vs AI', True, color_light_green)

        top_text_rect = top_text.get_rect(center=(middle_x_coord, y_coord - height - height - (height/4)))
        middle_top_text_rect = middle_top_text.get_rect(center=(middle_x_coord, y_coord - (height * 3 / 4)))
        middle_bottom_text_rect = middle_bottom_text.get_rect(center=(middle_x_coord, y_coord + (height * 3 / 4)))
        bottom_text_rect = bottom_text.get_rect(center=(middle_x_coord, y_coord + height + height + (height / 4)))

        pygame.draw.rect(screen, color_dark_green, (x_coord, y_coord - height - height - (height * 3 / 4), width, height))
        pygame.draw.rect(screen, color_dark_green, (x_coord, y_coord - height - (height / 4), width, height))
        pygame.draw.rect(screen, color_dark_green, (x_coord, y_coord + (height / 4), width, height))
        pygame.draw.rect(screen, color_dark_green, (x_coord, y_coord + height + (height * 3 / 4), width, height))

        screen.blit(top_text, top_text_rect)
        screen.blit(middle_top_text, middle_top_text_rect)
        screen.blit(middle_bottom_text, middle_bottom_text_rect)
        screen.blit(bottom_text, bottom_text_rect)
