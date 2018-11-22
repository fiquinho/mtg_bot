import logging
import json

from pathlib import Path


logger = logging.getLogger()


class GameEngine(object):

    def __init__(self):
        pass


class GameConfiguration(object):

    def __init__(self, game_config_dir: Path):

        with open(game_config_dir, "r", encoding="utf8") as file:
            game_config = json.load(file)
        logger.info("Game configurations:")
        for key, value in game_config.items():
            logger.info("{} = {}".format(key, value))

        for key, value in game_config.items():
            logger.info("{} = {}".format(key, value))

        self.name = game_config["name"]
        self.players_life = game_config["players_life"]
        self.first_draw = game_config["first_draw"]
        self.draw_initial = game_config["draw_initial"]
        self.max_cards_hand = game_config["max_cards_hand"]
        self.top_deck = game_config["top_deck"]
        self.lands_turn = game_config["lands_turn"]

    def __str__(self):
        return "Magic game - {}".format(self.name)
