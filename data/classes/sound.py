import pygame


class Sound:

    def __init__(self):
        pygame.mixer.init()

    @staticmethod
    def play(captured):
        if captured:
            pygame.mixer.music.load('sounds/capture.mp3')
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.load('sounds/move-self.mp3')
            pygame.mixer.music.play()
