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

    def change_player_focus(self):
        old_focus = self.player_focus
        self.player_focus = self.player_focus_not
        self.player_focus_not = old_focus

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
        logger.info("")

    @staticmethod
    def print_players_hand(player: Player):
        logger.info("   Player hand:")
        for card in player.hand:
            logger.info("      - {}".format(card))
        logger.info("")

    @staticmethod
    def print_board_state(player_1: Player, player_2: Player):
        logger.info("")
        logger.info("############ Board ############")
        logger.info("#  {} - board".format(player_1.name))
        logger.info("#     - Health points: {}".format(player_1.health_points))
        logger.info("#     - Lands:")
        for land_card in player_1.lands:
            logger.info("#         + {} - {}".format(land_card.name, land_card.status))
        logger.info("#     - Creatures:")
        for creature_card in player_1.creatures:
            logger.info("#         + {} - {}/{} - {}".format(creature_card.name, creature_card.attack,
                                                             creature_card.defense, creature_card.status))
        logger.info("#     - Mana pool = {}".format(player_1.mana_pool))

        logger.info("#  {} - board".format(player_2.name))
        logger.info("#     - Health points: {}".format(player_2.health_points))
        logger.info("#     - Lands:")
        for land_card in player_2.lands:
            logger.info("#         + {} - {}".format(land_card.name, land_card.status))
        logger.info("#     - Creatures:")
        for creature_card in player_2.creatures:
            logger.info("#         + {} - {}/{} - {}".format(creature_card.name, creature_card.attack,
                                                             creature_card.defense, creature_card.status))
        logger.info("#     - Mana pool = {}".format(player_2.mana_pool))
        logger.info("###############################")
        logger.info("")

    @staticmethod
    def print_attacking_creatures(player: Player):
        logger.info("   Attacking creatures:")
        for card in player.attacking_creatures:
            logger.info("      - {}".format(card))
        logger.info("")


class GameConfiguration(object):

    def __init__(self, game_config_dir: Path):

        with open(game_config_dir, "r", encoding="utf8") as file:
            game_config = json.load(file)
        logger.info("Game configurations:")
        for key, value in game_config.items():
            logger.info("   - {} = {}".format(key, value))

        self.name = game_config["name"]
        self.players_life = game_config["players_life"]
        self.first_draw = game_config["first_draw"]
        self.draw_initial = game_config["draw_initial"]
        self.max_cards_hand = game_config["max_cards_hand"]
        self.top_deck = game_config["top_deck"]
        self.lands_turn = game_config["lands_turn"]
        self.shuffle_decks = game_config["shuffle_decks"]

    def __str__(self):
        return "Magic game - {}".format(self.name)
