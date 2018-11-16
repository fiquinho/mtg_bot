from game.game import MagicGame
from game.player import Player


class Action(object):

    def __init__(self, game: MagicGame, player: Player):

        self.game = game
        self.player = player
