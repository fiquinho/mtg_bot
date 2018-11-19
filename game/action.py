from game.game import MagicGame
from game.player import Player
from game.card import Card


class Action(object):

    def __init__(self, game: MagicGame, player: Player):

        self.game = game
        self.player = player


class LandSpell(Action):

    def __init__(self, game: MagicGame, player: Player, land_card: Card):
        Action.__init__(self, game, player)
        self.land_card = land_card

    def use(self):
        assert self.player.board_side
