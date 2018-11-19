import logging

# from game.game import MagicGame as mg
# from game.player import *


logger = logging.getLogger()


class Board(object):

    def __init__(self, game):
        self.game = game
        self.player_1_side = PlayerSide(self.game.player_1)
        self.player_2_side = PlayerSide(self.game.player_2)


class PlayerSide(object):

    def __init__(self, player):
        self.player = player
        self.player.board_assign(self)

        self.lands = []
        self.creatures = []
        self.mana_pool = []

    def available_actions(self):
        for card in self.player.hand:
            if card.playable():
                return
