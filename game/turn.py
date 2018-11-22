import logging

from game.game_engine import GameConfiguration, GameEngine
from game.action import get_hand_actions


logger = logging.getLogger()


class Turn(object):

    def __init__(self, game_engine: GameEngine, game_config: GameConfiguration):
        self.game_engine = game_engine
        self.player = game_engine.player_focus
        self.game_config = game_config
        self.opponent = game_engine.player_focus_not

    def start(self):
        logger.info("")
        logger.info("Started turn [ {} ] for player [ {} ]".format(self.game_engine.turns_count, self.player.name))

        main_phase = MainPhase(self)
        main_phase.start_phase()


class Phase(object):

    def __init__(self, turn: Turn):
        self.turn = turn
        self.name = None

    def start_phase(self):
        raise NotImplementedError

    def get_available_actions(self):
        raise NotImplementedError


class MainPhase(Phase):
    def __init__(self, turn: Turn):
        Phase.__init__(self, turn)
        self.name = "main"

    def start_phase(self):
        self.turn.game_engine.print_players_hand(self.turn.player)
        available_actions = self.get_available_actions()
        self.turn.game_engine.print_players_actions(available_actions)

    def get_available_actions(self):
        
        action_list = get_hand_actions(player=self.turn.player,
                                       can_play_land=self.turn.game_config.lands_turn > 0)
        action_list.add_pass()
        return action_list
