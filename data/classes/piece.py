import os
import pygame


class Piece:
    # store scaled images into a dictionary
    piece_images = {}
    other_images = {}

    @classmethod
    def preload_images(cls):

        # chess move preview circle
        img_path = os.path.join(f'images/move_preview_circle.png')
        img = pygame.image.load(img_path).convert_alpha()
        cls.other_images[f'move_preview_circle'] = pygame.transform.smoothscale(img, (100, 100))

        # chess piece images
        for color in ['white', 'black']:
            for name in ['pawn', 'king', 'knight', 'bishop', 'rook', 'queen']:
                image_path = os.path.join(f'images/{color}_{name}.png')
                image = pygame.image.load(image_path).convert_alpha()
                cls.piece_images[f'{color}_{name}'] = pygame.transform.smoothscale(image, (90, 90))

    def __init__(self, name, color, value, img=None, img_rect=None):
        self.name = name
        self.color = color

        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign

        self.pinned = []

        self.preload_images()
        self.img = img
        self.img = self.piece_images[f'{color}_{name}']
        self.img_rect = img_rect

    '''
    # append a move into the self.moves list
    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []
    '''

