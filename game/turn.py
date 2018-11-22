from game.player import Player
from game.game_engine import GameConfiguration


class Turn(object):

    def __init__(self, player: Player, game_config: GameConfiguration, opponent: Player):
        self.player = player
        self.game_config = game_config
        self.opponent = opponent

    def start(self):
        main_phase = MainPhase(self)


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
        available_actions = self.get_available_actions()

    def get_available_actions(self):
        
        actions = self.turn.player.get_hand_actions(can_play_land=self.turn.game_config.lands_turn > 0)
        return actions