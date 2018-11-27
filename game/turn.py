import logging

from game.game_engine import GameConfiguration, GameEngine
from game.ability import get_hand_abilities, get_board_abilities, AbilityList


logger = logging.getLogger()


class Turn(object):

    def __init__(self, game_engine: GameEngine, game_config: GameConfiguration):
        self.game_engine = game_engine
        self.player = game_engine.player_focus
        self.game_config = game_config
        self.opponent = game_engine.player_focus_not

    def start(self):
        logger.info("")
        logger.info("--------------------------------------")
        logger.info("Started turn [ {} ] for player [ {} ]".format(self.game_engine.turns_count, self.player.name))

        main_phase = MainPhase(self)
        main_phase.start_phase()


class Phase(object):

    def __init__(self, turn: Turn):
        self.turn = turn
        self.name = None

    def start_phase(self):
        raise NotImplementedError

    def get_available_abilities(self):
        abilities_list = get_hand_abilities(player=self.turn.player, phase=self.name)

        board_abilities = get_board_abilities(player=self.turn.player, phase=self.name)
        if len(board_abilities) >= 1:
            abilities_list += board_abilities

        final_abilities_list = AbilityList(abilities_list)
        final_abilities_list.add_pass(player=self.turn.player)
        return final_abilities_list


class MainPhase(Phase):
    def __init__(self, turn: Turn):
        Phase.__init__(self, turn)
        self.name = "main"

    def start_phase(self):
        logger.info("Main phase start - {}".format(self.turn.player.name))
        self.turn.player.refresh_land_spells(lands_turn=self.turn.game_config.lands_turn)

        while True:
            self.turn.game_engine.print_board_state(self.turn.game_engine.player_1,
                                                    self.turn.game_engine.player_2)
            self.turn.game_engine.print_players_hand(self.turn.player)
            available_abilities = self.get_available_abilities()
            self.turn.game_engine.print_players_actions(available_abilities)
            logger.info("{} please select an ability: ".format(self.turn.player.name))

            # Player selection
            while True:
                selection = input("{} please select action: ".format(self.turn.player.name))
                try:
                    selected_ability = available_abilities.list[int(selection)]
                    break
                except KeyError:
                    logger.info("[ {} ] not in available choices".format(selection))

            action_end = selected_ability.execute()

            if action_end is None:
                break



