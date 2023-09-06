class Board:
    def __init__(self, screen):
        self.screen = screen
        self.squares = [[Square((i, j)) for j in range(8)]for i in range(8)]
        self.start_pos()

    def start_pos(self):
        for i in range(8):
            self.squares[i][1].occupying_piece = Pawn((i, 1), 'black', self)
            self.squares[i][6].occupying_piece = Pawn((i, 6), 'white', self)