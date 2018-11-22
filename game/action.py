from typing import List

from game.card import Card
from game.player import Player


class Action(object):

    def __init__(self, player: Player):
        self.player = player

    def __str__(self):
        raise NotImplementedError


class ActionList(object):

    def __init__(self, actions: List[Action]):
        self.list = {}
        for i in range(len(actions)):
            self.list[i + 1] = actions[i]

    def __iter__(self):
        for idx, action in self.list.items():
            yield idx, action

    def add_pass(self, player: Player):
        self.list[len(self.list) + 1] = NullAction(player=player)


class NullAction(Action):
    def __init__(self, player: Player):
        Action.__init__(self, player=player)

    def __str__(self):
        return "Pass"


class LandSpell(Action):

    def __init__(self, player: Player, land_card: Card):
        Action.__init__(self, player=player)
        self.land_card = land_card

    def __str__(self):
        return "Pay {} mana - Place land in the board".format(self.land_card.cost)


def get_hand_actions(player: Player, can_play_land: bool) -> ActionList:
    hand_actions = []
    for card in player.hand:
        if card.cost <= player.mana_pool:
            if card.type == "land":
                if can_play_land:
                    hand_actions.append(create_action_by_card_type(card=card, player=player))
            else:
                hand_actions.append(create_action_by_card_type(card=card, player=player))

    hand_actions_list = ActionList(actions=hand_actions)

    return hand_actions_list


def create_action_by_card_type(card: Card, player: Player):
    action = None

    if card.type == "land":
        action = LandSpell(land_card=card, player=player)

    if action is None:
        raise ValueError("Error with card type {}".format(card.type))
    return action
