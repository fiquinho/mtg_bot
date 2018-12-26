import logging
import json
from pathlib import Path
from typing import List


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
        self.actions = card_data["actions"]
        self.abilities = card_data["abilities"]

        # Used by some abilities to save the current state of the card (i.e. blocking)
        self.saved_status = None

    def __str__(self):
        return self.name


class LandCard(Card):

    def __init__(self, card_id: str):
        Card.__init__(self, card_id=card_id)
        with open(self.card_data_file, "r", encoding="utf8") as file:
            card_data = json.load(file)

        self.other_types = card_data["other_types"]

        self.available_phases = ["main", "second"]


class CreatureCard(Card):

    def __init__(self, card_id: str):
        Card.__init__(self, card_id=card_id)
        with open(self.card_data_file, "r", encoding="utf8") as file:
            card_data = json.load(file)

        self.other_types = card_data["other_types"]
        self.attack = card_data["attack"]
        self.defense = card_data["defense"]

        self.available_phases = ["main", "second"]

        self.blocking_creatures = []
        self.turn_attack = self.attack
        self.turn_defense = self.defense

    def __str__(self):
        return "{} - Creature {}/{} - Costs {}".format(self.name, self.attack, self.defense, self.cost)

    def reset(self):
        self.turn_attack = self.attack
        self.turn_defense = self.defense

def create_card_by_type(card: str):
    card_data_file = Path(CARDS_PATH, card + ".json")

    with open(card_data_file, "r", encoding="utf8") as file:
        card_data = json.load(file)

    card_type = card_data["type"]

    if card_type == "land":
        return LandCard(card_id=card)
    elif card_type == "creature":
        return CreatureCard(card_id=card)
