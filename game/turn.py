import logging

from game.game_engine import GameConfiguration, GameEngine
from game.ability import get_hand_abilities, get_board_abilities, AbilityList
from game.card import CreatureCard


logger = logging.getLogger()


class Turn(object):

    def __init__(self, game_engine: GameEngine, game_config: GameConfiguration):
        self.game_engine = game_engine
        self.player = game_engine.player_focus
        self.game_config = game_config
        self.opponent = game_engine.player_focus_not

    def start(self):

        fmt = logging.Formatter('[ Turn {} start - {} ] %(message)s '.format(self.game_engine.turns_count,
                                                                             self.player.name), '%p')
        logger.handlers[0].setFormatter(fmt)

        logger.info("")
        logger.info("--------------------------------------")
        logger.info("--------------------------------------")

        logger.info("Started turn [ {} ] for player [ {} ]".format(self.game_engine.turns_count, self.player.name))

        main_phase = MainPhase(self)
        main_phase.start_phase()

        attack_phase = AttackPhase(self)
        attack_phase.start_phase()

        second_phase = SecondPhase(self)
        second_phase.start_phase()

    def destroy_creatures(self):
        """
        Destroy any creature on the board that should die
        """

        destroy_creatures = []
        for creature in self.player.creatures:
            if creature.turn_defense <= 0:
                destroy_creatures.append(creature)
        self.player.destroy_creatures(destroy_creatures)

        destroy_creatures = []
        for creature in self.opponent.creatures:
            if creature.turn_defense <= 0:
                destroy_creatures.append(creature)
        self.opponent.destroy_creatures(destroy_creatures)

    def reset_creatures(self):
        self.player.reset_creatures()
        self.opponent.reset_creatures()

    def check_win(self):
        if self.player.health_points <= 0:
            logger.info("{} wins !!".format(self.player.name))
            self.game_engine.game_ended = True
            exit()
        if self.opponent.health_points <= 0:
            logger.info("{} wins !!".format(self.opponent.name))
            self.game_engine.game_ended = True
            exit()


class Phase(object):

    def __init__(self, turn: Turn):
        self.turn = turn
        self.name = None

    def start_phase(self):
        raise NotImplementedError

    def get_available_abilities(self):
        abilities_list = get_hand_abilities(player=self.turn.player, phase=self.name)

        board_abilities = get_board_abilities(player=self.turn.player, phase=self.name, opponent=self.turn.opponent)
        if len(board_abilities) >= 1:
            abilities_list += board_abilities

        final_abilities_list = AbilityList(abilities_list)
        final_abilities_list.add_pass(player=self.turn.player)
        return final_abilities_list


# TODO: Untap and draw phase


class MainPhase(Phase):
    def __init__(self, turn: Turn):
        Phase.__init__(self, turn)
        self.name = "main"

    def start_phase(self):
        fmt = logging.Formatter('[ Turn {} - Main phase - {} ] %(message)s '.format(self.turn.game_engine.turns_count,
                                                                                    self.turn.player.name), '%p')
        logger.handlers[0].setFormatter(fmt)

        logger.info("")
        logger.info("--------------------------------------")
        logger.info("Main phase start - {}".format(self.turn.player.name))
        self.turn.player.refresh_land_spells(lands_turn=self.turn.game_config.lands_turn)
        self.turn.player.untap_lands()
        self.turn.player.untap_creatures()

        while True:
            self.turn.game_engine.print_board_state(self.turn.game_engine.player_1,
                                                    self.turn.game_engine.player_2)
            self.turn.game_engine.print_players_hand(self.turn.player)
            available_abilities = self.get_available_abilities()
            self.turn.game_engine.print_players_actions(available_abilities)

            # Player selection
            while True:
                selection = input("{} please select an ability: ".format(self.turn.player.name))
                try:
                    selected_ability = available_abilities.list[int(selection)]
                    logger.info("Selected ability {}".format(selection))
                    break
                except KeyError:
                    logger.info("[ {} ] not in available choices".format(selection))

            action_end = selected_ability.execute()

            if action_end is None:
                break


