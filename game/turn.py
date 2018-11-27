import logging

from game.game_engine import GameConfiguration, GameEngine
from game.ability import get_hand_abilities, get_lands_actions, AbilityList


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
        logger.info("Main phase start - {}".format(self.turn.player.name))
        self.turn.player.refresh_land_spells(lands_turn=self.turn.game_config.lands_turn)

        while True:
            self.turn.game_engine.print_players_hand(self.turn.player)
            available_abilities = self.get_available_actions()
            self.turn.game_engine.print_players_actions(available_abilities)
            logger.info("{} please select action: ".format(self.turn.player.name))

            # Player selection
            while True:
                selection = input("{} please select action: ".format(self.turn.player.name))
                try:
                    selected_action = available_abilities.list[int(selection)]
                    break
                except KeyError:
                    logger.info("[ {} ] not in available choices".format(selection))

            action_end = selected_action.execute()

            if action_end is None:
                break

    def get_available_actions(self) -> AbilityList:
        
        action_list = get_hand_abilities(player=self.turn.player)

        lands_action_list = get_lands_actions(player=self.turn.player)
        if len(lands_action_list) >= 1:
            action_list += lands_action_list

        final_action_list = AbilityList(action_list)
        final_action_list.add_pass(player=self.turn.player)
        return final_action_list
