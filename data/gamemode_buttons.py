import global_variables
from global_variables import *


def draw_game_mode_buttons(screen, width, height):
    middleX, middleY = screen_x / 20, screen_y / 2 - (height / 2)
    topX, topY = middleX, middleY - height - (height/2)
    bottomX, bottomY = middleX, middleY + height + height/2

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


def check_game_mode_buttons(dragger, width, height):
    middleX, middleY = screen_x / 20, screen_y / 2 - (height / 2)
    topX, topY = middleX, middleY - height - (height / 2)
    bottomX, bottomY = middleX, middleY + height + (height / 2)

    if topX < dragger.mouseX < (topX + width) and topY < dragger.mouseY < (topY + height):
        return 'pvp'
    elif middleX < dragger.mouseX < (middleX + width) and middleY < dragger.mouseY < (middleY + height):
        return 'pva'
    elif bottomX < dragger.mouseX < (bottomX + width) and bottomY < dragger.mouseY < (bottomY + height):
        return 'ava'


