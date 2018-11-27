import logging
import json
from pathlib import Path


logger = logging.getLogger()

CARDS_PATH = Path(Path.cwd(), "cards")


class Card(object):

    def __init__(self, card_id: str):

        self.card_data_file = Path(CARDS_PATH, card_id + ".json")

        with open(self.card_data_file, "r", encoding="utf8") as file:
            card_data = json.load(file)

        self.name = card_data["name"]
        self.status = card_data["status"]
        self.cost = card_data["cost"]
        self.type = card_data["type"]
        self.location = "deck"

    def __str__(self):
        return self.name


class LandCard(Card):

    def __init__(self, card_id: str):
        Card.__init__(self, card_id=card_id)
        with open(self.card_data_file, "r", encoding="utf8") as file:
            card_data = json.load(file)

        self.other_types = card_data["other_types"]
        self.abilities = card_data["abilities"]


class CreatureCard(Card):

    def __init__(self, card_id: str):
        Card.__init__(self, card_id=card_id)
        with open(self.card_data_file, "r", encoding="utf8") as file:
            card_data = json.load(file)

        self.other_types = card_data["other_types"]
        self.abilities = card_data["abilities"]
        self.attack = card_data["attack"]
        self.defense = card_data["defense"]


def create_card_by_type(card: str):
    card_data_file = Path(CARDS_PATH, card + ".json")

    with open(card_data_file, "r", encoding="utf8") as file:
        card_data = json.load(file)

    card_type = card_data["type"]

    if card_type == "land":
        return LandCard(card_id=card)
    elif card_type == "creature":
        return CreatureCard(card_id=card)
