import random
import logging
from pathlib import Path
from copy import deepcopy

from game.card import Card, create_card_by_type


logger = logging.getLogger()

CARDS_PATH = Path(Path.cwd(), "cards")


class Deck(object):

    def __init__(self, deck_file: Path, name: str):

        self.name = name

        # Load deck list from file and check cards
        self.deck_list = []
        with open(deck_file, "r", encoding="utf8") as file:
            for line in file:
                self.deck_list.append(line[:-1])
        self.check_deck_cards()
        self.deck_list = [create_card_by_type(card_name) for card_name in self.deck_list]

        self.deck_status = deepcopy(self.deck_list)

    def check_deck_cards(self):
        """
        Check that all cards in the deck list are in the database.
        """
        for card in self.deck_list:
            card_path = Path(CARDS_PATH, "{}.json".format(card))
            if not card_path.exists():
                raise FileNotFoundError("The card {} doesn't exists on the database".format(card_path))

    def shuffle_deck(self, seed: int=None):
        """
        Shuffle the deck (self.deck_status).
        """
        if seed is not None:
            random.seed(seed)

        logger.info("Shuffling deck {}".format(self.name))
        random.shuffle(self.deck_status)

    def draw_card(self) -> Card:
        """
        Extract the first card of the deck.

        :return: The top deck card
        """
        draw = self.deck_status.pop(0)
        return draw
