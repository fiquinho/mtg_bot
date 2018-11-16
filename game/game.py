import logging
import json
from pathlib import Path

from game.deck import Deck
from game.player import Player


logger = logging.getLogger()


class MagicGame(object):

    def __init__(self, game_config_dir: Path, player_1_deck_file: Path,
                 player_2_deck_file: Path):

        logger.info("Initializing new Magic game with configurations:")
        with open(game_config_dir, "r", encoding="utf8") as file:
            game_config = json.load(file)
        for key, value in game_config.items():
            logger.info("{} = {}".format(key, value))

        self.name = game_config["name"]
        self.players_life = game_config["players_life"]
        self.first_draw = game_config["first_draw"]
        self.draw_initial = game_config["draw_initial"]
        self.max_cards_hand = game_config["max_cards_hand"]
        self.top_deck = game_config["top_deck"]
        self.lands_turn = game_config["lands_turn"]

        logger.info("Player 1 will be playing the deck {}".format(player_1_deck_file))
        logger.info("Player 2 will be playing the deck {}".format(player_2_deck_file))

        self.deck_1 = Deck(deck_file=player_1_deck_file, name="p1_deck")
        self.deck_2 = Deck(deck_file=player_2_deck_file, name="p2_deck")

        self.player_1 = Player(deck=self.deck_1, hp=self.players_life)
        self.player_2 = Player(deck=self.deck_2, hp=self.players_life)

        self.turns_count = 0

    def start_game(self):

        # Shuffle the decks
        self.deck_1.shuffle_deck()
        self.deck_2.shuffle_deck()

        self.player_1.draw_card(self.draw_initial)
        self.player_2.draw_card(self.draw_initial)
