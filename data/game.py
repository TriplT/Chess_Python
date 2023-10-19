
class Game:

    def __init__(self, game_mode='pvp', player='white'):
        self.game_mode = game_mode
        self.player = player

    def turn_made(self):
        if self.player == 'white':
            self.player = 'black'
        else:
            self.player = 'white'

    def reset_turn(self):
        self.player = 'white'


