import logging
from pathlib import Path

from game.player import Player
from game.game_engine import GameEngine, GameConfiguration
from game.turn import Turn


logger = logging.getLogger()


class MagicGame(object):

    def __init__(self, game_config_dir: Path, player_1_deck_file: Path,
                 player_2_deck_file: Path):

        self.game_engine = GameEngine()

        logger.info("Initializing new Magic game.")
        self.game_config = GameConfiguration(game_config_dir=game_config_dir)

        logger.info("Player 1 will be playing the deck {}".format(player_1_deck_file))
        logger.info("Player 2 will be playing the deck {}".format(player_2_deck_file))

        self.player_1 = Player(deck_file=player_1_deck_file, hp=self.game_config.players_life, name="Player_1")
        self.player_2 = Player(deck_file=player_2_deck_file, hp=self.game_config.players_life, name="Player_2")

        self.turns_count = 0
        self.game_ended = False
        self.player_focus = self.player_1
        self.player_focus_not = self.player_2

    def start_game(self):

        # Shuffle the decks
        self.player_1.deck.shuffle_deck()
        self.player_2.deck.shuffle_deck()

        # Each player draws the first hand
        self.player_1.draw_card(self.game_config.draw_initial)
        self.player_2.draw_card(self.game_config.draw_initial)

        while not self.game_ended:

            turn = Turn(player=self.player_focus, game_config=self.game_config,
                        opponent=self.player_focus_not)
            turn.start()

            if self.turns_count > 25:
                break
            self.turns_count += 1
