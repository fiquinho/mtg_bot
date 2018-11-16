import sys
import os
import argparse
import logging
from pathlib import Path

from utils.files_utils import validate_input_file
from game.game import MagicGame


logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(description="Test game mechanics.")

    # Optional arguments
    parser.add_argument("--game_type", default="config/game_normal.json", type=str,
                        help="Path to the game configurations file (.json). "
                             "Defaults to 'config/game_normal.json'.")
    parser.add_argument("--deck_1", default="config/deck_basic.txt", type=str,
                        help="Deck file for player 1 (.txt). "
                             "Defaults to 'config/deck_basic.txt'.")
    parser.add_argument("--deck_2", default="config/deck_basic.txt", type=str,
                        help="Deck file for player 2 (.txt). "
                             "Defaults to 'config/deck_basic.txt'.")

    args = parser.parse_args()

    game_config_file = validate_input_file(file_path=args.game_type, file_types=[".json"])
    player_1_deck_file = validate_input_file(file_path=args.deck_1, file_types=[".txt"])
    player_2_deck_file = validate_input_file(file_path=args.deck_2, file_types=[".txt"])

    MagicGame(game_config_dir=game_config_file,
              player_1_deck_file=player_1_deck_file,
              player_2_deck_file=player_2_deck_file)

if __name__ == '__main__':
    main()
