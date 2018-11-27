import logging
import json

from pathlib import Path

from game.player import Player
from game.ability import AbilityList


logger = logging.getLogger()


class GameEngine(object):

    def __init__(self, player_1: Player, player_2: Player):
        self.player_1 = player_1
        self.player_2 = player_2

        self.player_focus = player_1
        self.player_focus_not = player_2

        self.turns_count = 0
        self.game_ended = False

    @staticmethod
    def start_game(game_name: str):
        logger.info("")
        logger.info("")
        logger.info("######################################")
        logger.info("Starting new magic game: {}".format(game_name))
        logger.info("######################################")
        logger.info("")

    @staticmethod
    def print_players_actions(abilities: AbilityList):
        logger.info("   Available abilities:")
        if len(abilities.list) > 0:
            for i, ability in abilities:
                logger.info("       {} _ {}".format(i, ability))

    @staticmethod
    def print_players_hand(player: Player):
        logger.info("   Player hand:")
        for card in player.hand:
            logger.info("       {}".format(card))


class GameConfiguration(object):

    def __init__(self, game_config_dir: Path):

        with open(game_config_dir, "r", encoding="utf8") as file:
            game_config = json.load(file)
        logger.info("Game configurations:")
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
