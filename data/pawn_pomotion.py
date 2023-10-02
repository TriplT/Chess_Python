import pygame
from global_variables import *
from classes.board import Board
from classes.square import *
from classes.piece import *
from classes.pieces.pawn import Pawn


def pawn_promotion(screen, piece, last):
    if isinstance(piece, Pawn) and (last.rank == 0 or last.rank == 7):
        # create border
        color = (255, 255, 255) if piece.color == 'white' else (0, 0, 0)
        pygame.draw.rect(screen, color,
                         pygame.Rect((screen_x / 2, screen_y / 2), (2 * square_size + 40, 2 * square_size + 40)))

        # create piece images
        piece_queen_image = Piece.images[f'{piece.color}_queen']
        piece_rook_image = Piece.images[f'{piece.color}_rook']
        piece_bishop_image = Piece.images[f'{piece.color}_bishop']
        piece_knight_image = Piece.images[f'{piece.color}_knight']

        variables = [((screen_x / 2 - 110), (screen_y / 2 - 110)),
                     ((screen_x / 2 + 10), (screen_y / 2 - 110)),
                     ((screen_x / 2 - 110), (screen_y / 2 + 10)),
                     ((screen_x / 2 + 10), (screen_y / 2 + 10))]

        screen.blit(piece_queen_image, piece_queen_image.get_rect(center=variables[0]))

        screen.blit(piece_rook_image, piece_rook_image.get_rect(center=variables[1]))
        screen.blit(piece_bishop_image, piece_bishop_image.get_rect(center=variables[2]))
        screen.blit(piece_knight_image, piece_knight_image.get_rect(center=variables[3]))
