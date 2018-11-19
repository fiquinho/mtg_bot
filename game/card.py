import random
import logging
import json
from pathlib import Path
from copy import deepcopy
from pathlib import Path


logger = logging.getLogger()

CARDS_PATH = Path(Path.cwd(), "cards")


class Card(object):

    def __init__(self, id: str):

        self.card_data_file = Path(CARDS_PATH, id + ".json")
        with open(self.card_data_file, "r", encoding="utf8") as file:
            card_data = json.load(file)

        self.name = card_data["name"]
        self.type = card_data["type"]
        self.other_types = card_data["other_types"]
        self.cost = card_data["cost"]
        self.abilities = card_data["abilities"]

    def __str__(self):
        return self.name

    def playable(self, mana_pool: int):
        # TODO: Need to rework this for different mana types
        return self.cost <= mana_pool