class AttackPhase(Phase):
    def __init__(self, turn: Turn):
        Phase.__init__(self, turn)
        self.name = "attack"

    def start_phase(self):
        fmt = logging.Formatter('[ Turn {} - Attack phase - {} ] %(message)s '.format(self.turn.game_engine.turns_count,
                                                                                      self.turn.player.name), '%p')
        logger.handlers[0].setFormatter(fmt)

        logger.info("")
        logger.info("--------------------------------------")
        logger.info("Attack phase start - {}".format(self.turn.player.name))

        while True:
            self.turn.game_engine.print_board_state(self.turn.game_engine.player_1,
                                                    self.turn.game_engine.player_2)

            self.turn.game_engine.print_attacking_creatures(self.turn.player)

            available_abilities = self.get_available_abilities()
            self.turn.game_engine.print_players_actions(available_abilities)

            # Player selection
            while True:
                selection = input("{} please select attacking creature: ".format(self.turn.player.name))
                try:
                    selected_ability = available_abilities.list[int(selection)]
                    logger.info("Selected ability {}".format(selection))
                    break
                except KeyError:
                    logger.info("[ {} ] not in available choices".format(selection))

            action_end = selected_ability.execute()

            if action_end is None:
                break

            if action_end == "attack":
                logger.info("Player 1 attacks with creatures:")
                for attack_creature in self.turn.player.attacking_creatures:
                    logger.info("   - {} - {}/{}".format(attack_creature.name, attack_creature.attack,
                                                         attack_creature.defense))

                block_phase = BlockPhase(self.turn)
                block_phase.start_phase()

                damage_phase = DamagePhase(self.turn)
                damage_phase.start_phase()

                break

    def get_available_abilities(self):
        abilities_list = get_hand_abilities(player=self.turn.player, phase=self.name)

        board_abilities = get_board_abilities(player=self.turn.player, phase=self.name,
                                              opponent=self.turn.opponent)
        if len(board_abilities) >= 1:
            abilities_list += board_abilities

        final_abilities_list = AbilityList(abilities_list)

        if len(self.turn.player.attacking_creatures) > 0:
            final_abilities_list.add_attack(player=self.turn.player)
        else:
            final_abilities_list.add_pass(player=self.turn.player)
        return final_abilities_list


class BlockPhase(Phase):
    def __init__(self, turn: Turn):
        Phase.__init__(self, turn)
        self.name = "block"

    def start_phase(self):
        fmt = logging.Formatter('[ Turn {} - Block phase - {} ] %(message)s '.format(self.turn.game_engine.turns_count,
                                                                                     self.turn.opponent.name), '%p')
        logger.handlers[0].setFormatter(fmt)

        logger.info("")
        logger.info("--------------------------------------")
        logger.info("Block phase start - {}".format(self.turn.opponent.name))

        while True:
            self.turn.game_engine.print_board_state(self.turn.game_engine.player_1,
                                                    self.turn.game_engine.player_2)

            available_abilities = self.get_available_abilities()
            self.turn.game_engine.print_players_actions(available_abilities)

            # Player selection
            while True:
                selection = input("{} please creature to block: ".format(self.turn.opponent.name))
                try:
                    selected_ability = available_abilities.list[int(selection)]
                    break
                except KeyError:
                    logger.info("[ {} ] not in available choices".format(selection))

            action_end = selected_ability.execute()

            if action_end is None:
                break

    def get_available_abilities(self):
        abilities_list = get_hand_abilities(player=self.turn.opponent, phase=self.name)

        board_abilities = get_board_abilities(player=self.turn.opponent, phase=self.name,
                                              opponent=self.turn.player)
        if len(board_abilities) >= 1:
            abilities_list += board_abilities

        final_abilities_list = AbilityList(abilities_list)

        final_abilities_list.add_pass(player=self.turn.opponent)
        return final_abilities_list


class DamagePhase(Phase):
    def __init__(self, turn: Turn):
        Phase.__init__(self, turn)
        self.name = "damage"

    def start_phase(self):
        for creature in self.turn.player.attacking_creatures:
            self.creature_combat(creature)

        self.turn.destroy_creatures()
        self.turn.check_win()
        self.turn.player.clear_attacking_creatures()
        self.turn.reset_creatures()

    def creature_combat(self, creature: CreatureCard):
        total_damage = creature.turn_attack

        if len(creature.blocking_creatures) > 0:
            for blocking_creature in creature.blocking_creatures:
                creature.turn_defense -= blocking_creature.turn_attack

                if blocking_creature.turn_defense >= total_damage:
                    blocking_creature.turn_defense -= total_damage
                    break
                else:
                    total_damage -= blocking_creature.turn_defense
                    blocking_creature.turn_defense = 0
        else:
            self.turn.opponent.health_points -= total_damage


class SecondPhase(Phase):
    def __init__(self, turn: Turn):
        Phase.__init__(self, turn)
        self.name = "second"

    def start_phase(self):
        fmt = logging.Formatter('[ Turn {} - Second phase - {} ] %(message)s '.format(self.turn.game_engine.turns_count,
                                                                                      self.turn.player.name), '%p')
        logger.handlers[0].setFormatter(fmt)

        logger.info("")
        logger.info("--------------------------------------")
        logger.info("Second phase start - {}".format(self.turn.player.name))

        while True:
            self.turn.game_engine.print_board_state(self.turn.game_engine.player_1,
                                                    self.turn.game_engine.player_2)
            self.turn.game_engine.print_players_hand(self.turn.player)
            available_abilities = self.get_available_abilities()
            self.turn.game_engine.print_players_actions(available_abilities)

            # Player selection
            while True:
                selection = input("{} please select ability: ".format(self.turn.player.name))
                try:
                    selected_ability = available_abilities.list[int(selection)]
                    break
                except KeyError:
                    logger.info("[ {} ] not in available choices".format(selection))

            action_end = selected_ability.execute()

            if action_end is None:
                break
