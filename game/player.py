from pathlib import Path

from game.deck import Deck


class Player(object):

    def __init__(self, deck_file: Path, hp: int, name: str):

        self.name = name
        self.deck = Deck(deck_file=deck_file, name="{}_deck".format(name))
        self.health_points = hp

        self.hand = []
        self.lands = []
        self.mana_pool = 0
        self.land_spells = 0
        self.creatures = []

        self.board = [self.lands, self.creatures]

        self.attacking_creatures = []
        self.blocking_creatures = []

    def draw_card(self, cards_count: int=1):
        for i in range(cards_count):
            draw_card = self.deck.draw_card()
            draw_card.location = "hand"
            self.hand.append(draw_card)

    def refresh_land_spells(self, lands_turn: int):
        self.land_spells = lands_turn

    def untap_lands(self):
        for land_card in self.lands:
            land_card.status = "ready"
