import os
import pygame


class Piece:

    images = {}

    @classmethod
    def preload_images(cls):
        # store scales images into a dictionary
        for color in ['white', 'black']:
            for name in ['pawn', 'king', 'knight', 'bishop', 'rook', 'queen']:
                img_path = os.path.join(f'images/{color}_{name}.png')
                image = pygame.image.load(img_path).convert_alpha()
                cls.images[f'{color}_{name}'] = pygame.transform.smoothscale(image, (100, 100))

    def __init__(self, name, color, value, img=None, img_rect=None):
        self.name = name
        self.color = color

        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign

        self.moves = []
        self.moved = False

        self.preload_images()
        self.img = img
        self.img = self.images[f'{color}_{name}']
        self.img_rect = img_rect

    # append a move into the self.moves list
    def add_move(self, move):
        self.moves.append(move)
