from typing import List

from game.player import Player
from game.card import Card
from game.action import Action, create_action_by_name, DeployLand, NullAction, DeployCreature
from game.cost import AbilityCosts


class Ability(object):

    def __init__(self, player: Player, costs: List,
                 actions: List[Action], card: Card=None):
        self.player = player
        self.costs = AbilityCosts(costs)
        self.actions = actions
        self.card = card

    def __str__(self):
        return "Card: {} - Location: {} - Costs: {} - {}".format(self.card.name,
                                                                 self.card.location,
                                                                 self.costs,
                                                                 str([str(action) for action in self.actions]))

    def check_costs(self):
        return self.costs.check_costs(self.player, self.card)

    def execute(self):
        self.costs.pay_costs(self.player, self.card)

        action_end = None
        for action in self.actions:
            action_end = action.execute()

        return action_end


class Pass(Ability):
    def __init__(self, player: Player):
        Ability.__init__(self, player=player, card=None, costs=[0],
                         actions=[NullAction(player)])

    def __str__(self):
        return "Pass"


class AbilityList(object):

    def __init__(self, actions: List[Ability]):
        self.list = {}
        for i in range(len(actions)):
            self.list[i + 1] = actions[i]

    def __iter__(self):
        for idx, action in self.list.items():
            yield idx, action

    def add_pass(self, player: Player):
        self.list[len(self.list) + 1] = Pass(player=player)


def get_hand_abilities(player: Player) -> List[Ability]:
    hand_abilities = []
    for card in player.hand:
        if card.cost <= player.mana_pool:
            if card.type == "land":
                if player.land_spells > 0:
                    hand_abilities.append(Ability(player=player,
                                                  card=card,
                                                  costs=[card.cost],
                                                  actions=[DeployLand(player, card)]))
            elif card.type == "creature":
                hand_abilities.append(Ability(player=player,
                                              card=card,
                                              costs=[card.cost],
                                              actions=[DeployCreature(player, card)]))

            else:
                pass

    return hand_abilities


def get_lands_actions(player: Player) -> List[Ability]:
    land_actions = []
    for land_card in player.lands:
        for ability in land_card.abilities:
            ability_object = create_card_ability(player, card=land_card, ability_data=ability)

            if ability_object is not None:
                land_actions.append(ability_object)

    return land_actions


def create_card_ability(player: Player, card: Card, ability_data: dict):
    ability_cost = ability_data["cost"]

    actions = []
    for action in ability_data["actions"]:
        actions.append(create_action_by_name(player, action))

    ability = Ability(player=player, costs=ability_cost,
                      actions=actions, card=card)
    check_cost = ability.check_costs()

    if check_cost:
        return ability
    else:
        return None
