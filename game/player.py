from pathlib import Path

from game.deck import Deck
from game.action import create_action_by_card_type


class Player(object):

    def __init__(self, deck_file: Path, hp: int, name: str):

        self.name = name
        self.deck = Deck(deck_file=deck_file, name="{}_deck".format(name))
        self.health_points = hp

        self.hand = []
        self.lands = []
        self.mana_pool = 0

    def draw_card(self, cards_count: int=1):
        for i in range(cards_count):
            draw_card = self.deck.draw_card()
            self.hand.append(draw_card)

    def get_hand_actions(self, can_play_land: bool):
        hand_actions = []
        for card in self.hand:
            if card.cost <= self.mana_pool:
                if card.type == "land":
                    if can_play_land:
                        hand_actions.append(create_action_by_card_type(card))
                else:
                    hand_actions.append(create_action_by_card_type(card))

        return hand_actions
