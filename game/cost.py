from typing import List

from game.player import Player
from game.card import Card


class AbilityCosts(object):
    def __init__(self, costs: List):
        self.raw_costs = costs
        self.costs = []

        for cost in costs:
            cost_instance = create_cost_instance(cost)
            self.costs.append(cost_instance)

    def __str__(self):
        return str(self.raw_costs)

    def check_costs(self, player: Player, card: Card):
        for cost in self.costs:
            cost_check = cost.check_cost(player=player, card=card)
            if not cost_check:
                return False

        return True

    def pay_costs(self, player: Player, card: Card):

        for cost in self.costs:
            cost.pay_cost(player=player, card=card)


class BaseCost(object):
    def pay_cost(self, player: Player, card: Card):
        raise NotImplementedError

    def check_cost(self, player: Player, card: Card):
        raise NotImplementedError


class ManaCost(BaseCost):
    def __init__(self, mana_cost):
        self.mana_cost = mana_cost

    def check_cost(self, player: Player, card: Card):
        return player.mana_pool >= self.mana_cost

    def pay_cost(self, player: Player, card: Card):
        player.mana_pool -= self.mana_cost


class TapCard(BaseCost):
    def __init__(self):
        pass

    def check_cost(self, player: Player, card: Card):
        return card.status == "ready"

    def pay_cost(self, player: Player, card: Card):
        card.status = "tapped"


def create_cost_instance(cost) -> BaseCost:
    if type(cost) == int:
        cost_instance = ManaCost(cost)
    elif cost == "tap_this":
        cost_instance = TapCard()
    else:
        raise ValueError("{} mana cost unknown".format(cost))

    return cost_instance
