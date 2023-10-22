from Pycharm_Projects.Chess_Test.data.global_variables import *
from Pycharm_Projects.Chess_Test.data.classes.board import *


class Game:

    def __init__(self, game_mode='pvp', player='white'):
        self.game_mode = game_mode
        self.player = player
        self.message = False

    def turn_made(self):
        if self.player == 'white':
            self.player = 'black'
        else:
            self.player = 'white'

    def check_game_mode_buttons(self, dragger, board, width, height):
        middleX, middleY = screen_x / 20, screen_y / 2 - (height / 2)
        topX, topY = middleX, middleY - height - (height / 2)
        bottomX, bottomY = middleX, middleY + height + (height / 2)

        if topX < dragger.mouseX < (topX + width) and topY < dragger.mouseY < (topY + height):
            board.reset_board()
            board.add_startposition('white')
            board.add_startposition('black')
            self.game_mode = 'pvp'
            self.player = 'white'
        elif middleX < dragger.mouseX < (middleX + width) and middleY < dragger.mouseY < (middleY + height):
            board.reset_board()
            board.add_startposition('white')
            board.add_startposition('black')
            self.game_mode = 'pva'
            self.player = 'white'
        elif bottomX < dragger.mouseX < (bottomX + width) and bottomY < dragger.mouseY < (bottomY + height):
            board.reset_board()
            board.add_startposition('white')
            board.add_startposition('black')
            self.game_mode = 'ava'
            self.player = 'white'

    @staticmethod
    def draw_game_mode_buttons(screen, width, height):
        middleX, middleY = screen_x / 20, screen_y / 2 - (height / 2)
        topX, topY = middleX, middleY - height - (height / 2)
        bottomX, bottomY = middleX, middleY + height + height / 2

        font = pygame.font.SysFont('times new roman', 50)
        color_dark_green = (118, 150, 86)
        color_light_green = (238, 238, 210)

        top_text = font.render('Player vs Player', True, color_light_green)
        middle_text = font.render('Player vs AI', True, color_light_green)
        bottom_text = font.render('AI vs AI', True, color_light_green)

        top_text_rect = top_text.get_rect(center=(topX + (width / 2), topY + (height / 2)))
        middle_text_rect = middle_text.get_rect(center=(middleX + (width / 2), middleY + (height / 2)))
        bottom_text_rect = bottom_text.get_rect(center=(bottomX + (width / 2), bottomY + (height / 2)))

        pygame.draw.rect(screen, color_dark_green, (topX, topY, width, height))
        pygame.draw.rect(screen, color_dark_green, (middleX, middleY, width, height))
        pygame.draw.rect(screen, color_dark_green, (bottomX, bottomY, width, height))

        screen.blit(top_text, top_text_rect)
        screen.blit(middle_text, middle_text_rect)
        screen.blit(bottom_text, bottom_text_rect)

    def game_end_display(self, screen, message, width, height):

        color_dark_green = (118, 150, 86)
        color_light_green = (238, 238, 210)

        font_1 = pygame.font.SysFont('times new roman', 50)
        font_2 = pygame.font.SysFont('times new roman', 30)

        text = font_1.render(message, True, color_light_green)
        text_rect = text.get_rect(center=(screen_x / 2, int(screen_y / 2 - height / 10)))

        print(message)
        personal_message = 'error'
        if message == 'checkmate':
            if self.player == 'white':
                personal_message = 'you lost'
            if self.player == 'black':
                personal_message = 'you won'
        elif message == 'stalemate' or message == 'insufficient material' \
                or message == 'repetition' or message == '50 move-rule':
            personal_message = 'draw'

        text_2 = font_2.render(personal_message, True, color_light_green)
        text_2_rect = text_2.get_rect(center=(screen_x / 2, int(screen_y / 2 + height / 5)))

        pygame.draw.rect(screen, color_dark_green, pygame.Rect(screen_x / 2 - (width / 2), screen_y / 2 - (height / 2), width, height))

        screen.blit(text, text_rect)
        screen.blit(text_2, text_2_rect)







